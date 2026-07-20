import { useCallback, useEffect, useRef, useState } from "react";

/**
 * useTelemetrySocket
 * ------------------
 * Handles:
 * - WebSocket connection
 * - Auto reconnect
 * - Event buffering
 * - Sending telemetry batches
 * - Receiving backend responses
 */

const DEFAULTS = {
  wsUrl: null,
  batchIntervalMs: 500,
  maxBatchSize: 50,
  maxQueuedBatches: 5,
  reconnect: true,
  reconnectBaseDelayMs: 1000,
  reconnectMaxDelayMs: 15000,
};

export function useTelemetrySocket(options = {}) {
  const config = { ...DEFAULTS, ...options };

  const [status, setStatus] = useState("idle");
  const [backendMessage, setBackendMessage] = useState(null);
<<<<<<< Updated upstream
=======
  const [generatedCode, setGeneratedCode] = useState("");
  const [generationError, setGenerationError] = useState(null);
>>>>>>> Stashed changes

  const wsRef = useRef(null);
  const bufferRef = useRef([]);

  const reconnectAttemptRef = useRef(0);
  const reconnectTimeoutRef = useRef(null);
  const flushIntervalRef = useRef(null);

  const flush = useCallback(() => {
    if (bufferRef.current.length === 0) return;

    const batch = bufferRef.current;
    bufferRef.current = [];

    const ws = wsRef.current;

    if (ws && ws.readyState === WebSocket.OPEN) {
      ws.send(
        JSON.stringify({
          type: "telemetry_batch",
          events: batch,
          sentAt: Date.now(),
        })
      );
    } else {
      const merged = batch.concat(bufferRef.current);

      bufferRef.current = merged.slice(
        -config.maxBatchSize * config.maxQueuedBatches
      );
    }
  }, [config.maxBatchSize, config.maxQueuedBatches]);

  const enqueue = useCallback(
    (event) => {
      bufferRef.current.push(event);

      if (bufferRef.current.length >= config.maxBatchSize) {
        flush();
      }
    },
    [config.maxBatchSize, flush]
  );

  const scheduleReconnect = useCallback(
    (connectFn) => {
      const attempt = reconnectAttemptRef.current + 1;

      reconnectAttemptRef.current = attempt;

      const delay = Math.min(
        config.reconnectBaseDelayMs * Math.pow(2, attempt - 1),
        config.reconnectMaxDelayMs
      );

      reconnectTimeoutRef.current = setTimeout(connectFn, delay);
    },
    [config.reconnectBaseDelayMs, config.reconnectMaxDelayMs]
  );

  const connect = useCallback(() => {
    if (!config.wsUrl) return;

    setStatus("connecting");

    const ws = new WebSocket(config.wsUrl);

    wsRef.current = ws;

    ws.onopen = () => {
      reconnectAttemptRef.current = 0;
      setStatus("open");

      console.log("✅ Connected to Backend");
    };

    ws.onclose = () => {
      setStatus("closed");

      console.log("❌ WebSocket Closed");

      if (config.reconnect) {
        scheduleReconnect(connect);
      }
    };

    ws.onerror = (err) => {
      console.error(err);
      setStatus("error");
    };

    // ==========================
    // Receive Backend Messages
    // ==========================

    ws.onmessage = (event) => {
      const message = JSON.parse(event.data);

      console.log("Backend Message:", message);

      setBackendMessage(message);

      if (message.type === "cognitive_score") {
        console.log("Score:", message.score);
      }

      if (message.type === "generated_component") {
        console.log("Generated Component:", message.filename);
        console.log(message.code);
<<<<<<< Updated upstream
=======
        console.log("============================================");

        setGenerationError(null);
        setGeneratedCode(message.code);

        console.log("State Updated with Generated Code");
>>>>>>> Stashed changes
      }

      if (message.type === "generation_error") {
        console.error("Generation failed on backend:", message.message);
        setGenerationError(message.message);
      }
    };
  }, [config.wsUrl, config.reconnect, scheduleReconnect]);

  useEffect(() => {
    if (config.wsUrl) {
      connect();
    }

    flushIntervalRef.current = setInterval(
      flush,
      config.batchIntervalMs
    );

    return () => {
      clearInterval(flushIntervalRef.current);
      clearTimeout(reconnectTimeoutRef.current);

      const ws = wsRef.current;

      if (ws) {
        ws.onopen = null;
        ws.onclose = null;
        ws.onerror = null;
        ws.onmessage = null;

        if (
          ws.readyState === WebSocket.OPEN ||
          ws.readyState === WebSocket.CONNECTING
        ) {
          ws.close();
        }
      }
    };
  }, [connect, flush, config.wsUrl, config.batchIntervalMs]);

  return {
    status,
    enqueue,
    flush,
    backendMessage,
<<<<<<< Updated upstream
=======
    generatedCode,
    generationError,
>>>>>>> Stashed changes
  };
}

export default useTelemetrySocket;