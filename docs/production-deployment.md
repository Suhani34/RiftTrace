# RiftTrace Production Deployment

## Architecture

RiftTrace uses the following production-style
deployment architecture:

Browser
→ Nginx
→ React production bundle

API requests:
Browser
→ Nginx `/api`
→ Gunicorn
→ Django
→ PostgreSQL


## Production Application Server

Django's development server is not used in
production.

Gunicorn serves the Django WSGI application.


## Reverse Proxy

Nginx serves the compiled React frontend and
proxies `/api` requests to the Django backend.

Only the reverse proxy should be publicly
reachable.

The PostgreSQL database and Gunicorn backend
should remain on the internal container network.


## Production Settings

Production Django uses:

`config.settings_prod`

Important properties include:

- DEBUG disabled
- environment-based SECRET_KEY
- environment-based database credentials
- configurable ALLOWED_HOSTS
- configurable CSRF trusted origins
- secure cookies for HTTPS deployments
- HTTPS redirect support
- HSTS support
- proxy HTTPS awareness
- structured logging


## Secrets

Production secrets are stored outside Git.

The real production file is:

`.env.prod`

The repository contains only:

`.env.prod.example`

Never commit `.env.prod`.


## Health Endpoints

Liveness:

`/api/health/live/`

This verifies that the Django application is
running.

Readiness:

`/api/health/ready/`

This verifies that the application can reach
its PostgreSQL database.


## Request IDs

Responses include an `X-Request-ID` header.

Request IDs are included in structured backend
logs so requests can be correlated during
troubleshooting.


## Logging

Production Django logs are written as structured
JSON to standard output.

Containers therefore remain compatible with
container logging systems and external log
collectors.


## Docker Compose

The production-style stack is defined in:

`docker-compose.prod.yml`

Services include:

- PostgreSQL
- migration job
- Django/Gunicorn backend
- React/Nginx frontend


## Start

```bash
docker compose \
  -f docker-compose.prod.yml \
  --env-file .env.prod \
  up -d
