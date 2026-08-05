## ADDED Requirements

### Requirement: Page prose is independent of corpus membership

A knowledge page's prose SHALL describe its subject, and SHALL NOT assert what the
wiki does or does not contain. The governing test is **falsifiability by ingest**: a
sentence is disallowed when ingesting some plausible future source would make it
false. This applies to every knowledge page type and to both authoring paths, and it
covers two classes of claim:

- **Presence or absence** — that a work is or is not an ingested source, that no page
  covers some topic, or that a page is the corpus's first on a subject.
- **Corpus-scoped superlatives and counts** — that something is the corpus's only,
  best, or earliest instance of a thing, or a count of how many pages mention it.

Where an absence would otherwise be stated, the page SHALL name what is true of the
subject and stop, rather than reporting what the corpus lacks.

Two things are explicitly **not** violations. **Sibling orientation** — situating a
subject among related pages, such as noting that an implementation sits alongside
other implementations the wiki covers — is permitted, because a later ingest adds to
such a grouping without falsifying it. **Superlatives scoped to a source** rather than
to the corpus are permitted, because their truth does not depend on corpus membership.

This constraint SHALL NOT apply to `wiki/log.md`, whose entries are dated,
append-only records of what was true when written.

#### Scenario: Absence claim is refused at authoring

- **WHEN** a page would state that some work is not an ingested source, or that no
  page in the wiki covers a topic
- **THEN** that claim is not written; the page names what is true of the subject
  instead

#### Scenario: Corpus-scoped superlative is refused at authoring

- **WHEN** a page would state that its subject is the corpus's only, first, or best
  instance of something, or would count the pages that mention it
- **THEN** that claim is not written

#### Scenario: Sibling orientation is permitted

- **WHEN** a hub page situates its subject among related pages the wiki already holds,
  without ranking them or asserting completeness
- **THEN** the prose is conformant and SHALL NOT be flagged or removed

#### Scenario: Source-scoped superlative is permitted

- **WHEN** a summary states a superlative about the source it summarizes, such as the
  only measurement that source reports
- **THEN** the prose is conformant, because a later ingest cannot falsify it

#### Scenario: Log entries are exempt

- **WHEN** a `wiki/log.md` entry records that no ingested source covered a topic at the
  time the entry was written
- **THEN** that entry is conformant and is never rewritten
