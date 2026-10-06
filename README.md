# obs-metrics-alerting

Metrics, dashboards, alert routing, SLO burn-rate alerts, health probes and synthetic checks for a small Orders service, each in its own runnable folder.

## What is inside

| Folder | What it shows | Run |
| --- | --- | --- |
| [`micrometer-prometheus`](./micrometer-prometheus) | RED and saturation metrics for Orders with Micrometer, in Prometheus text format | `mvn -q -B test` |
| [`grafana-dashboards-as-code`](./grafana-dashboards-as-code) | A dashboard kept as JSON and provisioned with its datasource | `python3 check.py` |
| [`alertmanager-rules`](./alertmanager-rules) | Symptom-based alert rules, severity routing and inhibition | `python3 check.py` |
| [`slo-burn-rate`](./slo-burn-rate) | Multi-window burn-rate rules generated from a 99.9% SLO | `python3 gen_rules.py --check` |
| [`actuator-probes`](./actuator-probes) | Spring Boot health groups wired to Kubernetes probes | `python3 check.py` |
| [`blackbox-synthetic-checks`](./blackbox-synthetic-checks) | Outside-in HTTP probing with the blackbox exporter | `docker compose config -q` |
| [`datadog-newrelic-awareness`](./datadog-newrelic-awareness) | How these concepts map to Datadog and New Relic | `python3 check.py` |

All folders use the same tiny Orders domain and the same metric names.

## Prerequisites

- Java 21 and Maven 3.9+ (`micrometer-prometheus`)
- Python 3 with PyYAML (the `check.py` scripts)
- Docker with Compose (optional stacks, and `promtool` / `amtool` validation)

## How to read it

Start with `micrometer-prometheus`, which defines the metrics every other folder queries. Then follow the order in the table: dashboard, alerts, SLO alerts, probes, synthetic checks.
