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
  CounterfactualSimulationResult,
} from "../types/counterfactual";

import type {
  SecurityControlSimulationResult,
} from "../types/controlSimulation";

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

export function runCounterfactualSimulation(
  organizationId: number,
  startAssetId: number,
  startPrivilege:
    "LOW"
    | "HIGH",
  disabledRelationshipIds:
    number[],
  disabledVulnerabilityIds:
    number[],
) {
  return apiRequest<
    CounterfactualSimulationResult
  >(
    "/simulations/counterfactual/",

    {
      method: "POST",

      body: JSON.stringify({
        organization:
          organizationId,

        start_asset:
          startAssetId,

        start_privilege:
          startPrivilege,

        disabled_relationship_ids:
          disabledRelationshipIds,

        disabled_vulnerability_ids:
          disabledVulnerabilityIds,
      }),
    },
  );
}

export function runSecurityControlSimulation(
  organizationId: number,

  startAssetId: number,

  startPrivilege:
    "LOW"
    | "HIGH",

  controlIds:
    number[],
) {
  return apiRequest<
    SecurityControlSimulationResult
  >(
    "/simulations/security-controls/",

    {
      method: "POST",

      body: JSON.stringify({
        organization:
          organizationId,

        start_asset:
          startAssetId,

        start_privilege:
          startPrivilege,

        control_ids:
          controlIds,
      }),
    },
  );
}
