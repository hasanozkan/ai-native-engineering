# 3. Gates

A gate turns a convention into a build failure. Each one below is cheap to
run locally and runs again in CI.

| Gate | Fails when | Tool here |
|---|---|---|
| Branch name | the branch does not match `<type>/<card>-<kebab>` | [`tools/branch_name.py`](../tools/branch_name.py) |
| Architecture | a module imports what it must not | import-linter / dependency-cruiser |
| Traceability | a spec rule has no test, or a test cites no rule | see *spec-driven-ddd-python* |
| Contract snapshot | an API changed but its committed snapshot did not | generated OpenAPI/AsyncAPI, diffed |
| Secrets | a credential enters the history | gitleaks |
| Memory hygiene | a memory file is malformed or missing from the index | [`tools/memory_lint.py`](../tools/memory_lint.py) |

## Verify the gate, not just the code

A gate that has never been red is a hypothesis. [`tools/negative_control.py`](../tools/negative_control.py)
runs a check twice: on the healthy tree (must pass) and after a deliberate
mutation (must fail), then restores the tree.

```sh
python tools/negative_control.py \
  --check "make test" \
  --file src/rules.py --replace "min(fee, cap)" --with "fee"
```

Two failure modes this catches, both seen in practice:

- **The wrapper swallows the exit code.** A task runner prints the failure
  and exits 0; CI stays green forever.
- **The gate measures the wrong thing.** It checks a claim (a version string
  in one file) instead of the effect (what was actually installed).

## Chains fail silently

"Wait for CI; merge; release" run as one background script is three gates in
a row. If the merge step fails quietly, the release ships the *old* code with
a green badge. Each step must check the previous step's **measured result**
(PR state is `MERGED`; the release's commit equals the merge commit) and stop
otherwise.
