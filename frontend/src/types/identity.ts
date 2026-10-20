export type IdentityType =
  | "USER"
  | "SERVICE_ACCOUNT"
  | "MACHINE_ACCOUNT"
  | "GROUP"
  | "ROLE";


export type IdentityPrivilege =
  | "LOW"
  | "HIGH";


export interface Identity {
  id: number;

  organization: number;

  name: string;

  identity_type: IdentityType;

  identity_type_display: string;

  privilege_level:
    IdentityPrivilege;

  privilege_level_display:
    string;

  enabled: boolean;

  description: string;

  created_at: string;

  updated_at: string;
}


export interface CredentialExposure {
  id: number;

  organization: number;

  name: string;

  identity: number;

  identity_name: string;

  stored_on_asset: number;

  stored_on_asset_name:
    string;

  credential_type: string;

  discoverable_on_compromise:
    boolean;

  satisfies_mfa: boolean;

  active: boolean;

  description: string;
}


export interface IdentityAccess {
  id: number;

  organization: number;

  identity: number;

  identity_name: string;

  asset: number;

  asset_name: string;

  access_type: string;

  granted_privilege:
    IdentityPrivilege;

  requires_mfa: boolean;

  enabled: boolean;

  description: string;
}


export interface IdentityLink {
  id: number;

  organization: number;

  source_identity: number;

  source_identity_name:
    string;

  target_identity: number;

  target_identity_name:
    string;

  link_type: string;

  requires_mfa: boolean;

  enabled: boolean;

  description: string;
}


export interface IdentityPropagationResult {
  organization: number;

  summary: {
    seed_assets: number;

    potentially_compromised_assets:
      number;

    new_assets_from_identity:
      number;

    acquired_identities:
      number;

    successful_identity_steps:
      number;

    blocked_identity_steps:
      number;
  };

  compromised_assets: Array<{
    asset_id: number;

    asset_name: string;

    privilege:
      IdentityPrivilege;

    seed: boolean;
  }>;

  acquired_identities: Array<{
    identity_id: number;

    identity_name: string;

    mfa_satisfied:
      boolean;
  }>;

  steps: Array<{
    step_type: string;

    source_kind: string;

    source_id: number;

    source_name: string;

    target_kind: string;

    target_id: number;

    target_name: string;

    reference_id: number;

    reference_name: string;

    detail: string;
  }>;

  blocked_steps: Array<{
    step_type: string;

    source_kind: string;

    source_id: number;

    source_name: string;

    target_kind: string;

    target_id: number;

    target_name: string;

    reference_id: number;

    reason: string;
  }>;
}
