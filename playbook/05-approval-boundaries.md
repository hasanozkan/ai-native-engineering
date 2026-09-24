# 5. Approval boundaries

Speed comes from agents doing the reversible work without asking. Safety
comes from humans holding the irreversible buttons.

| Agent does without asking | Agent asks first |
|---|---|
| Read anything, run tests, run linters | Merge code to `main` (= deploy) |
| Create branches, commit, push, open PRs | Delete data, repositories or branches that are not its own |
| Fix its own failing checks | Change infrastructure state (`apply`, not `plan`) |
| Write and update memory and docs | Anything that costs money or sends a message as the team |
| Open cards for problems it finds | Dismiss a security or quality finding |

Two refinements that worked well:

- **Low-risk merges can be delegated explicitly** ("docs PRs may auto-merge
  when green"). The delegation is written down, scoped and revocable.
- **An approval covers one action.** "Yes, merge it" is not "yes, merge
  everything from now on".
