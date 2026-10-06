# datadog-newrelic-awareness

A concept mapping from Prometheus to Datadog and New Relic, a Spring Boot vendor profile, and a script that validates both.

## Goal
Show how the Prometheus and Grafana concepts in this repo map to Datadog and New Relic, and how the same Micrometer meters can feed a vendor instead.

## Run it
```
python3 check.py
```
Expected: `vendor mapping ok` (needs PyYAML).

## What it proves
- `mapping.json` has six rows (scrape/export, dashboards, alerting, SLOs, tracing/APM, synthetic checks), each with a Prometheus, Datadog and New Relic equivalent; `check.py` fails on an empty cell.
- `application-vendor.yml` configures the Datadog and New Relic exporters while the `orders.*` meters stay as they are.
- Both exporters are `enabled: false` and read API keys from `${DD_API_KEY:}` and `${NEW_RELIC_API_KEY:}`; `check.py` enforces both.

## Trade-offs
- Awareness only: no vendor account or agent was used, so the mapping reflects documented concepts, not tested behaviour.
- Vendors bill per host, custom metric or ingested volume; high-cardinality tags that are cheap in Prometheus can be costly there.
- Push-based export loses the pull model's built-in "target down" signal.

## When not to use it
- When you have no vendor contract and no plan for one.
- As a feature comparison: product names and capabilities change, so check current vendor documentation.
