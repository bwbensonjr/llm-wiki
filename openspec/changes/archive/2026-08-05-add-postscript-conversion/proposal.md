## Why

PostScript is how a large part of the pre-2000 programming-languages literature is
still published — author pages and university tech-report servers host `.ps` and
`.ps.gz` where no PDF was ever made. Today the capture pipeline cannot read any of it:
PostScript falls through the router's "any other file type" arm to MarkItDown, which
raises `UnsupportedFormatException` ("No converter attempted a conversion"), so capture
writes nothing and the inbox entry parks.

This is not hypothetical. A corpus query on lambda lifting versus closure conversion
identified two gaps whose closing sources are PostScript-only:

- **Steckler & Wand, *Lightweight Closure Conversion* (TOPLAS 1997)** —
  `ccs.neu.edu/home/wand/papers/steckler-wand-97.ps`, served as
  `application/postscript`. This is the third sense of "closure conversion" that
  `wiki/concepts/closure-conversion.md` and `wiki/concepts/lambda-lifting.md` both flag
  as a terminological hazard without describing.
- **Shao & Appel, *Space-Efficient Closure Representations* (LFP 1994)** —
  `cs.princeton.edu/techreports/1994/454.ps.gz`, served as `application/x-gzip`. It is
  SML/NJ's closure-conversion algorithm published in the same venue and year as Twobit,
  the paper that says lifting and closure conversion are the same transformation.

The current workaround is for the curator to download, run `ps2pdf` by hand, and queue
the result as a local path in `inbox-files/` — the same manual recovery already used
three times for ACM papers. That workaround is fine for a one-off and wrong as a
standing policy: it puts a human in the loop for a purely mechanical step, and the
unattended path cannot perform it at all, so a queued `.ps` URL parks every time.

## What Changes

- **Add a PostScript route** to converter detection and routing. A source recognized as
  PostScript is converted to PDF with **ghostscript** and then handed to the **existing
  Docling route**; the composition is verified working end to end (see design).
- **Recognize PostScript by both content type and extension**, consistent with the
  existing precedence rule (fetched content type wins). `application/postscript` and
  `.ps`/`.eps` are PostScript.
- **Recognize gzipped PostScript.** This needs explicit handling on two counts: the
  served content type is `application/x-gzip`, which says nothing about the payload, and
  `os.path.splitext("454.ps.gz")` yields `.gz`, so neither existing path recognizes it.
  Decompression happens in memory before the ghostscript step.
- **Report the route honestly in the twin.** The raw twin's `converter:` field records
  what actually ran. A PostScript capture is a two-stage conversion, and the front-matter
  must not claim it was plain `docling`.
- **Fail with a diagnosable reason when ghostscript is absent.** ghostscript is an
  external system binary, not a Python dependency, so it can be missing on a machine
  where the rest of the pipeline works. The error must name the missing binary rather
  than surfacing a generic conversion failure.
- **No change to the all-or-nothing contract.** A PostScript failure at any stage writes
  no twin and no `wiki/` pages, exactly as every other route behaves.

Not in scope: DVI (Wand's POPL '94 version is `.dvi`), which needs a different tool
chain and has no queued source waiting on it. Worth revisiting only if a wanted paper is
DVI-only.

## Capabilities

### New Capabilities

None. This extends the existing converter router with another route rather than
introducing a new capability; a separate capability for one file format would fragment
requirements that belong with the router they govern.

### Modified Capabilities

- `resource-ingestion`: the **Content-type converter router** requirement gains the
  PostScript route, its gzip variant, and the two-stage reporting rule. The router
  requirement currently states that all non-PDF file types go to MarkItDown, which this
  change makes false as written.

## Impact

- **Code**: `wiki_ingest/detect.py` (a `POSTSCRIPT` route, extension and content-type
  recognition, gzip handling) and `wiki_ingest/convert.py` (a `_convert_postscript`
  that shells out to ghostscript into a temporary file, then delegates to
  `_convert_docling`). No change to `capture()`'s ordering, the twin write, or image
  localization — PostScript carries no localizable images, so it is unaffected by the
  Jina-only image path.
- **Tests**: `tests/` gains coverage for PostScript routing, gzip routing, the
  missing-ghostscript error, and the recorded converter name.
- **Dependencies**: **a new external system dependency, ghostscript** — the first
  non-Python tool the pipeline requires. `mise.toml` and the README/`CLAUDE.md`
  toolchain notes need to say so, and its absence must degrade to a clear error rather
  than a confusing one.
- **Skills**: `.claude/skills/file/SKILL.md` and `.claude/skills/ingest-inbox/SKILL.md`
  describe converter routing in prose ("web URL → Jina, PDF → Docling, any other file
  type → MarkItDown") and need the PostScript arm added. `CLAUDE.md`'s *Converter
  routing (Phase 1)* section is the binding statement and needs the same.
- **Corpus**: unblocks Steckler & Wand (verified end to end). **Shao & Appel turns out
  not to be unblocked**: its 1994 PostScript uses bitmap fonts, so the resulting PDF has
  no recoverable text layer and extraction yields glyph codes rather than characters.
  Capture refuses that rather than writing an unusable twin (see design decision 7), so
  the paper still needs a manual route until a decoder or OCR change lands. No existing
  `raw/` twin or `wiki/` page changes; nothing is re-captured.
- **No change** to `wiki/`, to the two-layer storage model, or to any curation command.
