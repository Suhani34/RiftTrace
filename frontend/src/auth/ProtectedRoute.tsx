import {
  Navigate,
} from "react-router";

import type {
  ReactNode,
} from "react";

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


  if (loading) {
    return (
      <div>
        Loading RiftTrace...
      </div>
    );
  }


  if (!user) {
    return (
      <Navigate
        to="/login"
        replace
      />
    );
  }


  return (
    <>
      {children}
    </>
  );
}
