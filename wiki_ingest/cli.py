"""`wiki-capture` — the CLI the `file` skill invokes for Phase 1 (capture).

Detects the content type of a source, routes it to the right converter, writes
the immutable raw twin, and prints a JSON object describing the result:

    {"raw_path": "raw/2026-06-22-foo.md",
     "source": "https://example.com/foo",
     "converter": "jina",
     "detected_type": "text/html; charset=utf-8",
     "title": "Foo"}

`source` is what the twin recorded, which for a YouTube video is the canonical
watch URL; use it, not the filed string, for the summary's `source:`.
`--canonical` prints just that form without capturing.

On any failure it writes nothing, prints a JSON error to stderr, and exits 1.
"""

import argparse
import json
import sys

from .convert import ConversionError, capture
from .detect import DetectionError


def main(argv=None):
    parser = argparse.ArgumentParser(
        prog="wiki-capture",
        description="Phase 1 capture: convert a source and write its raw twin.",
    )
    parser.add_argument("source", help="URL or local path to ingest")
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
    args = parser.parse_args(argv)

    if args.canonical:
        from .youtube import canonical_source

        json.dump({"source": canonical_source(args.source)}, sys.stdout)
        sys.stdout.write("\n")
        return 0

    try:
        result = capture(
            args.source,
            raw_dir=args.raw_dir,
            localize_images=not args.no_images,
        )
    except (DetectionError, ConversionError) as exc:
        json.dump({"error": str(exc), "source": args.source}, sys.stderr)
        sys.stderr.write("\n")
        return 1

    payload: dict = {
        "raw_path": str(result.raw_path),
        "source": result.source,
        "converter": result.converter,
        "detected_type": result.detected_type,
        "title": result.title,
    }
    if result.images is not None:
        payload["images"] = result.images
    json.dump(payload, sys.stdout)
    sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
