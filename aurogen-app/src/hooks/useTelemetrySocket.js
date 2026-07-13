import { useCallback, useEffect, useRef, useState } from 'react';

/**
 * useTelemetrySocket
 * ------------------
 * Owns the WebSocket connection, event buffering, batch flushing, and
 * reconnect-with-backoff. Knows nothing about mice or clicks — it just
 * ships whatever events it's given.
 *
 * const { status, enqueue, flush } = useTelemetrySocket({ wsUrl });
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

  const [status, setStatus] = useState('idle'); // idle | connecting | open | closed | error

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
      ws.send(JSON.stringify({ type: 'telemetry_batch', events: batch, sentAt: Date.now() }));
    } else {
      // Bounded backlog: keep events across brief disconnects without growing forever.
      const merged = batch.concat(bufferRef.current);
      bufferRef.current = merged.slice(-config.maxBatchSize * config.maxQueuedBatches);
    }
  }, [config.maxBatchSize, config.maxQueuedBatches]);

  const enqueue = useCallback(
    (event) => {
      bufferRef.current.push(event);
      if (bufferRef.current.length >= config.maxBatchSize) flush();
    },
    [config.maxBatchSize, flush]
  );

  const scheduleReconnect = useCallback(
    (connectFn) => {
      const attempt = reconnectAttemptRef.current + 1;
      reconnectAttemptRef.current = attempt;
      const delay = Math.min(
        config.reconnectBaseDelayMs * 2 ** (attempt - 1),
        config.reconnectMaxDelayMs
      );
      reconnectTimeoutRef.current = setTimeout(connectFn, delay);
    },
    [config.reconnectBaseDelayMs, config.reconnectMaxDelayMs]
  );

  const connect = useCallback(() => {
    if (!config.wsUrl) return;
    setStatus('connecting');
    const ws = new WebSocket(config.wsUrl);
    wsRef.current = ws;

    ws.onopen = () => {
      reconnectAttemptRef.current = 0;
      setStatus('open');
    };
    ws.onclose = () => {
      setStatus('closed');
      if (config.reconnect) scheduleReconnect(connect);
    };
    ws.onerror = () => setStatus('error');
  }, [config.wsUrl, config.reconnect, scheduleReconnect]);

  useEffect(() => {
    if (config.wsUrl) connect();
    flushIntervalRef.current = setInterval(flush, config.batchIntervalMs);

   return () => {
    clearInterval(flushIntervalRef.current);
    clearTimeout(reconnectTimeoutRef.current);

  const ws = wsRef.current;

  if (ws) {
    ws.onopen = null;
    ws.onclose = null;
    ws.onerror = null;

    if (
      ws.readyState === WebSocket.OPEN ||
      ws.readyState === WebSocket.CONNECTING
    ) {
      ws.close();
    }
  }
  };
  }, [connect, flush, config.wsUrl, config.batchIntervalMs]);

  return { status, enqueue, flush };
}

export default useTelemetrySocket;
