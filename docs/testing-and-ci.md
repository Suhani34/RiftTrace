# RiftTrace Testing and CI

## Purpose

RiftTrace uses automated testing and quality gates
to protect the correctness of the application and
the counterfactual cyber-risk simulation model.

A change should not be considered ready until the
relevant automated quality gates pass.


## Backend Testing

The backend uses Django's built-in test runner.

The backend suite covers areas including:

- authentication and authorization
- organization isolation
- assets and relationships
- vulnerabilities
- business processes
- counterfactual simulations
- security controls
- identity propagation
- ATT&CK annotations
- saved scenarios
- reporting
- evaluation
- simulation behaviour


## Simulation Verification

The simulation engine has additional contract and
architecture verification.

Important properties include:

- deterministic results
- connectivity is not treated as exploitability
- privilege semantics are respected
- authentication and MFA constraints are respected
- simulation inputs are not mutated
- path enumeration is bounded
- cycles do not create infinite propagation
- ATT&CK mappings annotate modeled events
- Django ORM access is kept outside the pure engine


## Frontend Testing

The frontend uses Vitest and Testing Library.

Tests focus on behaviour rather than internal React
implementation details.

Current critical areas include:

- shared page states
- protected routes
- authentication transitions
- CSRF initialization
- API request behaviour
- error handling


## Frontend Quality Gate

Run:

```bash
./scripts/frontend_quality_gate.sh
