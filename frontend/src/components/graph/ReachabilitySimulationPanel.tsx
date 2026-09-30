import type {
  Asset,
} from "../../types/models";

import type {
  ReachabilitySimulationResult,
} from "../../types/simulation";


interface ReachabilitySimulationPanelProps {
  assets: Asset[];

  selectedStartAssetId: string;

  running: boolean;

  error: string;

  result:
    ReachabilitySimulationResult
    | null;

  onStartAssetChange:
    (value: string) => void;

  onRun:
    () => void;

  onClear:
    () => void;
}


export default function ReachabilitySimulationPanel({
  assets,
  selectedStartAssetId,
  running,
  error,
  result,
  onStartAssetChange,
  onRun,
  onClear,
}: ReachabilitySimulationPanelProps) {
  return (
    <section className="simulation-panel">
      <div className="simulation-panel-header">
        <div>
          <span className="details-eyebrow">
            Phase 7 Simulation
          </span>

          <h3>
            Topology Reachability
          </h3>

          <p>
            Select a starting asset to
            calculate which systems are
            potentially reachable through
            the directed modeled topology.
          </p>
        </div>
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
                event.target.value
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
                  {" — "}
                  {
                    asset
                      .asset_type_display
                  }
                </option>
              ),
            )}
          </select>
        </label>


        <div className="simulation-actions">
          <button
            type="button"
            onClick={onRun}
            disabled={
              !selectedStartAssetId
              || running
            }
          >
            {running
              ? "Running..."
              : "Run Reachability"}
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
                Start Asset
              </span>

              <strong>
                {
                  result
                    .start_asset
                    .name
                }
              </strong>
            </article>


            <article className="simulation-summary-card">
              <span>
                Reachable Assets
              </span>

              <strong>
                {
                  result
                    .summary
                    .reachable_asset_count
                }
              </strong>
            </article>


            <article className="simulation-summary-card">
              <span>
                Reachable Critical
              </span>

              <strong>
                {
                  result
                    .summary
                    .reachable_critical_asset_count
                }
              </strong>
            </article>


            <article className="simulation-summary-card">
              <span>
                Maximum Hops
              </span>

              <strong>
                {
                  result
                    .summary
                    .max_hops
                }
              </strong>
            </article>
          </div>


          <div className="simulation-semantics">
            {result.semantics}
          </div>


          <div className="simulation-paths">
            <h4>
              Shortest Topology Paths
            </h4>


            {
              result
                .reachable_assets
                .length === 0
              ? (
                  <p>
                    No other assets are
                    reachable from this
                    starting asset through
                    the current directed
                    topology.
                  </p>
                )
              : (
                  result
                    .reachable_assets
                    .map(
                      (item) => (
                        <article
                          className="simulation-path-card"
                          key={
                            item.asset.id
                          }
                        >
                          <div>
                            <strong>
                              {
                                item
                                  .asset
                                  .name
                              }
                            </strong>

                            <span>
                              {
                                item
                                  .hop_count
                              }
                              {
                                item
                                  .hop_count
                                === 1
                                  ? " hop"
                                  : " hops"
                              }
                            </span>
                          </div>

                          <p>
                            {
                              item
                                .shortest_path_asset_names
                                .join(
                                  " → "
                                )
                            }
                          </p>
                        </article>
                      ),
                    )
                )
            }
          </div>
        </>
      )}
    </section>
  );
}
