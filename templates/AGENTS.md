# Instructions for coding agents

<!-- The rules live in ONE place. This file points at them; it does not restate them. -->

Read before changing anything:

- Conventions: `docs/CONVENTIONS.md` (the only copy — link to it, never paste it)
- Architecture decisions: `docs/adr/`
- The feature you are working on: `specs/features/<n>-<slug>/`
- Team memory: `<memory repo>/MEMORY.md`, then the facts it lists that are relevant

Working agreement:

1. Implement numbered spec rules; if the rule you need is not written, write it first and ask.
2. Branch: `<type>/<card>-<kebab>`. One card, one slice, one PR.
3. Run `make check` before you say a change is done, and report its output as it is.
4. A new or changed gate is verified by breaking it once (`tools/negative_control.py`).
5. Ask before: merging code or infra, deleting anything you did not create,
   applying infrastructure, spending money, or sending messages as the team.
6. When you learn something the next session would have to rediscover, write it to memory now.
