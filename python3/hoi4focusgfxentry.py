#!/usr/bin/env python3
"""HoI4 Focus GFX entry generator (Python 3 rewrite)."""

import argparse
from pathlib import Path


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Given a folder and a focus icon name, add missing sprite entries "
            "to the goals and goals_shine GFX files."
        )
    )
    parser.add_argument(
        "icon_name",
        help="Focus icon sprite name without the leading GFX_ prefix",
    )
    parser.add_argument(
        "-d",
        "--directory",
        default=Path.cwd(),
        type=Path,
        help=(
            "Directory containing the goals/goals_shine files "
            "(default: current directory)"
        ),
    )
    parser.add_argument(
        "--goals",
        default="goals.gfx",
        help="Name of the goals .gfx file (default: goals.gfx)",
    )
    parser.add_argument(
        "--goals-shine",
        dest="goals_shine",
        default="goals_shine.gfx",
        help="Name of the goals_shine .gfx file (default: goals_shine.gfx)",
    )
    return parser.parse_args()


def read_lines(path: Path) -> list[str]:
    try:
        return path.read_text(encoding="utf-8").splitlines()
    except FileNotFoundError as exc:
        raise SystemExit(f"File '{path}' was not found.") from exc


def write_lines(path: Path, lines: list[str]) -> None:
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def contains_sprite(lines: list[str], sprite_name: str) -> bool:
    target = f'"{sprite_name}"'
    return any(target in line for line in lines)


def find_insert_index(lines: list[str]) -> int:
    for index in range(len(lines) - 1, -1, -1):
        if lines[index].strip().startswith("}"):
            return index
    return len(lines)


def update_goals_file(path: Path, icon_name: str) -> bool:
    sprite_name = f"GFX_{icon_name}"
    lines = read_lines(path)
    if contains_sprite(lines, sprite_name):
        return False

    insert_at = find_insert_index(lines)
    block = [
        "\tSpriteType = {",
        f"\t\tname = \"{sprite_name}\"",
        f"\t\ttexturefile = \"gfx/interface/goals/{icon_name}.dds\"",
        "\t}",
    ]
    lines[insert_at:insert_at] = block
    write_lines(path, lines)
    return True


def update_goals_shine_file(path: Path, icon_name: str) -> bool:
    sprite_name = f"GFX_{icon_name}_shine"
    lines = read_lines(path)
    if contains_sprite(lines, sprite_name):
        return False

    insert_at = find_insert_index(lines)
    block = [
        "\tSpriteType = {",
        f"\t\tname = \"{sprite_name}\"",
        f"\t\ttexturefile = \"gfx/interface/goals/{icon_name}.dds\"",
        "\t\tanimation = {",
        "\t\t\tanimationtexturescale = { x = 1.0 y = 1.0 }",
        "\t\t\tanimationrotationoffset = { x = 0.0 y = 0.0 }",
        "\t\t\tanimationtype = \"scrolling\"",
        "\t\t\tanimationblendmode = \"add\"",
        "\t\t\tanimationdelay = 0",
        "\t\t\tanimationtime = 0.75",
        "\t\t\tanimationlooping = no",
        "\t\t\tanimationrotation = 90.0",
        "\t\t\tanimationtexturefile = \"gfx/interface/goals/shine_overlay.dds\"",
        f"\t\t\tanimationmaskfile = \"gfx/interface/goals/{icon_name}.dds\"",
        "\t\t}",
        "\t\tanimation = {",
        "\t\t\tanimationtexturescale = { x = 1.0 y = 1.0 }",
        "\t\t\tanimationrotationoffset = { x = 0.0 y = 0.0 }",
        "\t\t\tanimationtype = \"scrolling\"",
        "\t\t\tanimationblendmode = \"add\"",
        "\t\t\tanimationdelay = 0",
        "\t\t\tanimationtime = 0.75",
        "\t\t\tanimationlooping = no",
        "\t\t\tanimationrotation = -90.0",
        "\t\t\tanimationtexturefile = \"gfx/interface/goals/shine_overlay.dds\"",
        f"\t\t\tanimationmaskfile = \"gfx/interface/goals/{icon_name}.dds\"",
        "\t\t\teffectFile = \"gfx/FX/buttonstate.lua\"",
        "\t\t}",
        "\t\tlegacy_lazy_load = no",
        "\t}",
    ]
    lines[insert_at:insert_at] = block
    write_lines(path, lines)
    return True


def main() -> None:
    args = parse_args()
    directory: Path = args.directory
    if not directory.is_dir():
        raise SystemExit(f"Directory '{directory}' was not found or is not accessible.")

    goals_path = directory / args.goals
    goals_shine_path = directory / args.goals_shine

    added_sprite = update_goals_file(goals_path, args.icon_name)
    added_shine = update_goals_shine_file(goals_shine_path, args.icon_name)

    if added_sprite:
        print(f"Added GFX_{args.icon_name} to {goals_path}.")
    else:
        print(f"Sprite GFX_{args.icon_name} already present in {goals_path}, skipping.")

    if added_shine:
        print(f"Added GFX_{args.icon_name}_shine to {goals_shine_path}.")
    else:
        print(
            f"Sprite GFX_{args.icon_name}_shine already present in "
            f"{goals_shine_path}, skipping."
        )


if __name__ == "__main__":
    main()
