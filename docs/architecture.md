# RiftTrace Architecture

## System Objective

RiftTrace evaluates potential cyber-risk
consequences using an explicit environment model.

The system separates persistence and API
orchestration from simulation logic.

## High-Level Architecture

```text
User
 |
 v
React Frontend
 |
 v
Django REST API
 |
 +--------------------------+
 |                          |
 v                          v
PostgreSQL            Simulation Services
                            |
                            v
                     Simulation Engine
                            |
                            v
                       NetworkX Graph
