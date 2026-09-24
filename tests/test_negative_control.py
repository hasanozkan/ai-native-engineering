import sys
from pathlib import Path

import pytest

from tools.negative_control import main, probe


def _project(tmp_path: Path) -> tuple[Path, str]:
    rule = tmp_path / "rule.py"
    rule.write_text("def fee(days):\n    return min(days * 25, 1000)\n", encoding="utf-8")
    check = tmp_path / "check.py"
    check.write_text(
        "import sys\nsys.path.insert(0, sys.argv[1])\nfrom rule import fee\n"
        "sys.exit(0 if fee(100) == 1000 else 1)\n",
        encoding="utf-8",
    )
    return rule, f"{sys.executable} {check} {tmp_path}"


def test_a_real_gate_passes_healthy_fails_mutated_and_the_file_is_restored(tmp_path: Path) -> None:
    rule, check = _project(tmp_path)
    before = rule.read_text(encoding="utf-8")
    assert probe(check, rule, "min(days * 25, 1000)", "days * 25") == (0, 1)
    assert rule.read_text(encoding="utf-8") == before
    assert (
        main(
            [
                "--check",
                check,
                "--file",
                str(rule),
                "--replace",
                "min(days * 25, 1000)",
                "--with",
                "days * 25",
            ]
        )
        == 0
    )


def test_a_gate_that_misses_the_mutation_is_reported(tmp_path: Path) -> None:
    rule, _ = _project(tmp_path)
    always_green = f"{sys.executable} -c pass"
    assert main(["--check", always_green, "--file", str(rule), "--replace", "1000", "--with", "9"]) == 1


def test_a_mutation_that_matches_nothing_is_refused(tmp_path: Path) -> None:
    rule, check = _project(tmp_path)
    with pytest.raises(ValueError, match="no-op"):
        probe(check, rule, "does-not-exist", "x")
