import { useCallback, useEffect, useRef, useState } from "react";

const DEFAULTS = {
  wsUrl: null,
  batchIntervalMs: 3000,
  maxBatchSize: 50,
  maxQueuedBatches: 5,
  reconnect: true,
  reconnectBaseDelayMs: 1000,
  reconnectMaxDelayMs: 15000,
};

// Minimum gap (ms) between successive UI swaps shown to the user
const UI_UPDATE_THROTTLE_MS = 3000;

// ==========================================================
// Helpers
// ==========================================================

function getMinimalDomContext() {
  try {
    const inputs = Array.from(
      document.querySelectorAll("input, textarea, select")
    );

    const fields = inputs
      .filter((el) => el.id || el.name || el.placeholder)
      .map((el) => ({
        tag: el.tagName.toLowerCase(),
        type: el.type || "",
        id: el.id || "",
        name: el.name || "",
        placeholder: el.placeholder || "",
        value: el.value || "",
      }));

    if (fields.length === 0) {
      return "No form fields detected.";
    }

    return JSON.stringify(fields);
  } catch {
    return "DOM context unavailable.";
  }
}

function getFormData() {
  try {
    const inputs = Array.from(
      document.querySelectorAll("input, textarea, select")
    );

    const data = {};

    inputs.forEach((el) => {
      const key = el.id || el.name || el.placeholder;
      if (key && el.value) {
        data[key] = el.value;
      }
    });

    return data;
  } catch {
    return {};
  }
}

// ==========================================================
// Hook
// ==========================================================

export function useTelemetrySocket(options = {}) {
  const [status, setStatus] = useState("idle");

  const [backendMessage, setBackendMessage] =
    useState(null);

  const [generatedCode, setGeneratedCode] =
    useState("");

  const [isGenerating, setIsGenerating] =
    useState(false);

  const [cognitiveScore, setCognitiveScore] =
    useState(0);

  const [highLoad, setHighLoad] =
    useState(false);

  const [isFallback, setIsFallback] =
    useState(false);

  const [decision, setDecision] =
    useState("");

  const [generationTime, setGenerationTime] =
    useState(null);

  // Stable ref so onmessage closure always has latest setter (avoids stale closure / HMR issues)
  const setIsFallbackRef = useRef(setIsFallback);
  useEffect(() => { setIsFallbackRef.current = setIsFallback; }, [setIsFallback]);

  const wsRef = useRef(null);

  const bufferRef = useRef([]);

  const tokenStreamBufferRef = useRef("");

  const sessionIdRef = useRef(
    (() => {
      try {
        const stored = localStorage.getItem("auragen_session_id");
        if (stored) return stored;
        const fresh = crypto.randomUUID();
        localStorage.setItem("auragen_session_id", fresh);
        return fresh;
      } catch {
        return crypto.randomUUID();
      }
    })()
  );

  const reconnectAttemptRef = useRef(0);

  const reconnectTimeoutRef = useRef(null);

  const flushIntervalRef = useRef(null);

  const isUnmountedRef = useRef(false);

  const cognitiveScoreRef = useRef(0);
  const activeGenPageRef = useRef("");

  // Throttle — tracks when we last swapped the visible UI (ms timestamp)
  const lastUiUpdateRef = useRef(0);
  const uiUpdateTimerRef = useRef(null);

  const wsUrlRef = useRef(options.wsUrl ?? DEFAULTS.wsUrl);
  const reconnectRef = useRef(options.reconnect ?? DEFAULTS.reconnect);
  const reconnectBaseDelayRef = useRef(options.reconnectBaseDelayMs ?? DEFAULTS.reconnectBaseDelayMs);
  const reconnectMaxDelayRef = useRef(options.reconnectMaxDelayMs ?? DEFAULTS.reconnectMaxDelayMs);
  const batchIntervalRef = useRef(options.batchIntervalMs ?? DEFAULTS.batchIntervalMs);
  const maxBatchSizeRef = useRef(options.maxBatchSize ?? DEFAULTS.maxBatchSize);
  const maxQueuedBatchesRef = useRef(options.maxQueuedBatches ?? DEFAULTS.maxQueuedBatches);

  const pageNameRef = useRef(options.pageName ?? "login");
  const activeFieldRef = useRef(options.activeField ?? "");

  useEffect(() => {
    pageNameRef.current = options.pageName ?? "login";
  }, [options.pageName]);

  useEffect(() => {
    activeFieldRef.current = options.activeField ?? "";
  }, [options.activeField]);

  useEffect(() => {
    cognitiveScoreRef.current = cognitiveScore;
  }, [cognitiveScore]);

  // ==========================================
  // Flush telemetry events
  // ==========================================

  const flush = useCallback((flushOpts = {}) => {
    const isForce = Boolean(flushOpts.forceGenerate);

    // Always send telemetry batch for 1-second continuous score recalculation
    const batch = [...bufferRef.current];
    bufferRef.current = [];

    if (
      wsRef.current &&
      wsRef.current.readyState === WebSocket.OPEN
    ) {
      wsRef.current.send(
        JSON.stringify({
          type: "telemetry_batch",

          session_id: sessionIdRef.current,

          page_name: pageNameRef.current,

          current_component: pageNameRef.current,

          active_field: activeFieldRef.current,

          cognitive_score: cognitiveScoreRef.current,

          user_action: batch.at(-1)?.type ?? "move",

          force_generate: isForce,

          dom_state: getMinimalDomContext(),

          form_data: getFormData(),

          sentAt: Date.now(),

          events: batch,
        })
      );
    } else {
      bufferRef.current.unshift(...batch);

      bufferRef.current = bufferRef.current.slice(
        -maxBatchSizeRef.current * maxQueuedBatchesRef.current
      );
    }
  }, []);

  // ==========================================
  // Queue events
  // ==========================================

  const enqueue = useCallback(
    (event) => {
      bufferRef.current.push(event);

      if (bufferRef.current.length >= maxBatchSizeRef.current) {
        flush();
      }
    },
    [flush]
  );

  // ==========================================
  // WebSocket Connection
  // ==========================================

  const connectRef = useRef(null);

  // eslint-disable-next-line react-hooks/refs
  connectRef.current = () => {
    const wsUrl = wsUrlRef.current;

    if (!wsUrl) {
      return;
    }

    if (
      wsRef.current &&
      (wsRef.current.readyState === WebSocket.OPEN ||
        wsRef.current.readyState === WebSocket.CONNECTING)
    ) {
      return;
    }

    setStatus("connecting");

    console.log("[AuraGen] Connecting to:", wsUrl);

    const ws = new WebSocket(wsUrl);

    wsRef.current = ws;

    ws.onopen = () => {
      reconnectAttemptRef.current = 0;
      setStatus("open");
      console.log("[AuraGen] ✅ WebSocket Connected, session:", sessionIdRef.current);
      // Send a ping with session_id so backend can replay last generated code
      try {
        ws.send(JSON.stringify({
          type: "session_restore",
          session_id: sessionIdRef.current,
        }));
      } catch { /* ignore */ }
    };

    ws.onmessage = (event) => {
      try {
        const message = JSON.parse(event.data);

        setBackendMessage(message);

        switch (message.type) {

          case "cognitive_score":
            setCognitiveScore(message.score ?? 0);
            setHighLoad(Boolean(message.high_load));
            break;

          case "generation_start":
            if (message.page_name && message.page_name !== pageNameRef.current) {
              console.log("[AuraGen] Ignoring generation_start for old page:", message.page_name);
              break;
            }
            activeGenPageRef.current = message.page_name || pageNameRef.current;
            console.log("[AuraGen] Generation start for page:", message.page_name);
            setIsGenerating(true);
            setGenerationTime(null);
            if (message.decision) setDecision(message.decision);
            if (message.baseline_code) {
              const now = Date.now();
              const elapsed = now - lastUiUpdateRef.current;
              if (elapsed >= UI_UPDATE_THROTTLE_MS) {
                lastUiUpdateRef.current = now;
                setGeneratedCode(message.baseline_code);
              } else {
                const delay = UI_UPDATE_THROTTLE_MS - elapsed;
                clearTimeout(uiUpdateTimerRef.current);
                uiUpdateTimerRef.current = setTimeout(() => {
                  lastUiUpdateRef.current = Date.now();
                  setGeneratedCode(message.baseline_code);
                }, delay);
              }
            }
            tokenStreamBufferRef.current = "";
            break;

          case "token":
            if (activeGenPageRef.current && activeGenPageRef.current !== pageNameRef.current) {
              break;
            }
            tokenStreamBufferRef.current += (message.content ?? "");
            break;

          case "complete":
            if (message.page_name && message.page_name !== pageNameRef.current) {
              console.log("[AuraGen] Ignoring complete message for old page:", message.page_name);
              break;
            }
            console.log("[AuraGen] Received COMPLETE for page:", message.page_name);
            setIsGenerating(false);
            if (typeof setIsFallbackRef.current === "function") {
              setIsFallbackRef.current(Boolean(message.is_fallback));
            }
            if (message.decision) setDecision(message.decision);
            if (message.generation_time !== undefined) {
              setGenerationTime(message.generation_time);
            }
            {
              const finalCode = message.generated_code || tokenStreamBufferRef.current;
              const now = Date.now();
              const elapsed = now - lastUiUpdateRef.current;
              if (elapsed >= UI_UPDATE_THROTTLE_MS) {
                lastUiUpdateRef.current = now;
                setGeneratedCode(finalCode);
              } else {
                const delay = UI_UPDATE_THROTTLE_MS - elapsed;
                clearTimeout(uiUpdateTimerRef.current);
                uiUpdateTimerRef.current = setTimeout(() => {
                  lastUiUpdateRef.current = Date.now();
                  setGeneratedCode(finalCode);
                }, delay);
              }
            }
            break;

          case "error":
            console.error("[AuraGen] Backend Error:", message.message);
            setIsGenerating(false);
            break;

          default:
            console.log("[AuraGen] Unknown Message:", message);
        }

      } catch (error) {
        console.error("[AuraGen] WebSocket Parse Error:", error);
      }
    };

    ws.onerror = () => {
      setStatus("error");
    };

    ws.onclose = () => {
      console.log("[AuraGen] ❌ WebSocket Closed");
      setStatus("closed");
      wsRef.current = null;

      if (isUnmountedRef.current) {
        return;
      }

      if (!reconnectRef.current) {
        return;
      }

      reconnectAttemptRef.current += 1;

      const delay = Math.min(
        reconnectBaseDelayRef.current *
          Math.pow(2, reconnectAttemptRef.current - 1),
        reconnectMaxDelayRef.current
      );

      reconnectTimeoutRef.current = setTimeout(() => {
        if (!isUnmountedRef.current) {
          connectRef.current();
        }
      }, delay);
    };
  };

  const connect = useCallback(() => {
    connectRef.current();
  }, []);

  // ==========================================
  // Lifecycle
  // ==========================================

  useEffect(() => {
    isUnmountedRef.current = false;

    connect();

    flushIntervalRef.current = setInterval(
      flush,
      batchIntervalRef.current
    );

    return () => {
      isUnmountedRef.current = true;

      if (flushIntervalRef.current) {
        clearInterval(flushIntervalRef.current);
        flushIntervalRef.current = null;
      }

      if (reconnectTimeoutRef.current) {
        clearTimeout(reconnectTimeoutRef.current);
        reconnectTimeoutRef.current = null;
      }

      if (wsRef.current) {
        wsRef.current.onopen = null;
        wsRef.current.onmessage = null;
        wsRef.current.onerror = null;
        wsRef.current.onclose = null;
        wsRef.current.close();
        wsRef.current = null;
      }
    };
  }, [connect, flush]);

  // ==========================================
  // Manual reconnect
  // ==========================================

  const reconnect = useCallback(() => {
    if (wsRef.current) {
      wsRef.current.onopen = null;
      wsRef.current.onmessage = null;
      wsRef.current.onerror = null;
      wsRef.current.onclose = null;
      wsRef.current.close();
      wsRef.current = null;
    }

    reconnectAttemptRef.current = 0;

    connect();
  }, [connect]);

  const clearGeneratedCode = useCallback(() => {
    setGeneratedCode("");
    setDecision("");
    setGenerationTime(null);
  }, []);

  return {
    status,

    enqueue,

    flush,

    reconnect,

    backendMessage,

    generatedCode,

    isGenerating,

    clearGeneratedCode,

    cognitiveScore,

    highLoad,

    isFallback,

    decision,

    generationTime,
  };
}

export default useTelemetrySocket;