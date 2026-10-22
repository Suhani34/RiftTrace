# RiftTrace

RiftTrace is a counterfactual cyber-risk simulation and
business-impact prioritization platform.

It models an organization's technical environment,
simulates potential compromise propagation under explicit
security prerequisites, maps affected technical assets to
business processes, compares hypothetical defensive changes,
and ranks candidate security controls by modeled consequence
reduction.

## Core Question

If a particular asset is compromised:

1. What could become technically reachable?
2. Which transitions satisfy modeled cybersecurity conditions?
3. Which business processes depend on the affected assets?
4. How would hypothetical defensive changes alter the result?
5. Which candidate control reduces the most important modeled
   consequences?

## Technology Stack

Backend:
- Python
- Django
- Django REST Framework
- PostgreSQL
- NetworkX

Frontend:
- React
- TypeScript
- Vite
- React Flow
- Recharts

Deployment:
- Docker
- Docker Compose
- Gunicorn
- Nginx

## Main Capabilities

- Organization and asset modeling
- Network-zone modeling
- Directed asset relationships
- Vulnerability modeling
- Graph topology visualization
- Topology reachability simulation
- Security-aware propagation
- Privilege escalation modeling
- Authentication and MFA prerequisites
- Business-process dependency modeling
- Business-impact propagation
- Counterfactual simulation
- Security-control simulation
- Business-aware remediation ranking
- JSON environment ingestion
- CSV environment ingestion
- Pre-import validation and preview
- Atomic environment imports
- Repeatable/idempotent imports
- Import history
- Identity modeling
- User/service-account/role representation
- Modeled credential exposure
- Identity-to-identity privilege relationships
- Identity-to-asset access permissions
- MFA-aware identity propagation
- Credential-driven lateral movement analysis

## Simulation Semantics

RiftTrace does not predict exact attacker behavior.

Its results represent potential consequences under the
explicitly modeled topology, vulnerabilities, privileges,
authentication requirements, security controls and
business dependencies.

## Saved Simulation Scenarios

RiftTrace supports reproducible simulation history.

A completed simulation can be saved as a scenario containing
its simulation type and request payload. Each execution creates
an immutable ScenarioRun containing the request used, complete
result payload, normalized comparison metrics, status, and
timestamp.

Saved scenarios can later be rerun against the current modeled
environment. Historical runs remain unchanged, allowing users
to compare modeled before/after results after modifying security
controls, vulnerabilities, relationships, identity access, or
other modeled conditions.

The comparison represents differences between modeled scenarios
and must not be interpreted as observed real-world attack behavior.

## Architecture

Django handles persistence, API validation and orchestration.

The `simulation_engine` package contains the pure graph,
propagation, business-impact, counterfactual, control and
prioritization algorithms.

External data
    ↓
Ingestion parser
    ↓
Normalized records
    ↓
Validation planner
    ↓
Atomic application
    ↓
RiftTrace model

## Local Development

Backend:

```bash
cd backend
source ../.venv/bin/activate
python manage.py migrate
python manage.py runserver

##MITRE ATT&CK Mapping

RiftTrace includes a versioned ATT&CK annotation layer that
maps modeled simulation events to applicable ATT&CK
techniques through deterministic, explainable rules.

Initial supported mappings include:

T1190 — Exploit Public-Facing Application
T1552 — Unsecured Credentials
T1078 — Valid Accounts
T1021 — Remote Services

ATT&CK annotations describe modeled behavior and are not
detections or evidence of observed malicious activity.
ATT&CK source release: v20.0
