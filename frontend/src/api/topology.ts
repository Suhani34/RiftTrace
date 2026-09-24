import { apiRequest } from "./client";

import type {
  OrganizationTopology,
} from "../types/models";


export function getOrganizationTopology(
  organizationId: number,
) {
  return apiRequest<OrganizationTopology>(
    `/organizations/${organizationId}/topology/`,
  );
}
