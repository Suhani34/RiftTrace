import type {
  SimulationType,
} from "../types/scenarios";


const COMPARABLE_KEYS = [
  "attack_paths",
  "reachable_assets",
  "propagated_assets",
  "compromised_assets",
  "critical_assets",
  "impacted_processes",
  "critical_processes",
  "essential_dependency_hits",
  "acquired_identities",
  "successful_identity_steps",
  "new_assets_from_identity",
] as const;


function isRecord(
  value: unknown,
): value is Record<
  string,
  unknown
> {
  return (
    typeof value === "object"
    && value !== null
    && !Array.isArray(
      value
    )
  );
}


function addNumericValue(
  metrics:
    Record<string, number>,

  key: string,

  value: unknown,
) {
  if (
    typeof value === "number"
    && Number.isFinite(
      value
    )
  ) {
    metrics[key] =
      value;
  }
}


export function extractComparableMetrics(
  simulationType:
    SimulationType,

  result: unknown,
): Record<string, number> {
  const metrics:
    Record<string, number> = {};


  if (!isRecord(result)) {
    return metrics;
  }


  const summary =
    isRecord(
      result.summary
    )
      ? result.summary
      : {};


  const resultMetrics =
    isRecord(
      result.metrics
    )
      ? result.metrics
      : {};


  for (
    const key
    of COMPARABLE_KEYS
  ) {
    addNumericValue(
      metrics,
      key,
      summary[key],
    );


    if (
      metrics[key]
      === undefined
    ) {
      addNumericValue(
        metrics,
        key,
        result[key],
      );
    }


    if (
      metrics[key]
      === undefined
    ) {
      addNumericValue(
        metrics,
        key,
        resultMetrics[key],
      );
    }


    if (
      metrics[key]
      === undefined
      && Array.isArray(
        result[key]
      )
    ) {
      metrics[key] =
        result[key].length;
    }
  }


  if (
    simulationType
    === "IDENTITY_PROPAGATION"
  ) {
    if (
      Array.isArray(
        result.compromised_assets
      )
    ) {
      metrics.compromised_assets =
        result
          .compromised_assets
          .length;
    }
  }


  return metrics;
}
