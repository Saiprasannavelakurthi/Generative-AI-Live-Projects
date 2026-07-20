import React, { useEffect, useMemo, useRef, useState, useCallback, useContext, useReducer, useLayoutEffect } from 'react';
import { loadBabel, compileComponent } from '../utils/babelLoader';
import RenderBoundary from './RenderBoundary';
import StatusBadge from './StatusBadge';
import ErrorPanel from './ErrorPanel';
import CodeEditorPanel from './CodeEditorPanel';

/**
 * DynamicCodeRenderer
 * -------------------
 * Downloads (or accepts) a raw source-code string, compiles it in the
 * browser via `utils/babelLoader`, and renders the resulting component
 * inside a `RenderBoundary`. Purely an orchestrator — the actual pieces
 * (status badge, error panel, editor, compile logic, error boundary)
 * each live in their own file.
 *
 * Contract for the source code: it must assign the root component to a
 * top-level identifier named `Component`. `React` and anything passed
 * via `scope` are available inside the compiled code without an import.
 */
export default function DynamicCodeRenderer({
  sourceUrl = null,
<<<<<<< Updated upstream
  code: initialCode = '',
=======
  code: initialCode = "",
  backendError = null,
>>>>>>> Stashed changes
  pollIntervalMs = 0,
  scope = {},
  className = '',
}) {
  const [status, setStatus] = useState('idle'); // idle | loading | compiling | ready | error
  const [errorMessage, setErrorMessage] = useState(null);
  const [rawCode, setRawCode] = useState(initialCode);
  const [editableCode, setEditableCode] = useState(initialCode);
  const [CompiledComponent, setCompiledComponent] = useState(null);
  const [renderKey, setRenderKey] = useState(0);
  const pollRef = useRef(null);

  const memoScope = useMemo(() => ({ React, useState, useEffect, useMemo, useRef, useCallback, useContext, useReducer, useLayoutEffect, ...scope }), [scope]);

  const downloadCode = async () => {
    if (!sourceUrl) return rawCode;
    const res = await fetch(sourceUrl, { cache: 'no-store' });
    if (!res.ok) throw new Error(`Failed to download source: ${res.status} ${res.statusText}`);
    return res.text();
  };

  // Surface backend generation failures (e.g. Groq rate limit) directly,
  // instead of letting an empty/missing code string fall through to Babel
  // and produce a confusing "Component was not created" error.
  useEffect(() => {
    if (backendError) {
      setStatus("error");
      setErrorMessage(`Backend generation failed: ${backendError}`);
    }
  }, [backendError]);

  const build = async (codeOverride) => {
<<<<<<< Updated upstream
    setStatus('loading');
=======
    // Nothing to compile yet (e.g. no successful generation has arrived).
    // Stay idle rather than throwing a misleading Babel error.
    const pending = codeOverride ?? (sourceUrl ? null : rawCode);
    if (!sourceUrl && !pending?.trim()) {
      setStatus("idle");
      setErrorMessage(null);
      return;
    }

    setStatus("loading");
>>>>>>> Stashed changes
    setErrorMessage(null);
    try {
      const source = codeOverride ?? (sourceUrl ? await downloadCode() : rawCode);
      setRawCode(source);
      setEditableCode(source);

      setStatus('compiling');
      const Babel = await loadBabel();
      const Compiled = compileComponent(source, Babel, memoScope);

      setCompiledComponent(() => Compiled);
      setRenderKey((k) => k + 1);
      setStatus('ready');
    } catch (err) {
      setStatus('error');
      setErrorMessage(err.message || String(err));
    }
  };

  useEffect(() => {
    build();
    if (pollIntervalMs > 0 && sourceUrl) {
      pollRef.current = setInterval(() => build(), pollIntervalMs);
    }
    return () => clearInterval(pollRef.current);
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [sourceUrl]);

  return (
    <div className={`flex flex-col gap-3 ${className}`}>
      <div className="flex items-center justify-between rounded-lg border border-slate-200 bg-slate-50 px-3 py-2">
        <StatusBadge status={status} />
        <button
          type="button"
          onClick={() => build()}
          className="rounded-md bg-slate-900 px-3 py-1.5 text-xs font-medium text-white transition hover:bg-slate-700"
        >
          Reload source
        </button>
      </div>

<<<<<<< Updated upstream
      {status === 'error' && <ErrorPanel title="Compilation failed" message={errorMessage} />}
=======
      {status === "error" && (
        <ErrorPanel
          title={backendError ? "Generation failed" : "Compilation failed"}
          message={errorMessage}
        />
      )}
>>>>>>> Stashed changes

      <div className="rounded-lg border border-slate-200 p-4">
        {status === 'ready' && CompiledComponent ? (
          <RenderBoundary key={renderKey} onError={(e) => setErrorMessage(e.message)}>
            <CompiledComponent />
          </RenderBoundary>
        ) : (
          <div className="py-6 text-center text-sm text-slate-400">
            {status === 'loading' && 'Downloading source…'}
            {status === 'compiling' && 'Compiling component…'}
            {status === 'idle' && 'Waiting for source…'}
          </div>
        )}
      </div>

      <CodeEditorPanel
        code={editableCode}
        onChange={setEditableCode}
        onRun={() => build(editableCode)}
      />
    </div>
  );
}
