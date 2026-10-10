import type {
  Asset,
  Organization,
} from "./models";

import type {
  CounterfactualComparison,
  CounterfactualRun,
} from "./counterfactual";

import type {
  SecurityControl,
} from "./securityControl";


export interface ControlReductionMetrics {
  critical_process_reduction:
    number;

  critical_asset_reduction:
    number;

  essential_dependency_hit_reduction:
    number;

  impacted_process_reduction:
    number;

  propagated_asset_reduction:
    number;
}


export interface RankedSecurityControl {
  rank: number;

  tied: boolean;

  has_measured_effect:
    boolean;

  control:
    SecurityControl;

  metrics:
    ControlReductionMetrics;

  priority_reason:
    string;

  controlled_scenario:
    CounterfactualRun;

  comparison:
    CounterfactualComparison;
}


export interface ControlRankingResult {
  simulation_type:
    "security_control_ranking";

  organization:
    Organization;

  start_asset:
    Asset;

  start_privilege:
    "LOW"
    | "HIGH";

  candidate_control_count:
    number;

  ranking_method: {
    strategy:
      string;

    priority_order:
      string[];

    tie_behavior:
      string;
  };

  baseline:
    CounterfactualRun;

  ranked_controls:
    RankedSecurityControl[];

  semantics:
    string;
}
