const API_BASE_URL =
  import.meta.env.VITE_API_BASE_URL ??
  "http://127.0.0.1:8000/api";


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
    this.status = status;
    this.details = details;
  }
}


export async function apiRequest<T>(
  path: string,
  options: RequestInit = {},
): Promise<T> {
  const response = await fetch(
    `${API_BASE_URL}${path}`,
    {
      ...options,

      headers: {
        "Content-Type": "application/json",
        ...options.headers,
      },
    },
  );

  if (response.status === 204) {
    return undefined as T;
  }

  const text = await response.text();

  let data: unknown = null;

  if (text) {
    try {
      data = JSON.parse(text);
    } catch {
      data = text;
    }
  }

  if (!response.ok) {
    throw new ApiError(
      `API request failed with status ${response.status}`,
      response.status,
      data,
    );
  }

  return data as T;
}
