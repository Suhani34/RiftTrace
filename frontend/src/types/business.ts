export type BusinessCriticality =
  | "LOW"
  | "MEDIUM"
  | "HIGH"
  | "CRITICAL";


export type DependencyLevel =
  | "SUPPORTING"
  | "IMPORTANT"
  | "ESSENTIAL";


export interface BusinessProcess {
  id: number;

  organization: number;

  organization_name: string;

  name: string;

  criticality:
    BusinessCriticality;

  criticality_display: string;

  description: string;

  impact_description: string;

  created_at: string;

  updated_at: string;
}


export interface BusinessProcessDependency {
  id: number;

  organization: number;

  business_process: number;

  business_process_name: string;

  asset: number;

  asset_name: string;

  dependency_level:
    DependencyLevel;

  dependency_level_display:
    string;

  description: string;

  created_at: string;

  updated_at: string;
}


export interface CreateBusinessProcessInput {
  organization: number;

  name: string;

  criticality:
    BusinessCriticality;

  description: string;

  impact_description: string;
}


export interface CreateBusinessDependencyInput {
  business_process: number;

  asset: number;

  dependency_level:
    DependencyLevel;

  description: string;
}

