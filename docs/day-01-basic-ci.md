# Day 1 - GitHub Actions Basic CI

## Purpose

Day 1 focuses on the core GitHub Actions model and the first real CI workflow in this lab.

The objective is not to memorize every GitHub Actions feature. The objective is to become comfortable reading, running, changing, and troubleshooting a basic workflow that builds confidence for later topics such as artifacts, Docker, secrets, environments, reusable workflows, runners, and Jenkins migration.

## Lab repository

Main repository for Day 1:

```text
https://github.com/avishni01/gha-lab-app
```

Other repos exist in the lab, but Day 1 uses only `gha-lab-app`.

| Repo | Used on Day 1? | Purpose |
| --- | --- | --- |
| `gha-lab-app` | Yes | Main FastAPI app and basic CI workflow |
| `gha-lab-shared-workflows` | No | Used later for reusable workflows |
| `gha-lab-infra` | No | Used later for Terraform and deployment practice |
| `gha-lab-jenkins-migration` | No | Used later for Jenkins migration exercises |

## Day 1 outcomes

By the end of Day 1, you should be able to:

1. Explain the basic GitHub Actions execution model.
2. Read a simple workflow YAML file.
3. Explain the difference between workflow, job, step, action, and runner.
4. Explain `uses` versus `run`.
5. Run the sample app locally.
6. Run tests and lint locally.
7. Understand how the CI workflow runs on push and pull request.
8. Trigger a workflow manually with `workflow_dispatch`.
9. Review workflow logs and identify a failed step.
10. Make a small workflow change through a branch and pull request.

## Recommended time plan

| Block | Duration | Focus |
| --- | ---: | --- |
| 1 | 30-45 min | Repo orientation and local app run |
| 2 | 45-60 min | Workflow YAML concepts |
| 3 | 45-60 min | Run tests, lint, and first CI |
| 4 | 45-60 min | Pull request workflow and manual run |
| 5 | 60-90 min | Debugging exercises |
| 6 | 30 min | Notes, review, and checklist |

## Day 1 topics

### Core GitHub Actions concepts

| Topic | What to understand |
| --- | --- |
| Workflow | Automated process defined by a YAML file under `.github/workflows/` |
| Event trigger | The event that starts the workflow, such as push, pull request, or manual dispatch |
| Job | A unit of work that runs on a runner |
| Step | A single action or command inside a job |
| Action | A reusable unit called with `uses` |
| Runner | The machine that executes the job |
| GitHub-hosted runner | Runner managed by GitHub, such as `ubuntu-latest` |
| `uses` | Runs a reusable action or reusable workflow |
| `run` | Runs shell commands directly |
| `with` | Passes inputs to an action |
| `permissions` | Controls the token permissions available to the workflow |
| Workflow logs | Main source for troubleshooting failures |

### GitHub Actions YAML topics for Day 1

Focus only on these YAML keys:

```yaml
name:
on:
permissions:
jobs:
  <job_id>:
    name:
    runs-on:
    steps:
      - name:
        uses:
      - name:
        run:
      - name:
        with:
```

Do not go deep yet into matrix, environments, secrets, reusable workflows, self-hosted runners, OIDC, or deployments. Those are later days.

## Application overview

The Day 1 app is a small FastAPI service.

Important files:

| File | Purpose |
| --- | --- |
| `app/main.py` | FastAPI application code |
| `app/config.py` | Simple app configuration |
| `tests/test_main.py` | Pytest test suite |
| `requirements.txt` | Runtime dependencies |
| `requirements-dev.txt` | Local test and lint dependencies |
| `.github/workflows/01-basic-ci.yml` | Basic CI workflow |

Important endpoints:

| Endpoint | Purpose |
| --- | --- |
| `GET /` | Returns app name and version |
| `GET /health` | Returns health status |
| `GET /config-check` | Checks whether `APP_ENV` is configured |
| `GET /fail-demo` | Intentional failure endpoint for later debugging practice |

## Current workflow under review

File:

```text
.github/workflows/01-basic-ci.yml
```

Expected structure:

```yaml
name: 01 Basic CI

on:
  push:
  pull_request:
  workflow_dispatch:

permissions:
  contents: read

jobs:
  test:
    name: Test Python app
    runs-on: ubuntu-latest

    steps:
      - name: Checkout repository
        uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: "3.12"
          cache: pip

      - name: Install dependencies
        run: pip install -r requirements-dev.txt

      - name: Run lint
        run: ruff check .

      - name: Run tests
        run: pytest
```

## Explanation of the workflow

| Section | Explanation |
| --- | --- |
| `name` | Display name shown in the GitHub Actions tab |
| `on: push` | Runs the workflow when code is pushed |
| `on: pull_request` | Runs the workflow on pull requests |
| `on: workflow_dispatch` | Allows manual execution from the Actions tab |
| `permissions: contents: read` | Gives the workflow read-only repository access |
| `jobs.test` | Defines one job named `test` |
| `runs-on: ubuntu-latest` | Runs the job on a GitHub-hosted Ubuntu runner |
| `actions/checkout@v4` | Checks out the repository files into the runner |
| `actions/setup-python@v5` | Installs/configures Python on the runner |
| `pip install -r requirements-dev.txt` | Installs app, test, and lint dependencies |
| `ruff check .` | Runs lint/static checks |
| `pytest` | Runs automated tests |

## Day 1 learning resources

Use these resources only for the Day 1 topics. Do not try to read the entire documentation set.

| Resource | What to read |
| --- | --- |
| GitHub Actions workflow syntax | Focus on `name`, `on`, `permissions`, `jobs`, `runs-on`, `steps`, `uses`, and `run` |
| GitHub Actions contexts | Skim only. Understand that contexts expose workflow metadata such as `github`, `runner`, and `env` |
| GitHub-hosted runners | Understand what `ubuntu-latest` means and why the workflow can run without your own server |
| `actions/checkout` README | Understand why checkout is usually the first step |
| `actions/setup-python` README | Understand Python version selection and pip cache basics |
| Pytest basics | Only enough to understand test output |
| Ruff basics | Only enough to understand lint output |

## Task 1 - Clone the repository

```bash
git clone https://github.com/avishni01/gha-lab-app.git
cd gha-lab-app
```

Expected result:

```text
You can see app/, tests/, requirements files, and .github/workflows/.
```

## Task 2 - Create a local Python environment

```bash
python3.12 -m venv .venv
source .venv/bin/activate
pip install -r requirements-dev.txt
```

If your machine uses `python3` instead of `python3.12`, use:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements-dev.txt
```

Expected result:

```text
The Python virtual environment is active and dependencies are installed.
```

## Task 3 - Run the app locally

```bash
APP_ENV=local uvicorn app.main:app --reload
```

In another terminal:

```bash
curl http://127.0.0.1:8000/
curl http://127.0.0.1:8000/health
curl http://127.0.0.1:8000/config-check
```

Expected result:

| Endpoint | Expected result |
| --- | --- |
| `/` | App name and version |
| `/health` | Healthy status |
| `/config-check` | `APP_ENV` appears as configured |

## Task 4 - Run tests locally

```bash
pytest
```

Expected result:

```text
All tests pass.
```

Questions to answer:

| Question | Your answer |
| --- | --- |
| How many tests ran? | |
| Which file contains the tests? | |
| Which endpoint tests health? | |
| Which test checks missing `APP_ENV`? | |

## Task 5 - Run lint locally

```bash
ruff check .
```

Expected result:

```text
No lint errors.
```

Questions to answer:

| Question | Your answer |
| --- | --- |
| What tool runs linting? | |
| Where is the tool installed from? | |
| Does lint run before or after tests in the workflow? | |

## Task 6 - Read the workflow file

Open:

```text
.github/workflows/01-basic-ci.yml
```

Fill this table:

| Question | Your answer |
| --- | --- |
| What is the workflow name? | |
| What events trigger the workflow? | |
| What is the job id? | |
| What is the displayed job name? | |
| What runner does it use? | |
| Which steps use `uses`? | |
| Which steps use `run`? | |
| What Python version is configured? | |
| What happens if dependency installation fails? | |
| What happens if lint fails? | |
| What happens if tests fail? | |

## Task 7 - Review the Day 1 workflow improvement PR

Review the PR that adds two Day 1 workflow improvements:

- `workflow_dispatch`
- `permissions: contents: read`

Review checklist:

| Check | Done |
| --- | --- |
| I understand why manual runs are useful | |
| I understand why read-only permissions are safer | |
| I checked the changed YAML indentation | |
| I checked that the workflow still has push and pull request triggers | |
| I checked that the workflow still runs lint and tests | |

After reviewing, merge it only if CI passes.

## Task 8 - Open a small practice PR

Create a new branch:

```bash
git checkout -b day1/my-first-doc-change
```

Make a small documentation-only change, for example add one line to `README.md` or to this guide.

Commit and push:

```bash
git add README.md docs/day-01-basic-ci.md
git commit -m "Practice Day 1 pull request"
git push -u origin day1/my-first-doc-change
```

Open a pull request in GitHub.

Expected result:

```text
The pull request opens and the basic CI workflow appears as a check.
```

Questions to answer:

| Question | Your answer |
| --- | --- |
| Did the workflow start automatically? | |
| Which event triggered it? | |
| Which job ran? | |
| Did the check pass? | |
| Where did you find the logs? | |

## Task 9 - Manually run the workflow

After `workflow_dispatch` is merged, go to:

```text
GitHub -> gha-lab-app -> Actions -> 01 Basic CI -> Run workflow
```

Run the workflow manually.

Expected result:

```text
The workflow runs without creating a new commit.
```

Questions to answer:

| Question | Your answer |
| --- | --- |
| Which branch did you select? | |
| Did the same job run? | |
| Was the log different from push or PR runs? | |

## Task 10 - Debug a failing test

Create a temporary branch:

```bash
git checkout -b day1/break-test-demo
```

Edit `tests/test_main.py` and temporarily change the health test expectation from:

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

Expected local result:

```text
Pytest fails and shows the assertion difference.
```

Push the branch and open a pull request:

```bash
git add tests/test_main.py
git commit -m "Break test for Day 1 debugging practice"
git push -u origin day1/break-test-demo
```

Expected GitHub result:

```text
The workflow fails at the Run tests step.
```

Record:

| Item | Notes |
| --- | --- |
| Failed job name | |
| Failed step name | |
| Error message | |
| How to fix | |

After the exercise, revert or close the PR without merging.

## Task 11 - Debug a lint failure

Create a temporary branch:

```bash
git checkout main
git pull
git checkout -b day1/break-lint-demo
```

Edit `app/main.py` and add an unused import:

```python
import os
```

Run locally:

```bash
ruff check .
```

Expected local result:

```text
Ruff reports an unused import.
```

Push the branch and open a pull request:

```bash
git add app/main.py
git commit -m "Break lint for Day 1 debugging practice"
git push -u origin day1/break-lint-demo
```

Expected GitHub result:

```text
The workflow fails at the Run lint step.
```

Record:

| Item | Notes |
| --- | --- |
| Failed job name | |
| Failed step name | |
| Ruff error code | |
| How to fix | |

After the exercise, revert or close the PR without merging.

## Task 12 - Debug a workflow command failure

Create a temporary branch:

```bash
git checkout main
git pull
git checkout -b day1/break-install-demo
```

Edit `.github/workflows/01-basic-ci.yml` and change:

```yaml
run: pip install -r requirements-dev.txt
```

To:

```yaml
run: pip install -r requirements-missing.txt
```

Push and open a PR.

Expected GitHub result:

```text
The workflow fails at the Install dependencies step.
```

Record:

| Item | Notes |
| --- | --- |
| Failed step name | |
| Command that failed | |
| Exit code if shown | |
| How to fix | |

After the exercise, revert or close the PR without merging.

## Notes template

Create a local notes file outside the repo or inside your own learning notes folder:

```text
learning-notes/day-01-notes.md
```

Use this template:

```markdown
# Day 1 Notes - Basic GitHub Actions CI

## What I practiced

## Commands I used

## Workflow concepts I understand now

## Difference between uses and run

## Trigger types tested

## What failed during practice

## How I found the failure in logs

## Things I still need to review

## Questions for later days
```

## Day 1 completion checklist

| Check | Done |
| --- | --- |
| I cloned the `gha-lab-app` repo | |
| I created a local Python environment | |
| I ran the app locally | |
| I called `/`, `/health`, and `/config-check` | |
| I ran `pytest` locally | |
| I ran `ruff check .` locally | |
| I read `01-basic-ci.yml` | |
| I understand `push`, `pull_request`, and `workflow_dispatch` | |
| I understand `permissions: contents: read` | |
| I understand `uses` versus `run` | |
| I opened or reviewed a pull request | |
| I found workflow logs | |
| I identified a failed step | |
| I practiced at least one failing workflow scenario | |

## What not to cover on Day 1

Avoid these topics for now:

- Secrets
- Repository variables
- GitHub environments
- Deployment approvals
- Docker publishing
- Artifacts
- Matrix builds
- Self-hosted runners
- Reusable workflows
- Terraform
- Jenkins migration
- OIDC
- Production branch protection

These are important, but they belong to later days.

## Day 1 deliverables

At the end of Day 1, you should have:

| Deliverable | Location |
| --- | --- |
| Successful local test run | Local terminal |
| Successful local lint run | Local terminal |
| Reviewed or merged workflow improvement PR | GitHub PR |
| At least one practice PR | GitHub PR |
| Notes from one failed workflow | `learning-notes/day-01-notes.md` |
| Completed checklist | This document |

## Success criteria

Day 1 is complete when you can look at a simple GitHub Actions workflow and explain:

- What starts it.
- Where it runs.
- What each step does.
- Which step failed.
- How to find the logs.
- How to safely make a small workflow change using a branch and PR.
