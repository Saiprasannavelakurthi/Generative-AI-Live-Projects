import React from 'react';

const STATUS_MAP = {
  idle: ['bg-slate-100 text-slate-600 ring-slate-200', 'Idle'],
  loading: ['bg-amber-100 text-amber-700 ring-amber-200', 'Downloading'],
  compiling: ['bg-blue-100 text-blue-700 ring-blue-200', 'Compiling'],
  ready: ['bg-emerald-100 text-emerald-700 ring-emerald-200', 'Live'],
  error: ['bg-red-100 text-red-700 ring-red-200', 'Error'],
};

export default function StatusBadge({ status }) {
  const [cls, label] = STATUS_MAP[status] || STATUS_MAP.idle;
  const isPulsing = status === 'loading' || status === 'compiling';

  return (
    <span className={`inline-flex items-center gap-1.5 rounded-full px-3 py-1 text-xs font-semibold ring-1 ring-inset ${cls}`}>
      <span className={`h-1.5 w-1.5 rounded-full bg-current ${isPulsing ? 'animate-pulse' : ''}`} />
      {label}
    </span>
  );
}