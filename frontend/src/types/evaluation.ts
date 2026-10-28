import type {
  ScenarioMetricDifference,
} from "./scenarios";


export interface EvaluationExperiment {
  id: number;

  organization: number;

  organization_name: string;

  name: string;

  scenario: number;

  scenario_name: string;

  simulation_type: string;

  baseline_run: number;

  baseline_run_number: number;

  treatment_run: number;

  treatment_run_number: number;

  intervention_label: string;

  notes: string;

  comparison:
    ScenarioMetricDifference[];

  created_at: string;

  updated_at: string;
}


export interface CreateEvaluationExperimentPayload {
  organization: number;

  name: string;

  scenario: number;

  baseline_run: number;

  treatment_run: number;

  intervention_label: string;

  notes?: string;
}


export interface EvaluationSummaryMetric {
  metric: string;

  label: string;

  observations: number;

  mean_before: number;

  mean_after: number;

  mean_reduction: number;

  improved: number;

  worsened: number;

  unchanged: number;
}


export interface EvaluationSummary {
  experiment_count: number;

  metric_observation_count: number;

  improved_observations: number;

  worsened_observations: number;

  unchanged_observations: number;

  metrics:
    EvaluationSummaryMetric[];

  disclaimer: string;
}
