import React, { Component } from "react";

/**
 * Error Boundary for AI-generated React components.
 *
 * Prevents a broken generated component
 * from crashing the whole application.
 */

export default class RenderBoundary extends Component {
  constructor(props) {
    super(props);

    this.state = {
      error: null,
      errorInfo: null,
    };
  }

  static getDerivedStateFromError(error) {
    return {
      error,
    };
  }

  componentDidCatch(error, errorInfo) {
    this.setState({
      errorInfo,
    });

    if (this.props.onError) {
      this.props.onError(error, errorInfo);
    }
  }

  componentDidUpdate(previousProps) {
    if (previousProps.children !== this.props.children) {
      if (this.state.error) {
        this.setState({
          error: null,
          errorInfo: null,
        });
      }
    }
  }

  handleRetry = () => {
    this.setState({
      error: null,
      errorInfo: null,
    });

    if (this.props.onRetry) {
      this.props.onRetry();
    }
  };

  render() {
    if (this.state.error) {
      return (
        <div className="rounded-xl border border-red-200 bg-red-50 p-5">
          <h2 className="text-lg font-semibold text-red-700">
            Component crashed while rendering
          </h2>

          <p className="mt-3 rounded bg-red-100 p-3 font-mono text-sm text-red-800">
            {String(
              this.state.error.message ||
                this.state.error
            )}
          </p>

          {process.env.NODE_ENV ===
            "development" &&
            this.state.errorInfo && (
              <pre className="mt-4 overflow-auto rounded bg-slate-900 p-3 text-xs text-slate-100">
                {
                  this.state.errorInfo
                    .componentStack
                }
              </pre>
            )}

          {this.props.onRetry && (
            <button
              type="button"
              onClick={this.handleRetry}
              className="mt-5 rounded-md bg-red-600 px-4 py-2 text-sm font-medium text-white transition hover:bg-red-700"
            >
              Revert to Last Stable Version
            </button>
          )}
        </div>
      );
    }

    return this.props.children;
  }
}