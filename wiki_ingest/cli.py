"""`wiki-capture` — the CLI the `file` and `ingest-inbox` skills invoke for Phase 1.

Capture: acquires a source (trying the fallback chain when the routed fetch fails
or yields a stub), converts it, writes the immutable raw twin, and prints a JSON
object describing the result:

    {"raw_path": "raw/2026-06-22-foo.md",
     "source": "https://example.com/foo",
     "converter": "jina",
     "detected_type": "text/html; charset=utf-8",
     "title": "Foo",
     "acquired_via": "primary"}

`source` is what the twin recorded, which for a YouTube video is the canonical
watch URL; use it, not the filed string, for the summary's `source:`. When content
came from somewhere other than the source itself, `fetched_from` names the URL
actually fetched.

    wiki-capture <url-or-path>                   capture a source
    wiki-capture <file> --source-url <url>       capture a hand-fetched copy under its URL
    wiki-capture <url> --canonical               print the `source:` form; no network
    wiki-capture --pending [--text]              list parked inbox entries; no network
    wiki-capture --drop-path <url> [--title T]   print the drop path for a parked source

On any capture failure it writes nothing, prints a JSON error to stderr, and exits
1. The error carries `attempts` (each step, URL, and outcome) and `title` (the best
title learned) when the fallback chain ran.

Optional configuration, read from the environment (put it in `mise.local.toml`):
`UNPAYWALL_EMAIL` enables the Unpaywall lookup; `LIBRARY_PROXY_PREFIX` adds a
proxied link to each `--pending` entry.
"""

import argparse
import json
import os
import sys

from .convert import AcquisitionError, ConversionError, capture
from .detect import DetectionError


def _emit(payload, stream=None):
    # Resolve sys.stdout at call time, so test capture of stdout sees the output.
    stream = stream or sys.stdout
    json.dump(payload, stream)
    stream.write("\n")


def main(argv=None):
    parser = argparse.ArgumentParser(
        prog="wiki-capture",
        description="Phase 1 capture: acquire and convert a source, write its raw twin.",
    )
    parser.add_argument("source", nargs="?", help="URL or local path to ingest")
    parser.add_argument(
        "--canonical",
        action="store_true",
        help=(
            "print the form this source would be recorded under in `source:` "
            "and exit, with no network access and no writes"
        ),
    )
    parser.add_argument(
        "--raw-dir",
        default="raw",
        help="directory for raw twins (default: raw)",
    )
    parser.add_argument(
        "--no-images",
        action="store_true",
        help=(
            "suppress image localization for this source "
            "(web/Jina content images are localized into raw/assets/ by default)"
        ),
    )
    parser.add_argument(
        "--source-url",
        metavar="URL",
        help=(
            "capture a local file on behalf of its original URL: the twin records "
            "the URL as `source:` and the file as `local-copy:`"
        ),
    )
    parser.add_argument(
        "--pending",
        action="store_true",
        help=(
            "list parked (`- [!]`) inbox entries awaiting a hand-fetched file, and "
            "those whose file has arrived; reads inbox.md only, no network"
        ),
    )
    parser.add_argument(
        "--text", action="store_true", help="with --pending, print a plain list"
    )
    parser.add_argument(
        "--inbox", default="inbox.md", help="inbox file for --pending (default: inbox.md)"
    )
    parser.add_argument(
        "--drop-path",
        metavar="URL",
        help="print the inbox-files/ drop path a parked source should name",
    )
    parser.add_argument("--title", help="with --drop-path, the best known title")
    parser.add_argument("--ext", help="with --drop-path, the expected extension")
    args = parser.parse_args(argv)

    if args.pending:
        from . import inbox

        try:
            entries = inbox.read(args.inbox)
        except OSError as exc:
            _emit({"error": f"could not read inbox: {exc}"}, sys.stderr)
            return 1
        root = os.path.dirname(os.path.abspath(args.inbox))
        report = inbox.pending(
            entries, root=root, proxy_prefix=os.environ.get("LIBRARY_PROXY_PREFIX")
        )
        if args.text:
            sys.stdout.write(inbox.format_text(report) + "\n")
        else:
            _emit(report)
        return 0

    if args.drop_path:
        from . import inbox

        taken = []
        if os.path.exists(args.inbox):
            taken = [e.drop for e in inbox.read(args.inbox) if e.drop]
        _emit(
            {
                "drop": inbox.name_drop(
                    args.drop_path, title=args.title, ext=args.ext, taken=taken
                )
            }
        )
        return 0

    if not args.source:
        parser.error("a source is required unless --pending or --drop-path is given")

    if args.canonical:
        from .youtube import canonical_source

        _emit({"source": canonical_source(args.source)})
        return 0

    try:
        result = capture(
            args.source,
            raw_dir=args.raw_dir,
            localize_images=not args.no_images,
            source_url=args.source_url,
        )
    except (DetectionError, ConversionError) as exc:
        error = {"error": str(exc), "source": args.source_url or args.source}
        if isinstance(exc, AcquisitionError):
            error["attempts"] = exc.attempts
            error["title"] = exc.title
        _emit(error, sys.stderr)
        return 1

    payload: dict = {
        "raw_path": str(result.raw_path),
        "source": result.source,
        "converter": result.converter,
        "detected_type": result.detected_type,
        "title": result.title,
        "acquired_via": result.acquired_via,
    }
    if result.fetched_from:
        payload["fetched_from"] = result.fetched_from
    if result.local_copy:
        payload["local_copy"] = result.local_copy
    if result.images is not None:
        payload["images"] = result.images
    _emit(payload)
    return 0


if __name__ == "__main__":
    sys.exit(main())
