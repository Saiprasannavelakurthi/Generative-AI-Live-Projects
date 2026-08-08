import CognitiveLoadMeter from "./CognitiveLoadMeter";

const STATUS_COLORS = {
  open: "bg-emerald-500",
  connecting: "bg-amber-500",
  closed: "bg-red-500",
  error: "bg-red-500",
  idle: "bg-slate-400",
};

export default function TelemetryReadout({
  telemetry,
}) {
  const {
    connectionStatus = "idle",
    velocity = 0,
    isHesitating = false,
    clickCount = 0,
    cognitiveScore = 0,
  } = telemetry ?? {};

  const statusColor =
    STATUS_COLORS[connectionStatus] ??
    STATUS_COLORS.idle;

  return (
    <div className="flex flex-wrap items-center gap-3">
      <div className="flex items-center gap-4 rounded-full border border-slate-200 bg-white px-4 py-2 text-xs text-slate-600 shadow-sm">
        <div className="flex items-center gap-2">
          <span
            className={`h-2 w-2 rounded-full ${statusColor}`}
          />

          <span className="font-medium">
            WS:
          </span>

          <span className="capitalize">
            {connectionStatus}
          </span>
        </div>

        <span>
          ⚡{" "}
          {Number(velocity).toFixed(2)}
          {" "}px/ms
        </span>

        <span>
          {isHesitating
            ? "⏸ Hesitating"
            : "➜ Moving"}
        </span>

        <span>
          🖱 {clickCount} Clicks
        </span>

        {telemetry?.isFallback && (
          <span className="rounded-full bg-amber-100 border border-amber-300 text-amber-800 px-2.5 py-0.5 text-[10px] font-bold uppercase tracking-wider">
            ⚠️ LLM Limit (Fallback Active)
          </span>
        )}
      </div>

      <CognitiveLoadMeter
        score={cognitiveScore}
      />
    </div>
  );
}