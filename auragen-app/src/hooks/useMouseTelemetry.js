import { useCallback, useMemo } from "react";

import { useTelemetrySocket } from "./useTelemetrySocket";
import { useMouseVelocityAndHesitation } from "./useMouseVelocityAndHesitation";
import { useClickPatterns } from "./useClickPatterns";

/**
 * useMouseTelemetry
 *
 * Combines:
 * 1. Mouse movement tracking
 * 2. Click tracking
 * 3. WebSocket telemetry
 * 4. Cognitive score updates
 * 5. Generated React component streaming
 */

export function useMouseTelemetry(options = {}) {
  const {
    status,
    enqueue,
    flush,
    reconnect,
    backendMessage,
    generatedCode,
    clearGeneratedCode,
    cognitiveScore,
    highLoad,
  } = useTelemetrySocket(options);

  const handleEvent = useCallback(
    (event) => {
      enqueue(event);

      // Flush immediately on clicks
      if (event.type === "click") {
        flush();
      }
    },
    [enqueue, flush]
  );

  const mouse = useMouseVelocityAndHesitation(
    handleEvent,
    options
  );

  const clicks = useClickPatterns(
    handleEvent,
    options
  );

  return useMemo(
    () => ({
      x: mouse.x,
      y: mouse.y,

      velocity: mouse.velocity,

      isHesitating: mouse.isHesitating,

      lastClick: clicks.lastClick,

      clickCount: clicks.clickCount,

      connectionStatus: status,

      flushNow: flush,

      reconnect,

      backendMessage,

      generatedCode,

      clearGeneratedCode,

      cognitiveScore,

      highLoad,
    }),
    [
      mouse,
      clicks,
      status,
      flush,
      reconnect,
      backendMessage,
      generatedCode,
      clearGeneratedCode,
      cognitiveScore,
      highLoad,
    ]
  );
}

export default useMouseTelemetry;