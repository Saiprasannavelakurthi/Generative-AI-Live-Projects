import React from "react";

/**
 * Static fallback UI shown when:
 * - AI generation is still running
 * - Component compilation fails
 * - Runtime rendering fails
 */

export default function StaticFallbackForm({
  onRetry,
}) {
  return (
    <div className="rounded-xl border border-slate-200 bg-white p-6 shadow-sm">
      <div className="mb-5 text-center">
        <div className="mb-3 text-5xl">
          🧠
        </div>

        <h2 className="text-lg font-semibold text-slate-800">
          Loading Adaptive Interface
        </h2>

        <p className="mt-2 text-sm text-slate-500">
          The AI-generated interface is not
          available yet. You can continue using
          this temporary form while the new UI is
          being prepared.
        </p>
      </div>

      <form
        className="space-y-4"
        onSubmit={(event) =>
          event.preventDefault()
        }
      >
        <div>
          <label className="mb-2 block text-sm font-medium text-slate-700">
            Name
          </label>

          <input
            type="text"
            placeholder="Enter your name"
            className="w-full rounded-lg border border-slate-300 px-3 py-2 focus:border-blue-500 focus:outline-none"
          />
        </div>

        <div>
          <label className="mb-2 block text-sm font-medium text-slate-700">
            Email
          </label>

          <input
            type="email"
            placeholder="Enter your email"
            className="w-full rounded-lg border border-slate-300 px-3 py-2 focus:border-blue-500 focus:outline-none"
          />
        </div>

        <button
          type="submit"
          className="w-full rounded-lg bg-slate-900 py-2 font-medium text-white transition hover:bg-slate-800"
        >
          Continue
        </button>
      </form>

      {onRetry && (
        <button
          type="button"
          onClick={onRetry}
          className="mt-5 w-full rounded-lg border border-blue-500 px-4 py-2 text-sm font-medium text-blue-600 transition hover:bg-blue-50"
        >
          🔄 Retry AI Generation
        </button>
      )}
    </div>
  );
}