"""Branch-name gate: `<type>/<card>-<kebab>`.

The shape carries the card number into every commit's context and keeps
branch lists greppable. The traps it catches look correct at a glance:
uppercase, underscores, dots, double or trailing hyphens, non-ASCII letters.

    python tools/branch_name.py feature/142-return-late-fees   # exit 0
    python tools/branch_name.py Feature/142_return             # exit 1
"""

import re
import sys

TYPES = ("feature", "fix", "chore", "docs", "refactor")
PATTERN = re.compile(rf"^({'|'.join(TYPES)})/\d+-[a-z0-9]+(-[a-z0-9]+)*$")
EXEMPT = ("main",)


def problem(name: str) -> str | None:
    """None when the name is valid, otherwise the first reason it is not."""
    if name in EXEMPT or PATTERN.match(name):
        return None
    kind, _, rest = name.partition("/")
    if kind not in TYPES:
        return f"type must be one of {', '.join(TYPES)}; got {kind!r}"
    if not re.match(r"^\d+-", rest):
        return "expected the card number right after the slash: <type>/<card>-<slug>"
    if not rest.isascii():
        return "non-ASCII letters are not allowed"
    if re.search(r"[A-Z]", rest):
        return "uppercase letters are not allowed"
    if re.search(r"[_.]", rest):
        return "use hyphens, not underscores or dots"
    if "--" in rest or rest.endswith("-"):
        return "no double or trailing hyphens"
    return "does not match <type>/<card>-<kebab-slug>"


def main(argv: list[str]) -> int:
    if len(argv) != 2:
        print("usage: branch_name.py <branch>", file=sys.stderr)
        return 2
    reason = problem(argv[1])
    if reason:
        print(f"branch {argv[1]!r}: {reason}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
