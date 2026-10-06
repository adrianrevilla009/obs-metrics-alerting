#!/usr/bin/env python3
"""Generate multi-window multi-burn-rate alert rules (Google SRE workbook) for a 99.9% / 30d availability SLO.

Usage: gen_rules.py [--check]   (--check verifies rules.yml is up to date and the budget maths hold)
"""
import pathlib, sys

SLO = 0.999
PERIOD_H = 30 * 24
BUDGET = 1 - SLO
# (burn rate, long window, short window, severity): 2% budget in 1h, 5% in 6h, 10% in 3d
WINDOWS = [(14.4, "1h", "5m", "page"), (6.0, "6h", "30m", "page"), (1.0, "3d", "6h", "ticket")]
ERR = 'sum(rate(orders_placed_total{{outcome="error"}}[{w}])) / sum(rate(orders_placed_total[{w}]))'


def budget_consumed(burn, window_h):
    return burn * window_h / PERIOD_H


def render():
    out = ["groups:", "  - name: orders-slo-burn", "    rules:"]
    for burn, long_w, short_w, sev in WINDOWS:
        thr = f"{burn * BUDGET:.6g}"
        out += [
            f"      - alert: OrdersErrorBudgetBurn{long_w}",
            f"        expr: ({ERR.format(w=long_w)}) > {thr} and ({ERR.format(w=short_w)}) > {thr}",
            f"        labels: {{severity: {sev}, team: orders}}",
            f'        annotations: {{summary: "Burning error budget {burn}x over {long_w}", runbook: "https://example.com/runbooks/orders-slo"}}',
        ]
    return "\n".join(out) + "\n"


if __name__ == "__main__":
    path = pathlib.Path(__file__).with_name("rules.yml")
    text = render()
    if "--check" in sys.argv:
        assert abs(budget_consumed(14.4, 1) - 0.02) < 1e-9, "14.4x for 1h must burn 2% of budget"
        assert abs(budget_consumed(6, 6) - 0.05) < 1e-9, "6x for 6h must burn 5% of budget"
        assert abs(budget_consumed(1, 72) - 0.10) < 1e-9, "1x for 3d must burn 10% of budget"
        if not path.exists() or path.read_text() != text:
            sys.exit("rules.yml is stale: run gen_rules.py")
        print("burn-rate maths and rules.yml ok")
    else:
        path.write_text(text)
        print(f"wrote {path.name}")
