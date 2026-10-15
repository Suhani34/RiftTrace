import type {
  Organization,
} from "./models";


export interface DashboardDistributionItem {
  name: string;

  key: string;

  value: number;
}


export interface DashboardSummary {
  organization:
    Organization;

  totals: {
    network_zones:
      number;

    assets:
      number;

    relationships:
      number;

    vulnerabilities:
      number;

    exploitable_vulnerabilities:
      number;

    security_controls:
      number;

    business_processes:
      number;

    business_dependencies:
      number;
  };

  asset_criticality:
    DashboardDistributionItem[];

  business_process_criticality:
    DashboardDistributionItem[];

  security_control_types:
    DashboardDistributionItem[];
}
