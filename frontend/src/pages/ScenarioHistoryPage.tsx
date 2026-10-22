import {
  useEffect,
  useState,
} from "react";

import {
  listOrganizations,
} from "../api/organizations";

import {
  compareScenarioRuns,
  createScenarioRun,
  executeSavedScenario,
  listScenarioRuns,
  listScenarios,
} from "../api/scenarios";

import {
  extractComparableMetrics,
} from "../utils/scenarioMetrics";

import type {
  SavedScenario,
  ScenarioComparison,
  ScenarioRun,
} from "../types/scenarios";


interface OrganizationOption {
  id: number;

  name: string;
}


export default function ScenarioHistoryPage() {
  const [
    organizations,
    setOrganizations,
  ] = useState<
    OrganizationOption[]
  >([]);

  const [
    organizationId,
    setOrganizationId,
  ] = useState("");

  const [
    scenarios,
    setScenarios,
  ] = useState<
    SavedScenario[]
  >([]);

  const [
    selectedScenarioId,
    setSelectedScenarioId,
  ] = useState("");

  const [
    runs,
    setRuns,
  ] = useState<
    ScenarioRun[]
  >([]);

  const [
    beforeRunId,
    setBeforeRunId,
  ] = useState("");

  const [
    afterRunId,
    setAfterRunId,
  ] = useState("");

  const [
    comparison,
    setComparison,
  ] = useState<
    ScenarioComparison | null
  >(null);

  const [
    loading,
    setLoading,
  ] = useState(false);

  const [
    rerunning,
    setRerunning,
  ] = useState(false);

  const [
    error,
    setError,
  ] = useState("");


  const selectedScenario =
    scenarios.find(
      (scenario) =>
        String(
          scenario.id
        )
        === selectedScenarioId
    )
    ?? null;


  async function loadRuns(
    scenarioId: number,
  ) {
    const data =
      await listScenarioRuns(
        scenarioId
      );


    setRuns(
      data
    );


    const successfulRuns =
      data.filter(
        (run) =>
          run.status
          === "SUCCESS"
      );


    if (
      successfulRuns.length >= 2
    ) {
      setBeforeRunId(
        String(
          successfulRuns[1].id
        )
      );

      setAfterRunId(
        String(
          successfulRuns[0].id
        )
      );

    } else {
      setBeforeRunId("");
      setAfterRunId("");
    }


    setComparison(null);
  }


  async function loadScenariosForOrganization(
    nextOrganizationId: number,
  ) {
    const data =
      await listScenarios(
        nextOrganizationId
      );


    setScenarios(
      data
    );

    setSelectedScenarioId("");
    setRuns([]);
    setBeforeRunId("");
    setAfterRunId("");
    setComparison(null);
  }


  useEffect(
    () => {
      let cancelled = false;


      async function loadInitialData() {
        setLoading(true);
        setError("");


        try {
          const data =
            await listOrganizations();


          if (cancelled) {
            return;
          }


          setOrganizations(
            data
          );


          if (
            data.length > 0
          ) {
            const firstId =
              data[0].id;


            setOrganizationId(
              String(
                firstId
              )
            );


            const scenarioData =
              await listScenarios(
                firstId
              );


            if (cancelled) {
              return;
            }


            setScenarios(
              scenarioData
            );
          }

        } catch (caughtError) {
          if (!cancelled) {
            setError(
              caughtError
                instanceof Error
                ? caughtError.message
                : (
                    "Unable to load "
                    + "scenario history."
                  )
            );
          }

        } finally {
          if (!cancelled) {
            setLoading(false);
          }
        }
      }


      void loadInitialData();


      return () => {
        cancelled = true;
      };
    },
    [],
  );


  async function handleOrganizationChange(
    value: string,
  ) {
    setOrganizationId(
      value
    );

    setError("");


    if (!value) {
      setScenarios([]);
      setSelectedScenarioId("");
      setRuns([]);

      return;
    }


    try {
      await loadScenariosForOrganization(
        Number(
          value
        )
      );

    } catch (caughtError) {
      setError(
        caughtError
          instanceof Error
          ? caughtError.message
          : "Unable to load scenarios."
      );
    }
  }


  async function handleScenarioSelect(
    value: string,
  ) {
    setSelectedScenarioId(
      value
    );

    setRuns([]);
    setComparison(null);
    setError("");


    if (!value) {
      return;
    }


    try {
      await loadRuns(
        Number(
          value
        )
      );

    } catch (caughtError) {
      setError(
        caughtError
          instanceof Error
          ? caughtError.message
          : "Unable to load runs."
      );
    }
  }


  async function handleRerun() {
    if (
      selectedScenario
      === null
    ) {
      return;
    }


    setRerunning(true);
    setError("");
    setComparison(null);


    try {
      const result =
        await executeSavedScenario(
          selectedScenario
        );


      const metrics =
        extractComparableMetrics(
          selectedScenario
            .simulation_type,

          result,
        );


      await createScenarioRun(
        selectedScenario.id,

        {
          label:
            "Rerun from saved request",

          status:
            "SUCCESS",

          request_payload:
            selectedScenario
              .request_payload,

          result_payload:
            result,

          metrics,
        },
      );


      await loadRuns(
        selectedScenario.id
      );


      await loadScenariosForOrganization(
        selectedScenario.organization
      );


      setSelectedScenarioId(
        String(
          selectedScenario.id
        )
      );


      await loadRuns(
        selectedScenario.id
      );

    } catch (caughtError) {
      const message =
        caughtError
          instanceof Error
          ? caughtError.message
          : "Scenario rerun failed.";


      try {
        await createScenarioRun(
          selectedScenario.id,

          {
            label:
              "Failed rerun",

            status:
              "FAILED",

            request_payload:
              selectedScenario
                .request_payload,

            result_payload:
              {},

            metrics:
              {},

            error_message:
              message,
          },
        );


        await loadRuns(
          selectedScenario.id
        );

      } catch {
        // Keep the original rerun error.
      }


      setError(
        message
      );

    } finally {
      setRerunning(false);
    }
  }


  async function handleCompare() {
    if (
      selectedScenario
      === null
      || !beforeRunId
      || !afterRunId
    ) {
      return;
    }


    setError("");


    try {
      const data =
        await compareScenarioRuns(
          selectedScenario.id,

          Number(
            beforeRunId
          ),

          Number(
            afterRunId
          ),
        );


      setComparison(
        data
      );

    } catch (caughtError) {
      setError(
        caughtError
          instanceof Error
          ? caughtError.message
          : (
              "Unable to compare runs."
            )
      );
    }
  }


  return (
    <div className="page">
      <div className="page-header">
        <div>
          <h2>
            Saved Scenarios
          </h2>

          <p>
            Rerun the same modeled
            simulation request after
            environment changes and
            compare historical results.
          </p>
        </div>
      </div>


      {error && (
        <div className="error-box">
          {error}
        </div>
      )}


      <section className="panel">
        <div className="form-grid">
          <label>
            Organization

            <select
              value={
                organizationId
              }

              onChange={(event) => {
                void handleOrganizationChange(
                  event.target.value
                );
              }}
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
            Saved Scenario

            <select
              value={
                selectedScenarioId
              }

              onChange={(event) => {
                void handleScenarioSelect(
                  event.target.value
                );
              }}
            >
              <option value="">
                Select a scenario
              </option>

              {scenarios.map(
                (scenario) => (
                  <option
                    key={
                      scenario.id
                    }

                    value={
                      scenario.id
                    }
                  >
                    {
                      scenario.name
                    }
                    {" — "}
                    {
                      scenario
                        .simulation_type
                    }
                  </option>
                ),
              )}
            </select>
          </label>
        </div>


        {loading && (
          <p>
            Loading...
          </p>
        )}


        {!loading
          && scenarios.length === 0
          && (
            <p>
              No saved scenarios exist
              for this organization yet.
            </p>
          )}
      </section>


      {selectedScenario && (
        <>
          <section className="panel scenario-summary">
            <h3>
              {
                selectedScenario.name
              }
            </h3>

            <p>
              {
                selectedScenario.description
                || (
                  "No description provided."
                )
              }
            </p>

            <div className="scenario-meta-grid">
              <div>
                <strong>
                  Simulation Type
                </strong>

                <span>
                  {
                    selectedScenario
                      .simulation_type
                  }
                </span>
              </div>

              <div>
                <strong>
                  Runs
                </strong>

                <span>
                  {
                    selectedScenario
                      .run_count
                  }
                </span>
              </div>

              <div>
                <strong>
                  Latest Run
                </strong>

                <span>
                  {
                    selectedScenario
                      .latest_run_number
                    ?? "None"
                  }
                </span>
              </div>
            </div>

            <button
              type="button"

              onClick={
                handleRerun
              }

              disabled={
                rerunning
              }
            >
              {
                rerunning
                  ? "Running..."
                  : "Rerun Saved Scenario"
              }
            </button>
          </section>


          <section className="panel">
            <h3>
              Run History
            </h3>

            {runs.length === 0 && (
              <p>
                This scenario has no
                saved runs yet.
              </p>
            )}

            <div className="scenario-run-list">
              {runs.map(
                (run) => (
                  <article
                    key={
                      run.id
                    }

                    className="scenario-run-card"
                  >
                    <div>
                      <strong>
                        Run #
                        {
                          run.run_number
                        }
                      </strong>

                      <span>
                        {
                          run.label
                          || "Simulation run"
                        }
                      </span>
                    </div>

                    <div>
                      <span>
                        Status:
                        {" "}
                        {
                          run.status
                        }
                      </span>

                      <span>
                        {
                          new Date(
                            run.created_at
                          )
                            .toLocaleString()
                        }
                      </span>
                    </div>

                    {run.status
                      === "FAILED"
                      && (
                        <div className="error-box">
                          {
                            run.error_message
                          }
                        </div>
                      )}
                  </article>
                ),
              )}
            </div>
          </section>


          <section className="panel">
            <h3>
              Before / After Comparison
            </h3>

            <div className="form-grid">
              <label>
                Before Run

                <select
                  value={
                    beforeRunId
                  }

                  onChange={(event) =>
                    setBeforeRunId(
                      event.target.value
                    )
                  }
                >
                  <option value="">
                    Select run
                  </option>

                  {runs
                    .filter(
                      (run) =>
                        run.status
                        === "SUCCESS"
                    )
                    .map(
                      (run) => (
                        <option
                          key={
                            run.id
                          }

                          value={
                            run.id
                          }
                        >
                          Run #
                          {
                            run.run_number
                          }
                          {" — "}
                          {
                            run.label
                          }
                        </option>
                      ),
                    )}
                </select>
              </label>


              <label>
                After Run

                <select
                  value={
                    afterRunId
                  }

                  onChange={(event) =>
                    setAfterRunId(
                      event.target.value
                    )
                  }
                >
                  <option value="">
                    Select run
                  </option>

                  {runs
                    .filter(
                      (run) =>
                        run.status
                        === "SUCCESS"
                    )
                    .map(
                      (run) => (
                        <option
                          key={
                            run.id
                          }

                          value={
                            run.id
                          }
                        >
                          Run #
                          {
                            run.run_number
                          }
                          {" — "}
                          {
                            run.label
                          }
                        </option>
                      ),
                    )}
                </select>
              </label>
            </div>

            <button
              type="button"

              onClick={
                handleCompare
              }

              disabled={
                !beforeRunId
                || !afterRunId
              }
            >
              Compare Runs
            </button>
          </section>


          {comparison && (
            <section className="panel">
              <h3>
                Comparison Result
              </h3>

              {comparison.metrics.length
                === 0
                ? (
                    <p>
                      These runs do not
                      contain shared
                      comparable metrics.
                    </p>
                  )
                : (
                    <div className="table-wrap">
                      <table className="scenario-comparison-table">
                        <thead>
                          <tr>
                            <th>
                              Metric
                            </th>

                            <th>
                              Before
                            </th>

                            <th>
                              After
                            </th>

                            <th>
                              Reduction
                            </th>

                            <th>
                              Result
                            </th>
                          </tr>
                        </thead>

                        <tbody>
                          {comparison
                            .metrics
                            .map(
                              (metric) => (
                                <tr
                                  key={
                                    metric.metric
                                  }
                                >
                                  <td>
                                    {
                                      metric.label
                                    }
                                  </td>

                                  <td>
                                    {
                                      metric.before
                                    }
                                  </td>

                                  <td>
                                    {
                                      metric.after
                                    }
                                  </td>

                                  <td>
                                    {
                                      metric.reduction
                                    }
                                  </td>

                                  <td>
                                    <span
                                      className={
                                        (
                                          "scenario-diff "
                                          + (
                                            `scenario-diff-`
                                            + metric
                                              .interpretation
                                              .toLowerCase()
                                          )
                                        )
                                      }
                                    >
                                      {
                                        metric
                                          .interpretation
                                      }
                                    </span>
                                  </td>
                                </tr>
                              ),
                            )}
                        </tbody>
                      </table>
                    </div>
                  )}

              <p className="scenario-disclaimer">
                {
                  comparison.disclaimer
                }
              </p>
            </section>
          )}
        </>
      )}
    </div>
  );
}
