# corpus-query Specification

## Purpose

Answer a natural-language question against the wiki corpus with cited,
corpus-grounded synthesis, and optionally file the answer back as an `analysis`
page under a curator-gated commit. This is the `query` command — the producer of
the `analysis` page type the taxonomy defines — turning the wiki from a
write-only archive into a knowledge base whose explorations compound.

## Requirements

### Requirement: Corpus-grounded answers

The `query` command SHALL answer a natural-language question using the content
of the wiki corpus. It SHALL survey `wiki/index.md` to locate candidate pages,
read the relevant `summary`, `entity`, and `concept` pages, and synthesize an
answer from what those pages say. The answer SHALL cite the pages it draws on
using Obsidian `[[wikilinks]]` that resolve by filename.

#### Scenario: Answer is drawn from corpus pages

- **WHEN** the user asks a question the wiki covers
- **THEN** the command produces an answer synthesized from the relevant wiki
  pages, with `[[wikilinks]]` to those pages as citations

#### Scenario: Retrieval starts from the index

- **WHEN** the command begins answering a question
- **THEN** it consults `wiki/index.md` to identify candidate pages before
  reading page bodies, rather than reading the whole corpus blindly

### Requirement: Honesty about corpus coverage

The `query` command SHALL NOT present outside knowledge as if it came from the
wiki. When the corpus does not cover the question, or covers it only partially,
the command SHALL say so plainly. Any answer content that is not grounded in a
wiki page SHALL be clearly marked as not corpus-backed, and the command MAY
suggest filing a source to close the gap.

#### Scenario: Corpus does not cover the question

- **WHEN** the user asks a question for which no relevant wiki page exists
- **THEN** the command states that the corpus does not cover it rather than
  fabricating a cited answer, and may suggest filing a source

#### Scenario: Outside knowledge is marked

- **WHEN** the command supplements a partial corpus answer with outside
  knowledge
- **THEN** the outside-knowledge portion is explicitly marked as not
  corpus-backed and carries no false `[[wikilink]]` citation

### Requirement: Filing the answer is optional and curator-gated

The `query` command SHALL answer the question without writing any files by
default. After answering, it SHALL offer to file the answer as an `analysis`
page through a propose → coach → commit interview, and SHALL write nothing to
the wiki unless the user commits. Abandoning the command after the answer SHALL
leave the wiki unchanged.

#### Scenario: Quick lookup writes nothing

- **WHEN** the user asks a question and does not ask to file the answer
- **THEN** no files under `wiki/` are created or modified

#### Scenario: Answer is filed only on commit

- **WHEN** the command proposes filing the answer as an `analysis` page
- **THEN** the `analysis` page and bookkeeping updates are written only after
  the user commits, and the user can revise the proposed title, tags, and links
  first

### Requirement: Analysis page schema and dual voice

When filed, an `analysis` page SHALL be written to `wiki/analyses/<slug>.md`
with `type: analysis` and front-matter carrying `title`, `created` (today),
`question` (the original question), `tags`, and `sources` (the cited pages). Its
body SHALL carry two distinct voices: a `## Answer` section containing the LLM's
corpus-grounded synthesis with inline `[[wikilinks]]`, and a `## Why this
matters` section containing the curator's own commentary, collected during the
interview. The slug SHALL derive from the final title, with a numeric suffix on
collision.

#### Scenario: Analysis page carries required front-matter

- **WHEN** an `analysis` page is committed
- **THEN** its front-matter contains `type: analysis`, `title`, `created`,
  `question`, `tags`, and `sources`, and the page lives under `wiki/analyses/`

#### Scenario: Both voices are present

- **WHEN** an `analysis` page is committed
- **THEN** it contains a `## Answer` section authored by the LLM and a `## Why
  this matters` section authored from the user's commentary

#### Scenario: Invalid type is rejected

- **WHEN** a page would be written with a `type` outside the defined set
- **THEN** the command halts and reports the discrepancy rather than writing the
  page

### Requirement: Bookkeeping updates on filing an analysis

When an `analysis` page is filed, the `query` command SHALL update
`wiki/index.md` to list the new page under its `Analyses` grouping as a
`[[wikilink]]` with a one-line summary, and SHALL append one greppable entry to
`wiki/log.md` of the form `## [<date>] query: <subject>` without rewriting
existing entries. Where appropriate it SHALL add a `[[wikilink]]` from a cited
hub page back to the analysis.

#### Scenario: Index gains the analysis

- **WHEN** an `analysis` page is committed
- **THEN** `wiki/index.md` is updated to include a `[[wikilink]]` to it with a
  one-line summary under the `Analyses` grouping

#### Scenario: Log records the query

- **WHEN** an `analysis` page is committed
- **THEN** a new `## [<date>] query: <subject>` entry is appended to
  `wiki/log.md` without rewriting existing entries

### Requirement: Tag vocabulary consistency at query time

When proposing tags for an `analysis` page, the `query` command SHALL prefer
tags already in use elsewhere in the wiki over minting new ones, and SHALL
surface any genuinely new tag explicitly for the user to approve or redirect
before commit. Corpus-wide tag reconciliation remains out of scope and deferred
to the future `lint` command.

#### Scenario: Existing tags are preferred

- **WHEN** the command proposes tags for an analysis page
- **THEN** it draws from tags already used in the wiki where they apply rather
  than inventing near-duplicates

#### Scenario: New tags are surfaced for approval

- **WHEN** the command proposes a tag not already present in the wiki
- **THEN** it flags the tag as new during the interview so the user can approve
  or redirect it before commit
