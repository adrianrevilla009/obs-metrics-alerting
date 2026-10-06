# micrometer-prometheus

A small Java class that records RED and saturation metrics for placing orders with Micrometer, plus a test that checks the Prometheus scrape output.

## Goal
Expose custom rate, error and duration (RED) metrics and a queue-depth saturation gauge for the Orders domain in Prometheus text format.

## Run it
```
mvn -q -B test
```
Expected: no output and exit code 0 (quiet mode); `OrderMetricsTest` passes. Without `-q` Maven reports one test run, no failures.

`OrderMetrics.main` also prints a scrape of one successful and one failed order. It is not run through Maven here, because `pom.xml` does not pin the exec plugin; run it from an IDE or with `java -cp` on the compiled classes.

## What it proves
- `orders.placed` is a counter tagged `outcome=success|error`; the test asserts `orders_placed_total{outcome="success"} 1.0` and the same for `error`.
- `orders.place.duration` is a timer with a percentile histogram and 100 ms / 500 ms SLO buckets, scraped as `orders_place_duration_seconds_bucket`. The other folders query these names.
- `orders.queue.depth` is a gauge that rises while an order is in flight and returns to `0.0` afterwards.

## Trade-offs
- Plain Java, no Spring: the registry is the subject. In Spring Boot the same meters would be exposed on `/actuator/prometheus`.
- Tags must stay low-cardinality; never tag with an order id.
- Histograms cost memory per bucket per tag combination.

## When not to use it
- When the platform already instruments what you need, such as HTTP server metrics in Spring Boot.
- For debugging a single request: use traces or logs, not metrics.
