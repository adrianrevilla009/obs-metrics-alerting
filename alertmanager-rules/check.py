#!/usr/bin/env python3
"""Lint alert rules and the Alertmanager routing tree: required fields, route receivers exist, every severity is routed."""
import pathlib, sys
import yaml

here = pathlib.Path(__file__).parent
rules = yaml.safe_load((here / "rules.yml").read_text())
am = yaml.safe_load((here / "alertmanager.yml").read_text())
errors = []

receivers = {r["name"] for r in am["receivers"]}
routes = am["route"].get("routes", [])
routed = set()
if am["route"]["receiver"] not in receivers:
    errors.append("root receiver undefined")
for r in routes:
    if r["receiver"] not in receivers:
        errors.append(f"route to undefined receiver {r['receiver']}")
    for m in r["matchers"]:
        if m.startswith("severity="):
            routed.add(m.split("=", 1)[1].strip('"'))

for g in rules["groups"]:
    for a in g["rules"]:
        n = a["alert"]
        for k in ("expr", "for", "labels", "annotations"):
            if k not in a:
                errors.append(f"{n}: missing {k}")
        if a.get("labels", {}).get("severity") not in routed:
            errors.append(f"{n}: severity not routed")
        if "runbook" not in a.get("annotations", {}):
            errors.append(f"{n}: no runbook annotation")
if errors:
    print("\n".join(errors)); sys.exit(1)
print("rules and routing ok")
