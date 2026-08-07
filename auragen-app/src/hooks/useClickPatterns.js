import { useCallback, useEffect, useRef, useState } from "react";

/**
 * Tracks click behavior including:
 * - Click count
 * - Double-click detection
 * - Pause before click
 * - Click rhythm variance
 */

const DEFAULTS = {
  doubleClickWindowMs: 400,
  doubleClickDistancePx: 12,
};

const MAX_CLICK_HISTORY = 20;

function variance(values) {
  if (values.length < 2) {
    return null;
  }

  const mean =
    values.reduce((sum, value) => sum + value, 0) /
    values.length;

  return (
    values.reduce(
      (sum, value) => sum + (value - mean) ** 2,
      0
    ) / values.length
  );
}

function describeTarget(element) {
  if (!element || !element.tagName) {
    return null;
  }

  const tag = element.tagName.toLowerCase();

  const id = element.id
    ? `#${element.id}`
    : "";

  const classes =
    typeof element.className === "string" &&
    element.className.trim()
      ? `.${element.className
          .trim()
          .split(/\s+/)
          .join(".")}`
      : "";

  return `${tag}${id}${classes}`.slice(0, 120);
}

export function useClickPatterns(
  onEvent,
  options = {}
) {
  const config = {
    ...DEFAULTS,
    ...options,
  };

  const [state, setState] = useState({
    lastClick: null,
    clickCount: 0,
  });

  const lastMoveTimeRef = useRef(
    performance.now()
  );

  const lastClickRef = useRef(null);

  const clickHistoryRef = useRef([]);

  const handleMouseMove = useCallback(() => {
    lastMoveTimeRef.current = performance.now();
  }, []);

  const handleClick = useCallback(
    (event) => {
      const now = performance.now();

      const pauseBeforeClickMs =
        now - lastMoveTimeRef.current;

      let isDoubleClick = false;

      if (lastClickRef.current) {
        const timeDifference =
          now - lastClickRef.current.t;

        const distance = Math.hypot(
          event.clientX - lastClickRef.current.x,
          event.clientY - lastClickRef.current.y
        );

        isDoubleClick =
          timeDifference <=
            config.doubleClickWindowMs &&
          distance <=
            config.doubleClickDistancePx;
      }

      clickHistoryRef.current.push(now);

      if (
        clickHistoryRef.current.length >
        MAX_CLICK_HISTORY
      ) {
        clickHistoryRef.current.shift();
      }

      const intervals = [];

      for (
        let i = 1;
        i < clickHistoryRef.current.length;
        i++
      ) {
        intervals.push(
          clickHistoryRef.current[i] -
            clickHistoryRef.current[i - 1]
        );
      }

      const rhythmVariance =
        variance(intervals);

      const clickEvent = {
        type: "click",
        x: event.clientX,
        y: event.clientY,
        target: describeTarget(event.target),
        pauseBeforeClickMs: Math.round(
          pauseBeforeClickMs
        ),
        isDoubleClick,
        rhythmVarianceMs:
          rhythmVariance === null
            ? null
            : Math.round(rhythmVariance),
        timestamp: Date.now(),
      };

      lastClickRef.current = {
        x: event.clientX,
        y: event.clientY,
        t: now,
      };

      onEvent(clickEvent);

      setState((previous) => ({
        lastClick: clickEvent,
        clickCount:
          previous.clickCount + 1,
      }));
    },
    [
      config.doubleClickWindowMs,
      config.doubleClickDistancePx,
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

    window.addEventListener(
      "click",
      handleClick,
      {
        passive: true,
      }
    );

    return () => {
      window.removeEventListener(
        "mousemove",
        handleMouseMove
      );

      window.removeEventListener(
        "click",
        handleClick
      );
    };
  }, [handleMouseMove, handleClick]);

  return state;
}

export default useClickPatterns;