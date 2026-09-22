from __future__ import annotations

import argparse
import json
from pathlib import Path

from .generate import generate_all, refresh_ephemeris
from .p2_cad import generate_p2_cad
from .p2_analysis import generate_p2_analysis


def main() -> None:
    parser = argparse.ArgumentParser(description="Solar Watch reproducible artifact generator")
    subparsers = parser.add_subparsers(dest="command", required=True)
    generate = subparsers.add_parser("generate", help="regenerate P0/P1 artifacts offline")
    generate.add_argument("--root", type=Path, default=Path.cwd())
    validate = subparsers.add_parser(
        "validate-ephemeris", help="refresh the independent JPL DE421 table (network on first run)"
    )
    validate.add_argument("--root", type=Path, default=Path.cwd())
    validate.add_argument("--cache", type=Path, default=Path(".cache/skyfield"))
    p2 = subparsers.add_parser("generate-p2", help="regenerate P2 CNC manufacturing files")
    p2.add_argument("--root", type=Path, default=Path.cwd())
    analysis = subparsers.add_parser("analyze-p2", help="regenerate P2 mechanical analysis")
    analysis.add_argument("--root", type=Path, default=Path.cwd())
    args = parser.parse_args()
    if args.command == "validate-ephemeris":
        path = refresh_ephemeris(args.root, args.cache)
        print(path)
    elif args.command == "generate-p2":
        print(json.dumps(generate_p2_cad(args.root), indent=2))
    elif args.command == "analyze-p2":
        print(json.dumps(generate_p2_analysis(args.root), indent=2))
    else:
        print(json.dumps(generate_all(args.root), indent=2))


if __name__ == "__main__":
    main()
