from pathlib import Path

from tools.memory_lint import lint

EXAMPLES = Path(__file__).resolve().parent.parent / "examples" / "memory"


def _fact(root: Path, file: str, name: str, kind: str = "feedback", body: str = "") -> None:
    (root / file).write_text(
        f"---\nname: {name}\ndescription: one line\nmetadata:\n  type: {kind}\n---\n{body}\n",
        encoding="utf-8",
    )


def test_the_shipped_examples_are_clean() -> None:
    errors, _ = lint(EXAMPLES)
    assert errors == []


def test_a_fact_missing_from_the_index_and_a_dangling_index_entry(tmp_path: Path) -> None:
    _fact(tmp_path, "a.md", "a")
    (tmp_path / "MEMORY.md").write_text("- [B](b.md) — gone\n", encoding="utf-8")
    errors, _ = lint(tmp_path)
    assert "a.md: not listed in MEMORY.md" in errors
    assert "MEMORY.md: points at missing b.md" in errors


def test_bad_frontmatter_unknown_type_and_duplicate_names(tmp_path: Path) -> None:
    (tmp_path / "x.md").write_text("no frontmatter\n", encoding="utf-8")
    _fact(tmp_path, "y.md", "same", kind="opinion")
    _fact(tmp_path, "z.md", "same")
    (tmp_path / "MEMORY.md").write_text("[x](x.md) [y](y.md) [z](z.md)\n", encoding="utf-8")
    errors, _ = lint(tmp_path)
    assert any("x.md: frontmatter has no 'name'" in e for e in errors)
    assert any("type 'opinion'" in e for e in errors)
    assert any("also used by" in e for e in errors)


def test_unknown_links_warn_but_do_not_fail(tmp_path: Path) -> None:
    _fact(tmp_path, "a.md", "a", body="see [[not-written-yet]]")
    (tmp_path / "MEMORY.md").write_text("[A](a.md)\n", encoding="utf-8")
    errors, warnings = lint(tmp_path)
    assert errors == []
    assert warnings == ["a.md: [[not-written-yet]] has no fact yet"]
