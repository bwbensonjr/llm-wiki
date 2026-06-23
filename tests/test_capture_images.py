"""Integration tests for image localization through `capture()`."""

import datetime

import pytest

from wiki_ingest.convert import ConversionError, capture

from .conftest import FakeSession

TODAY = datetime.date(2026, 6, 23)
SOURCE = "https://example.com/page"
STEM = "2026-06-23-test-figure-page"

AVATAR = "https://avatars.githubusercontent.com/u/1?s=64&v=4"
DIAGRAM = "https://example.com/diagram.png"

MARKDOWN = (
    "Title: Test Figure Page\n\n"
    "Markdown Content:\n"
    "# Test Figure Page\n\n"
    "Body text.\n\n"
    f"![Image 1: avatar]({AVATAR})\n\n"
    f"![Image 2: diagram]({DIAGRAM})\n"
)


def _capture(tmp_path, session, **kw):
    return capture(
        SOURCE, raw_dir=tmp_path / "raw", session=session, today=TODAY, **kw
    )


def test_default_capture_localizes_nothing(tmp_path, png_bytes):
    session = FakeSession(jina_markdown=MARKDOWN, images={DIAGRAM: png_bytes})
    result = _capture(tmp_path, session)  # no localize_images

    twin = (tmp_path / "raw" / f"{STEM}.md").read_text()
    assert DIAGRAM in twin  # original remote link retained
    assert "assets/" not in twin
    assert not (tmp_path / "raw" / "assets").exists()
    assert result.images is None


def test_flagged_capture_downloads_into_assets(tmp_path, png_bytes):
    session = FakeSession(jina_markdown=MARKDOWN, images={DIAGRAM: png_bytes})
    result = _capture(tmp_path, session, localize_images=True)

    twin = (tmp_path / "raw" / f"{STEM}.md").read_text()
    assert f"assets/{STEM}/img-2.png" in twin  # diagram rewritten to local path
    assert AVATAR in twin  # avatar left remote
    assert (tmp_path / "raw" / "assets" / STEM / "img-2.png").read_bytes() == png_bytes

    assert result.images["kept"] == [
        {"src": DIAGRAM, "path": f"assets/{STEM}/img-2.png"}
    ]
    assert [s["src"] for s in result.images["skipped"]] == [AVATAR]


def test_core_conversion_failure_writes_nothing(tmp_path):
    session = FakeSession(jina_markdown="")  # empty -> ConversionError
    with pytest.raises(ConversionError):
        _capture(tmp_path, session, localize_images=True)

    assert not (tmp_path / "raw" / f"{STEM}.md").exists()
    assert not (tmp_path / "raw" / "assets").exists()


def test_assets_stem_tracks_unique_path_suffix(tmp_path, png_bytes):
    # Pre-create the twin so _unique_path appends -2; assets must follow the stem.
    raw_dir = tmp_path / "raw"
    raw_dir.mkdir()
    (raw_dir / f"{STEM}.md").write_text("pre-existing twin")

    session = FakeSession(jina_markdown=MARKDOWN, images={DIAGRAM: png_bytes})
    result = _capture(tmp_path, session, localize_images=True)

    assert result.raw_path.name == f"{STEM}-2.md"
    twin = result.raw_path.read_text()
    assert f"assets/{STEM}-2/img-2.png" in twin
    assert (raw_dir / "assets" / f"{STEM}-2" / "img-2.png").exists()
