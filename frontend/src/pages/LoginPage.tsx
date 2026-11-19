import {
  useState,
} from "react";

import type {
  FormEvent,
} from "react";

import {
  Navigate,
} from "react-router";

import {
  useAuth,
} from "../auth/authContext";


export default function LoginPage() {
  const {
    user,
    loading,
    login,
  } = useAuth();


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


  if (loading) {
    return (
      <main
        style={{
          maxWidth: "480px",
          margin: "80px auto",
          padding: "24px",
        }}
      >
        <section className="panel">
          <p>
            Loading RiftTrace...
          </p>
        </section>
      </main>
    );
  }


  if (user) {
    return (
      <Navigate
        to="/"
        replace
      />
    );
  }


  async function handleSubmit(
    event: FormEvent<HTMLFormElement>,
  ) {
    event.preventDefault();

    setError(null);
    setSubmitting(true);


    try {
      await login(
        username,
        password,
      );
    } catch {
      setError(
        "Unable to sign in. Check your username and password.",
      );
    } finally {
      setSubmitting(false);
    }
  }


  return (
    <main
      style={{
        maxWidth: "480px",
        margin: "80px auto",
        padding: "24px",
      }}
    >
      <section className="panel">
        <h1>
          RiftTrace
        </h1>

        <p>
          Sign in to continue.
        </p>


        {error && (
          <div
            role="alert"
            style={{
              marginBottom: "16px",
            }}
          >
            {error}
          </div>
        )}


        <form
          onSubmit={handleSubmit}
        >
          <div
            style={{
              marginBottom: "16px",
            }}
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
              onChange={(event) => {
                setUsername(
                  event.target.value
                );
              }}
              required
              disabled={submitting}
              style={{
                display: "block",
                width: "100%",
                marginTop: "6px",
              }}
            />
          </div>


          <div
            style={{
              marginBottom: "20px",
            }}
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
              autoComplete="current-password"
              value={password}
              onChange={(event) => {
                setPassword(
                  event.target.value
                );
              }}
              required
              disabled={submitting}
              style={{
                display: "block",
                width: "100%",
                marginTop: "6px",
              }}
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
