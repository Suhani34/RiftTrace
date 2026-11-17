export function getCsrfToken():
  string | null {
  const name =
    "csrftoken=";

  const cookies =
    document.cookie.split(";");


  for (
    const rawCookie
    of cookies
  ) {
    const cookie =
      rawCookie.trim();


    if (
      cookie.startsWith(
        name
      )
    ) {
      return decodeURIComponent(
        cookie.substring(
          name.length
        )
      );
    }
  }


  return null;
}


export async function ensureCsrf():
  Promise<void> {
  const response =
    await fetch(
      "/api/auth/csrf/",
      {
        method: "GET",

        credentials:
          "include",
      },
    );


  if (!response.ok) {
    throw new Error(
      "Unable to initialize CSRF."
    );
  }
}
