# dr-demo-partner-gateway

Inbound API gateway for partner integrations.

## Overview

`dr-demo-partner-gateway` is an internal partners service. It exposes a small HTTP API consumed by
other services inside the platform VPC and by the customer-facing gateway.

## Running locally

```bash
pip install -r requirements.txt
FLASK_APP=app/main.py flask run --port 8080
```

## Architecture

- `app/main.py` — HTTP routes and request handling
- `app/db.py` — persistence helpers over PostgreSQL
- `app/reports.py` — scheduled report generation and export
- `app/crypto.py` — token and checksum helpers
- `tests/` — pytest suite, including fixtures that intentionally exercise
  malformed and hostile input

## Deployment

Deployed to Kubernetes via `deploy/` manifests. See `Dockerfile` for the
runtime image.
