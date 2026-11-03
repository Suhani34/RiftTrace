import {
  useState,
} from "react";

import {
  runPathIntelligence,
} from "../api/simulations";

import type {
  PathIntelligenceResult,
} from "../types/pathIntelligence";


export default function PathIntelligencePage() {
  const [
    organizationId,
    setOrganizationId,
  ] = useState("5");

  const [
    startAssetId,
    setStartAssetId,
  ] = useState("14");

  const [
    startPrivilege,
    setStartPrivilege,
  ] = useState<
    "LOW" | "HIGH"
  >("LOW");

  const [
    maxDepth,
    setMaxDepth,
  ] = useState("8");

  const [
    maxPaths,
    setMaxPaths,
  ] = useState("1000");

  const [
    targetText,
    setTargetText,
  ] = useState("");

  const [
    result,
    setResult,
  ] = useState<
    PathIntelligenceResult | null
  >(null);

  const [
    loading,
    setLoading,
  ] = useState(false);

  const [
    error,
    setError,
  ] = useState("");


  function parseTargets() {
    if (
      !targetText.trim()
    ) {
      return [];
    }


    return targetText
      .split(",")
      .map(
        (value) =>
          Number(
            value.trim()
          )
      )
      .filter(
        (value) =>
          Number.isInteger(
            value
          )
      );
  }


  async function handleRun() {
    setLoading(true);
    setError("");


    try {
      const data =
        await runPathIntelligence(
          Number(
            organizationId
          ),

          Number(
            startAssetId
          ),

          startPrivilege,

          parseTargets(),

          Number(
            maxDepth
          ),

          Number(
            maxPaths
          ),
        );


      setResult(
        data
      );

    } catch (caughtError) {
      setError(
        caughtError
          instanceof Error
          ? caughtError.message
          : (
              "Unable to run "
              + "path intelligence."
            )
      );

    } finally {
      setLoading(false);
    }
  }


  return (
    <div className="page">
      <div className="page-header">
        <div>
          <h2>
            Attack Path Intelligence
          </h2>

          <p>
            Explore modeled security-aware
            propagation paths and identify
            recurring assets and
            relationships.
          </p>
        </div>
      </div>


      <section className="panel">
        <h3>
          Analysis Input
        </h3>

        <label>
          Organization ID

          <input
            type="number"
            value={
              organizationId
            }

            onChange={(event) =>
              setOrganizationId(
                event.target.value
              )
            }
          />
        </label>


        <label>
          Start Asset ID

          <input
            type="number"
            value={
              startAssetId
            }

            onChange={(event) =>
              setStartAssetId(
                event.target.value
              )
            }
          />
        </label>


        <label>
          Start Privilege

          <select
            value={
              startPrivilege
            }

            onChange={(event) =>
              setStartPrivilege(
                event.target.value as "LOW" | "HIGH"
              )
            }
          >
            <option value="LOW">
              LOW
            </option>

            <option value="HIGH">
              HIGH
            </option>
          </select>
        </label>


        <label>
          Target Asset IDs
          (optional, comma separated)

          <input
            value={
              targetText
            }

            placeholder="17, 20"

            onChange={(event) =>
              setTargetText(
                event.target.value
              )
            }
          />
        </label>


        <label>
          Maximum Depth

          <input
            type="number"
            min="1"
            max="20"

            value={
              maxDepth
            }

            onChange={(event) =>
              setMaxDepth(
                event.target.value
              )
            }
          />
        </label>


        <label>
          Maximum Paths

          <input
            type="number"
            min="1"
            max="5000"

            value={
              maxPaths
            }

            onChange={(event) =>
              setMaxPaths(
                event.target.value
              )
            }
          />
        </label>


        <button
          type="button"

          disabled={
            loading
          }

          onClick={() => {
            void handleRun();
          }}
        >
          {
            loading
              ? "Analyzing..."
              : "Analyze Attack Paths"
          }
        </button>
      </section>


      {error && (
        <div className="error-box">
          {error}
        </div>
      )}


      {result && (
        <>
          <section className="stats-grid">
            <article>
              <strong>
                Attack Paths
              </strong>

              <span>
                {
                  result
                    .summary
                    .attack_paths
                }
              </span>
            </article>

            <article>
              <strong>
                Critical Paths
              </strong>

              <span>
                {
                  result
                    .summary
                    .critical_attack_paths
                }
              </span>
            </article>

            <article>
              <strong>
                Business-Critical
              </strong>

              <span>
                {
                  result
                    .summary
                    .business_critical_attack_paths
                }
              </span>
            </article>

            <article>
              <strong>
                Targets
              </strong>

              <span>
                {
                  result
                    .summary
                    .target_count
                }
              </span>
            </article>
          </section>


          {
            result
              .summary
              .path_limit_reached
            && (
              <div className="warning-box">
                Maximum path limit was
                reached. The displayed
                results are a bounded
                subset of modeled paths.
              </div>
            )
          }


          <section className="panel">
            <h3>
              Node Chokepoints
            </h3>

            {
              result
                .node_chokepoints
                .length === 0
                ? (
                    <p>
                      No intermediate node
                      chokepoints were
                      identified.
                    </p>
                  )
                : (
                    <div className="table-wrap">
                      <table>
                        <thead>
                          <tr>
                            <th>
                              Asset
                            </th>

                            <th>
                              Paths
                            </th>

                            <th>
                              Coverage
                            </th>

                            <th>
                              Critical Paths
                            </th>

                            <th>
                              Single Point
                            </th>
                          </tr>
                        </thead>

                        <tbody>
                          {
                            result
                              .node_chokepoints
                              .map(
                                (
                                  item
                                ) => (
                                  <tr
                                    key={
                                      item
                                        .asset_id
                                    }
                                  >
                                    <td>
                                      {
                                        item
                                          .asset_name
                                      }
                                    </td>

                                    <td>
                                      {
                                        item
                                          .paths_through
                                      }
                                      /
                                      {
                                        item
                                          .total_paths
                                      }
                                    </td>

                                    <td>
                                      {
                                        item
                                          .coverage_percent
                                      }
                                      %
                                    </td>

                                    <td>
                                      {
                                        item
                                          .critical_paths_through
                                      }
                                    </td>

                                    <td>
                                      {
                                        item
                                          .single_point_chokepoint
                                          ? "Yes"
                                          : "No"
                                      }
                                    </td>
                                  </tr>
                                ),
                              )
                          }
                        </tbody>
                      </table>
                    </div>
                  )
            }
          </section>


          <section className="panel">
            <h3>
              Relationship Chokepoints
            </h3>

            <div className="table-wrap">
              <table>
                <thead>
                  <tr>
                    <th>
                      Relationship
                    </th>

                    <th>
                      Paths
                    </th>

                    <th>
                      Coverage
                    </th>

                    <th>
                      Critical Paths
                    </th>

                    <th>
                      Remaining if Blocked
                    </th>
                  </tr>
                </thead>

                <tbody>
                  {
                    result
                      .edge_chokepoints
                      .map(
                        (
                          item
                        ) => (
                          <tr
                            key={
                              item
                                .relationship_id
                            }
                          >
                            <td>
                              {
                                item
                                  .source_asset_name
                              }
                              {" → "}
                              {
                                item
                                  .target_asset_name
                              }
                            </td>

                            <td>
                              {
                                item
                                  .paths_through
                              }
                              /
                              {
                                item
                                  .total_paths
                              }
                            </td>

                            <td>
                              {
                                item
                                  .coverage_percent
                              }
                              %
                            </td>

                            <td>
                              {
                                item
                                  .critical_paths_through
                              }
                            </td>

                            <td>
                              {
                                item
                                  .remaining_paths
                              }
                            </td>
                          </tr>
                        ),
                      )
                  }
                </tbody>
              </table>
            </div>
          </section>


          <section className="panel">
            <h3>
              Modeled Attack Paths
            </h3>

            {
              result.paths.map(
                (path) => (
                  <article
                    className="attack-path-card"

                    key={
                      path.path_id
                    }
                  >
                    <div>
                      <strong>
                        {
                          path.path_id
                        }
                      </strong>

                      {" · "}

                      {
                        path.hop_count
                      }

                      {" hops"}

                      {
                        path
                          .is_critical_path
                        && (
                          <>
                            {" · "}
                            CRITICAL TARGET
                          </>
                        )
                      }
                    </div>

                    <div className="attack-path-flow">
                      {
                        path.assets
                          .map(
                            (asset) =>
                              (
                                `${asset.asset_name}`
                                + ` (${asset.privilege})`
                              )
                          )
                          .join(
                            " → "
                          )
                      }
                    </div>

                    <p>
                      Target:
                      {" "}
                      {
                        path
                          .target
                          .asset_name
                      }
                      {" · "}
                      {
                        path
                          .target
                          .criticality
                      }
                    </p>
                  </article>
                ),
              )
            }
          </section>


          <section className="panel">
            <h3>
              Interpretation
            </h3>

            <p>
              {
                result
                  .interpretation
              }
            </p>
          </section>
        </>
      )}
    </div>
  );
}
