import React from 'react';

const STATUS_MAP = {
  idle: ['bg-slate-200 text-slate-600', 'Idle'],
  loading: ['bg-amber-100 text-amber-700', 'Downloading'],
  compiling: ['bg-blue-100 text-blue-700', 'Compiling'],
  ready: ['bg-emerald-100 text-emerald-700', 'Live'],
  error: ['bg-red-100 text-red-700', 'Error'],
};

export default function StatusBadge({ status }) {
  const [cls, label] = STATUS_MAP[status] || STATUS_MAP.idle;
  return (
    <span className={`inline-flex items-center gap-1.5 rounded-full px-2.5 py-1 text-xs font-medium ${cls}`}>
      <span className="h-1.5 w-1.5 rounded-full bg-current" />
      {label}
    </span>
  );
}
