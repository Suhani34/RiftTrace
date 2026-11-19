import {
  Component,
} from "react";

import type {
  ErrorInfo,
  ReactNode,
} from "react";


interface AppErrorBoundaryProps {
  children: ReactNode;
}


interface AppErrorBoundaryState {
  hasError: boolean;
}


export class AppErrorBoundary extends Component<
  AppErrorBoundaryProps,
  AppErrorBoundaryState
> {
  state: AppErrorBoundaryState = {
    hasError: false,
  };


  static getDerivedStateFromError():
    AppErrorBoundaryState {
    return {
      hasError: true,
    };
  }


  componentDidCatch(
    error: Error,
    info: ErrorInfo,
  ) {
    console.error(
      "RiftTrace frontend error:",
      error,
      info,
    );
  }


  private handleReload = () => {
    window.location.reload();
  };


  render() {
    if (
      this.state.hasError
    ) {
      return (
        <main
          className="app-error-page"
        >
          <section
            className={[
              "panel",
              "app-error-panel",
            ].join(" ")}
            role="alert"
          >
            <h1>
              RiftTrace encountered
              a problem
            </h1>

            <p>
              The current page could not
              be displayed safely.
            </p>

            <button
              type="button"
              onClick={
                this.handleReload
              }
            >
              Reload RiftTrace
            </button>
          </section>
        </main>
      );
    }


    return this.props.children;
  }
}
