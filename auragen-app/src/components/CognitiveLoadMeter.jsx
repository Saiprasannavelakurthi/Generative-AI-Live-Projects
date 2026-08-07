import React from "react";

export default function CognitiveLoadMeter({
  score = 0,
  highLoad,
}) {
  if (score === null || score === undefined) {
    return null;
  }

  // Backend returns score between 0 and 10
  const normalizedScore = Math.max(
    0,
    Math.min(score, 10)
  );

  const isHighLoad =
    highLoad ?? normalizedScore >= 6;

  let level;

  if (isHighLoad) {
    level = {
      label: "High Friction",
      text: "text-red-600",
      bar: "bg-red-500",
      ring: "ring-red-200",
      dot: "bg-red-500",
    };
  } else if (normalizedScore >= 3) {
    level = {
      label: "Friction Rising",
      text: "text-amber-600",
      bar: "bg-amber-500",
      ring: "ring-amber-200",
      dot: "bg-amber-500",
    };
  } else {
    level = {
      label: "Calm",
      text: "text-emerald-600",
      bar: "bg-emerald-500",
      ring: "ring-emerald-200",
      dot: "bg-emerald-500",
    };
  }

  const percentage = normalizedScore * 10;

  return (
    <div
      className={`flex items-center gap-3 rounded-xl border bg-white px-4 py-2 shadow-sm ring-1 ${level.ring}`}
    >
      <span
        className={`h-2 w-2 rounded-full ${level.dot} ${
          isHighLoad
            ? "animate-pulse"
            : ""
        }`}
      />

      <div className="flex flex-col gap-1">
        <div className="flex items-center gap-2">
          <span className="text-xs font-medium text-slate-600">
            Cognitive Load
          </span>

          <span
            className={`font-semibold ${level.text}`}
          >
            {normalizedScore.toFixed(2)}
          </span>
        </div>

        <div className="h-2 w-28 overflow-hidden rounded-full bg-slate-200">
          <div
            className={`h-full rounded-full transition-all duration-500 ${level.bar}`}
            style={{
              width: `${percentage}%`,
            }}
          />
        </div>
      </div>

      <span
        className={`text-xs font-medium ${level.text}`}
      >
        {level.label}
      </span>
    </div>
  );
}