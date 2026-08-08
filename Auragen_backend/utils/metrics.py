import time
from threading import Lock


class Timer:
    """
    Simple performance timer.
    """

    def __init__(self):
        self.start_time: float | None = None

    def start(self) -> None:
        self.start_time = time.perf_counter()

    def elapsed(self) -> float:
        if self.start_time is None:
            return 0.0
        return round(time.perf_counter() - self.start_time, 4)

    def reset(self) -> None:
        self.start_time = None

    def restart(self) -> None:
        self.start()

    def is_running(self) -> bool:
        return self.start_time is not None


class SystemMetricsTracker:
    """
    Thread-safe tracker for system-wide performance, cache utilization,
    latency telemetry, and error rates.
    """

    def __init__(self):
        self._lock = Lock()
        self.total_generations = 0
        self.cache_hits = 0
        self.cache_misses = 0
        self.fallback_activations = 0
        self.error_count = 0
        self.total_latency_sec = 0.0
        self.min_latency_sec = float("inf")
        self.max_latency_sec = 0.0
        self.model_usage: dict[str, int] = {}
        self.active_websocket_sessions = 0

    def record_generation(
        self,
        latency_sec: float,
        cached: bool,
        model_name: str = "groq",
        fallback: bool = False,
    ) -> None:
        with self._lock:
            self.total_generations += 1
            if cached:
                self.cache_hits += 1
            else:
                self.cache_misses += 1
                self.total_latency_sec += latency_sec
                if latency_sec < self.min_latency_sec:
                    self.min_latency_sec = latency_sec
                if latency_sec > self.max_latency_sec:
                    self.max_latency_sec = latency_sec

            if fallback:
                self.fallback_activations += 1

            if model_name:
                self.model_usage[model_name] = (
                    self.model_usage.get(model_name, 0) + 1
                )

    def record_error(self, error_type: str = "generic") -> None:
        with self._lock:
            self.error_count += 1

    def update_connections(self, count: int) -> None:
        with self._lock:
            self.active_websocket_sessions = count

    def get_summary(self) -> dict:
        with self._lock:
            total_cache = self.cache_hits + self.cache_misses
            cache_hit_rate = (
                round((self.cache_hits / total_cache) * 100, 2)
                if total_cache > 0
                else 0.0
            )
            avg_latency = (
                round((self.total_latency_sec / self.cache_misses) * 1000, 2)
                if self.cache_misses > 0
                else 0.0
            )
            min_lat = (
                round(self.min_latency_sec * 1000, 2)
                if self.min_latency_sec != float("inf")
                else 0.0
            )
            max_lat = round(self.max_latency_sec * 1000, 2)

            return {
                "total_generations": self.total_generations,
                "cache_hits": self.cache_hits,
                "cache_misses": self.cache_misses,
                "cache_hit_rate_pct": cache_hit_rate,
                "avg_latency_ms": avg_latency,
                "min_latency_ms": min_lat,
                "max_latency_ms": max_lat,
                "fallback_activations": self.fallback_activations,
                "error_count": self.error_count,
                "model_usage": self.model_usage.copy(),
                "active_websocket_sessions": self.active_websocket_sessions,
            }


metrics_tracker = SystemMetricsTracker()