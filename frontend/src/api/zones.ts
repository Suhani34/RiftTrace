import { apiRequest } from "./client";

import type {
  CreateNetworkZoneInput,
  NetworkZone,
} from "../types/models";


export function listZones(
  organizationId?: number,
) {
  const query = organizationId
    ? `?organization=${organizationId}`
    : "";

  return apiRequest<NetworkZone[]>(
    `/zones/${query}`,
  );
}


export function createZone(
  data: CreateNetworkZoneInput,
) {
  return apiRequest<NetworkZone>(
    "/zones/",
    {
      method: "POST",
      body: JSON.stringify(data),
    },
  );
}


export function deleteZone(
  zoneId: number,
) {
  return apiRequest<void>(
    `/zones/${zoneId}/`,
    {
      method: "DELETE",
    },
  );
}
