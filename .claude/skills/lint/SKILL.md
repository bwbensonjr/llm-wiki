---
name: lint
description: Audit the llm-wiki corpus for consistency defects and optionally repair them. Checks front-matter/taxonomy validity, broken wikilinks, orphan pages, index/log drift, missing body sections, and tag-vocabulary consistency — reporting findings read-only by default, then optionally running a propose→coach→commit interview to apply repairs. Use when the user wants to lint, audit, check, or clean up the wiki.
metadata:
  author: llm-wiki
  version: "1.0"
---

# The `lint` command

Audit the whole `wiki/` corpus for structural and consistency defects, report
them, and — only if the user commits — repair them. Read the repo `CLAUDE.md`
first: the page taxonomy, per-type front-matter, slug rules, folder→type
mapping, body shapes, and tag conventions are the **source of truth** for what
counts as a defect. Enforce those rules; do not invent new ones.

**Input:** an optional scope argument. With none, audit the whole corpus
(the default). The command never narrows scope on its own.

**The command always reports in conversation first. Repair is a separate,
optional step that writes nothing to the wiki until the user commits.**

---

## Phase 1 — audit (read-only)

Do **no** writes in this phase. Load the corpus from disk, then run every check.

### 0. Load the corpus

Enumerate every `wiki/` knowledge page **from disk** (glob `wiki/**/*.md`), not
from `index.md` — the index may itself be stale, so coverage must not depend on
it. For each page, parse its YAML front-matter and note its body sections and
its `[[wikilinks]]`. Read `CLAUDE.md` for the allowed `type`s, the fields each
`type` requires, the folder each `type` maps to, and the fixed body shapes.

**Ignore illustrative text.** A `[[wikilink]]` inside an inline-code span
(backticks) or a fenced code block is documentation *about* the convention, not
a real citation — `index.md` and `log.md` describe their own formats this way,
and pages like `obsidian.md` mention `[[wikilinks]]` in prose. Likewise, the
format example in `log.md`'s header (`## [<date>] <op>: <subject>`) is not a real
log entry. Treat only live links and real entries as findings, never the
examples that explain them.

### 1. Front-matter & taxonomy

Flag any page that:

- has no `type`, or a `type` outside `summary | entity | concept | analysis`;
- omits a front-matter field its `type` requires;
- lives in a folder that does not match its `type` (e.g. a `concept` under
  `wiki/entities/`);
- (for a `summary`) has a `raw:` path that does not resolve to an existing file.

### 2. Link integrity

Resolve every `[[wikilink]]` across the corpus against the set of existing page
filenames. Flag links that resolve to no page. Watch for links broken by line
wrapping — a `[[wikilink]]` split across a newline does not resolve in Obsidian;
report it as broken.

**Skip `wiki/log.md` in this check**, per `CLAUDE.md`. The log is append-only, so a
link it contains can be un-made by a later `curate` rejection or merge that no
operation is permitted to go back and repair. Reporting it would be reporting a
defect nothing can fix. Note in passing if you like; never count it as a defect.

### 3. Orphans

Flag knowledge pages with **no inbound** `[[wikilink]]` from any other page. Keep
this as a softer *advisory*, distinct from broken-link defects — an orphan is
not malformed, just unreachable.

### 4. Index integrity

Reconcile `wiki/index.md` against the pages on disk. Flag:

- knowledge pages on disk with no entry in the index;
- index entries that point to a page whose file no longer exists;
- entries filed under a type grouping (`## Summaries`, `## Entities`,
  `## Concepts`, `## Analyses`) that differs from the page's actual `type`.

### 5. Log integrity

Flag any `wiki/log.md` entry that does not follow the greppable
`## [<date>] <op>: <subject>` form (the stable `## [` prefix).

### 6. Body sections

For pages whose `type` defines a fixed body shape, flag a missing or extra named
section: a `summary` must have exactly `## Summary` and `## Why this matters`; an
`analysis` must have exactly `## Answer` and `## Why this matters`.

### 7. Tag vocabulary

Collect the tag set used across the whole corpus. Cluster tags that are casing,
pluralization, or hyphenation variants of one another (e.g. `LLM` / `llm`,
`type-system` / `type-systems`), and singletons that appear to restate an
existing tag. For each cluster, **propose** a canonical form — but never decide
it. The canonical choice and every fold-in is a curator decision (Phase 3).

### 8. Coverage advisory (read-only, never acts)

After the fixed checks, surface recurring patterns the corpus exhibits that **no
current check governs** — e.g. a front-matter field used on several pages that
the schema does not define, or a body section recurring outside the defined
shapes. Describe each as a *candidate* new check or convention for the curator
to consider. This is purely advisory: do **not** treat these as defects, do not
propose repairs for them, and do not modify any file. Adopting one means the
curator edits `CLAUDE.md` — not something `lint` does.

---

## Phase 2 — report

Present the findings grouped by category. For each finding, name the affected
page (and line where useful) so the curator can locate it. Keep three things
visibly separate:

- **Defects** — the checks in §1–§6 above, grouped by category.
- **Advisories** — orphans (§3) and the coverage advisory (§8): real but softer,
  not necessarily wrong.
- **Tag clusters** — the §7 proposals, each with its candidate canonical form.

If the corpus has no detectable defects, report a clean result and offer no
repairs (a coverage advisory may still be worth noting). Stop here unless the
user wants to repair something — nothing has been written.

---

## Phase 3 — repair (optional: propose → coach → commit)

Offer to apply repairs. If the user only wanted the report, stop — nothing is
written.

### 1. Propose

Separate the repairs into two buckets so the user can act on them
independently:

- **Mechanical fixes** — one correct outcome, safe to batch-approve: restore a
  missing `index.md` entry, remove a stale one, move a page into the folder
  matching its `type`, add a missing required field, repoint a broken
  `[[wikilink]]` whose intended target is **unambiguous**.
- **Judgment calls** — no single right answer, decided one at a time: which tag
  is canonical and which variants fold into it, which of several plausible pages
  a broken link meant, whether an orphan should gain a link.

The coverage advisory (§8) is never a repair — it only ever informs a future
`CLAUDE.md` edit by the curator.

### 2. Coach

Let the user accept, reject, or adjust each proposal. For tag merges, confirm
the canonical tag and the exact set of variants that fold in before touching any
page. For ambiguous links, let the user pick the target (or skip). Iterate until
they are satisfied.

### 3. Preview, then commit

Before writing anything, **preview** the intended changes — a diff or an
explicit per-file change list — especially for corpus-wide tag rewrites that
span many files. Write only after the user commits. Then:

- Apply each approved fix to the relevant `wiki/` page(s).
- **Never edit or rename a file under `raw/`.** `raw/` twins are immutable; lint
  reads them only to check a `summary`'s `raw:` pointer.
- Reflect any page move/rename in `wiki/index.md` (and fix the index entries the
  run repaired).
- Append exactly one entry to `wiki/log.md` (do not rewrite existing ones):
  `## [<date>] lint: <subject>` followed by a line summarizing what was fixed.

After writing, re-check the touched pages: every `[[wikilink]]` still resolves,
each page's `type` is valid and matches its folder, and required sections are
present. Fix any regression rather than leaving a half-applied repair.

---

## Guardrails

- The audit (Phases 1–2) writes nothing; never touch `wiki/` until the user
  commits in Phase 3.
- Raw twins are immutable: never edit or rename a file under `raw/`.
- `CLAUDE.md` is the source of truth for validity rules — enforce its
  conventions, do not invent your own defects.
- Tag merges and ambiguous link repairs require explicit approval; never merge
  tags or guess a link target on your own.
- The coverage advisory only proposes candidate checks — it never labels a
  pattern a defect, repairs it, or writes a file.
- Coverage comes from globbing pages on disk, not from `index.md` (which may be
  the very thing that is stale).
- A committed run must append a single `## [<date>] lint: <subject>` entry to
  `wiki/log.md` and reflect any move/rename in `index.md`.
