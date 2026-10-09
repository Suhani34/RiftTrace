export type SecurityControlType =
  | "NETWORK_SEGMENTATION"
  | "VULNERABILITY_REMEDIATION"
  | "MFA"
  | "LEAST_PRIVILEGE"
  | "AUTHENTICATION_ENFORCEMENT";


export interface SecurityControl {
  id: number;

  organization: number;

  organization_name: string;

  name: string;

  control_type:
    SecurityControlType;

  control_type_display:
    string;

  target_relationship:
    number | null;

  target_relationship_display:
    string | null;

  target_vulnerability:
    number | null;

  target_vulnerability_display:
    string | null;

  description: string;

  created_at: string;

  updated_at: string;
}


export interface CreateSecurityControlInput {
  organization: number;

  name: string;

  control_type:
    SecurityControlType;

  target_relationship:
    number | null;

  target_vulnerability:
    number | null;

  description: string;
}
