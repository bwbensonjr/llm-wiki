# Proposal

## Why

Capture currently has one shot per source: the routed converter either succeeds or
the entry is parked `- [!]`, and the curator then repairs it by hand in an ad-hoc
way. The inbox shows the cost: publisher pages (ACM `epdf`, Springer) and bot checks
park papers that are freely available elsewhere; a Cloudflare page and a Racket 404
became permanent junk twins in `raw/` because they were recognized only after the
twin was written; hand-fetched files were filed as new `inbox-files/...` lines, so
four summaries record a local path as `source:` instead of the paper's URL (and some
of those local files are already gone); resolved parks stay `[!]` forever; and
"needs the curator" is indistinguishable from "dead, leave it."

## What Changes

- **Fallback acquisition chain in `wiki-capture`.** Before failing, capture tries
  further candidates in a fixed order: known publisher URL rewrites (ACM
  `doi/epdf/` to `doi/pdf/`), DOI-based open-access lookup (OpenAlex, then
  Unpaywall when a contact email is configured, then an arXiv title match), a direct
  fetch with local MarkItDown conversion when Jina is refused, and a Wayback Machine
  snapshot. Each candidate re-enters the ordinary content-type router.
- **Mechanical stub detection before the twin write.** Bot-check pages, HTTP error
  pages rendered as content, JavaScript loading shells, and implausibly thin output
  count as a failed attempt, so the chain moves on and no junk twin is written.
- **Acquisition provenance in the twin.** `source:` always stays the original URL;
  new `acquired-via:` and (when different) `fetched-from:` fields record which step
  and URL actually produced the content.
- **Capturing a local copy on behalf of a URL.** `wiki-capture <file> --source-url
  <url>` converts a local file while recording the original URL as `source:` and
  the file as `local-copy:`.
- **A principled manual-fetch queue in `inbox.md`.** `- [!]` now means "needs the
  curator": its annotation lists the attempts already made and a drop path
  (`→ drop: inbox-files/<slug>.<ext>`). A new `- [-]` state marks entries that are
  dead or rejected and need nothing. When a file appears at a parked entry's drop
  path, the next `ingest-inbox` run ingests it under the original URL and flips the
  **same line** to `- [x]`; no second line is written.
- **Seeing what needs fetching.** Each `ingest-inbox` run ends with a "needs manual
  fetch" list, and `wiki-capture --pending` prints the same list on demand,
  optionally rendering each link through a library proxy prefix configured in
  `mise.local.toml`.
- **Explicit non-goals.** No circumvention of bot checks or captchas, no shadow
  libraries, no headless browser. Historical `[!]` lines and the existing
  `inbox-files/` summaries are left as written.

## Capabilities

### New Capabilities

- `source-acquisition`: how capture obtains a source's content before conversion —
  the fallback candidate chain, mechanical stub detection, acquisition provenance in
  the twin, capturing a local copy under its original URL, and the network and
  privacy limits on acquisition.

### Modified Capabilities

- `unattended-ingestion`: the inbox gains the `- [-]` state and a defined meaning
  for `- [!]` (needs the curator, with attempts and a drop path); parked entries
  are resolved in place from dropped files; implausible-capture refusal no longer
  presumes a twin was written; runs report the pending manual fetches.

## Impact

- **Code:** `wiki_ingest/convert.py` (capture loop, twin front-matter),
  `wiki_ingest/detect.py`, `wiki_ingest/cli.py` (`--source-url`, `--pending`, richer
  error JSON); new modules for the resolver chain, stub detection, and inbox
  parsing. Tests under `tests/` with mocked HTTP.
- **Dependencies:** none new; OpenAlex, Unpaywall, arXiv, and Wayback are plain HTTP
  APIs reachable with `requests`.
- **Configuration:** optional `UNPAYWALL_EMAIL` and `LIBRARY_PROXY_PREFIX` in the
  gitignored `mise.local.toml`.
- **Docs and skills:** `CLAUDE.md` (converter routing, raw front-matter, inbox
  section), the `inbox.md` header, `.claude/skills/ingest-inbox/SKILL.md`, and
  `.claude/skills/file/SKILL.md` (interactive path can ask the curator to drop a
  file and use `--source-url`). The Codex-linked copies under `.agents/` follow
  whatever linking already exists.
