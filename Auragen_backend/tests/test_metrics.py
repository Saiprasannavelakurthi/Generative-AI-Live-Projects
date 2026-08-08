from utils.metrics import SystemMetricsTracker, Timer


def test_timer_elapsed():
    timer = Timer()
    assert timer.elapsed() == 0.0
    timer.start()
    assert timer.is_running() is True
    assert timer.elapsed() >= 0.0
    timer.reset()
    assert timer.is_running() is False


def test_metrics_tracker_recording():
    tracker = SystemMetricsTracker()
    summary_initial = tracker.get_summary()
    assert summary_initial["total_generations"] == 0
    assert summary_initial["cache_hit_rate_pct"] == 0.0

    tracker.record_generation(latency_sec=0.5, cached=False, model_name="llama-3.1-8b-instant")
    tracker.record_generation(latency_sec=0.0, cached=True, model_name="llama-3.1-8b-instant")
    tracker.record_generation(latency_sec=1.0, cached=False, model_name="llama-3.3-70b-versatile", fallback=True)
    tracker.record_error("api_error")
    tracker.update_connections(3)

    summary = tracker.get_summary()
    assert summary["total_generations"] == 3
    assert summary["cache_hits"] == 1
    assert summary["cache_misses"] == 2
    assert summary["cache_hit_rate_pct"] == 33.33
    assert summary["avg_latency_ms"] == 750.0
    assert summary["min_latency_ms"] == 500.0
    assert summary["max_latency_ms"] == 1000.0
    assert summary["fallback_activations"] == 1
    assert summary["error_count"] == 1
    assert summary["active_websocket_sessions"] == 3
    assert summary["model_usage"]["llama-3.1-8b-instant"] == 2
    assert summary["model_usage"]["llama-3.3-70b-versatile"] == 1
