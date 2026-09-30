import {
  apiRequest,
} from "./client";

import type {
  ReachabilitySimulationResult,
} from "../types/simulation";


export function runReachabilitySimulation(
  organizationId: number,
  startAssetId: number,
) {
  return apiRequest<
    ReachabilitySimulationResult
  >(
    "/simulations/reachability/",

    {
      method: "POST",

      body: JSON.stringify({
        organization:
          organizationId,

        start_asset:
          startAssetId,
      }),
    },
  );
}
