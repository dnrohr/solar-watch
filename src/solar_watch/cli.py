from __future__ import annotations

import argparse
import json
from pathlib import Path

from .generate import generate_all, refresh_ephemeris


def main() -> None:
    parser = argparse.ArgumentParser(description="Solar Watch P0/P1 artifact generator")
    subparsers = parser.add_subparsers(dest="command", required=True)
    generate = subparsers.add_parser("generate", help="regenerate P0/P1 artifacts offline")
    generate.add_argument("--root", type=Path, default=Path.cwd())
    validate = subparsers.add_parser(
        "validate-ephemeris", help="refresh the independent JPL DE421 table (network on first run)"
    )
    validate.add_argument("--root", type=Path, default=Path.cwd())
    validate.add_argument("--cache", type=Path, default=Path(".cache/skyfield"))
    args = parser.parse_args()
    if args.command == "validate-ephemeris":
        path = refresh_ephemeris(args.root, args.cache)
        print(path)
    else:
        print(json.dumps(generate_all(args.root), indent=2))


if __name__ == "__main__":
    main()
