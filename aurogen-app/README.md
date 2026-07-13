
# Mouse Telemetry + Dynamic Component Kit (separated components)

Same functionality as before, decomposed into single-responsibility hooks
and components instead of two large files.

```
mouse-telemetry-kit-v2/
├── hooks/
│   ├── useTelemetrySocket.js            WebSocket transport: buffering, batching, reconnect
│   ├── useMouseVelocityAndHesitation.js Cursor velocity + hesitation detection
│   ├── useClickPatterns.js              Click rhythm, double-click, pause-before-click
│   └── useMouseTelemetry.js             Composes the three above into one hook
├── components/
│   ├── RenderBoundary.jsx               Error boundary around the compiled component
│   ├── StatusBadge.jsx                  Idle/downloading/compiling/live/error pill
│   ├── ErrorPanel.jsx                   Reusable error display
│   ├── CodeEditorPanel.jsx              Manual code textarea + "Run this code"
│   ├── DynamicCodeRenderer.jsx          Orchestrates the above into the rendering shell
│   └── TelemetryReadout.jsx             Small header widget for the demo app
├── utils/
│   └── babelLoader.js                   Lazy-loads Babel standalone + compiles source -> Component
└── App.example.jsx                      Wires useMouseTelemetry + DynamicCodeRenderer together
```

Tailwind is assumed to already be configured in your app (CDN Play script
or a normal build-time config both work).

## Why split it up

- `useTelemetrySocket` has zero knowledge of mice — it just buffers and
  ships whatever events it's given. You could reuse it for keyboard or
  scroll telemetry.
- `useMouseVelocityAndHesitation` and `useClickPatterns` each own one
  `window` listener setup and are independently testable/importable.
- `useMouseTelemetry` is the only place that wires them together — swap
  in a different transport or drop click tracking by editing one file.
- `DynamicCodeRenderer` no longer owns any markup for status/errors/editing
  directly; each piece is its own component, easy to reskin or replace.

## `useMouseTelemetry(options)`

```js
const telemetry = useMouseTelemetry({
  wsUrl: 'wss://api.example.com/telemetry', // omit/null to track locally without streaming
  batchIntervalMs: 500,
  maxBatchSize: 50,
  hesitationVelocityThreshold: 0.05, // px/ms
  hesitationMinDurationMs: 300,
  doubleClickWindowMs: 400,
  doubleClickDistancePx: 12,
});
```

Returns `{ x, y, velocity, isHesitating, lastClick, clickCount, connectionStatus, flushNow }`.

### Wire message schema

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

Clicks flush immediately; moves/hesitations batch on `batchIntervalMs`.
While disconnected, events queue in a bounded backlog
(`maxBatchSize * maxQueuedBatches`) and reconnects use exponential backoff
up to `reconnectMaxDelayMs`.

## `DynamicCodeRenderer`

```jsx
<DynamicCodeRenderer
  sourceUrl="https://your-code-host.example.com/latest-component.jsx"
  pollIntervalMs={5000}       // 0 = fetch once, no polling
  scope={{ telemetry }}       // extra values available inside the compiled code
/>
```

The downloaded (or pasted) source must assign the root component to a
top-level `Component` identifier:

```jsx
const Component = () => (
  <div className="p-4 text-sm text-slate-700">
    Hello from a dynamically compiled component
  </div>
);
```

`utils/babelLoader.js` lazy-loads Babel standalone from a CDN, transforms
the string with the `react` and `env` presets, then wraps the result in
`new Function(...)` to extract `Component`. `React` and anything in
`scope` are passed in as arguments, so the code can use them without an
`import`.

**Security note:** this evaluates arbitrary JS — the same trust model as
any in-browser playground. Only point `sourceUrl` at code you control or
trust. For user-submitted code, isolate it inside a sandboxed `<iframe>`
rather than compiling it directly in the host page.
