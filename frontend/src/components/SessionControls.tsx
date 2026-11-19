import {
  useState,
} from "react";

import {
  useNavigate,
} from "react-router";

import {
  useAuth,
} from "../auth/authContext";


export default function SessionControls() {
  const {
    user,
    logout,
  } = useAuth();


  const navigate =
    useNavigate();


  const [
    loggingOut,
    setLoggingOut,
  ] = useState(false);


  const [
    error,
    setError,
  ] = useState<string | null>(
    null
  );


  if (!user) {
    return null;
  }


  async function handleLogout() {
    if (loggingOut) {
      return;
    }


    setError(null);
    setLoggingOut(true);


    try {
      await logout();


      navigate(
        "/login",
        {
          replace: true,
        },
      );
    } catch {
      setError(
        "Unable to sign out."
      );
    } finally {
      setLoggingOut(false);
    }
  }


  return (
    <aside
      className="session-controls"
      aria-label="User session"
    >
      <div
        className="session-controls__user"
      >
        <span>
          Signed in as
        </span>

        <strong>
          {user.username}
        </strong>
      </div>


      <button
        type="button"
        onClick={handleLogout}
        disabled={loggingOut}
      >
        {
          loggingOut
            ? "Signing out..."
            : "Sign out"
        }
      </button>


      {
        error
        && (
          <span
            className="session-controls__error"
            role="alert"
          >
            {error}
          </span>
        )
      }
    </aside>
  );
}
