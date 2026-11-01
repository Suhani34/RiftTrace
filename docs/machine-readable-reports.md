# RiftTrace Machine-Readable Export and Reporting

## Purpose

RiftTrace supports portable environment exports and machine-readable
simulation reports for automation, reproducibility, interoperability,
and archival use.

## Environment Export

Two environment representations are supported.

### Portable Environment

The portable representation contains:

- schema identifier
- schema version
- generation timestamp
- organization metadata
- SHA-256 integrity identifier
- modeled environment data

The schema identifier is:

`rifttrace.environment`

### Ingestion Environment

The ingestion-ready representation contains:

- network zones
- assets
- relationships
- vulnerabilities

It is intended for reuse through the existing RiftTrace environment
ingestion workflow.

Database primary keys are not used as the portable identity of assets
or relationships. References are represented using modeled object
names where appropriate.

## Saved Scenario Export

Saved scenarios can be exported together with their historical runs.

The scenario export contains:

- scenario definition
- simulation type
- original request payload
- historical run input
- historical run output
- normalized metrics
- status and timestamps

## Simulation Run Report

A single ScenarioRun can be exported as a standalone JSON report.

The schema identifier is:

`rifttrace.simulation-run-report`

The report contains both the simulation request and result so that
the modeled experiment can be understood and reproduced.

## Metrics CSV

Normalized ScenarioRun metrics can also be exported in CSV format for
use with spreadsheets, notebooks, scripts, and external analysis
tools.

## Versioning

Machine-readable documents include a schema version.

The initial version is:

`1.0`

Future incompatible format changes should increment the schema
version rather than silently changing the meaning of existing fields.

## Integrity

Portable environment exports include a SHA-256 digest calculated over
the canonicalized environment data.

The digest is an integrity and reproducibility identifier. It is not
encryption and does not provide confidentiality.

## Interoperability Validation

Environment interoperability is validated by:

1. exporting an existing RiftTrace organization;
2. creating a new organization;
3. submitting the ingestion-ready export through the standard
   ingestion preview;
4. confirming that the exported environment is accepted;
5. applying the import;
6. comparing modeled object counts.

## Scientific Interpretation

RiftTrace simulation exports describe modeled cyber consequences under
specified assumptions.

They do not represent observed attacker activity, predictions of exact
attacker behavior, or guarantees of real-world control effectiveness.
