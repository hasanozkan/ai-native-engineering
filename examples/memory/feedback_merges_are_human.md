---
name: merges-are-human
description: Code and infrastructure merges wait for an explicit "merge"; docs PRs may auto-merge when green
metadata:
  type: feedback
---

Open the PR, get it green, then ask. Docs-only PRs are delegated: auto-merge
when the checks pass.

**Why:** merging to main deploys (see [[deploy-is-merge]]); the person who
answers for production holds that button.

**How to apply:** "merge it" covers that one PR. It is not standing approval
for the next one.
