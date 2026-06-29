# Day 1 - Basic GitHub Actions CI

## Goal

By the end of this day you should be able to read, run, and troubleshoot a basic GitHub Actions CI workflow for a small Python FastAPI application.

## Main files

| File | Purpose |
| --- | --- |
| `app/main.py` | FastAPI application code |
| `tests/test_main.py` | Pytest test suite |
| `requirements-dev.txt` | Development dependencies for linting and tests |
| `.github/workflows/01-basic-ci.yml` | Basic CI workflow |

## Concepts to learn

- Workflow
- Event trigger
- Job
- Step
- Runner
- `uses` versus `run`
- GitHub-hosted runner
- Workflow logs
- Pull request checks
- Manual workflow run with `workflow_dispatch`
- Minimal workflow permissions

## Task 1 - Run the app locally

```bash
python3.12 -m venv .venv
source .venv/bin/activate
pip install -r requirements-dev.txt
APP_ENV=local uvicorn app.main:app --reload
```

Open or curl these endpoints:

```bash
curl http://127.0.0.1:8000/
curl http://127.0.0.1:8000/health
curl http://127.0.0.1:8000/config-check
```

Expected result:

- `/` returns the app name and version.
- `/health` returns healthy status.
- `/config-check` shows that `APP_ENV` is configured.

## Task 2 - Run tests locally

```bash
pytest
```

Expected result: all tests pass.

## Task 3 - Run lint locally

```bash
ruff check .
```

Expected result: no lint errors.

## Task 4 - Read the workflow

Open:

```text
.github/workflows/01-basic-ci.yml
```

Answer these questions:

| Question | Your answer |
| --- | --- |
| What triggers the workflow? | |
| What runner does the job use? | |
| How many jobs are defined? | |
| Which steps use `uses`? | |
| Which steps use `run`? | |
| What happens if lint fails? | |
| What happens if tests fail? | |

## Task 5 - Review the pull request workflow

Create a branch, make a small change, and open a pull request.

Recommended small change:

- Add a comment to this guide.
- Or change the README wording only.

Validate that the CI workflow appears as a PR check.

## Task 6 - Manual workflow run

After the workflow includes `workflow_dispatch`, go to:

```text
Actions -> 01 Basic CI -> Run workflow
```

Run it manually from the selected branch.

## Task 7 - Debug a failing test

Temporarily change the health test expectation from:

```python
assert response.json() == {"status": "healthy"}
```

To:

```python
assert response.json() == {"status": "broken"}
```

Run locally:

```bash
pytest
```

Then push to a temporary branch and observe the workflow failure in GitHub Actions.

Revert the change after the exercise.

## Task 8 - Debug a lint failure

Temporarily add an unused import to `app/main.py`:

```python
import os
```

Run:

```bash
ruff check .
```

Then push to a temporary branch and observe the workflow failure in GitHub Actions.

Revert the change after the exercise.

## Completion checklist

| Check | Done |
| --- | --- |
| I can explain what a workflow is | |
| I can explain what a job is | |
| I can explain what a step is | |
| I understand `uses` versus `run` | |
| I can trigger a workflow on push | |
| I can trigger a workflow on pull request | |
| I can trigger a workflow manually | |
| I can find workflow logs | |
| I can identify the failed step | |
| I can fix a simple workflow failure | |

## Notes

Do not add real secrets during Day 1. Secrets, variables, environments, and deployment approvals are covered later in the learning path.
