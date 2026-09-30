import type {
  TopologyEdge,
  TopologyNode,
} from "./types";

import type {
  ReachabilitySimulationResult,
} from "../types/simulation";


interface HighlightedTopology {
  nodes: TopologyNode[];
  edges: TopologyEdge[];
}


export function applyReachabilityHighlight(
  nodes: TopologyNode[],
  edges: TopologyEdge[],
  result:
    ReachabilitySimulationResult
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


  const reachableAssetIds =
    new Set(
      result.reachable_asset_ids
    );


  const reachableRelationshipIds =
    new Set(
      result
        .reachable_relationship_ids
    );


  const startAssetId =
    result.start_asset.id;


  return {
    nodes: nodes.map(
      (node) => {
        if (node.type !== "asset") {
          return node;
        }


        const assetId =
          node.data.asset.id;


        let simulationState:
          "start"
          | "reachable"
          | "dimmed";


        if (assetId === startAssetId) {
          simulationState =
            "start";
        } else if (
          reachableAssetIds.has(
            assetId
          )
        ) {
          simulationState =
            "reachable";
        } else {
          simulationState =
            "dimmed";
        }


        return {
          ...node,

          data: {
            ...node.data,

            simulationState,
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


        const reachable =
          relationshipId
          !== undefined
          && (
            reachableRelationshipIds
              .has(
                relationshipId
              )
          );


        return {
          ...edge,

          animated: reachable,

          style: {
            ...edge.style,

            stroke: reachable
              ? "#2563eb"
              : "#94a3b8",

            strokeWidth: reachable
              ? 3
              : 1.5,

            opacity: reachable
              ? 1
              : 0.18,
          },

          labelStyle: {
            ...edge.labelStyle,

            opacity: reachable
              ? 1
              : 0.2,
          },
        };
      },
    ),
  };
}
