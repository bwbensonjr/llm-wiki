# corpus-lint Specification

## Purpose

Audit the whole wiki corpus for structural and consistency defects — invalid or
incomplete front-matter, `type`/folder mismatches, broken `[[wikilinks]]`,
orphan pages, index/log drift, missing body sections, and an inconsistent tag
vocabulary — and, under a curator-gated commit, repair them. This is the `lint`
command: the corpus-wide hygiene the `file` and `query` commands defer to it,
reporting read-only by default and mutating `wiki/` only when the curator
commits, never touching immutable `raw/` twins. It completes the capture →
query → lint command set.

## Requirements

### Requirement: Read-only audit by default

The `lint` command SHALL audit the wiki corpus and report its findings without
writing any files by default. Running `lint` to inspect the corpus SHALL leave
`wiki/`, `raw/`, and all bookkeeping files unchanged. The report SHALL group
findings by category and identify each affected page by its filename so the
curator can locate it.

#### Scenario: Audit writes nothing

- **WHEN** the user runs `lint` and does not commit any repair
- **THEN** no files under `wiki/` or `raw/` are created, modified, or renamed

#### Scenario: Findings are grouped and located

- **WHEN** the command reports defects
- **THEN** findings are grouped by category and each names the affected page so
  the curator can find it

#### Scenario: Clean corpus reports no defects

- **WHEN** the corpus has no detectable defects
- **THEN** the command reports a clean result and offers no repairs

### Requirement: Front-matter and taxonomy validation

The `lint` command SHALL check every `wiki/` knowledge page for a valid `type`
drawn from the defined set (`summary`, `entity`, `concept`, `analysis`), the
front-matter fields required for that `type`, and placement in the folder that
mirrors its `type`. It SHALL report any page whose `type` is missing or outside
the set, whose required fields are absent, or whose folder does not match its
`type`. For a `summary` page it SHALL report when the `raw:` twin it points to
does not exist on disk.

#### Scenario: Invalid type is reported

- **WHEN** a page carries a `type` outside the defined set or no `type` at all
- **THEN** the command reports it as an invalid-type defect rather than silently
  accepting the page

#### Scenario: Folder and type disagree

- **WHEN** a page's `type` does not match the folder it lives in
- **THEN** the command reports the mismatch and identifies the folder the page
  belongs in

#### Scenario: Missing required front-matter

- **WHEN** a page omits a front-matter field its `type` requires
- **THEN** the command reports the missing field for that page

#### Scenario: Summary points to a missing raw twin

- **WHEN** a `summary` page's `raw:` path does not resolve to an existing file
- **THEN** the command reports the dangling `raw:` reference

### Requirement: Link and orphan integrity

The `lint` command SHALL resolve every `[[wikilink]]` across the corpus against
the set of existing page filenames and SHALL report any link that resolves to no
page, including links broken by line wrapping. It SHALL also report orphan
pages — knowledge pages with no inbound `[[wikilink]]` from any other page — as
a softer advisory finding distinct from broken links.

#### Scenario: Broken wikilink is reported

- **WHEN** a `[[wikilink]]` names a page filename that does not exist
- **THEN** the command reports the broken link and the page it appears on

#### Scenario: Orphan page is surfaced

- **WHEN** a knowledge page has no inbound `[[wikilink]]` from any other page
- **THEN** the command surfaces it as an orphan advisory, separate from
  broken-link defects

### Requirement: Index and log integrity

The `lint` command SHALL reconcile `wiki/index.md` against the pages on disk. It
SHALL report any knowledge page absent from the index, any index entry that
points to a page that no longer exists, and any entry filed under a grouping
that does not match its page's `type`. It SHALL verify that `wiki/log.md`
entries follow the greppable `## [<date>] <op>: <subject>` form and report
entries that do not.

#### Scenario: Page missing from the index

- **WHEN** a knowledge page exists on disk but has no entry in `wiki/index.md`
- **THEN** the command reports the page as missing from the index

#### Scenario: Index entry points to a deleted page

- **WHEN** `wiki/index.md` lists a page whose file no longer exists
- **THEN** the command reports the stale index entry

#### Scenario: Index grouping disagrees with page type

- **WHEN** an index entry is filed under a type grouping that differs from the
  page's actual `type`
- **THEN** the command reports the mis-grouped entry

### Requirement: Body-section validation

The `lint` command SHALL verify that pages whose `type` defines a fixed body
shape carry exactly the named sections that shape requires — `## Summary` and
`## Why this matters` for a `summary`, `## Answer` and `## Why this matters` for
an `analysis`. It SHALL report a page that is missing a required section or that
adds sections beyond the defined shape.

#### Scenario: Required section is missing

- **WHEN** a `summary` or `analysis` page lacks one of its required named
  sections
- **THEN** the command reports the missing section for that page

### Requirement: Tag-vocabulary reconciliation

The `lint` command SHALL collect the tag set used across the corpus and surface
inconsistencies for the curator: near-duplicate tags (casing, pluralization, or
hyphenation variants of one another) and singletons that appear to restate an
existing tag. It SHALL propose a canonical form for each cluster but SHALL NOT
merge tags on its own; the choice of canonical tag and which variants fold into
it SHALL be a curator decision made during the interview.

#### Scenario: Near-duplicate tags are clustered

- **WHEN** the corpus contains tags that are casing, plural, or hyphenation
  variants of one another
- **THEN** the command clusters them and proposes a canonical form for the
  curator to confirm

#### Scenario: Tag merges require approval

- **WHEN** the command proposes folding tag variants into a canonical tag
- **THEN** it does not rewrite any page's tags until the curator approves the
  merge

### Requirement: Repairs are optional and curator-gated

After reporting, the `lint` command SHALL offer to apply repairs through a
propose → coach → commit interview, separating mechanical fixes (restoring a
missing index entry, re-filing a page into the folder matching its `type`,
correcting a broken link to an unambiguous target) from judgment calls (tag
merges, choosing among multiple plausible link targets). It SHALL preview the
intended changes before writing and SHALL write nothing unless the curator
commits. It SHALL never edit or rename a file under `raw/`. On commit it SHALL
append one `## [<date>] lint: <subject>` entry to `wiki/log.md` without
rewriting existing entries.

#### Scenario: Repairs apply only on commit

- **WHEN** the command proposes repairs and the curator does not commit
- **THEN** the wiki is left unchanged

#### Scenario: Mechanical and judgment fixes are separated

- **WHEN** the command proposes repairs
- **THEN** mechanical fixes are distinguished from judgment calls so the curator
  can approve them independently

#### Scenario: raw twins are never modified

- **WHEN** lint applies any repair
- **THEN** no file under `raw/` is edited or renamed

#### Scenario: Committed run is logged

- **WHEN** the curator commits one or more repairs
- **THEN** a single `## [<date>] lint: <subject>` entry is appended to
  `wiki/log.md` without rewriting existing entries

### Requirement: Coverage advisory for emergent conventions

After running its fixed set of checks, the `lint` command SHALL perform a
read-only advisory pass that surfaces recurring patterns the corpus exhibits but
that no current check governs — for example, a front-matter field used on
several pages that the schema does not define, or a body section recurring
outside the defined shapes. For each pattern it SHALL describe a candidate new
check or convention for the curator to consider. This pass SHALL be purely
advisory: it SHALL NOT treat such patterns as defects, propose repairs for them,
or modify any file, and adopting a candidate into the validity rules SHALL
remain a curator decision recorded in `CLAUDE.md` rather than an action `lint`
takes on its own.

#### Scenario: Emergent pattern is surfaced as a candidate

- **WHEN** several pages share a structure no current check governs (such as an
  undefined front-matter field)
- **THEN** the command surfaces it as a candidate new check or convention,
  distinct from the defect findings, rather than ignoring it

#### Scenario: Coverage advisory never acts

- **WHEN** the coverage advisory surfaces a candidate convention
- **THEN** the command proposes no repair for it and modifies no file; adopting
  it is left to the curator updating `CLAUDE.md`
