# Inbox

The queue of sources awaiting unattended ingest. Append links here from anywhere;
the `ingest-inbox` command drains it, checks off what it filed, and parks what it
could not.

This file is **committed mutable working state**, not a knowledge page. It lives
at the repo root deliberately: outside `wiki/`, so the site build does not publish
it and `lint` does not read it as an untyped page.

## Line format

Each entry is one Markdown checklist line: a checkbox, a URL or local path, and
an optional separator (` — ` or ` - `) followed by a free-text curator note.

| Checkbox | Meaning |
|----------|---------|
| `- [ ]`  | unprocessed — the next run will ingest it |
| `- [x]`  | ingested (or skipped as already ingested) — not retried |
| `- [!]`  | parked after a failure, annotated with the date and reason — not retried |

The note, when present, is the curator's reason for saving the link. It seeds the
drafted `## Why this matters` on the resulting summary page, so a provisional
page's significance is anchored to why the link was actually saved rather than
purely machine-inferred. It costs nothing to leave off.

Entries are never deleted — the checkbox carries the state, so the file stays a
legible, diffable record of what was queued. Re-running against a drained inbox
is a no-op.

```markdown
- [ ] https://example.com/paper.pdf — worth it for the CPS angle
- [ ] https://example.com/post
- [x] https://example.com/already-ingested
- [!] https://example.com/broken — 2026-08-05: docling failed, unparseable PDF
```

## Queue

<!-- Append new sources below as `- [ ] <url-or-path> — <optional note>`. -->
- [x] https://research.scheme.org/lambda-papers/lambda-papers-compiler-optimization.html - Seminal Scheme compiler paper by co-inventor of Scheme
- [ ] https://www.ccs.neu.edu/home/shivers/cs6983/papers/kranz-diss-tr632.pdf - Motivation and details of closure analysis and CPS transformation
- [ ] http://scheme2006.cs.uchicago.edu/11-ghuloum.pdf - Introduces the nanopass idea of incremental compiler transformations
- [ ] http://foo.bar.baz/bad-link - Introduced for testing bad link handling
