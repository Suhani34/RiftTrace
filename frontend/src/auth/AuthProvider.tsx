import {
  useEffect,
  useState,
  type ReactNode,
} from "react";

import {
  getCurrentUser,
  loginUser,
  logoutUser,
  type CurrentUser,
} from "../api/auth";

import {
  AuthContext,
} from "./authContext";


interface AuthProviderProps {
  children: ReactNode;
}


export function AuthProvider({
  children,
}: AuthProviderProps) {
  const [
    user,
    setUser,
  ] = useState<CurrentUser | null>(
    null,
  );

  const [
    loading,
    setLoading,
  ] = useState(true);


  useEffect(() => {
    async function loadUser() {
      try {
        const currentUser =
          await getCurrentUser();

        setUser(
          currentUser,
        );
      } catch {
        setUser(
          null,
        );
      } finally {
        setLoading(
          false,
        );
      }
    }


    void loadUser();
  }, []);


  async function login(
    username: string,
    password: string,
  ) {
    await loginUser(
      username,
      password,
    );


    const currentUser =
      await getCurrentUser();


    setUser(
      currentUser,
    );
  }


  async function logout() {
    await logoutUser();


    setUser(
      null,
    );
  }


  return (
    <AuthContext.Provider
      value={{
        user,
        loading,
        login,
        logout,
      }}
    >
      {children}
    </AuthContext.Provider>
  );
}
