export type SimulationType =
  | "REACHABILITY"
  | "ATTACK_PROPAGATION"
  | "BUSINESS_IMPACT"
  | "COUNTERFACTUAL"
  | "SECURITY_CONTROL"
  | "CONTROL_RANKING"
  | "IDENTITY_PROPAGATION";


export type ScenarioRunStatus =
  | "SUCCESS"
  | "FAILED";


export interface SavedScenario {
  id: number;

  organization: number;

  organization_name: string;

  name: string;

  simulation_type:
    SimulationType;

  description: string;

  request_payload:
    Record<string, unknown>;

  run_count: number;

  latest_run_number:
    number | null;

  latest_run_at:
    string | null;

  created_at: string;

  updated_at: string;
}


export interface ScenarioRun {
  id: number;

  scenario: number;

  scenario_name: string;

  run_number: number;

  label: string;

  status:
    ScenarioRunStatus;

  request_payload:
    Record<string, unknown>;

  result_payload: unknown;

  metrics:
    Record<string, number>;

  error_message: string;

  created_at: string;
}


export interface CreateScenarioPayload {
  organization: number;

  name: string;

  simulation_type:
    SimulationType;

  description: string;

  request_payload:
    Record<string, unknown>;
}


export interface CreateScenarioRunPayload {
  label?: string;

  status?:
    ScenarioRunStatus;

  request_payload?:
    Record<string, unknown>;

  result_payload?: unknown;

  metrics?:
    Record<string, number>;

  error_message?: string;
}


export interface ScenarioMetricDifference {
  metric: string;

  label: string;

  before: number;

  after: number;

  delta: number;

  reduction: number;

  interpretation:
    | "IMPROVED"
    | "WORSENED"
    | "UNCHANGED";
}


export interface ScenarioComparison {
  scenario: {
    id: number;

    name: string;

    simulation_type:
      SimulationType;
  };

  before_run:
    ScenarioRun;

  after_run:
    ScenarioRun;

  metrics:
    ScenarioMetricDifference[];

  disclaimer: string;
}
