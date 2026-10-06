package lab;

import io.micrometer.core.instrument.Counter;
import io.micrometer.core.instrument.Gauge;
import io.micrometer.core.instrument.MeterRegistry;
import io.micrometer.core.instrument.Timer;
import io.micrometer.prometheusmetrics.PrometheusConfig;
import io.micrometer.prometheusmetrics.PrometheusMeterRegistry;
import java.time.Duration;
import java.util.concurrent.atomic.AtomicInteger;
import java.util.function.Supplier;

/** RED (rate, errors, duration) for order placement plus a USE-style saturation gauge. */
public class OrderMetrics {
    private final MeterRegistry registry;
    private final AtomicInteger queueDepth = new AtomicInteger();
    private final Timer duration;

    public OrderMetrics(MeterRegistry registry) {
        this.registry = registry;
        this.duration = Timer.builder("orders.place.duration")
                .description("Latency of placing an order")
                .publishPercentileHistogram()
                .serviceLevelObjectives(Duration.ofMillis(100), Duration.ofMillis(500))
                .register(registry);
        Gauge.builder("orders.queue.depth", queueDepth, AtomicInteger::get)
                .description("Pending orders (saturation)")
                .register(registry);
    }

    public <T> T place(Supplier<T> work) {
        queueDepth.incrementAndGet();
        try {
            T result = duration.record(work);
            Counter.builder("orders.placed").tag("outcome", "success").register(registry).increment();
            return result;
        } catch (RuntimeException e) {
            Counter.builder("orders.placed").tag("outcome", "error").register(registry).increment();
            throw e;
        } finally {
            queueDepth.decrementAndGet();
        }
    }

    public static void main(String[] args) {
        PrometheusMeterRegistry reg = new PrometheusMeterRegistry(PrometheusConfig.DEFAULT);
        OrderMetrics m = new OrderMetrics(reg);
        m.place(() -> "ok");
        try {
            m.place(() -> {
                throw new IllegalStateException("boom");
            });
        } catch (IllegalStateException ignored) {
            // expected: counted as outcome=error
        }
        System.out.println(reg.scrape());
    }
}
