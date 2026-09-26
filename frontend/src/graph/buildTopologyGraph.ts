import {
  MarkerType,
} from "@xyflow/react";

import type {
  Asset,
  NetworkZone,
  OrganizationTopology,
} from "../types/models";

import type {
  BuiltTopologyGraph,
  TopologyNode,
} from "./types";


const GROUP_WIDTH = 340;
const ASSET_NODE_WIDTH = 260;
const ASSET_NODE_HEIGHT = 125;

const GROUP_HEADER_HEIGHT = 70;
const GROUP_BOTTOM_PADDING = 30;

const CHILD_X = 40;
const CHILD_GAP = 20;

const GROUP_HORIZONTAL_GAP = 90;
const GROUP_VERTICAL_GAP = 90;

const GROUP_COLUMNS = 2;


type ZoneBucket = {
  zone: NetworkZone | null;
  assets: Asset[];
};


function createZoneBuckets(
  topology: OrganizationTopology,
): ZoneBucket[] {
  const knownZoneIds = new Set(
    topology.zones.map(
      (zone) => zone.id,
    ),
  );

  const buckets: ZoneBucket[] =
    topology.zones.map(
      (zone) => ({
        zone,

        assets: topology.nodes.filter(
          (asset) =>
            asset.network_zone === zone.id,
        ),
      }),
    );

  const unassignedAssets =
    topology.nodes.filter(
      (asset) =>
        asset.network_zone === null
        || !knownZoneIds.has(
          asset.network_zone,
        ),
    );

  if (unassignedAssets.length > 0) {
    buckets.push({
      zone: null,
      assets: unassignedAssets,
    });
  }

  return buckets;
}


function getZoneClassName(
  zone: NetworkZone | null,
) {
  if (!zone) {
    return (
      "zone-group zone-type-unassigned"
    );
  }

  return (
    `zone-group zone-type-${zone.zone_type.toLowerCase()}`
  );
}


export function buildTopologyGraph(
  topology: OrganizationTopology,
): BuiltTopologyGraph {
  const nodes: TopologyNode[] = [];

  const buckets =
    createZoneBuckets(topology);

  let groupX = 0;
  let groupY = 0;

  let currentColumn = 0;
  let rowMaximumHeight = 0;


  for (const bucket of buckets) {
    const groupId = bucket.zone
      ? `zone-${bucket.zone.id}`
      : "zone-unassigned";

    const assetCount =
      bucket.assets.length;

    const requiredHeight =
      GROUP_HEADER_HEIGHT
      + GROUP_BOTTOM_PADDING
      + (
        assetCount
        * (
          ASSET_NODE_HEIGHT
          + CHILD_GAP
        )
      );

    const groupHeight =
      Math.max(
        220,
        requiredHeight,
      );


    nodes.push({
      id: groupId,

      type: "group",

      position: {
        x: groupX,
        y: groupY,
      },

      data: {
        label:
          bucket.zone?.name
          ?? "Unassigned",

        zone: bucket.zone,
      },

      className:
        getZoneClassName(
          bucket.zone,
        ),

      style: {
        width: GROUP_WIDTH,
        height: groupHeight,
      },

      draggable: false,
      selectable: false,
      deletable: false,
    });


    bucket.assets.forEach(
      (asset, index) => {
        nodes.push({
          id: `asset-${asset.id}`,

          type: "asset",

          parentId: groupId,

          extent: "parent",

          position: {
            x: CHILD_X,

            y:
              GROUP_HEADER_HEIGHT
              + (
                index
                * (
                  ASSET_NODE_HEIGHT
                  + CHILD_GAP
                )
              ),
          },

          data: {
            asset,
          },

          style: {
            width: ASSET_NODE_WIDTH,
          },

          draggable: true,
          deletable: false,
        });
      },
    );


    rowMaximumHeight =
      Math.max(
        rowMaximumHeight,
        groupHeight,
      );


    currentColumn += 1;


    if (
      currentColumn
      >= GROUP_COLUMNS
    ) {
      currentColumn = 0;

      groupX = 0;

      groupY +=
        rowMaximumHeight
        + GROUP_VERTICAL_GAP;

      rowMaximumHeight = 0;
    } else {
      groupX +=
        GROUP_WIDTH
        + GROUP_HORIZONTAL_GAP;
    }
  }


  const edges =
    topology.edges.map(
      (relationship) => ({
        id:
          `relationship-${relationship.id}`,

        source:
          `asset-${relationship.source}`,

        target:
          `asset-${relationship.target}`,

        type: "smoothstep",

        label:
          relationship
            .relationship_type_display,

        data: {
          relationship,
        },

        markerEnd: {
          type:
            MarkerType.ArrowClosed,
        },

        deletable: false,
        selectable: true,

        zIndex: 1,

        style: {
          strokeWidth: 2,
        },

        labelStyle: {
          fontSize: 11,
          fontWeight: 700,
        },

        labelBgPadding: [
          7,
          4,
        ] as [number, number],

        labelBgBorderRadius: 4,

        labelBgStyle: {
          fill: "#ffffff",
          fillOpacity: 0.95,
        },
      }),
    );


  return {
    nodes,
    edges,
  };
}
