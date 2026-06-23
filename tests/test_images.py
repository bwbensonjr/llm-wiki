"""Unit tests for the image-localization helper (`wiki_ingest.images`)."""

from wiki_ingest import images
from wiki_ingest.images import find_image_refs, is_decorative_url, localize

from .conftest import FakeSession

AVATAR = "https://avatars.githubusercontent.com/u/1?s=64&v=4"
THUMB = "https://example.com/pic.png?s=80"
DIAGRAM = "https://example.com/diagram.png"


def test_find_image_refs_includes_wrapped_image():
    md = f"[![Image 1: diagram]({DIAGRAM})](https://example.com/full)"
    refs = find_image_refs(md)
    assert [src for _, src, _ in refs] == [DIAGRAM]


def test_is_decorative_url_flags_avatars_and_thumbnails():
    assert is_decorative_url(AVATAR) is True
    assert is_decorative_url(THUMB) is True
    assert is_decorative_url(DIAGRAM) is False


def test_localize_keeps_content_skips_avatar(tmp_path, png_bytes):
    md = (
        f"![avatar]({AVATAR})\n\n![diagram]({DIAGRAM})\n"
    )
    session = FakeSession(images={DIAGRAM: png_bytes})
    new_md, report = localize(
        md, tmp_path / "assets", "assets", session=session
    )

    # Avatar link is left remote; diagram link is rewritten to a local path.
    assert AVATAR in new_md
    assert "assets/img-2.png" in new_md
    assert (tmp_path / "assets" / "img-2.png").read_bytes() == png_bytes

    assert report.kept == [{"src": DIAGRAM, "path": "assets/img-2.png"}]
    assert [s["src"] for s in report.skipped] == [AVATAR]
    assert report.skipped[0]["reason"] == "decorative"


def test_localize_skips_undersized_image(tmp_path):
    session = FakeSession(images={DIAGRAM: b"tiny"})
    new_md, report = localize(
        f"![d]({DIAGRAM})", tmp_path / "assets", "assets", session=session
    )
    assert new_md == f"![d]({DIAGRAM})"  # link unchanged
    assert report.kept == []
    assert report.skipped[0]["reason"] == "below-size-threshold"
    assert not (tmp_path / "assets").exists()  # no dir without a keep


def test_localize_tolerates_download_failure(tmp_path):
    session = FakeSession(fail_urls={DIAGRAM})
    new_md, report = localize(
        f"![d]({DIAGRAM})", tmp_path / "assets", "assets", session=session
    )
    assert new_md == f"![d]({DIAGRAM})"  # link left remote
    assert report.kept == []
    assert report.skipped[0]["reason"].startswith("download-failed")


def test_localize_creates_dir_only_when_keeping(tmp_path, png_bytes):
    session = FakeSession(images={DIAGRAM: png_bytes})
    localize(f"![d]({DIAGRAM})", tmp_path / "assets", "assets", session=session)
    assert (tmp_path / "assets").is_dir()


def test_min_image_bytes_is_the_threshold():
    # Guard against silent drift of the documented threshold.
    assert images.MIN_IMAGE_BYTES == 5000
