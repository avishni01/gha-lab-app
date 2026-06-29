# Day 4 Exercise - Composite Action Review Lab

## Purpose

This exercise reviews the composite action in the shared workflow repository.

Shared repo:

```text
gha-lab-shared-workflows
```

Composite action:

```text
actions/print-build-info/action.yml
```

## Goal

Understand how a composite action packages repeated step logic and when it should be used instead of a reusable workflow.

## Part 1 - Open the composite action

Open:

```text
gha-lab-shared-workflows/actions/print-build-info/action.yml
```

Review the structure:

```yaml
runs:
  using: composite
  steps:
    - name: Print safe context
      shell: bash
      run: |
        echo "Repository: $GITHUB_REPOSITORY"
        echo "Ref: $GITHUB_REF"
        echo "Runner OS: $RUNNER_OS"
        echo "Commit SHA: $GITHUB_SHA"
        echo "Workflow: $GITHUB_WORKFLOW"
```

## Part 2 - Identify the composite action structure

| Question | Your answer |
| --- | --- |
| Which key identifies this as a composite action? | |
| Does it define a full job? | |
| Is it called as a step or as a job? | |
| Which shell does it use? | |
| What values does it print? | |

## Part 3 - Decide where this action could be useful

| Workflow | Useful? | Notes |
| --- | --- | --- |
| Basic CI workflow | | |
| Docker build workflow | | |
| Debug practice workflow | | |
| Deployment placeholder workflow | | |
| Shared reusable Python CI workflow | | |

## Part 4 - Optional practice: call the composite action

Create a branch in `gha-lab-app`:

```bash
git checkout main
git pull
git checkout -b day4/use-print-build-info-action
```

Add this step to `05-debug-practice.yml` after checkout:

```yaml
- name: Print shared build info
  uses: avishni01/gha-lab-shared-workflows/actions/print-build-info@main
```

Commit and push:

```bash
git add .github/workflows/05-debug-practice.yml
git commit -m "Use shared print build info composite action"
git push -u origin day4/use-print-build-info-action
```

Open a PR and run the workflow.

## Part 5 - Compare reusable workflows and composite actions

| Scenario | Better option | Why |
| --- | --- | --- |
| Standard Python CI job | | |
| Print build metadata | | |
| Standard deployment flow | | |
| Repeated shell validation step | | |
| Multi-job pipeline | | |
| Small repeated command sequence | | |

## Part 6 - Production considerations

| Question | Your answer |
| --- | --- |
| Should this action be referenced with `@main` in production? | |
| Would a version tag such as `@v1` be safer? | |
| Who should approve updates to the shared action? | |
| What information should not be printed by shared actions? | |

## Completion criteria

This exercise is complete when:

- You can explain what `runs.using: composite` means.
- You can explain why this is a step-level reusable unit.
- You can explain when to use a composite action instead of a reusable workflow.
- You can explain why shared actions need careful review before production use.
