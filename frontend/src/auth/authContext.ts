import {
  createContext,
  useContext,
} from "react";

import type {
  CurrentUser,
} from "../api/auth";


export interface AuthContextValue {
  user: CurrentUser | null;

  loading: boolean;

  login: (
    username: string,
    password: string,
  ) => Promise<void>;

  logout: () => Promise<void>;
}


export const AuthContext =
  createContext<AuthContextValue | null>(
    null,
  );


export function useAuth() {
  const context =
    useContext(
      AuthContext,
    );


  if (context === null) {
    throw new Error(
      "useAuth must be used inside AuthProvider.",
    );
  }


  return context;
}
