"""PostScript route: detection, two-stage conversion, and capture integration.

No test here runs ghostscript or Docling. Detection is pure, and the conversion
tests fake `subprocess.run` and `_convert_docling` so the route's own logic —
the missing-binary guard, gzip inflation, the magic check, and delegation — is
what gets exercised.
"""

import gzip
import subprocess

import pytest

from wiki_ingest import convert, detect
from wiki_ingest.convert import ConversionError

from .conftest import FakeSession

PS_BYTES = b"%!PS-Adobe-2.0\n%%Pages: 3\nshowpage\n"


# --- detection -------------------------------------------------------------


@pytest.mark.parametrize("name", ["paper.ps", "paper.eps", "paper.PS"])
def test_local_postscript_routes_to_postscript(tmp_path, name):
    path = tmp_path / name
    path.write_bytes(PS_BYTES)
    route, detected = detect.detect(str(path))
    assert route == detect.POSTSCRIPT
    assert detected == "file"


def test_local_gzipped_postscript_routes_to_postscript(tmp_path):
    """`os.path.splitext` sees only `.gz`, so this is the case a single-extension
    check silently misroutes to MarkItDown."""
    path = tmp_path / "454.ps.gz"
    path.write_bytes(gzip.compress(PS_BYTES))
    route, _ = detect.detect(str(path))
    assert route == detect.POSTSCRIPT


def test_url_served_as_postscript_routes_to_postscript():
    session = FakeSession(content_type="application/postscript")
    route, detected = detect.detect(
        "https://www.ccs.neu.edu/home/wand/papers/steckler-wand-97.ps",
        session=session,
    )
    assert route == detect.POSTSCRIPT
    assert detected == "application/postscript"


def test_gzip_content_type_does_not_override_a_ps_gz_path():
    """Princeton serves `.ps.gz` as `application/x-gzip`, which describes the
    envelope. The path has to decide the route."""
    session = FakeSession(content_type="application/x-gzip")
    route, detected = detect.detect(
        "https://www.cs.princeton.edu/techreports/1994/454.ps.gz", session=session
    )
    assert route == detect.POSTSCRIPT
    assert detected == "application/x-gzip"


def test_gzip_content_type_on_a_non_postscript_path_still_falls_through():
    session = FakeSession(content_type="application/x-gzip")
    route, _ = detect.detect("https://example.com/archive.tar.gz", session=session)
    assert route == detect.MARKITDOWN


def test_other_file_types_still_route_to_markitdown(tmp_path):
    path = tmp_path / "notes.docx"
    path.write_bytes(b"stub")
    route, _ = detect.detect(str(path))
    assert route == detect.MARKITDOWN


def test_pdf_and_html_routes_are_unchanged(tmp_path):
    pdf = tmp_path / "paper.pdf"
    pdf.write_bytes(b"%PDF-1.4")
    assert detect.detect(str(pdf))[0] == detect.DOCLING
    session = FakeSession(content_type="text/html")
    assert detect.detect("https://example.com/post", session=session)[0] == detect.JINA


# --- conversion ------------------------------------------------------------


@pytest.fixture
def fake_ghostscript(monkeypatch):
    """Stand in for `gs`: record the argv and write a non-empty PDF."""
    calls = []

    def fake_run(command, **kwargs):
        calls.append(command)
        output = [a for a in command if a.startswith("-sOutputFile=")][0]
        path = output.split("=", 1)[1]
        with open(path, "wb") as handle:
            handle.write(b"%PDF-1.4 fake")
        return subprocess.CompletedProcess(command, 0, b"", b"")

    monkeypatch.setattr(convert.shutil, "which", lambda name: f"/usr/bin/{name}")
    monkeypatch.setattr(convert.subprocess, "run", fake_run)
    monkeypatch.setattr(convert, "_convert_docling", lambda source: "# Converted\n")
    return calls


def test_missing_ghostscript_names_the_binary(tmp_path, monkeypatch):
    monkeypatch.setattr(convert.shutil, "which", lambda name: None)
    path = tmp_path / "paper.ps"
    path.write_bytes(PS_BYTES)
    with pytest.raises(ConversionError) as excinfo:
        convert.convert(str(path), detect.POSTSCRIPT)
    message = str(excinfo.value)
    assert "ghostscript (gs) not found on PATH" in message
    # The unattended path writes this into an inbox annotation, so it has to say
    # what to do without any surrounding context.
    assert "install" in message


def test_non_postscript_payload_behind_a_ps_name_is_refused(tmp_path, monkeypatch):
    monkeypatch.setattr(convert.shutil, "which", lambda name: "/usr/bin/gs")
    path = tmp_path / "mislabeled.ps"
    path.write_bytes(b"<!doctype html><html>not postscript</html>")
    with pytest.raises(ConversionError, match="does not begin with"):
        convert.convert(str(path), detect.POSTSCRIPT)


def test_ghostscript_failure_surfaces_its_stderr(tmp_path, monkeypatch):
    monkeypatch.setattr(convert.shutil, "which", lambda name: "/usr/bin/gs")

    def failing_run(command, **kwargs):
        return subprocess.CompletedProcess(command, 1, b"", b"gs: syntax error")

    monkeypatch.setattr(convert.subprocess, "run", failing_run)
    path = tmp_path / "paper.ps"
    path.write_bytes(PS_BYTES)
    with pytest.raises(ConversionError) as excinfo:
        convert.convert(str(path), detect.POSTSCRIPT)
    assert "exited 1" in str(excinfo.value)
    assert "syntax error" in str(excinfo.value)


def test_empty_ghostscript_output_is_refused(tmp_path, monkeypatch):
    monkeypatch.setattr(convert.shutil, "which", lambda name: "/usr/bin/gs")

    def silent_run(command, **kwargs):
        return subprocess.CompletedProcess(command, 0, b"", b"")

    monkeypatch.setattr(convert.subprocess, "run", silent_run)
    path = tmp_path / "paper.ps"
    path.write_bytes(PS_BYTES)
    with pytest.raises(ConversionError, match="produced no PDF output"):
        convert.convert(str(path), detect.POSTSCRIPT)


def test_success_delegates_to_docling_with_safer_set(tmp_path, fake_ghostscript):
    path = tmp_path / "paper.ps"
    path.write_bytes(PS_BYTES)
    assert convert.convert(str(path), detect.POSTSCRIPT) == "# Converted\n"
    argv = fake_ghostscript[0]
    assert "-dSAFER" in argv
    assert "-sDEVICE=pdfwrite" in argv
    # `gs` directly, never the ps2pdf wrapper.
    assert argv[0].endswith("/gs")


def test_gzipped_source_is_decompressed_before_ghostscript(tmp_path, fake_ghostscript):
    path = tmp_path / "454.ps.gz"
    path.write_bytes(gzip.compress(PS_BYTES))
    assert convert.convert(str(path), detect.POSTSCRIPT) == "# Converted\n"


def test_gzip_is_detected_by_magic_not_by_name(tmp_path, fake_ghostscript):
    """A gzipped payload served under a bare `.ps` name still inflates, because
    decompression keys off the bytes rather than the path."""
    path = tmp_path / "compressed-but-unnamed.ps"
    path.write_bytes(gzip.compress(PS_BYTES))
    assert convert.convert(str(path), detect.POSTSCRIPT) == "# Converted\n"


def test_url_source_is_downloaded_then_converted(fake_ghostscript):
    class PostScriptSession(FakeSession):
        def get(self, url, **kwargs):
            from .conftest import FakeResponse

            return FakeResponse(content=PS_BYTES)

    session = PostScriptSession(content_type="application/postscript")
    markdown = convert.convert(
        "https://example.com/paper.ps", detect.POSTSCRIPT, session=session
    )
    assert markdown == "# Converted\n"


def test_no_temporary_files_survive(tmp_path, fake_ghostscript):
    path = tmp_path / "paper.ps"
    path.write_bytes(PS_BYTES)
    convert.convert(str(path), detect.POSTSCRIPT)
    # The temp dir is the only place scratch is written; nothing lands beside
    # the source, and nothing is left under raw/.
    assert sorted(p.name for p in tmp_path.iterdir()) == ["paper.ps"]


# --- unrecoverable glyph codes ---------------------------------------------

# What a bitmap-font source actually extracts to: "Abstract" as decimal codes.
GLYPH_CODED = "## /65/98/115/116/114/97/99/116\n\n" + " ".join(
    ["/77/97/110/121"] * 200
)


def test_glyph_coded_output_is_refused(tmp_path, monkeypatch, fake_ghostscript):
    monkeypatch.setattr(convert, "_convert_docling", lambda source: GLYPH_CODED)
    path = tmp_path / "bitmap-fonts.ps"
    path.write_bytes(PS_BYTES)
    with pytest.raises(ConversionError) as excinfo:
        convert.convert(str(path), detect.POSTSCRIPT)
    message = str(excinfo.value)
    assert "glyph codes" in message
    assert "bitmap fonts" in message
    # Actionable on its own, since it reaches the curator as a park annotation.
    assert "by hand" in message


def test_glyph_coded_capture_writes_no_twin(tmp_path, monkeypatch, fake_ghostscript):
    monkeypatch.setattr(convert, "_convert_docling", lambda source: GLYPH_CODED)
    source = tmp_path / "bitmap-fonts.ps"
    source.write_bytes(PS_BYTES)
    raw_dir = tmp_path / "raw"
    with pytest.raises(ConversionError):
        convert.capture(str(source), raw_dir=str(raw_dir))
    assert not raw_dir.exists() or list(raw_dir.glob("*.md")) == []


def test_ordinary_prose_with_stray_slashes_is_kept(tmp_path, monkeypatch,
                                                   fake_ghostscript):
    """The tolerable case: dvips ligature artifacts render `fl` as `/`, which must
    not trip the glyph-code check."""
    artifacted = (
        "Lightweight Closure Conversion PAUL A/. STECKLER and MITCHELL WAND\n\n"
        "We formulate the /ow analysis as a deductive system, with multiple "
        "procedure call pro/tocols coexisting in the same code/.\n"
    )
    monkeypatch.setattr(convert, "_convert_docling", lambda source: artifacted)
    path = tmp_path / "paper.ps"
    path.write_bytes(PS_BYTES)
    assert convert.convert(str(path), detect.POSTSCRIPT) == artifacted


@pytest.mark.parametrize(
    "markdown,expected",
    [
        ("", 0.0),
        ("plain prose with no codes", 0.0),
        ("/65/98/115 /116/114/97", 1.0),
        ("half /65/98 and /116/114 real words here", 2 / 7),
    ],
)
def test_glyph_code_ratio(markdown, expected):
    assert convert._glyph_code_ratio(markdown) == pytest.approx(expected)


# --- capture integration ---------------------------------------------------


def test_capture_records_the_two_stage_converter(tmp_path, fake_ghostscript):
    source = tmp_path / "paper.ps"
    source.write_bytes(PS_BYTES)
    raw_dir = tmp_path / "raw"
    result = convert.capture(str(source), raw_dir=str(raw_dir))
    assert result.converter == "ghostscript+docling"
    twin = result.raw_path.read_text()
    assert "converter: ghostscript+docling" in twin
    assert f"source: {source}" in twin


def test_capture_of_postscript_localizes_no_images(tmp_path, fake_ghostscript):
    source = tmp_path / "paper.ps"
    source.write_bytes(PS_BYTES)
    result = convert.capture(str(source), raw_dir=str(tmp_path / "raw"))
    # Image localization is Jina-only; PostScript must not enter that path.
    assert result.images is None
    assert not (tmp_path / "raw" / "assets").exists()


@pytest.mark.parametrize(
    "break_stage",
    ["missing_binary", "bad_magic", "ghostscript_failure", "docling_failure"],
)
def test_failure_at_any_stage_writes_no_twin(tmp_path, monkeypatch, break_stage):
    source = tmp_path / "paper.ps"
    source.write_bytes(PS_BYTES)
    raw_dir = tmp_path / "raw"

    monkeypatch.setattr(convert.shutil, "which", lambda name: "/usr/bin/gs")

    def ok_run(command, **kwargs):
        output = [a for a in command if a.startswith("-sOutputFile=")][0]
        with open(output.split("=", 1)[1], "wb") as handle:
            handle.write(b"%PDF-1.4 fake")
        return subprocess.CompletedProcess(command, 0, b"", b"")

    monkeypatch.setattr(convert.subprocess, "run", ok_run)
    monkeypatch.setattr(convert, "_convert_docling", lambda s: "# Converted\n")

    if break_stage == "missing_binary":
        monkeypatch.setattr(convert.shutil, "which", lambda name: None)
    elif break_stage == "bad_magic":
        source.write_bytes(b"not postscript at all")
    elif break_stage == "ghostscript_failure":
        monkeypatch.setattr(
            convert.subprocess,
            "run",
            lambda command, **kw: subprocess.CompletedProcess(command, 1, b"", b"boom"),
        )
    elif break_stage == "docling_failure":

        def exploding(source_path):
            raise ConversionError("Docling could not convert source")

        monkeypatch.setattr(convert, "_convert_docling", exploding)

    with pytest.raises(ConversionError):
        convert.capture(str(source), raw_dir=str(raw_dir))
    assert not raw_dir.exists() or list(raw_dir.glob("*.md")) == []
