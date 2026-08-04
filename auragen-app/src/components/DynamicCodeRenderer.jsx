import TransitionShell from './TransitionShell';
import React, {
  useEffect,
  useMemo,
  useRef,
  useState,
  useCallback,
  useContext,
  useReducer,
  useLayoutEffect,
} from "react";

import { loadBabel, compileComponent } from "../utils/babelLoader";
import RenderBoundary from "./RenderBoundary";
import StatusBadge from "./StatusBadge";
import ErrorPanel from "./ErrorPanel";
import CodeEditorPanel from "./CodeEditorPanel";
import StaticFallbackForm from "./StaticFallbackForm";

const SHELL_STATUS = {
  idle: "idle",
  loading: "downloading",
  compiling: "compiling",
  ready: "live",
  error: "error",
};

export default function DynamicCodeRenderer({
  sourceUrl = null,
  code: initialCode = "",
  defaultCode = null,
  pollIntervalMs = 0,
  scope = {},
  className = "",
}) {
  const [status, setStatus] = useState("idle");
  const [errorMessage, setErrorMessage] = useState(null);

  const [rawCode, setRawCode] = useState(initialCode);
  const [editableCode, setEditableCode] = useState(initialCode);

  const [CompiledComponent, setCompiledComponent] = useState(null);
  const [renderKey, setRenderKey] = useState(0);

  const lastGoodRef = useRef(null);
  const [degraded, setDegraded] = useState(false);

  const pollRef = useRef(null);

  useEffect(() => {
    setRawCode(initialCode);
    setEditableCode(initialCode);
  }, [initialCode]);

  const memoScope = useMemo(
    () => ({
      React, useState, useEffect, useMemo, useRef,
      useCallback, useContext, useReducer, useLayoutEffect,
      ...scope,
    }),
    [scope]
  );

  const downloadCode = async () => {
    if (!sourceUrl) return rawCode;
    const res = await fetch(sourceUrl, { cache: "no-store" });
    if (!res.ok) {
      throw new Error(`Failed to download source: ${res.status} ${res.statusText}`);
    }
    return await res.text();
  };

  const revertToLastGood = useCallback(() => {
    if (!lastGoodRef.current) return;
    setCompiledComponent(() => lastGoodRef.current.component);
    setStatus("ready");
    setErrorMessage(null);
    setDegraded(true);
    setRenderKey((k) => k + 1);
  }, []);

  const build = async (codeOverride) => {
    const pendingSource = codeOverride ?? (sourceUrl ? undefined : rawCode);

    if (!sourceUrl && (!pendingSource || !pendingSource.trim())) {
      setStatus("idle");
      setErrorMessage(null);
      setCompiledComponent(null);
      return;
    }

    setStatus("loading");
    setErrorMessage(null);

    try {
      const source = codeOverride ?? (sourceUrl ? await downloadCode() : rawCode);
      setRawCode(source);
      setEditableCode(source);
      setStatus("compiling");

      const Babel = await loadBabel();
      const Compiled = compileComponent(source, Babel, memoScope);

      setCompiledComponent(() => Compiled);
      setRenderKey((k) => k + 1);
      setStatus("ready");
      setDegraded(false);

      lastGoodRef.current = { component: Compiled, code: source };
    } catch (err) {
      console.error(err);
      setErrorMessage(err.message || String(err));

      if (lastGoodRef.current) {
        setCompiledComponent(() => lastGoodRef.current.component);
        setStatus("ready");
        setDegraded(true);
      } else {
        setStatus("error");
      }
    }
  };

  const resetToDefault = useCallback(() => {
    if (defaultCode === null) return;
    lastGoodRef.current = null;
    setDegraded(false);
    setErrorMessage(null);
    build(defaultCode);
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [defaultCode]);

  useEffect(() => {
    build(initialCode);
    if (pollIntervalMs > 0 && sourceUrl) {
      pollRef.current = setInterval(() => build(), pollIntervalMs);
    }
    return () => clearInterval(pollRef.current);
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [sourceUrl, initialCode]);

  const isReady = status === "ready" && CompiledComponent;

  return (
    <div className={`flex flex-col gap-4 ${className}`}>
      {/* Toolbar */}
      <div className="flex items-center justify-between rounded-2xl border border-white/60 bg-white/80 px-4 py-3 shadow-sm backdrop-blur">
        <div className="flex items-center gap-2">
          <StatusBadge status={status} />
          {degraded && isReady && (
            <span className="rounded-full bg-amber-100 px-2.5 py-1 text-[11px] font-medium text-amber-700 ring-1 ring-inset ring-amber-200">
              showing last stable version
            </span>
          )}
        </div>

        <div className="flex items-center gap-2">
          {defaultCode !== null && (
            <button
              type="button"
              onClick={resetToDefault}
              className="rounded-lg border border-slate-200 bg-white px-3.5 py-1.5 text-xs font-semibold text-slate-600 shadow-sm transition hover:border-slate-300 hover:bg-slate-50 active:scale-95"
            >
              ↺ Reset to Default
            </button>
          )}
          <button
            type="button"
            onClick={() => build(editableCode)}
            className="rounded-lg bg-gradient-to-r from-indigo-600 to-purple-600 px-3.5 py-1.5 text-xs font-semibold text-white shadow-sm shadow-indigo-200 transition hover:from-indigo-500 hover:to-purple-500 active:scale-95"
          >
            ⟳ Reload Source
          </button>
        </div>
      </div>

      {errorMessage && (
        <ErrorPanel
          title={degraded ? "Latest generation failed — reverted" : "Compilation failed"}
          message={errorMessage}
        />
      )}

      {/* Render surface */}
      <div className="rounded-2xl border border-white/60 bg-white/90 p-5 shadow-md backdrop-blur">
        <TransitionShell
          status={SHELL_STATUS[isReady ? "ready" : status] ?? "idle"}
          staticUI={
            status === "error" && !lastGoodRef.current ? (
              <StaticFallbackForm onRetry={() => build(editableCode)} />
            ) : (
              <div className="py-10 text-center text-sm text-slate-400">
                {status === "loading" && "⬇ Downloading source..."}
                {status === "compiling" && "⚙ Compiling component..."}
                {status === "idle" && "💤 Waiting for source..."}
              </div>
            )
          }
          errorPanel={<StaticFallbackForm onRetry={() => build(editableCode)} />}
          generatedComponent={isReady ? CompiledComponent : null}
          scope={{}}
        >
          {isReady && (
            <RenderBoundary
              key={renderKey}
              onError={(e) => setErrorMessage(e.message)}
              onRetry={revertToLastGood}
            >
              <CompiledComponent />
            </RenderBoundary>
          )}
        </TransitionShell>
      </div>

      <CodeEditorPanel
        code={editableCode}
        onChange={setEditableCode}
        onRun={() => build(editableCode)}
      />
    </div>
  );
}