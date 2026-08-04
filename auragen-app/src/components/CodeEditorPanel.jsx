import React from 'react';

export default function CodeEditorPanel({ code, onChange, onRun }) {
  return (
    <details className="group rounded-2xl border border-white/60 bg-white/90 p-4 text-sm shadow-sm backdrop-blur" open>
      <summary className="flex cursor-pointer select-none items-center gap-2 font-semibold text-slate-700">
        <span className="transition-transform group-open:rotate-90">▶</span>
        Edit source manually
      </summary>

      <div className="mt-3 overflow-hidden rounded-xl border border-slate-800 shadow-inner">
        <div className="flex items-center gap-1.5 bg-slate-800 px-3 py-2">
          <span className="h-2.5 w-2.5 rounded-full bg-red-500" />
          <span className="h-2.5 w-2.5 rounded-full bg-amber-500" />
          <span className="h-2.5 w-2.5 rounded-full bg-emerald-500" />
          <span className="ml-2 text-[11px] font-medium text-slate-400">component.jsx</span>
        </div>
        <textarea
          value={code}
          onChange={(e) => onChange(e.target.value)}
          rows={14}
          spellCheck={false}
          className="w-full resize-y bg-slate-900 p-4 font-mono text-xs leading-relaxed text-slate-100 outline-none"
        />
      </div>

      <button
        type="button"
        onClick={onRun}
        className="mt-3 rounded-lg bg-gradient-to-r from-emerald-600 to-teal-600 px-4 py-2 text-xs font-semibold text-white shadow-sm shadow-emerald-200 transition hover:from-emerald-500 hover:to-teal-500 active:scale-95"
      >
        ▶ Run this code
      </button>
    </details>
  );
}