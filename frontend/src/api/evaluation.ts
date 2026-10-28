import type {
  CreateEvaluationExperimentPayload,
  EvaluationExperiment,
  EvaluationSummary,
} from "../types/evaluation";


const API_BASE_URL =
  import.meta.env.VITE_API_BASE_URL
  ?? "http://127.0.0.1:8000/api";


async function jsonRequest<T>(
  url: string,

  options?: RequestInit,
): Promise<T> {
  const response =
    await fetch(
      url,
      options,
    );


  const text =
    await response.text();


  if (!response.ok) {
    throw new Error(
      text
      || (
        `Request failed with `
        + `${response.status}`
      ),
    );
  }


  if (!text) {
    return undefined as T;
  }


  return JSON.parse(
    text
  ) as T;
}


export async function listEvaluationExperiments(
  organizationId: number,
): Promise<EvaluationExperiment[]> {
  return jsonRequest<
    EvaluationExperiment[]
  >(
    (
      `${API_BASE_URL}`
      + `/evaluation/experiments/`
      + `?organization=${organizationId}`
    ),
  );
}


export async function createEvaluationExperiment(
  payload:
    CreateEvaluationExperimentPayload,
): Promise<EvaluationExperiment> {
  return jsonRequest<
    EvaluationExperiment
  >(
    (
      `${API_BASE_URL}`
      + `/evaluation/experiments/`
    ),

    {
      method: "POST",

      headers: {
        "Content-Type":
          "application/json",
      },

      body:
        JSON.stringify(
          payload
        ),
    },
  );
}


export async function getEvaluationSummary(
  organizationId: number,
): Promise<EvaluationSummary> {
  return jsonRequest<
    EvaluationSummary
  >(
    (
      `${API_BASE_URL}`
      + `/evaluation/summary/`
      + `?organization=${organizationId}`
    ),
  );
}


export function getEvaluationExportUrl(
  organizationId: number,
): string {
  return (
    `${API_BASE_URL}`
    + `/evaluation/export.csv`
    + `?organization=${organizationId}`
  );
}
