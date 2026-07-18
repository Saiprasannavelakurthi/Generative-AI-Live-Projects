import { useCallback, useEffect, useRef, useState } from 'react';

/**
 * useMouseVelocityAndHesitation
 * -----------------------------
 * Tracks live cursor position + velocity (px/ms) and detects "hesitation":
 * a sustained low-velocity dwell lasting at least `hesitationMinDurationMs`.
 * Emits raw events through `onEvent` and also returns live state for
 * rendering (e.g. a status readout).
 *
 * const { x, y, velocity, isHesitating } =
 *   useMouseVelocityAndHesitation(onEvent, { hesitationMinDurationMs: 300 });
 */

const DEFAULTS = {
  hesitationVelocityThreshold: 0.05, // px/ms below this counts as "not moving"
  hesitationMinDurationMs: 300,
};

export function useMouseVelocityAndHesitation(onEvent, options = {}) {
  const config = { ...DEFAULTS, ...options };

  const [state, setState] = useState({ x: 0, y: 0, velocity: 0, isHesitating: false });

  const lastPointRef = useRef({ x: 0, y: 0, t: performance.now() });
  const hesitationStartRef = useRef(null);

  const handleMouseMove = useCallback(
    (e) => {
      const now = performance.now();
      const prev = lastPointRef.current;
      const dt = Math.max(now - prev.t, 1);
      const distance = Math.hypot(e.clientX - prev.x, e.clientY - prev.y);
      const velocity = distance / dt; // px per ms

      lastPointRef.current = { x: e.clientX, y: e.clientY, t: now };

      let isHesitating = hesitationStartRef.current !== null;

      if (velocity < config.hesitationVelocityThreshold) {
        if (hesitationStartRef.current === null) {
          hesitationStartRef.current = { t: now, x: e.clientX, y: e.clientY };
        }
        isHesitating = true;
      } else if (hesitationStartRef.current !== null) {
        const duration = now - hesitationStartRef.current.t;
        if (duration >= config.hesitationMinDurationMs) {
          onEvent({
            type: 'hesitation',
            x: hesitationStartRef.current.x,
            y: hesitationStartRef.current.y,
            durationMs: Math.round(duration),
            timestamp: Date.now(),
          });
        }
        hesitationStartRef.current = null;
        isHesitating = false;
      }

      onEvent({
        type: 'move',
        x: e.clientX,
        y: e.clientY,
        velocity: Number(velocity.toFixed(4)),
        timestamp: Date.now(),
      });

      setState({ x: e.clientX, y: e.clientY, velocity, isHesitating });
    },
    [config.hesitationVelocityThreshold, config.hesitationMinDurationMs, onEvent]
  );

  useEffect(() => {
    window.addEventListener('mousemove', handleMouseMove, { passive: true });
    return () => window.removeEventListener('mousemove', handleMouseMove);
  }, [handleMouseMove]);

  return state;
}

export default useMouseVelocityAndHesitation;
