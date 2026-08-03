import React from 'react';

export default function StaticFallbackForm({ onRetry }) {
  return (
    <div className="rounded-lg border border-slate-200 bg-white p-4">
      <p className="mb-3 text-sm text-slate-500">
        The generated UI isn't ready yet — here's a basic form so you're not blocked.
      </p>
      <form className="flex flex-col gap-2" onSubmit={(e) => e.preventDefault()}>
        <input
          className="rounded-md border border-slate-300 px-3 py-2 text-sm"
          placeholder="Enter a value"
        />
        <button
          type="submit"
          className="rounded-md bg-slate-900 px-3 py-2 text-sm font-medium text-white"
        >
          Submit
        </button>
      </form>
      <button
        type="button"
        onClick={onRetry}
        className="mt-3 text-xs font-medium text-blue-600 hover:underline"
      >
        Retry generation
      </button>
    </div>
  );
}