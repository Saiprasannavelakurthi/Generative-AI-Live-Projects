import React from 'react';

export default function CodeEditorPanel({ code, onChange, onRun }) {
  return (
    <details className="rounded-lg border border-slate-200 p-3 text-sm">
      <summary className="cursor-pointer select-none font-medium text-slate-700">
        Edit source manually
      </summary>
      <textarea
        value={code}
        onChange={(e) => onChange(e.target.value)}
        rows={12}
        spellCheck={false}
        className="mt-2 w-full rounded-md border border-slate-300 bg-slate-900 p-3 font-mono text-xs text-slate-100"
      />
      <button
        type="button"
        onClick={onRun}
        className="mt-2 rounded-md bg-emerald-600 px-3 py-1.5 text-xs font-medium text-white transition hover:bg-emerald-500"
      >
        Run this code
      </button>
    </details>
  );
}
