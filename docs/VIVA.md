# RiftTrace Viva Preparation

## What problem does RiftTrace solve?

Traditional vulnerability information may indicate that a
system has a high-severity weakness but does not necessarily
explain what an attacker could potentially reach, what
business processes depend on those systems, or which
defensive change would reduce the consequence most.

RiftTrace connects those layers.

## Does RiftTrace predict cyberattacks?

No.

RiftTrace performs deterministic scenario-based consequence
analysis using the environment and security conditions that
have been modeled.

## Why NetworkX?

The technical environment naturally forms a directed graph.

NetworkX provides mature graph traversal and path-analysis
algorithms while keeping the simulation engine lightweight.

## Why MultiDiGraph?

Two assets can have multiple distinct relationships.

For example one system may both authenticate to and call
another system.

A MultiDiGraph preserves those separate edges.

## Why isn't connectivity equal to compromise?

Connectivity only indicates that a modeled path exists.

Security-aware propagation additionally evaluates
vulnerabilities, privileges, authentication and MFA
conditions.

## Why does the simulation engine not import Django models?

This separates persistence from analytical logic.

The engine can therefore be tested using plain immutable
records without requiring the Django ORM.

## What is counterfactual analysis?

It compares the baseline model with a temporary modified copy
to answer "what if" questions.

The stored organization model is not modified.

## How is network segmentation modeled?

The selected relationship is temporarily removed from the
counterfactual graph.

This represents the logical consequence of making that
communication path unavailable.

## How is MFA modeled?

An MFA control temporarily requires MFA on a relationship.

Propagation can continue only if the selected modeled
vulnerability is explicitly capable of bypassing MFA.

## How does RiftTrace prioritize controls?

Each candidate control is simulated independently against the
same baseline.

Controls are ranked using business-first lexicographic
ordering:

1. critical process reduction
2. critical asset reduction
3. essential dependency reduction
4. impacted process reduction
5. propagated asset reduction

## Why not use one weighted score?

Arbitrary weights can make the ranking difficult to justify.

RiftTrace keeps the prioritization criteria explicit and
auditable.

## Why can the same control have different ranks?

Because its effectiveness depends on the selected starting
asset, attack path, vulnerabilities and business dependencies.

## What is the main limitation?

RiftTrace only reasons over what has been modeled.

Incomplete or inaccurate asset, vulnerability or business
dependency information can affect the result.

## Is this a real attack simulator?

It is a defensive consequence-analysis platform.

It does not execute exploits or attack real infrastructure.
