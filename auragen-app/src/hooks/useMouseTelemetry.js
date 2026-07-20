import { useCallback } from 'react';
import { useTelemetrySocket } from './useTelemetrySocket';
import { useMouseVelocityAndHesitation } from './useMouseVelocityAndHesitation';
import { useClickPatterns } from './useClickPatterns';

/**
 * useMouseTelemetry
 * -----------------
 * Composition root: wires the socket hook (transport), the velocity/
 * hesitation hook, and the click-pattern hook into one API. Each concern
 * lives in its own file and can be used independently if needed.
 *
 * const telemetry = useMouseTelemetry({ wsUrl: 'wss://api.example.com/telemetry' });
 * telemetry -> { x, y, velocity, isHesitating, lastClick, clickCount, connectionStatus, flushNow }
 */
export function useMouseTelemetry(options = {}) {
<<<<<<< Updated upstream
  const { status, enqueue, flush } = useTelemetrySocket(options);
=======
  const { status, enqueue, flush, generatedCode, generationError } = useTelemetrySocket(options);
>>>>>>> Stashed changes

  // Clicks are meaningful, low-frequency events — ship them immediately
  // instead of waiting for the next batch tick.
  const handleEvent = useCallback(
    (event) => {
      enqueue(event);
      if (event.type === 'click') flush();
    },
    [enqueue, flush]
  );

  const velocity = useMouseVelocityAndHesitation(handleEvent, options);
  const clicks = useClickPatterns(handleEvent, options);

  return {
    x: velocity.x,
    y: velocity.y,
    velocity: velocity.velocity,
    isHesitating: velocity.isHesitating,
    lastClick: clicks.lastClick,
    clickCount: clicks.clickCount,
    connectionStatus: status,
    flushNow: flush,
<<<<<<< Updated upstream
=======
    generatedCode,
    generationError,
>>>>>>> Stashed changes
  };
}

export default useMouseTelemetry;