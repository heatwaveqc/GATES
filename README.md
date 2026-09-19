# GATES

A GURPS Fourth Edition interdimensional post-apocalyptic setting built as a
TiddlyWiki with git as the source of truth.

## Audience builds

The repository generates two human-facing wikis:

- **Player:** includes only `gates-audience: player`
- **GM:** includes `player` + `gm`
- **AI:** source-level instruction/retrieval material; not included in either human build

The Player build is published at the GitHub Pages root and under `/player/`.
The GM build is published under `/gm/`.

Audience inheritance is:

```
Player ⊂ GM ⊂ AI
```

Unclassified legacy tiddlers fail closed: they are excluded from both human builds
until migration assigns their metadata.

## Foundation metadata

A classified GATES tiddler must provide:

- `gates-audience` — `player`, `gm`, or `ai`
- `gates-section` — Campaigns, System, Design, Domains, Gods, Monsters,
  Setting, Species, Technology, AI Instruction, or Art
- `gates-kind` — section-specific object type

Reserved structural fields:

- `gates-parent` — direct structural parent
- `gates-stage` — normalized Concept → Usable → Complete → Audited → Final
- `gates-authority` — rules/canon authority, vocabulary still being reconciled
- `tags` — free semantic relationships

The detailed architecture lives in the Drive Design document
**GATES TiddlyWiki Information Architecture**.

## Structural rule

Sections are broad organizational buckets. Kinds describe what an object is.
Parent relationships create the direct hierarchy. Tags describe semantic relationships.

For example:

```
Kung Fu
└── Gaoshou
    └── Tiger and Phoenix Style
```

would use `gates-parent: Kung Fu` on Gaoshou and
`gates-parent: Gaoshou` on Tiger and Phoenix Style.

## Repository layout

- `tiddlywiki.info` — Player and GM build targets
- `scripts/validate-metadata.js` — validates classified tiddler metadata
- `tiddlers/System/` — TiddlyWiki system/chrome tiddlers
- `tiddlers/Content/` — GATES content and migration seeds
- `static/` — generated output; gitignored

## Local use

```
npm install -g tiddlywiki
node scripts/validate-metadata.js
tiddlywiki . --build player
tiddlywiki . --build gm
```

To preview the complete source wiki rather than an audience-filtered build:

```
tiddlywiki . --listen
```

## Migration principle

Do not automatically copy large Drive documents into single giant tiddlers.
Prefer small, linked units that are useful independently. This is both better
for human navigation and safer for targeted LLM retrieval.

## Work migration handoff

The canonical execution contract for the first population pass is
[`WORK_HANDOFF.md`](WORK_HANDOFF.md). The queued execution checklist is
[`migration/FIRST_PASS_MANIFEST.md`](migration/FIRST_PASS_MANIFEST.md).

When the user says **"Make the first pass at populating the GATES Wiki"**, use
`WORK_HANDOFF.md` as the operational specification. It defines the exact pilot
entities, source Drive IDs, target repository paths, audience behavior, recursive
Jutsu test, validation commands, commit policy, and stop condition.

Do not substitute a broad Drive crawl, bulk migration, or visual redesign for that
bounded first pass.
