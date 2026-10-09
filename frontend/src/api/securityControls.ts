import {
  apiRequest,
} from "./client";

import type {
  CreateSecurityControlInput,
  SecurityControl,
} from "../types/securityControl";


export function listSecurityControls(
  organizationId: number,
) {
  return apiRequest<
    SecurityControl[]
  >(
    "/security-controls/"
    + `?organization=${organizationId}`,
  );
}


export function createSecurityControl(
  input:
    CreateSecurityControlInput,
) {
  return apiRequest<
    SecurityControl
  >(
    "/security-controls/",

    {
      method: "POST",

      body: JSON.stringify(
        input,
      ),
    },
  );
}


export function deleteSecurityControl(
  id: number,
) {
  return apiRequest<void>(
    `/security-controls/${id}/`,

    {
      method: "DELETE",
    },
  );
}
