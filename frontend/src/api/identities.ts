import type {
  CredentialExposure,
  Identity,
  IdentityAccess,
  IdentityLink,
  IdentityPropagationResult,
} from "../types/identity";


const API_BASE_URL =
  import.meta.env
    .VITE_API_BASE_URL
  ?? "http://127.0.0.1:8000/api";


async function jsonRequest<T>(
  path: string,

  options?: RequestInit,
): Promise<T> {
  const response =
    await fetch(
      `${API_BASE_URL}${path}`,

      {
        ...options,

        headers: {
          "Content-Type":
            "application/json",

          ...(options?.headers ?? {}),
        },
      },
    );


  if (!response.ok) {
    const data =
      await response.json();


    throw new Error(
      JSON.stringify(
        data
      )
    );
  }


  if (
    response.status
    === 204
  ) {
    return undefined as T;
  }


  return (
    await response.json()
  ) as T;
}


export function listIdentities(
  organizationId: number,
) {
  return jsonRequest<
    Identity[]
  >(
    (
      "/identities/"
      + `?organization=${organizationId}`
    ),
  );
}


export function createIdentity(
  payload:
    Omit<
      Identity,
      | "id"
      | "identity_type_display"
      | "privilege_level_display"
      | "created_at"
      | "updated_at"
    >,
) {
  return jsonRequest<
    Identity
  >(
    "/identities/",

    {
      method: "POST",

      body: JSON.stringify(
        payload
      ),
    },
  );
}


export function listCredentialExposures(
  organizationId: number,
) {
  return jsonRequest<
    CredentialExposure[]
  >(
    (
      "/credential-exposures/"
      + `?organization=${organizationId}`
    ),
  );
}


export function listIdentityAccess(
  organizationId: number,
) {
  return jsonRequest<
    IdentityAccess[]
  >(
    (
      "/identity-access/"
      + `?organization=${organizationId}`
    ),
  );
}


export function listIdentityLinks(
  organizationId: number,
) {
  return jsonRequest<
    IdentityLink[]
  >(
    (
      "/identity-links/"
      + `?organization=${organizationId}`
    ),
  );
}


export function runIdentityPropagation(
  payload: {
    organization:
      number;

    compromised_assets:
      Array<{
        asset_id:
          number;

        privilege:
          "LOW" | "HIGH";
      }>;
  },
) {
  return jsonRequest<
    IdentityPropagationResult
  >(
    "/simulations/identity-propagation/",

    {
      method: "POST",

      body: JSON.stringify(
        payload
      ),
    },
  );
}
