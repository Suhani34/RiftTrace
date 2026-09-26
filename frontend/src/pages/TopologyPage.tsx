import {
  useEffect,
  useState,
} from "react";

import {
  Background,
  Controls,
  MiniMap,
  ReactFlow,
  useEdgesState,
  useNodesState,
} from "@xyflow/react";

import type {
  EdgeMouseHandler,
  NodeMouseHandler,
} from "@xyflow/react";

import {
  listOrganizations,
} from "../api/organizations";

import {
  getOrganizationTopology,
} from "../api/topology";

import AssetNode
  from "../components/graph/AssetNode";

import GraphDetailsPanel
  from "../components/graph/GraphDetailsPanel";

import GraphLegend
  from "../components/graph/GraphLegend";

import {
  buildTopologyGraph,
} from "../graph/buildTopologyGraph";

import type {
  TopologyEdge,
  TopologyNode,
} from "../graph/types";

import type {
  Asset,
  Organization,
  OrganizationTopology,
  Relationship,
} from "../types/models";


const nodeTypes = {
  asset: AssetNode,
};


export default function TopologyPage() {
  const [
    organizations,
    setOrganizations,
  ] = useState<Organization[]>([]);

  const [
    selectedOrganization,
    setSelectedOrganization,
  ] = useState("");

  const [
    topology,
    setTopology,
  ] = useState<OrganizationTopology | null>(
    null,
  );

  const [
    selectedAsset,
    setSelectedAsset,
  ] = useState<Asset | null>(null);

  const [
    selectedRelationship,
    setSelectedRelationship,
  ] = useState<Relationship | null>(
    null,
  );

  const [
    loading,
    setLoading,
  ] = useState(true);

  const [
    error,
    setError,
  ] = useState("");


  const [
    nodes,
    setNodes,
    onNodesChange,
  ] = useNodesState<TopologyNode>([]);

  const [
    edges,
    setEdges,
    onEdgesChange,
  ] = useEdgesState<TopologyEdge>([]);


  useEffect(() => {
    let cancelled = false;


    async function initializeTopology() {
      try {
        const organizationData =
          await listOrganizations();

        if (cancelled) {
          return;
        }

        setOrganizations(
          organizationData,
        );


        if (
          organizationData.length === 0
        ) {
          setLoading(false);

          return;
        }


        const initialOrganization =
          organizationData.find(
            (organization) =>
              organization.name
              === "RiftTrace Labs",
          )
          ?? organizationData[0];


        setSelectedOrganization(
          String(
            initialOrganization.id,
          ),
        );


        const topologyData =
          await getOrganizationTopology(
            initialOrganization.id,
          );


        if (cancelled) {
          return;
        }


        const graph =
          buildTopologyGraph(
            topologyData,
          );


        setTopology(
          topologyData,
        );

        setNodes(
          graph.nodes,
        );

        setEdges(
          graph.edges,
        );

        setError("");

        setLoading(false);
      } catch {
        if (!cancelled) {
          setError(
            "Unable to load the topology.",
          );

          setLoading(false);
        }
      }
    }


    void initializeTopology();


    return () => {
      cancelled = true;
    };
  }, [
    setEdges,
    setNodes,
  ]);


  async function handleOrganizationChange(
    value: string,
  ) {
    setSelectedOrganization(value);

    setSelectedAsset(null);

    setSelectedRelationship(null);


    if (!value) {
      setTopology(null);

      setNodes([]);

      setEdges([]);

      return;
    }


    try {
      setLoading(true);

      setError("");


      const topologyData =
        await getOrganizationTopology(
          Number(value),
        );


      const graph =
        buildTopologyGraph(
          topologyData,
        );


      setTopology(
        topologyData,
      );

      setNodes(
        graph.nodes,
      );

      setEdges(
        graph.edges,
      );
    } catch {
      setError(
        "Unable to load the selected "
        + "organization topology.",
      );
    } finally {
      setLoading(false);
    }
  }


  const handleNodeClick:
    NodeMouseHandler<TopologyNode> =
    (_event, node) => {
      if (node.type !== "asset") {
        return;
      }

      setSelectedAsset(
        node.data.asset,
      );

      setSelectedRelationship(null);
    };


  const handleEdgeClick:
    EdgeMouseHandler<TopologyEdge> =
    (_event, edge) => {
      const relationship =
        edge.data?.relationship;

      if (!relationship) {
        return;
      }

      setSelectedRelationship(
        relationship,
      );

      setSelectedAsset(null);
    };


  function handlePaneClick() {
    setSelectedAsset(null);

    setSelectedRelationship(null);
  }


  return (
    <>
      <div className="page-heading">
        <div>
          <h2>
            Cyber Topology
          </h2>

          <p>
            Interactive visualization of
            assets, network zones and
            technical relationships.
          </p>
        </div>
      </div>


      {error && (
        <div className="error-box">
          {error}
        </div>
      )}


      <section className="topology-toolbar">
        <label>
          Organization

          <select
            value={selectedOrganization}
            onChange={(event) =>
              void handleOrganizationChange(
                event.target.value,
              )
            }
          >
            {organizations.length === 0 && (
              <option value="">
                No organizations available
              </option>
            )}

            {organizations.map(
              (organization) => (
                <option
                  key={organization.id}
                  value={organization.id}
                >
                  {organization.name}
                </option>
              ),
            )}
          </select>
        </label>


        {topology && (
          <div className="topology-stats">
            <div className="topology-stat">
              <span>Zones</span>

              <strong>
                {topology.zones.length}
              </strong>
            </div>

            <div className="topology-stat">
              <span>Assets</span>

              <strong>
                {topology.nodes.length}
              </strong>
            </div>

            <div className="topology-stat">
              <span>Relationships</span>

              <strong>
                {topology.edges.length}
              </strong>
            </div>
          </div>
        )}
      </section>


      <GraphLegend />


      <section className="topology-workspace">
        <div className="topology-canvas-card">
          {loading ? (
            <div className="graph-message">
              Loading topology...
            </div>
          ) : nodes.length === 0 ? (
            <div className="graph-message">
              This organization has no
              assets to visualize.
            </div>
          ) : (
            <div className="topology-canvas">
              <ReactFlow<
                TopologyNode,
                TopologyEdge
              >
                nodes={nodes}
                edges={edges}

                onNodesChange={
                  onNodesChange
                }

                onEdgesChange={
                  onEdgesChange
                }

                nodeTypes={
                  nodeTypes
                }

                onNodeClick={
                  handleNodeClick
                }

                onEdgeClick={
                  handleEdgeClick
                }

                onPaneClick={
                  handlePaneClick
                }

                nodesConnectable={
                  false
                }

                fitView

                fitViewOptions={{
                  padding: 0.15,
                }}

                minZoom={0.2}
                maxZoom={1.8}
              >
                <MiniMap
                  pannable
                  zoomable
                />

                <Controls />

                <Background
                  gap={22}
                  size={1}
                />
              </ReactFlow>
            </div>
          )}
        </div>


        <GraphDetailsPanel
          asset={selectedAsset}
          relationship={
            selectedRelationship
          }
        />
      </section>
    </>
  );
}
