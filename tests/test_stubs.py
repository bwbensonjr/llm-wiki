"""Tests for mechanical stub detection (wiki_ingest.stubs)."""

from pathlib import Path

import pytest

from wiki_ingest import detect, stubs

FIXTURES = Path(__file__).parent / "fixtures"


def _fixture(name):
    return (FIXTURES / name).read_text()


def test_cloudflare_bot_check_is_a_stub():
    md = _fixture("stub-2026-08-05-just-a-moment.md")
    assert stubs.classify(md, detect.JINA) == "bot check or captcha page"


def test_jina_reported_error_page_is_a_stub():
    md = _fixture("stub-2026-10-31-racket-page-not-found.md")
    assert "HTTP 403" in stubs.classify(md, detect.JINA)


def test_acm_reader_shell_is_a_stub():
    md = _fixture(
        "stub-2026-08-05-a-nanopass-framework-for-commercial-compiler-development.md"
    )
    assert "loading shell" in stubs.classify(md, detect.JINA)


def test_error_title_without_jina_header_is_a_stub():
    md = "# 404 Not Found\n\nThe requested URL was not found on this server.\n"
    assert "error page" in stubs.classify(md, detect.MARKITDOWN)


def test_thin_pdf_is_a_stub():
    md = "# A Paper Title\n\nReferences\n\n1. Someone. Some paper. 1990.\n"
    assert "implausibly thin" in stubs.classify(md, detect.DOCLING)


def test_short_genuine_web_page_is_not_a_stub():
    md = "Title: A Short Note\n\nMarkdown Content:\n# A Short Note\n\nBody text.\n"
    assert stubs.classify(md, detect.JINA) is None


@pytest.mark.parametrize("route", [detect.DOCLING, detect.POSTSCRIPT])
def test_legible_ligature_artifacts_are_not_a_stub(route):
    # dvips output renders `fl` as `/`; that is legible prose, not a stub.
    sentence = (
        "We formulate the /ow analysis as a deductive system with multiple "
        "passes over the program text, and the analysis is sound. "
    )
    md = "# Control /ow Analysis\n\n" + sentence * 20
    assert stubs.classify(md, route) is None
