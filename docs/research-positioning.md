# RiftTrace Research Positioning

## Research Problem

Cybersecurity teams often have information about
assets, vulnerabilities, identities and business
services, but understanding the possible consequence
of compromising one element can still require
significant manual reasoning.

RiftTrace explores whether an explicit graph-based
environment model can support structured
counterfactual cyber-risk analysis.

## Central Question

RiftTrace is designed around the question:

> If a particular asset is compromised, what could
> become reachable, what business operations could
> potentially be affected, and which defensive change
> would reduce that impact most?

## Approach

The environment is represented as a graph.

Nodes and supporting entities represent information
such as:

- technical assets
- identities
- business processes
- vulnerabilities
- security controls

Relationships represent modeled connectivity,
dependencies or access.

Simulation logic evaluates possible propagation
through this model subject to explicit security
conditions.

## Counterfactual Reasoning

RiftTrace supports comparisons between an original
modeled environment and modified modeled states.

This enables questions such as:

- What changes if this relationship is disabled?
- What changes if this control is applied?
- Which candidate control reduces modeled business
  impact most?

## Determinism

Simulation behavior is designed to be deterministic.

Given equivalent inputs and configuration, repeated
simulation requests should produce equivalent
results.

This property improves reproducibility for
evaluation and academic analysis.

## Connectivity and Exploitability

A central design principle is:

> Connectivity does not imply exploitability.

An asset being connected or reachable in the graph
does not automatically mean it can be compromised.

Security-aware propagation may additionally depend
on modeled vulnerabilities, privileges,
authentication requirements, MFA and controls.

## Business Consequence

Technical impact alone may not describe operational
importance.

RiftTrace therefore links technical assets to
business processes and uses these dependencies to
identify potential business consequences.

## MITRE ATT&CK

ATT&CK mappings provide standardized security
context for modeled events.

They annotate simulation results rather than create
or expand reachability.

## Evaluation

The platform supports:

- saved scenarios
- repeated runs
- before-and-after comparison
- experiment evaluation
- scalability benchmarking
- CSV reporting

These mechanisms allow simulation behavior to be
examined in a structured and reproducible manner.

## Limitations

RiftTrace does not predict exact future attacks.

Results depend on the modeled environment.

Incomplete or incorrect modeling may result in
incomplete or misleading simulation output.

The system does not independently prove that a
vulnerability can be exploited in a real target.

It does not replace penetration testing, security
monitoring, threat intelligence or incident
response.

Instead, RiftTrace should be viewed as a
decision-support and research platform for exploring
modeled cyber-risk consequences.

## Future Research

Potential future areas include:

- richer probabilistic modeling
- external vulnerability intelligence
- temporal attack modeling
- larger empirical datasets
- validation against real incident data
- advanced control optimization

These areas are intentionally outside the scope of
RiftTrace v1.0.0.
