import {
  useEffect,
  useState,
} from "react";

import {
  listOrganizations,
} from "../api/organizations";

import {
  getOrganizationTopology,
} from "../api/topology";

import {
  listSecurityControls,
} from "../api/securityControls";

import {
  runSecurityControlSimulation,
} from "../api/simulations";

import type {
  Organization,
  OrganizationTopology,
} from "../types/models";

import type {
  SecurityControl,
} from "../types/securityControl";

import type {
  SecurityControlSimulationResult,
} from "../types/controlSimulation";


export default function ControlSimulationPage() {
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
    controls,
    setControls,
  ] = useState<
    SecurityControl[]
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
    selectedControlIds,
    setSelectedControlIds,
  ] = useState<number[]>([]);


  const [
    result,
    setResult,
  ] = useState<
    SecurityControlSimulationResult
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


  async function loadData(
    organizationId: number,
  ) {
    const [
      topologyData,
      controlData,
    ] = await Promise.all([
      getOrganizationTopology(
        organizationId
      ),

      listSecurityControls(
        organizationId
      ),
    ]);


    setTopology(
      topologyData
    );

    setControls(
      controlData
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
          controlData,
        ] = await Promise.all([
          getOrganizationTopology(
            initial.id
          ),

          listSecurityControls(
            initial.id
          ),
        ]);


        if (cancelled) {
          return;
        }


        setTopology(
          topologyData
        );

        setControls(
          controlData
        );
      } catch {
        if (!cancelled) {
          setError(
            "Unable to load control "
            + "simulation data.",
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
    setSelectedOrganization(
      value
    );

    setStartAssetId("");

    setSelectedControlIds([]);

    setResult(null);

    setError("");


    if (!value) {
      setTopology(null);

      setControls([]);

      return;
    }


    try {
      await loadData(
        Number(value)
      );
    } catch {
      setError(
        "Unable to load selected "
        + "organization.",
      );
    }
  }


  function toggleControl(
    controlId: number,
  ) {
    setSelectedControlIds(
      (current) =>
        current.includes(
          controlId
        )
          ? current.filter(
              (id) =>
                id !== controlId,
            )

          : [
              ...current,
              controlId,
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
      selectedControlIds.length
      === 0
    ) {
      setError(
        "Select at least one "
        + "security control.",
      );

      return;
    }


    try {
      setRunning(true);

      setError("");


      const simulationResult =
        await runSecurityControlSimulation(
          Number(
            selectedOrganization
          ),

          Number(
            startAssetId
          ),

          startPrivilege,

          selectedControlIds,
        );


      setResult(
        simulationResult
      );
    } catch {
      setError(
        "Unable to run security "
        + "control simulation.",
      );
    } finally {
      setRunning(false);
    }
  }


  return (
    <>
      <div className="page-heading">
        <div>
          <h2>
            Security Control Simulation
          </h2>

          <p>
            Compare baseline consequence
            against one or more modeled
            defensive controls.
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
                  event.target.value
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
              value={
                startAssetId
              }

              onChange={(event) => {
                setStartAssetId(
                  event.target.value
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
              value={
                startPrivilege
              }

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
        <div className="control-selection-heading">
          <div>
            <h3>
              Apply Controls
            </h3>

            <p>
              Controls are applied only to
              the temporary comparison
              scenario.
            </p>
          </div>

          <strong>
            {
              selectedControlIds.length
            }
            {" selected"}
          </strong>
        </div>


        {controls.length === 0 ? (
          <p>
            No security controls modeled.
          </p>
        ) : (
          <div className="control-selection-grid">
            {controls.map(
              (control) => (
                <label
                  className="control-selection-card"

                  key={
                    control.id
                  }
                >
                  <input
                    type="checkbox"

                    checked={
                      selectedControlIds
                        .includes(
                          control.id
                        )
                    }

                    onChange={() =>
                      toggleControl(
                        control.id
                      )
                    }
                  />

                  <div>
                    <strong>
                      {control.name}
                    </strong>

                    <span>
                      {
                        control
                          .control_type_display
                      }
                    </span>

                    <span>
                      {
                        control
                          .target_relationship_display

                        ?? control
                          .target_vulnerability_display

                        ?? "No target"
                      }
                    </span>
                  </div>
                </label>
              ),
            )}
          </div>
        )}


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
            ? "Simulating..."
            : "Simulate Controls"
          }
        </button>
      </section>


      {result && (
        <>
          <section className="panel">
            <h3>
              Baseline vs Controlled Scenario
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
                  Controlled
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
                  Essential Dependency Hits
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


          <section className="control-result-grid">
            <article className="panel">
              <h3>
                Applied Controls
              </h3>

              <div className="comparison-item-list">
                {result.applied_controls.map(
                  (control) => (
                    <div
                      key={
                        control.id
                      }
                    >
                      <strong>
                        {
                          control.name
                        }
                      </strong>

                      <span>
                        {
                          control
                            .control_type_display
                        }
                      </span>
                    </div>
                  ),
                )}
              </div>
            </article>


            <article className="panel">
              <h3>
                Prevented Assets
              </h3>

              {
                result
                  .comparison
                  .prevented_propagated_assets
                  .length === 0
              ? (
                <p>
                  No propagated assets were
                  prevented.
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
                Avoided Business Processes
              </h3>

              {
                result
                  .comparison
                  .avoided_business_processes
                  .length === 0
              ? (
                <p>
                  No business process was
                  completely avoided.
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
            <div className="simulation-semantics">
              {result.semantics}
            </div>
          </section>
        </>
      )}
    </>
  );
}
