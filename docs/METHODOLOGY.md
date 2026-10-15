# RiftTrace Methodology

## 1. Environment Modeling

An organization is represented using assets, network zones,
directed relationships, vulnerabilities and business
dependencies.

## 2. Reachability

Topology reachability identifies directed downstream assets.

This stage does not claim successful compromise.

## 3. Security-Aware Propagation

Propagation is permitted only when modeled prerequisites are
satisfied.

Examples include:
- sufficient source privilege
- eligible remote vulnerability
- attack-vector conditions
- target privilege requirements
- authentication bypass
- MFA bypass
- local privilege escalation

## 4. Business Impact

Affected technical assets are mapped to explicit business
process dependencies.

Business process impact means potential consequence, not
guaranteed outage.

## 5. Counterfactual Analysis

A baseline simulation is compared with an in-memory modified
environment.

The stored environment is not changed.

## 6. Security-Control Simulation

Named controls are translated into temporary simulation
modifications.

Examples:
- segmentation → relationship removal
- remediation → vulnerability removal
- MFA → MFA requirement
- least privilege → higher source privilege requirement
- authentication enforcement → authentication requirement

## 7. Remediation Ranking

Candidate controls are evaluated independently against the
same baseline.

Ranking uses business-first lexicographic ordering:

1. Critical business processes avoided
2. Critical assets prevented
3. Essential dependency hits reduced
4. Total business processes avoided
5. Total propagated assets prevented

No arbitrary weighted risk score is used.

## 8. Interpretation

Results are deterministic consequences of the supplied model.

They are not predictions of exact real-world attacker
behavior.
