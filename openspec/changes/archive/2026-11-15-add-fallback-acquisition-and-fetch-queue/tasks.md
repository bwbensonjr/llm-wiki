# Tasks

## 1. Stub detection before the twin write

- [x] 1.1 Add `wiki_ingest/stubs.py` with `classify(markdown, detected_type, step)` returning `None` or a reason (bot-check, error page, loading shell, word floor per route); verify with `tests/test_stubs.py` using fixtures copied from `raw/2026-08-05-just-a-moment.md` and `raw/2026-10-31-racket-page-not-found.md`, plus a legible ligature-artifact PostScript sample that must not be flagged
- [x] 1.2 Call `classify()` in `capture()` before writing, raising a `ConversionError` that carries the stub reason; verify a capture test with a mocked Jina response of a bot-check page writes no file under `raw/`
- [x] 1.3 Tune the word floors by running `classify()` over every existing twin in `raw/` and confirm that only the two known junk twins are flagged; record the chosen constants in a module docstring

## 2. Fallback acquisition chain

- [x] 2.1 Add `wiki_ingest/acquire.py` with a lazy `candidates(source, session, env)` generator and DOI extraction for `doi.org`, ACM, Springer, and generic `10.NNNN/` paths; verify unit tests cover each URL form, including `10.1023/A:1010016816429`
- [x] 2.2 Implement the `url-rewrite` step (ACM `doi/epdf/` and `doi/abs/` to `doi/pdf/`, arXiv `abs/` to `pdf/`); verify by unit test
- [x] 2.3 Implement the `openalex` step (best OA PDF location, records the title) and the `unpaywall` step gated on `UNPAYWALL_EMAIL`; verify with mocked responses that unpaywall is never requested when the variable is unset and that no request carries identifying data in that case
- [x] 2.4 Implement the `arxiv` title-search step with exact normalized title matching; verify a mismatched title is rejected and a matching one yields the PDF URL
- [x] 2.5 Implement the `direct` step (applies only after a failed or stub Jina primary: fetch HTML with `PROBE_HEADERS`, convert with MarkItDown); verify with a mocked Jina 403 and a reachable page
- [x] 2.6 Implement the `wayback` step (availability API, then the `id_` snapshot URL routed through the normal router); verify with mocked availability and snapshot responses
- [x] 2.7 Restructure `capture()` to loop over candidates, run detect, convert, and classify for each, and write exactly one twin from the first success; collect `attempts` on failure; verify that a primary success makes no fallback request and that an exhausted chain raises with every attempt listed
- [x] 2.8 Verify end to end by mocked-session tests that each step's success writes a twin and each scenario in `specs/source-acquisition/spec.md` has a matching test; run `uv run pytest`

## 3. Provenance and CLI

- [x] 3.1 Write `acquired-via:` always and `fetched-from:` when it differs from `source:` in the twin front-matter; add `acquired_via` and `fetched_from` to `CaptureResult` and the success JSON; verify by capture tests asserting the front-matter for a primary capture and an OA-copy capture
- [x] 3.2 Add `attempts` and `title` to the CLI error JSON; verify by a CLI test that parses stderr after an exhausted chain
- [x] 3.3 Add `--source-url <url>` (local file only, primary step only, writes `source:`, `local-copy:`, `acquired-via: manual`); verify by a test capturing a fixture PDF and asserting the front-matter and a title-derived slug
- [x] 3.4 Update the `CLAUDE.md` converter-routing and raw front-matter sections (fallback chain, stub rejection, new fields, `UNPAYWALL_EMAIL` in `mise.local.toml`, the access limits) and the `wiki_ingest/cli.py` module docstring; verify the documented `wiki-capture` invocations run as written

## 4. Inbox parsing and the pending list

- [x] 4.1 Add `wiki_ingest/inbox.py` parsing checklist lines into state, source, note, annotations, and `→ drop:` path, recognizing `[ ]`, `[x]`, `[!]`, `[-]`; verify with `tests/test_inbox.py` against a copy of the current `inbox.md`, which must parse every line without error
- [x] 4.2 Add drop-path naming (`inbox-files/<slug>.<ext>`, stem matching with any extension, `-2` on collision) and expose it on the CLI (e.g. `wiki-capture --drop-path <url> --title <title>`) so the skill does not hand-slugify; verify by unit tests including the nanopass example from the spec
- [x] 4.3 Add `wiki-capture --pending` (source optional when given; JSON by default, `--text` for a plain list; proxied URL when `LIBRARY_PROXY_PREFIX` is set; "no drop path" for legacy `[!]` lines); verify by a test that runs it with networking disabled and checks both formats
- [x] 4.4 Update the `inbox.md` header (state table with `[-]`, the `→ drop:` convention, how to resolve a park by dropping a file) and the inbox section of `CLAUDE.md` (also documenting `LIBRARY_PROXY_PREFIX`); verify `wiki-capture --pending` still parses the edited `inbox.md`

## 5. Skills

- [x] 5.1 Update `.claude/skills/ingest-inbox/SKILL.md`: drop-resolution pre-pass (capture with `--source-url`, author, flip the same line to `[x]` keeping its text), the new park format with attempts and drop path, `[-]` for out-of-scope or non-document sources, step 2c noting that mechanically rejected stubs leave no twin, and the closing manual-fetch report from `--pending`; verify the skill text matches every scenario in `specs/unattended-ingestion/spec.md`
- [x] 5.2 Update `.claude/skills/file/SKILL.md`: on capture failure show the attempts and drop path, and offer to capture the curator's file with `--source-url`; verify by reading the skill against the `source-acquisition` local-copy requirement
- [x] 5.3 Confirm the Codex skill links under `.agents/skills/` still resolve to the updated skill files; verify with `ls -l .agents/skills`

## 6. Integration check

- [x] 6.1 In a scratch copy of the repo, add a `[!]` line with a drop path and the matching fixture file, run the drop-resolution flow, and confirm the summary's `source:` is the original URL, the same inbox line is `[x]`, and no line was added
- [x] 6.2 Run `uv run pytest` and `mise exec -- openspec validate add-fallback-acquisition-and-fetch-queue --strict`, both passing

## Workflow follow-up

- Optionally, as a separate curator edit: add `→ drop:` tokens to the still-parked historical lines, or flip the four already-resolved ones to `[x]`.
- Archive the change after review with the `openspec-archive-change` skill.
