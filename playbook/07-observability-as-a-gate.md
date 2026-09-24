# 7. Observability as a gate

The build proves the code does what the tests say. Production proves nothing
unless someone is told when it stops. Observability gets the same treatment
as everything else here: a contract, and gates that fail.

## Telemetry is part of the contract

Write down what a service emits — metric names, types, the attributes you
will filter and group by — in a file next to the specs, and test the service
against it. Dashboards and alerts are then written against that file, not
against whatever a scrape happened to show one afternoon.

```yaml
# telemetry.yaml
metrics:
  - name: library.refusals
    type: counter
    attributes: [library.code]
```

With the contract in place three cheap gates become possible:

| Gate | Fails when |
|---|---|
| The service's test scrapes `/metrics` and compares with the contract | a metric or attribute is renamed or dropped |
| Every series **and label** a dashboard or alert queries is looked up in the contracts | a panel would silently go empty |
| Alert rules run under `promtool test rules`, each **both ways** | a rule never fires, or fires on normal traffic |

Name things by the OpenTelemetry semantic conventions where they exist
(`http.server.request.duration`, `gen_ai.client.token.usage`); every backend
then reads them without a mapping, and a second implementation in another
language can be held to the same file.

## Count decisions where they are made

For an AI agent the interesting numbers are behavioural, not just tokens and
latency: how often a write was proposed that nobody asked for, how often tool
output looked like an instruction, how often a person confirmed despite a
warning. Those are only visible if the guard that decided also counts —
inside the code path, not reconstructed from logs later.

## Failure patterns

| Pattern | Symptom | Counter |
|---|---|---|
| **The empty panel** | A metric was renamed; the dashboard shows "No data" and nobody notices for weeks | Check queries against the contract in CI |
| **The alert that never fires** | The rule has a typo'd label; it evaluates to nothing, forever | Unit-test every rule on synthetic series, firing and quiet |
| **The stale series** | A deleted job's last value keeps showing; the graph looks alive | Alert on staleness (`absent`, `time() - timestamp()`), not just on values |
| **Alerts to a place nobody reads** | The alert fires into an issue tracker or a dashboard | Route alerts to where people already are (chat, pager); issues are records |
| **The zero that means "broken"** | A counter reads 0; the feature is fine, or the instrumentation is dead | Negative control: drive the path once in a test and see the counter move |
| **Parallel tests share a meter** | A count is 2 instead of 1 in CI only | Process-wide metric listeners: run metric tests alone or assert on deltas |

See it applied: [llm-tool-calling-assistant](https://github.com/hasanozkan/llm-tool-calling-assistant)
(LLM telemetry and tested alerts), [spec-driven-ddd-python](https://github.com/hasanozkan/spec-driven-ddd-python)
and [-dotnet](https://github.com/hasanozkan/spec-driven-ddd-dotnet) (one telemetry
contract, two languages), [gitops-reference](https://github.com/hasanozkan/gitops-reference)
(dashboards and alerts checked against the contracts).
