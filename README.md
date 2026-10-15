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

## Simulation Semantics

RiftTrace does not predict exact attacker behavior.

Its results represent potential consequences under the
explicitly modeled topology, vulnerabilities, privileges,
authentication requirements, security controls and
business dependencies.

## Architecture

Django handles persistence, API validation and orchestration.

The `simulation_engine` package contains the pure graph,
propagation, business-impact, counterfactual, control and
prioritization algorithms.

## Local Development

Backend:

```bash
cd backend
source ../.venv/bin/activate
python manage.py migrate
python manage.py runserver
