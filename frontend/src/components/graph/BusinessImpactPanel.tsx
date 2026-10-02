import type {
  Asset,
} from "../../types/models";

import type {
  BusinessImpactSimulationResult,
} from "../../types/businessImpact";


interface Props {
  assets: Asset[];

  selectedStartAssetId:
    string;

  startPrivilege:
    "LOW"
    | "HIGH";

  running: boolean;

  error: string;

  result:
    BusinessImpactSimulationResult
    | null;

  onStartAssetChange:
    (value: string) => void;

  onStartPrivilegeChange:
    (
      value:
        "LOW"
        | "HIGH"
    ) => void;

  onRun:
    () => void;

  onClear:
    () => void;
}


export default function BusinessImpactPanel({
  assets,
  selectedStartAssetId,
  startPrivilege,
  running,
  error,
  result,
  onStartAssetChange,
  onStartPrivilegeChange,
  onRun,
  onClear,
}: Props) {
  return (
    <section className="simulation-panel business-impact-panel">
      <div className="simulation-panel-header">
        <span className="details-eyebrow">
          Phase 9 Simulation
        </span>

        <h3>
          Business Impact
        </h3>

        <p>
          Propagate the modeled technical
          compromise into explicitly linked
          business processes.
        </p>
      </div>


      <div className="simulation-controls">
        <label>
          Starting Asset

          <select
            value={
              selectedStartAssetId
            }
            onChange={(event) =>
              onStartAssetChange(
                event.target.value,
              )
            }
          >
            <option value="">
              Select starting asset
            </option>

            {assets.map(
              (asset) => (
                <option
                  key={asset.id}
                  value={asset.id}
                >
                  {asset.name}
                </option>
              ),
            )}
          </select>
        </label>


        <label>
          Starting Privilege

          <select
            value={startPrivilege}
            onChange={(event) =>
              onStartPrivilegeChange(
                event.target.value as
                    | "LOW"
                    | "HIGH",
              )
            }
          >
            <option value="LOW">
              Low
            </option>

            <option value="HIGH">
              High
            </option>
          </select>
        </label>


        <div className="simulation-actions">
          <button
            type="button"
            disabled={
              running
              || !selectedStartAssetId
            }
            onClick={onRun}
          >
            {running
              ? "Running..."
              : "Analyze Business Impact"}
          </button>


          {result && (
            <button
              type="button"
              className="secondary-button"
              onClick={onClear}
            >
              Clear Result
            </button>
          )}
        </div>
      </div>


      {error && (
        <div className="error-box">
          {error}
        </div>
      )}


      {result && (
        <>
          <div className="simulation-summary-grid">
            <article className="simulation-summary-card">
              <span>
                Affected Assets
              </span>

              <strong>
                {
                  result
                    .technical_consequence
                    .affected_asset_ids
                    .length
                }
              </strong>
            </article>


            <article className="simulation-summary-card">
              <span>
                Impacted Processes
              </span>

              <strong>
                {
                  result
                    .business_impact
                    .summary
                    .impacted_process_count
                }
              </strong>
            </article>


            <article className="simulation-summary-card">
              <span>
                Critical Processes
              </span>

              <strong>
                {
                  result
                    .business_impact
                    .summary
                    .critical_process_count
                }
              </strong>
            </article>


            <article className="simulation-summary-card">
              <span>
                Essential Dependency Hits
              </span>

              <strong>
                {
                  result
                    .business_impact
                    .summary
                    .essential_dependency_hit_count
                }
              </strong>
            </article>
          </div>


          <div className="simulation-semantics">
            {result.semantics}
          </div>


          <div className="business-impact-results">
            <h4>
              Potentially Impacted
              Business Processes
            </h4>


            {
              result
                .business_impact
                .impacted_processes
                .length === 0
            ? (
              <p>
                No modeled business process
                depends on the affected
                technical assets.
              </p>
            ) : (
              result
                .business_impact
                .impacted_processes
                .map(
                  (impact) => (
                    <article
                      className="business-impact-result-card"
                      key={
                        impact
                          .business_process
                          .id
                      }
                    >
                      <div>
                        <strong>
                          {
                            impact
                              .business_process
                              .name
                          }
                        </strong>

                        <span>
                          {
                            impact
                              .business_process
                              .criticality_display
                          }
                        </span>
                      </div>


                      <p>
                        Strongest affected
                        dependency:
                        {" "}
                        {
                          impact
                            .strongest_dependency_level
                        }
                      </p>


                      <p>
                        Affected assets:
                        {" "}
                        {
                          impact
                            .affected_assets
                            .map(
                              (asset) =>
                                asset.name,
                            )
                            .join(", ")
                        }
                      </p>


                      <p>
                        Potential consequence:
                        {" "}
                        {
                          impact
                            .business_process
                            .impact_description
                          || "Not specified"
                        }
                      </p>
                    </article>
                  ),
                )
            )}
          </div>
        </>
      )}
    </section>
  );
}
