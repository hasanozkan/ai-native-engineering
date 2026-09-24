import pytest

from tools.branch_name import main, problem


@pytest.mark.parametrize(
    "name",
    ["feature/142-return-late-fees", "fix/7-null-due-date", "docs/1830-profile", "main"],
)
def test_valid_names_pass(name: str) -> None:
    assert problem(name) is None


@pytest.mark.parametrize(
    ("name", "reason"),
    [
        ("feat/142-x", "type must be"),
        ("feature/return-late-fees", "card number"),
        ("feature/142-Return", "uppercase"),
        ("feature/142-return_fees", "underscores"),
        ("feature/142-v1.2", "underscores or dots"),
        ("feature/142-return--fees", "double or trailing"),
        ("feature/142-return-", "double or trailing"),
        ("feature/142-café-menu", "non-ASCII"),
    ],
)
def test_the_traps_that_look_correct_are_named(name: str, reason: str) -> None:
    found = problem(name)
    assert found is not None and reason in found


def test_exit_codes() -> None:
    assert main(["x", "fix/1-a"]) == 0
    assert main(["x", "Fix/1-a"]) == 1
    assert main(["x"]) == 2
