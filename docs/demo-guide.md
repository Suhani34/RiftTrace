# RiftTrace Demonstration Guide

## Recommended Demo Length

Approximately 7 to 10 minutes.

## 1. Explain the Problem

Start with:

RiftTrace investigates the potential consequence of
a cyber compromise across a modeled organization.

The central question is:

"If this asset is compromised, what could become
reachable, which business operations could
potentially be affected, and which security change
would reduce that impact most?"

## 2. Open the Dashboard

Show the main application and explain that the
environment is organized through the navigation
menu.

## 3. Show Environment Modeling

Open:

- Organizations
- Network Zones
- Assets
- Relationships

Explain that these elements form the technical
environment model.

## 4. Show Topology

Open Topology.

Explain that the graph shows modeled technical
relationships.

Emphasize:

Connectivity alone does not automatically represent
successful compromise.

## 5. Show Vulnerabilities

Open Vulnerabilities.

Explain that vulnerabilities provide security
conditions used by attack-propagation analysis.

## 6. Run a Simulation

Open a relevant simulation view.

Choose a starting asset and starting privilege.

Run the simulation.

Explain the potentially compromised assets and
propagation results.

## 7. Show Business Impact

Show how affected technical assets connect to
business processes.

Explain why the same number of compromised assets
can have different business importance.

## 8. Show Counterfactual Analysis

Modify one modeled condition through a
counterfactual simulation.

Compare the before and after results.

Explain that the original environment is not
destroyed or modified by the simulation.

## 9. Show Remediation Ranking

Open Remediation Ranking.

Explain how candidate defensive changes are
compared based on reduction in modeled consequence.

## 10. Show Attack Paths

Open Path Intelligence.

Show paths and chokepoints.

Explain that path enumeration is bounded and cycle
safe.

## 11. Show Identity Propagation

Open Identity Graph or Identity Propagation.

Explain credential/access relationships and MFA
constraints.

## 12. Show ATT&CK Mapping

Open ATT&CK Mapping.

Explain that ATT&CK provides standardized context
for modeled events but does not create reachability.

## 13. Show Research Evaluation

Open:

- Scenario History
- Evaluation
- Benchmarking

Explain reproducibility and performance evaluation.

## 14. Explain Production Engineering

Briefly mention:

- authentication
- CSRF
- organization isolation
- automated tests
- GitHub Actions
- Docker
- PostgreSQL
- Gunicorn
- Nginx
- health checks
- structured logs

## Closing Statement

RiftTrace is not designed to predict an exact
future attack.

It is designed to provide a reproducible
counterfactual environment where security teams can
explore modeled technical propagation, business
consequence and defensive alternatives.
