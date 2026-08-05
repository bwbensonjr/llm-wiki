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
- [x] https://www.ccs.neu.edu/home/shivers/cs6983/papers/kranz-diss-tr632.pdf - Motivation and details of closure analysis and CPS transformation
- [x] http://scheme2006.cs.uchicago.edu/11-ghuloum.pdf - Introduces the nanopass idea of incremental compiler transformations
- [!] http://foo.bar.baz/bad-link - Introduced for testing bad link handling — 2026-08-05: capture failed, DNS could not resolve host foo.bar.baz
- [x] https://3e8.org/pub/scheme/doc/lisp-pointers/v7i3/p128-clinger.pdf - Describes an approach to code transformation and lambda lifting
- [x] https://en.wikipedia.org/wiki/Western_Sahara - A link to test reject because it doesn't match the subject matter of this wiki 
- [x] https://www.deinprogramm.de/sperber/papers/tractable-native-code-scheme-system.pdf - Looks at going from virtual machine to native code
- [!] https://dl.acm.org/doi/epdf/10.1145/1159803.1159805 - An in-depth history of an important Scheme compiler — 2026-08-05: Cloudflare bot check, no article content (twin: raw/2026-08-05-just-a-moment.md)
- [!] https://dl.acm.org/doi/epdf/10.1145/2544174.2500618 - A particular framework for multi-pass compilers — 2026-08-05: ACM JS reader shell, only a loading stub, no article content. Title resolves to Keep & Dybvig, "A nanopass framework for commercial compiler development" (ICFP 2013); retry via a direct PDF host.
- [!] https://link.springer.com/content/pdf/10.1023/A:1010016816429.pdf - Compilation approaches for Scheme continuations — 2026-08-05: Springer served only the bibliography (47 references, no abstract or body). Paper is Clinger, Hartheimer & Ost, "Implementation Strategies for First-Class Continuations" (HOSC 1999); retry via a direct PDF host.
- [x] https://dl.acm.org/doi/pdf/10.1145/3386330 - A broad overview of hygenic macro technologies like those available in Scheme
- [x] inbox-files/1159803.1159805.pdf - Local version of failed to download Chez Scheme paper - An in-depth history of an important Scheme compiler
- [x] inbox-files/2544174.2500618.pdf - Local version of failed to download nanopass paper - A particular framework for multi-pass compilers
- [ ] inbox-files/A_1010016816429.pdf - Local version of failed to download continuation paper - Compilation approaches for Scheme continuations
