---
name: negative-control
description: Break a new gate on purpose once and watch it fail before trusting its green
metadata:
  type: feedback
---

A check that has only ever been green is unproven.

**Why:** a task runner once printed a failure and exited 0; the gate was
green for weeks while measuring nothing.

**How to apply:** after adding or changing a gate, run
`tools/negative_control.py` with a one-line mutation it must catch. Record the
red run in the PR description.
