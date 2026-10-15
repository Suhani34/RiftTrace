# RiftTrace Evaluation

## Objective

Evaluate whether RiftTrace distinguishes the consequence of
different defensive controls under different modeled attack
starting points.

## Scenarios

The repeatable evaluation command considers representative
starting assets such as:

- Public Web App
- VPN Gateway
- Admin Workstation
- CI/CD Server
- Internal API

## Measurements

For each candidate security control RiftTrace records:

- critical business process reduction
- critical asset reduction
- essential dependency hit reduction
- impacted business process reduction
- propagated asset reduction

## Experiment

Run:

```bash
cd backend
python manage.py evaluate_demo
