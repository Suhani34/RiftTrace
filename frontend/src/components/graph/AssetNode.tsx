import {
  Handle,
  Position,
} from "@xyflow/react";

import type {
  NodeProps,
} from "@xyflow/react";

import type {
  AssetGraphNode,
} from "../../graph/types";


export default function AssetNode({
  data,
  selected,
}: NodeProps<AssetGraphNode>) {
  const asset = data.asset;

  const criticalityClass =
    `graph-criticality-${asset.criticality.toLowerCase()}`;


  return (
    <div
      className={[
        "asset-graph-node",
        criticalityClass,

	`simulation-${data.simulationState}`,
        selected
          ? "asset-graph-node-selected"
          : "",
      ]
        .filter(Boolean)
        .join(" ")}
    >
      <Handle
        type="target"
        position={Position.Left}
        className="asset-node-handle"
      />

      <div className="asset-node-header">
        <strong>
          {asset.name}
        </strong>

        <span
          className={
            `badge criticality-${asset.criticality.toLowerCase()}`
          }
        >
          {asset.criticality_display}
        </span>
      </div>

      <div className="asset-node-type">
        {asset.asset_type_display}
      </div>

      <div className="asset-node-meta">
        <span>
          {asset.environment_display}
        </span>

        <span>
          {asset.network_zone_name
            ?? "Unassigned"}
        </span>
      </div>

      {asset.ip_address && (
        <div className="asset-node-address">
          {asset.ip_address}
        </div>
      )}

      {asset.is_internet_exposed && (
        <div className="asset-node-exposed">
          Internet exposed
        </div>
      )}

      <Handle
        type="source"
        position={Position.Right}
        className="asset-node-handle"
      />
    </div>
  );
}
