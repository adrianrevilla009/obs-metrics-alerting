# alertmanager-rules

Two Prometheus alert rules for Orders, an Alertmanager routing tree, and a script that cross-checks them.

## Goal
Write symptom-based alert rules and route them by severity with grouping, repeat intervals and inhibition.

## Run it
```
python3 check.py
docker run --rm --entrypoint amtool -v "$PWD:/c:ro" prom/alertmanager:v0.27.0 check-config /c/alertmanager.yml
```
Expected: `check.py` prints `rules and routing ok` (needs PyYAML). The `amtool` command is optional and was not run here.

## What it proves
- `rules.yml` has `OrdersHighErrorRatio` (page, error ratio above 5% for 10m) and `OrdersQueueSaturated` (ticket, queue depth above 100 for 15m), each with `for`, labels and a runbook annotation.
- `alertmanager.yml` sends `severity="page"` to `oncall` with a 1h repeat and `severity="ticket"` to `ticket-queue`; a page alert inhibits a ticket alert of the same `team`.
- `check.py` fails if a route points at an undefined receiver or an alert has a severity that no route matches.

## Trade-offs
- The receivers are webhooks on `localhost:9095` and the runbook links use `example.com`; real setups use PagerDuty or Slack with secrets kept outside git.
- `check.py` does not parse PromQL. `promtool check rules` and `promtool test rules` would; neither was run here.
- Fixed thresholds are simple but ignore the error budget; `slo-burn-rate` replaces them.

## When not to use it
- When alerts would fire on causes such as CPU or restarts rather than user-visible symptoms.
- When the on-call tool already handles routing and deduplication, which makes Alertmanager an extra hop.
