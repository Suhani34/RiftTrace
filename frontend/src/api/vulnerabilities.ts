import {
  apiRequest,
} from "./client";

import type {
  CreateVulnerabilityInput,
  Vulnerability,
} from "../types/security";


export function listVulnerabilities(
  organizationId: number,
) {
  return apiRequest<
    Vulnerability[]
  >(
    "/vulnerabilities/"
    + `?organization=${organizationId}`,
  );
}


export function createVulnerability(
  input: CreateVulnerabilityInput,
) {
  return apiRequest<
    Vulnerability
  >(
    "/vulnerabilities/",
    {
      method: "POST",

      body: JSON.stringify(
        input,
      ),
    },
  );
}


export function deleteVulnerability(
  id: number,
) {
  return apiRequest<void>(
    `/vulnerabilities/${id}/`,
    {
      method: "DELETE",
    },
  );
}
