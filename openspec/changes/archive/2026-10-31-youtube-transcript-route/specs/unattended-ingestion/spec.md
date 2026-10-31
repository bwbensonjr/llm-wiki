## MODIFIED Requirements

### Requirement: Duplicate sources are skipped

Before capturing an entry, the unattended path SHALL check whether the entry's URL
or path already appears as the `source:` of an existing summary page. If it does,
the path SHALL skip capture and authoring entirely, write no `raw/` twin, and mark
the entry `- [x]` with an annotation identifying it as already ingested.

YouTube video URLs SHALL be compared by video ID, not literal string.

#### Scenario: Already-ingested link is skipped

- **WHEN** a queue entry's URL matches the `source:` of an existing summary
- **THEN** no new `raw/` twin or `wiki/` page is written and the entry is checked
  off as already ingested

#### Scenario: Re-running a drained inbox is a no-op

- **WHEN** the unattended path runs against an inbox whose entries are all
  `- [x]` or `- [!]`
- **THEN** no files are created or modified under `raw/` or `wiki/`

#### Scenario: Different share link for an ingested video is skipped

- **WHEN** a queue entry is `https://youtu.be/<id>?si=<token>` and an existing summary
  has `source: https://www.youtube.com/watch?v=<id>`
- **THEN** the entry is treated as already ingested, no new `raw/` twin or `wiki/` page
  is written, and the entry is checked off naming the existing page
