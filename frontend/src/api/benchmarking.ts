import type {
  BenchmarkResult,
} from "../types/benchmarking";


const API_BASE_URL =
  import.meta.env.VITE_API_BASE_URL
  ?? "http://127.0.0.1:8000/api";


export async function listBenchmarkResults():
  Promise<BenchmarkResult[]> {
  const response =
    await fetch(
      (
        `${API_BASE_URL}`
        + "/benchmarking/results/"
      )
    );


  if (!response.ok) {
    throw new Error(
      (
        "Unable to load "
        + "benchmark results."
      )
    );
  }


  return (
    await response.json()
  ) as BenchmarkResult[];
}
