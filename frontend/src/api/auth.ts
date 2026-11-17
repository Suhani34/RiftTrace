import {
  ensureCsrf,
  getCsrfToken,
} from "./csrf";


export interface CurrentUser {
  id: number;

  username: string;

  email: string;

  is_superuser: boolean;

  memberships: Array<{
    organization_id: number;

    organization_name: string;

    role:
      "ADMIN"
      | "ANALYST"
      | "VIEWER";
  }>;
}


export async function loginUser(
  username: string,
  password: string,
) {
  await ensureCsrf();


  const csrf =
    getCsrfToken();


  const response =
    await fetch(
      "/api/auth/login/",
      {
        method: "POST",

        credentials:
          "include",

        headers: {
          "Content-Type":
            "application/json",

          "X-CSRFToken":
            csrf ?? "",
        },

        body: JSON.stringify({
          username,
          password,
        }),
      },
    );


  if (!response.ok) {
    throw new Error(
      "Invalid username or password."
    );
  }


  return response.json();
}


export async function getCurrentUser():
  Promise<CurrentUser> {
  const response =
    await fetch(
      "/api/auth/me/",
      {
        credentials:
          "include",
      },
    );


  if (!response.ok) {
    throw new Error(
      "Not authenticated."
    );
  }


  return response.json();
}


export async function logoutUser() {
  await ensureCsrf();


  const csrf =
    getCsrfToken();


  const response =
    await fetch(
      "/api/auth/logout/",
      {
        method: "POST",

        credentials:
          "include",

        headers: {
          "X-CSRFToken":
            csrf ?? "",
        },
      },
    );


  if (!response.ok) {
    throw new Error(
      "Unable to log out."
    );
  }
}
