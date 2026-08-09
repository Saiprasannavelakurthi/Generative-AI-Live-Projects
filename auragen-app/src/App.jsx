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

const PAGE_TEMPLATES = {
  login: `const Component = () => {
  return (
    <div className="max-w-md mx-auto p-8 bg-white border border-slate-200 rounded-2xl shadow-xl">
      <h2 className="text-2xl font-bold text-indigo-700 mb-2">Welcome Back</h2>
      <p className="text-xs text-slate-500 mb-6">Enter your credentials to access your account</p>
      <div className="space-y-4">
        <div>
          <label className="block text-xs font-semibold text-slate-700 mb-1">Email Address</label>
          <input type="email" placeholder="user@example.com" className="w-full px-4 py-2.5 bg-slate-50 border border-slate-300 rounded-xl text-slate-900 text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500" />
        </div>
        <div>
          <label className="block text-xs font-semibold text-slate-700 mb-1">Password</label>
          <input type="password" placeholder="••••••••" className="w-full px-4 py-2.5 bg-slate-50 border border-slate-300 rounded-xl text-slate-900 text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500" />
        </div>
        <button className="w-full py-3 bg-indigo-600 hover:bg-indigo-700 text-white font-semibold text-sm rounded-xl shadow-md transition-all">Sign In to Dashboard</button>
      </div>
    </div>
  );
};`,

  dashboard: `const Component = () => {
  return (
    <div className="p-6 bg-white rounded-2xl border border-slate-200 shadow-xl max-w-4xl mx-auto text-slate-800">
      <div className="flex items-center justify-between mb-6">
        <div>
          <h2 className="text-xl font-bold text-slate-900">AuraGen Dashboard Summary</h2>
          <p className="text-xs text-slate-500">Real-time Telemetry & System Overview</p>
        </div>
        <span className="px-3 py-1 bg-emerald-50 text-emerald-700 border border-emerald-200 rounded-full text-xs font-semibold">
          Live System Active
        </span>
      </div>
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-6">
        <div className="p-4 bg-indigo-50 rounded-xl border border-indigo-100">
          <p className="text-xs font-medium text-indigo-700">Total Balance</p>
          <h3 className="text-2xl font-bold text-indigo-900 mt-1">$24,500</h3>
        </div>
        <div className="p-4 bg-slate-50 rounded-xl border border-slate-200">
          <p className="text-xs font-medium text-slate-500">Active Services</p>
          <h3 className="text-2xl font-bold text-slate-800 mt-1">4 Active</h3>
        </div>
        <div className="p-4 bg-slate-50 rounded-xl border border-slate-200">
          <p className="text-xs font-medium text-slate-500">System Performance</p>
          <h3 className="text-2xl font-bold text-emerald-600 mt-1">Optimal</h3>
        </div>
      </div>
    </div>
  );
};`,

  loan: `const Component = () => {
  const [amount, setAmount] = React.useState(10000);
  const [salary, setSalary] = React.useState(5000);
  return (
    <div className="p-6 bg-white rounded-2xl border border-slate-200 shadow-xl max-w-xl mx-auto text-slate-800">
      <h2 className="text-2xl font-bold text-indigo-600 mb-1">Instant Loan Application</h2>
      <p className="text-xs text-slate-500 mb-6">Calculate estimated monthly EMI</p>
      <div className="space-y-4">
        <div>
          <label className="block text-xs font-semibold text-slate-700 mb-1">Monthly Income ($)</label>
          <input type="number" value={salary} onChange={(e) => setSalary(Number(e.target.value))} className="w-full px-4 py-2.5 bg-slate-50 border border-slate-300 rounded-xl text-slate-900 text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500" />
        </div>
        <div>
          <div className="flex justify-between text-xs font-semibold text-slate-700 mb-1">
            <span>Requested Loan Amount</span>
            <span className="text-indigo-600">\${amount.toLocaleString()}</span>
          </div>
          <input type="range" min="1000" max="50000" step="1000" value={amount} onChange={(e) => setAmount(Number(e.target.value))} className="w-full accent-indigo-600" />
        </div>
        <div className="p-4 bg-indigo-50 rounded-xl border border-indigo-100 flex items-center justify-between">
          <span className="text-xs font-medium text-indigo-900">Estimated Monthly EMI</span>
          <span className="text-lg font-bold text-indigo-600">\${Math.round(amount / 24)}/mo</span>
        </div>
        <button className="w-full py-3 bg-indigo-600 hover:bg-indigo-700 text-white font-semibold text-sm rounded-xl shadow-md transition-all">Submit Application Now →</button>
      </div>
    </div>
  );
};`,

  register: `const Component = () => {
  return (
    <div className="p-6 bg-white rounded-2xl border border-slate-200 shadow-xl max-w-md mx-auto text-slate-800">
      <h2 className="text-2xl font-bold text-slate-900 mb-1">Create Account</h2>
      <p className="text-xs text-slate-500 mb-6">Sign up to get started with AuraGen</p>
      <div className="space-y-4">
        <div>
          <label className="block text-xs font-semibold text-slate-700 mb-1">Full Name</label>
          <input type="text" placeholder="John Doe" className="w-full px-4 py-2.5 bg-slate-50 border border-slate-300 rounded-xl text-slate-900 text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500" />
        </div>
        <div>
          <label className="block text-xs font-semibold text-slate-700 mb-1">Email Address</label>
          <input type="email" placeholder="name@example.com" className="w-full px-4 py-2.5 bg-slate-50 border border-slate-300 rounded-xl text-slate-900 text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500" />
        </div>
        <button className="w-full py-3 bg-indigo-600 hover:bg-indigo-700 text-white font-semibold text-sm rounded-xl shadow-md transition-all">Register Account</button>
      </div>
    </div>
  );
};`,

  profile: `const Component = () => {
  return (
    <div className="p-6 bg-white rounded-2xl border border-slate-200 shadow-xl max-w-lg mx-auto text-slate-800">
      <div className="flex items-center space-x-4 mb-6">
        <div className="w-14 h-14 rounded-full bg-indigo-600 text-white flex items-center justify-center text-xl font-bold">JD</div>
        <div>
          <h2 className="text-xl font-bold text-slate-900">User Profile</h2>
          <p className="text-xs text-slate-500">Account Settings and Preferences</p>
        </div>
      </div>
      <div className="space-y-4">
        <div>
          <label className="block text-xs font-semibold text-slate-700 mb-1">Full Name</label>
          <input type="text" defaultValue="John Doe" className="w-full px-4 py-2.5 bg-slate-50 border border-slate-300 rounded-xl text-slate-900 text-sm" />
        </div>
        <div>
          <label className="block text-xs font-semibold text-slate-700 mb-1">Email Address</label>
          <input type="email" defaultValue="john@example.com" className="w-full px-4 py-2.5 bg-slate-50 border border-slate-300 rounded-xl text-slate-900 text-sm" />
        </div>
        <button className="w-full py-3 bg-indigo-600 hover:bg-indigo-700 text-white font-semibold text-sm rounded-xl shadow-md transition-all">Save Changes</button>
      </div>
    </div>
  );
};`,

  contact: `const Component = () => {
  return (
    <div className="p-6 bg-white rounded-2xl border border-slate-200 shadow-xl max-w-md mx-auto text-slate-800">
      <h2 className="text-2xl font-bold text-slate-900 mb-1">Contact Support</h2>
      <p className="text-xs text-slate-500 mb-6">Send us a message and we will reply shortly</p>
      <div className="space-y-4">
        <div>
          <label className="block text-xs font-semibold text-slate-700 mb-1">Your Message</label>
          <textarea rows="4" placeholder="How can we help you?" className="w-full px-4 py-2.5 bg-slate-50 border border-slate-300 rounded-xl text-slate-900 text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500"></textarea>
        </div>
        <button className="w-full py-3 bg-indigo-600 hover:bg-indigo-700 text-white font-semibold text-sm rounded-xl shadow-md transition-all">Send Message</button>
      </div>
    </div>
  );
};`,
};

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

    return PAGE_TEMPLATES[selectedPage] || DEFAULT_CODE;

  }, [telemetry.generatedCode, selectedPage]);

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
                  telemetry.clearGeneratedCode();
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

            {/* Generated UI Type Status */}
            <div className="flex items-center gap-2">

              {telemetry.isGenerating ? (
                <span className="inline-flex items-center gap-2 rounded-full border border-indigo-200 bg-indigo-50 px-3 py-1.5 text-xs font-semibold text-indigo-700">
                  <span className="inline-block h-2 w-2 animate-pulse rounded-full bg-indigo-500"></span>
                  Generating UI…
                </span>
              ) : telemetry.isFallback ? (
                <span className="inline-flex items-center gap-2 rounded-full border border-amber-300 bg-amber-50 px-3 py-1.5 text-xs font-semibold text-amber-800">
                  <span className="inline-block h-2 w-2 rounded-full bg-amber-500"></span>
                  ⚠️ Groq Quota — Fallback Active
                </span>
              ) : telemetry.decision ? (
                <span className="inline-flex items-center gap-2 rounded-full border border-emerald-200 bg-emerald-50 px-3 py-1.5 text-xs font-semibold text-emerald-700">
                  <span className="inline-block h-2 w-2 rounded-full bg-emerald-500"></span>
                  {telemetry.decision
                    .split('_')
                    .map(w => w.charAt(0).toUpperCase() + w.slice(1))
                    .join(' ')}
                </span>
              ) : null}

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

          decision={telemetry.decision}

          isFallback={telemetry.isFallback}

          generationTime={telemetry.generationTime}

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