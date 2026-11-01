import {
  useEffect,
  useState,
} from "react";

import {
  listOrganizations,
} from "../api/organizations";

import {
  listScenarioRuns,
  listScenarios,
} from "../api/scenarios";

import {
  getIngestionEnvironmentUrl,
  getPortableEnvironmentUrl,
  getReportingSummary,
  getRunMetricsCsvUrl,
  getRunReportUrl,
  getScenarioExportUrl,
} from "../api/reporting";

import type {
  SavedScenario,
  ScenarioRun,
} from "../types/scenarios";

import type {
  ReportingSummary,
} from "../types/reporting";


interface OrganizationOption {
  id: number;

  name: string;
}


export default function ReportsPage() {
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
    summary,
    setSummary,
  ] = useState<
    ReportingSummary | null
  >(null);

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
    runId,
    setRunId,
  ] = useState("");

  const [
    loading,
    setLoading,
  ] = useState(false);

  const [
    error,
    setError,
  ] = useState("");


  async function loadOrganizationData(
    nextOrganizationId: number,
  ) {
    const [
      summaryData,
      scenarioData,
    ] = await Promise.all(
      [
        getReportingSummary(
          nextOrganizationId
        ),

        listScenarios(
          nextOrganizationId
        ),
      ],
    );


    setSummary(
      summaryData
    );

    setScenarios(
      scenarioData
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
              data[
                0
              ].id;


            setOrganizationId(
              String(
                firstId
              )
            );


            const [
              summaryData,
              scenarioData,
            ] = await Promise.all(
              [
                getReportingSummary(
                  firstId
                ),

                listScenarios(
                  firstId
                ),
              ],
            );


            if (cancelled) {
              return;
            }


            setSummary(
              summaryData
            );

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
                    + "reporting data."
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
    setRunId("");
    setRuns([]);
    setError("");


    if (!value) {
      setSummary(null);
      setScenarios([]);

      return;
    }


    try {
      await loadOrganizationData(
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
              + "organization reports."
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

    setRunId("");
    setRuns([]);
    setError("");


    if (!value) {
      return;
    }


    try {
      const runData =
        await listScenarioRuns(
          Number(
            value
          )
        );


      setRuns(
        runData
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


  function downloadUrl(
    url: string,
  ) {
    window.open(
      url,
      "_blank",
      "noopener,noreferrer",
    );
  }


  return (
    <div className="page">
      <div className="page-header">
        <div>
          <h2>
            Import / Export & Reports
          </h2>

          <p>
            Export RiftTrace environments,
            saved scenarios and simulation
            results in machine-readable
            formats.
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
          Organization
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


      {summary && (
        <section className="stats-grid">
          <article>
            <strong>
              Assets
            </strong>

            <span>
              {
                summary
                  .environment
                  .assets
              }
            </span>
          </article>

          <article>
            <strong>
              Relationships
            </strong>

            <span>
              {
                summary
                  .environment
                  .relationships
              }
            </span>
          </article>

          <article>
            <strong>
              Vulnerabilities
            </strong>

            <span>
              {
                summary
                  .environment
                  .vulnerabilities
              }
            </span>
          </article>

          <article>
            <strong>
              Saved Runs
            </strong>

            <span>
              {
                summary
                  .scenarios
                  .runs
              }
            </span>
          </article>
        </section>
      )}


      <section className="panel">
        <h3>
          Environment Export
        </h3>

        <p>
          Portable JSON includes schema,
          organization metadata and an
          integrity hash. Ingestion JSON
          is designed for the existing
          RiftTrace environment importer.
        </p>

        <div className="report-actions">
          <button
            type="button"

            disabled={
              !organizationId
            }

            onClick={() => {
              downloadUrl(
                getPortableEnvironmentUrl(
                  Number(
                    organizationId
                  )
                )
              );
            }}
          >
            Export Portable JSON
          </button>

          <button
            type="button"

            disabled={
              !organizationId
            }

            onClick={() => {
              downloadUrl(
                getIngestionEnvironmentUrl(
                  Number(
                    organizationId
                  )
                )
              );
            }}
          >
            Export Ingestion JSON
          </button>
        </div>
      </section>


      <section className="panel">
        <h3>
          Saved Scenario Export
        </h3>

        <label>
          Scenario

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

        <button
          type="button"

          disabled={
            !scenarioId
          }

          onClick={() => {
            downloadUrl(
              getScenarioExportUrl(
                Number(
                  scenarioId
                )
              )
            );
          }}
        >
          Export Scenario JSON
        </button>
      </section>


      <section className="panel">
        <h3>
          Simulation Run Report
        </h3>

        <label>
          Run

          <select
            value={
              runId
            }

            disabled={
              !scenarioId
            }

            onChange={(event) =>
              setRunId(
                event.target.value
              )
            }
          >
            <option value="">
              Select run
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
                    run.status
                  }
                </option>
              ),
            )}
          </select>
        </label>

        <div className="report-actions">
          <button
            type="button"

            disabled={
              !runId
            }

            onClick={() => {
              downloadUrl(
                getRunReportUrl(
                  Number(
                    runId
                  )
                )
              );
            }}
          >
            Export Run JSON
          </button>

          <button
            type="button"

            disabled={
              !runId
            }

            onClick={() => {
              downloadUrl(
                getRunMetricsCsvUrl(
                  Number(
                    runId
                  )
                )
              );
            }}
          >
            Export Metrics CSV
          </button>
        </div>
      </section>


      <section className="panel">
        <h3>
          Interpretation
        </h3>

        <p>
          Exported simulation reports
          describe modeled RiftTrace
          scenarios and consequences.
          They do not represent observed
          attacker activity or guaranteed
          real-world security outcomes.
        </p>
      </section>
    </div>
  );
}
