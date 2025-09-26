#!/usr/bin/env python3
"""Multiply manpower values in HoI4 state history files."""

import argparse
import re
from pathlib import Path
from typing import Iterable

MANPOWER_REGEX = re.compile(r"manpower\s*=\s*(\d+)")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Given a state history file or directory of files, multiply each "
            "manpower value by the provided multiplier."
        )
    )
    parser.add_argument(
        "input",
        type=Path,
        help="State history file or directory containing state files",
    )
    parser.add_argument(
        "multiplier",
        type=float,
        help="Multiplier applied to each manpower value",
    )
    return parser.parse_args()


def iter_state_files(path: Path) -> Iterable[Path]:
    if path.is_dir():
        yield from sorted(child for child in path.glob("*.txt") if child.is_file())
    else:
        yield path


def process_file(path: Path, multiplier: float) -> bool:
    text = path.read_text(encoding="utf-8")
    changed = False

    def repl(match: re.Match[str]) -> str:
        nonlocal changed
        value = int(match.group(1))
        new_value = int(value * multiplier)
        if new_value != value:
            changed = True
        return f"manpower = {new_value}"

    updated = MANPOWER_REGEX.sub(repl, text)
    if changed:
        path.write_text(updated, encoding="utf-8")
    return changed


def main() -> None:
    args = parse_args()
    if not args.input.exists():
        raise SystemExit(f"Input '{args.input}' was not found.")

    processed = 0
    for state_file in iter_state_files(args.input):
        if process_file(state_file, args.multiplier):
            print(f"Updated {state_file}")
            processed += 1
    print(f"Finished, {processed} state files updated.")


if __name__ == "__main__":
    main()
