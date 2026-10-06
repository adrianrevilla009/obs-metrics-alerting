#!/usr/bin/env python3
"""Check the concept mapping is complete and the vendor profile keeps secrets out of git and exporters off by default."""
import json, pathlib, sys
import yaml

here = pathlib.Path(__file__).parent
errors = []
for row in json.loads((here / "mapping.json").read_text())["concepts"]:
    for k in ("concept", "prometheus", "datadog", "newrelic"):
        if not row.get(k):
            errors.append(f"{row.get('concept')}: empty {k}")

cfg = yaml.safe_load((here / "application-vendor.yml").read_text())["management"]
for vendor in ("datadog", "newrelic"):
    exp = cfg[vendor]["metrics"]["export"]
    if exp["enabled"] is not False:
        errors.append(f"{vendor}: exporter must be disabled by default")
    if not str(exp["api-key"]).startswith("${"):
        errors.append(f"{vendor}: api-key must come from the environment")
if errors:
    print("\n".join(errors)); sys.exit(1)
print("vendor mapping ok")
