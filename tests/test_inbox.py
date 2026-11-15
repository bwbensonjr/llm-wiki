"""Tests for inbox.md parsing, drop paths, --pending, and the capture CLI error JSON."""

import json
import socket
from pathlib import Path

import pytest

from wiki_ingest import cli, convert, inbox

REPO_INBOX = Path(__file__).resolve().parent.parent / "inbox.md"

SAMPLE = """# Inbox

```markdown
- [ ] https://example.com/paper.pdf — worth it for the CPS angle
- [!] https://example.com/broken — 2026-08-05: docling failed
```

## Queue

- [ ] https://example.com/new — a note
- [x] https://example.com/done
- [!] https://legacy.cs.indiana.edu/~dyb/pubs/implicit-phasing.pdf - note — 2026-10-31: unreachable; tried wayback (none) → drop: inbox-files/implicit-phasing-for-r6rs-libraries.pdf
- [!] https://dl.acm.org/doi/epdf/10.1145/2544174.2500618 — 2026-11-15: bot check → drop: inbox-files/a-nanopass-framework-for-commercial-compiler-development.pdf
- [!] https://opendylan.org/books/drm/Sealing - 2026-10-31: chapter landing page only
- [-] http://foo.bar.baz/bad-link — 2026-11-15: host does not exist
"""


@pytest.fixture
def no_network(monkeypatch):
    def refuse(*args, **kwargs):
        raise AssertionError("network access attempted")

    monkeypatch.setattr(socket, "create_connection", refuse)
    monkeypatch.setattr(socket.socket, "connect", refuse)


def test_parse_skips_fenced_examples_and_reads_states():
    entries = inbox.parse(SAMPLE)
    assert [e.state for e in entries] == [" ", "x", "!", "!", "!", "-"]
    assert entries[0].source == "https://example.com/new"
    assert entries[0].line == 10
    assert entries[2].drop == "inbox-files/implicit-phasing-for-r6rs-libraries.pdf"
    assert entries[4].drop is None
    assert entries[5].state_name == "dead"


def test_repo_inbox_parses_every_entry():
    text = REPO_INBOX.read_text()
    entries = inbox.parse(text)
    in_fence, expected = False, 0
    for line in text.splitlines():
        if line.lstrip().startswith("```"):
            in_fence = not in_fence
        elif not in_fence and line.startswith("- ["):
            expected += 1
    assert len(entries) == expected > 0


def test_drop_named_from_title():
    drop = inbox.name_drop(
        "https://dl.acm.org/doi/epdf/10.1145/2544174.2500618",
        title="A Nanopass Framework for Commercial Compiler Development",
    )
    assert drop == "inbox-files/a-nanopass-framework-for-commercial-compiler-development.pdf"


def test_drop_falls_back_to_url_and_md_for_web_pages():
    assert inbox.name_drop("https://opendylan.org/books/drm/Sealing") == "inbox-files/sealing.md"


def test_drop_collision_gets_suffix():
    taken = ["inbox-files/sealing.md"]
    assert inbox.name_drop("https://x.org/a/Sealing", taken=taken) == "inbox-files/sealing-2.md"


def test_find_drop_matches_stem_with_any_extension(tmp_path):
    (tmp_path / "inbox-files").mkdir()
    (tmp_path / "inbox-files" / "sealing.md").write_text("# Sealing\n")
    found = inbox.find_drop("inbox-files/sealing.pdf", tmp_path)
    assert found == tmp_path / "inbox-files" / "sealing.md"
    assert inbox.find_drop("inbox-files/other.pdf", tmp_path) is None


def _write_inbox(tmp_path):
    path = tmp_path / "inbox.md"
    path.write_text(SAMPLE)
    (tmp_path / "inbox-files").mkdir()
    (tmp_path / "inbox-files" / "implicit-phasing-for-r6rs-libraries.pdf").write_bytes(b"%PDF")
    return path


def test_pending_json_offline(tmp_path, capsys, monkeypatch, no_network):
    path = _write_inbox(tmp_path)
    monkeypatch.delenv("LIBRARY_PROXY_PREFIX", raising=False)
    assert cli.main(["--pending", "--inbox", str(path)]) == 0
    report = json.loads(capsys.readouterr().out)
    assert [i["source"] for i in report["pending"]] == [
        "https://dl.acm.org/doi/epdf/10.1145/2544174.2500618",
        "https://opendylan.org/books/drm/Sealing",
    ]
    assert report["pending"][1]["status"] == "no drop path"
    assert [i["file"] for i in report["ready"]] == [
        "inbox-files/implicit-phasing-for-r6rs-libraries.pdf"
    ]
    # Dead and unprocessed entries never appear.
    sources = [i["source"] for i in report["pending"] + report["ready"]]
    assert "http://foo.bar.baz/bad-link" not in sources
    assert "proxied" not in report["pending"][0]


def test_pending_text_with_proxy(tmp_path, capsys, monkeypatch, no_network):
    path = _write_inbox(tmp_path)
    monkeypatch.setenv("LIBRARY_PROXY_PREFIX", "https://proxy.example.edu/login?url=")
    assert cli.main(["--pending", "--text", "--inbox", str(path)]) == 0
    out = capsys.readouterr().out
    assert "Needs manual fetch:" in out
    assert (
        "via proxy: https://proxy.example.edu/login?url="
        "https://dl.acm.org/doi/epdf/10.1145/2544174.2500618"
    ) in out
    assert "Ready to resolve" in out


def test_cli_drop_path(tmp_path, capsys):
    path = _write_inbox(tmp_path)
    code = cli.main(
        ["--drop-path", "https://example.org/x.pdf", "--title", "Some Paper", "--inbox", str(path)]
    )
    assert code == 0
    assert json.loads(capsys.readouterr().out) == {"drop": "inbox-files/some-paper.pdf"}


def test_cli_error_json_carries_attempts(tmp_path, capsys, monkeypatch):
    def failing(*args, **kwargs):
        raise convert.AcquisitionError(
            "Jina Reader request failed; also tried: ...",
            attempts=[{"step": "primary", "url": "u", "outcome": "stub: bot check"}],
            title="A Title",
        )

    monkeypatch.setattr(cli, "capture", failing)
    assert cli.main(["https://dl.acm.org/doi/epdf/10.1/x"]) == 1
    err = json.loads(capsys.readouterr().err)
    assert err["attempts"][0]["step"] == "primary"
    assert err["title"] == "A Title"


def test_cli_source_url_success_json(tmp_path, capsys, monkeypatch):
    local = tmp_path / "copy.pdf"
    local.write_bytes(b"%PDF-1.4")
    monkeypatch.setattr(convert, "_convert_docling", lambda s: "# Real Title\n\nBody.\n")
    code = cli.main(
        [str(local), "--source-url", "https://example.org/real.pdf", "--raw-dir", str(tmp_path / "raw")]
    )
    assert code == 0
    out = json.loads(capsys.readouterr().out)
    assert out["source"] == "https://example.org/real.pdf"
    assert out["acquired_via"] == "manual"
    assert out["local_copy"] == str(local)
