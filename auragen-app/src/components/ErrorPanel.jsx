import React from "react";

/**
 * Displays validation, compilation,
 * or runtime errors.
 */

export default function ErrorPanel({
  title = "Error",
  message,
}) {
  if (!message) {
    return null;
  }

  return (
    <div
      role="alert"
      className="rounded-xl border border-red-200 bg-red-50 p-4 shadow-sm"
    >
      <div className="flex items-start gap-3">
        <span className="text-xl">
          ⚠️
        </span>

        <div className="flex-1">
          <h3 className="text-sm font-semibold text-red-700">
            {title}
          </h3>

          <pre className="mt-2 max-h-64 overflow-auto whitespace-pre-wrap rounded-lg bg-red-100 p-3 font-mono text-xs text-red-800">
            {message}
          </pre>
        </div>
      </div>
    </div>
  );
}