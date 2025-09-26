#!/usr/bin/env python3
"""HoI4 Localisation Adder (Python 3)."""

import argparse
import re
from collections import OrderedDict
from pathlib import Path
from typing import Iterable, List, Tuple


DECISION_HINTS = {
    "available",
    "visible",
    "fire_only_once",
    "cost",
    "days_remove",
    "remove_effect",
    "complete_effect",
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Parse an event/focus/ideas/decisions file and append missing "
            "localisation keys to the provided localisation file."
        )
    )
    parser.add_argument("input", type=Path, help="Script file to parse")
    parser.add_argument(
        "output",
        type=Path,
        help="Localisation file to append to (created if missing)",
    )
    parser.add_argument(
        "-t",
        "--todo",
        action="store_true",
        help="Prefix every generated entry with #TODO (rather than once)",
    )
    return parser.parse_args()


def read_lines_with_fallback(path: Path) -> List[str]:
    encodings = ("utf-8", "utf-8-sig", "cp1252")
    for encoding in encodings:
        try:
            return path.read_text(encoding=encoding).splitlines()
        except FileNotFoundError:
            raise SystemExit(f"File '{path}' was not found.")
        except UnicodeDecodeError:
            continue
    raise SystemExit(f"Could not decode '{path}' using UTF-8 or CP1252.")


def try_read_lines(path: Path) -> List[str]:
    if not path.exists():
        return []
    encodings = ("utf-8", "utf-8-sig", "cp1252")
    for encoding in encodings:
        try:
            return path.read_text(encoding=encoding).splitlines()
        except UnicodeDecodeError:
            continue
    raise SystemExit(f"Could not decode '{path}' using UTF-8 or CP1252.")


def parse_input_script(path: Path) -> Tuple[List[str], Tuple[bool, bool, bool, bool]]:
    lines = read_lines_with_fallback(path)
    tags: "OrderedDict[str, None]" = OrderedDict()

    open_blocks = 0
    is_event = is_focus = is_idea = is_decision_categories = False
    is_decision = False
    decision_candidates: list[str] = []

    for raw_line in lines:
        stripped = re.sub(r"#.*", "", raw_line)
        if not stripped.strip():
            open_blocks += raw_line.count("{")
            open_blocks -= raw_line.count("}")
            continue

        if not any((is_event, is_focus, is_idea, is_decision_categories)):
            if "focus_tree" in stripped:
                is_focus = True
                print(f"File {path} detected as national_focus.")
            elif "add_namespace" in stripped:
                is_event = True
                print(f"File {path} detected as event file.")
            elif "ideas" in stripped:
                is_idea = True
                print(f"File {path} detected as ideas file.")
            elif "{" in stripped:
                is_decision_categories = True
                decision_candidates = []
                print(f"File {path} detected as decisions or decision_categories.")

        if is_decision_categories:
            if open_blocks < 2 and "{" in stripped:
                tag = re.sub(r"\s|=(\s|){", "", stripped)
                if not is_decision and open_blocks == 1:
                    decision_candidates.append(tag)
                else:
                    tags[tag] = None
                    tags[f"{tag}_desc"] = None
            if (
                not is_decision
                and open_blocks == 2
                and any(hint in stripped for hint in DECISION_HINTS)
            ):
                is_decision = True
                for candidate in decision_candidates:
                    tags[candidate] = None
                    tags[f"{candidate}_desc"] = None
        elif is_focus:
            if open_blocks == 2 and re.match(r"^.*id ?=", stripped):
                tag = re.sub(r"^.*id ?=", "", stripped)
                tag = re.sub(r"\s", "", tag)
                tags[tag] = None
                tags[f"{tag}_desc"] = None
        elif is_idea:
            if open_blocks == 2 and "{" in stripped:
                tag = re.sub(r"\s|=(\s|){", "", stripped)
                tags[tag] = None
                tags[f"{tag}_desc"] = None
        elif is_event:
            if 0 < open_blocks < 3 and re.match(r"^.*(title|desc|name|text) ?=", stripped):
                tag = re.sub(r"^.*(title|desc|name|text) ?=", "", stripped)
                tag = re.sub(r"\s", "", tag)
                tags[tag] = None

        open_blocks += raw_line.count("{")
        open_blocks -= raw_line.count("}")

    print(f"File {path} read successfully!")
    return list(tags.keys()), (is_event, is_focus, is_idea, is_decision_categories)


def collect_existing_keys(lines: Iterable[str]) -> set[str]:
    keys = set()
    for line in lines:
        match = NAME_LINE_REGEX.match(line)
        if match:
            keys.add(match.group(1).strip())
    return keys


def append_localisation(path: Path, entries: List[str], add_todo_per_line: bool) -> None:
    output_lines = [""]
    if not add_todo_per_line:
        output_lines.append(" #TODO")
    for entry in entries:
        if add_todo_per_line:
            output_lines.append(" #TODO")
        output_lines.append(f" {entry}:0 \"\"")
    with path.open("a", encoding="utf-8-sig") as handle:
        handle.write("\n".join(output_lines) + "\n")


def main() -> None:
    args = parse_args()
    tags, metadata = parse_input_script(args.input)

    output_lines = try_read_lines(args.output)
    if not output_lines:
        print(
            f"Output file {args.output} is empty or missing; creating a new l_english stub."
        )
        args.output.write_text("l_english:\n", encoding="utf-8-sig")
        output_lines = ["l_english:"]

    existing = collect_existing_keys(output_lines)
    missing = [tag for tag in tags if tag not in existing]

    if not missing:
        print("No new localisation keys were required.")
        return

    append_localisation(args.output, missing, args.todo)
    print(
        f"Appended {len(missing)} lines to output file {args.output} successfully!"
    )


if __name__ == "__main__":
    main()
