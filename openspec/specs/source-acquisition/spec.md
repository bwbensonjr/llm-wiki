# source-acquisition Specification

## Purpose

Defines how capture obtains a source's content before it is written as a raw twin:
the ordered fallback candidates tried when the routed fetch fails, the mechanical
detection of stub pages, the provenance recorded for whatever succeeded, and the
limits on what acquisition may do.

## Requirements

### Requirement: Fallback acquisition chain

When the routed fetch for a URL source fails or yields a stub, capture SHALL try
further candidates in a fixed order before failing: known publisher URL rewrites,
DOI-based open-access lookup, a direct fetch converted locally, and an archived
snapshot. Each candidate SHALL be converted by the ordinary content-type router.
The first candidate that converts to a non-stub result SHALL be written as the twin.

#### Scenario: ACM reader URL is rewritten to the PDF URL

- **WHEN** a source `https://dl.acm.org/doi/epdf/<doi>` yields a loading shell
- **THEN** capture tries `https://dl.acm.org/doi/pdf/<doi>`, and if that converts,
  writes the twin from it

#### Scenario: Open-access copy is found by DOI

- **WHEN** a publisher URL carrying a DOI fails and an open-access lookup for that DOI
  returns a PDF location on another host
- **THEN** capture converts that PDF and writes the twin from it

#### Scenario: Jina refusal falls back to a direct fetch

- **WHEN** Jina Reader is refused for an HTML page (for example HTTP 403) but the
  page itself is reachable directly
- **THEN** capture fetches the HTML directly, converts it locally, and writes the
  twin from it

#### Scenario: Unreachable host falls back to an archived snapshot

- **WHEN** a source's host cannot be reached and an archived snapshot of that URL
  exists
- **THEN** capture converts the snapshot's original content and writes the twin
  from it

#### Scenario: Primary success tries nothing else

- **WHEN** the routed fetch converts to a non-stub result
- **THEN** no fallback candidate is requested

### Requirement: Open-access lookup by DOI

Capture SHALL extract a DOI from `doi.org` URLs and from publisher URLs that embed
one, and SHALL query open-access indexes for that DOI. A keyless index SHALL always
be queried; an index that requires a contact email SHALL be queried only when the
curator has configured one. A title search of a preprint server SHALL accept only a
match whose title agrees with the DOI's recorded title.

#### Scenario: DOI is extracted from a publisher URL

- **WHEN** the source is `https://link.springer.com/content/pdf/10.1023/A:1010016816429.pdf`
- **THEN** the DOI `10.1023/A:1010016816429` is used for the open-access lookup

#### Scenario: Email-gated index is skipped without configuration

- **WHEN** no contact email is configured
- **THEN** the email-gated index is not queried, and the keyless index still is

#### Scenario: Preprint with a different title is rejected

- **WHEN** a preprint title search returns a paper whose title does not agree with
  the DOI's title
- **THEN** that preprint is not used as a candidate

### Requirement: Stub pages are rejected before the twin write

Capture SHALL classify converted output as a stub, mechanically and before writing,
when it is a bot-check or captcha page, an HTTP error page rendered as content, a
JavaScript loading shell, or implausibly thin for a paper or article. A stub SHALL
count as a failed attempt; it SHALL NOT be written to `raw/`.

#### Scenario: Bot-check page writes no twin

- **WHEN** a candidate converts to a page titled "Just a moment..." with a bot-check
  body
- **THEN** that attempt is recorded as a stub and no twin is written for it

#### Scenario: Error page writes no twin

- **WHEN** a candidate converts to a "Page Not Found" page of a few dozen words
- **THEN** that attempt is recorded as a stub and no twin is written for it

### Requirement: Failure reports every attempt

When every candidate fails, capture SHALL write nothing and SHALL report, in its
error output, each attempt made with its URL and outcome, plus the best title known
for the source, so that the curator does not repeat attempts already made.

#### Scenario: Exhausted chain lists its attempts

- **WHEN** the routed fetch, the URL rewrite, the open-access lookup, and the
  archived snapshot all fail for a source
- **THEN** no file is written, and the error output lists each of those attempts
  with its outcome and names the source's title when one was learned

### Requirement: Acquisition provenance in the twin

A twin's `source:` SHALL always be the original source URL. The twin SHALL record
`acquired-via:` naming the step that produced its content, and SHALL record
`fetched-from:` with the URL actually fetched whenever it differs from `source:`.

#### Scenario: Open-access copy keeps the original source

- **WHEN** a twin is produced from an open-access copy found for a publisher URL
- **THEN** its `source:` is the publisher URL, its `fetched-from:` is the copy's
  URL, and its `acquired-via:` names the open-access step

#### Scenario: Primary fetch records no fetched-from

- **WHEN** a twin is produced by the routed fetch of its own URL
- **THEN** its `acquired-via:` names the primary route and it has no
  `fetched-from:` field

### Requirement: Local copy captured under its original URL

Capture SHALL accept a local file together with an original source URL. It SHALL
convert the file by the ordinary router, record the URL as `source:`, record the
file path as `local-copy:`, and record `acquired-via: manual`. Duplicate checks and
the summary's `source:` SHALL use the original URL.

#### Scenario: Hand-fetched PDF is filed under its paper URL

- **WHEN** the curator's copy `inbox-files/implicit-phasing-for-r6rs-libraries.pdf`
  is captured with original URL
  `https://legacy.cs.indiana.edu/~dyb/pubs/implicit-phasing.pdf`
- **THEN** the twin's `source:` is that URL, its `local-copy:` is the file path, and
  its `acquired-via:` is `manual`

### Requirement: Acquisition stays within ordinary access

Acquisition SHALL NOT attempt to defeat bot checks or captchas, SHALL NOT use
shadow libraries or other unauthorized copies, and SHALL NOT send curator personal
data to any service other than a contact email the curator explicitly configured
for an index that requires one.

#### Scenario: Bot check is reported, not bypassed

- **WHEN** every candidate for a source returns a bot-check page
- **THEN** capture fails reporting the bot check, and no attempt is made to solve or
  evade it

#### Scenario: No personal data without configuration

- **WHEN** no contact email is configured
- **THEN** no acquisition request carries any curator identifying information
