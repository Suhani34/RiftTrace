# RiftTrace Evaluation Protocol

## Purpose

The evaluation measures how modeled cybersecurity controls alter
the simulated consequences of a specified compromise within the
RiftTrace digital environment model.

The evaluation does not claim to reproduce exact real-world attacker
behavior or to estimate real-world attack probability.

## Research Questions

### RQ1

How do modeled defensive changes affect the number of assets that
become potentially reachable or compromised from the same initial
compromise?

### RQ2

How do modeled authentication and privilege controls affect acquired
identities and assets reached through identity-based access?

### RQ3

How do modeled defensive changes affect the number and criticality of
business processes potentially impacted by a compromise scenario?

### RQ4

Which modeled security-control changes produce the greatest reduction
in simulated technical and business exposure?

## Experimental Method

Each controlled experiment consists of:

1. A fixed organization model.
2. A fixed initial compromise scenario.
3. A baseline simulation run.
4. One explicitly documented modeled defensive change.
5. A treatment simulation run using the same initial compromise.
6. A comparison of shared quantitative metrics.

The baseline and treatment results are preserved as immutable
ScenarioRun records.

EvaluationExperiment records identify the intervention and link the
baseline and treatment runs.

## Metrics

Depending on the simulation type, metrics may include:

- potentially reachable assets
- propagated assets
- compromised assets
- critical assets
- impacted business processes
- critical business processes
- essential dependency hits
- acquired identities
- successful identity-propagation steps
- assets reached through identity access

Metrics are evaluated independently.

RiftTrace does not create an arbitrary weighted aggregate risk score
for the research evaluation.

## Interpretation

For exposure metrics where lower values represent reduced modeled
exposure:

reduction = baseline value - treatment value

A positive reduction is labelled IMPROVED.

A zero reduction is labelled UNCHANGED.

A negative reduction is labelled WORSENED.

## Evaluation Design

Primary controlled experiments should modify one defensive condition
at a time while preserving the initial compromise scenario.

Examples include:

- network segmentation
- vulnerability remediation
- MFA enforcement
- least privilege
- authentication enforcement

Additional combined-control experiments may be performed separately.

## Reproducibility

Each experiment stores references to:

- organization
- saved scenario
- baseline run
- treatment run
- intervention
- comparison metrics

The complete simulation request and result snapshots remain stored in
the associated ScenarioRun records.

Evaluation results can be exported to CSV for independent inspection
and report analysis.

## Limitations

RiftTrace evaluates consequences within a user-defined environment
model.

The results depend on the completeness and correctness of that model.

Connectivity does not necessarily imply exploitability.

MITRE ATT&CK annotations indicate that modeled events are consistent
with mapped techniques; they do not indicate observed or detected
attacker behavior.

The evaluation uses descriptive simulation results and does not, by
itself, establish statistical evidence of real-world security-control
effectiveness.
