import React, { useMemo } from "react";

import { useMouseTelemetry } from "./hooks/useMouseTelemetry";

import DynamicCodeRenderer from "./components/DynamicCodeRenderer";
import TelemetryReadout from "./components/TelemetryReadout";

const DEFAULT_CODE = `
const Component = () => {
  return (
    <div className="min-h-screen flex items-center justify-center bg-slate-100">
      <div className="rounded-xl bg-white p-10 shadow-lg text-center">
        <h1 className="text-2xl font-bold text-slate-800">
          AuraGen AI
        </h1>

        <p className="mt-3 text-sm text-slate-500">
          Waiting for an adaptive UI from the backend...
        </p>
      </div>
    </div>
  );
};
`;

export default function App() {

  const telemetry = useMouseTelemetry({
    wsUrl:
      import.meta.env.VITE_WS_URL ??
      "ws://127.0.0.1:8000/ws",

    batchIntervalMs: 3000,
  });

  const codeToRender = useMemo(() => {

    if (
      telemetry.generatedCode &&
      telemetry.generatedCode.trim().length > 0
    ) {
      return telemetry.generatedCode;
    }

    return DEFAULT_CODE;

  }, [telemetry.generatedCode]);

  return (
    <div className="min-h-screen bg-slate-100">

      <header className="sticky top-0 z-20 border-b border-slate-200 bg-white/90 backdrop-blur">

        <div className="mx-auto flex max-w-7xl items-center justify-between px-6 py-5">

          <div>

            <div className="flex items-center gap-3">

              <span className="text-3xl">
                🧠
              </span>

              <h1 className="text-2xl font-bold text-slate-800">
                Live Component Playground
              </h1>

            </div>

            <p className="mt-2 text-sm text-slate-500">
              AuraGen • Adaptive React UI Generation
            </p>

          </div>

          <TelemetryReadout
            telemetry={telemetry}
          />

        </div>

      </header>

      <main className="mx-auto max-w-7xl p-6">

        <DynamicCodeRenderer

          key={codeToRender}

          code={codeToRender}

          defaultCode={DEFAULT_CODE}

          pollIntervalMs={0}

          scope={{
            telemetry,
          }}

          className="mx-auto max-w-4xl"

        />

      </main>

    </div>
  );
}