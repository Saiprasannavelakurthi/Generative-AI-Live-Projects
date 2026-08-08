import { useState, useMemo } from "react";

import { useMouseTelemetry } from "./hooks/useMouseTelemetry";
import { useKeyboardTelemetry } from "./hooks/useKeyboardTelemetry";

import DynamicCodeRenderer from "./components/DynamicCodeRenderer";
import TelemetryReadout from "./components/TelemetryReadout";
import AnalyticsModal from "./components/AnalyticsModal";

const DEFAULT_CODE = `
const Component = () => {
  return (
    <div className="min-h-screen flex items-center justify-center bg-slate-100 p-6">
      <div className="rounded-xl bg-white p-10 shadow-lg text-center max-w-md w-full">
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

const PAGE_OPTIONS = [
  { id: "login", label: "Login Page" },
  { id: "dashboard", label: "Dashboard" },
  { id: "loan", label: "Loan Application" },
  { id: "register", label: "Registration" },
  { id: "profile", label: "User Profile" },
  { id: "contact", label: "Contact Form" },
];

export default function App() {

  const [selectedPage, setSelectedPage] = useState("login");
  const [activeField, setActiveField] = useState("");
  const [isAnalyticsOpen, setIsAnalyticsOpen] = useState(false);

  const telemetry = useMouseTelemetry({
    wsUrl:
      import.meta.env.VITE_WS_URL ??
      "ws://127.0.0.1:8000/ws",

    batchIntervalMs: 1000,
    pageName: selectedPage,
    activeField: activeField,
  });

  // Track typing pauses and backspaces telemetry
  useKeyboardTelemetry({ enqueue: telemetry.enqueue });

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

      {/* Analytics Modal */}
      <AnalyticsModal
        isOpen={isAnalyticsOpen}
        onClose={() => setIsAnalyticsOpen(false)}
      />

      {/* Header */}
      <header className="sticky top-0 z-20 border-b border-slate-200 bg-white/90 backdrop-blur">

        <div className="mx-auto flex max-w-7xl flex-wrap items-center justify-between gap-4 px-6 py-4">

          <div className="flex items-center gap-3">

            <span className="text-3xl">
              🧠
            </span>

            <div>

              <h1 className="text-xl font-bold text-slate-800">
                AuraGen AI Playground
              </h1>

              <p className="text-xs text-slate-500">
                Adaptive Generative UI Engine
              </p>

            </div>

          </div>

          <div className="flex items-center gap-3">
            <button
              onClick={() => setIsAnalyticsOpen(true)}
              className="flex items-center gap-2 rounded-xl bg-slate-900 hover:bg-slate-800 text-white px-3.5 py-2 text-xs font-semibold shadow-sm transition-all active:scale-95 cursor-pointer"
            >
              <span>📊 Live Analytics</span>
            </button>

            <TelemetryReadout
              telemetry={telemetry}
            />
          </div>

        </div>

      </header>

      <main className="mx-auto max-w-7xl p-6 space-y-6">

        {/* LLM Rate Limit Fallback Banner */}
        {telemetry.isFallback && (
          <div className="flex items-center justify-between rounded-2xl border border-amber-300 bg-amber-50 p-4 text-amber-900 shadow-sm transition-all">
            <div className="flex items-center gap-3">
              <span className="flex h-9 w-9 items-center justify-center rounded-xl bg-amber-200 text-lg font-bold text-amber-800">
                ⚠️
              </span>
              <div>
                <h4 className="text-xs font-bold text-amber-900 uppercase tracking-wide">
                  LLM Rate Limit Reached (Groq 429)
                </h4>
                <p className="text-xs text-amber-700">
                  External AI models reached token quotas. AuraGen deployed the <strong>Smart Fallback Component</strong> for "{selectedPage}".
                </p>
              </div>
            </div>
            <span className="rounded-full bg-amber-200/80 border border-amber-300 px-3 py-1 text-xs font-semibold text-amber-800 whitespace-nowrap">
              Resilient Fallback Active
            </span>
          </div>
        )}

        {/* Page & Cognitive State Control Panel */}
        <div className="rounded-2xl border border-slate-200 bg-white p-5 shadow-sm space-y-4">

          <div className="flex flex-wrap items-center justify-between gap-4 border-b border-slate-100 pb-4">

            <div className="flex items-center gap-3">

              <span className="text-sm font-semibold text-slate-700">
                📄 Select Target Page:
              </span>

              <select
                value={selectedPage}
                onChange={(e) => {
                  const val = e.target.value;
                  setSelectedPage(val);
                  setTimeout(() => telemetry.flushNow({ forceGenerate: true }), 50);
                }}
                className="rounded-lg border border-slate-300 bg-slate-50 px-3 py-2 text-sm font-medium text-slate-800 shadow-sm focus:border-indigo-500 focus:bg-white focus:outline-none"
              >
                {PAGE_OPTIONS.map((opt) => (
                  <option key={opt.id} value={opt.id}>
                    {opt.label}
                  </option>
                ))}
              </select>

              {selectedPage === "loan" && (
                <select
                  value={activeField}
                  onChange={(e) => {
                    const val = e.target.value;
                    setActiveField(val);
                    setTimeout(() => telemetry.flushNow({ forceGenerate: true }), 50);
                  }}
                  className="rounded-lg border border-slate-300 bg-amber-50 px-3 py-2 text-sm font-medium text-amber-900 shadow-sm focus:border-amber-500 focus:outline-none"
                >
                  <option value="">No Active Field Focus</option>
                  <option value="salary">Focus: Salary Field (Triggers Helper Tip)</option>
                  <option value="income">Focus: Income Field (Triggers Helper Tip)</option>
                </select>
              )}

            </div>

            <div className="flex items-center gap-2">

              <button
                type="button"
                onClick={() => telemetry.flushNow()}
                className="rounded-lg bg-indigo-600 px-4 py-2 text-xs font-semibold text-white shadow transition hover:bg-indigo-500"
              >
                ⚡ Generate Now for "{selectedPage}"
              </button>

            </div>

          </div>

          {/* Cognitive Adaptation Rule Info */}
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4 text-xs text-slate-600 bg-slate-50 p-4 rounded-xl border border-slate-200">

            <div className="flex items-start gap-2">

              <span className="text-emerald-600 font-bold text-base">🟢</span>

              <div>

                <span className="font-semibold text-slate-800 block">
                  Calm Mode (Cognitive Load 0 – 3):
                </span>

                <span>
                  Generates standard or rich UI components with complete features, charts, and navigation options.
                </span>

              </div>

            </div>

            <div className="flex items-start gap-2">

              <span className="text-red-600 font-bold text-base">🔴</span>

              <div>

                <span className="font-semibold text-slate-800 block">
                  Hesitation / High Friction Mode (Cognitive Load &gt; 6):
                </span>

                <span>
                  Generates <strong>minimal distraction-free UI</strong> with larger buttons, simplified fields, and targeted tooltips to help struggling users.
                </span>

              </div>

            </div>

          </div>

        </div>

        {/* Dynamic Renderer */}
        <DynamicCodeRenderer

          code={codeToRender}

          defaultCode={DEFAULT_CODE}

          pollIntervalMs={0}

          scope={{
            telemetry,
            formData: telemetry?.formData || {},
          }}

          className="mx-auto max-w-4xl"

        />

      </main>

    </div>
  );
}