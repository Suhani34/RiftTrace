# RiftTrace v1.0.0 Release Checklist

## Backend

- [ ] Django system checks pass
- [ ] migration check passes
- [ ] backend tests pass
- [ ] backend coverage runs

## Simulation

- [ ] simulation-engine tests pass
- [ ] deterministic contract tests pass
- [ ] architecture check passes
- [ ] no unintended ORM dependency exists in the
      simulation engine

## Frontend

- [ ] frontend tests pass
- [ ] ESLint passes
- [ ] production build passes
- [ ] login works
- [ ] logout works
- [ ] protected routes work
- [ ] hamburger navigation works
- [ ] every application route can be opened
- [ ] responsive layout is usable

## Production

- [ ] PostgreSQL is healthy
- [ ] migrations complete
- [ ] Gunicorn backend is healthy
- [ ] Nginx frontend is healthy
- [ ] liveness endpoint works
- [ ] readiness endpoint works
- [ ] login works through production stack
- [ ] structured logs are generated
- [ ] request IDs are returned

## Security

- [ ] no real `.env` file is tracked
- [ ] no production password is tracked
- [ ] no API token is tracked
- [ ] secure production settings exist
- [ ] DEBUG is disabled in production settings

## Documentation

- [ ] README is current
- [ ] architecture documentation is current
- [ ] research positioning is documented
- [ ] deployment documentation is current
- [ ] testing documentation is current
- [ ] demo guide exists
- [ ] portfolio summary exists
- [ ] changelog exists
- [ ] release notes exist

## GitHub

- [ ] working tree is clean
- [ ] main branch contains the final release
- [ ] GitHub Actions backend job passes
- [ ] GitHub Actions frontend job passes
- [ ] version is 1.0.0
- [ ] v1.0.0 tag is created
- [ ] GitHub release is published
