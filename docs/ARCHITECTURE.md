# RiftTrace Architecture

## Layers

### React Frontend

Responsible for:
- CRUD interfaces
- topology visualization
- simulation forms
- comparison views
- dashboards
- remediation ranking presentation

### Django REST API

Responsible for:
- persistence
- organization isolation
- request validation
- serialization
- simulation orchestration

### PostgreSQL

Stores:
- organizations
- network zones
- assets
- relationships
- vulnerabilities
- business processes
- business dependencies
- candidate security controls

### Simulation Engine

The `simulation_engine` package intentionally does not depend
on Django ORM models.

Django records are converted into immutable simulation
records before analysis.

## Simulation Pipeline

Organization Model
→ Topology Graph
→ Reachability
→ Security-Aware Propagation
→ Business Impact
→ Counterfactual Analysis
→ Security-Control Simulation
→ Remediation Ranking

## Graph Representation

RiftTrace uses a NetworkX MultiDiGraph.

This allows:
- directed dependencies
- multiple relationships between the same two assets
- relationship-specific security metadata

## Important Modeling Principle

Connectivity does not imply exploitability.

A relationship describes modeled connectivity or dependency.

Security-aware propagation additionally checks:
- source privilege
- vulnerability availability
- attack vector
- target privileges required
- authentication
- MFA
- local privilege escalation

## Counterfactual Safety

Hypothetical changes are applied to in-memory graph and
vulnerability copies.

The PostgreSQL environment model is not changed by
simulation.

## Environment Ingestion

External technical environment data is normalized before
being written to RiftTrace's persistence layer.

The ingestion pipeline is:

Source File
→ Parser
→ Normalized Ingestion Records
→ Validation/Preview
→ Atomic Application
→ RiftTrace Domain Models

JSON and CSV use the same normalized ingestion records and
application engine.

A failed validation does not modify the environment.

Applied imports are recorded through `IngestionRun`, but raw
uploaded files are not stored.

##Identity-aware

               TECHNICAL GRAPH
                    │
               compromised
                    ▼
                  Asset
                    │
           credential exposure
                    ▼
                Identity
                    │
              identity link
                    ▼
                 Role
                    │
             identity access
                    ▼
                  Asset
