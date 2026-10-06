package lab;

import static org.junit.jupiter.api.Assertions.assertTrue;

import io.micrometer.prometheusmetrics.PrometheusConfig;
import io.micrometer.prometheusmetrics.PrometheusMeterRegistry;
import org.junit.jupiter.api.Test;

class OrderMetricsTest {
    @Test
    void scrapeExposesRedAndUseMetrics() {
        PrometheusMeterRegistry reg = new PrometheusMeterRegistry(PrometheusConfig.DEFAULT);
        OrderMetrics m = new OrderMetrics(reg);
        m.place(() -> 1);
        try {
            m.place(() -> {
                throw new IllegalStateException();
            });
        } catch (IllegalStateException ignored) {
            // expected
        }
        String out = reg.scrape();
        assertTrue(out.contains("orders_placed_total{outcome=\"success\"} 1.0"), out);
        assertTrue(out.contains("orders_placed_total{outcome=\"error\"} 1.0"), out);
        assertTrue(out.contains("orders_place_duration_seconds_bucket"), out);
        assertTrue(out.contains("orders_queue_depth 0.0"), out);
    }
}
