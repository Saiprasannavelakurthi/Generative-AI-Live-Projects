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
  const config = { ...DEFAULTS, ...options };

  const [status, setStatus] = useState("idle");
  const [backendMessage, setBackendMessage] = useState(null);
  const [generatedCode, setGeneratedCode] = useState("");
  const [cognitiveScore, setCognitiveScore] = useState(0);
  const [highLoad, setHighLoad] = useState(false);

  const wsRef = useRef(null);
  const bufferRef = useRef([]);
  const sessionIdRef = useRef(crypto.randomUUID());

  const reconnectAttemptRef = useRef(0);
  const reconnectTimeoutRef = useRef(null);
  const flushIntervalRef = useRef(null);

  const flush = useCallback(() => {
    if (!bufferRef.current.length) return;

    const batch = [...bufferRef.current];
    bufferRef.current = [];

    if (wsRef.current?.readyState === WebSocket.OPEN) {
      wsRef.current.send(
        JSON.stringify({
          type: "telemetry_batch",
          session_id: sessionIdRef.current,
          page_name: "login",
          current_component: "Login",
          active_field: "",
          cognitive_score: cognitiveScore,
          user_action: batch[batch.length - 1]?.type ?? "move",
          dom_state: document.body.innerHTML,
          form_data: {},
          sentAt: Date.now(),
          events: batch,
        })
      );
    }
  }, [cognitiveScore]);

  const enqueue = useCallback(
    (event) => {
      bufferRef.current.push(event);

      if (bufferRef.current.length >= config.maxBatchSize) {
        flush();
      }
    },
    [flush, config.maxBatchSize]
  );

  const connect = useCallback(() => {
    if (!config.wsUrl) return;

    if (
      wsRef.current &&
      (wsRef.current.readyState === WebSocket.OPEN ||
        wsRef.current.readyState === WebSocket.CONNECTING)
    ) {
      return;
    }

    setStatus("connecting");

    const ws = new WebSocket(config.wsUrl);

    wsRef.current = ws;

    ws.onopen = () => {
      reconnectAttemptRef.current = 0;
      setStatus("open");
      console.log("Connected");
    };

    ws.onmessage = (event) => {
      const message = JSON.parse(event.data);

      console.log("FULL MESSAGE");
      console.log(JSON.stringify(message, null, 2));

      setBackendMessage(message);

      switch (message.type) {
        case "cognitive_score":
          setCognitiveScore(message.score ?? 0);
          setHighLoad(!!message.high_load);
          break;

        case "complete":
          console.log("Generated UI received");
          setGeneratedCode(message.generated_code ?? "");
          break;

        default:
          break;
      }
    };

    ws.onclose = () => {
      setStatus("closed");

      if (config.reconnect) {
        reconnectTimeoutRef.current = setTimeout(() => {
          connect();
        }, 3000);
      }
    };

    ws.onerror = (err) => {
      console.error(err);
      setStatus("error");
    };
  }, [config.wsUrl, config.reconnect]);

  useEffect(() => {
    connect();

    flushIntervalRef.current = setInterval(
      flush,
      config.batchIntervalMs
    );

    return () => {
      clearInterval(flushIntervalRef.current);
      clearTimeout(reconnectTimeoutRef.current);

      if (wsRef.current) {
        wsRef.current.close();
      }
    };
  }, [connect, flush, config.batchIntervalMs]);

  return {
    status,
    enqueue,
    flush,
    backendMessage,
    generatedCode,
    cognitiveScore,
    highLoad,
  };
}

export default useTelemetrySocket;