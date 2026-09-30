import type {
  Edge,
  Node,
} from "@xyflow/react";

import type {
  Asset,
  NetworkZone,
  Relationship,
} from "../types/models";

export type SimulationNodeState =
  | "normal"
  | "start"
  | "reachable"
  | "dimmed";


export type AssetNodeData = {
  asset: Asset;

  simulationState:
    SimulationNodeState;
};

export type ZoneNodeData = {
  label: string;
  zone: NetworkZone | null;
};


export type RelationshipEdgeData = {
  relationship: Relationship;
};


export type AssetGraphNode = Node<
  AssetNodeData,
  "asset"
>;


export type ZoneGraphNode = Node<
  ZoneNodeData,
  "group"
>;


export type TopologyNode =
  | AssetGraphNode
  | ZoneGraphNode;


export type TopologyEdge = Edge<
  RelationshipEdgeData
>;


export interface BuiltTopologyGraph {
  nodes: TopologyNode[];
  edges: TopologyEdge[];
}
