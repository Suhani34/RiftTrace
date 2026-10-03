import {
  useEffect,
  useState,
} from "react";

import {
  listOrganizations,
} from "../api/organizations";

import {
  runCounterfactualSimulation,
} from "../api/simulations";

import {
  getOrganizationTopology,
} from "../api/topology";

import {
  listVulnerabilities,
} from "../api/vulnerabilities";

import type {
  Organization,
  OrganizationTopology,
} from "../types/models";

import type {
  Vulnerability,
} from "../types/security";

import type {
  CounterfactualSimulationResult,
} from "../types/counterfactual";


export default function CounterfactualPage() {
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
  ] = useState<
    OrganizationTopology
    | null
  >(null);


  const [
    vulnerabilities,
    setVulnerabilities,
  ] = useState<
    Vulnerability[]
  >([]);


  const [
    startAssetId,
    setStartAssetId,
  ] = useState("");


  const [
    startPrivilege,
    setStartPrivilege,
  ] = useState<
    "LOW"
    | "HIGH"
  >("LOW");


  const [
    disabledRelationshipIds,
    setDisabledRelationshipIds,
  ] = useState<number[]>([]);


  const [
    disabledVulnerabilityIds,
    setDisabledVulnerabilityIds,
  ] = useState<number[]>([]);


  const [
    result,
    setResult,
  ] = useState<
    CounterfactualSimulationResult
    | null
  >(null);


  const [
    running,
    setRunning,
  ] = useState(false);


  const [
    error,
    setError,
  ] = useState("");


  async function loadOrganizationData(
    organizationId: number,
  ) {
    const [
      topologyData,
      vulnerabilityData,
    ] = await Promise.all([
      getOrganizationTopology(
        organizationId,
      ),

      listVulnerabilities(
        organizationId,
      ),
    ]);


    setTopology(
      topologyData
    );


    setVulnerabilities(
      vulnerabilityData
    );
  }


  useEffect(() => {
    let cancelled = false;


    async function initialize() {
      try {
        const organizationData =
          await listOrganizations();


        if (cancelled) {
          return;
        }


        setOrganizations(
          organizationData
        );


        if (
          organizationData.length
          === 0
        ) {
          return;
        }


        const initial =
          organizationData.find(
            (organization) =>
              organization.name
              === "RiftTrace Labs",
          )
          ?? organizationData[0];


        setSelectedOrganization(
          String(
            initial.id
          )
        );


        const [
          topologyData,
          vulnerabilityData,
        ] = await Promise.all([
          getOrganizationTopology(
            initial.id,
          ),

          listVulnerabilities(
            initial.id,
          ),
        ]);


        if (cancelled) {
          return;
        }


        setTopology(
          topologyData
        );


        setVulnerabilities(
          vulnerabilityData
        );
      } catch {
        if (!cancelled) {
          setError(
            "Unable to load "
            + "counterfactual data.",
          );
        }
      }
    }


    void initialize();


    return () => {
      cancelled = true;
    };
  }, []);


  async function handleOrganizationChange(
    value: string,
  ) {
    setSelectedOrganization(value);

    setStartAssetId("");

    setDisabledRelationshipIds([]);

    setDisabledVulnerabilityIds([]);

    setResult(null);

    setError("");


    if (!value) {
      setTopology(null);

      setVulnerabilities([]);

      return;
    }


    try {
      await loadOrganizationData(
        Number(value)
      );
    } catch {
      setError(
        "Unable to load selected "
        + "organization.",
      );
    }
  }


  function toggleRelationship(
    relationshipId: number,
  ) {
    setDisabledRelationshipIds(
      (current) =>
        current.includes(
          relationshipId
        )
          ? current.filter(
              (id) =>
                id !== relationshipId,
            )

          : [
              ...current,
              relationshipId,
            ],
    );


    setResult(null);
  }


  function toggleVulnerability(
    vulnerabilityId: number,
  ) {
    setDisabledVulnerabilityIds(
      (current) =>
        current.includes(
          vulnerabilityId
        )
          ? current.filter(
              (id) =>
                id !== vulnerabilityId,
            )

          : [
              ...current,
              vulnerabilityId,
            ],
    );


    setResult(null);
  }


  async function handleRun() {
    if (
      !selectedOrganization
      || !startAssetId
    ) {
      setError(
        "Select a starting asset.",
      );

      return;
    }


    if (
      disabledRelationshipIds.length
      === 0

      &&

      disabledVulnerabilityIds.length
      === 0
    ) {
      setError(
        "Select at least one "
        + "counterfactual change.",
      );

      return;
    }


    try {
      setRunning(true);

      setError("");


      const simulationResult =
        await runCounterfactualSimulation(
          Number(
            selectedOrganization
          ),

          Number(
            startAssetId
          ),

          startPrivilege,

          disabledRelationshipIds,

          disabledVulnerabilityIds,
        );


      setResult(
        simulationResult
      );
    } catch {
      setError(
        "Unable to run "
        + "counterfactual simulation.",
      );
    } finally {
      setRunning(false);
    }
  }


  function handleResetScenario() {
    setDisabledRelationshipIds([]);

    setDisabledVulnerabilityIds([]);

    setResult(null);

    setError("");
  }


  return (
    <>
      <div className="page-heading">
        <div>
          <h2>
            Counterfactual Analysis
          </h2>

          <p>
            Compare the current modeled
            environment with temporary
            hypothetical changes without
            modifying stored data.
          </p>
        </div>
      </div>


      {error && (
        <div className="error-box">
          {error}
        </div>
      )}


      <section className="panel">
        <h3>
          Scenario
        </h3>


        <div className="form-grid">
          <label>
            Organization

            <select
              value={
                selectedOrganization
              }
              onChange={(event) =>
                void handleOrganizationChange(
                  event.target.value,
                )
              }
            >
              {organizations.map(
                (organization) => (
                  <option
                    key={
                      organization.id
                    }
                    value={
                      organization.id
                    }
                  >
                    {
                      organization.name
                    }
                  </option>
                ),
              )}
            </select>
          </label>


          <label>
            Initial Compromised Asset

            <select
              value={startAssetId}
              onChange={(event) => {
                setStartAssetId(
                  event.target.value,
                );

                setResult(null);
              }}
            >
              <option value="">
                Select asset
              </option>

              {
                topology?.nodes.map(
                  (asset) => (
                    <option
                      key={asset.id}
                      value={asset.id}
                    >
                      {asset.name}
                    </option>
                  ),
                )
              }
            </select>
          </label>


          <label>
            Initial Privilege

            <select
              value={startPrivilege}
              onChange={(event) => {
                setStartPrivilege(
                  event.target.value as
                      | "LOW"
                      | "HIGH",
                );

                setResult(null);
              }}
            >
              <option value="LOW">
                Low
              </option>

              <option value="HIGH">
                High
              </option>
            </select>
          </label>
        </div>
      </section>


      <section className="panel">
        <div className="counterfactual-section-heading">
          <div>
            <h3>
              Temporarily Disable
              Relationships
            </h3>

            <p>
              Selected relationships are
              removed only from the
              temporary simulation copy.
            </p>
          </div>

          <strong>
            {
              disabledRelationshipIds
                .length
            }
            {" selected"}
          </strong>
        </div>


        {
          !topology
          || topology.edges.length === 0
        ? (
          <p>
            No relationships available.
          </p>
        )
        : (
          <div className="counterfactual-option-grid">
            {topology.edges.map(
              (relationship) => (
                <label
                  className="counterfactual-option"
                  key={
                    relationship.id
                  }
                >
                  <input
                    type="checkbox"
                    checked={
                      disabledRelationshipIds
                        .includes(
                          relationship.id
                        )
                    }
                    onChange={() =>
                      toggleRelationship(
                        relationship.id
                      )
                    }
                  />

                  <div>
                    <strong>
                      {
                        relationship
                          .source_name
                      }
                      {" → "}
                      {
                        relationship
                          .target_name
                      }
                    </strong>

                    <span>
                      {
                        relationship
                          .relationship_type_display
                      }

                      {
                        relationship.protocol
                        ? (
                            ` · ${relationship.protocol}`
                          )
                        : ""
                      }

                      {
                        relationship.port
                        ? (
                            `:${relationship.port}`
                          )
                        : ""
                      }
                    </span>
                  </div>
                </label>
              ),
            )}
          </div>
        )}
      </section>


      <section className="panel">
        <div className="counterfactual-section-heading">
          <div>
            <h3>
              Temporarily Disable
              Vulnerabilities
            </h3>

            <p>
              Selected vulnerabilities are
              excluded only from the
              hypothetical simulation.
            </p>
          </div>

          <strong>
            {
              disabledVulnerabilityIds
                .length
            }
            {" selected"}
          </strong>
        </div>


        {vulnerabilities.length === 0 ? (
          <p>
            No vulnerabilities available.
          </p>
        ) : (
          <div className="counterfactual-option-grid">
            {vulnerabilities.map(
              (vulnerability) => (
                <label
                  className="counterfactual-option"
                  key={
                    vulnerability.id
                  }
                >
                  <input
                    type="checkbox"
                    checked={
                      disabledVulnerabilityIds
                        .includes(
                          vulnerability.id
                        )
                    }
                    onChange={() =>
                      toggleVulnerability(
                        vulnerability.id
                      )
                    }
                  />

                  <div>
                    <strong>
                      {
                        vulnerability
                          .reference_id
                        || vulnerability
                          .title
                      }
                    </strong>

                    <span>
                      {
                        vulnerability
                          .asset_name
                      }
                      {" · "}
                      {
                        vulnerability
                          .attack_vector_display
                      }
                      {" · "}
                      {
                        vulnerability
                          .grants_privilege_display
                      }
                    </span>
                  </div>
                </label>
              ),
            )}
          </div>
        )}
      </section>


      <section className="panel">
        <div className="counterfactual-actions">
          <button
            type="button"
            disabled={
              running
              || !startAssetId
            }
            onClick={() => {
              void handleRun();
            }}
          >
            {
              running
              ? "Comparing..."
              : "Compare Scenario"
            }
          </button>


          <button
            type="button"
            className="secondary-button"
            onClick={
              handleResetScenario
            }
          >
            Reset Changes
          </button>
        </div>


        <p className="counterfactual-note">
          This analysis does not write the
          selected changes to PostgreSQL.
        </p>
      </section>


      {result && (
        <>
          <section className="panel">
            <h3>
              Baseline vs Counterfactual
            </h3>


            <div className="comparison-table">
              <div className="comparison-row comparison-header">
                <span>
                  Metric
                </span>

                <span>
                  Baseline
                </span>

                <span>
                  Counterfactual
                </span>

                <span>
                  Reduction
                </span>
              </div>


              <div className="comparison-row">
                <span>
                  Propagated Assets
                </span>

                <strong>
                  {
                    result
                      .baseline
                      .technical_consequence
                      .propagated_asset_count
                  }
                </strong>

                <strong>
                  {
                    result
                      .counterfactual
                      .technical_consequence
                      .propagated_asset_count
                  }
                </strong>

                <strong>
                  {
                    result
                      .comparison
                      .propagated_asset_reduction
                  }
                </strong>
              </div>


              <div className="comparison-row">
                <span>
                  Critical Assets
                </span>

                <strong>
                  {
                    result
                      .baseline
                      .technical_consequence
                      .critical_asset_count
                  }
                </strong>

                <strong>
                  {
                    result
                      .counterfactual
                      .technical_consequence
                      .critical_asset_count
                  }
                </strong>

                <strong>
                  {
                    result
                      .comparison
                      .critical_asset_reduction
                  }
                </strong>
              </div>


              <div className="comparison-row">
                <span>
                  Impacted Processes
                </span>

                <strong>
                  {
                    result
                      .baseline
                      .business_impact
                      .summary
                      .impacted_process_count
                  }
                </strong>

                <strong>
                  {
                    result
                      .counterfactual
                      .business_impact
                      .summary
                      .impacted_process_count
                  }
                </strong>

                <strong>
                  {
                    result
                      .comparison
                      .impacted_process_reduction
                  }
                </strong>
              </div>


              <div className="comparison-row">
                <span>
                  Critical Processes
                </span>

                <strong>
                  {
                    result
                      .baseline
                      .business_impact
                      .summary
                      .critical_process_count
                  }
                </strong>

                <strong>
                  {
                    result
                      .counterfactual
                      .business_impact
                      .summary
                      .critical_process_count
                  }
                </strong>

                <strong>
                  {
                    result
                      .comparison
                      .critical_process_reduction
                  }
                </strong>
              </div>


              <div className="comparison-row">
                <span>
                  Essential Dependency
                  Hits
                </span>

                <strong>
                  {
                    result
                      .baseline
                      .business_impact
                      .summary
                      .essential_dependency_hit_count
                  }
                </strong>

                <strong>
                  {
                    result
                      .counterfactual
                      .business_impact
                      .summary
                      .essential_dependency_hit_count
                  }
                </strong>

                <strong>
                  {
                    result
                      .comparison
                      .essential_dependency_hit_reduction
                  }
                </strong>
              </div>
            </div>
          </section>


          <section className="counterfactual-result-grid">
            <article className="panel">
              <h3>
                Prevented Technical
                Propagation
              </h3>

              {
                result
                  .comparison
                  .prevented_propagated_assets
                  .length === 0
              ? (
                <p>
                  No propagated assets were
                  prevented by this scenario.
                </p>
              )
              : (
                <div className="comparison-item-list">
                  {
                    result
                      .comparison
                      .prevented_propagated_assets
                      .map(
                        (asset) => (
                          <div
                            key={
                              asset.id
                            }
                          >
                            <strong>
                              {
                                asset.name
                              }
                            </strong>

                            <span>
                              {
                                asset
                                  .criticality_display
                              }
                            </span>
                          </div>
                        ),
                      )
                  }
                </div>
              )}
            </article>


            <article className="panel">
              <h3>
                Avoided Business
                Processes
              </h3>

              {
                result
                  .comparison
                  .avoided_business_processes
                  .length === 0
              ? (
                <p>
                  No business process was
                  completely avoided by this
                  scenario.
                </p>
              )
              : (
                <div className="comparison-item-list">
                  {
                    result
                      .comparison
                      .avoided_business_processes
                      .map(
                        (process) => (
                          <div
                            key={
                              process.id
                            }
                          >
                            <strong>
                              {
                                process.name
                              }
                            </strong>

                            <span>
                              {
                                process
                                  .criticality_display
                              }
                            </span>
                          </div>
                        ),
                      )
                  }
                </div>
              )}
            </article>
          </section>


          <section className="panel">
            <h3>
              Scenario Interpretation
            </h3>

            <div className="simulation-semantics">
              {result.semantics}
            </div>


            <p>
              A reduction of zero does not
              necessarily mean the change
              had no effect. For example, a
              business process may remain
              potentially impacted through
              the starting compromised
              asset while fewer of its
              technical dependencies are
              affected.
            </p>
          </section>
        </>
      )}
    </>
  );
}
