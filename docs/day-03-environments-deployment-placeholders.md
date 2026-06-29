# Day 3 - Environments, Variables, Secrets, and Deployment Placeholders

## Purpose

Day 3 introduces deployment workflow structure without deploying to a real server yet.

The goal is to understand how GitHub Actions models deployment stages such as dev and prod, how environments are used, how variables and secrets are referenced, and how production approval can be simulated safely.

This is still a lab day. Do not add real production secrets or real cloud credentials.

## Lab repository

Main repository:

```text
https://github.com/avishni01/gha-lab-app
```

Day 3 uses this workflow:

```text
.github/workflows/06-deploy-placeholder.yml
```

## Day 3 outcomes

By the end of Day 3, you should be able to:

1. Explain the difference between CI and CD.
2. Explain the difference between build and deploy.
3. Understand GitHub Environments such as `dev` and `prod`.
4. Understand repository variables versus environment variables.
5. Understand where secrets are referenced in workflows.
6. Configure a placeholder `dev` environment.
7. Configure a placeholder `prod` environment.
8. Add manual approval to the `prod` environment.
9. Run a deployment placeholder workflow.
10. Understand job dependencies using `needs`.
11. Explain why production deployment should be gated.

## Recommended time plan

| Block | Duration | Focus |
| --- | ---: | --- |
| 1 | 30-45 min | CI/CD and deployment model concepts |
| 2 | 45-60 min | Read deployment placeholder workflow |
| 3 | 45-60 min | Configure GitHub environments |
| 4 | 45-60 min | Run dev and prod placeholder deployment |
| 5 | 60-90 min | Environment approval and failure scenarios |
| 6 | 30 min | Notes and checklist |

## Day 3 topics

### Deployment workflow topics

| Topic | What to understand |
| --- | --- |
| CI | Build, lint, and test validation |
| CD | Delivery/deployment flow after validation |
| Environment | GitHub deployment target such as dev or prod |
| Environment protection | Rules such as required reviewers before deployment |
| Job dependency | `needs` controls job order |
| Deployment promotion | Dev first, prod later |
| Build once, deploy many | Important production pattern; introduced conceptually today |
| Placeholder deployment | Simulated deployment that does not change real infrastructure |

### Configuration topics

| Topic | What to understand |
| --- | --- |
| `env` | Environment variables available to a job or step |
| `vars` | GitHub repository or environment variables for non-secret config |
| `secrets` | Sensitive values stored by GitHub and masked in logs |
| Environment-specific config | Different values for dev and prod |
| Secret masking | GitHub attempts to hide secret values in logs |
| Safe logging | Never print secrets intentionally |

## Workflow under review

File:

```text
.github/workflows/06-deploy-placeholder.yml
```

Current behavior:

1. Runs manually using `workflow_dispatch`.
2. Also runs on push to `main`.
3. Runs a `deploy-dev` job using the `dev` environment.
4. Runs a `deploy-prod` job after `deploy-dev` using `needs`.
5. Uses `vars.DEPLOY_TARGET` with a fallback placeholder.
6. References `secrets.DEPLOY_TOKEN` with a placeholder fallback.

Important structure:

```yaml
jobs:
  deploy-dev:
    environment: dev
    env:
      APP_ENV: dev
      DEPLOY_TARGET: ${{ vars.DEPLOY_TARGET || 'dev-placeholder' }}

  deploy-prod:
    needs: deploy-dev
    environment: prod
    env:
      APP_ENV: prod
      DEPLOY_TARGET: ${{ vars.DEPLOY_TARGET || 'prod-placeholder' }}
```

## Explanation of key workflow parts

| Part | Explanation |
| --- | --- |
| `workflow_dispatch` | Allows manual deployment simulation |
| `push` to `main` | Simulates automatic deployment after merge |
| `environment: dev` | Associates the job with the GitHub `dev` environment |
| `environment: prod` | Associates the job with the GitHub `prod` environment |
| `needs: deploy-dev` | Prod job waits for dev job to complete successfully |
| `APP_ENV` | Normal environment variable used by the job |
| `vars.DEPLOY_TARGET` | Non-secret configurable deployment target |
| `secrets.DEPLOY_TOKEN` | Placeholder for sensitive deployment credential |

## Important safety rule

For this lab:

```text
Do not add real cloud credentials, production SSH keys, real deploy tokens, or customer secrets.
```

Use placeholder values only.

## Task 1 - Read the deployment workflow

Open:

```text
.github/workflows/06-deploy-placeholder.yml
```

Answer:

| Question | Your answer |
| --- | --- |
| What triggers this workflow? | |
| Which job runs first? | |
| Which job waits for another job? | |
| Which environment is used by the dev job? | |
| Which environment is used by the prod job? | |
| What value does `APP_ENV` have in dev? | |
| What value does `APP_ENV` have in prod? | |
| Is this a real deployment? | |

## Task 2 - Create GitHub environments

In GitHub UI, go to:

```text
Repo -> Settings -> Environments
```

Create two environments:

```text
dev
prod
```

For `dev`:

- No required reviewer yet.
- Optional variable: `DEPLOY_TARGET=dev-placeholder-target`.

For `prod`:

- Add required reviewer approval if available in your GitHub plan/settings.
- Optional variable: `DEPLOY_TARGET=prod-placeholder-target`.

Record:

| Environment | Created? | Required approval? | DEPLOY_TARGET value |
| --- | --- | --- | --- |
| dev | | | |
| prod | | | |

## Task 3 - Add placeholder secret

Create a repository or environment secret only for practice.

Suggested name:

```text
DEPLOY_TOKEN
```

Suggested placeholder value:

```text
placeholder-token-for-training-only
```

Do not use a real token.

Record:

| Question | Your answer |
| --- | --- |
| Where did you create the secret? Repository or environment? | |
| Why should secrets not be printed? | |
| Why is this only a placeholder? | |

## Task 4 - Run deployment placeholder manually

Go to:

```text
GitHub -> gha-lab-app -> Actions -> 06 Deploy Placeholder -> Run workflow
```

Run the workflow.

Expected result:

1. `deploy-dev` starts first.
2. `deploy-prod` waits for `deploy-dev`.
3. If prod approval is configured, the workflow waits for approval before prod.
4. The workflow prints placeholder deployment messages.

Record:

| Question | Your answer |
| --- | --- |
| Did dev run first? | |
| Did prod wait for dev? | |
| Did prod require approval? | |
| What DEPLOY_TARGET was printed for dev? | |
| What DEPLOY_TARGET was printed for prod? | |
| Was any secret printed? | |

## Task 5 - Review deployment history

Open the workflow run and the repository Environments UI.

Record:

| Question | Your answer |
| --- | --- |
| Can you see deployment history for dev? | |
| Can you see deployment history for prod? | |
| Can you identify which commit was deployed? | |
| Can you identify who approved prod? | |

## Task 6 - Create a safer deployment PR

Create a branch:

```bash
git checkout -b day3/deploy-placeholder-improvements
```

Suggested improvements:

1. Add explicit workflow permissions:

```yaml
permissions:
  contents: read
```

2. Add `concurrency` to avoid overlapping placeholder deployments:

```yaml
concurrency:
  group: deploy-placeholder-${{ github.ref }}
  cancel-in-progress: false
```

3. Add a clearer deployment summary step:

```yaml
- name: Deployment summary
  run: |
    echo "Environment: $APP_ENV"
    echo "Commit: $GITHUB_SHA"
    echo "Target: $DEPLOY_TARGET"
```

Commit and open a PR.

Review checklist:

| Check | Done |
| --- | --- |
| The PR does not add real secrets | |
| The workflow still supports manual run | |
| The prod job still depends on dev | |
| Permissions are read-only unless more access is required | |
| Concurrency group is understandable | |

## Task 7 - Failure scenario: dev fails, prod does not run

Create a temporary branch:

```bash
git checkout -b day3/dev-failure-demo
```

Add a temporary failure to the dev deployment step:

```bash
exit 1
```

Push and open a PR or run manually.

Expected result:

```text
deploy-dev fails and deploy-prod does not run because it needs deploy-dev.
```

Record:

| Question | Your answer |
| --- | --- |
| Which job failed? | |
| Did prod run? | |
| What did `needs` control? | |
| How would you fix the failure? | |

Close the PR or revert the branch after the exercise.

## Task 8 - Failure scenario: missing configuration

Temporarily remove or rename `DEPLOY_TARGET` and run the workflow.

Expected result:

```text
The workflow uses the fallback placeholder value.
```

Record:

| Question | Your answer |
| --- | --- |
| Was the fallback value used? | |
| Is fallback behavior good for production? | |
| When should a workflow fail instead of using fallback? | |

## Notes template

Create or update:

```text
learning-notes/day-03-notes.md
```

Use this template:

```markdown
# Day 3 Notes - Environments and Deployment Placeholders

## CI vs CD notes

## Environment setup

## Variables configured

## Secrets configured

## Approval behavior observed

## Deployment workflow run notes

## Failure scenarios tested

## Questions for real deployments
```

## Day 3 completion checklist

| Check | Done |
| --- | --- |
| I read `06-deploy-placeholder.yml` | |
| I understand `environment: dev` and `environment: prod` | |
| I understand `needs: deploy-dev` | |
| I created or reviewed GitHub environments | |
| I configured placeholder variables | |
| I configured a placeholder secret | |
| I ran the deployment placeholder workflow | |
| I observed or configured prod approval | |
| I understand why secrets should not be printed | |
| I tested or understood a dev failure scenario | |
| I understand this is not a real deployment yet | |

## What not to cover on Day 3

Avoid these topics for now:

- Real EC2 or Azure deployment
- Real cloud credentials
- OIDC to AWS or Azure
- Docker image publishing
- Kubernetes deployment
- Self-hosted runners
- Jenkins migration

These will come later after the deployment model is clear.

## Day 3 deliverables

| Deliverable | Location |
| --- | --- |
| Created `dev` environment | GitHub settings |
| Created `prod` environment | GitHub settings |
| Placeholder `DEPLOY_TARGET` variable | GitHub variables |
| Placeholder `DEPLOY_TOKEN` secret | GitHub secrets |
| Deployment placeholder workflow run | GitHub Actions |
| Notes about approval behavior | Notes file |
| Optional deployment improvement PR | GitHub PR |

## Success criteria

Day 3 is complete when you can explain:

- How a deployment workflow differs from a CI workflow.
- Why dev should run before prod.
- How `needs` controls job order.
- How environments help separate dev and prod behavior.
- Why production should have approval.
- Why secrets should not be printed.
- Why this workflow is only a placeholder and not a real deployment.
