export type BenchmarkVariant =
  | "BASELINE"
  | "OPTIMIZED";


export interface BenchmarkSample {
  iteration: number;

  elapsed_ms: number;

  query_count: number;

  peak_memory_kib: number;
}


export interface BenchmarkResult {
  id: number;

  name: string;

  variant:
    BenchmarkVariant;

  organization:
    number | null;

  organization_name:
    string | null;

  endpoint: string;

  method: string;

  asset_count: number;

  relationship_count: number;

  iterations: number;

  warmup_iterations: number;

  mean_ms: number;

  median_ms: number;

  p95_ms: number;

  min_ms: number;

  max_ms: number;

  peak_memory_kib: number;

  mean_query_count: number;

  status_code: number;

  payload_sha256: string;

  samples:
    BenchmarkSample[];

  notes: string;

  created_at: string;
}
