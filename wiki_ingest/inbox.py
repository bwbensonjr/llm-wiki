"""Parsing `inbox.md` and naming drop paths for parked entries.

Each queue entry is one checklist line: `- [<state>] <source> <tail>`, where the
tail holds the optional curator note and any dated annotations. States:

    " "  unprocessed        "x"  ingested
    "!"  parked, needs the curator (normally with a drop path)
    "-"  dead or rejected, never retried

A parked entry names where the curator should put a hand-fetched copy with a
`→ drop: inbox-files/<slug>.<ext>` token. A file with the same stem and any
extension satisfies the drop, so an assembled `.md` can stand in for a `.pdf`.

Lines inside fenced code blocks (the format examples in the file's header) are
not entries.
"""

import os
import re
from dataclasses import dataclass
from pathlib import Path
from typing import List, Optional
from urllib.parse import urlparse

from .slug import fallback_name, slugify

DROP_DIR = "inbox-files"
STATES = {" ": "unprocessed", "x": "ingested", "!": "parked", "-": "dead"}

_ENTRY = re.compile(r"^- \[(?P<state>[ xX!\-])\] (?P<source>\S+)(?P<tail>.*)$")
_DROP = re.compile(r"(?:→|->)\s*drop:\s*(?P<path>\S+)")


@dataclass
class Entry:
    line: int  # 1-based line number in inbox.md
    state: str  # one of " ", "x", "!", "-"
    source: str
    tail: str
    drop: Optional[str]

    @property
    def state_name(self):
        return STATES[self.state]


def parse(text):
    """Return the queue entries in ``text``, skipping fenced code blocks."""
    entries: List[Entry] = []
    in_fence = False
    for number, raw in enumerate(text.splitlines(), start=1):
        if raw.lstrip().startswith("```"):
            in_fence = not in_fence
            continue
        if in_fence:
            continue
        match = _ENTRY.match(raw.rstrip())
        if not match:
            continue
        tail = match.group("tail")
        drop = _DROP.search(tail)
        state = match.group("state").lower()
        entries.append(
            Entry(
                line=number,
                state=state,
                source=match.group("source"),
                tail=tail.strip(),
                drop=drop.group("path") if drop else None,
            )
        )
    return entries


def read(path="inbox.md"):
    return parse(Path(path).read_text(encoding="utf-8"))


def default_extension(source):
    """`pdf` for a paper-like source, `md` for a web page that needs assembly."""
    from .acquire import extract_doi

    path = urlparse(source).path.lower()
    if path.endswith((".pdf", ".ps", ".ps.gz", ".eps")) or extract_doi(source):
        return "pdf"
    return "md"


def name_drop(source, title=None, ext=None, taken=()):
    """Return the drop path for a parked source.

    The stem is the slug of the best known title (falling back to the URL's last
    path segment); a stem already used by another entry's drop gets `-2`, `-3`.
    """
    stem = slugify(title or "") or slugify(fallback_name(source)) or "untitled"
    ext = (ext or default_extension(source)).lstrip(".")
    taken_stems = {Path(t).stem for t in taken}
    candidate, n = stem, 2
    while candidate in taken_stems:
        candidate = f"{stem}-{n}"
        n += 1
    return f"{DROP_DIR}/{candidate}.{ext}"


def find_drop(drop, root="."):
    """Return the dropped file matching ``drop`` by stem (any extension), or None."""
    target = Path(root) / drop
    if target.exists():
        return target
    if not target.parent.is_dir():
        return None
    matches = sorted(
        p for p in target.parent.iterdir() if p.is_file() and p.stem == target.stem
    )
    return matches[0] if matches else None


def pending(entries, root=".", proxy_prefix=None):
    """Split parked entries into those awaiting a file and those ready to resolve.

    Returns {"pending": [...], "ready": [...]}. Read-only and offline.
    """
    waiting, ready = [], []
    for entry in entries:
        if entry.state != "!":
            continue
        item = {"line": entry.line, "source": entry.source, "drop": entry.drop}
        if proxy_prefix and entry.source.startswith(("http://", "https://")):
            item["proxied"] = proxy_prefix + entry.source
        if entry.drop is None:
            item["status"] = "no drop path"
            waiting.append(item)
            continue
        found = find_drop(entry.drop, root)
        if found is None:
            item["status"] = "awaiting file"
            waiting.append(item)
        else:
            item["status"] = "ready"
            item["file"] = os.path.relpath(found, root)
            ready.append(item)
    return {"pending": waiting, "ready": ready}


def format_text(report):
    lines = []
    if report["pending"]:
        lines.append("Needs manual fetch:")
        for item in report["pending"]:
            where = item["drop"] or "(no drop path; add `→ drop: inbox-files/<name>`)"
            lines.append(f"  line {item['line']}: {item['source']}")
            if item.get("proxied"):
                lines.append(f"    via proxy: {item['proxied']}")
            lines.append(f"    drop: {where}")
    else:
        lines.append("Needs manual fetch: none")
    if report["ready"]:
        lines.append("Ready to resolve on the next ingest-inbox run:")
        for item in report["ready"]:
            lines.append(f"  line {item['line']}: {item['source']} <- {item['file']}")
    return "\n".join(lines)
