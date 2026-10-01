import type {
  Asset,
} from "../../types/models";

import type {
  AttackPropagationResult,
} from "../../types/attackSimulation";


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
    AttackPropagationResult
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


export default function AttackPropagationPanel({
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
    <section className="simulation-panel attack-panel">
      <div className="simulation-panel-header">
        <span className="details-eyebrow">
          Phase 8 Simulation
        </span>

        <h3>
          Security-Aware Propagation
        </h3>

        <p>
          Simulate propagation using
          modeled vulnerabilities,
          privileges and authentication
          requirements.
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
              : "Run Propagation"}
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
                Propagated Assets
              </span>

              <strong>
                {
                  result.summary
                    .propagated_asset_count
                }
              </strong>
            </article>

            <article className="simulation-summary-card">
              <span>
                Critical Assets
              </span>

              <strong>
                {
                  result.summary
                    .propagated_critical_asset_count
                }
              </strong>
            </article>

            <article className="simulation-summary-card">
              <span>
                Maximum Hops
              </span>

              <strong>
                {
                  result.summary
                    .max_hops
                }
              </strong>
            </article>

            <article className="simulation-summary-card">
              <span>
                Blocked Transitions
              </span>

              <strong>
                {
                  result.summary
                    .blocked_transition_count
                }
              </strong>
            </article>
          </div>


          <div className="simulation-semantics">
            {result.semantics}
          </div>


          <div className="simulation-paths">
            <h4>
              Propagation Paths
            </h4>

            {result.propagated_assets.length
            === 0 ? (
              <p>
                No downstream compromise
                propagated under the
                current security model.
              </p>
            ) : (
              result.propagated_assets.map(
                (item) => (
                  <article
                    className="simulation-path-card"
                    key={item.asset.id}
                  >
                    <div>
                      <strong>
                        {item.asset.name}
                      </strong>

                      <span>
                        {
                          item.privilege
                        }
                        {" · "}
                        {
                          item.hop_count
                        }
                        {
                          item.hop_count
                          === 1
                            ? " hop"
                            : " hops"
                        }
                      </span>
                    </div>

                    <p>
                      {
                        item.path_asset_names
                        .join(" → ")
                      }
                    </p>

                    {item.via_vulnerability
                    && (
                      <p>
                        Via:{" "}
                        {
                          item
                            .via_vulnerability
                            .reference_id
                          || item
                            .via_vulnerability
                            .title
                        }
                      </p>
                    )}
                  </article>
                ),
              )
            )}
          </div>


          <div className="blocked-transitions">
            <h4>
              Blocked Transitions
            </h4>

            {
              result
                .blocked_transitions
                .length === 0
            ? (
              <p>
                No evaluated downstream
                transition was blocked.
              </p>
            ) : (
              result
                .blocked_transitions
                .map(
                  (blocked) => (
                    <article
                      className="blocked-transition-card"
                      key={
                        `${blocked.relationship_id}-${blocked.reason_code}`
                      }
                    >
                      <strong>
                        {
                          blocked
                            .source_asset_name
                        }
                        {" → "}
                        {
                          blocked
                            .target_asset_name
                        }
                      </strong>

                      <span>
                        {
                          blocked
                            .reason_code
                        }
                      </span>

                      <p>
                        {
                          blocked.reason
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
