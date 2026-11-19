# RiftTrace Simulation Engine Verification

## Purpose

RiftTrace is a model-driven cybersecurity
consequence simulator.

It does not claim to predict the exact actions
of a real attacker.

Given a modeled compromise scenario, RiftTrace
calculates potential technical and business
consequences under the assumptions represented
in the environment model.

## Core Architecture

The simulation engine is separated from the
Django application layer.

The architecture is:

Django ORM
→ service / adapter layer
→ immutable record structures
→ pure simulation engine
→ result structures

The production simulation engine does not
perform Django ORM queries or writes.

## Determinism

RiftTrace simulations are deterministic for a
fixed modeled input.

The same environment state, start state and
simulation parameters should produce the same
modeled result.

The production engine does not intentionally
use random-number generation.

## Reachability

Topology reachability represents modeled
connectivity.

Reachability does not by itself indicate that
a target asset can be compromised.

## Attack Propagation

Attack propagation is security-aware.

A modeled transition may depend on:

- source privilege
- target vulnerabilities
- vulnerability exploitability
- vulnerability attack vector
- required privileges
- authentication requirements
- MFA requirements
- authentication/MFA bypass properties

Connectivity alone is insufficient for attack
propagation.

## Privilege

RiftTrace models LOW and HIGH privilege states.

Relationships may require a minimum source
privilege.

Successful modeled vulnerabilities may grant
privilege.

Local privilege-escalation vulnerabilities may
increase privilege on an already compromised
asset.

## Authentication and MFA

Authentication and MFA affect transition
eligibility.

They are not implemented as arbitrary numerical
risk-score reductions.

## Business Impact

Technical propagation may be mapped to business
process dependencies.

Results describe potential business consequences
within the modeled environment.

RiftTrace does not claim a deterministic real
financial loss unless such a financial model is
explicitly provided.

## Counterfactual Simulation

Counterfactual simulations compare a baseline
against temporary modeled changes.

Counterfactual modifications do not mutate the
persisted source environment.

## Security Controls

Supported modeled controls affect explicit
simulation behavior:

- network segmentation
- vulnerability remediation
- MFA
- least privilege
- authentication enforcement

Controls are evaluated by rerunning the modeled
scenario rather than subtracting arbitrary risk
points.

## Remediation Ranking

Control ranking is business-first and
lexicographic.

The ordering considers:

1. critical business-process reduction
2. critical asset reduction
3. essential dependency-hit reduction
4. impacted process reduction
5. propagated asset reduction

Dense ranking is used for equivalent outcomes.

## Identity Propagation

Identity-aware propagation uses a fixed-point
process.

Compromised assets may reveal modeled credential
exposures.

Acquired identities may traverse identity links
and access assets subject to privilege and MFA
requirements.

Propagation stops when no additional state can
be acquired.

## MITRE ATT&CK Mapping

ATT&CK mappings annotate modeled propagation
events.

ATT&CK annotations do not create attack
reachability.

A mapping indicates that a modeled event is
consistent with a technique, not that the
technique was observed in the real world.

## Path Intelligence

Attack-path intelligence reuses the
security-aware attack-propagation semantics.

It does not treat every topology edge as an
attack edge.

Path enumeration is bounded by maximum depth
and maximum path count.

Cycles are prevented from causing unbounded
path enumeration.

## Chokepoints

Node and edge chokepoints indicate modeled
components that occur across multiple modeled
attack paths.

A chokepoint is analytical evidence and is not
automatically proof of the globally optimal
remediation.

## Side-Effect Safety

Pure simulation operations do not modify their
input graph.

Counterfactual and control simulations do not
persist temporary modeled changes into the
source environment.

## Verification

Run:

```bash
./scripts/simulation_quality_gate.sh
