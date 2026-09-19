// Run after both builds. Uses the same TiddlyWiki version as the build.
const fs = require('fs');
const path = require('path');
const assert = require('assert');
const tw = require('tiddlywiki').TiddlyWiki();
tw.boot.argv = ['.']; tw.boot.boot();
const wiki=tw.wiki;
const inventory=JSON.parse(fs.readFileSync('migration/GENERATED_INVENTORY.json','utf8'));
for(const item of inventory) {
  const f=wiki.getTiddler(item.title)?.fields;
  assert(f,`Missing ${item.title}`);
  if(f['gates-parent']) assert(wiki.tiddlerExists(f['gates-parent']),`Missing parent: ${item.title}`);
  for(const r of tw.utils.parseStringArray(f['gates-inherits']||'')) assert(wiki.tiddlerExists(r),`Missing inherited rule ${r}`);
  if(f['gates-index']==='yes') {
    const rendered=wiki.renderTiddler('text/html',item.title,{variables:{currentTiddler:item.title}});
    assert(!rendered.includes('tc-error'),`Render error: ${item.title}`);
    assert(!rendered.includes('tc-tiddlylink-missing'),`Broken link: ${item.title}`);
  }
}
const forms=wiki.filterTiddlers('[field:gates-parent[Water Breathing]field:gates-kind[jutsu]sort[tree-order]]');
assert.equal(forms.length,11);
const costs=[];
for(const [i,t] of forms.entries()) {
  const f=wiki.getTiddler(t).fields;
  assert.equal(Number(f['tree-order']),i+1);
  const parts=wiki.filterTiddlers(`[field:gates-parent[${t}]field:gates-kind[jutsu-component]]`).map(x=>wiki.getTiddler(x).fields['jutsu-component']);
  assert.deepEqual(parts.sort(),['cost','effect','name','prerequisites','requirements']);
  costs.push(Number(f['jutsu-cost']));
}
assert.equal(costs.slice(0,10).reduce((a,b)=>a+b,0),60);
assert.equal(costs[10],2);
const tree=wiki.renderTiddler('text/html','Water Breathing',{variables:{currentTiddler:'Water Breathing'}});
assert(tree.includes('absolute defensive stillness'));
assert(tree.includes('Martial Delivery through one sword attack'));
assert.equal(wiki.filterTiddlers('[field:gates-parent[The Veltrass System]field:gates-index[yes]]').length,9);
for(const setting of ['GATES Earth','Star Wars','Eternal War','Stellar Conflict']) {
  assert(wiki.tiddlerExists('Setting: '+setting));
  assert(wiki.filterTiddlers(`[tag[Setting: ${setting}]field:gates-index[yes]]`).length,`Empty setting ${setting}`);
}
function buildStore(file) {
  const html=fs.readFileSync(file,'utf8');
  const match=html.match(/<script[^>]*class="tiddlywiki-tiddler-store"[^>]*>([\s\S]*?)<\/script>/);
  assert(match,`Missing JSON store ${file}`);
  return new Map(JSON.parse(match[1]).map(t=>[t.title,t]));
}
const player=buildStore('static/player/index.html'), gm=buildStore('static/gm/index.html');
for(const [title,t] of player) if(!title.startsWith('$:/')) assert.equal(t['gates-audience'],'player',`Player leakage: ${title}`);
for(const [title,t] of gm) if(!title.startsWith('$:/')) assert(['player','gm'].includes(t['gates-audience']),`GM leakage: ${title}`);
for(const item of inventory.filter(i=>!i.title.startsWith('$:/'))) {
  assert.equal(player.has(item.title),item.audience==='player',`Player membership: ${item.title}`);
  assert.equal(gm.has(item.title),['player','gm'].includes(item.audience),`GM membership: ${item.title}`);
}
assert(!player.has('Goldblood')); assert(gm.has('Goldblood'));
console.log(`First pass verified: ${inventory.length} generated tiddlers; 11 ordered composite Jutsu; ${player.size} Player and ${gm.size} GM stored tiddlers.`);
