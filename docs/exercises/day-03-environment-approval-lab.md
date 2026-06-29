# Day 3 Exercise - Environment Approval Lab

## Purpose

This exercise focuses on GitHub Environments, approval gates, variables, and secrets using the deployment placeholder workflow.

Workflow:

```text
.github/workflows/06-deploy-placeholder.yml
```

The goal is to simulate a real deployment process without touching real infrastructure.

## Exercise goals

By the end of this exercise, you should be able to:

1. Create `dev` and `prod` environments.
2. Configure environment-specific variables.
3. Configure a placeholder secret.
4. Require approval for prod.
5. Run the deployment placeholder workflow.
6. Observe how prod waits for approval.
7. Confirm that dev runs before prod.
8. Confirm that secrets are not printed.

## Part 1 - Environment setup

Go to:

```text
Repo -> Settings -> Environments
```

Create:

```text
dev
prod
```

## Part 2 - Configure variables

Add this variable to `dev`:

| Variable | Value |
| --- | --- |
| `DEPLOY_TARGET` | `dev-placeholder-target` |

Add this variable to `prod`:

| Variable | Value |
| --- | --- |
| `DEPLOY_TARGET` | `prod-placeholder-target` |

Record:

| Environment | Variable | Value configured? |
| --- | --- | --- |
| dev | `DEPLOY_TARGET` | |
| prod | `DEPLOY_TARGET` | |

## Part 3 - Configure placeholder secret

Create a placeholder secret named:

```text
DEPLOY_TOKEN
```

Use a fake value only, for example:

```text
placeholder-token-for-training-only
```

You can create it as a repository secret or as environment-specific secrets.

For learning, environment-specific secrets are better because they show how dev and prod can be separated.

Record:

| Environment or repo | Secret configured? | Notes |
| --- | --- | --- |
| dev | | |
| prod | | |
| repository-level | | |

## Part 4 - Configure prod approval

For the `prod` environment, configure required reviewer approval if the option is available.

Record:

| Setting | Value |
| --- | --- |
| Required reviewer enabled? | |
| Reviewer username | |
| Can self-approve? | |

## Part 5 - Run the deployment placeholder

Go to:

```text
Actions -> 06 Deploy Placeholder -> Run workflow
```

Run the workflow.

Expected behavior:

1. `deploy-dev` starts first.
2. `deploy-dev` completes.
3. `deploy-prod` waits for prod approval if configured.
4. After approval, `deploy-prod` runs.

Record:

| Item | Notes |
| --- | --- |
| Workflow run URL | |
| Dev job result | |
| Prod job result | |
| Approval required? | |
| Who approved? | |
| Dev target printed | |
| Prod target printed | |

## Part 6 - Validate no secret exposure

Open the logs and search for:

```text
placeholder-token-for-training-only
DEPLOY_TOKEN
```

Expected result:

```text
The secret value should not appear in logs.
```

Record:

| Question | Your answer |
| --- | --- |
| Did the secret value appear? | |
| Was anything masked with `***`? | |
| Which logs did you check? | |

## Part 7 - Test approval behavior

Run the workflow again and do not approve prod immediately.

Record:

| Question | Your answer |
| --- | --- |
| Does the workflow wait? | |
| Which job is waiting? | |
| Can you cancel it? | |
| What happens after approval? | |

## Part 8 - Suggested improvement PR

Create a branch:

```bash
git checkout -b day3/environment-safety-improvements
```

Make one or more safe improvements to `06-deploy-placeholder.yml`:

- Add explicit `permissions: contents: read`.
- Add `concurrency` for deployments.
- Add clearer summary output.
- Add comments explaining that this is placeholder deployment only.

Open a PR.

PR checklist:

| Check | Done |
| --- | --- |
| No real secrets added | |
| No real cloud credentials added | |
| Dev still runs before prod | |
| Prod still uses `environment: prod` | |
| Workflow can still be run manually | |
| Comments are useful but not noisy | |

## Reflection questions

| Question | Your answer |
| --- | --- |
| Why should prod have approval? | |
| What should be different between dev and prod? | |
| What values should be variables? | |
| What values should be secrets? | |
| What should never be logged? | |
| What would change in a real EC2/Azure deployment? | |

## Completion criteria

This exercise is complete when:

- `dev` and `prod` environments exist.
- Placeholder variable or fallback behavior was tested.
- Placeholder secret behavior was tested.
- Prod approval behavior was tested or reviewed.
- You can explain the deployment job order.
