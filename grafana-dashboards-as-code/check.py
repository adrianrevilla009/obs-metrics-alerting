#!/usr/bin/env python3
"""Validate committed dashboards and provisioning: JSON shape, unique ids, datasource uids, metric names."""
import json, pathlib, sys
import yaml

here = pathlib.Path(__file__).parent
ds_uids = {d["uid"] for d in yaml.safe_load((here / "provisioning/datasources.yml").read_text())["datasources"]}
known = ("orders_placed_total", "orders_place_duration_seconds_bucket", "orders_queue_depth")
errors = []
for f in sorted((here / "dashboards").glob("*.json")):
    d = json.loads(f.read_text())
    for key in ("uid", "title", "panels", "schemaVersion"):
        if key not in d:
            errors.append(f"{f.name}: missing {key}")
    ids = [p["id"] for p in d.get("panels", [])]
    if len(ids) != len(set(ids)):
        errors.append(f"{f.name}: duplicate panel ids")
    for p in d.get("panels", []):
        if p["datasource"]["uid"] not in ds_uids:
            errors.append(f"{f.name}: panel {p['id']} unknown datasource")
        for t in p.get("targets", []):
            if not any(m in t["expr"] for m in known):
                errors.append(f"{f.name}: panel {p['id']} uses no known orders metric")
if errors:
    print("\n".join(errors)); sys.exit(1)
print("dashboards ok")
