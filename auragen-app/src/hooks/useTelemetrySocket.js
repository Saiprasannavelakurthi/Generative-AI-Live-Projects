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

export function useTelemetrySocket(options = {}) {
  const config = {
    ...DEFAULTS,
    ...options,
  };

  const [status, setStatus] = useState("idle");

  const [backendMessage, setBackendMessage] =
    useState(null);

  const [generatedCode, setGeneratedCode] =
    useState("");

  const [cognitiveScore, setCognitiveScore] =
    useState(0);

  const [highLoad, setHighLoad] =
    useState(false);

  const wsRef = useRef(null);

  const bufferRef = useRef([]);

  const sessionIdRef = useRef(
    crypto.randomUUID()
  );

  const reconnectAttemptRef =
    useRef(0);

  const reconnectTimeoutRef =
    useRef(null);

  const flushIntervalRef =
    useRef(null);

  const isUnmountedRef =
    useRef(false);

  // ==========================================
  // Flush telemetry events
  // ==========================================

  const flush = useCallback(() => {
    if (!bufferRef.current.length) {
      return;
    }

    const batch = [...bufferRef.current];

    bufferRef.current = [];

    if (
      wsRef.current &&
      wsRef.current.readyState === WebSocket.OPEN
    ) {
      wsRef.current.send(
        JSON.stringify({
          type: "telemetry_batch",

          session_id:
            sessionIdRef.current,

          page_name: "login",

          current_component:
            "Login",

          active_field: "",

          cognitive_score:
            cognitiveScore,

          user_action:
            batch.at(-1)?.type ??
            "move",

          dom_state:
            document.body.innerHTML,

          form_data: {},

          sentAt: Date.now(),

          events: batch,
        })
      );
    } else {
      bufferRef.current.unshift(
        ...batch
      );

      bufferRef.current =
        bufferRef.current.slice(
          -config.maxBatchSize *
            config.maxQueuedBatches
        );
    }
  }, [
    cognitiveScore,
    config.maxBatchSize,
    config.maxQueuedBatches,
  ]);

  // ==========================================
  // Queue events
  // ==========================================

  const enqueue = useCallback(
    (event) => {
      bufferRef.current.push(event);

      if (
        bufferRef.current.length >=
        config.maxBatchSize
      ) {
        flush();
      }
    },
    [
      flush,
      config.maxBatchSize,
    ]
  );

    // ==========================================
  // WebSocket Connection
  // ==========================================

  const connect = useCallback(() => {
    if (!config.wsUrl) {
      return;
    }

    // Prevent duplicate connections
    if (
      wsRef.current &&
      (wsRef.current.readyState === WebSocket.OPEN ||
        wsRef.current.readyState === WebSocket.CONNECTING)
    ) {
      return;
    }

    setStatus("connecting");

    console.log("Connecting to:", config.wsUrl);

    const ws = new WebSocket(config.wsUrl);

    wsRef.current = ws;

    ws.onopen = () => {
      reconnectAttemptRef.current = 0;

      setStatus("open");

      console.log("✅ WebSocket Connected");
    };

    ws.onmessage = (event) => {
      try {
        console.log("========== RAW WS ==========");
        console.log(event.data);

        const message = JSON.parse(event.data);

        console.log("========== PARSED ==========");
        console.log(message);

        setBackendMessage(message);

        switch (message.type) {

          case "cognitive_score":
            console.log("Received cognitive_score");

            setCognitiveScore(message.score ?? 0);

            setHighLoad(Boolean(message.high_load));

            break;

          case "token":
            console.log("Received TOKEN");

            setGeneratedCode((previous) =>
              previous + (message.content ?? "")
            );

            break;

          case "complete":
            console.log("Received COMPLETE");

            setGeneratedCode(
              message.generated_code ?? ""
            );

            break;

          case "error":
            console.error(
              "Backend Error:",
              message.message
            );

            break;

          default:
            console.log(
              "Unknown Message:",
              message
            );
        }

      } catch (error) {

        console.error(
          "WebSocket Parse Error:",
          error
        );
      }
    };

    ws.onerror = (error) => {

      console.error(
        "WebSocket Error:",
        error
      );

      setStatus("error");
    };

    ws.onclose = () => {

      console.log("❌ WebSocket Closed");

      setStatus("closed");

      wsRef.current = null;

      // Don't reconnect after component unmount
      if (isUnmountedRef.current) {
        return;
      }

      if (!config.reconnect) {
        return;
      }

      reconnectAttemptRef.current += 1;

      const delay = Math.min(
        config.reconnectBaseDelayMs *
          Math.pow(
            2,
            reconnectAttemptRef.current - 1
          ),
        config.reconnectMaxDelayMs
      );

      console.log(
        `Reconnect in ${delay} ms`
      );

      reconnectTimeoutRef.current =
        setTimeout(() => {
          connect();
        }, delay);
    };

  }, [
    config.wsUrl,
    config.reconnect,
    config.reconnectBaseDelayMs,
    config.reconnectMaxDelayMs,
  ]);

    // ==========================================
  // Lifecycle
  // ==========================================

  useEffect(() => {
    isUnmountedRef.current = false;

    connect();

    flushIntervalRef.current = setInterval(
      flush,
      config.batchIntervalMs
    );

    return () => {
      isUnmountedRef.current = true;

      if (flushIntervalRef.current) {
        clearInterval(flushIntervalRef.current);
      }

      if (reconnectTimeoutRef.current) {
        clearTimeout(reconnectTimeoutRef.current);
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

  }, [
    connect,
    flush,
    config.batchIntervalMs,
  ]);

  // ==========================================
  // Manual reconnect
  // ==========================================

  const reconnect = useCallback(() => {

    if (wsRef.current) {
      wsRef.current.close();
      wsRef.current = null;
    }

    reconnectAttemptRef.current = 0;

    connect();

  }, [connect]);

  // ==========================================
  // Reset generated component
  // ==========================================

  const clearGeneratedCode = useCallback(() => {
    setGeneratedCode("");
  }, []);

  // ==========================================
  // Return
  // ==========================================

  return {
    status,

    enqueue,

    flush,

    reconnect,

    backendMessage,

    generatedCode,

    clearGeneratedCode,

    cognitiveScore,

    highLoad,
  };
}

export default useTelemetrySocket;