import {
  Navigate,
  useLocation,
} from "react-router";

import type {
  ReactNode,
} from "react";

import PageState
  from "../components/PageState";

import {
  useAuth,
} from "./authContext";


interface ProtectedRouteProps {
  children: ReactNode;
}


export function ProtectedRoute({
  children,
}: ProtectedRouteProps) {
  const {
    user,
    loading,
  } = useAuth();


  const location =
    useLocation();


  if (loading) {
    return (
      <main
        className="auth-loading-page"
      >
        <PageState
          kind="loading"
          title="Loading RiftTrace"
          message={
            "Checking your authenticated session."
          }
        />
      </main>
    );
  }


  if (!user) {
    return (
      <Navigate
        to="/login"
        replace
        state={{
          from:
            location.pathname
            + location.search,
        }}
      />
    );
  }


  return (
    <>
      {children}
    </>
  );
}
