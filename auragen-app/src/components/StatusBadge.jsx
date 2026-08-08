
const STATUS_CONFIG = {
  idle: {
    label: "Idle",
    color:
      "bg-slate-100 text-slate-600 ring-slate-200",
    icon: "⏸",
  },

  loading: {
    label: "Downloading",
    color:
      "bg-amber-100 text-amber-700 ring-amber-200",
    icon: "⬇",
  },

  compiling: {
    label: "Compiling",
    color:
      "bg-blue-100 text-blue-700 ring-blue-200",
    icon: "⚙",
  },

  ready: {
    label: "Live",
    color:
      "bg-emerald-100 text-emerald-700 ring-emerald-200",
    icon: "✓",
  },

  error: {
    label: "Error",
    color:
      "bg-red-100 text-red-700 ring-red-200",
    icon: "⚠",
  },
};

export default function StatusBadge({
  status = "idle",
}) {
  const config =
    STATUS_CONFIG[status] ??
    STATUS_CONFIG.idle;

  const isAnimated =
    status === "loading" ||
    status === "compiling";

  return (
    <span
      className={`inline-flex items-center gap-2 rounded-full px-3 py-1 text-xs font-semibold ring-1 ring-inset ${config.color}`}
    >
      <span>{config.icon}</span>

      <span
        className={`h-2 w-2 rounded-full bg-current ${
          isAnimated
            ? "animate-pulse"
            : ""
        }`}
      />

      <span>{config.label}</span>
    </span>
  );
}