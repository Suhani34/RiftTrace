import { apiRequest } from "./client";

import type {
  CreateOrganizationInput,
  Organization,
} from "../types/models";


export function listOrganizations() {
  return apiRequest<Organization[]>(
    "/organizations/",
  );
}


export function createOrganization(
  data: CreateOrganizationInput,
) {
  return apiRequest<Organization>(
    "/organizations/",
    {
      method: "POST",
      body: JSON.stringify(data),
    },
  );
}


export function deleteOrganization(
  organizationId: number,
) {
  return apiRequest<void>(
    `/organizations/${organizationId}/`,
    {
      method: "DELETE",
    },
  );
}
