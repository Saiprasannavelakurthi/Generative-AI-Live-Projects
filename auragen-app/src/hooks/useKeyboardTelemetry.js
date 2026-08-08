import { useEffect, useRef } from "react";

/**
 * Custom React hook to collect keyboard interaction telemetry:
 * - Backspace count (indicates hesitation or form confusion)
 * - Typing pauses (> 1.5s while actively typing in a field)
 * - Typing velocity (keys per second)
 */
export function useKeyboardTelemetry({ enqueue }) {
  const backspaceCountRef = useRef(0);
  const lastKeyTimeRef = useRef(0);
  const pauseTimerRef = useRef(null);

  useEffect(() => {
    if (typeof window === "undefined" || !enqueue) return;

    const handleKeyDown = (event) => {
      const targetTag = event.target?.tagName?.toLowerCase();
      const isInput = targetTag === "input" || targetTag === "textarea";

      const now = Date.now();
      lastKeyTimeRef.current = now;

      if (event.key === "Backspace") {
        backspaceCountRef.current += 1;
      }

      if (pauseTimerRef.current) {
        clearTimeout(pauseTimerRef.current);
      }

      if (isInput) {
        // Schedule pause check: if user stops typing for > 1.5 seconds inside an input
        pauseTimerRef.current = setTimeout(() => {
          enqueue({
            type: "keyboard",
            user_action: "typing_hesitation",
            hesitation: true,
            pause_ms: 1500,
            backspaces: backspaceCountRef.current,
            target_field: event.target.id || event.target.name || "input",
            timestamp: Date.now(),
          });
          // Reset backspace tracker after emitting hesitation
          backspaceCountRef.current = 0;
        }, 1500);

        // If high backspace burst (> 3 backspaces)
        if (backspaceCountRef.current >= 3) {
          enqueue({
            type: "keyboard",
            user_action: "backspace_burst",
            hesitation: true,
            backspaces: backspaceCountRef.current,
            target_field: event.target.id || event.target.name || "input",
            timestamp: Date.now(),
          });
          backspaceCountRef.current = 0;
        }
      }
    };

    window.addEventListener("keydown", handleKeyDown);

    return () => {
      window.removeEventListener("keydown", handleKeyDown);
      if (pauseTimerRef.current) {
        clearTimeout(pauseTimerRef.current);
      }
    };
  }, [enqueue]);
}

export default useKeyboardTelemetry;
