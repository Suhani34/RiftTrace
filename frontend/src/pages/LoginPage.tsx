import {
  useState,
} from "react";

import type {
  FormEvent,
} from "react";

import {
  Navigate,
  useLocation,
  useNavigate,
} from "react-router";

import {
  useAuth,
} from "../auth/authContext";


interface LoginLocationState {
  from?: string;
}


export default function LoginPage() {
  const {
    user,
    loading,
    login,
  } = useAuth();


  const location =
    useLocation();

  const navigate =
    useNavigate();


  const state = location.state as LoginLocationState | null;


  const requestedPath =
    state?.from;


  const destination =
    (
      requestedPath
      && requestedPath.startsWith(
        "/"
      )
    )
      ? requestedPath
      : "/";


  const [
    username,
    setUsername,
  ] = useState("");


  const [
    password,
    setPassword,
  ] = useState("");


  const [
    error,
    setError,
  ] = useState<string | null>(
    null
  );


  const [
    submitting,
    setSubmitting,
  ] = useState(false);


  if (
    !loading
    && user
  ) {
    return (
      <Navigate
        to={destination}
        replace
      />
    );
  }


  async function handleSubmit(
    event:
      FormEvent<HTMLFormElement>,
  ) {
    event.preventDefault();


    if (submitting) {
      return;
    }


    setError(null);
    setSubmitting(true);


    try {
      await login(
        username.trim(),
        password,
      );


      navigate(
        destination,
        {
          replace: true,
        },
      );
    } catch {
      setError(
        (
          "Unable to sign in. "
          + "Check your username "
          + "and password."
        ),
      );
    } finally {
      setSubmitting(false);
    }
  }


  return (
    <main
      className="login-page"
    >
      <section
        className={[
          "panel",
          "login-card",
        ].join(" ")}
      >
        <header
          className="login-card__header"
        >
          <h1>
            RiftTrace
          </h1>

          <p>
            Sign in to continue to
            your cyber-risk environment.
          </p>
        </header>


        {
          error
          && (
            <p
              className="form-error"
              role="alert"
              aria-live="assertive"
            >
              {error}
            </p>
          )
        }


        <form
          onSubmit={handleSubmit}
        >
          <div
            className="form-field"
          >
            <label
              htmlFor="username"
            >
              Username
            </label>

            <input
              id="username"
              name="username"
              type="text"
              autoComplete="username"
              value={username}
              onChange={
                (
                  event
                ) => {
                  setUsername(
                    event.target.value
                  );
                }
              }
              required
              disabled={submitting}
              autoFocus
            />
          </div>


          <div
            className="form-field"
          >
            <label
              htmlFor="password"
            >
              Password
            </label>

            <input
              id="password"
              name="password"
              type="password"
              autoComplete={
                "current-password"
              }
              value={password}
              onChange={
                (
                  event
                ) => {
                  setPassword(
                    event.target.value
                  );
                }
              }
              required
              disabled={submitting}
            />
          </div>


          <button
            type="submit"
            disabled={submitting}
          >
            {
              submitting
                ? "Signing in..."
                : "Sign in"
            }
          </button>
        </form>
      </section>
    </main>
  );
}
