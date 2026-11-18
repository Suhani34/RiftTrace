# RiftTrace Backend Reliability

## Error Handling

RiftTrace uses Django REST Framework's
central exception handling mechanism.

Handled API errors preserve DRF's normal
error payload and additionally include the
HTTP status code.

Unexpected programming errors are not
silently converted into validation errors.

## Data Integrity

Data integrity is enforced at multiple layers:

1. Serializer validation
2. Model validation
3. Database constraints where applicable

Cross-organization references are rejected.

## Transaction Boundaries

Multi-record operations that must succeed
or fail together use Django transactions.

Important transactional operations include:

- Environment ingestion apply
- Scenario run numbering/creation

## Simulation Isolation

The pure simulation_engine package does not
perform ORM writes.

Counterfactual and security-control simulations
operate on modeled copies/state rather than
mutating the persisted environment.

## Ingestion Guarantees

Ingestion provides:

- preview before apply
- validation before persistence
- atomic apply
- repeatable/idempotent behavior
- cross-reference validation

## Scenario Reliability

Scenario runs maintain immutable historical
request/result data.

Run numbering is protected against concurrent
creation.

Failed executions are recorded safely without
exposing internal stack traces.

## Request Limits

Backend request/file memory limits are configured
to prevent unbounded in-memory uploads.

## Database Query Practices

Related objects are loaded with select_related()
or prefetch_related() when appropriate to avoid
N+1 query behavior.
