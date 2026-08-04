import React from 'react';

export default function CognitiveLoadMeter({ score, highLoad }) {
  if (score === null || score === undefined) return null;

  const level = highLoad
    ? { label: 'High friction', text: 'text-red-600', bar: 'from-red-500 to-rose-500', ring: 'ring-red-200', dot: 'bg-red-500' }
    : score > 0.3
    ? { label: 'Friction rising', text: 'text-amber-600', bar: 'from-amber-400 to-orange-500', ring: 'ring-amber-200', dot: 'bg-amber-500' }
    : { label: 'Calm', text: 'text-emerald-600', bar: 'from-emerald-400 to-teal-500', ring: 'ring-emerald-200', dot: 'bg-emerald-500' };

  // Display-only scaling so the bar has *some* visual movement — not a real percentage.
  const pct = Math.min(score / 1.5, 1);

  return (
    <div className={`flex items-center gap-3 rounded-2xl border border-white/60 bg-white/80 px-4 py-2 shadow-sm ring-1 ${level.ring} backdrop-blur`}>
      <span className={`h-2 w-2 rounded-full ${level.dot} ${highLoad ? 'animate-pulse' : ''}`} />

      <div className="flex flex-col gap-1">
        <div className="flex items-center gap-2">
          <span className="text-[11px] font-semibold uppercase tracking-wide text-slate-500">
            Cognitive Load
          </span>
          <span className={`text-sm font-bold tabular-nums ${level.text}`}>
            {score.toFixed(2)}
          </span>
        </div>

        <div className="h-2 w-32 overflow-hidden rounded-full bg-slate-100">
          <div
            className={`h-full rounded-full bg-gradient-to-r ${level.bar} transition-all duration-500 ease-out`}
            style={{ width: `${pct * 100}%` }}
          />
        </div>
      </div>

      <span className={`whitespace-nowrap text-xs font-medium ${level.text}`}>
        {level.label}
      </span>
    </div>
  );
}