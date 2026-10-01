export interface Organization {
  id: number;
  name: string;
  description: string;
  created_at: string;
  updated_at: string;
}

export type RequiredSourcePrivilege =
  | "NONE"
  | "LOW"
  | "HIGH";

export type ZoneType =
  | "DMZ"
  | "INTERNAL"
  | "RESTRICTED"
  | "MANAGEMENT"
  | "CLOUD"
  | "ENDPOINT"
  | "OTHER";


export interface NetworkZone {
  id: number;
  organization: number;
  organization_name: string;
  name: string;
  zone_type: ZoneType;
  zone_type_display: string;
  description: string;
  created_at: string;
  updated_at: string;
}


export type Environment =
  | "PRODUCTION"
  | "STAGING"
  | "TEST"
  | "DEVELOPMENT"
  | "OTHER";

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

  environment: Environment;
  environment_display: string;

  network_zone: number | null;
  network_zone_name: string | null;

  hostname: string;
  ip_address: string | null;

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
  protocol: string;
  port: number | null;
  requires_authentication: boolean;
  target_name: string;
  required_source_privilege:
    RequiredSourcePrivilege;
  required_source_privilege_display:
    string;
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
  environment: Environment;
  network_zone: number | null;
  hostname: string;
  ip_address: string | null;
  description: string;
  is_internet_exposed: boolean;
}

export interface CreateRelationshipInput {
  source: number;
  target: number;
  relationship_type: RelationshipType;
  protocol: string;
  port: number | null;
  required_source_privilege:
    RequiredSourcePrivilege;
  requires_authentication: boolean;
  description: string;
}

export interface CreateNetworkZoneInput {
  organization: number;
  name: string;
  zone_type: ZoneType;
  description: string;
}

export interface OrganizationTopology {
  organization: Organization;
  zones: NetworkZone[];
  nodes: Asset[];
  edges: Relationship[];
}
