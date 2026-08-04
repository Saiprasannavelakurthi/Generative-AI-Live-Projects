# AuraGen — Self-Healing Generative UI (Frontend)

Frontend for the AuraGen project: tracks mouse telemetry (velocity, hesitation,
click patterns), streams it to the backend over WebSockets, displays the live
Cognitive Load Score, and renders LLM-generated React components in-browser
with a morphing transition and graceful fallback if generation fails.

## Status: Weeks 1–4 complete (frontend)

| Week | Deliverable | Status |
|---|---|---|
| 1 | Telemetry tracker (velocity, hesitation, clicks) over WebSockets | ✅ |
| 2 | Dynamic in-browser code compile + render | ✅ |
| 3 | Morphing transition (Framer Motion) between static/generated UI | ✅ |
| 4 | Fallback states + graceful degradation on bad/failed generation | ✅ |

Cognitive Load Score display and generation triggering depend on backend
thresholds (`Auragen_backend`) — see Known Issues below.

## Project structure
```
auragen-app/
├── src/
│ ├── hooks/
│ │ ├── useTelemetrySocket.js WebSocket transport, batching, reconnect, backend message handling
│ │ ├── useMouseVelocityAndHesitation.js Cursor velocity + hesitation detection
│ │ ├── useClickPatterns.js Click rhythm, double-click, pause-before-click
│ │ └── useMouseTelemetry.js Composes the above into one hook
│ ├── components/
│ │ ├── DynamicCodeRenderer.jsx Orchestrates compile/render/fallback, wraps TransitionShell
│ │ ├── TransitionShell.jsx Framer Motion crossfade between static/generated/error views
│ │ ├── RenderBoundary.jsx Runtime error boundary, reverts to last stable version
│ │ ├── StaticFallbackForm.jsx Safe default UI shown when generation fails and no prior version exists
│ │ ├── CognitiveLoadMeter.jsx Live Cognitive Load Score bar (driven by backend's high_load flag)
│ │ ├── StatusBadge.jsx Idle/downloading/compiling/live/error pill
│ │ ├── ErrorPanel.jsx Reusable error display
│ │ ├── CodeEditorPanel.jsx Manual code textarea + "Run this code" (for testing without backend)
│ │ └── TelemetryReadout.jsx Header widget: connection status, velocity, clicks, cognitive load
│ └── utils/
│ └── babelLoader.js Lazy-loads Babel standalone, compiles source string -> Component
└── App.jsx Wires useMouseTelemetry + DynamicCodeRenderer together
```
## Setup

```bash
npm install
npm run dev
```
Runs on http://localhost:5173. Requires the backend running separately
(`uvicorn app:app --reload` from `Auragen_backend`, with its venv active)
so the WebSocket at `ws://127.0.0.1:8000/ws` (set in `App.jsx`) has
something to connect to.

## Testing without the backend

Expand **"Edit source manually"** in the UI and paste a component directly —
useful for testing the compiler, TransitionShell animation, and fallback
states without waiting on a live LLM generation:

```jsx
function Demo() {
  return <div className="p-4 text-lg">Hello from generated UI</div>;
}
```

## Wire message schema (backend → frontend)

```json
{ "type": "cognitive_score", "score": 0.42, "high_load": false }
{ "type": "generated_component", "code": "function Demo() { ... }" }
```

## Wire message schema (frontend → backend)

```json
{
  "type": "telemetry_batch",
  "sentAt": 1731000000000,
  "events": [
    { "type": "move", "x": 412, "y": 220, "velocity": 0.83, "timestamp": 1731000000010 },
    { "type": "hesitation", "x": 412, "y": 220, "durationMs": 540, "timestamp": 1731000000550 },
    {
      "type": "click",
      "x": 412,
      "y": 220,
      "target": "button#submit.btn.btn-primary",
      "pauseBeforeClickMs": 180,
      "isDoubleClick": false,
      "rhythmVarianceMs": 340,
      "timestamp": 1731000000700
    }
  ]
}
```
Clicks flush immediately; moves/hesitations batch on `batchIntervalMs`. While
disconnected, events queue in a bounded backlog
(`maxBatchSize * maxQueuedBatches`) and reconnects use exponential backoff
up to `reconnectMaxDelayMs`.

## Known issues / backend-dependent

- Cognitive Load Score's numeric scale is backend-defined (not a clean 0–1
  fraction) — the meter currently trusts the backend's `high_load` boolean
  for color/label rather than the raw score value.
- UI generation only triggers once the backend flips `high_load: true`;
  during testing this threshold has rarely fired even under simulated
  rage-clicks/hesitation, so tuning is pending on the backend side.

## Security note

`DynamicCodeRenderer` evaluates code returned by the backend via
`new Function(...)` after Babel compilation. Only point this at a backend
you control — for untrusted/user-submitted code, sandbox in an `<iframe>`
instead.
