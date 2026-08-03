import React from 'react';
import CognitiveLoadMeter from './CognitiveLoadMeter';

export default function TelemetryReadout({ telemetry }) {
  return (
    <div className="flex flex-wrap items-center gap-3">
      <div className="flex items-center gap-4 rounded-full border border-slate-200 bg-white px-4 py-2 text-xs text-slate-600">
        <span>ws: {telemetry.connectionStatus}</span>
        <span>velocity: {telemetry.velocity.toFixed(2)} px/ms</span>
        <span>hesitation: {telemetry.isHesitating ? 'hesitating' : 'moving'}</span>
        <span>clicks: {telemetry.clickCount}</span>
      </div>
      <CognitiveLoadMeter score={telemetry.cognitiveScore} />
    </div>
  );
}