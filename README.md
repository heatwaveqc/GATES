# GATES

A GURPS Fourth Edition interdimensional post-apocalyptic setting, run as a
[TiddlyWiki](https://tiddlywiki.com/) with git as the backend.

## How this repo is organized

- `tiddlywiki.info` — the wiki's build config (plugins, themes, static build target).
- `tiddlers/System/` — wiki chrome (site title, default tiddlers, etc.).
- `tiddlers/Content/` — the actual GATES rules, setting, and reference material,
  one tiddler (`.tid` file) per document.

Each content tiddler carries a few custom fields for tracking migration and authority:

- `gates-status` — Canon / Canon, incomplete / Provisional / Reference / Deprecated / Archive,
  matching the status labels defined in `00_GATES_Master_Design`.
- `gates-import-status` — whether this tiddler holds the full source document yet,
  or is a placeholder/partial seed pending a follow-up import pass.
- `gates-source` — where the content came from in the old Google Drive library,
  for traceability during migration.
- `gates-visibility` — set to `gm-only` on tooling/meta notes that should never
  ship in a player-facing build (e.g. connector diagnostics).

## Editing model

This repo is the single source of truth. There is intentionally no live,
browser-editable TiddlyWiki server for this project — all edits happen as
git commits, authored either directly or through an LLM (Claude) with file
access to a local clone. Google Drive holds a synced, read-only mirror of
this folder for casual browsing and extra redundancy; it is never the
source of edits.

**Two audiences, one repo:**
- **GMs** get the full editable source — every tiddler, including
  Provisional/Draft/incomplete material and GM-only tooling notes.
- **Players** get a static, read-only build generated from the subset of
  tiddlers that are Canon/Reference and not marked `gm-only`.

## Running it locally

```
npm install -g tiddlywiki
tiddlywiki . --listen
```

Then open `http://127.0.0.1:8080` to browse/edit in a real TiddlyWiki
interface (useful for spot-checking the migration; ongoing edits still go
through git as described above).

To produce a static export:

```
tiddlywiki . --build index
```

This writes a self-contained `static/index.html` — the file a read-only
GitHub Pages deploy would serve to players.

## Migration status

This is an in-progress migration from a Google Drive library of Google Docs.
See `gates-import-status` on each tiddler. As of the initial seed commit:

- **Fully imported:** GATES Enchanted Loot Reference.
- **Partially imported (seed only):** 00_GATES_Master_Design, GATES Time
  Travel Rules — both need a follow-up pass to bring in their full body text.
- **Not yet imported:** everything else in the old `GATES/Markdown` Drive
  folder, present here as placeholder stub tiddlers so nothing is silently
  dropped from the plan. The `GURPS_Core_Fantasy_Heroic_Search_Optimized`
  source is ~7.7MB and will need to be split into multiple tiddlers rather
  than imported as one file.
