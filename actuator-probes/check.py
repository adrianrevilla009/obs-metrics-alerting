#!/usr/bin/env python3
"""Check that Kubernetes probe paths match the Actuator health groups, and that liveness never depends on dependencies."""
import pathlib, sys
import yaml

here = pathlib.Path(__file__).parent
app = yaml.safe_load((here / "application.yml").read_text())
dep = yaml.safe_load((here / "deployment.yml").read_text())
errors = []

health = app["management"]["endpoint"]["health"]
groups = health["group"]
if not health["probes"]["enabled"]:
    errors.append("probes not enabled")
liveness = set(groups["liveness"]["include"].split(","))
if liveness - {"livenessState", "ping"}:
    errors.append(f"liveness must not include dependencies: {liveness}")
if "readinessState" not in groups["readiness"]["include"]:
    errors.append("readiness must include readinessState")
if "health" not in app["management"]["endpoints"]["web"]["exposure"]["include"]:
    errors.append("health endpoint not exposed")

c = dep["spec"]["template"]["spec"]["containers"][0]
expect = {"startupProbe": "liveness", "livenessProbe": "liveness", "readinessProbe": "readiness"}
for probe, group in expect.items():
    if probe not in c:
        errors.append(f"missing {probe}")
    elif c[probe]["httpGet"]["path"] != f"/actuator/health/{group}":
        errors.append(f"{probe} path must be /actuator/health/{group}")
if app["server"]["shutdown"] != "graceful":
    errors.append("graceful shutdown disabled")
if errors:
    print("\n".join(errors)); sys.exit(1)
print("probe config ok")
