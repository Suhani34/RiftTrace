import type {
  Asset,
  Organization,
} from "./models";

import type {
  BusinessProcess,
  DependencyLevel,
} from "./business";


export interface BusinessImpactPropagatedAsset {
  asset: Asset;

  privilege:
    "LOW"
    | "HIGH";

  hop_count: number;
}


export interface ImpactedBusinessProcess {
  business_process:
    BusinessProcess;

  strongest_dependency_level:
    DependencyLevel;

  affected_asset_ids:
    number[];

  affected_assets:
    Asset[];

  affected_dependency_ids:
    number[];
}


export interface BusinessImpactSummary {
  impacted_process_count:
    number;

  critical_process_count:
    number;

  essential_dependency_hit_count:
    number;
}


export interface BusinessImpactSimulationResult {
  simulation_type:
    "business_impact";

  organization:
    Organization;

  start_asset:
    Asset;

  start_privilege:
    "LOW"
    | "HIGH";

  technical_consequence: {
    affected_asset_ids:
      number[];

    propagated_asset_ids:
      number[];

    traversed_relationship_ids:
      number[];

    propagated_assets:
      BusinessImpactPropagatedAsset[];

    blocked_transition_count:
      number;
  };

  business_impact: {
    summary:
      BusinessImpactSummary;

    impacted_processes:
      ImpactedBusinessProcess[];
  };

  semantics: string;
}
