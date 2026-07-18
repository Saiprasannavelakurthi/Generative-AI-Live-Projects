import React from 'react';

export default function ErrorPanel({ title, message }) {
  if (!message) return null;
  return (
    <div className="rounded-lg border border-red-300 bg-red-50 p-3 text-sm text-red-800">
      <p className="font-semibold">{title}</p>
      <pre className="mt-1 whitespace-pre-wrap font-mono text-xs">{message}</pre>
    </div>
  );
}
