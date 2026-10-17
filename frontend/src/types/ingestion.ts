export type IngestionSourceFormat =
  | "JSON"
  | "CSV";


export interface IngestionEntitySummary {
  create: number;

  update: number;

  unchanged: number;
}


export interface IngestionIssue {
  section: string;

  message: string;
}


export interface IngestionPlan {
  valid: boolean;

  normalized_counts: {
    network_zones:
      number;

    assets:
      number;

    relationships:
      number;

    vulnerabilities:
      number;
  };

  summary: {
    network_zones:
      IngestionEntitySummary;

    assets:
      IngestionEntitySummary;

    relationships:
      IngestionEntitySummary;

    vulnerabilities:
      IngestionEntitySummary;
  };

  issues:
    IngestionIssue[];

  source_files:
    string[];

  parse_error?:
    string;
}


export interface IngestionRun {
  id: number;

  organization:
    number;

  organization_name:
    string;

  source_format:
    IngestionSourceFormat;

  source_format_display:
    string;

  source_files:
    string[];

  summary:
    IngestionPlan["summary"];

  created_at:
    string;
}


export interface IngestionApplyResult {
  applied:
    boolean;

  run:
    IngestionRun;

  plan:
    IngestionPlan;
}
