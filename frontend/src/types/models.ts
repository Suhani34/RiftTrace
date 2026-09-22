export interface Organization {
  id: number;
  name: string;
  description: string;
  created_at: string;
  updated_at: string;
}

export type AssetType =
  | "APPLICATION"
  | "API"
  | "SERVER"
  | "DATABASE"
  | "WORKSTATION"
  | "FILE_SERVER"
  | "VPN_GATEWAY"
  | "CLOUD_SERVICE"
  | "CI_CD"
  | "EMAIL_SERVER"
  | "DOMAIN_CONTROLLER"
  | "NETWORK_DEVICE"
  | "OTHER";

export type Criticality =
  | "LOW"
  | "MEDIUM"
  | "HIGH"
  | "CRITICAL";

export interface Asset {
  id: number;
  organization: number;
  organization_name: string;
  name: string;
  asset_type: AssetType;
  asset_type_display: string;
  criticality: Criticality;
  criticality_display: string;
  description: string;
  is_internet_exposed: boolean;
  created_at: string;
  updated_at: string;
}

export type RelationshipType =
  | "CONNECTS_TO"
  | "CALLS"
  | "READS"
  | "WRITES"
  | "AUTHENTICATES_TO"
  | "DEPENDS_ON";

export interface Relationship {
  id: number;
  organization: number;
  source: number;
  source_name: string;
  target: number;
  target_name: string;
  relationship_type: RelationshipType;
  relationship_type_display: string;
  description: string;
  created_at: string;
}

export interface CreateOrganizationInput {
  name: string;
  description: string;
}

export interface CreateAssetInput {
  organization: number;
  name: string;
  asset_type: AssetType;
  criticality: Criticality;
  description: string;
  is_internet_exposed: boolean;
}

export interface CreateRelationshipInput {
  source: number;
  target: number;
  relationship_type: RelationshipType;
  description: string;
}
