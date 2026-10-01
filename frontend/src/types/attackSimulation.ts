import type {
  Asset,
  Organization,
} from "./models";

import type {
  Vulnerability,
} from "./security";


export interface AttackPropagationSummary {
  total_assets: number;

  propagated_asset_count: number;

  propagated_critical_asset_count:
    number;

  max_hops: number;

  blocked_transition_count:
    number;
}


export interface PropagatedAsset {
  asset: Asset;

  privilege:
    "LOW"
    | "HIGH";

  hop_count: number;

  path_asset_ids: number[];

  path_asset_names: string[];

  path_relationship_ids:
    number[];

  via_vulnerability:
    Vulnerability
    | null;
}


export interface BlockedTransition {
  relationship_id: number;

  source_asset_id: number;
  source_asset_name: string;

  target_asset_id: number;
  target_asset_name: string;

  reason_code: string;

  reason: string;
}


export interface AttackPropagationResult {
  simulation_type:
    "security_aware_propagation";

  organization: Organization;

  start_asset: Asset;

  start_privilege:
    "LOW"
    | "HIGH";

  summary:
    AttackPropagationSummary;

  propagated_asset_ids:
    number[];

  traversed_relationship_ids:
    number[];

  exploited_vulnerability_ids:
    number[];

  exploited_vulnerabilities:
    Vulnerability[];

  propagated_assets:
    PropagatedAsset[];

  blocked_transitions:
    BlockedTransition[];

  semantics: string;
}
