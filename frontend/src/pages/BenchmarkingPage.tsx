import {
  useEffect,
  useMemo,
  useState,
} from "react";

import {
  CartesianGrid,
  Legend,
  Line,
  LineChart,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis,
} from "recharts";

import {
  listBenchmarkResults,
} from "../api/benchmarking";

import type {
  BenchmarkResult,
} from "../types/benchmarking";


interface ChartRow {
  asset_count: number;

  baseline?: number;

  optimized?: number;
}


export default function BenchmarkingPage() {
  const [
    results,
    setResults,
  ] = useState<
    BenchmarkResult[]
  >([]);

  const [
    selectedName,
    setSelectedName,
  ] = useState("");

  const [
    loading,
    setLoading,
  ] = useState(false);

  const [
    error,
    setError,
  ] = useState("");


  useEffect(
    () => {
      let cancelled = false;


      async function loadData() {
        setLoading(true);
        setError("");


        try {
          const data =
            await listBenchmarkResults();


          if (cancelled) {
            return;
          }


          setResults(
            data
          );


          if (
            data.length > 0
          ) {
            setSelectedName(
              data[
                0
              ].name
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
                    + "benchmarks."
                  )
            );
          }

        } finally {
          if (!cancelled) {
            setLoading(false);
          }
        }
      }


      void loadData();


      return () => {
        cancelled = true;
      };
    },
    [],
  );


  const benchmarkNames =
    useMemo(
      () => (
        Array.from(
          new Set(
            results.map(
              (result) =>
                result.name
            )
          )
        )
      ),
      [
        results,
      ],
    );


  const selectedResults =
    useMemo(
      () => (
        results.filter(
          (result) =>
            result.name
            === selectedName
        )
      ),
      [
        results,
        selectedName,
      ],
    );


  const chartData =
    useMemo(
      () => {
        const rows =
          new Map<
            number,
            ChartRow
          >();


        for (
          const result
          of selectedResults
        ) {
          if (
            result.asset_count
            <= 0
          ) {
            continue;
          }


          const existing =
            rows.get(
              result.asset_count
            )
            ?? {
              asset_count:
                result.asset_count,
            };


          if (
            result.variant
            === "BASELINE"
          ) {
            existing.baseline =
              result.mean_ms;

          } else {
            existing.optimized =
              result.mean_ms;
          }


          rows.set(
            result.asset_count,
            existing,
          );
        }


        return Array.from(
          rows.values()
        ).sort(
          (
            left,
            right,
          ) =>
            (
              left.asset_count
              - right.asset_count
            ),
        );
      },
      [
        selectedResults,
      ],
    );


  return (
    <div className="page">
      <div className="page-header">
        <div>
          <h2>
            Performance Benchmarking
          </h2>

          <p>
            Measure RiftTrace latency,
            SQL activity and Python
            allocation growth across
            repeatable benchmark runs.
          </p>
        </div>
      </div>


      {error && (
        <div className="error-box">
          {error}
        </div>
      )}


      <section className="panel">
        <label>
          Benchmark

          <select
            value={
              selectedName
            }

            onChange={(event) =>
              setSelectedName(
                event.target.value
              )
            }
          >
            {benchmarkNames.map(
              (name) => (
                <option
                  key={
                    name
                  }

                  value={
                    name
                  }
                >
                  {
                    name
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


      {chartData.length > 0 && (
        <section className="panel">
          <h3>
            Mean Latency by Asset Count
          </h3>

          <div className="benchmark-chart">
            <ResponsiveContainer
              width="100%"
              height={340}
            >
              <LineChart
                data={
                  chartData
                }
              >
                <CartesianGrid
                  strokeDasharray="3 3"
                />

                <XAxis
                  dataKey={
                    "asset_count"
                  }

                  label={{
                    value:
                      "Assets",

                    position:
                      "insideBottom",

                    offset:
                      -5,
                  }}
                />

                <YAxis
                  label={{
                    value:
                      "Milliseconds",

                    angle:
                      -90,

                    position:
                      "insideLeft",
                  }}
                />

                <Tooltip />

                <Legend />

                <Line
                  type="monotone"
                  dataKey="baseline"
                  name="Baseline"
                />

                <Line
                  type="monotone"
                  dataKey="optimized"
                  name="Optimized"
                />
              </LineChart>
            </ResponsiveContainer>
          </div>
        </section>
      )}


      <section className="panel">
        <h3>
          Benchmark Results
        </h3>

        {selectedResults.length === 0
          ? (
              <p>
                No benchmark results
                exist yet.
              </p>
            )
          : (
              <div className="table-wrap">
                <table className="benchmark-table">
                  <thead>
                    <tr>
                      <th>
                        Variant
                      </th>

                      <th>
                        Assets
                      </th>

                      <th>
                        Mean
                      </th>

                      <th>
                        Median
                      </th>

                      <th>
                        P95
                      </th>

                      <th>
                        Queries
                      </th>

                      <th>
                        Peak KiB
                      </th>
                    </tr>
                  </thead>

                  <tbody>
                    {selectedResults.map(
                      (result) => (
                        <tr
                          key={
                            result.id
                          }
                        >
                          <td>
                            {
                              result.variant
                            }
                          </td>

                          <td>
                            {
                              result.asset_count
                            }
                          </td>

                          <td>
                            {
                              result.mean_ms
                            }
                            {" ms"}
                          </td>

                          <td>
                            {
                              result.median_ms
                            }
                            {" ms"}
                          </td>

                          <td>
                            {
                              result.p95_ms
                            }
                            {" ms"}
                          </td>

                          <td>
                            {
                              result
                                .mean_query_count
                            }
                          </td>

                          <td>
                            {
                              result
                                .peak_memory_kib
                            }
                          </td>
                        </tr>
                      ),
                    )}
                  </tbody>
                </table>
              </div>
            )}
      </section>


      <section className="panel">
        <h3>
          Interpretation
        </h3>

        <p>
          These measurements describe
          execution performance on the
          recorded benchmark environment.
          They do not represent attack
          likelihood or security risk.
        </p>
      </section>
    </div>
  );
}
