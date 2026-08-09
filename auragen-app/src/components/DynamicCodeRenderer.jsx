import React, {
  useCallback,
  useContext,
  useEffect,
  useLayoutEffect,
  useMemo,
  useReducer,
  useRef,
  useState,
} from "react";

import TransitionShell from "./TransitionShell";
import RenderBoundary from "./RenderBoundary";
import StatusBadge from "./StatusBadge";
import ErrorPanel from "./ErrorPanel";
import CodeEditorPanel from "./CodeEditorPanel";
import StaticFallbackForm from "./StaticFallbackForm";

import {
  loadBabel,
  compileComponent,
} from "../utils/babelLoader";

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
  decision = "",
  isFallback = false,
  generationTime = null,
}) {

  const [status, setStatus] = useState("idle");

  const [errorMessage, setErrorMessage] =
    useState(null);

  const [rawCode, setRawCode] =
    useState(initialCode);

  const [editableCode, setEditableCode] =
    useState(initialCode);

  const [
    CompiledComponent,
    setCompiledComponent,
  ] = useState(null);

  const [renderKey, setRenderKey] =
    useState(0);

  const [degraded, setDegraded] =
    useState(false);

  const lastGoodRef = useRef(null);

  const pollRef = useRef(null);

  // Track the last source we compiled to avoid
  // recompiling the same code on repeated renders.
  const lastCompiledSource = useRef(null);

  // Boolean state mirroring whether lastGoodRef has a value.
  // Used during render to avoid accessing refs directly.
  const [hasLastGood, setHasLastGood] = useState(false);

  // Render timing: measures ms from code-change to successful compile+render
  const [renderTimeMs, setRenderTimeMs] = useState(null);
  const codeArrivalRef = useRef(null);

  // Expose all React hooks and safe context objects that generated components
  // may use without importing (since imports are forbidden).
  const memoScope = useMemo(() => {
    const rawFormData = scope.formData || {};
    const safeFormData = new Proxy(rawFormData, {
      get: (target, prop) => {
        if (typeof prop === "symbol" || prop in Object.prototype) {
          return target[prop];
        }
        return target[prop] !== undefined ? target[prop] : "";
      },
    });

    const noop = () => {};

    return {
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
      formData: safeFormData,
      FormaData: safeFormData,
      formdata: safeFormData,
      FormData: safeFormData,
      handlePurposeChange: noop,
      handleChange: noop,
      handleSubmit: noop,
      handleClick: noop,
      handleBlur: noop,
      handleSelect: noop,
      handleToggle: noop,
    };
  }, [scope]);

  const downloadCode = useCallback(async () => {
    if (!sourceUrl) {
      return rawCode;
    }

    const controller = new AbortController();

    const timeout = setTimeout(() => {
      controller.abort();
    }, 10000);

    try {
      const response = await fetch(sourceUrl, {
        cache: "no-store",
        signal: controller.signal,
      });

      if (!response.ok) {
        throw new Error(
          `Failed to download source (${response.status})`
        );
      }

      return await response.text();
    } finally {
      clearTimeout(timeout);
    }
  }, [sourceUrl, rawCode]);

  const revertToLastGood =
    useCallback(() => {
      if (!lastGoodRef.current) return;

      setCompiledComponent(
        () => lastGoodRef.current.component
      );

      setStatus("ready");

      setErrorMessage(null);

      setDegraded(true);

      setRenderKey((v) => v + 1);
    }, []);

  const build = useCallback(
    async (codeOverride = null) => {
      try {
        let source;

        if (codeOverride !== null) {
          source = codeOverride;
        } else if (sourceUrl) {
          source = await downloadCode();
        } else {
          source = rawCode;
        }

        if (!source || !source.trim()) {
          setCompiledComponent(null);
          setStatus("idle");
          return;
        }

        // Skip recompilation if nothing changed
        if (source === lastCompiledSource.current) {
          return;
        }

        setStatus("loading");
        setErrorMessage(null);
        setRenderTimeMs(null);

        setRawCode(source);
        setEditableCode(source);

        setStatus("compiling");

        const Babel = await loadBabel();

        const Component = compileComponent(
          source,
          Babel,
          memoScope
        );

        lastCompiledSource.current = source;

        if (typeof Component !== "function") {
          throw new Error(
            "Generated code did not export a valid React component."
          );
        }

        lastGoodRef.current = {
          component: Component,
          code: source,
        };
        setHasLastGood(true);

        setCompiledComponent(() => Component);

        setRenderKey((value) => value + 1);

        setStatus("ready");

        setDegraded(false);

        // Capture render time (code arrival → compile done)
        if (codeArrivalRef.current !== null) {
          const elapsed = Math.round(performance.now() - codeArrivalRef.current);
          setRenderTimeMs(elapsed);
          codeArrivalRef.current = null;
        }

      } catch (error) {
        console.error("[AuraGen] Compilation error:", error);

        setErrorMessage(
          error?.message ||
            "Unknown compilation error."
        );

        if (lastGoodRef.current) {
          setCompiledComponent(
            () => lastGoodRef.current.component
          );

          setStatus("ready");

          setDegraded(true);
        } else {
          setCompiledComponent(null);
          setStatus("error");
        }
      }
    },
    [
      rawCode,
      sourceUrl,
      memoScope,
      downloadCode,
    ]
  );

  const resetToDefault = useCallback(() => {
    if (defaultCode === null) return;

    lastCompiledSource.current = "";

    lastGoodRef.current = null;
    setHasLastGood(false);

    setErrorMessage(null);

    setDegraded(false);

    build(defaultCode);
  }, [defaultCode, build]);

  // Main effect: build when initialCode changes.
  // NOTE: The redundant sync effect that only updated rawCode
  // and editableCode has been removed — build() already
  // calls setRawCode and setEditableCode internally, so
  // a separate effect was causing double-compilation.
  //
  useEffect(() => {
    // Stamp arrival time for render-time measurement (only ref writes — no setState here)
    if (initialCode && initialCode.trim()) {
      codeArrivalRef.current = performance.now();
    }
    // The build() function triggers async state updates as part of the
    // intentional compilation pipeline. This is not a cascading render issue —
    // it is the designed behavior for a dynamic code renderer.
    // eslint-disable-next-line react-hooks/set-state-in-effect
    build(initialCode);

    if (pollIntervalMs > 0 && sourceUrl) {
      pollRef.current = setInterval(() => {
        build();
      }, pollIntervalMs);
    }

    return () => {
      if (pollRef.current) {
        clearInterval(pollRef.current);
      }
    };

    // build intentionally omitted to prevent rebuild loops
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [
    initialCode,
    pollIntervalMs,
    sourceUrl,
  ]);

  const isReady =
    status === "ready" &&
    CompiledComponent;

  const renderStaticUI = () => {
    if (
      status === "error" &&
      !hasLastGood
    ) {
      return (
        <StaticFallbackForm
          onRetry={() =>
            build(editableCode)
          }
        />
      );
    }

    if (status === "loading") {
      return (
        <div className="py-12 text-center text-slate-500">
          ⏳ Downloading source...
        </div>
      );
    }

    if (status === "compiling") {
      return (
        <div className="py-12 text-center text-slate-500">
          ⚙️ Compiling React component...
        </div>
      );
    }

    return (
      <div className="py-12 text-center text-slate-400">
        🧠 Waiting for generated UI...
      </div>
    );
  };

  return (
    <div className={`flex flex-col gap-4 ${className}`}>
      {/* ============================
          Toolbar
      ============================ */}

      <div className="flex flex-wrap items-center justify-between gap-3 rounded-xl border border-slate-200 bg-white p-4 shadow-sm">
        {/* Left: Status + degraded badge */}
        <div className="flex items-center gap-3">
          <StatusBadge
            status={
              status === "ready"
                ? "ready"
                : status
            }
          />

          {degraded && isReady && (
            <span className="rounded-full bg-amber-100 px-3 py-1 text-xs font-semibold text-amber-700">
              Showing last stable version
            </span>
          )}
        </div>

        {/* Center: UI Type + timing badges */}
        <div className="flex-1 flex flex-wrap items-center justify-center gap-2">
          {(status === "compiling" || status === "loading") ? (
            <span className="inline-flex items-center gap-2 rounded-full border border-indigo-200 bg-indigo-50 px-4 py-1.5 text-xs font-semibold text-indigo-700">
              <span className="inline-block h-2 w-2 animate-pulse rounded-full bg-indigo-500"></span>
              Generating UI…
            </span>
          ) : isFallback ? (
            <span className="inline-flex items-center gap-2 rounded-full border border-amber-300 bg-amber-50 px-4 py-1.5 text-xs font-semibold text-amber-800">
              <span className="inline-block h-2 w-2 rounded-full bg-amber-500"></span>
              ⚠️ Groq Quota — Fallback Active
            </span>
          ) : decision ? (
            <span className="inline-flex items-center gap-2 rounded-full border border-emerald-200 bg-emerald-50 px-4 py-1.5 text-xs font-semibold text-emerald-700">
              <span className="inline-block h-2 w-2 rounded-full bg-emerald-500"></span>
              🖼 {decision
                .split('_')
                .map(w => w.charAt(0).toUpperCase() + w.slice(1))
                .join(' ')}
            </span>
          ) : null}

          {/* Backend generation time */}
          {generationTime != null && (
            <span
              title="Backend LLM generation time"
              className="inline-flex items-center gap-1.5 rounded-full border border-slate-200 bg-slate-100 px-3 py-1.5 text-xs font-semibold text-slate-600"
            >
              ⚡ Gen: {generationTime}s
            </span>
          )}

          {/* Frontend render time */}
          {renderTimeMs != null && (
            <span
              title="Frontend compile + render time"
              className="inline-flex items-center gap-1.5 rounded-full border border-violet-200 bg-violet-50 px-3 py-1.5 text-xs font-semibold text-violet-700"
            >
              🎨 Render: {renderTimeMs}ms
            </span>
          )}
        </div>

        {/* Right: Reset + Reload buttons */}
        <div className="flex items-center gap-2">
          {defaultCode !== null && (
            <button
              type="button"
              onClick={resetToDefault}
              className="rounded-lg border border-slate-200 bg-white px-4 py-2 text-sm font-medium text-slate-700 transition hover:bg-slate-50"
            >
              ↺ Reset
            </button>
          )}

          <button
            type="button"
            onClick={() => build(editableCode)}
            className="rounded-lg bg-indigo-600 px-4 py-2 text-sm font-medium text-white transition hover:bg-indigo-500"
          >
            ⟳ Reload
          </button>
        </div>
      </div>

      {/* ============================
          Error Panel
      ============================ */}

      {errorMessage && (
        <ErrorPanel
          title={
            degraded
              ? "Latest generation failed. Showing previous version."
              : "Compilation Failed"
          }
          message={errorMessage}
        />
      )}

      {/* ============================
          Renderer
      ============================ */}

      <div className="rounded-2xl border border-slate-200 bg-white p-5 shadow-sm">
        <RenderBoundary
          key={renderKey}
          onError={(error) =>
            setErrorMessage(error.message)
          }
          onRetry={revertToLastGood}
        >
          <TransitionShell
            status={
              SHELL_STATUS[
                isReady
                  ? "ready"
                  : status
              ] ?? "idle"
            }
            staticUI={renderStaticUI()}
            errorPanel={
              <StaticFallbackForm
                onRetry={() =>
                  build(editableCode)
                }
              />
            }
            generatedComponent={
              isReady
                ? CompiledComponent
                : null
            }
            scope={memoScope}
          />
        </RenderBoundary>
      </div>

      {/* ============================
          Code Editor
      ============================ */}

      <CodeEditorPanel
        code={editableCode}
        onChange={setEditableCode}
        onRun={() => build(editableCode)}
      />
    </div>
  );
}
