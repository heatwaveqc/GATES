# GATES Wiki — Work Handoff

This file defines what the instruction **"Make the first pass at populating the GATES Wiki"** means.

## Authority and starting points

Work in:

- Repository: `heatwaveqc/GATES`
- Branch: `main`
- Content root: `tiddlers/Content/`
- TiddlyWiki system/chrome root: `tiddlers/System/`
- GitHub is the wiki source of truth. Google Drive remains the source corpus during migration.

Before migrating content, read these Drive documents:

1. **GATES TiddlyWiki Information Architecture**
   - https://docs.google.com/document/d/1cVnfsv6GxPd_tu_Cqkzz5vrVcAxmpQlpYwaCiwAcgvI/edit
2. **GATES TiddlyWiki Migration Procedure**
   - https://docs.google.com/document/d/1cQipf45JVQKtHADn6pSkfpOybPmsPiiKdqjZM82LuPk/edit
3. For Domain/Tradition work, also use **01_GATES_Class_and_Tradition_Engine_Design_Guidelines**
   - Drive ID: `1RGIXSgUR8SmawgQ_Pc238QQubVOgabtXnmoDPJMxjr4`

Current GATES house rules and direct GM rulings override older drafts, archives, and published GURPS rules. Do not infer authority from modification date alone.

## Objective

Create the first usable player-facing vertical slice of the GATES wiki.

The first pass must:

1. create the basic user-facing navigation;
2. migrate the exact pilot content listed below;
3. store rules atomically and assemble readable pages from those pieces;
4. use centralized inheritance instead of copied rules;
5. preserve Player/GM/AI audience separation;
6. validate and build both human-facing wikis;
7. update `migration/FIRST_PASS_MANIFEST.md`;
8. stop before visual redesign or bulk migration.

This is a structural/content pass, not an appearance pass. Do not redesign the theme, typography, colors, or layout beyond minimal navigation and readable assembly.

## Repository placement

Put migrated GATES content under:

`tiddlers/Content/<Section>/`

Use these section directories as needed:

- `tiddlers/Content/Navigation/`
- `tiddlers/Content/Domains/`
- `tiddlers/Content/Species/`
- `tiddlers/Content/Setting/`
- `tiddlers/Content/Gods/`
- `tiddlers/Content/Monsters/`
- `tiddlers/Content/Technology/`
- `tiddlers/Content/Campaigns/`
- `tiddlers/Content/System/`

Dense entities may use subdirectories for source organization. File paths are not semantic; tiddler titles and metadata are authoritative.

Do **not** put ordinary GATES rules in `tiddlers/System/`; that folder is reserved for TiddlyWiki system/chrome tiddlers such as `$:/DefaultTiddlers`.

## Tiddler format

Every classified non-system tiddler must include:

- `title`
- `gates-audience`
- `gates-section`
- `gates-kind`

Use where applicable:

- `gates-parent`
- `gates-stage`
- `tags`
- schema-specific component fields such as `species-component`, `tradition-component`, or `jutsu-component`

Do not invent a `gates-authority` vocabulary during this pass. If authority is uncertain, preserve the source status in the migration manifest and flag it rather than inventing a value.

Use provenance fields on migrated content where practical:

- `source-drive-id`
- `source-drive-title`

Use `type: text/x-markdown` for ordinary prose/component tiddlers. Use TiddlyWiki wikitext for dynamic index/assembly tiddlers when filters, transclusion, or widgets require it.

### Audience rule

- Player-safe rules and setting material: `gates-audience: player`
- Explicit GM-only/secret material: `gates-audience: gm`
- Retrieval, migration, or AI-only instruction: `gates-audience: ai`

If visibility is genuinely ambiguous, fail closed: classify it as `gm` and flag the decision in the manifest rather than exposing it to Player.

## General migration rules

- A Drive file is an input container, not a target wiki page.
- Do not copy large Drive documents wholesale into giant tiddlers.
- Store information as atomically as is useful for searching, reuse, auditing, and inheritance.
- Assemble coherent human-facing pages from the atomic pieces.
- Put a rule at the highest authoritative level that owns it.
- Reference/transclude inherited Tier, Origin, Engine, Domain, or framework rules instead of copying them into every child.
- Do not silently change game mechanics during migration.
- When a lower-level source duplicates a centralized rule, prefer the centralized authoritative rule and record any substantive conflict in the manifest.
- Do not migrate archives/backups merely because they appear in search results.
- Do not migrate design notes/open questions into the Player build unless they are themselves intended player-facing rules.
- When a nonblocking ambiguity appears, make the safest reasonable structural choice, flag it in the manifest, and continue.

## Navigation to create

Update **GATES Home** into the player-facing top-level hub and create section landing pages for:

- Domains
- Species
- Setting
- Gods
- Monsters
- Technology
- Campaigns
- System

Do not make Design or AI Instruction prominent Player navigation.

Each section landing page should be metadata-driven where practical.

Create Setting hub tiddlers for the setting tags used by the pilot content, including at least:

- `Setting: GATES Earth`
- `Setting: Star Wars`
- `Setting: Eternal War`
- `Setting: Stellar Conflict`

Setting membership uses normal tags such as `[[Setting: GATES Earth]]`; do not use `gates-parent` merely for setting membership.

## Exact first-pass content

### Domains

Import these three Domain roots:

1. **Kung Fu**
   - source: `Kung Fu GATES`
   - Drive ID: `138Rw052iOGusYVsBcpDPUZHmtQERXktD95EwqHpBBCI`

2. **Foundational**
   - source: `Foundational Magics GATES`
   - Drive ID: `1H3-_qwSQZWB8bFAvQquusxw5Hf2oM6iJGSskCy8x4Lo`

3. **Eldritch Gifts**
   - source: `Eldritch Gifts Domain GATES`
   - Drive ID: `1_F8il7EGu-k4mOHJwZDx2_7l0EZJPcPFN9QmmACyfSU`

Domain pages should be concise navigation/orientation pages: description, Origin(s), Domain-wide/Core rules or links, and a generated/listed Tradition roster showing Tradition name + concise description + link to full Tradition page. Do not embed every full Tradition on the Domain page.

Import these pilot Traditions:

**Kung Fu**
- Gaoshou
- Shadow Arts

**Foundational**
- Low Magic
- Innovator
- High Magic

**Eldritch Gifts**
- Revelator
- Dreadhound
- Spawn

Tradition pages inherit the Universal Tradition schema plus their Engine schema, Domain rules, Hybrid rules where applicable, and local mechanics.

Do not repeat inherited Engine/Domain text when a centralized tiddler can be referenced or transcluded.

### Recursive Jutsu test

Under **Shadow Arts**, migrate the complete **Water Breathing** institutional Jutsu Tree example.

- The Tree is a Tradition instance, not the Tradition itself.
- The Shadow Arts Tradition must provide a Tree index/list that can eventually contain multiple institutional trees.
- The Water Breathing Tree page assembles its Tree Profile and ordered Jutsu.
- Each Water Breathing Jutsu is its own composite entity.
- Each Jutsu must at minimum expose atomic components for:
  - name
  - cost
  - requirements / Potence
  - prerequisites
  - description/effect
- Preserve tree order as structured metadata or relationship data, not only prose.
- If the same Jutsu relationship needs tree-specific data that cannot safely live on the Jutsu, use an explicit relationship/edge tiddler and record that decision in the manifest.
- Do not import Snake Style in the first pass.

### Species

Source: **GATES Species**
Drive ID: `1al1svM0dKcm4E150iH6LuwUuoPcSZY1LdSZBgy61_C0`

Migrate the central Species framework rules needed by the selected Species, including:

- Species Framework
- Species Types
- Qualification and Attribute Limits
- Unlocks
- Classes and Instruction
- Hybrids and Derived Species

Treat these as centralized `species-rule` material rather than copying them into each Species.

Migrate these four Species:

- Firrerreo
- Perfectly Normal Cat
- Worgen
- Goldblood

Use the Species atomic component schema from the architecture guide. Do not create empty component tiddlers for categories with no content.

### Setting

Migrate:

1. **GATES Earth** setting root from `Setting`
   - Drive ID: `1zk6aHWu3EybLwSeriF_d2EV5DsiQHrVMuw_ZoAzihVA`

2. **France under the Blood Moon**
   - Drive ID: `1dCjSis-3euD-EgTd134vOH33RkIETBaQaHWg9TWhfUM`

3. **The Veltrass System**
   - Drive ID: `1vhe-wZrvUWA8Ow0jvSvGSiSGq9vqVkz9msUYfKFwyLM`

Decompose substantial independently useful setting subjects rather than forcing each source into one monolith. Keep the first pass limited to what is needed to make these three entities coherent and navigable.

### Gods

From **The Celestial Dragons**
Drive ID: `1l9sefqa0UAycpmkxJto9pRPRcPnljvbvBJl1og6DV9M`

Migrate:
- The Celestial Dragons group/index
- The Gold Dragon
- The Jade Dragon

From **Barbarian Gods**
Drive ID: `1IRwsCixEUUTV9yfmF5zjTGoK0kwjqF6cIH9Gs4WU80k`

Migrate:
- Barbarian Gods group/index
- Father Sky
- Friend Darkness

Preserve repeated deity fields such as disposition/nature, Consecration, Oath, Mark/Gifts/Magic where present as atomic components when useful.

### Monsters

From **Undead**
Drive ID: `11QeSCcOb0yhCk71NWp43sPZ3uYGxtRyj1W4LIe2RvCo`

Migrate:
- Undead index/root
- Vampires
- Demon Slayer Demons

From **Demons**
Drive ID: `1X5TQKfcj49zNYiV1jQjy5V28w9n8rtHKh02qBG3ZtnI`

Migrate:
- Demons index/root
- Balseraphs
- Djinn

Do not attempt to migrate the entire monster corpora in this pass.

### Technology

From **GATES Cybernetics Framework**
Drive ID: `1NTr6GTV4QI3BIeH-oShuHraa6VoGIyJLdhcLl3EsWgg`

Migrate:
- a Cybernetics framework/root page with the central rules needed by the pilot entries;
- Tactical Cyber-Eyes;
- Combat Bionic Arm;
- Total Cyborg Body.

From **Chems**
Drive ID: `1yP4YxCaRRroUsORJ-LpOMSEzlGSmLLD2kjMEJxoewe0`

Migrate:
- Chem Design Rules/root;
- Commercial Jet;
- Stimpak;
- Mentats.

Do not import the complete Cybernetics or Chem catalogs.

### Campaigns

Migrate:

1. **Starbucks Adventuring Division**
   - Drive ID: `1SrNtdazV9bEp6sRrr3Ma_t_V-reU0vu9CkQ2T4VlLeM`

2. **Fall of Tokyo — Working Campaign Document**
   - Drive ID: `1-lgMToA6x-oeX-6tzgitobsfoILo5XPOSTVteLDDplI`

For the first pass, make each a coherent campaign root/index. Do not bulk-import every campaign note or player file.

### System

Migrate these central frameworks completely enough to be useful as inherited references:

1. **Godmath**
   - Drive ID: `19-zr0zLjEEanMedfv-lxCbrIByik7-vByLafg4rqU98`

2. **Supernatural Power Abundance (SPA)**
   - Drive ID: `1So1EtjXdwr38tlv4dmA-FZaTZXeh6Xavc9C97Arh3Nc`

3. **GATES Drive and Mark Framework**
   - Drive ID: `1YUpe2p-LSdzFwTplBJ4yG97iAU2gbJFisiYc5pD_sFM`

Split these into independently useful rule tiddlers when the source clearly contains multiple reusable rules. Do not preserve arbitrary Google Doc boundaries merely for convenience.

## Domain/Tradition schema requirements

The baseline human-facing Tradition sections are:

- Description
- Tradition Mechanics
- Tradition Paths
- Mastery Requirements
- Mastery Unlocks
- Examples and Boundaries

The storage underneath may be more atomic.

Engine schemas add only the sections/components that apply to that Engine.

Full Hybrid Traditions inherit the complete schemas of both contributing Engines plus Hybrid integration. Partial Hybrids inherit the complete primary Engine plus only the explicitly selected qualities from the secondary Engine.

Mastery Requirements should preferentially assemble centralized Tier/Origin/Engine/Domain requirements and local Tradition-specific requirements. Unique demonstrations normally remain local.

## Migration manifest

Use `migration/FIRST_PASS_MANIFEST.md`.

For every source/entity, record:

- source title and Drive ID;
- target entity;
- section/kind;
- audience;
- status: Queued / Mapping / Migrating / Validation / Complete / Needs Revisit;
- created tiddlers;
- inherited rules referenced;
- open questions or visibility/authority decisions;
- validation result.

Do not leave the manifest as a plan only; update it as work is completed.

## Build and validation

Before finalizing the first pass:

```bash
node scripts/validate-metadata.js
tiddlywiki . --build player
tiddlywiki . --build gm
```

Verify:

- Player build includes Player material and no GM/AI-only material;
- GM build includes Player + GM material;
- section landing pages resolve;
- Domain pages link to pilot Traditions;
- Species pages assemble their components;
- Water Breathing Tree assembles its Jutsu in correct order;
- Jutsu pages assemble their atomic fields;
- Setting hubs find tagged pilot material;
- inherited rules resolve without copied contradictions;
- all new internal links/transclusions resolve;
- the existing GitHub Actions deploy workflow succeeds.

Published targets are:

- Player root: https://heatwaveqc.github.io/GATES/
- Player explicit: https://heatwaveqc.github.io/GATES/player/
- GM: https://heatwaveqc.github.io/GATES/gm/

## Commit policy

Work directly on `main` unless the user explicitly requests a branch/PR.

Prefer coherent commits, for example:

1. navigation and index infrastructure;
2. Domains/Traditions and Water Breathing recursive test;
3. remaining section pilot imports;
4. validation and cleanup.

Do not combine visual redesign with the migration commits.

## Stop condition

The first pass is complete when:

- the player can navigate Home → Section → Entity → related/child entity without needing Drive;
- all exact pilot entities above have been migrated or explicitly marked Needs Revisit with a concrete reason;
- the recursive Water Breathing structure works;
- centralized inherited rules are being reused rather than copied;
- Player/GM builds validate;
- GitHub Actions succeeds;
- the manifest reflects the final state.

Then stop. Do not begin bulk migration or appearance/style redesign without a new instruction.
