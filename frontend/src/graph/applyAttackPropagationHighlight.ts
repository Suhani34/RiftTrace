import type {
  AttackPropagationResult,
} from "../types/attackSimulation";

import type {
  TopologyEdge,
  TopologyNode,
} from "./types";


interface HighlightedTopology {
  nodes: TopologyNode[];
  edges: TopologyEdge[];
}


export function applyAttackPropagationHighlight(
  nodes: TopologyNode[],
  edges: TopologyEdge[],
  result:
    AttackPropagationResult
    | null,
): HighlightedTopology {
  if (!result) {
    return {
      nodes: nodes.map(
        (node) => {
          if (node.type !== "asset") {
            return node;
          }

          return {
            ...node,

            data: {
              ...node.data,

              simulationState:
                "normal",
            },
          };
        },
      ),

      edges: edges.map(
        (edge) => ({
          ...edge,

          animated: false,

          style: {
            ...edge.style,

            stroke: "#64748b",

            strokeWidth: 2,

            opacity: 1,
          },

          labelStyle: {
            ...edge.labelStyle,

            opacity: 1,
          },
        }),
      ),
    };
  }

  const propagatedById =
    new Map(
      result.propagated_assets.map(
        (item) => [
          item.asset.id,
          item,
        ],
      ),
    );

  const traversedRelationshipIds =
    new Set(
      result
        .traversed_relationship_ids,
    );

  return {
    nodes: nodes.map(
      (node) => {
        if (node.type !== "asset") {
          return node;
        }

        const assetId =
          node.data.asset.id;

        if (
          assetId
          === result.start_asset.id
        ) {
          return {
            ...node,

            data: {
              ...node.data,

              simulationState:
                "start",
            },
          };
        }

        const propagated =
          propagatedById.get(
            assetId,
          );

        if (propagated) {
          return {
            ...node,

            data: {
              ...node.data,

              simulationState:
                propagated.privilege
                === "HIGH"
                  ? "compromised-high"
                  : "compromised-low",
            },
          };
        }

        return {
          ...node,

          data: {
            ...node.data,

            simulationState:
              "dimmed",
          },
        };
      },
    ),

    edges: edges.map(
      (edge) => {
        const relationshipId =
          edge.data
            ?.relationship
            .id;

        const traversed =
          relationshipId
          !== undefined

          && (
            traversedRelationshipIds
            .has(
              relationshipId,
            )
          );

        return {
          ...edge,

          animated: traversed,

          style: {
            ...edge.style,

            stroke: traversed
              ? "#dc2626"
              : "#94a3b8",

            strokeWidth: traversed
              ? 3
              : 1.5,

            opacity: traversed
              ? 1
              : 0.18,
          },

          labelStyle: {
            ...edge.labelStyle,

            opacity: traversed
              ? 1
              : 0.2,
          },
        };
      },
    ),
  };
}
