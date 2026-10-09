export type AttackVector =
  | "NETWORK"
  | "ADJACENT"
  | "LOCAL"
  | "PHYSICAL";


export type PrivilegeLevel =
  | "NONE"
  | "LOW"
  | "HIGH";


export type GrantedPrivilege =
  | "LOW"
  | "HIGH";


export interface Vulnerability {
  id: number;

  organization: number;

  asset: number;
  asset_name: string;

  reference_id: string;

  title: string;

  cvss_score: string | null;

  attack_vector: AttackVector;

  attack_vector_display: string;

  privileges_required:
    PrivilegeLevel;

  privileges_required_display:
    string;

  grants_privilege:
    GrantedPrivilege;

  grants_privilege_display:
    string;

  bypasses_authentication:
    boolean;

  bypasses_mfa: boolean;

  is_exploitable: boolean;

  description: string;

  created_at: string;
  updated_at: string;
}


export interface CreateVulnerabilityInput {
  asset: number;

  reference_id: string;

  title: string;

  cvss_score: string | null;

  attack_vector: AttackVector;

  privileges_required:
    PrivilegeLevel;

  grants_privilege:
    GrantedPrivilege;

  bypasses_authentication:
    boolean;

  bypasses_mfa: boolean;

  is_exploitable: boolean;

  description: string;
}
