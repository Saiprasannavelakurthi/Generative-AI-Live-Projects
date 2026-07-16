import { useCallback, useEffect, useRef, useState } from 'react';

/**
 * useClickPatterns
 * ----------------
 * Tracks click rhythm: how long the cursor paused before each click,
 * whether consecutive clicks form a double-click, and the variance of
 * recent click intervals as a rough rhythm signal.
 *
 * const { lastClick, clickCount } = useClickPatterns(onEvent, options);
 */

const DEFAULTS = {
  doubleClickWindowMs: 400,
  doubleClickDistancePx: 12,
};

function variance(values) {
  if (values.length < 2) return null;
  const mean = values.reduce((a, b) => a + b, 0) / values.length;
  return values.reduce((a, b) => a + (b - mean) ** 2, 0) / values.length;
}

function describeTarget(el) {
  if (!el || !el.tagName) return null;
  const tag = el.tagName.toLowerCase();
  const id = el.id ? `#${el.id}` : '';
  const cls =
    typeof el.className === 'string' && el.className.trim()
      ? `.${el.className.trim().split(/\s+/).join('.')}`
      : '';
  return `${tag}${id}${cls}`.slice(0, 120);
}

export function useClickPatterns(onEvent, options = {}) {
  const config = { ...DEFAULTS, ...options };

  const [state, setState] = useState({ lastClick: null, clickCount: 0 });

  const lastMoveTRef = useRef(performance.now());
  const lastClickRef = useRef(null);
  const clickTimestampsRef = useRef([]);

  const trackMove = useCallback(() => {
    lastMoveTRef.current = performance.now();
  }, []);

  const handleClick = useCallback(
    (e) => {
      const now = performance.now();
      const pauseBeforeClickMs = now - lastMoveTRef.current;

      const prevClick = lastClickRef.current;
      let isDoubleClick = false;
      if (prevClick) {
        const dt = now - prevClick.t;
        const dist = Math.hypot(e.clientX - prevClick.x, e.clientY - prevClick.y);
        isDoubleClick = dt <= config.doubleClickWindowMs && dist <= config.doubleClickDistancePx;
      }

      clickTimestampsRef.current.push(now);
      if (clickTimestampsRef.current.length > 20) clickTimestampsRef.current.shift();

      const intervals = [];
      for (let i = 1; i < clickTimestampsRef.current.length; i++) {
        intervals.push(clickTimestampsRef.current[i] - clickTimestampsRef.current[i - 1]);
      }
      const rhythmVarianceMs = variance(intervals);

      const clickEvent = {
        type: 'click',
        x: e.clientX,
        y: e.clientY,
        target: describeTarget(e.target),
        pauseBeforeClickMs: Math.round(pauseBeforeClickMs),
        isDoubleClick,
        rhythmVarianceMs: rhythmVarianceMs !== null ? Math.round(rhythmVarianceMs) : null,
        timestamp: Date.now(),
      };

      lastClickRef.current = { x: e.clientX, y: e.clientY, t: now };
      onEvent(clickEvent);
      setState((s) => ({ lastClick: clickEvent, clickCount: s.clickCount + 1 }));
    },
    [config.doubleClickWindowMs, config.doubleClickDistancePx, onEvent]
  );

  useEffect(() => {
    window.addEventListener('mousemove', trackMove, { passive: true });
    window.addEventListener('click', handleClick, { passive: true });
    return () => {
      window.removeEventListener('mousemove', trackMove);
      window.removeEventListener('click', handleClick);
    };
  }, [trackMove, handleClick]);

  return state;
}

export default useClickPatterns;
