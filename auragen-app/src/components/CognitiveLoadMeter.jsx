import React from 'react';

export default function CognitiveLoadMeter({ score, highLoad }) {
  if (score === null || score === undefined) return null;

  const level = highLoad
    ? { label: 'High friction', color: 'bg-red-500', track: 'bg-red-100' }
    : score > 0.3
    ? { label: 'Friction rising', color: 'bg-amber-500', track: 'bg-amber-100' }
    : { label: 'Calm', color: 'bg-emerald-500', track: 'bg-emerald-100' };

  // Display-only scaling so the bar has *some* visual movement — not a real percentage.
  const pct = Math.min(score / 1.5, 1);

  return (
    <div className="flex items-center gap-2 rounded-full border border-slate-200 bg-white px-3 py-1.5 text-xs text-slate-600">
      <span className="font-medium text-slate-700">Cognitive Load</span>
      <div className={`h-1.5 w-24 overflow-hidden rounded-full ${level.track}`}>
        <div
          className={`h-full rounded-full transition-all duration-500 ${level.color}`}
          style={{ width: `${pct * 100}%` }}
        />
      </div>
      <span className="tabular-nums">{score.toFixed(2)}</span>
      <span className="text-slate-400">· {level.label}</span>
    </div>
  );
}