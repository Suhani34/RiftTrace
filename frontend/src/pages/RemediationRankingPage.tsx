import {
  useEffect,
  useState,
} from "react";

import {
  listOrganizations,
} from "../api/organizations";

import {
  listSecurityControls,
} from "../api/securityControls";

import {
  runControlRanking,
} from "../api/simulations";

import {
  getOrganizationTopology,
} from "../api/topology";

import type {
  Organization,
  OrganizationTopology,
} from "../types/models";

import type {
  SecurityControl,
} from "../types/securityControl";

import type {
  ControlRankingResult,
} from "../types/prioritization";


export default function RemediationRankingPage() {
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
    selectedControlIds,
    setSelectedControlIds,
  ] = useState<number[]>([]);


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
    result,
    setResult,
  ] = useState<
    ControlRankingResult
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


    setSelectedControlIds(
      controlData.map(
        (control) =>
          control.id,
      )
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


        setSelectedControlIds(
          controlData.map(
            (control) =>
              control.id,
          )
        );
      } catch {
        if (!cancelled) {
          setError(
            "Unable to load "
            + "remediation ranking data.",
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


  function selectAllControls() {
    setSelectedControlIds(
      controls.map(
        (control) =>
          control.id,
      )
    );


    setResult(null);
  }


  function clearControls() {
    setSelectedControlIds([]);

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
        + "candidate security control.",
      );

      return;
    }


    try {
      setRunning(true);

      setError("");


      const rankingResult =
        await runControlRanking(
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
        rankingResult
      );
    } catch {
      setError(
        "Unable to rank candidate "
        + "security controls.",
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
            Remediation Ranking
          </h2>

          <p>
            Rank candidate defensive
            controls by modeled technical
            and business consequence
            reduction.
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
          Attack Scenario
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
              value={startAssetId}

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
                      key={
                        asset.id
                      }

                      value={
                        asset.id
                      }
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
        <div className="ranking-selection-heading">
          <div>
            <h3>
              Candidate Controls
            </h3>

            <p>
              Select which controls RiftTrace
              should evaluate independently
              against the same baseline.
            </p>
          </div>

          <strong>
            {
              selectedControlIds
                .length
            }
            {" selected"}
          </strong>
        </div>


        <div className="ranking-selection-actions">
          <button
            type="button"

            className="secondary-button"

            onClick={
              selectAllControls
            }
          >
            Select All
          </button>


          <button
            type="button"

            className="secondary-button"

            onClick={
              clearControls
            }
          >
            Clear
          </button>
        </div>


        {controls.length === 0 ? (
          <p>
            No candidate security controls
            have been modeled.
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
            || selectedControlIds
              .length === 0
          }

          onClick={() => {
            void handleRun();
          }}
        >
          {
            running
            ? "Ranking..."
            : "Rank Candidate Controls"
          }
        </button>
      </section>


      {result && (
        <>
          <section className="panel">
            <h3>
              Ranking Method
            </h3>

            <p>
              {
                result
                  .ranking_method
                  .strategy
              }
            </p>


            <div className="ranking-method-order">
              {
                result
                  .ranking_method
                  .priority_order
                  .map(
                    (
                      item,
                      index,
                    ) => (
                      <div
                        key={
                          item
                        }
                      >
                        <strong>
                          {
                            index + 1
                          }
                        </strong>

                        <span>
                          {item}
                        </span>
                      </div>
                    ),
                  )
              }
            </div>


            <p>
              {
                result
                  .ranking_method
                  .tie_behavior
              }
            </p>
          </section>


          <section className="panel">
            <div className="ranking-results-heading">
              <div>
                <h3>
                  Recommended Priority
                </h3>

                <p>
                  {
                    result
                      .candidate_control_count
                  }
                  {" candidate control(s) evaluated."}
                </p>
              </div>
            </div>


            <div className="ranking-result-list">
              {
                result
                  .ranked_controls
                  .map(
                    (item) => (
                      <article
                        className={
                          "ranking-result-card"
                          + (
                            item
                              .has_measured_effect
                              ? ""
                              : " ranking-no-effect"
                          )
                        }

                        key={
                          item
                            .control
                            .id
                        }
                      >
                        <div className="ranking-result-header">
                          <div className="ranking-number">
                            <span>
                              Rank
                            </span>

                            <strong>
                              #
                              {
                                item.rank
                              }
                            </strong>
                          </div>


                          <div className="ranking-control-title">
                            <strong>
                              {
                                item
                                  .control
                                  .name
                              }
                            </strong>

                            <span>
                              {
                                item
                                  .control
                                  .control_type_display
                              }
                            </span>

                            {
                              item.tied
                              && (
                                <span className="ranking-tie">
                                  Tied
                                </span>
                              )
                            }
                          </div>
                        </div>


                        <p>
                          Target:
                          {" "}
                          {
                            item
                              .control
                              .target_relationship_display

                            ?? item
                              .control
                              .target_vulnerability_display

                            ?? "None"
                          }
                        </p>


                        <p className="ranking-reason">
                          {
                            item
                              .priority_reason
                          }
                        </p>


                        <div className="ranking-metric-grid">
                          <div>
                            <span>
                              Critical Processes
                            </span>

                            <strong>
                              {
                                item
                                  .metrics
                                  .critical_process_reduction
                              }
                            </strong>
                          </div>


                          <div>
                            <span>
                              Critical Assets
                            </span>

                            <strong>
                              {
                                item
                                  .metrics
                                  .critical_asset_reduction
                              }
                            </strong>
                          </div>


                          <div>
                            <span>
                              Essential Dependencies
                            </span>

                            <strong>
                              {
                                item
                                  .metrics
                                  .essential_dependency_hit_reduction
                              }
                            </strong>
                          </div>


                          <div>
                            <span>
                              Processes Avoided
                            </span>

                            <strong>
                              {
                                item
                                  .metrics
                                  .impacted_process_reduction
                              }
                            </strong>
                          </div>


                          <div>
                            <span>
                              Assets Prevented
                            </span>

                            <strong>
                              {
                                item
                                  .metrics
                                  .propagated_asset_reduction
                              }
                            </strong>
                          </div>
                        </div>


                        {!item
                          .has_measured_effect
                        && (
                          <div className="ranking-zero-message">
                            No measurable reduction
                            for this specific
                            attack scenario.
                          </div>
                        )}
                      </article>
                    ),
                  )
              }
            </div>
          </section>


          <section className="panel">
            <h3>
              Interpretation
            </h3>

            <div className="simulation-semantics">
              {result.semantics}
            </div>


            <p>
              A lower-ranked control may still
              be valuable for a different
              starting asset, privilege level,
              attack path, operational
              requirement or threat scenario.
            </p>
          </section>
        </>
      )}
    </>
  );
}
