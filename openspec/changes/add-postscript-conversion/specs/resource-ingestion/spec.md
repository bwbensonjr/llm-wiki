## MODIFIED Requirements

### Requirement: Content-type converter router

The `file` command SHALL detect the content type of the resource and route
conversion accordingly: web URLs to Jina Reader, PDFs to Docling, **PostScript to
ghostscript-then-Docling**, and all other file types to MarkItDown. Detection SHALL
consider the fetched content type, not the file extension alone, so that a URL
resolving to a PDF is routed to Docling.

A source SHALL be recognized as PostScript when its fetched content type is
`application/postscript`, or when its path carries a PostScript extension (`.ps`,
`.eps`). A **gzipped** PostScript source SHALL also be recognized, by its `.ps.gz` path
even though the trailing extension is `.gz` and even though its served content type
(commonly `application/x-gzip`) does not identify the payload; it SHALL be decompressed
before conversion.

PostScript conversion is **two-stage**: ghostscript renders the source to PDF and the
existing Docling route converts that PDF to Markdown. The raw twin's `converter:` field
SHALL record that both stages ran rather than naming Docling alone, so the twin does not
misreport how it was produced.

Because ghostscript is an external system binary rather than a Python dependency, its
absence SHALL produce a failure that names the missing binary, distinguishable from a
source the converter could not parse.

#### Scenario: Web URL routes to Jina Reader

- **WHEN** the user files an `http(s)` URL that resolves to an HTML page
- **THEN** the resource is converted with Jina Reader

#### Scenario: PDF routes to Docling

- **WHEN** the user files a PDF, whether a local path or a URL resolving to PDF
  content
- **THEN** the resource is converted with Docling

#### Scenario: PostScript routes to ghostscript then Docling

- **WHEN** the user files a PostScript source, whether a local `.ps` path or a URL
  served as `application/postscript`
- **THEN** ghostscript converts it to PDF, Docling converts that PDF to Markdown, and
  the twin records the two-stage route

#### Scenario: Gzipped PostScript is recognized and decompressed

- **WHEN** the user files a `.ps.gz` source, whose trailing extension is `.gz` and whose
  served content type does not identify the payload
- **THEN** it is recognized as PostScript, decompressed, and converted by the same
  two-stage route

#### Scenario: Missing ghostscript is reported as such

- **WHEN** a PostScript source is filed on a machine where the ghostscript binary is not
  on `PATH`
- **THEN** conversion fails naming the missing binary, no twin is written, and the
  failure is distinguishable from unparseable content

#### Scenario: Other file types route to MarkItDown

- **WHEN** the user files a non-PDF, non-PostScript document such as `.docx`, `.pptx`,
  `.xlsx`, or an image
- **THEN** the resource is converted with MarkItDown
