import { apiRequest } from "./client";

import type {
  Asset,
  CreateAssetInput,
} from "../types/models";


export function listAssets(
  organizationId?: number,
) {
  const query = organizationId
    ? `?organization=${organizationId}`
    : "";

  return apiRequest<Asset[]>(
    `/assets/${query}`,
  );
}


export function createAsset(
  data: CreateAssetInput,
) {
  return apiRequest<Asset>(
    "/assets/",
    {
      method: "POST",
      body: JSON.stringify(data),
    },
  );
}


export function deleteAsset(
  assetId: number,
) {
  return apiRequest<void>(
    `/assets/${assetId}/`,
    {
      method: "DELETE",
    },
  );
}
