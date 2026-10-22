import type {
  CreateScenarioPayload,
  CreateScenarioRunPayload,
  SavedScenario,
  ScenarioComparison,
  ScenarioRun,
  SimulationType,
} from "../types/scenarios";


const API_BASE_URL =
  import.meta.env.VITE_API_BASE_URL
  ?? "http://127.0.0.1:8000/api";


async function jsonRequest<T>(
  url: string,

  options?: RequestInit,
): Promise<T> {
  const response =
    await fetch(
      url,
      options,
    );


  const text =
    await response.text();


  if (!response.ok) {
    throw new Error(
      text
      || (
        `Request failed with `
        + `${response.status}`
      ),
    );
  }


  if (!text) {
    return undefined as T;
  }


  return JSON.parse(
    text
  ) as T;
}


export async function listScenarios(
  organizationId?: number,
): Promise<SavedScenario[]> {
  const query =
    organizationId
      ? (
          `?organization=`
          + `${organizationId}`
        )
      : "";


  return jsonRequest<
    SavedScenario[]
  >(
    `${API_BASE_URL}/scenarios/${query}`,
  );
}


export async function createScenario(
  payload:
    CreateScenarioPayload,
): Promise<SavedScenario> {
  return jsonRequest<
    SavedScenario
  >(
    `${API_BASE_URL}/scenarios/`,

    {
      method: "POST",

      headers: {
        "Content-Type":
          "application/json",
      },

      body:
        JSON.stringify(
          payload
        ),
    },
  );
}


export async function listScenarioRuns(
  scenarioId: number,
): Promise<ScenarioRun[]> {
  return jsonRequest<
    ScenarioRun[]
  >(
    (
      `${API_BASE_URL}/scenarios/`
      + `${scenarioId}/runs/`
    ),
  );
}


export async function createScenarioRun(
  scenarioId: number,

  payload:
    CreateScenarioRunPayload,
): Promise<ScenarioRun> {
  return jsonRequest<
    ScenarioRun
  >(
    (
      `${API_BASE_URL}/scenarios/`
      + `${scenarioId}/runs/`
    ),

    {
      method: "POST",

      headers: {
        "Content-Type":
          "application/json",
      },

      body:
        JSON.stringify(
          payload
        ),
    },
  );
}


export async function compareScenarioRuns(
  scenarioId: number,

  beforeRunId: number,

  afterRunId: number,
): Promise<ScenarioComparison> {
  return jsonRequest<
    ScenarioComparison
  >(
    (
      `${API_BASE_URL}/scenarios/`
      + `${scenarioId}/compare/`
      + `?before_run=${beforeRunId}`
      + `&after_run=${afterRunId}`
    ),
  );
}


const SIMULATION_ENDPOINTS:
  Record<
    SimulationType,
    string
  > = {
    REACHABILITY:
      "/simulations/reachability/",

    ATTACK_PROPAGATION:
      "/simulations/attack-propagation/",

    BUSINESS_IMPACT:
      "/simulations/business-impact/",

    COUNTERFACTUAL:
      "/simulations/counterfactual/",

    SECURITY_CONTROL:
      "/simulations/security-controls/",

    CONTROL_RANKING:
      "/simulations/control-ranking/",

    IDENTITY_PROPAGATION:
      "/simulations/identity-propagation/",
  };


export async function executeSavedScenario(
  scenario:
    SavedScenario,
): Promise<unknown> {
  const endpoint =
    SIMULATION_ENDPOINTS[
      scenario.simulation_type
    ];


  return jsonRequest<unknown>(
    `${API_BASE_URL}${endpoint}`,

    {
      method: "POST",

      headers: {
        "Content-Type":
          "application/json",
      },

      body:
        JSON.stringify(
          scenario.request_payload
        ),
    },
  );
}
