# Design

## Context

`capture()` in `wiki_ingest/convert.py` is a single pass: `detect.detect()` picks a
route, `convert_with_source()` produces Markdown, and the twin is written with
`source:`, `fetched-at:`, `converter:`. Any `DetectionError` / `ConversionError`
becomes `{"error": ...}` on stderr. Stub recognition happens only later, in the
`ingest-inbox` skill's judgment step (2c), after the twin already exists. The CLI
takes exactly one positional `source`. `inbox.md` state is parsed by the skill
prose, not by code. See proposal.md for motivation and the specs for the required
behavior.

## Goals / Non-Goals

**Goals:**
- Keep `capture()` all-or-nothing: candidates are tried in memory, and exactly one
  twin (or none) is written at the end.
- Make the acquisition chain deterministic and testable with a mocked
  `requests.Session`, like the existing image and PostScript tests.
- Move inbox line parsing into code, so `--pending` and drop resolution do not
  depend on an LLM re-reading the file format.

**Non-Goals:**
- No retroactive rewrite of existing twins, summaries, or historical `[!]` lines.
- No automatic multi-page assembly (DRM chapters, LaTeX2HTML nodes); those stay a
  curator drop of an assembled `.md`.
- No image localization for the direct-fetch fallback (it is defined as the
  web/Jina route only; see image-capture spec). Wayback snapshots go back through
  Jina, so they do localize.

## Decisions

**1. A candidate generator in front of the existing router.** New module
`wiki_ingest/acquire.py` yields `Candidate(url, step)` objects lazily, in order:
`primary` (the source itself), `url-rewrite`, `openalex`, `unpaywall`, `arxiv`,
`direct`, `wayback`. `capture()` loops: for each candidate, `detect()` + convert,
then `stubs.classify()`; the first non-stub result wins. Laziness matters: the
OpenAlex request is never made when the primary succeeds.
*Alternative:* bolt retries into each converter. Rejected: the fallback is about
*where* to fetch, which is orthogonal to *how* to convert, and would duplicate
across routes.

**2. Which steps apply to which sources.** Steps self-select:
- `url-rewrite` only for hosts in a small table (ACM `doi/epdf/` and `doi/abs/` to
  `doi/pdf/`; arXiv `abs/` to `pdf/`). The table is code, extended as cases appear.
- `openalex` / `unpaywall` / `arxiv` only when a DOI is extracted (`doi.org/<doi>`,
  `dl.acm.org/doi/.../<doi>`, `link.springer.com/.../<doi>`, generic `10.\d{4,}/...`
  in the path). `unpaywall` only when `UNPAYWALL_EMAIL` is set. `arxiv` searches by
  the OpenAlex title and accepts a result only when normalized titles match exactly
  (lowercased, punctuation stripped); fuzzy matching is not worth a wrong paper.
- `direct` only when the primary route was Jina and Jina failed or returned a stub:
  GET with `PROBE_HEADERS`, write the HTML to a temp file, convert with MarkItDown.
- `wayback` always last for URL sources: query the availability API, then fetch
  `https://web.archive.org/web/<ts>id_/<url>` so the snapshot is the original
  bytes without the archive toolbar.
Local file sources get only `primary`.

**3. Stub classification is a separate pure function.** `wiki_ingest/stubs.py`
takes `(markdown, detected_type, step)` and returns `None` or a short reason.
Signals: known bot-check titles/phrases ("Just a moment", "Checking your browser",
"Enable JavaScript and cookies"), error titles ("Page Not Found", "403 Forbidden",
"Access Denied"), loading-shell markers, and a word-count floor (for example under
150 words for a PDF route, under 80 for HTML). Thresholds are constants with tests
built from the two junk twins already in `raw/`. The `ingest-inbox` judgment check
(2c) stays as the second line of defense for subtler cases (bibliography-only
Springer output, table-of-contents landing pages).
*Alternative:* leave all stub judgment to the LLM. Rejected: it cannot stop the
write, which is the defect being fixed.

**4. Provenance fields.** Twin front-matter gains `acquired-via:` always, and
`fetched-from:` / `local-copy:` when applicable. `converter:` keeps its existing
vocabulary (the direct step records `markitdown`). `CaptureResult` and the success
JSON gain `acquired_via` and `fetched_from`; the error JSON gains `attempts: [{step,
url, outcome}]` and `title` (best known, from OpenAlex or a stub's H1 or the URL).

**5. `--source-url` on the CLI.** `wiki-capture <local-file> --source-url <url>`
runs only the `primary` candidate on the file and writes `source: <url>`,
`local-copy: <file>`, `acquired-via: manual`. The twin slug still comes from the
converted title, so a file named `1291151.1291197.pdf` no longer yields an
unreadable slug when the document has a title.

**6. Inbox parsing in code.** New `wiki_ingest/inbox.py` parses lines into
`(state, source, note, annotations, drop_path)` where `drop_path` is taken from the
`→ drop: <path>` token. `wiki-capture --pending` (with the positional source made
optional when `--pending` is given) reads `inbox.md`, lists `[!]` entries whose drop
stem has no file in `inbox-files/`, and prints JSON (`[{line, source, drop,
proxied}]`) or, with `--text`, a plain list. `LIBRARY_PROXY_PREFIX` is prepended
verbatim to the URL (EZproxy style `https://proxy.example.edu/login?url=`). No
network access.
*Alternative:* a separate `fetch.md` queue. Rejected: two files would hold the same
state and drift; `inbox.md` stays the single source of truth.

**7. Drop path naming.** `inbox-files/<slugify(best title)>.<ext>`, `ext` from the
expected type (`.pdf` when the source or any candidate was a PDF, `.md` for HTML
pages that need assembly). Matching is by stem, any extension. A slug collision with
an existing file for a different entry gets `-2`, as slugs do elsewhere.

**8. Skill changes carry the workflow.** `ingest-inbox` gains: a pre-pass that
resolves `[!]` entries with a present drop (capture with `--source-url`, author,
flip the same line to `[x]`), the park format with attempts and drop path, the
`[-]` outcome for out-of-scope or non-document sources, and the closing
manual-fetch report (which it gets from `--pending`). `file` gains: on capture
failure, show the attempts and the drop path and offer to wait for the curator's
file, then capture with `--source-url`.

## Risks / Trade-offs

- [More network requests per failure, slower failing runs] → Steps are lazy and
  self-selecting; each request keeps the existing 20s / 120s timeouts.
- [Third-party APIs change or rate-limit] → Every step failure is just a recorded
  attempt; the chain degrades to today's behavior plus Wayback.
- [Wrong paper from an open-access index] → DOI lookups are exact; the arXiv title
  match is exact after normalization; the LLM plausibility check still reads the
  twin before authoring.
- [Stub heuristics reject a genuinely short page] → Word floors are low and
  route-specific; the attempt list names the reason, and the curator can drop the
  page by hand or file it interactively.
- [Wayback copy is older than the live page] → `fetched-from:` records the snapshot
  URL with its timestamp, so the twin is honest about what it captured.
- [Curator email reaches Unpaywall] → Only when `UNPAYWALL_EMAIL` is explicitly set
  in the gitignored `mise.local.toml`; never defaulted.

## Migration Plan

No data migration. Existing `[!]` lines without a drop path keep working: they are
skipped as today and listed by `--pending` as "no drop path"; the curator can add a
`→ drop:` token by hand to use the new resolution. Rollback is reverting the code
and skill changes; twins written with the extra front-matter fields remain valid
YAML that nothing else reads.

## Open Questions

- Exact word-count floors for the stub classifier; tune against the existing
  `raw/` corpus during implementation.
- Whether to add Semantic Scholar or CORE as further open-access indexes later; the
  candidate generator makes that a local addition.
