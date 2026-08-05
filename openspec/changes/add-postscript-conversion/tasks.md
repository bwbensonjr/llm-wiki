## 1. Detection and routing

- [x] 1.1 Add a `POSTSCRIPT = "ghostscript+docling"` route constant and a
      `POSTSCRIPT_EXTENSIONS = {".ps", ".eps"}` set to `wiki_ingest/detect.py`. The
      constant's value is what lands in the twin's `converter:` field, so it names both
      stages in the order they ran.
- [x] 1.2 Recognize PostScript by content type in `_route_from_content_type`:
      `application/postscript` routes to `POSTSCRIPT`. Place the check before the
      catch-all MarkItDown arm.
- [x] 1.3 Recognize PostScript by extension in both `_route_from_extension` and
      `_url_route_from_extension`. Match on the **full path suffix** so `.ps.gz` is
      caught — `os.path.splitext("454.ps.gz")` returns `.gz`, so a single-extension check
      silently misroutes it to MarkItDown.
- [x] 1.4 Ensure a gzip content type does not override a `.ps.gz` path. Princeton serves
      `application/x-gzip`, which describes the envelope and not the payload, so the
      content-type arm must not claim that source for MarkItDown.
- [x] 1.5 Add detection tests: local `.ps`, local `.ps.gz`, local `.eps`, a URL served
      `application/postscript`, a `.ps.gz` URL served `application/x-gzip`, and a
      regression case confirming `.docx` still routes to MarkItDown.

## 2. Conversion

- [x] 2.1 Add `_convert_postscript(source)` to `wiki_ingest/convert.py`. Guard first with
      `shutil.which("gs")` and raise `ConversionError` naming the missing binary
      (`ghostscript (gs) not found on PATH`) before any work — this message reaches the
      curator through an `inbox.md` park annotation, so it must be actionable alone.
- [x] 2.2 Fetch-or-read the source into a `tempfile` directory, decompressing in memory
      when the path is `.ps.gz`. Write no scratch files under `raw/`.
- [x] 2.3 Confirm the decompressed bytes begin with the `%!PS` magic, and raise a clear
      `ConversionError` if not — a name-based route that turns out not to be PostScript
      should say so rather than handing garbage to ghostscript.
- [x] 2.4 Invoke `gs` explicitly rather than the `ps2pdf` wrapper:
      `gs -dSAFER -dNOPAUSE -dBATCH -sDEVICE=pdfwrite -sOutputFile=<tmp.pdf> <tmp.ps>`.
      Set `-dSAFER` explicitly even though modern releases default to it. Raise
      `ConversionError` with ghostscript's stderr on non-zero exit.
- [x] 2.5 Delegate the produced PDF to `_convert_docling` and return its Markdown, so
      PostScript inherits the same extraction path as every other PDF. Clean up the temp
      directory on both success and failure.
- [x] 2.6 Wire `POSTSCRIPT` into `convert()`'s route dispatch.
- [x] 2.7 Add conversion tests: the missing-`gs` error path (monkeypatch `shutil.which`),
      a non-PostScript payload behind a `.ps` name, a ghostscript non-zero exit, and a
      success path asserting `_convert_docling` was delegated to.
- [x] 2.8 *(added during implementation — see design decision 7)* Refuse output dominated
      by unresolved `/NNN` glyph codes, which is what a bitmap-font source extracts to.
      Threshold on the ratio of glyph tokens to all tokens, set from the measured
      separation between a good twin (0.021) and an unusable one (0.956).
- [x] 2.9 Test the glyph-code check both ways: refuse coded output and write no twin, and
      confirm legible prose carrying ligature artifacts (`fl` → `/`) is still accepted, so
      the two cases are not conflated.

## 3. Capture integration

- [x] 3.1 Confirm `capture()` needs no ordering change and that a PostScript capture
      writes `converter: ghostscript+docling` in the twin front-matter.
- [x] 3.2 Confirm image localization stays Jina-only — PostScript must not enter the
      `localize()` path — and that `images` is `None` for a PostScript capture.
- [x] 3.3 Confirm the all-or-nothing contract holds: force a failure at each stage
      (missing binary, bad magic, `gs` failure, Docling failure) and assert no file is
      left under `raw/`.

## 4. Toolchain and documentation

- [x] 4.1 Determine whether `mise` has a usable ghostscript backend. If it does, pin it in
      `mise.toml`; if not, document `brew install ghostscript` and say plainly that this
      one tool is outside the pinned toolchain.
- [x] 4.2 Update `CLAUDE.md`'s *Converter routing (Phase 1)* section — the binding
      statement of routing — to add the PostScript arm, the gzip variant, and the
      ghostscript dependency.
- [x] 4.3 Update the routing prose in `.claude/skills/file/SKILL.md` and
      `.claude/skills/ingest-inbox/SKILL.md`, both of which currently say "any other file
      type → MarkItDown".
- [x] 4.4 Note in `ingest-inbox`'s guidance that a PostScript twin from old dvips output
      may carry ligature artifacts (`fl` → `/`), that this is a font-encoding artifact
      rather than a broken capture, and that it is worth mentioning in the log entry when
      conspicuous.

## 5. Verification

- [x] 5.1 Run the full test suite (`uv run pytest`) and confirm no regression in the
      existing detection, conversion, and image tests.
- [x] 5.2 Capture `https://www.ccs.neu.edu/home/wand/papers/steckler-wand-97.ps` (plain
      `.ps`, `application/postscript`) and confirm a twin is written with the two-stage
      converter recorded and legible body text. **Done:** twin written,
      `converter: ghostscript+docling`, `detected: application/postscript`, 92,953 bytes,
      correct title and authors, mild ligature artifacts as expected.
- [x] 5.3 Capture `https://www.cs.princeton.edu/techreports/1994/454.ps.gz` (gzipped,
      served `application/x-gzip`) and confirm the same. **Outcome differs:** routing and
      decompression both work, but the source's bitmap fonts leave no recoverable text
      layer, so it is now correctly refused (design decision 7) instead of writing an
      unusable twin. Verified refused at ratio 0.956 against the 0.25 limit.
- [x] 5.4 Queue in `inbox.md` and run the unattended path end to end, confirming a
      PostScript source ingests without a manual pre-conversion step — the whole point of
      the change. Scoped to Steckler & Wand, since Shao & Appel is refused by 5.3.
- [ ] 5.5 Temporarily shadow `gs` off `PATH` and confirm a queued PostScript entry parks
      with the actionable message rather than a traceback, and that no twin is left behind.
- [ ] 5.6 Run `lint` and confirm the corpus is clean after the two ingests.
