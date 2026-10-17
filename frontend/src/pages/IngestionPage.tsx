import {
  useEffect,
  useState,
} from "react";

import {
  listOrganizations,
} from "../api/organizations";

import {
  applyIngestion,
  listIngestionRuns,
  previewIngestion,
} from "../api/ingestion";

import type {
  Organization,
} from "../types/models";

import type {
  IngestionPlan,
  IngestionRun,
  IngestionSourceFormat,
} from "../types/ingestion";


export default function IngestionPage() {
  const [
    organizations,
    setOrganizations,
  ] = useState<Organization[]>([]);


  const [
    organizationId,
    setOrganizationId,
  ] = useState("");


  const [
    sourceFormat,
    setSourceFormat,
  ] = useState<
    IngestionSourceFormat
  >("JSON");


  const [
    bundleFile,
    setBundleFile,
  ] = useState<
    File | null
  >(null);


  const [
    zonesFile,
    setZonesFile,
  ] = useState<
    File | null
  >(null);


  const [
    assetsFile,
    setAssetsFile,
  ] = useState<
    File | null
  >(null);


  const [
    relationshipsFile,
    setRelationshipsFile,
  ] = useState<
    File | null
  >(null);


  const [
    vulnerabilitiesFile,
    setVulnerabilitiesFile,
  ] = useState<
    File | null
  >(null);


  const [
    preview,
    setPreview,
  ] = useState<
    IngestionPlan | null
  >(null);


  const [
    history,
    setHistory,
  ] = useState<
    IngestionRun[]
  >([]);


  const [
    working,
    setWorking,
  ] = useState(false);


  const [
    error,
    setError,
  ] = useState("");


  function clearPreview() {
    setPreview(null);

    setError("");
  }


  function clearFiles() {
    setBundleFile(null);

    setZonesFile(null);

    setAssetsFile(null);

    setRelationshipsFile(null);

    setVulnerabilitiesFile(null);

    clearPreview();
  }


  function buildFormData() {
    const formData =
      new FormData();


    formData.append(
      "organization",
      organizationId,
    );


    formData.append(
      "source_format",
      sourceFormat,
    );


    if (
      sourceFormat
      === "JSON"
    ) {
      if (bundleFile) {
        formData.append(
          "bundle_file",
          bundleFile,
        );
      }
    } else {
      if (zonesFile) {
        formData.append(
          "network_zones_file",
          zonesFile,
        );
      }


      if (assetsFile) {
        formData.append(
          "assets_file",
          assetsFile,
        );
      }


      if (
        relationshipsFile
      ) {
        formData.append(
          "relationships_file",
          relationshipsFile,
        );
      }


      if (
        vulnerabilitiesFile
      ) {
        formData.append(
          "vulnerabilities_file",
          vulnerabilitiesFile,
        );
      }
    }


    return formData;
  }


  async function refreshHistory(
    selectedOrganizationId:
      number,
  ) {
    const data =
      await listIngestionRuns(
        selectedOrganizationId
      );


    setHistory(
      data
    );
  }


  useEffect(() => {
    let cancelled =
      false;


    async function initialize() {
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
          data.length
          === 0
        ) {
          return;
        }


        const initial =
          data.find(
            (organization) =>
              organization.name
              === "RiftTrace Labs",
          )
          ?? data[0];


        setOrganizationId(
          String(
            initial.id
          )
        );


        const runData =
          await listIngestionRuns(
            initial.id
          );


        if (!cancelled) {
          setHistory(
            runData
          );
        }
      } catch {
        if (!cancelled) {
          setError(
            "Unable to initialize ingestion page.",
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
    setOrganizationId(
      value
    );

    clearPreview();


    if (!value) {
      setHistory([]);

      return;
    }


    try {
      await refreshHistory(
        Number(value)
      );
    } catch {
      setError(
        "Unable to load ingestion history.",
      );
    }
  }


  async function handlePreview() {
    if (!organizationId) {
      setError(
        "Select an organization.",
      );

      return;
    }


    try {
      setWorking(true);

      setError("");


      const result =
        await previewIngestion(
          buildFormData()
        );


      setPreview(
        result
      );
    } catch (
      caughtError
    ) {
      setPreview(null);

      setError(
        caughtError
        instanceof Error
          ? caughtError.message
          : "Preview failed.",
      );
    } finally {
      setWorking(false);
    }
  }


  async function handleApply() {
    if (
      !preview
      || !preview.valid
    ) {
      setError(
        "Run a valid preview first.",
      );

      return;
    }


    try {
      setWorking(true);

      setError("");


      await applyIngestion(
        buildFormData()
      );


      const newPreview =
        await previewIngestion(
          buildFormData()
        );


      setPreview(
        newPreview
      );


      await refreshHistory(
        Number(
          organizationId
        )
      );
    } catch (
      caughtError
    ) {
      setError(
        caughtError
        instanceof Error
          ? caughtError.message
          : "Import failed.",
      );
    } finally {
      setWorking(false);
    }
  }


  const summaryEntries =
    preview
      ? [
          [
            "Network Zones",
            preview
              .summary
              .network_zones,
          ],

          [
            "Assets",
            preview
              .summary
              .assets,
          ],

          [
            "Relationships",
            preview
              .summary
              .relationships,
          ],

          [
            "Vulnerabilities",
            preview
              .summary
              .vulnerabilities,
          ],
        ] as const

      : [];


  return (
    <>
      <div className="page-heading">
        <div>
          <h2>
            Environment Ingestion
          </h2>

          <p>
            Preview and import technical
            environment data from JSON or
            CSV without manually creating
            every RiftTrace object.
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
          Import Target
        </h3>


        <div className="form-grid">
          <label>
            Organization

            <select
              value={
                organizationId
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
            Source Format

            <select
              value={
                sourceFormat
              }

              onChange={(event) => {
                setSourceFormat(
                  event.target.value as
                    IngestionSourceFormat,
                );

                clearFiles();
              }}
            >
              <option value="JSON">
                JSON Bundle
              </option>

              <option value="CSV">
                CSV Files
              </option>
            </select>
          </label>
        </div>
      </section>


      <section className="panel">
        <h3>
          Source Files
        </h3>


        {sourceFormat
          === "JSON"
        ? (
          <label className="ingestion-file-field">
            JSON Bundle

            <input
              type="file"

              accept=".json,application/json"

              onChange={(event) => {
                setBundleFile(
                  event
                    .target
                    .files?.[0]
                  ?? null
                );

                clearPreview();
              }}
            />

            <span>
              {
                bundleFile?.name
                ?? "No file selected"
              }
            </span>
          </label>
        )
        : (
          <div className="ingestion-file-grid">
            <label>
              Network Zones CSV

              <input
                type="file"

                accept=".csv,text/csv"

                onChange={(event) => {
                  setZonesFile(
                    event
                      .target
                      .files?.[0]
                    ?? null
                  );

                  clearPreview();
                }}
              />
            </label>


            <label>
              Assets CSV

              <input
                type="file"

                accept=".csv,text/csv"

                onChange={(event) => {
                  setAssetsFile(
                    event
                      .target
                      .files?.[0]
                    ?? null
                  );

                  clearPreview();
                }}
              />
            </label>


            <label>
              Relationships CSV

              <input
                type="file"

                accept=".csv,text/csv"

                onChange={(event) => {
                  setRelationshipsFile(
                    event
                      .target
                      .files?.[0]
                    ?? null
                  );

                  clearPreview();
                }}
              />
            </label>


            <label>
              Vulnerabilities CSV

              <input
                type="file"

                accept=".csv,text/csv"

                onChange={(event) => {
                  setVulnerabilitiesFile(
                    event
                      .target
                      .files?.[0]
                    ?? null
                  );

                  clearPreview();
                }}
              />
            </label>
          </div>
        )}


        <div className="ingestion-actions">
          <button
            type="button"

            disabled={
              working
            }

            onClick={() => {
              void handlePreview();
            }}
          >
            {
              working
              ? "Working..."
              : "Preview Import"
            }
          </button>


          <button
            type="button"

            className="secondary-button"

            onClick={
              clearFiles
            }
          >
            Clear Files
          </button>
        </div>
      </section>


      {preview && (
        <section className="panel">
          <div className="ingestion-preview-heading">
            <div>
              <h3>
                Import Preview
              </h3>

              <p>
                No database changes occur
                during preview.
              </p>
            </div>


            <span
              className={
                preview.valid
                ? "ingestion-valid"
                : "ingestion-invalid"
              }
            >
              {
                preview.valid
                ? "VALID"
                : "INVALID"
              }
            </span>
          </div>


          <div className="ingestion-summary-grid">
            {summaryEntries.map(
              ([
                label,
                summary,
              ]) => (
                <article
                  key={label}
                  className="ingestion-summary-card"
                >
                  <strong>
                    {label}
                  </strong>

                  <div>
                    <span>
                      Create
                    </span>

                    <b>
                      {
                        summary.create
                      }
                    </b>
                  </div>

                  <div>
                    <span>
                      Update
                    </span>

                    <b>
                      {
                        summary.update
                      }
                    </b>
                  </div>

                  <div>
                    <span>
                      Unchanged
                    </span>

                    <b>
                      {
                        summary
                          .unchanged
                      }
                    </b>
                  </div>
                </article>
              ),
            )}
          </div>


          {preview
            .issues
            .length > 0
          && (
            <div className="ingestion-issue-list">
              <h4>
                Validation Issues
              </h4>

              {preview
                .issues
                .map(
                  (
                    issue,
                    index,
                  ) => (
                    <div
                      key={
                        `${issue.section}-${index}`
                      }
                    >
                      <strong>
                        {
                          issue.section
                        }
                      </strong>

                      <span>
                        {
                          issue.message
                        }
                      </span>
                    </div>
                  ),
                )}
            </div>
          )}


          <button
            type="button"

            disabled={
              working
              || !preview.valid
            }

            onClick={() => {
              void handleApply();
            }}
          >
            {
              working
              ? "Applying..."
              : "Apply Import"
            }
          </button>
        </section>
      )}


      <section className="panel">
        <h3>
          Recent Imports
        </h3>


        {history.length
          === 0
        ? (
          <p>
            No imports have been applied
            to this organization yet.
          </p>
        )
        : (
          <div className="ingestion-history">
            {history.map(
              (run) => (
                <article
                  key={
                    run.id
                  }
                >
                  <div>
                    <strong>
                      Import #
                      {run.id}
                    </strong>

                    <span>
                      {
                        run
                          .source_format_display
                      }
                    </span>
                  </div>


                  <p>
                    {
                      run.source_files
                        .join(", ")
                    }
                  </p>


                  <small>
                    {
                      new Date(
                        run.created_at
                      )
                        .toLocaleString()
                    }
                  </small>
                </article>
              ),
            )}
          </div>
        )}
      </section>
    </>
  );
}
