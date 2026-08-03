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

// Maps this component's internal status names to TransitionShell's vocabulary.
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

  // Tracks the last component that compiled AND rendered without crashing,
  // so a bad generation can fall back to it instead of going blank.
  const lastGoodRef = useRef(null);
  const [degraded, setDegraded] = useState(false);

  const pollRef = useRef(null);

  useEffect(() => {
    setRawCode(initialCode);
    setEditableCode(initialCode);
  }, [initialCode]);

  const memoScope = useMemo(
    () => ({
      React,
      useState,
      useEffect,
      useMemo,
      useRef,
      useCallback,
      useContext,
      useReducer,
      useLayoutEffect,
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
    setDegraded(true); // still flag it, since it's not the newest version
    setRenderKey((k) => k + 1);
  }, []);

  const build = async (codeOverride) => {
    const pendingSource = codeOverride ?? (sourceUrl ? undefined : rawCode);

    if (!sourceUrl && (!pendingSource || !pendingSource.trim())) {
      setStatus("idle");
      setErrorMessage(null);
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

      // Only remembered as "last good" once it renders without throwing —
      // RenderBoundary's onError below will revert if it crashes at runtime.
      lastGoodRef.current = { component: Compiled, code: source };
    } catch (err) {
      console.error(err);
      setErrorMessage(err.message || String(err));

      if (lastGoodRef.current) {
        // Graceful degradation: keep showing the last working component
        // instead of going blank on a bad generation.
        setCompiledComponent(() => lastGoodRef.current.component);
        setStatus("ready");
        setDegraded(true);
      } else {
        setStatus("error");
      }
    }
  };

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
    <div className={`flex flex-col gap-3 ${className}`}>
      <div className="flex items-center justify-between rounded-lg border border-slate-200 bg-slate-50 px-3 py-2">
        <div className="flex items-center gap-2">
          <StatusBadge status={status} />
          {degraded && isReady && (
            <span className="rounded-full bg-amber-100 px-2 py-0.5 text-[11px] font-medium text-amber-700">
              showing last stable version
            </span>
          )}
        </div>
        <button
          type="button"
          onClick={() => build(editableCode)}
          className="rounded-md bg-slate-900 px-3 py-1.5 text-xs font-medium text-white transition hover:bg-slate-700"
        >
          Reload Source
        </button>
      </div>

      {errorMessage && (
        <ErrorPanel
          title={degraded ? "Latest generation failed — reverted" : "Compilation failed"}
          message={errorMessage}
        />
      )}

      <div className="rounded-lg border border-slate-200 p-4">
        <TransitionShell
          status={SHELL_STATUS[isReady ? "ready" : status] ?? "idle"}
          staticUI={
            status === "error" && !lastGoodRef.current ? (
              <StaticFallbackForm onRetry={() => build(editableCode)} />
            ) : (
              <div className="py-6 text-center text-sm text-slate-400">
                {status === "loading" && "Downloading source..."}
                {status === "compiling" && "Compiling component..."}
                {status === "idle" && "Waiting for source..."}
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