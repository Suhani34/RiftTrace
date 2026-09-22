import { apiRequest } from "./client";

import type {
  CreateRelationshipInput,
  Relationship,
} from "../types/models";


export function listRelationships(
  organizationId?: number,
) {
  const query = organizationId
    ? `?organization=${organizationId}`
    : "";

  return apiRequest<Relationship[]>(
    `/relationships/${query}`,
  );
}


export function createRelationship(
  data: CreateRelationshipInput,
) {
  return apiRequest<Relationship>(
    "/relationships/",
    {
      method: "POST",
      body: JSON.stringify(data),
    },
  );
}


export function deleteRelationship(
  relationshipId: number,
) {
  return apiRequest<void>(
    `/relationships/${relationshipId}/`,
    {
      method: "DELETE",
    },
  );
}
