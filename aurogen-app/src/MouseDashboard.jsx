import useMouseAnalytics from "./useMouseAnalytics";

export default function MouseDashboard() {
  const metrics = useMouseAnalytics({
    websocketUrl: "ws://localhost:8080",
  });

  return (
    <div className="min-h-screen bg-slate-400 flex items-center justify-center p-8">
      <div className="w-full max-w-xl rounded-2xl bg-slate-800 shadow-2xl p-8">

        <h1 className="text-3xl font-bold text-white mb-8">
          Telemetry Tracker-Mouse Analytics
        </h1>

        <div className="grid grid-cols-2 gap-6">

          <div className="rounded-xl bg-slate-700 p-5">
            <p className="text-slate-400">Velocity</p>
            <h2 className="text-3xl font-bold text-cyan-400">
              {metrics.velocity.toFixed(1)}
            </h2>
            <p className="text-slate-500">px/sec</p>
          </div>

          <div className="rounded-xl bg-slate-700 p-5">
            <p className="text-slate-400">Acceleration</p>
            <h2 className="text-3xl font-bold text-green-400">
              {metrics.acceleration.toFixed(1)}
            </h2>
          </div>

          <div className="rounded-xl bg-slate-700 p-5">
            <p className="text-slate-400">Clicks</p>
            <h2 className="text-3xl font-bold text-yellow-400">
              {metrics.clicks}
            </h2>
          </div>

          <div className="rounded-xl bg-slate-700 p-5">
            <p className="text-slate-400">Hesitation</p>

            <span
              className={`inline-block px-4 py-2 rounded-full text-white font-semibold ${
                metrics.hesitation
                  ? "bg-red-500"
                  : "bg-emerald-500"
              }`}
            >
              {metrics.hesitation ? "Detected" : "Moving"}
            </span>
          </div>

        </div>
      </div>
    </div>
  );
}