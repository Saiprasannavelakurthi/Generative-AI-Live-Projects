import { useState, useEffect, useCallback } from "react";

export default function AnalyticsModal({ isOpen, onClose }) {
  const [metrics, setMetrics] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const fetchMetrics = useCallback(async () => {
    setLoading(true);
    setError(null);
    try {
      const res = await fetch("http://127.0.0.1:8000/api/v1/metrics");
      if (!res.ok) {
        throw new Error(`Metrics API returned ${res.status}`);
      }
      const json = await res.json();
      setMetrics(json.data);
    } catch (err) {
      console.error("Failed to fetch backend metrics:", err);
      setError("Unable to connect to backend metrics API.");
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    let timer;
    if (isOpen) {
      const loadMetrics = async () => {
        await fetchMetrics();
      };
      loadMetrics();
      timer = setInterval(fetchMetrics, 4000);
    }
    return () => {
      if (timer) clearInterval(timer);
    };
  }, [isOpen, fetchMetrics]);

  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-slate-900/70 backdrop-blur-sm p-4">
      <div className="relative w-full max-w-2xl rounded-2xl bg-white p-6 shadow-2xl border border-slate-200 space-y-6 animate-in fade-in zoom-in duration-200">
        
        {/* Header */}
        <div className="flex items-center justify-between border-b border-slate-100 pb-4">
          <div className="flex items-center gap-3">
            <span className="flex h-10 w-10 items-center justify-center rounded-xl bg-indigo-50 text-indigo-600 text-xl font-bold">
              📊
            </span>
            <div>
              <h2 className="text-lg font-bold text-slate-800">
                AuraGen Live System Telemetry
              </h2>
              <p className="text-xs text-slate-500">
                Real-time Backend Metrics, LLM Response Speeds & Cache Performance
              </p>
            </div>
          </div>
          <button
            onClick={onClose}
            className="rounded-lg p-2 text-slate-400 hover:bg-slate-100 hover:text-slate-600 transition-colors"
          >
            ✕
          </button>
        </div>

        {/* Content */}
        {loading && !metrics ? (
          <div className="py-12 text-center text-slate-500 text-sm">
            <span className="inline-block animate-spin text-indigo-600 text-xl mb-2">⏳</span>
            <p>Loading real-time telemetry metrics...</p>
          </div>
        ) : error ? (
          <div className="rounded-xl bg-red-50 p-4 text-center text-xs text-red-600 border border-red-200">
            ⚠️ {error}
            <button
              onClick={fetchMetrics}
              className="mt-3 block mx-auto rounded-md bg-red-600 px-3 py-1.5 text-white text-xs font-semibold"
            >
              Retry Connection
            </button>
          </div>
        ) : metrics ? (
          <div className="space-y-5">
            {/* Stat Cards Grid */}
            <div className="grid grid-cols-2 sm:grid-cols-4 gap-3">
              <div className="rounded-xl bg-slate-50 p-3 border border-slate-200/80">
                <span className="text-[10px] font-semibold uppercase tracking-wider text-slate-400 block mb-1">
                  Total UI Generations
                </span>
                <span className="text-2xl font-bold text-slate-800">
                  {metrics.total_generations}
                </span>
              </div>

              <div className="rounded-xl bg-indigo-50/50 p-3 border border-indigo-100">
                <span className="text-[10px] font-semibold uppercase tracking-wider text-indigo-500 block mb-1">
                  Cache Hit Rate
                </span>
                <span className="text-2xl font-bold text-indigo-700">
                  {metrics.cache_hit_rate_pct}%
                </span>
              </div>

              <div className="rounded-xl bg-emerald-50/50 p-3 border border-emerald-100">
                <span className="text-[10px] font-semibold uppercase tracking-wider text-emerald-600 block mb-1">
                  Avg LLM Latency
                </span>
                <span className="text-2xl font-bold text-emerald-700">
                  {metrics.avg_latency_ms > 0 ? `${metrics.avg_latency_ms} ms` : "Instant (Cached)"}
                </span>
              </div>

              <div className="rounded-xl bg-purple-50/50 p-3 border border-purple-100">
                <span className="text-[10px] font-semibold uppercase tracking-wider text-purple-600 block mb-1">
                  Active WS Sessions
                </span>
                <span className="text-2xl font-bold text-purple-700">
                  {metrics.active_websocket_sessions}
                </span>
              </div>
            </div>

            {/* Cache Efficiency Bar */}
            <div className="rounded-xl bg-slate-50 p-4 border border-slate-200/80 space-y-2">
              <div className="flex justify-between text-xs font-semibold text-slate-700">
                <span>Cache Optimization Efficiency</span>
                <span>{metrics.cache_hits} Hits / {metrics.cache_misses} Misses</span>
              </div>
              <div className="h-2.5 w-full rounded-full bg-slate-200 overflow-hidden flex">
                <div
                  className="bg-indigo-600 h-full transition-all duration-500"
                  style={{ width: `${Math.max(metrics.cache_hit_rate_pct, 5)}%` }}
                  title={`Cache Hits: ${metrics.cache_hits}`}
                />
                <div
                  className="bg-slate-300 h-full transition-all duration-500 flex-1"
                  title={`Cache Misses: ${metrics.cache_misses}`}
                />
              </div>
            </div>

            {/* LLM Models & Resilience status */}
            <div className="grid grid-cols-1 sm:grid-cols-2 gap-3 text-xs">
              <div className="rounded-xl bg-slate-50 p-3.5 border border-slate-200/80 space-y-1.5">
                <span className="font-semibold text-slate-700 block">🤖 LLM Model Usage Distribution</span>
                {Object.keys(metrics.model_usage || {}).length === 0 ? (
                  <span className="text-slate-400 italic">No LLM calls recorded yet</span>
                ) : (
                  <ul className="space-y-1 text-slate-600">
                    {Object.entries(metrics.model_usage).map(([model, count]) => (
                      <li key={model} className="flex justify-between font-mono text-[11px]">
                        <span className="truncate max-w-[160px]">{model}</span>
                        <span className="font-semibold text-indigo-600">{count} calls</span>
                      </li>
                    ))}
                  </ul>
                )}
              </div>

              <div className="rounded-xl bg-slate-50 p-3.5 border border-slate-200/80 space-y-1.5">
                <span className="font-semibold text-slate-700 block">🛡 Resilience & Fallback Metrics</span>
                <div className="space-y-1 text-slate-600">
                  <div className="flex justify-between">
                    <span>Fallback Component Triggers:</span>
                    <span className="font-semibold text-amber-600">{metrics.fallback_activations}</span>
                  </div>
                  <div className="flex justify-between">
                    <span>Recorded Errors:</span>
                    <span className="font-semibold text-red-600">{metrics.error_count}</span>
                  </div>
                  <div className="flex justify-between">
                    <span>Latency Range:</span>
                    <span className="font-mono text-[11px] text-slate-700">
                      {metrics.min_latency_ms}ms – {metrics.max_latency_ms}ms
                    </span>
                  </div>
                </div>
              </div>
            </div>
          </div>
        ) : null}

        {/* Footer */}
        <div className="flex items-center justify-between border-t border-slate-100 pt-4 text-xs text-slate-500">
          <span className="flex items-center gap-1.5">
            <span className="h-2 w-2 rounded-full bg-emerald-500 animate-pulse" />
            Auto-refreshing live data every 4s
          </span>
          <button
            onClick={fetchMetrics}
            className="rounded-lg bg-slate-100 hover:bg-slate-200 px-3 py-1.5 font-semibold text-slate-700 transition-colors"
          >
            🔄 Refresh Now
          </button>
        </div>

      </div>
    </div>
  );
}
