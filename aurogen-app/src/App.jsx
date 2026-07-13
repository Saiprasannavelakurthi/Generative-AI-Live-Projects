
import React from 'react';
import { useMouseTelemetry } from './hooks/useMouseTelemetry';
import DynamicCodeRenderer from './components/DynamicCodeRenderer';
import TelemetryReadout from './components/TelemetryReadout';

export default function App() {
  const telemetry = useMouseTelemetry({
    wsUrl:  "wss://echo.websocket.org/",
    batchIntervalMs: 500,
  });

  return (
    <div className="min-h-screen bg-slate-100 p-6">
      <header className="mb-6 flex items-center justify-between">
        <h1 className="text-lg font-semibold text-slate-800">Live Component Playground</h1>
        <TelemetryReadout telemetry={telemetry} />
      </header>

      <DynamicCodeRenderer
        sourceUrl="https://your-code-host.example.com/latest-component.jsx"
        pollIntervalMs={5000}
        scope={{ telemetry }}
        className="mx-auto max-w-3xl"
      />
    </div>
  );
}
