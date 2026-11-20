# RiftTrace

**Counterfactual Cyber Risk Simulation and Business Impact Prioritization Platform**

RiftTrace is a cybersecurity modeling and simulation
platform designed to answer a practical defensive
question:

> If a particular asset is compromised, what could
> become reachable, what business operations could
> potentially be affected, and which defensive change
> would reduce that impact most?

RiftTrace models an organization's technical
environment as a graph containing assets,
relationships, vulnerabilities, identities,
business processes and security controls.

It then performs deterministic simulations over
that model to explore potential compromise
propagation and business consequences.

---

## Important Research Positioning

RiftTrace does **not** claim to predict the exact
cyberattack that will occur in a real environment.

Its results represent modeled possibilities based
on the environment and assumptions supplied to the
simulation.

In particular:

- connectivity does not automatically imply
  exploitability
- attack propagation depends on modeled security
  conditions
- MITRE ATT&CK techniques annotate modeled events
  rather than create reachability
- business impact is derived from modeled
  dependencies
- counterfactual results compare modeled states,
  not guaranteed future outcomes

---

## Core Capabilities

### Environment Modeling

RiftTrace can model:

- organizations
- network zones
- applications
- APIs
- servers
- databases
- cloud services
- network devices
- relationships
- vulnerabilities
- identities
- credentials
- security controls
- business processes

Environment data can also be imported from JSON
and CSV sources.

### Cyber-Risk Simulation

RiftTrace supports:

- topology reachability
- security-aware attack propagation
- privilege-aware propagation
- authentication constraints
- MFA constraints
- vulnerability exploitation
- identity propagation
- credential exposure
- business-impact analysis
- counterfactual simulation
- security-control simulation
- remediation prioritization

### Attack-Path Intelligence

The platform can identify:

- modeled attack paths
- path relationships
- shared nodes
- shared relationships
- potential chokepoints

Path enumeration is bounded to prevent uncontrolled
graph expansion.

### MITRE ATT&CK Context

Modeled security events can be annotated with
relevant MITRE ATT&CK techniques.

ATT&CK mappings provide threat-context information.
They do not independently make an asset reachable.

### Research Evaluation

RiftTrace includes:

- saved scenarios
- scenario runs
- before/after comparison
- experiment evaluation
- scalability benchmarking
- reports
- CSV exports

---

## Architecture

```text
Browser
   |
   v
React + TypeScript
   |
   v
Nginx
   |
   v
Django REST API
   |
   +--------------------+
   |                    |
   v                    v
Simulation Engine    PostgreSQL
   |
   v
Graph / Path /
Impact Analysis
