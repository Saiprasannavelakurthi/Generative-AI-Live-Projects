import { useCallback, useEffect, useRef, useState } from "react";

/**
 * Tracks mouse movement, velocity, acceleration,
 * and hesitation events.
 */

const DEFAULTS = {
  hesitationVelocityThreshold: 0.05,
  hesitationMinDurationMs: 300,
};

export function useMouseVelocityAndHesitation(
  onEvent,
  options = {}
) {
  const config = {
    ...DEFAULTS,
    ...options,
  };

  const [state, setState] = useState({
    x: 0,
    y: 0,
    velocity: 0,
    isHesitating: false,
  });

  const lastPointRef = useRef({
    x: 0,
    y: 0,
    t: performance.now(),
    velocity: 0,
  });

  const hesitationStartRef = useRef(null);

  const handleMouseMove = useCallback(
    (event) => {
      const now = performance.now();

      const previous = lastPointRef.current;

      const dt = Math.max(now - previous.t, 1);

      const dx = event.clientX - previous.x;
      const dy = event.clientY - previous.y;

      const distance = Math.hypot(dx, dy);

      const velocity = distance / dt;

      const acceleration =
        (velocity - previous.velocity) / dt;

      let isHesitating = false;

      if (
        velocity <
        config.hesitationVelocityThreshold
      ) {
        if (!hesitationStartRef.current) {
          hesitationStartRef.current = {
            x: event.clientX,
            y: event.clientY,
            t: now,
          };
        }

        isHesitating = true;
      } else {
        if (hesitationStartRef.current) {
          const duration =
            now - hesitationStartRef.current.t;

          if (
            duration >=
            config.hesitationMinDurationMs
          ) {
            onEvent({
              type: "hesitation",
              x: hesitationStartRef.current.x,
              y: hesitationStartRef.current.y,
              durationMs: Math.round(duration),
              timestamp: Date.now(),
            });
          }

          hesitationStartRef.current = null;
        }

        isHesitating = false;
      }

      lastPointRef.current = {
        x: event.clientX,
        y: event.clientY,
        t: now,
        velocity,
      };

      onEvent({
        type: "move",
        x: event.clientX,
        y: event.clientY,
        velocity: Number(velocity.toFixed(4)),
        acceleration: Number(
          acceleration.toFixed(4)
        ),
        hesitation: isHesitating,
        timestamp: Date.now(),
      });

      setState({
        x: event.clientX,
        y: event.clientY,
        velocity,
        isHesitating,
      });
    },
    [
      config.hesitationVelocityThreshold,
      config.hesitationMinDurationMs,
      onEvent,
    ]
  );

  useEffect(() => {
    window.addEventListener(
      "mousemove",
      handleMouseMove,
      {
        passive: true,
      }
    );

    return () => {
      window.removeEventListener(
        "mousemove",
        handleMouseMove
      );
    };
  }, [handleMouseMove]);

  return state;
}

export default useMouseVelocityAndHesitation;