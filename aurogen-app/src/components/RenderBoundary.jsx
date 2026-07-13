import React, { Component } from 'react';

/**
 * RenderBoundary
 * --------------
 * Catches runtime errors thrown by a dynamically compiled component so a
 * bad component shows an inline error instead of crashing the host app.
 * Pass a changing `key` prop from the parent to reset it after a rebuild.
 */
export default class RenderBoundary extends Component {
  constructor(props) {
    super(props);
    this.state = { error: null };
  }

  static getDerivedStateFromError(error) {
    return { error };
  }

  componentDidCatch(error, info) {
    this.props.onError?.(error, info);
  }

  render() {
    if (this.state.error) {
      return (
        <div className="rounded-lg border border-red-300 bg-red-50 p-4 text-sm text-red-800">
          <p className="font-semibold">Component crashed while rendering</p>
          <pre className="mt-2 whitespace-pre-wrap font-mono text-xs text-red-700">
            {String(this.state.error?.message || this.state.error)}
          </pre>
        </div>
      );
    }
    return this.props.children;
  }
}
