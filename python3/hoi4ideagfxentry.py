#!/usr/bin/env python3
"""HoI4 Idea GFX entry generator (Python 3)."""

import argparse
import os
import re
from pathlib import Path


IDEA_BLOCK_REGEX = re.compile(r"^.*id\s*=\s*")
NAME_LINE_REGEX = re.compile(r"^([^#:]+):")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Given an ideas file, add missing sprite entries to the specified "
            ".gfx file (creating a skeleton if it does not exist)."
        )
    )
    parser.add_argument("idea_file", type=Path, help="Path to the ideas file to scan")
    parser.add_argument(
        "gfx_file",
        type=Path,
        help="GFX file to write sprite entries into (created if missing)",
    )
    parser.add_argument(
        "--icon-directory",
        default="",
        help="Subdirectory in gfx/interface/ideas that stores the icons",
    )
    parser.add_argument(
        "--icon-format",
        default="dds",
        help="Image extension (without dot) for idea icons (default: dds)",
    )
    parser.add_argument(
        "-np",
        "--no-prefix",
        action="store_true",
        help="Do not prepend 'idea_' to icon filenames",
    )
    return parser.parse_args()


def read_idea_pictures(path: Path) -> list[str]:
    print(f"Reading file {path}...")
    text = path.read_text(encoding="utf-8")
    lines = text.splitlines()

    tags: list[str] = []
    open_blocks = 0
    for raw_line in lines:
        line = re.sub(r"#.*", "", raw_line)
        line = line.strip()
        if not line:
            continue

        if open_blocks == 2 and "{" in line:
            idea_name = re.sub(r"\s|=(\s|){", "", line)
            if idea_name and idea_name not in tags:
                tags.append(idea_name)
        elif open_blocks > 2 and ("picture =" in line or "picture=" in line):
            picture = re.sub(r"(\s|).*=(\s|)", "", line)
            if picture and picture not in tags:
                tags.append(picture)

        open_blocks += raw_line.count("{")
        open_blocks -= raw_line.count("}")

    print(f"File {path} read successfully, {len(tags)} unique idea pictures found.")
    return tags


def load_gfx_lines(path: Path) -> list[str]:
    if path.exists():
        return path.read_text(encoding="utf-8").splitlines()
    return ["spriteTypes = {", "}"]


def has_sprite(lines: list[str], sprite_name: str) -> bool:
    pattern = re.compile(rf"name\s*=\s*\"{re.escape(sprite_name)}\"")
    return any(pattern.search(line) for line in lines)


def insert_sprite(lines: list[str], sprite_name: str, texture_path: str) -> None:
    insert_at = len(lines) - 1
    while insert_at >= 0 and not lines[insert_at].strip().startswith("}"):
        insert_at -= 1
    if insert_at < 0:
        insert_at = len(lines)
    block = [
        "\tSpriteType = {",
        f"\t\tname = \"{sprite_name}\"",
        f"\t\ttexturefile = \"{texture_path}\"",
        "\t}",
    ]
    lines[insert_at:insert_at] = block


def write_gfx_file(path: Path, lines: list[str]) -> None:
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    args = parse_args()
    if not args.idea_file.is_file():
        raise SystemExit(f"Idea file '{args.idea_file}' was not found.")

    sprite_prefix = "" if args.no_prefix else "idea_"
    icon_directory = f"/{args.icon_directory.strip('/')}" if args.icon_directory else ""

    pictures = read_idea_pictures(args.idea_file)
    lines = load_gfx_lines(args.gfx_file)

    added = 0
    for picture in pictures:
        sprite_name = f"GFX_idea_{picture}"
        if has_sprite(lines, sprite_name):
            continue
        icon_name = f"{sprite_prefix}{picture}.{args.icon_format}"
        texture_path = f"gfx/interface/ideas{icon_directory}/{icon_name}"
        insert_sprite(lines, sprite_name, texture_path)
        added += 1

    write_gfx_file(args.gfx_file, lines)
    print(
        f"GFX file {args.gfx_file} updated successfully; added {added} new entries."
    )


if __name__ == "__main__":
    main()
