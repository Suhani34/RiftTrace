import {
  useEffect,
  useState,
} from "react";

import {
  Bar,
  BarChart,
  CartesianGrid,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis,
} from "recharts";

import {
  listOrganizations,
} from "../api/organizations";

import {
  listScenarioRuns,
  listScenarios,
} from "../api/scenarios";

import {
  createEvaluationExperiment,
  getEvaluationExportUrl,
  getEvaluationSummary,
  listEvaluationExperiments,
} from "../api/evaluation";

import type {
  SavedScenario,
  ScenarioRun,
} from "../types/scenarios";

import type {
  EvaluationExperiment,
  EvaluationSummary,
} from "../types/evaluation";


interface OrganizationOption {
  id: number;

  name: string;
}


export default function EvaluationPage() {
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
    scenarioId,
    setScenarioId,
  ] = useState("");

  const [
    runs,
    setRuns,
  ] = useState<
    ScenarioRun[]
  >([]);

  const [
    baselineRunId,
    setBaselineRunId,
  ] = useState("");

  const [
    treatmentRunId,
    setTreatmentRunId,
  ] = useState("");

  const [
    experimentName,
    setExperimentName,
  ] = useState("");

  const [
    interventionLabel,
    setInterventionLabel,
  ] = useState("");

  const [
    notes,
    setNotes,
  ] = useState("");

  const [
    experiments,
    setExperiments,
  ] = useState<
    EvaluationExperiment[]
  >([]);

  const [
    summary,
    setSummary,
  ] = useState<
    EvaluationSummary | null
  >(null);

  const [
    loading,
    setLoading,
  ] = useState(false);

  const [
    saving,
    setSaving,
  ] = useState(false);

  const [
    error,
    setError,
  ] = useState("");

  const [
    success,
    setSuccess,
  ] = useState("");


  async function loadEvaluationData(
    nextOrganizationId: number,
  ) {
    const [
      scenarioData,
      experimentData,
      summaryData,
    ] = await Promise.all(
      [
        listScenarios(
          nextOrganizationId
        ),

        listEvaluationExperiments(
          nextOrganizationId
        ),

        getEvaluationSummary(
          nextOrganizationId
        ),
      ],
    );


    setScenarios(
      scenarioData
    );

    setExperiments(
      experimentData
    );

    setSummary(
      summaryData
    );
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


            const [
              scenarioData,
              experimentData,
              summaryData,
            ] = await Promise.all(
              [
                listScenarios(
                  firstId
                ),

                listEvaluationExperiments(
                  firstId
                ),

                getEvaluationSummary(
                  firstId
                ),
              ],
            );


            if (cancelled) {
              return;
            }


            setScenarios(
              scenarioData
            );

            setExperiments(
              experimentData
            );

            setSummary(
              summaryData
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
                    + "evaluation data."
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

    setScenarioId("");
    setRuns([]);
    setBaselineRunId("");
    setTreatmentRunId("");
    setError("");
    setSuccess("");


    if (!value) {
      setScenarios([]);
      setExperiments([]);
      setSummary(null);

      return;
    }


    try {
      await loadEvaluationData(
        Number(
          value
        )
      );

    } catch (caughtError) {
      setError(
        caughtError
          instanceof Error
          ? caughtError.message
          : (
              "Unable to load "
              + "evaluation data."
            )
      );
    }
  }


  async function handleScenarioChange(
    value: string,
  ) {
    setScenarioId(
      value
    );

    setBaselineRunId("");
    setTreatmentRunId("");
    setRuns([]);
    setError("");
    setSuccess("");


    if (!value) {
      return;
    }


    try {
      const data =
        await listScenarioRuns(
          Number(
            value
          )
        );


      setRuns(
        data.filter(
          (run) =>
            run.status
            === "SUCCESS"
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


  async function handleCreateExperiment() {
    if (
      !organizationId
      || !scenarioId
      || !baselineRunId
      || !treatmentRunId
      || !experimentName.trim()
      || !interventionLabel.trim()
    ) {
      setError(
        (
          "Complete all required "
          + "evaluation fields."
        )
      );

      return;
    }


    setSaving(true);
    setError("");
    setSuccess("");


    try {
      await createEvaluationExperiment(
        {
          organization:
            Number(
              organizationId
            ),

          name:
            experimentName.trim(),

          scenario:
            Number(
              scenarioId
            ),

          baseline_run:
            Number(
              baselineRunId
            ),

          treatment_run:
            Number(
              treatmentRunId
            ),

          intervention_label:
            interventionLabel.trim(),

          notes:
            notes.trim(),
        },
      );


      await loadEvaluationData(
        Number(
          organizationId
        )
      );


      setExperimentName("");
      setInterventionLabel("");
      setNotes("");
      setBaselineRunId("");
      setTreatmentRunId("");


      setSuccess(
        "Evaluation experiment saved."
      );

    } catch (caughtError) {
      setError(
        caughtError
          instanceof Error
          ? caughtError.message
          : (
              "Unable to save "
              + "evaluation experiment."
            )
      );

    } finally {
      setSaving(false);
    }
  }


  function handleExport() {
    if (!organizationId) {
      return;
    }


    window.open(
      getEvaluationExportUrl(
        Number(
          organizationId
        )
      ),

      "_blank",
      "noopener,noreferrer",
    );
  }


  return (
    <div className="page">
      <div className="page-header">
        <div>
          <h2>
            Research Evaluation
          </h2>

          <p>
            Compare baseline and
            post-intervention simulation
            runs using reproducible,
            descriptive model metrics.
          </p>
        </div>
      </div>


      {error && (
        <div className="error-box">
          {error}
        </div>
      )}


      {success && (
        <div className="success-box">
          {success}
        </div>
      )}


      <section className="panel">
        <h3>
          Evaluation Scope
        </h3>

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

        {loading && (
          <p>
            Loading...
          </p>
        )}
      </section>


      <section className="panel">
        <h3>
          Create Evaluation Experiment
        </h3>

        <p>
          Select two successful runs
          of the same saved scenario.
          The earlier run is the
          baseline and the later run
          represents the modeled
          intervention.
        </p>

        <div className="form-grid">
          <label>
            Saved Scenario

            <select
              value={
                scenarioId
              }

              onChange={(event) => {
                void handleScenarioChange(
                  event.target.value
                );
              }}
            >
              <option value="">
                Select scenario
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
                      scenario.simulation_type
                    }
                  </option>
                ),
              )}
            </select>
          </label>


          <label>
            Baseline Run

            <select
              value={
                baselineRunId
              }

              onChange={(event) =>
                setBaselineRunId(
                  event.target.value
                )
              }
            >
              <option value="">
                Select baseline
              </option>

              {runs.map(
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
                      || "Simulation run"
                    }
                  </option>
                ),
              )}
            </select>
          </label>


          <label>
            Treatment Run

            <select
              value={
                treatmentRunId
              }

              onChange={(event) =>
                setTreatmentRunId(
                  event.target.value
                )
              }
            >
              <option value="">
                Select treatment
              </option>

              {runs.map(
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
                      || "Simulation run"
                    }
                  </option>
                ),
              )}
            </select>
          </label>


          <label>
            Experiment Name

            <input
              value={
                experimentName
              }

              onChange={(event) =>
                setExperimentName(
                  event.target.value
                )
              }

              placeholder={
                "Example: MFA Experiment"
              }
            />
          </label>


          <label>
            Intervention

            <input
              value={
                interventionLabel
              }

              onChange={(event) =>
                setInterventionLabel(
                  event.target.value
                )
              }

              placeholder={
                (
                  "Example: Require MFA "
                  + "for DB administration"
                )
              }
            />
          </label>


          <label>
            Notes

            <input
              value={
                notes
              }

              onChange={(event) =>
                setNotes(
                  event.target.value
                )
              }

              placeholder={
                (
                  "Optional experiment "
                  + "notes"
                )
              }
            />
          </label>
        </div>

        <button
          type="button"

          onClick={
            handleCreateExperiment
          }

          disabled={
            saving
          }
        >
          {
            saving
              ? "Saving..."
              : "Save Experiment"
          }
        </button>
      </section>


      {summary && (
        <>
          <section className="stats-grid">
            <article>
              <strong>
                Experiments
              </strong>

              <span>
                {
                  summary
                    .experiment_count
                }
              </span>
            </article>

            <article>
              <strong>
                Improved
              </strong>

              <span>
                {
                  summary
                    .improved_observations
                }
              </span>
            </article>

            <article>
              <strong>
                Unchanged
              </strong>

              <span>
                {
                  summary
                    .unchanged_observations
                }
              </span>
            </article>

            <article>
              <strong>
                Worsened
              </strong>

              <span>
                {
                  summary
                    .worsened_observations
                }
              </span>
            </article>
          </section>


          <section className="panel">
            <div className="panel-header-row">
              <div>
                <h3>
                  Mean Modeled Reduction
                </h3>

                <p>
                  Positive values indicate
                  fewer modeled exposure
                  outcomes after the
                  intervention.
                </p>
              </div>

              <button
                type="button"

                onClick={
                  handleExport
                }
              >
                Export CSV
              </button>
            </div>

            {summary.metrics.length === 0
              ? (
                  <p>
                    No evaluation metrics
                    exist yet.
                  </p>
                )
              : (
                  <div className="evaluation-chart">
                    <ResponsiveContainer
                      width="100%"
                      height={320}
                    >
                      <BarChart
                        data={
                          summary.metrics
                        }
                      >
                        <CartesianGrid
                          strokeDasharray="3 3"
                        />

                        <XAxis
                          dataKey="label"
                        />

                        <YAxis />

                        <Tooltip />

                        <Bar
                          dataKey={
                            "mean_reduction"
                          }
                        />
                      </BarChart>
                    </ResponsiveContainer>
                  </div>
                )}
          </section>


          <section className="panel">
            <h3>
              Metric Summary
            </h3>

            <div className="table-wrap">
              <table className="evaluation-table">
                <thead>
                  <tr>
                    <th>
                      Metric
                    </th>

                    <th>
                      N
                    </th>

                    <th>
                      Mean Before
                    </th>

                    <th>
                      Mean After
                    </th>

                    <th>
                      Mean Reduction
                    </th>

                    <th>
                      Improved
                    </th>

                    <th>
                      Unchanged
                    </th>

                    <th>
                      Worsened
                    </th>
                  </tr>
                </thead>

                <tbody>
                  {summary.metrics.map(
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
                            metric.observations
                          }
                        </td>

                        <td>
                          {
                            metric.mean_before
                          }
                        </td>

                        <td>
                          {
                            metric.mean_after
                          }
                        </td>

                        <td>
                          {
                            metric.mean_reduction
                          }
                        </td>

                        <td>
                          {
                            metric.improved
                          }
                        </td>

                        <td>
                          {
                            metric.unchanged
                          }
                        </td>

                        <td>
                          {
                            metric.worsened
                          }
                        </td>
                      </tr>
                    ),
                  )}
                </tbody>
              </table>
            </div>

            <p className="evaluation-disclaimer">
              {
                summary.disclaimer
              }
            </p>
          </section>
        </>
      )}


      <section className="panel">
        <h3>
          Experiment Records
        </h3>

        {experiments.length === 0
          ? (
              <p>
                No evaluation experiments
                have been saved yet.
              </p>
            )
          : (
              <div className="evaluation-experiment-list">
                {experiments.map(
                  (experiment) => (
                    <article
                      key={
                        experiment.id
                      }

                      className={
                        "evaluation-experiment-card"
                      }
                    >
                      <h4>
                        {
                          experiment.name
                        }
                      </h4>

                      <p>
                        <strong>
                          Scenario:
                        </strong>
                        {" "}
                        {
                          experiment
                            .scenario_name
                        }
                      </p>

                      <p>
                        <strong>
                          Intervention:
                        </strong>
                        {" "}
                        {
                          experiment
                            .intervention_label
                        }
                      </p>

                      <p>
                        Run #
                        {
                          experiment
                            .baseline_run_number
                        }
                        {" → "}
                        Run #
                        {
                          experiment
                            .treatment_run_number
                        }
                      </p>

                      {experiment
                        .comparison
                        .map(
                          (metric) => (
                            <div
                              key={
                                metric.metric
                              }

                              className={
                                "evaluation-result-row"
                              }
                            >
                              <span>
                                {
                                  metric.label
                                }
                              </span>

                              <span>
                                {
                                  metric.before
                                }
                                {" → "}
                                {
                                  metric.after
                                }
                              </span>

                              <strong>
                                {
                                  metric
                                    .interpretation
                                }
                              </strong>
                            </div>
                          ),
                        )}
                    </article>
                  ),
                )}
              </div>
            )}
      </section>
    </div>
  );
}
