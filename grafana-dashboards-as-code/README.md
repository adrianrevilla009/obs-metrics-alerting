# grafana-dashboards-as-code

An Orders dashboard as JSON, Grafana provisioning files and a Compose file, with a script that validates the dashboard.

## Goal
Keep a Grafana dashboard as reviewed JSON in git and provision it, with its datasource, at startup instead of building it by hand in the UI.

## Run it
```
python3 check.py
docker compose up -d
docker compose down
```
Expected: `check.py` prints `dashboards ok` (needs PyYAML). The compose commands are optional; with them Grafana would listen on port 3000 with the dashboard loaded.

## What it proves
- `dashboards/orders-red.json` has four panels: rate, error ratio, p95 duration and queue depth, using the metric names from `micrometer-prometheus`.
- `provisioning/datasources.yml` registers the datasource with the fixed uid `prom`, which every panel references, so the JSON does not depend on the environment.
- `check.py` fails on missing keys, duplicate panel ids, unknown datasource uids or queries that use none of the Orders metrics.

## Trade-offs
- Not run end to end: the Compose stack was never started here. Prometheus in `compose.yml` has no scrape targets, so the panels would be empty even when it runs.
- `check.py` checks structure only and does not execute the queries.
- Provisioned dashboards cannot be deleted in the UI (`disableDeletion: true`), so changes go through git.
- Hand-written JSON is verbose; at scale export from the UI or generate it.

## When not to use it
- For throwaway exploration dashboards.
- When Terraform or an operator already manages dashboards and a second source of truth would conflict.
