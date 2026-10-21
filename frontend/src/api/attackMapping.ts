import type {
  AttackMappingEvaluation,
  AttackMappingRule,
  AttackTechnique,
} from "../types/attackMapping";


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


  return (
    await response.json()
  ) as T;
}


export function listAttackTechniques() {
  return jsonRequest<
    AttackTechnique[]
  >(
    "/attack/techniques/"
  );
}


export function listAttackMappingRules() {
  return jsonRequest<
    AttackMappingRule[]
  >(
    "/attack/rules/"
  );
}


export function evaluateAttackMapping(
  payload: {
    event_type: string;

    attributes: Record<
      string,
      unknown
    >;
  },
) {
  return jsonRequest<
    AttackMappingEvaluation
  >(
    "/attack/evaluate/",

    {
      method: "POST",

      body: JSON.stringify(
        payload
      ),
    },
  );
}
