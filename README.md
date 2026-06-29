# GHA Lab App

Small FastAPI application used to practice GitHub Actions workflows.

## Endpoints

| Endpoint | Purpose |
| --- | --- |
| `GET /` | Returns the app name and version. |
| `GET /health` | Returns `healthy` for CI and smoke-test practice. |
| `GET /config-check` | Checks whether `APP_ENV` is configured. |
| `GET /fail-demo` | Intentionally returns HTTP 500 for debugging practice. |

## Local Commands

```bash
python3.12 -m venv .venv
source .venv/bin/activate
pip install -r requirements-dev.txt
APP_ENV=local uvicorn app.main:app --reload
```

```bash
pytest
ruff check .
docker build -t gha-lab-app:local .
```

## Workflow Learning Order

1. `01-basic-ci.yml`
2. `02-build-and-artifact.yml`
3. `03-docker-build.yml`
4. `04-broken-workflow.yml`
5. `05-debug-practice.yml`
6. `06-deploy-placeholder.yml`
7. `07-reusable-workflow-consumer.yml`

Do not add real secrets to this training project. Use GitHub Actions secrets and variables with placeholder values until you are ready to connect real systems.

