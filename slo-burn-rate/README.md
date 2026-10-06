# slo-burn-rate

A Python generator for multi-window burn-rate alert rules, and the `rules.yml` it produces.

## Goal
Alert on how fast the error budget of a 99.9% / 30-day order-success SLO is being spent, instead of on a fixed error threshold.

## Run it
```
python3 gen_rules.py --check
python3 gen_rules.py
docker run --rm --entrypoint promtool -v "$PWD:/c:ro" prom/prometheus:v2.55.1 check rules /c/rules.yml
```
Expected: `--check` prints `burn-rate maths and rules.yml ok`; the second command rewrites `rules.yml` and prints `wrote rules.yml`. The `promtool` command is optional and was not run here.

## What it proves
- `gen_rules.py --check` asserts that 14.4x for 1h spends 2% of the budget, 6x for 6h spends 5% and 1x for 3d spends 10%.
- `rules.yml` has three alerts: 1h/5m at 0.0144 and 6h/30m at 0.006 (both page), and 3d/6h at 0.001 (ticket). Each needs the long and the short window above the threshold.
- The `--check` mode also fails if `rules.yml` differs from what the script generates, and the severity and team labels match the routing in `alertmanager-rules`.

## Trade-offs
- The rules were not checked with `promtool` or unit-tested with `promtool test rules`.
- Ratios come from raw counters at query time; at scale, recording rules per window are cheaper.
- Low-traffic services give noisy ratios, and the rules have no `for:` clause.

## When not to use it
- For services with no real SLO or very low request volume.
- When a simple threshold alert is enough and nobody tracks an error budget.
