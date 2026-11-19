import type {
  ReactNode,
} from "react";


interface PageStateProps {
  kind:
    | "loading"
    | "error"
    | "empty";

  title: string;

  message?: string;

  actionLabel?: string;

  onAction?: () => void;

  children?: ReactNode;
}


export default function PageState({
  kind,
  title,
  message,
  actionLabel,
  onAction,
  children,
}: PageStateProps) {
  const isError =
    kind === "error";


  return (
    <section
      className={[
        "panel",
        "page-state",
        `page-state--${kind}`,
      ].join(" ")}
      role={
        isError
          ? "alert"
          : "status"
      }
      aria-live={
        isError
          ? "assertive"
          : "polite"
      }
    >
      <h2
        className="page-state__title"
      >
        {title}
      </h2>


      {message && (
        <p
          className="page-state__message"
        >
          {message}
        </p>
      )}


      {children}


      {
        actionLabel
        && onAction
        && (
          <button
            type="button"
            onClick={onAction}
          >
            {actionLabel}
          </button>
        )
      }
    </section>
  );
}
