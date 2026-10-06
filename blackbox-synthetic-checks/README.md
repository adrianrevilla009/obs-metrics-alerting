# blackbox-synthetic-checks

Prometheus blackbox exporter, scrape configuration and alert rules, plus an nginx stand-in target, wired in Compose.

## Goal
Probe the Orders service from the outside so an outage is detected even when the app's own metrics are silent.

## Run it
```
docker run --rm --entrypoint promtool -v "$PWD:/c:ro" prom/prometheus:v2.55.1 check config /c/prometheus.yml
docker compose config -q
docker compose up -d
docker compose down
```
Expected: the `promtool` command should report the config and `probe-rules.yml` as valid, and `docker compose config -q` prints nothing. None of these were run here.

## What it proves
- `blackbox.yml` defines `http_2xx` and `tcp_connect` modules with 5s timeouts.
- `prometheus.yml` uses the relabel pattern that turns each target into a `/probe?target=` request to `blackbox:9115`; the one target is `http://target:80/`.
- `probe-rules.yml` has `OrdersEndpointDown` (`probe_success == 0` for 3m, page) and `TlsCertExpiringSoon` (under 14 days, ticket).
- `compose.yml` starts the exporter on 9115, Prometheus on 9090 and nginx, which stands in for the service; 8080 is only its host mapping.

## Trade-offs
- Not run end to end: the stack was never started and no probe result was observed.
- A probe from inside the same network proves less than one from outside; real checks run from several regions.
- Probing a health endpoint shows reachability, not that a user can place an order.
- Only `http_2xx` is used; `tcp_connect` is defined but no job references it.

## When not to use it
- For internal-only components with no network endpoint.
- When a managed synthetic monitoring service already covers the same journeys and regions.
