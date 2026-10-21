export interface AttackTechnique {
  id: number;

  attack_id: string;

  name: string;

  domain: string;

  domain_display: string;

  tactics: string[];

  is_subtechnique: boolean;

  parent_attack_id: string;

  source_version: string;

  source_url: string;

  enabled: boolean;
}


export interface AttackMappingRule {
  id: number;

  rule_code: string;

  name: string;

  event_type: string;

  technique: number;

  technique_attack_id: string;

  technique_name: string;

  conditions: Record<
    string,
    unknown
  >;

  rationale: string;

  priority: number;

  enabled: boolean;
}


export interface AttackAnnotation {
  attack_id: string;

  name: string;

  tactics: string[];

  source_version: string;

  source_url: string;

  rule_code: string;

  basis: string;
}


export interface AttackMappingEvaluation {
  event_type: string;

  attributes: Record<
    string,
    unknown
  >;

  annotations:
    AttackAnnotation[];

  disclaimer: string;
}
