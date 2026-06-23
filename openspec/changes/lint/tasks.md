## 1. Author the lint skill

- [x] 1.1 Create `.claude/skills/lint/SKILL.md` with name `lint` and a
  description matching the `file`/`query` skills' style (so the harness surfaces
  it for "lint", "audit", "check the wiki" requests)
- [x] 1.2 Write the corpus-load step: enumerate every `wiki/` knowledge page
  from disk (not from `index.md`, which may be stale), parse each page's
  front-matter and body sections, and read `CLAUDE.md` as the source of truth
  for allowed `type`s, required fields, body shapes, and the folder→type mapping

## 2. Implement the audit checks (read-only)

- [x] 2.1 Front-matter & taxonomy: flag missing/invalid `type`, missing required
  fields per `type`, `type`/folder mismatch, and a `summary` whose `raw:` twin
  does not exist on disk
- [x] 2.2 Link integrity: resolve every `[[wikilink]]` against existing page
  filenames; flag links that resolve to no page, including links broken by line
  wrapping
- [x] 2.3 Orphans: flag knowledge pages with no inbound `[[wikilink]]` as a
  softer advisory, separate from broken-link defects
- [x] 2.4 Index integrity: flag pages missing from `wiki/index.md`, index entries
  for pages that no longer exist, and entries grouped under a type that differs
  from the page's `type`
- [x] 2.5 Log integrity: flag `wiki/log.md` entries that do not follow the
  greppable `## [<date>] <op>: <subject>` form
- [x] 2.6 Body sections: flag `summary`/`analysis` pages missing a required named
  section (`## Summary`/`## Why this matters`, `## Answer`/`## Why this matters`)
- [x] 2.7 Tag vocabulary: collect the corpus-wide tag set and cluster
  near-duplicates (casing, plural, hyphenation variants) and restating
  singletons, proposing a canonical form per cluster
- [x] 2.8 Coverage advisory (read-only): surface emergent patterns no current
  check governs (e.g., an undefined front-matter field on several pages, a
  recurring section outside the defined shapes) as candidate new
  checks/conventions, distinct from defects and never repaired

## 3. Report and repair flow

- [x] 3.1 Write the report step: group findings by category, name the affected
  page for each, present the coverage advisory (2.8) as a section distinct from
  defects, and report a clean result with no repairs offered when the corpus has
  no defects
- [x] 3.2 Write the repair interview (propose → coach → commit): default to
  writing nothing; separate mechanical fixes (restore index entry, re-file
  misplaced page, repoint an unambiguous broken link) from judgment calls (tag
  merges, ambiguous link targets) so each can be approved independently
- [x] 3.3 Write the preview step: show intended changes as a diff / explicit
  per-file change list before any write, especially for corpus-wide tag rewrites
- [x] 3.4 Write the commit step: apply approved repairs only on commit, never
  edit or rename a file under `raw/`, and append one `## [<date>] lint:
  <subject>` entry to `wiki/log.md` (reflecting any page move/rename in
  `wiki/index.md`) without rewriting existing log entries
- [x] 3.5 Add a Guardrails section (audit writes nothing until commit; `raw/`
  immutable; tag merges and ambiguous link fixes require approval; conventions in
  `CLAUDE.md` are the source of truth for validity rules; the coverage advisory
  only proposes candidate checks and never acts on them)

## 4. Documentation

- [x] 4.1 Update `README.md` to describe the `lint` command alongside `file` and
  `query`, completing the capture → query → lint set
- [x] 4.2 Update the command roadmap note (memory/roadmap) so `lint` is marked
  done and no commands remain planned

## 5. Verify end-to-end

- [x] 5.1 Run `lint` on the current corpus; confirm a grouped, read-only report
  and that no files change when repairs are declined
- [x] 5.2 Introduce a broken `[[wikilink]]`, a page missing from `index.md`, and
  a `type`/folder mismatch; confirm each is detected and correctly categorized
- [x] 5.3 Introduce near-duplicate tags; confirm they cluster with a proposed
  canonical form and that nothing is rewritten without approval
- [x] 5.4 Commit a mechanical fix; confirm only `wiki/` changed, `raw/` is
  untouched, and one `## [<date>] lint:` entry was appended to `wiki/log.md`
- [x] 5.5 Re-run `lint` on the (intentionally clean) corpus; confirm it reports
  no defects and offers no repairs
- [x] 5.6 Add an undefined front-matter field to several pages; confirm the
  coverage advisory surfaces it as a candidate convention, separate from defects,
  and proposes no repair and changes no file
