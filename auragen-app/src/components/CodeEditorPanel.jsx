import React from "react";

/**
 * Code editor for manually editing
 * generated React components.
 */

export default function CodeEditorPanel({
  code = "",
  onChange,
  onRun,
}) {
  const lineCount =
    code.length > 0
      ? code.split("\n").length
      : 0;

  return (
    <details className="rounded-xl border border-slate-200 bg-white shadow-sm">
      <summary className="cursor-pointer select-none px-4 py-3 text-sm font-semibold text-slate-700">
        ▶ Edit Generated Component
      </summary>

      <div className="p-4">
        <div className="overflow-hidden rounded-xl border border-slate-700">
          {/* Header */}
          <div className="flex items-center justify-between bg-slate-800 px-4 py-2">
            <div className="flex items-center gap-2">
              <span className="h-3 w-3 rounded-full bg-red-500" />
              <span className="h-3 w-3 rounded-full bg-yellow-500" />
              <span className="h-3 w-3 rounded-full bg-emerald-500" />

              <span className="ml-3 text-xs text-slate-400">
                Component.jsx
              </span>
            </div>

            <span className="text-xs text-slate-500">
              {lineCount} lines
            </span>
          </div>

          {/* Editor */}
          <textarea
            value={code}
            rows={16}
            spellCheck={false}
            placeholder="Generated React component..."
            onChange={(e) =>
              onChange(e.target.value)
            }
            className="min-h-[350px] w-full resize-y bg-slate-900 p-4 font-mono text-xs leading-6 text-slate-100 outline-none"
          />
        </div>

        <div className="mt-4 flex justify-end">
          <button
            type="button"
            disabled={!code.trim()}
            onClick={onRun}
            className="rounded-lg bg-emerald-600 px-5 py-2 text-sm font-semibold text-white transition hover:bg-emerald-500 disabled:cursor-not-allowed disabled:bg-slate-400"
          >
            ▶ Run Component
          </button>
        </div>
      </div>
    </details>
  );
}