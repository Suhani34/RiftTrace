import {
  ensureCsrf,
  getCsrfToken,
} from "./csrf";


const API_BASE_URL =
  import.meta.env.VITE_API_BASE_URL
  ?? "/api";


const SAFE_METHODS =
  new Set([
    "GET",
    "HEAD",
    "OPTIONS",
    "TRACE",
  ]);


export class ApiError extends Error {
  status: number;

  details: unknown;


  constructor(
    message: string,
    status: number,
    details: unknown,
  ) {
    super(message);

    this.name = "ApiError";

    this.status =
      status;

    this.details =
      details;
  }
}


function getErrorMessage(
  data: unknown,
  status: number,
): string {
  if (
    typeof data === "object"
    && data !== null
    && "detail" in data
  ) {
    const detail =
      (
        data as {
          detail?: unknown;
        }
      ).detail;


    if (
      typeof detail
      === "string"
    ) {
      return detail;
    }
  }


  if (
    typeof data === "string"
    && data.trim()
  ) {
    return data;
  }


  return (
    "API request failed with "
    + `status ${status}.`
  );
}


async function readResponseBody(
  response: Response,
): Promise<unknown> {
  const text =
    await response.text();


  if (!text) {
    return null;
  }


  const contentType =
    response.headers.get(
      "content-type"
    )
    ?? "";


  if (
    contentType.includes(
      "application/json"
    )
  ) {
    try {
      return JSON.parse(
        text
      );
    } catch {
      return text;
    }
  }


  return text;
}


export async function apiRequest<T>(
  path: string,
  options: RequestInit = {},
): Promise<T> {
  const method =
    (
      options.method
      ?? "GET"
    ).toUpperCase();


  const headers =
    new Headers(
      options.headers
    );


  headers.set(
    "Accept",
    "application/json",
  );


  if (
    options.body
    && !(
      options.body
      instanceof FormData
    )
    && !headers.has(
      "Content-Type"
    )
  ) {
    headers.set(
      "Content-Type",
      "application/json",
    );
  }


  if (
    !SAFE_METHODS.has(
      method
    )
  ) {
    await ensureCsrf();


    const csrfToken =
      getCsrfToken();


    if (csrfToken) {
      headers.set(
        "X-CSRFToken",
        csrfToken,
      );
    }
  }


  const response =
    await fetch(
      `${API_BASE_URL}${path}`,
      {
        ...options,

        method,

        credentials:
          "include",

        headers,
      },
    );


  if (
    response.status === 204
  ) {
    return undefined as T;
  }


  const data =
    await readResponseBody(
      response
    );


  if (!response.ok) {
    throw new ApiError(
      getErrorMessage(
        data,
        response.status,
      ),

      response.status,

      data,
    );
  }


  return data as T;
}
