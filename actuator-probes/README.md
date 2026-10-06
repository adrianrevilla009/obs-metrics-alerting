# actuator-probes

Spring Boot Actuator health-group configuration, a Kubernetes Deployment with matching probes, and a script that checks they agree.

## Goal
Configure Actuator health groups so the Kubernetes startup, liveness and readiness probes each check the right thing.

## Run it
```
python3 check.py
```
Expected: `probe config ok` (needs PyYAML).

## What it proves
- `application.yml` enables probes: the liveness group includes only `livenessState`, readiness includes `readinessState` and `db`.
- `deployment.yml` points the startup and liveness probes at `/actuator/health/liveness` and the readiness probe at `/actuator/health/readiness`.
- Graceful shutdown is on with a 20s phase timeout, inside the pod's 30s grace period.
- `check.py` fails if liveness includes anything but `livenessState` or `ping`, if a probe path drifts from its group, or if graceful shutdown is off.

## Trade-offs
- Not run end to end: no Spring Boot app is built or started and no cluster is used, so the YAML is checked for consistency only, not against a live `/actuator/health`.
- Putting `db` in readiness removes pods from service during a database outage, which can turn a partial failure into a full one.
- `show-details: never` hides diagnostic detail from callers.

## When not to use it
- Outside Kubernetes or a similar orchestrator, where nothing consumes the probes.
- For non-Spring services, which have their own health mechanism.
