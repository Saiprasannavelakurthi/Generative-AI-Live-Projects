import { useEffect, useRef, useState } from "react";

export default function useMouseAnalytics({
  websocketUrl,
  batchInterval = 100,
  hesitationThreshold = 300,
}) {
  const ws = useRef(null);

  const [metrics, setMetrics] = useState({
    velocity: 0,
    acceleration: 0,
    hesitation: false,
    clicks: 0,
  });

  const previous = useRef({
    x: 0,
    y: 0,
    time: performance.now(),
    velocity: 0,
  });

  const lastMove = useRef(performance.now());
  const lastClick = useRef(0);

  const queue = useRef([]);

  useEffect(() => {
    ws.current = new WebSocket(websocketUrl);

    const handleMove = (e) => {
      const now = performance.now();

      const dt = (now - previous.current.time) / 1000;

      const dx = e.clientX - previous.current.x;
      const dy = e.clientY - previous.current.y;

      const distance = Math.sqrt(dx * dx + dy * dy);

      const velocity = dt ? distance / dt : 0;

      const acceleration = dt
        ? (velocity - previous.current.velocity) / dt
        : 0;

      const hesitation =
        now - lastMove.current > hesitationThreshold;

      const event = {
        type: "move",
        timestamp: Date.now(),
        x: e.clientX,
        y: e.clientY,
        velocity,
        acceleration,
        hesitation,
      };

      queue.current.push(event);

      setMetrics((m) => ({
        ...m,
        velocity,
        acceleration,
        hesitation,
      }));

      previous.current = {
        x: e.clientX,
        y: e.clientY,
        time: now,
        velocity,
      };

      lastMove.current = now;
    };

    const handleClick = (e) => {
      const now = Date.now();

      const interval = now - lastClick.current;

      queue.current.push({
        type: "click",
        timestamp: now,
        x: e.clientX,
        y: e.clientY,
        interval,
        doubleClick: interval < 300,
      });

      setMetrics((m) => ({
        ...m,
        clicks: m.clicks + 1,
      }));

      lastClick.current = now;
    };

    window.addEventListener("mousemove", handleMove);
    window.addEventListener("click", handleClick);

    const timer = setInterval(() => {
      if (
        ws.current.readyState === WebSocket.OPEN &&
        queue.current.length
      ) {
        ws.current.send(JSON.stringify(queue.current));
        queue.current = [];
      }
    }, batchInterval);

    return () => {
      clearInterval(timer);
      window.removeEventListener("mousemove", handleMove);
      window.removeEventListener("click", handleClick);
      ws.current.close();
    };
  }, [websocketUrl, batchInterval, hesitationThreshold]);

  return metrics;
}