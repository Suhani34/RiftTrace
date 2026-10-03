import type {
  Asset,
  Organization,
  Relationship,
} from "./models";

import type {
  BusinessProcess,
  DependencyLevel,
} from "./business";

import type {
  Vulnerability,
} from "./security";


export interface CounterfactualPropagatedAsset {
  asset: Asset;

  privilege:
    "LOW"
    | "HIGH";

  hop_count: number;
}


export interface CounterfactualImpactedProcess {
  business_process:
    BusinessProcess;

  strongest_dependency_level:
    DependencyLevel;

  affected_asset_ids:
    number[];

  affected_assets:
    Asset[];
}


export interface CounterfactualRun {
  technical_consequence: {
    affected_asset_ids:
      number[];

    propagated_asset_ids:
      number[];

    propagated_asset_count:
      number;

    critical_asset_count:
      number;

    traversed_relationship_ids:
      number[];

    exploited_vulnerability_ids:
      number[];

    max_hops:
      number;

    propagated_assets:
      CounterfactualPropagatedAsset[];
  };

  business_impact: {
    summary: {
      impacted_process_count:
        number;

      critical_process_count:
        number;

      essential_dependency_hit_count:
        number;
    };

    impacted_processes:
      CounterfactualImpactedProcess[];
  };
}


export interface CounterfactualComparison {
  propagated_asset_reduction:
    number;

  critical_asset_reduction:
    number;

  impacted_process_reduction:
    number;

  critical_process_reduction:
    number;

  essential_dependency_hit_reduction:
    number;

  prevented_propagated_asset_ids:
    number[];

  prevented_propagated_assets:
    Asset[];

  prevented_critical_asset_ids:
    number[];

  prevented_critical_assets:
    Asset[];

  avoided_business_process_ids:
    number[];

  avoided_business_processes:
    BusinessProcess[];

  prevented_traversed_relationship_ids:
    number[];

  prevented_exploited_vulnerability_ids:
    number[];
}


export interface CounterfactualSimulationResult {
  simulation_type:
    "counterfactual_comparison";

  organization:
    Organization;

  start_asset:
    Asset;

  start_privilege:
    "LOW"
    | "HIGH";

  modifications: {
    disabled_relationships:
      Relationship[];

    disabled_vulnerabilities:
      Vulnerability[];
  };

  baseline:
    CounterfactualRun;

  counterfactual:
    CounterfactualRun;

  comparison:
    CounterfactualComparison;

  semantics:
    string;
}

