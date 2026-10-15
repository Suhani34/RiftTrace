# RiftTrace Demo Flow

## 1. Dashboard

Open RiftTrace Labs.

Show:
- asset count
- vulnerabilities
- business processes
- security controls
- asset criticality chart

Explain that this is the modeled organization.

## 2. Topology

Open Topology.

Show:
- zones
- assets
- directional relationships

Explain that a relationship does not automatically represent
successful attack movement.

## 3. Phase 7 Reachability

Start from Public Web App.

Explain topology-only downstream reachability.

## 4. Phase 8 Security-Aware Propagation

Use Public Web App with LOW privilege.

Show:
- propagated assets
- privilege state
- exploited vulnerabilities
- blocked transitions

Explain the difference between reachability and exploitability.

## 5. Phase 9 Business Impact

Use the same starting asset.

Show how affected assets map to business processes such as
Customer Checkout.

## 6. Counterfactual

Disable the Public Web App → Internal API relationship.

Compare baseline and hypothetical consequence.

Explain that PostgreSQL is unchanged.

## 7. Security Controls

Show the named defensive controls.

## 8. Control Simulation

Apply "Segment Web from Internal API".

Show baseline vs controlled consequence.

## 9. Remediation Ranking

Start from Public Web App.

Rank all candidate controls.

Explain why unrelated controls can rank lower.

## 10. Change Scenario

Change start asset to VPN Gateway.

Run ranking again.

Show that MFA can become more useful for a different scenario.

## Final Message

RiftTrace does not predict the next cyberattack.

It evaluates the potential consequence of modeled compromise
scenarios and compares how defensive changes alter technical
and business impact.
