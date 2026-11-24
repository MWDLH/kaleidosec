#!/usr/bin/env python3
"""Verify the plugin entry stays in sync with the single source of truth.

The protocol has one source: SKILL.md at the repository root. The plugin's skill
entry (skills/kaleidosec/SKILL.md) is a thin pointer. Its description
must match the root, otherwise semantic triggering uses stale text.

Exit code 0 = in sync, 1 = drift detected.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SOURCE = ROOT / "SKILL.md"
ENTRY = ROOT / "skills" / "kaleidosec" / "SKILL.md"


def description_of(path: Path) -> str | None:
    try:
        text = path.read_text(encoding="utf-8")
    except OSError:
        return None
    match = re.match(r"^---\r?\n(.*?)\r?\n---\r?\n", text, re.S)
    if not match:
        return None
    for line in match.group(1).splitlines():
        if line.startswith("description:"):
            value = line[len("description:"):].strip()
            if value.startswith((">", "|")):
                raise ValueError(
                    f"{path}: folded/multiline description is not supported by this checker; "
                    "keep it on one line"
                )
            if len(value) >= 2 and value[0] == value[-1] == '"':
                value = value[1:-1]
            return value
    return None


def main() -> int:
    problems: list[str] = []

    if not SOURCE.is_file():
        problems.append(f"missing source: {SOURCE}")
    if not ENTRY.is_file():
        problems.append(f"missing plugin entry: {ENTRY}")

    source_desc = None
    entry_desc = None
    try:
        if SOURCE.is_file():
            source_desc = description_of(SOURCE)
    except ValueError as exc:
        problems.append(str(exc))
    try:
        if ENTRY.is_file():
            entry_desc = description_of(ENTRY)
    except ValueError as exc:
        problems.append(str(exc))

    if source_desc and entry_desc and source_desc != entry_desc:
        problems.append("description drift: root and plugin entry differ")
    if not source_desc:
        problems.append("root SKILL.md has no parseable description")
    if not entry_desc:
        problems.append("plugin entry has no parseable description")

    if ENTRY.is_file():
        entry_text = ENTRY.read_text(encoding="utf-8")
        if "../../SKILL.md" not in entry_text:
            problems.append("plugin entry does not point to ../../SKILL.md")
        if not (ENTRY.parent / "../../SKILL.md").resolve().is_file():
            problems.append("plugin entry pointer does not resolve to the root protocol")

    if problems:
        for item in problems:
            print(f"ERROR: {item}")
        return 1
    print(f"in sync: description {len(source_desc or '')} chars; entry points to root protocol")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
