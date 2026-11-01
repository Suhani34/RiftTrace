export interface ReportingEnvironmentSummary {
  network_zones: number;

  assets: number;

  relationships: number;

  vulnerabilities: number;
}


export interface ReportingScenarioSummary {
  total: number;

  runs: number;

  successful_runs: number;

  failed_runs: number;
}


export interface ReportingSummary {
  organization: {
    id: number;

    name: string;
  };

  environment:
    ReportingEnvironmentSummary;

  scenarios:
    ReportingScenarioSummary;
}
