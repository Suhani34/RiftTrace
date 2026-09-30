import type {
  Asset,
  Organization,
} from "./models";


export interface ReachableAssetPath {
  asset: Asset;

  hop_count: number;

  shortest_path_asset_ids: number[];

  shortest_path_asset_names: string[];
}


export interface ReachabilitySummary {
  total_assets: number;

  reachable_asset_count: number;

  reachable_critical_asset_count: number;

  max_hops: number;
}


export interface ReachabilitySimulationResult {
  simulation_type:
    "topology_reachability";

  organization: Organization;

  start_asset: Asset;

  summary: ReachabilitySummary;

  reachable_asset_ids: number[];

  reachable_relationship_ids:
    number[];

  reachable_assets:
    ReachableAssetPath[];

  semantics: string;
}
