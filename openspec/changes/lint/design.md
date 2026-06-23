## Context

The wiki has two commands: `file` (skill + `wiki-capture` Python CLI) ingests
sources into immutable `raw/` twins and curator-authored `wiki/` pages, and
`query` (skill-only) answers questions against the corpus and optionally files
an `analysis` page. Both are *additive* — they only create new pages and append
bookkeeping. Neither keeps the corpus internally consistent over time, and both
explicitly defer that work: tag reconciliation is "the future `lint` command's
job," and "index maintenance/repair is `lint`'s concern."

`lint` is the third and last planned command (capture done; query done; lint
now). It mirrors the established shape — a curator-gated skill — but differs in
two ways. First, its "Phase 1" is *auditing local Markdown*, work the LLM does
directly with Grep/Read, so like `query` it is skill-only with no Python
counterpart. Second, unlike `file` and `query`, its repairs *mutate existing
`wiki/` pages in bulk* (tag rewrites, page moves, index fixes) — it is the first
command that can change content already in the corpus.

## Goals / Non-Goals

**Goals:**

- Audit the whole corpus for the defect classes the other specs defer to `lint`:
  invalid/incomplete front-matter, `type`/folder mismatches, broken
  `[[wikilinks]]`, orphan pages, index/log drift, missing body sections, and an
  inconsistent tag vocabulary.
- Default to a read-only report; make every repair curator-gated through the
  same propose → coach → commit pattern as `file` and `query`.
- Preserve the wiki's invariants while fixing it: `raw/` stays immutable, and
  bulk page edits are previewed before any write.
- Complete the capture → query → lint command set.

**Non-Goals:**

- No embeddings, vector index, or external service. Auditing is reading/grepping
  local Markdown, same rationale as `query`.
- No Python/CLI changes; `wiki_ingest` and `wiki-capture` are untouched.
- No new page `type` and no taxonomy change — `lint` enforces the existing
  taxonomy, it does not extend it.
- No content rewriting beyond consistency repair: `lint` does not re-summarize,
  re-interview, or improve the prose of `## Summary` / `## Why this matters` /
  `## Answer` bodies. It fixes structure and metadata, not voice.
- No automatic tag merging — clustering is mechanical, but the canonical choice
  is always a curator decision.

## Decisions

**Skill-only, no Python CLI.** The checks are file reads and greps over `wiki/`
the agent already has tools for. A Python linter would add a dependency and a
sync-burden against `CLAUDE.md`'s evolving rules for no gain at this corpus size.
*Alternative:* a `wiki-lint` CLI encoding the rules — rejected as premature and
duplicative of the conventions already written in prose; revisit only if the
corpus outgrows whole-corpus reading.

**Report first, fix second (and optional).** `lint` always produces a diagnostic
report in conversation; repair is a separate, explicitly-offered step gated on
the curator's commit. A curator who just wants to see the corpus's health pays
nothing, exactly as a `query` lookup that is never filed writes nothing.

**Mechanical fixes vs. judgment calls.** Repairs split in two. *Mechanical*
fixes have one correct outcome — restore a missing index entry, move a page into
the folder matching its `type`, repoint a link whose target is unambiguous — and
can be batch-approved. *Judgment calls* have no single right answer — which tag
is canonical, which of several pages a broken link meant — and are interviewed
one at a time. The report and the proposal keep the two visibly separate so a
curator can accept the safe batch without adjudicating every tag.

**`raw/` is never touched.** `raw/` twins are immutable by the two-layer
contract. `lint` reads them only to confirm a `summary`'s `raw:` pointer
resolves; it never edits or renames one. All repairs land in `wiki/`. This is
called out explicitly because `lint` is the first command with the *power* to
mutate broadly, so the immutability boundary must be an enforced rule, not just
an emergent property.

**Preview before write.** Because repairs touch existing pages — including
corpus-wide tag rewrites that span many files — the commit step previews the
intended changes (as a diff or an explicit per-file change list) before writing.
This keeps the curator in control of bulk edits and guards against a single
misjudged merge rewriting the whole vocabulary.

**Bookkeeping symmetry with `file`/`query`.** A committed lint run appends one
`## [<date>] lint: <subject>` entry to `wiki/log.md`, matching the
`ingest:` / `query:` convention so the log stays greppable by the `## [`
prefix, and reflects any page move/rename in `wiki/index.md`. A read-only audit
that commits nothing adds no log line.

**Coverage advisory closes the discovery loop — without taking authority.**
The fixed-checklist design is reactive: it enforces known rules and finds
nothing it has no check for. A final read-only advisory pass mitigates that by
surfacing *emergent* patterns — an undefined front-matter field used on several
pages, a recurring body section outside the defined shapes — as *candidate* new
checks for the curator to consider. It deliberately stops there: candidates are
never treated as defects, never repaired, and adopting one means the curator
edits `CLAUDE.md`, not that `lint` acts. This keeps authority where the design
already puts it (conventions live in `CLAUDE.md`; `lint` enforces) while letting
the linter's coverage grow from what the corpus actually shows. *Alternative:* a
linter that silently enforces only its hard-coded checks — rejected for letting
coverage gaps persist invisibly; an LLM that mints and acts on its own rules —
rejected as exactly the curator judgment this command must not usurp.

**Index as derived, conventions as source of truth.** Where `index.md` and the
pages on disk disagree, the pages are authoritative and the index is the thing
repaired — the index is bookkeeping *about* the pages. Likewise the validity
rules (allowed `type`s, required fields, body shapes, folder mapping) are read
from the conventions in `CLAUDE.md`; `lint` enforces them rather than inventing
its own.

## Risks / Trade-offs

- **Bulk mutation of existing pages** (the headline risk — `lint` is the first
  command that can damage content already in the corpus) → mitigated by
  read-only-by-default, curator-gated commit, mechanical/judgment separation,
  preview-before-write, and the hard `raw/`-immutability rule. Git history is
  the backstop for any over-broad edit.
- **Over-eager tag clustering** merging genuinely distinct tags → clustering
  only *proposes*; the canonical choice and every fold-in is curator-approved,
  and singletons are surfaced, not auto-removed.
- **Ambiguous link repair** repointing a broken `[[wikilink]]` to the wrong page
  → only unambiguous targets are offered as mechanical fixes; multiple plausible
  targets fall to the judgment-call interview.
- **Convention drift** between `CLAUDE.md` and the linter's encoded rules → the
  rules live in `CLAUDE.md` prose and the skill reads them as the source of
  truth, rather than hard-coding a second copy that can fall out of sync.
- **False "clean" on a large corpus** if a check silently skips files → checks
  iterate the full page set from disk (not the index, which may itself be
  stale), so coverage does not depend on the artifact being audited.

## Migration Plan

Additive in code, corrective in content. New skill, new spec, and a documented
roadmap update; no existing spec requirements change and no Python changes. The
only effect on existing content is the repairs a curator explicitly commits,
each previewed and reversible through git. Nothing to roll back beyond deleting
the new skill if abandoned.

## Open Questions

- Should `lint` accept a scope argument (lint one page or one folder) or always
  audit the whole corpus? Whole-corpus is the default; a scoped mode can be a
  later refinement if runs get expensive.
- Should the orphan-page advisory ever propose a fix (e.g., suggest a hub to link
  from), or stay purely advisory? Left advisory for now; revisit against real
  orphans.
- Long-term, should a committed lint run record *which* defects it fixed in the
  log subject, or just that a run occurred? Settle during implementation against
  real runs.
