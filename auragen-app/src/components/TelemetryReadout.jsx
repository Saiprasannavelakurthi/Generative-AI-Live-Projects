import React from 'react';
import CognitiveLoadMeter from './CognitiveLoadMeter';

const wsColor = {
  open: 'bg-emerald-500',
  connecting: 'bg-amber-500',
  closed: 'bg-red-500',
  error: 'bg-red-500',
  idle: 'bg-slate-400',
};

export default function TelemetryReadout({ telemetry }) {
  const dot = wsColor[telemetry.connectionStatus] || 'bg-slate-400';

  return (
    <div className="flex flex-wrap items-center gap-3">
      <div className="flex items-center gap-4 rounded-2xl border border-white/60 bg-white/80 px-4 py-2 text-xs font-medium text-slate-600 shadow-sm backdrop-blur">
        <span className="flex items-center gap-1.5">
          <span className={`h-1.5 w-1.5 rounded-full ${dot}`} />
          {telemetry.connectionStatus}
        </span>
        <span className="h-3 w-px bg-slate-200" />
        <span>⚡ {telemetry.velocity.toFixed(2)} px/ms</span>
        <span className="h-3 w-px bg-slate-200" />
        <span>{telemetry.isHesitating ? '⏸ hesitating' : '➤ moving'}</span>
        <span className="h-3 w-px bg-slate-200" />
        <span>🖱 {telemetry.clickCount} clicks</span>
      </div>
      <CognitiveLoadMeter score={telemetry.cognitiveScore} highLoad={telemetry.highLoad} />
    </div>
  );
}