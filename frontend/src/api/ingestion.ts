import type {
  IngestionApplyResult,
  IngestionPlan,
  IngestionRun,
} from "../types/ingestion";


const API_BASE_URL =
  import.meta.env
    .VITE_API_BASE_URL
  ?? "http://127.0.0.1:8000/api";


async function multipartRequest<T>(
  path: string,

  formData:
    FormData,
): Promise<T> {
  const response =
    await fetch(
      `${API_BASE_URL}${path}`,

      {
        method: "POST",

        body:
          formData,
      },
    );


  const data =
    await response.json();


  if (!response.ok) {
    const message =
      data.detail
      ?? data.parse_error
      ?? "Ingestion request failed.";


    throw new Error(
      typeof message
        === "string"
        ? message
        : JSON.stringify(
            message
          ),
    );
  }


  return data as T;
}


export function previewIngestion(
  formData:
    FormData,
) {
  return multipartRequest<
    IngestionPlan
  >(
    "/ingestion/preview/",

    formData,
  );
}


export function applyIngestion(
  formData:
    FormData,
) {
  return multipartRequest<
    IngestionApplyResult
  >(
    "/ingestion/apply/",

    formData,
  );
}


export async function listIngestionRuns(
  organizationId:
    number,
): Promise<IngestionRun[]> {
  const response =
    await fetch(
      (
        `${API_BASE_URL}`
        + "/ingestion/runs/"
        + `?organization=${organizationId}`
      ),
    );


  if (!response.ok) {
    throw new Error(
      "Unable to load ingestion history.",
    );
  }


  return (
    await response.json()
  ) as IngestionRun[];
}
