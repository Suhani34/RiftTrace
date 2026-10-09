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


export interface AppliedControlModifications {
  disabled_relationship_ids:
    number[];

  disabled_vulnerability_ids:
    number[];

  force_authentication_relationship_ids:
    number[];

  force_mfa_relationship_ids:
    number[];

  high_privilege_relationship_ids:
    number[];
}


export interface SecurityControlSimulationResult {
  simulation_type:
    "security_control_comparison";

  organization:
    Organization;

  start_asset:
    Asset;

  start_privilege:
    "LOW"
    | "HIGH";

  applied_controls:
    SecurityControl[];

  applied_modifications:
    AppliedControlModifications;

  baseline:
    CounterfactualRun;

  counterfactual:
    CounterfactualRun;

  comparison:
    CounterfactualComparison;

  semantics:
    string;
}
