export interface AttackPathAsset {
  asset_id: number;

  asset_name: string;

  privilege: "LOW" | "HIGH" | string;
}


export interface AttackPathTransition {
  relationship_id: number;

  source_asset_id: number;

  source_asset_name: string;

  source_privilege: string;

  target_asset_id: number;

  target_asset_name: string;

  target_privilege: string;

  mechanism: string;

  vulnerability_id:
    number | null;

  vulnerability_title:
    string | null;
}


export interface AttackPath {
  path_id: string;

  hop_count: number;

  is_critical_path: boolean;

  is_business_critical_path:
    boolean;

  target: {
    asset_id: number;

    asset_name: string;

    criticality: string;

    business_processes:
      string[];

    critical_business_processes:
      string[];
  };

  assets:
    AttackPathAsset[];

  transitions:
    AttackPathTransition[];
}


export interface NodeChokepoint {
  asset_id: number;

  asset_name: string;

  paths_through: number;

  total_paths: number;

  coverage_percent: number;

  critical_paths_through:
    number;

  paths_removed_if_blocked:
    number;

  remaining_paths: number;

  single_point_chokepoint:
    boolean;
}


export interface EdgeChokepoint {
  relationship_id: number;

  source_asset_id: number;

  source_asset_name: string;

  target_asset_id: number;

  target_asset_name: string;

  paths_through: number;

  total_paths: number;

  coverage_percent: number;

  critical_paths_through:
    number;

  paths_removed_if_blocked:
    number;

  remaining_paths: number;

  single_point_chokepoint:
    boolean;
}


export interface PathIntelligenceResult {
  summary: {
    start_asset_id: number;

    start_asset_name: string;

    start_privilege: string;

    target_count: number;

    attack_paths: number;

    critical_attack_paths:
      number;

    business_critical_attack_paths:
      number;

    node_chokepoints:
      number;

    edge_chokepoints:
      number;

    max_depth: number;

    max_paths: number;

    path_limit_reached:
      boolean;
  };

  paths:
    AttackPath[];

  node_chokepoints:
    NodeChokepoint[];

  edge_chokepoints:
    EdgeChokepoint[];

  interpretation: string;
}
