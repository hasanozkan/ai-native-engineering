"""Trust a gate only after it has failed (playbook/03-gates.md).

Runs CHECK on the healthy tree (must exit 0), applies one textual mutation to
FILE (must make CHECK exit non-zero), and always restores FILE. Exit status:
0 = the gate passes healthy and catches the mutation; 1 = it does not.

    python tools/negative_control.py --check "make test" \\
        --file src/rules.py --replace "min(fee, cap)" --with "fee"
"""

import argparse
import shlex
import subprocess
import sys
from pathlib import Path


def run(check: str) -> int:
    return subprocess.run(shlex.split(check), capture_output=True, check=False).returncode


def probe(check: str, file: Path, old: str, new: str) -> tuple[int, int]:
    """Returns (healthy exit code, mutated exit code)."""
    original = file.read_text(encoding="utf-8")
    if old not in original:
        raise ValueError(f"{old!r} not found in {file} — the mutation would be a no-op")
    healthy = run(check)
    try:
        file.write_text(original.replace(old, new, 1), encoding="utf-8")
        mutated = run(check)
    finally:
        file.write_text(original, encoding="utf-8")
    return healthy, mutated


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--check", required=True)
    parser.add_argument("--file", required=True, type=Path)
    parser.add_argument("--replace", required=True, dest="old")
    parser.add_argument("--with", required=True, dest="new")
    args = parser.parse_args(argv)
    healthy, mutated = probe(args.check, args.file, args.old, args.new)
    print(f"healthy tree: exit {healthy} · mutated tree: exit {mutated}")
    if healthy != 0:
        print("FAIL: the check is already red on the healthy tree — fix that first")
        return 1
    if mutated == 0:
        print("FAIL: the mutation went unnoticed — this gate does not measure what you think")
        return 1
    print("ok: the gate passes when healthy and fails when broken")
    return 0


if __name__ == "__main__":
    sys.exit(main())
