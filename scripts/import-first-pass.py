"""Rebuild the bounded pilot from cached Google Docs paragraph/table responses.

Usage: python scripts/import-first-pass.py /path/to/source-cache
Source caches are intermediate material, deliberately not committed to the wiki.
Every imported atom records source tab/range; migration/SOURCE_MAP.json records hashes.
"""
import json, re, sys, hashlib
from pathlib import Path

SRC = Path(sys.argv[1]); ROOT = Path(__file__).resolve().parents[1]
DATA = {p.stem: json.loads(p.read_text()) for p in SRC.glob('*.json') if not p.stem.endswith('-tables')}
TABLES = {p.stem[:-7]: json.loads(p.read_text()).get('tables', []) for p in SRC.glob('*-tables.json')}
RECORDS=[]; CREATED={}; NOTES=[]
old_inventory=ROOT/'migration/GENERATED_INVENTORY.json'
if old_inventory.exists():
    for item in json.loads(old_inventory.read_text()):
        (ROOT/item['path']).unlink(missing_ok=True)

def slug(s):
    return re.sub(r'[^\w.-]+','_',s,flags=re.UNICODE).strip('_')

def md(ps, key=None):
    out=[]; done=set()
    for p in ps:
        t=p['text'].strip().replace('\x0b','\n'); table=next((x for x in TABLES.get(key,[]) if x['tabId']==p['tabId'] and x['startIndex']<=p['startIndex']<x['endIndex']),None)
        if table:
            tn=table['tableNumber']
            if tn in done: continue
            done.add(tn)
            rows=[['']*table['columnCount'] for _ in range(table['rowCount'])]
            for c in table['cells']:
                rows[c['rowNumber']-1][c['columnNumber']-1]=c['text'].strip().replace('|','\\|').replace('\n','<br>')
            if table['columnCount']==1:
                out.extend(r[0] for r in rows if r[0])
            else:
                out.append('\n'.join(['| '+' | '.join(rows[0])+' |','| '+' | '.join(['---']*len(rows[0]))+' |']+['| '+' | '.join(r)+' |' for r in rows[1:]]))
            continue
        if not t: continue
        if t.startswith('• '): t='- '+t[2:]
        style=p.get('namedStyleType','')
        if style.startswith('HEADING_') and len(t)<140: t='### '+t
        out.append(t)
    return '\n\n'.join(out)

def put(title,section,kind,body='',audience='player',parent=None,key=None,ps=None,fields=None,folder=None,wiki=False):
    f={'title':title,'type':'text/vnd.tiddlywiki' if wiki else 'text/x-markdown','gates-audience':audience,'gates-section':section,'gates-kind':kind}
    if parent: f['gates-parent']=parent
    if key:
        d=DATA[key]; f.update({'source-drive-id':d['documentId'],'source-drive-title':d['title']})
        if ps:
            f.update({'source-tab-id':ps[0]['tabId'],'source-start-index':str(ps[0]['startIndex']),'source-end-index':str(ps[-1]['endIndex'])})
            RECORDS.append({'title':title,'source':key,'driveId':d['documentId'],'revisionId':d.get('revisionId'),'tabId':ps[0]['tabId'],'startIndex':ps[0]['startIndex'],'endIndex':ps[-1]['endIndex'],'sha256':hashlib.sha256('\n'.join(p['text'] for p in ps).encode()).hexdigest()})
    f.update(fields or {})
    dest=ROOT/'tiddlers'/'Content'/(folder or section)/(slug(title)+'.tid')
    if title.startswith('$:/'): dest=ROOT/'tiddlers'/'System'/(slug(title)+'.tid')
    dest.parent.mkdir(parents=True,exist_ok=True)
    dest.write_text('\n'.join(k+': '+str(v).replace('\n',' ') for k,v in f.items())+'\n\n'+body.strip()+'\n')
    CREATED[title]={'path':str(dest.relative_to(ROOT)),'fields':f,'body':body}
    return title

def atom(key,start,end,title,section,kind,parent,order,subtype=None,audience='player',fields=None):
    ps=DATA[key]['paragraphs'][start:end]
    ff={'gates-order':f'{order:04d}','gates-component':'yes','caption':title.split(' — ',1)[-1]}
    if subtype: ff[kind]=subtype
    ff.update(fields or {})
    return put(title,section,kind,md(ps,None if kind=='equipment-component' else key),audience,parent,key,ps,ff)

def root(title,section,kind,description,key=None,parent=None,refs=None,tags=None,audience='player',extra='',fields=None):
    ff={'gates-index':'yes','gates-description':description}
    if refs: ff['gates-inherits']=' '.join('[['+x+']]' for x in refs)
    if tags: ff['tags']=' '.join('[[Setting: '+x+']]' for x in tags)
    ff.update(fields or {})
    body=description+'\n\n{{||$:/GATES/Assembly}}\n\n'+extra
    return put(title,section,kind,body,audience,parent,key,fields=ff,wiki=True)

def sections(key,start,end,parent,section,kind,base=0,subtype=None,audience='player',manual=None):
    ps=DATA[key]['paragraphs']; cuts=manual or [i for i in range(start,end) if ps[i].get('namedStyleType','').startswith('HEADING_') and 0<len(ps[i]['text'].strip())<120]
    cuts=sorted(set([start]+[i for i in cuts if start<=i<end]+[end])); names=[]
    for order,(a,b) in enumerate(zip(cuts,cuts[1:]),base):
        head=ps[a]['text'].strip()
        ishead=(a in (manual or [])) or (ps[a].get('namedStyleType','').startswith('HEADING_') and len(head)<120)
        label=head if ishead else 'Overview'
        label=re.sub(r'^\d+(?:\.\d+)*\.?\s+','',label).strip(': ')
        contentstart=a+1 if ishead else a
        if not any(p['text'].strip() for p in ps[contentstart:b]): continue
        name=parent+' — '+label
        if name in CREATED: name+=' ('+str(order+1)+')'
        names.append(atom(key,contentstart,b,name,section,kind,parent,order,subtype or slug(label).lower().replace('_','-'),audience))
    return names

# Reusable templates. All filters operate on the audience-filtered build.
put('$:/GATES/Assembly','System','template', '''<$let owner=<<currentTiddler>>>
<$list filter="[<owner>has[gates-parent]]" variable="entity">
<p>Parent: <$link to={{!!gates-parent}}><$text text={{!!gates-parent}}/></$link></p>
</$list>
<$list filter="[<owner>get[gates-inherits]enlist-input[]]" variable="inherited">
<$list filter="[<inherited>is[tiddler]]" variable="available">
<details><summary>Shared rules: <$link to=<<inherited>>><$text text=<<inherited>>/></$link></summary>
<$tiddler tiddler=<<inherited>>><$transclude/></$tiddler>
</details>
</$list>
</$list>
<$list filter="[all[tiddlers]field:gates-parent<owner>field:gates-component[yes]sort[gates-order]]">
<section class="gates-component">
<h2><$link><$text text={{!!caption}}/></$link></h2>
<$transclude/>
</section>
</$list>
<$list filter="[all[tiddlers]field:gates-parent<owner>field:gates-index[yes]!field:gates-component[yes]sort[gates-order]]">
<p><$link/> — <$text text={{!!gates-description}}/></p>
</$list>
</$let>''',wiki=True)
put('$:/GATES/SectionIndex','System','template','''<$let section={{!!gates-section}}>
<$list filter="[all[tiddlers]field:gates-section<section>field:gates-index[yes]!field:gates-kind[section-index]!field:gates-component[yes]sort[title]]">
<p><$link/> — <$text text={{!!gates-description}}/></p>
</$list>
</$let>''',wiki=True)
put('$:/GATES/SettingIndex','System','template','''<$let setting=<<currentTiddler>>>
<$list filter="[all[tiddlers]tag<setting>field:gates-index[yes]!field:gates-component[yes]sort[gates-section]]">
<p><$text text={{!!gates-section}}/>: <$link/> — <$text text={{!!gates-description}}/></p>
</$list>
</$let>''',wiki=True)
put('$:/GATES/JutsuTree','System','template','''<$let tree=<<currentTiddler>>>
<$list filter="[all[tiddlers]field:gates-parent<tree>field:gates-kind[jutsu]sort[tree-order]]">
<section><h2><$link/></h2><$transclude/></section>
</$list>
</$let>''',wiki=True)
SECTIONS=['Domains','Species','Setting','Gods','Monsters','Technology','Campaigns','System']
for sec in SECTIONS:
    put(sec,sec,'section-index','Browse '+sec.lower()+'.\n\n{{||$:/GATES/SectionIndex}}',fields={'gates-index':'yes'},folder='Navigation',wiki=True)
home=ROOT/'tiddlers/Content/GATES_Home.tid'
home.write_text('title: GATES Home\ntype: text/vnd.tiddlywiki\ngates-audience: player\ngates-section: System\ngates-kind: navigation\n\nWelcome to GATES: worlds, character options, and rules for play.\n\n'+'\n'.join('* [['+s+']]' for s in SECTIONS)+'\n\n! Browse by setting\n<$list filter="[field:gates-kind[setting-hub]sort[title]]"><p><$link/></p></$list>\n')

# Universal mastery: current authority expressly overrides conflicting local numbers.
root('Mastery Standards','System','rule-hub','Shared numerical Mastery standards. These govern conflicting local numerical benchmarks; local nonnumerical requirements still apply.',key='engine')
# Long first paragraphs are data, never titles.
for i,label in enumerate(['Scope and Precedence','Tier 2','Tier 3','Qualifying Investment','Relevant Governing Traits','Skill-Cap Exception','Preserved Requirements']):
    # replace the auto-split above with stable, concise atoms
    pass
for t in list(CREATED):
    if t.startswith('Mastery Standards —'):
        (ROOT/CREATED[t]['path']).unlink(); del CREATED[t]
RECORDS[:]=[r for r in RECORDS if not r['title'].startswith('Mastery Standards —')]
for n,(i,label) in enumerate(zip(range(343,350),['Scope and Precedence','Tier 2','Tier 3','Qualifying Investment','Relevant Governing Traits','Skill-Cap Exception','Preserved Requirements'])):
    atom('engine',i,i+1,'Mastery Standards — '+label,'System','rule','Mastery Standards',n)
engine_defs={'Regular':(398,425,353),'Ritual':(457,490,355),'Word':(612,699,359),'Psi Talented':(777,821,362),'Atavistic':(1000,1035,371),'Jutsu':(1260,1308,380),'Wuxia':(1308,1389,381)}
for name,(a,b,m) in engine_defs.items():
    title=name+' Engine'
    root(title,'System','engine','Shared '+name+' rules and requirements.',key='engine',refs=['Mastery Standards'])
    # Preserve operational text and construction requirements in separate reader units.
    sections('engine',a+1,b,title,'System','engine-rule')
    atom('engine',m,m+1,title+' — Numerical Mastery','System','rule',title,900)
root('Hybrid Tradition Rules','System','rule-hub','Complete and partial Engine composition.',key='engine')
sections('engine',1656,1670,'Hybrid Tradition Rules','System','rule')
atom('engine',379,380,'Martial Mastery Baseline','System','rule','Mastery Standards',90)

# Domains and their owned rules.
root('Kung Fu','Domains','domain','Martial cultivation through Shido, accelerated training, styles, and institutional Jutsu.',key='kungfu',fields={'gates-origin':'Martial'})
sections('kungfu',16,38,'Kung Fu','Domains','domain-rule')
root('Foundational','Domains','domain',DATA['foundational-core']['paragraphs'][2]['text'],key='foundational-core',fields={'gates-origin':'Occult'})
sections('foundational-core',15,27,'Foundational','Domains','domain-rule')
root('Eldritch Gifts','Domains','domain','A Hybrid Psionic and Super Domain whose Revelations develop latent Gifts.',key='eldritch-core',fields={'gates-origin':'[[Psionic]] [[Super]]'})
sections('eldritch-core',25,76,'Eldritch Gifts','Domains','domain-rule')
domain_refs={d:[t for t,v in CREATED.items() if v['fields'].get('gates-parent')==d and v['fields'].get('gates-kind')=='domain-rule'] for d in ['Kung Fu','Foundational','Eldritch Gifts']}

def tradition(key,start,end,title,domain,engine,tier,origin,instance=None):
    ps=DATA[key]['paragraphs']; desc=next((ps[i+1]['text'] for i in range(start,end-1) if ps[i]['text'].strip()=='Description'),ps[start+2]['text'])
    if title=='Dreadhound': engine='Hunter'
    refs=([engine+' Engine'] if engine+' Engine' in CREATED else ['Mastery Standards'])+domain_refs[domain]
    if origin=='Martial': refs+=['Martial Mastery Baseline']
    if '+' in origin: refs+=['Hybrid Tradition Rules']
    root(title,'Domains','tradition',desc,key=key,parent=domain,refs=refs,fields={'gates-engine':engine,'gates-tier':tier,'gates-origin':origin,'gates-instancing':instance or 'non-instanced'})
    # Keep all selected rules, preserving written Path and local exception wording.
    sections(key,start+2,end,title,'Domains','tradition-component')

tradition('kungfu',38,152,'Gaoshou','Kung Fu','Wuxia',2,'Martial','institutional')
tradition('kungfu',361,418,'Shadow Arts','Kung Fu','Jutsu',2,'Martial','institutional')
for key,title,engine,tier,origin,instance in [('low-magic','Low Magic','Regular',2,'Occult',None),('innovator','Innovator','Ritual',2,'Occult',None),('high-magic','High Magic','Word',3,'Occult',None),('revelator','Revelator','Psi Talented',2,'Psionic','personal'),('dreadhound','Dreadhound','Psi-Hunter',2,'Psionic + Super','personal'),('spawn','Spawn','Atavistic',2,'Super','personal')]:
    tradition(key,0,len(DATA[key]['paragraphs']),title,'Foundational' if origin=='Occult' else 'Eldritch Gifts',engine,tier,origin,instance)

# Complete Water Breathing tree, including the appended Secret Master Technique.
root('Water Breathing','Domains','tradition-instance','An institutional sword-Jutsu lineage. Forms One–Ten are ordinary tree material; Dead Calm is a later Secret Master Technique.',key='kungfu',parent='Shadow Arts',refs=['Jutsu Engine'],fields={'gates-instancing':'institutional'},extra='! Ordered Jutsu\n{{||$:/GATES/JutsuTree}}')
atom('kungfu',419,425,'Water Breathing — Tree Profile','Domains','tree-component','Water Breathing',0)
atom('kungfu',436,437,'Water Breathing — Mastery and Boundaries','Domains','tree-component','Water Breathing',20)
for n,i in enumerate(range(425,436),1):
    p=DATA['kungfu']['paragraphs'][i]; line=p['text']; name=line.split(' — ',1)[0].split('. ',1)[1]
    tail=line.split(' — ',1)[1]
    pre=re.search(r'Prerequisites?: (.*?)\. Minimum Potence',tail).group(1)
    pot=re.search(r'Minimum Potence (\d+)',tail).group(1)
    cost=re.search(r'Cost (\d+) CP',tail).group(1)
    root(name,'Domains','jutsu','Water Breathing form '+str(n)+'.',key='kungfu',parent='Water Breathing',fields={'tree-order':f'{n:02d}','gates-order':f'{n:04d}','jutsu-potence':pot,'jutsu-cost':cost})
    requirements=re.search(r'Minimum Potence .*?\.',tail).group(0)
    pricing=re.search(r'Raw .*?Cost \d+ CP\.',tail).group(0)
    effect=re.sub(r'^Prerequisites?: .*?\. ','',tail).replace(requirements,'').replace(pricing,'').strip()
    for order,(label,sub,body) in enumerate([('Name','name',name),('Cost','cost',pricing),('Requirements','requirements',requirements),('Prerequisites','prerequisites',pre+'.'),('Effect','effect',effect)]):
        put(name+' — '+label,'Domains','jutsu-component',body,parent=name,key='kungfu',ps=[p],fields={'jutsu-component':sub,'gates-component':'yes','caption':label,'gates-order':f'{order:04d}'})

# Species framework and four exact entries.
root('Species Framework','Species','rule-hub','Qualification, point-paid traits, Species types, Unlocks, and Class access.',key='species-framework')
sections('species-framework',1,29,'Species Framework','Species','species-rule')
SPMAP={'overview':'overview','attributes':'attributes','secondary-characteristics-required':'required-secondary-characteristics','advantages-required':'required-advantages','body-plan-and-features-required':'required-features','features-required':'required-features','advantages-optional':'optional-advantages','disadvantages-required':'required-disadvantages','optional-disadvantages':'optional-disadvantages','forbidden-traits':'forbidden-traits','unlocks':'unlocks','classes':'classes','native-society':'native-society','force-sensitivity':'special-rules','rules-clarification':'special-rules','optional-traits':'optional-advantages'}
def species(key,a,b,title,tags,stype='Natural',aud='player'):
    root(title,'Species','species',stype+' Species; traits cost their normal character points.',key=key,refs=['Species Framework'],tags=tags,audience=aud,fields={'species-type':stype})
    made=sections(key,a+1,b,title,'Species','species-component',audience=aud)
    for t in made:
        v=CREATED[t]; sub=v['fields']['species-component']; v['fields']['species-component']=SPMAP.get(sub,'special-rules')
        path=ROOT/v['path']; path.write_text('\n'.join(k+': '+str(x) for k,x in v['fields'].items())+'\n\n'+v['body']+'\n')
species('species-starwars',4,53,'Firrerreo',['Star Wars'])
species('species-animals',1,60,'Perfectly Normal Cat',['Perfectly Normal Earth'])
root('Worgen','Species','species','A Supernatural Modification Species, normally over Human; Gilneas is culture, while the curse is the modification.',key='species-eternal',refs=['Species Framework'],tags=['Eternal War'],fields={'species-type':'Supernatural Modification'})
for a,b,label,sub in [(164,166,'Overview','overview'),(166,167,'Required Traits','special-rules'),(167,168,'Unlocks','unlocks'),(168,169,'Classes','classes'),(169,170,'Culture','native-society')]:
    atom('species-eternal',a,b,'Worgen — '+label,'Species','species-component','Worgen',a,sub)
species('species-goldblood',64,113,'Goldblood',[],aud='gm')
# Goldblood depends on the Standard chassis without importing the entire Species.
for a,b,label,sub in [(23,33,'Standard Required Advantages','required-advantages'),(34,39,'Standard Required Features','required-features'),(40,43,'Standard Optional Traits','optional-advantages'),(54,58,'Standard Forbidden Traits','forbidden-traits')]:
    atom('species-goldblood',a,b,'Reichsmensch Baseline — '+label,'Species','species-rule','Goldblood',a,sub,'gm')
atom('species-goldblood',1,12,'Goldblood — Provisional Context','Species','species-component','Goldblood',0,'special-rules','gm')

# Settings. Preserve explicit provisional status and keep open design questions GM-only.
root('GATES Earth','Setting','world','Earth after the final war and the arrival of the Gates.',key='earth',tags=['GATES Earth'])
atom('earth',1,4,'GATES Earth — The World Ended','Setting','setting-component','GATES Earth',0)
atom('earth',6,14,'GATES Earth — Communications in the Gate Age','Setting','setting-component','GATES Earth',1)
root('France under the Blood Moon','Setting','nation','Provisional setting: a national compact with Niktul renewed through the Blood Moon Hunt.',key='france',tags=['GATES Earth'],refs=['Supernatural Power Abundance','Godmath'])
sections('france',4,93,'France under the Blood Moon','Setting','setting-component')
atom('france',93,108,'France under the Blood Moon — Open Questions','Setting','setting-component','France under the Blood Moon',99,audience='gm')
root('The Veltrass System','Setting','star-system','Planets, orbital zones, settlements, and trade in the Veltrass System.',key='veltrass',tags=['Stellar Conflict'])
vp=DATA['veltrass']['paragraphs']; starts=[i for i,p in enumerate(vp) if ('Planetary Profile:' in p['text'] or 'Orbital Zone Profile:' in p['text']) and p.get('namedStyleType','').startswith('HEADING_')]
for a,b in zip(starts,starts[1:]+[len(vp)]):
    name=vp[a]['text'].split('Profile: ',1)[1]
    root(name,'Setting','orbital-zone' if 'Belt' in name else 'planet', 'Veltrass system profile.',key='veltrass',parent='The Veltrass System',tags=['Stellar Conflict'],fields={'gates-order':f'{a:04d}'})
    made=sections('veltrass',a+1,b,name,'Setting','setting-component')
    for t in made:
        v=CREATED[t]
        if 'secretly benefit' in v['body']:
            v['fields']['gates-audience']='gm'
            (ROOT/v['path']).write_text('\n'.join(k+': '+str(x) for k,x in v['fields'].items())+'\n\n'+v['body']+'\n')

# Gods: only selected deities; unfinished gift mechanics are preserved as unresolved.
root('The Celestial Dragons','Gods','pantheon',DATA['dragons']['paragraphs'][1]['text'],key='dragons',refs=['Godmath'])
atom('dragons',3,4,'The Celestial Dragons — Consecrations, Oaths, and Gifts','Gods','god-rule','The Celestial Dragons',0)
for a,title in [(4,'The Gold Dragon'),(25,'The Jade Dragon')]:
    root(title,'Gods','god',DATA['dragons']['paragraphs'][a+1]['text'],key='dragons',parent='The Celestial Dragons',refs=['The Celestial Dragons — Consecrations, Oaths, and Gifts'])
    for i in range(a+1,a+7):
        label=DATA['dragons']['paragraphs'][i]['text'].split(':',1)[0]
        atom('dragons',i,i+1,title+' — '+label,'Gods','god-component',title,i)
root('Barbarian Gods','Gods','pantheon','Go out. Settle lands. Do stuff.',key='barbarian',refs=['Godmath'])
atom('barbarian',4,9,'Barbarian Gods — Holidays','Gods','god-rule','Barbarian Gods',0)
for title,a,b in [('Father Sky',11,16),('Friend Darkness',36,47)]:
    root(title,'Gods','god','A deity of the Barbarian Gods; the source contains unfinished Gifts.',key='barbarian',parent='Barbarian Gods')
    for i in range(a,b):
        p=DATA['barbarian']['paragraphs'][i]; t=p['text'].strip()
        if t.endswith(':') or t in ['Drives']: continue
        label=t.split(':',1)[0] if ':' in t else 'Drive '+str(i-40)
        atom('barbarian',i,i+1,title+' — '+label,'Gods','god-component',title,i)

# Monster source documents contain only names, no profiles or hyperlinks.
for title,key,names in [('Undead','undead',['Vampires','Demon Slayer Demons']),('Demons','demons',['Balseraphs','Djinn'])]:
    root(title,'Monsters','monster-group','Source outline; creature mechanics are not yet supplied.',key=key,audience='gm')
    for name in names:
        root(name,'Monsters','monster','The selected source lists this name but supplies no usable profile. Needs source completion.',key=key,parent=title,audience='gm',fields={'gates-stage':'concept'})

# Cybernetics: operational framework slices and GATES override appendix, no bulk catalog.
root('Cybernetics','Technology','technology-framework','Character traits with technological logistics. The GATES Setting Rules below override the setting-neutral baseline.',key='cybernetics')
for a,b,label in [(91,130,'Quick Start'),(145,271,'Classes and Functions'),(271,426,'Access and Facilities'),(426,530,'Procedures'),(530,803,'Limitations, Power, and Maintenance'),(803,856,'Strength and Support'),(1025,1078,'Sensory Access'),(1204,1267,'Armor and Survivability'),(3335,3376,'GATES Setting Rules')]:
    hub='Cybernetics — '+label
    root(hub,'Technology','rule-hub','Shared cybernetics '+label.lower()+'.',key='cybernetics',parent='Cybernetics',fields={'gates-component':'yes','caption':label,'gates-order':f'{a:04d}'})
    sections('cybernetics',a+1,b,hub,'Technology','technology-rule')
for a,title in [(2182,'Tactical Cyber-Eyes'),(2366,'Combat Bionic Arm'),(2574,'Total Cyborg Body')]:
    ps=DATA['cybernetics']['paragraphs']
    root(title,'Technology','equipment',ps[a+11]['text'],key='cybernetics',parent='Cybernetics',refs=['Cybernetics — GATES Setting Rules'])
    # Explicitly reconstruct the catalog card fields from the verified table layout.
    for order,(label,inds) in enumerate([('Profile',list(range(a+1,a+7))),('Procedure',[a+10]),('Traits',[a+11]),('Limits',[a+12]),('Power and Repair',[a+13]),('Use and Upgrade',[a+14])]):
        atom('cybernetics',inds[0],inds[-1]+1,title+' — '+label,'Technology','equipment-component',title,order)

root('Chem Design Rules','Technology','technology-framework','Chem targets, effects, duration, addiction, production, clearance, and overdose.',key='chem-rules')
sections('chem-rules',1,445,'Chem Design Rules','Technology','technology-rule')
for a,b,title in [(5,17,'Commercial Jet'),(138,150,'Stimpak'),(259,271,'Mentats')]:
    root(title,'Technology','equipment','Chem catalog entry; apply shared dosage, clearance, and overdose rules.',key='chem-catalog',parent='Chem Design Rules',refs=['Chem Design Rules'])
    for i in range(a+1,b):
        t=DATA['chem-catalog']['paragraphs'][i]['text']; label=t.split(':',1)[0] if ':' in t else 'Profile'
        if len(label)>80: label='Profile'
        name=title+' — '+label
        if name in CREATED: name+=' '+str(i-a)
        atom('chem-catalog',i,i+1,name,'Technology','equipment-component',title,i-a)

# Campaign hubs: readable operational material, hidden event details fail closed.
root('Starbucks Adventuring Division','Campaigns','campaign','Contractor ranks, missions, and field references.',key='starbucks',tags=['Stellar Conflict'],extra='Related setting: [[The Veltrass System]].')
for i,label in [(1,'Field Operator Ranks'),(2,'Mission Progression'),(3,'Rank Tests'),(5,'Expected Combat'),(6,'Teams and Rank Maintenance'),(7,'Accepting Missions'),(8,'Badges and Conduct'),(9,'Accounts and Benefits')]:
    atom('starbucks-handbook',i,i+1,'Starbucks Adventuring Division — '+label,'Campaigns','campaign-component','Starbucks Adventuring Division',i)
atom('starbucks-handbook',4,5,'Starbucks Adventuring Division — Source Pay Schedule','Campaigns','campaign-component','Starbucks Adventuring Division',90,audience='gm')
root('Starbucks — Vampire Field Manual','Campaigns','field-guide','In-universe contractor guidance; vulnerabilities vary by vampire type.',key='starbucks',parent='Starbucks Adventuring Division')
sections('starbucks',3,106,'Starbucks — Vampire Field Manual','Campaigns','campaign-component')
root('Fall of Tokyo','Campaigns','campaign','Furui Tokyo faces a major interdimensional disaster.',key='tokyo',tags=['GATES Earth'])
atom('tokyo',17,23,'Fall of Tokyo — City Baseline','Campaigns','campaign-component','Fall of Tokyo',0)
tp=DATA['tokyo']['paragraphs']; cuts=[i for i,p in enumerate(tp) if re.match(r'^\d+\. ',p['text']) and len(p['text'])<100]
sections('tokyo',23,len(tp),'Fall of Tokyo','Campaigns','campaign-component',base=10,audience='gm',manual=cuts)

# Central System frameworks.
root('Godmath','System','rule-hub','Gods, Demon Lords, souls, worship, afterlives, and divine advancement. Incomplete source options remain GM-only.',key='godmath')
gp=DATA['godmath']['paragraphs']
for a,b,label,aud in [(1,5,'Godhood and Choice','gm'),(6,12,'Godsoul and Divine Ranks','player'),(12,14,'Unfinished Divine Ranks','gm'),(14,15,'Afterlife Capacity','player'),(15,16,'Demon Lords','player'),(16,17,'Great Demon Lord Draft','gm'),(17,18,'Divine Servitors','player'),(18,19,'Demonic Minions','gm'),(21,23,'Champions','player'),(24,27,'Seedlings','player'),(28,31,'Clergy','player'),(32,33,'Priests','player'),(34,35,'Clerics','player'),(36,37,'Prophets','player'),(38,39,'Summoners','player'),(40,41,'Archivists','player'),(42,43,'Channels','player'),(44,45,'Paladins','player'),(46,47,'Heroes Draft','gm'),(49,51,'Soul Identity','player'),(51,54,'Creating and Classifying Souls','player'),(55,60,'Divine Experience','player'),(60,65,'Demon Lord Worked Example','gm'),(67,70,'Death and Fetters','player'),(71,72,'Wraiths and the Shadow','player'),(73,74,'Destruction and Recoalescence','player')]:
    atom('godmath',a,b,'Godmath — '+label,'System','rule','Godmath',a,audience=aud)
# Original first-person campaign examples and unfinished options are GM context.
for title,v in list(CREATED.items()):
    if v['fields'].get('source-drive-id')==DATA['godmath']['documentId'] and v['fields'].get('gates-component'):
        if any(s in v['body'] for s in ['like me or James','we are all currently','Great Demon Lord (Unusual','Greatest God:','Cosmic Divinity:']):
            v['fields']['gates-audience']='gm'
            (ROOT/v['path']).write_text('\n'.join(k+': '+str(x) for k,x in v['fields'].items())+'\n\n'+v['body']+'\n')
root('Supernatural Power Abundance','System','rule-hub','SPA/SPAA scaling and the rules preventing double multiplication.',key='spa')
for a,b,label in [(0,8,'Basic Scaling'),(8,12,'Martial and Psionic Scope'),(13,15,'Calculation Order'),(15,20,'Bane Bridge'),(20,26,'Worked Comparisons'),(26,28,'Weakness and Vulnerability')]:
    atom('spa',a,b,'Supernatural Power Abundance — '+label,'System','rule','Supernatural Power Abundance',a)
root('GATES Drive and Mark Framework','System','rule-hub','Campaign configuration, Drive sources, Marks, conversion, and optional prestige.',key='drive-mark')
sections('drive-mark',1,160,'GATES Drive and Mark Framework','System','rule')

for setting in ['GATES Earth','Star Wars','Eternal War','Stellar Conflict','Perfectly Normal Earth']:
    put('Setting: '+setting,'Setting','setting-hub','Browse '+setting+'.\n\n{{||$:/GATES/SettingIndex}}',fields={'gates-index':'yes'},folder='Navigation',wiki=True)

# Metadata + exact source map for repeatable review.
(ROOT/'migration/SOURCE_MAP.json').write_text(json.dumps(RECORDS,ensure_ascii=False,indent=2)+'\n')
(ROOT/'migration/GENERATED_INVENTORY.json').write_text(json.dumps([{ 'title':t, 'path':v['path'], 'audience':v['fields']['gates-audience'],'kind':v['fields']['gates-kind'],'parent':v['fields'].get('gates-parent')} for t,v in CREATED.items()],ensure_ascii=False,indent=2)+'\n')
print(f'Generated {len(CREATED)} tiddlers and {len(RECORDS)} source mappings.')
