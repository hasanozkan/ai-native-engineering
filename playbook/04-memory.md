# 4. Memory

An agent starts every session empty. What it knows about *this* team comes
from files it reads at the start. Treat those files like code.

## Shape

- **One fact per file**, with frontmatter: `name`, `description` (one line,
  used to decide relevance), `type`.
- **Four types:** `user` (who you work with and how they like to work),
  `feedback` (corrections and confirmed approaches — always with *why* and
  *how to apply*), `project` (decisions and constraints not visible in code),
  `reference` (where things live outside the repo).
- **An index** (`MEMORY.md`): one line per fact, loaded every session. It is a
  table of contents, not the memory.
- **Links** between facts as `[[name]]`, so a lesson points at its siblings.

## Rules

- Write it **when you learn it**, not at the end.
- **Update, don't duplicate.** Search the index first.
- **Delete what turned out wrong.** A stale fact is worse than none: it is
  believed.
- **Do not store what the repo already says** — code structure, git history,
  conventions files. Memory holds what is *not* derivable.
- **Absolute dates.** "Last week" means nothing next month.
- **The memory is a repository.** Committed, pushed, reviewable, shared by
  every machine and every agent on the team.

[`tools/memory_lint.py`](../tools/memory_lint.py) enforces the shape;
[`examples/memory/`](../examples/memory) shows it.
