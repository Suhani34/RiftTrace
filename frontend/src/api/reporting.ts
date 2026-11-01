import type {
  ReportingSummary,
} from "../types/reporting";


const API_BASE_URL =
  import.meta.env.VITE_API_BASE_URL
  ?? "http://127.0.0.1:8000/api";


async function getJson<T>(
  url: string,
): Promise<T> {
  const response =
    await fetch(
      url
    );


  if (!response.ok) {
    throw new Error(
      (
        "Reporting request failed "
        + `with ${response.status}.`
      )
    );
  }


  return (
    await response.json()
  ) as T;
}


export async function getReportingSummary(
  organizationId: number,
): Promise<ReportingSummary> {
  return getJson<
    ReportingSummary
  >(
    (
      `${API_BASE_URL}`
      + "/reporting/summary/"
      + `?organization=${organizationId}`
    ),
  );
}


export function getPortableEnvironmentUrl(
  organizationId: number,
): string {
  return (
    `${API_BASE_URL}`
    + "/reporting/environment/"
    + `${organizationId}/`
  );
}


export function getIngestionEnvironmentUrl(
  organizationId: number,
): string {
  return (
    `${API_BASE_URL}`
    + "/reporting/environment/"
    + `${organizationId}/ingestion/`
  );
}


export function getScenarioExportUrl(
  scenarioId: number,
): string {
  return (
    `${API_BASE_URL}`
    + "/reporting/scenarios/"
    + `${scenarioId}/`
  );
}


export function getRunReportUrl(
  runId: number,
): string {
  return (
    `${API_BASE_URL}`
    + "/reporting/runs/"
    + `${runId}/`
  );
}


export function getRunMetricsCsvUrl(
  runId: number,
): string {
  return (
    `${API_BASE_URL}`
    + "/reporting/runs/"
    + `${runId}/metrics.csv`
  );
}
