## Context

`wiki_ingest/detect.py` classifies a source into one of three routes and
`wiki_ingest/convert.py` runs the matching converter, producing Markdown in memory before
a single all-or-nothing twin write. The router's fall-through arm sends everything that is
not PDF or HTML to MarkItDown:

```python
def _route_from_extension(path):
    ext = os.path.splitext(path)[1].lower()
    if ext in PDF_EXTENSIONS:   return DOCLING
    if ext in HTML_EXTENSIONS:  return JINA
    return MARKITDOWN
```

PostScript therefore reaches MarkItDown, which rejects it. Measured on this machine:

| Step | Result |
|---|---|
| `MarkItDown().convert("steckler-wand-97.ps")` | raises `UnsupportedFormatException` — "No converter attempted a conversion, suggesting that the filetype is simply not supported" |
| `curl` of the same URL | HTTP 200, 492 KB, `application/postscript`, DSC 2.0, 39 pages |
| `ps2pdf sw97.ps sw97.pdf` | 0.66 s wall, valid `PDF 1.4, 39 pages`, 427 KB |
| `DocumentConverter().convert("sw97.pdf")` | 92,821 chars of Markdown; title and both authors correct |

So the capability gap is entirely in routing — the tools to do the job are already here
(Docling) or already installed (ghostscript 10.07.0 via Homebrew).

Content types observed on the two sources that motivate this: Wand's site serves `.ps` as
`application/postscript`; Princeton's tech-report server serves `.ps.gz` as
`application/x-gzip`.

## Goals / Non-Goals

**Goals:**

- Capture PostScript sources on both paths, including the unattended one, with no manual
  pre-conversion step.
- Handle gzipped PostScript, since that is how tech-report servers actually publish it.
- Keep the all-or-nothing twin-write contract exactly as it is.
- Make a missing ghostscript diagnosable rather than mysterious.
- Report the two-stage route truthfully in the immutable twin.

**Non-Goals:**

- DVI support. Different tool chain (`dvipdfm`/`dvips`), and no source is waiting on it.
- Improving Docling's extraction quality, or post-processing the ligature artifacts
  described under Risks. The twin is a mechanical transcript and stays one.
- Re-capturing anything already in `raw/`. Twins are immutable.
- Any `wiki/` change. This is Phase 1 only.

## Decisions

**1. Convert via ghostscript to PDF, then reuse the Docling route — do not add a third
converter.**

PostScript is a page-description language, not a document format with extractable
structure; anything that reads it usefully rasterizes or interprets it first. Rendering to
PDF and delegating means all the layout, table, and figure handling the pipeline already
gets from Docling applies unchanged, and PostScript inherits future Docling improvements
for free.

*Alternative considered:* find a Python PostScript-to-text library and add it as a
MarkItDown-peer converter. Rejected — it would produce a second, worse extraction path
whose output quality differs from every other document in `raw/`, for a format where the
two-stage route is already verified to work.

**2. Shell out to the `gs` binary rather than `ps2pdf`.**

`ps2pdf` is a shell wrapper around `gs`; invoking `gs` directly with explicit arguments
(`-dNOPAUSE -dBATCH -sDEVICE=pdfwrite -sOutputFile=…`) avoids depending on the wrapper
being installed and makes the invocation auditable. `ps2pdf` is what a human types; `gs`
is what a program should call.

**3. A new `POSTSCRIPT` route constant, not a flag on the Docling route.**

The route name is what the twin's `converter:` field records and what the CLI reports as
JSON, so it has to be a distinct value — a PostScript capture that reported `docling`
would misdescribe an immutable artifact. Record it as `ghostscript+docling`, which names
both stages in the order they ran.

*Alternative considered:* record `docling` and mention ghostscript nowhere. Rejected: the
twin is the audit record of how its own content was produced, and `raw/` cannot be
corrected later.

**4. Recognize gzip by path, and decompress before dispatch.**

Two mechanisms both fail on `.ps.gz`: `os.path.splitext` returns `.gz`, and the served
content type `application/x-gzip` describes the envelope rather than the payload. So the
extension check must look at the **full path suffix** (`.ps.gz`) rather than one
extension, and the content-type check must not be trusted to identify a gzip payload.
Decompression happens in memory into the temporary file handed to ghostscript, so no
intermediate artifact is left in the repo.

Sniffing the decompressed bytes for the `%!PS` magic would be more robust than trusting
the name, and is cheap — worth doing as a confirmation, but the routing decision stays
name-driven so that detection needs no download.

**5. Temporary files, never `raw/` scratch space.**

The intermediate PDF is written to a `tempfile` directory and deleted. `raw/` holds twins
and localized assets, nothing else; writing scratch there would create files that look
like content and that the immutability rule then forbids cleaning up.

**6. Missing ghostscript is its own error, raised before conversion is attempted.**

Check for the binary with `shutil.which("gs")` and raise `ConversionError` naming it. This
is the one new failure mode a machine can have while every other route still works, and
the unattended path will write the message into an `inbox.md` park annotation where the
curator reads it — so the message has to be actionable on its own ("ghostscript (`gs`) not
found on PATH"), not a wrapped subprocess traceback.

**7. Refuse a conversion that yields glyph codes instead of text; defer recovery.**

*Added during implementation, after the second verification source failed.* Shao & Appel's
`.ps.gz` converts to a structurally valid twin containing no prose: 95.6% of its tokens are
unresolved glyph codes (`/65/98/115/116/114/97/99/116` where "Abstract" belongs). The cause
is bitmap (PK) fonts — the ghostscript-produced PDF carries no `ToUnicode` map, so *no* PDF
text extractor can recover characters and Docling falls back to emitting glyph names.

Capture refuses such output rather than writing it. A twin that parses but says nothing is
worse than no twin, because `raw/` is immutable and the authoring step would then write a
confident summary of nothing — the exact failure the unattended path's plausibility check
exists to prevent, arriving in a form that check would not catch.

The test is the ratio of bare `/NNN` tokens to all tokens. Measured on the two real papers
this separates cleanly — **0.021** for the good twin, **0.956** for the unusable one — so
the threshold sits at **0.25**, an order of magnitude clear of the good case and well below
the bad one. The good twin's 2.1% comes from genuine symbol runs, which is why the check
counts a ratio rather than any occurrence.

*Recovery is deliberately deferred.* The text is mechanically recoverable: decoding those
codes through the TeX OT1 encoding (with slots 11–15 as the ff/fi/fl/ffi/ffl ligatures)
reproduces the text exactly — verified on the abstract. But a TeX-encoding decoder is a
distinct capability, assumes OT1 where T1/Cork sources differ, and would make the twin
something other than a mechanical transcript. It belongs in its own change, and this
check is the trigger such a change would need anyway.

*Alternative considered:* force Docling to OCR the rendered pages, since RapidOCR is
already installed. Rejected for now on the same scope grounds, and because it needs this
same detection to know when to fire.

## Risks / Trade-offs

- **A new external system dependency.** ghostscript is the first non-Python tool the
  pipeline needs, so "clone and `uv sync`" no longer suffices. Mitigation: declare it in
  `mise.toml` if a suitable backend exists, document it in `CLAUDE.md`'s toolchain
  section either way, and make its absence a clear, single-line error. Every other route
  keeps working without it, so the degradation is scoped to PostScript sources.
- **Old dvips output extracts with systematic ligature corruption.** Verified on the
  Steckler & Wand paper: `fl` renders as `/`, giving `/ow analysis` for "flow analysis",
  `pro/tocols`, and `PAUL A/. STECKLER`. This is a font-encoding artifact of 1997
  dvips-produced PostScript, not a ghostscript or Docling defect, and `raw/` is immutable
  so it persists in the twin. Accepted: the text is entirely legible to the LLM authoring
  the summary (the abstract above reads fine), and the `wiki/` layer is a distillation
  rather than a transcript. Worth a note in the ingest log entry when it is conspicuous,
  so a later reader does not mistake it for a broken converter. **This is a different case
  from the glyph-code failure in decision 7, and the distinction matters**: legible-with-
  artifacts is authored from normally, while no-recoverable-text is refused. Both skills
  say so explicitly, so the tolerance for one is not read as tolerance for the other.
- **Bitmap-font sources remain un-ingestable.** The check in decision 7 keeps them out of
  the corpus but does not convert them, so Shao & Appel still needs the manual route
  (`ps2pdf` by hand is not enough either — the font problem is upstream of the container).
  The gap this change was partly meant to close stays open for that paper until a decoder
  or OCR change lands.
- **Ghostscript is a large attack surface for untrusted input.** PostScript is a
  programming language and `gs` has a history of sandbox-escape CVEs. Mitigation: run with
  `-dSAFER` (the default in modern releases, but set it explicitly), and note that inputs
  here are curator-chosen academic papers rather than arbitrary web content.
- **Silent quality cliff on figure-heavy sources.** A PostScript paper whose figures are
  vector drawings converts to a PDF whose figures Docling may not describe. No worse than
  the existing PDF route, and the unattended path's figure judgment already handles
  undecoded images by distilling captions.
- **Detection cost.** None added: PostScript is recognized from the content type or the
  path, both already available at detection time. No extra network round trip.

## Migration Plan

1. Add the route constant, extension set, and gzip-aware recognition in `detect.py`, with
   unit tests for `.ps`, `.eps`, `.ps.gz`, `application/postscript`, and the
   `application/x-gzip` case.
2. Add `_convert_postscript` in `convert.py`: `shutil.which` guard, gzip decompression,
   `gs` invocation into a temp file, delegate to `_convert_docling`, clean up.
3. Wire the route into `convert()` and confirm `capture()` records
   `converter: ghostscript+docling`.
4. Update the prose that describes routing: `CLAUDE.md` *Converter routing (Phase 1)*,
   `.claude/skills/file/SKILL.md`, `.claude/skills/ingest-inbox/SKILL.md`.
5. Verify end to end on the two motivating sources by queueing them in `inbox.md` and
   running the unattended path.

Rollback is `git revert`; nothing is stateful, and any twin already written from a
PostScript source stays valid since it is ordinary Markdown.

## Open Questions

- **Does `mise` have a usable ghostscript backend?** If not, the toolchain note becomes
  "install ghostscript yourself" (`brew install ghostscript`), which is weaker than the
  rest of the pinned toolchain. Worth checking during implementation; not a blocker,
  since the error path covers absence.
- **Should `.eps` really route here?** Encapsulated PostScript is usually a single figure
  rather than a document, so a captured `.eps` twin would be one page of a diagram with
  little text. Included for consistency, but a case could be made for treating a lone
  figure as out of scope for ingestion entirely.
