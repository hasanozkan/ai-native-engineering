# AI-native engineering

[![ci](https://github.com/hasanozkan/ai-native-engineering/actions/workflows/ci.yml/badge.svg)](https://github.com/hasanozkan/ai-native-engineering/actions/workflows/ci.yml)
![license](https://img.shields.io/badge/license-MIT-green)

**A playbook, templates and three small tools for teams that build software
with AI coding agents** — distilled from running a product where agents
write most of the code and humans own the decisions.

The premise: agents are fast and tireless, and wrong with total confidence.
Supervising every keystroke does not scale. Putting agents inside the same
**specs, conventions and gates** that keep humans honest does — provided that
structure is *mechanical*, has *one owner per rule*, and every gate has been
seen to fail.

## Playbook

| | |
|---|---|
| [1. Principles](playbook/01-principles.md) | Spec leads · one owner per rule · gates not guidelines · a gate is trusted after it fails · report outcomes as they are |
| [2. The loop](playbook/02-the-loop.md) | Card → groom together → vertical slice → gates → human acceptance → merge = deploy → write it down |
| [3. Gates](playbook/03-gates.md) | What to check mechanically, negative controls, why chained steps fail silently |
| [4. Memory](playbook/04-memory.md) | An agent's memory as a versioned repository of one-fact files and an index |
| [5. Approval boundaries](playbook/05-approval-boundaries.md) | What agents do without asking, what waits for a human |
| [6. Failure patterns](playbook/06-failure-patterns.md) | Ten traps, each with a symptom and a counter |

## Templates

[`AGENTS.md`](templates/AGENTS.md) (with a one-line [`CLAUDE.md`](templates/CLAUDE.md)
pointing at it) · [feature spec](templates/feature-spec.md) with DoR/DoD ·
[ADR](templates/adr.md) · [PR description](templates/pull_request.md) ·
[memory fact](templates/memory/fact.md) — and a worked
[example memory](examples/memory).

## Tools

Plain Python, no dependencies, each with tests.

| Tool | Does |
|---|---|
| [`branch_name.py`](tools/branch_name.py) | Enforces `<type>/<card>-<kebab>` and names the trap that failed (uppercase, `_`, `.`, `--`, non-ASCII) |
| [`memory_lint.py`](tools/memory_lint.py) | Validates a memory directory: frontmatter, types, unique names, index ↔ files, dangling links |
| [`negative_control.py`](tools/negative_control.py) | Runs a check on the healthy tree and after one deliberate mutation; passes only if the check goes red — then restores the file |

```sh
make install
make check      # lint, strict types, tests, the example memory, and a self-check:
                # the repo's own test gate must catch a mutation in branch_name.py
```

## Companion

[spec-driven-ddd-python](https://github.com/hasanozkan/spec-driven-ddd-python)
shows the code side of the same approach: numbered spec rules traced to
tests, bounded contexts that can only talk through events, and architecture
enforced as build gates.

---

By [Hasan Özkan](https://github.com/hasanozkan) · [LinkedIn](https://www.linkedin.com/in/hasanozkan/)
