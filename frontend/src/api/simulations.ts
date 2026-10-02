import {
  apiRequest,
} from "./client";

import type {
  ReachabilitySimulationResult,
} from "../types/simulation";

import type {
  AttackPropagationResult,
} from "../types/attackSimulation";

import type {
  BusinessImpactSimulationResult,
} from "../types/businessImpact";

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

export function runAttackPropagation(
  organizationId: number,
  startAssetId: number,
  startPrivilege:
    "LOW"
    | "HIGH",
) {
  return apiRequest<
    AttackPropagationResult
  >(
    "/simulations/"
    + "attack-propagation/",

    {
      method: "POST",

      body: JSON.stringify({
        organization:
          organizationId,

        start_asset:
          startAssetId,

        start_privilege:
          startPrivilege,
      }),
    },
  );
}

export function runBusinessImpactSimulation(
  organizationId: number,
  startAssetId: number,
  startPrivilege:
    "LOW"
    | "HIGH",
) {
  return apiRequest<
    BusinessImpactSimulationResult
  >(
    "/simulations/business-impact/",

    {
      method: "POST",

      body: JSON.stringify({
        organization:
          organizationId,

        start_asset:
          startAssetId,

        start_privilege:
          startPrivilege,
      }),
    },
  );
}
