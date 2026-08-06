import React from 'react';
import { useMouseTelemetry } from './hooks/useMouseTelemetry';
import DynamicCodeRenderer from './components/DynamicCodeRenderer';
import TelemetryReadout from './components/TelemetryReadout';

const DEFAULT_CODE = `function Component() {
  return (
    <div className="p-4 text-center text-slate-600">
      <h1 className="text-xl font-semibold">Hello 👋</h1>
      <p className="mt-1 text-sm text-slate-400">
        Waiting for a generated component from the backend...
      </p>
    </div>
  );
}`;

export default function App() {
  const telemetry = useMouseTelemetry({
    wsUrl: "ws://127.0.0.1:8000/ws",
    batchIntervalMs: 3000,
  });

  const { generatedCode } = telemetry;
  const codeToRender = generatedCode && generatedCode.trim() ? generatedCode : DEFAULT_CODE;
  console.log("========== APP ==========");
  console.log(generatedCode);
  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 via-indigo-50/40 to-slate-100 p-6">
      <header className="mx-auto mb-8 flex max-w-5xl flex-wrap items-center justify-between gap-4">
        <div className="flex items-center gap-3">
          <div className="flex h-10 w-10 items-center justify-center rounded-xl bg-gradient-to-br from-indigo-500 to-purple-600 text-lg shadow-md">
            🧠
          </div>
          <div>
            <h1 className="text-lg font-bold text-slate-800">
              Live Component Playground
            </h1>
            <p className="text-xs text-slate-400">AuraGen · Self-Healing Generative UI</p>
          </div>
        </div>

        <TelemetryReadout telemetry={telemetry} />
      </header>

      <DynamicCodeRenderer
        code={codeToRender}
        defaultCode={DEFAULT_CODE}
        pollIntervalMs={0}
        scope={{ telemetry }}
        className="mx-auto max-w-3xl"
      />
    </div>
  );
}