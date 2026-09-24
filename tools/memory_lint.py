"""Memory hygiene gate (playbook/04-memory.md).

Checks a memory directory: every fact file has frontmatter with `name`,
`description` and a known `type`; names are unique; every fact appears in
the index; the index points at no missing file. Unknown `[[links]]` are
reported as warnings — a link to a fact not yet written is allowed.

    python tools/memory_lint.py examples/memory
"""

import re
import sys
from pathlib import Path

TYPES = {"user", "feedback", "project", "reference"}
INDEX = "MEMORY.md"
FRONTMATTER = re.compile(r"\A---\n(.*?)\n---\n", re.DOTALL)
LINK = re.compile(r"\[\[([a-z0-9-]+)\]\]")
INDEX_ENTRY = re.compile(r"\]\(([^)]+\.md)\)")


def _fields(text: str) -> dict[str, str]:
    match = FRONTMATTER.match(text)
    if not match:
        return {}
    fields: dict[str, str] = {}
    for line in match.group(1).splitlines():
        key, sep, value = line.strip().partition(":")
        if sep and value.strip():
            fields[key.strip()] = value.strip().strip('"')
    return fields


def lint(root: Path) -> tuple[list[str], list[str]]:
    errors: list[str] = []
    warnings: list[str] = []
    index = root / INDEX
    if not index.exists():
        return [f"{INDEX} is missing"], warnings
    facts = sorted(p for p in root.glob("*.md") if p.name != INDEX)
    names: dict[str, str] = {}
    for path in facts:
        fields = _fields(path.read_text(encoding="utf-8"))
        for key in ("name", "description", "type"):
            if key not in fields:
                errors.append(f"{path.name}: frontmatter has no {key!r}")
        if fields.get("type") and fields["type"] not in TYPES:
            errors.append(f"{path.name}: type {fields['type']!r} is not one of {sorted(TYPES)}")
        if "name" in fields:
            if fields["name"] in names:
                errors.append(f"{path.name}: name {fields['name']!r} also used by {names[fields['name']]}")
            names[fields["name"]] = path.name
    listed = set(INDEX_ENTRY.findall(index.read_text(encoding="utf-8")))
    for path in facts:
        if path.name not in listed:
            errors.append(f"{path.name}: not listed in {INDEX}")
    for entry in sorted(listed):
        if not (root / entry).exists():
            errors.append(f"{INDEX}: points at missing {entry}")
    for path in facts:
        for link in LINK.findall(path.read_text(encoding="utf-8")):
            if link not in names:
                warnings.append(f"{path.name}: [[{link}]] has no fact yet")
    return errors, warnings


def main(argv: list[str]) -> int:
    root = Path(argv[1]) if len(argv) > 1 else Path(".")
    errors, warnings = lint(root)
    for w in warnings:
        print(f"warning: {w}")
    for e in errors:
        print(f"error: {e}", file=sys.stderr)
    if not errors:
        print(f"memory: ok ({root})")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
