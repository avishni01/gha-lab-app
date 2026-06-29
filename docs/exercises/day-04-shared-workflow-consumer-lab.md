# Day 4 Exercise - Shared Workflow Consumer Lab

## Purpose

This exercise updates the app repository so it consumes the reusable Python CI workflow from the shared workflow repository.

Consumer repo:

```text
gha-lab-app
```

Shared workflow repo:

```text
gha-lab-shared-workflows
```

Workflow to update in the app repo:

```text
.github/workflows/07-reusable-workflow-consumer.yml
```

## Goal

Replace the local placeholder reusable workflow call with a cross-repository reusable workflow call.

Current local placeholder call:

```yaml
uses: ./.github/workflows/reusable-python-ci-placeholder.yml
```

Target shared workflow call:

```yaml
uses: avishni01/gha-lab-shared-workflows/.github/workflows/reusable-python-ci.yml@main
```

## Why this matters

In real migration projects, many repositories may need the same CI pattern. If every repository has its own copied workflow, changes become slow and risky.

A shared workflow allows the team to maintain one standard workflow and reuse it across many repositories.

## Part 1 - Review the current consumer workflow

Open:

```text
.github/workflows/07-reusable-workflow-consumer.yml
```

Record:

| Question | Your answer |
| --- | --- |
| What is the workflow name? | |
| What event triggers it? | |
| What reusable workflow does it currently call? | |
| What inputs are passed? | |
| Is the reusable workflow local or cross-repo? | |

## Part 2 - Review the shared reusable workflow

Open in `gha-lab-shared-workflows`:

```text
.github/workflows/reusable-python-ci.yml
```

Record:

| Question | Your answer |
| --- | --- |
| What keyword makes it reusable? | |
| Which inputs are defined? | |
| What are the default values? | |
| Which output is defined? | |
| What dependencies file does it install if `requirements-dev.txt` exists? | |

## Part 3 - Create a branch

From local `gha-lab-app`:

```bash
git checkout main
git pull
git checkout -b day4/use-shared-reusable-workflow
```

## Part 4 - Update the consumer workflow

Edit:

```text
.github/workflows/07-reusable-workflow-consumer.yml
```

Recommended final version:

```yaml
name: 07 Reusable Workflow Consumer

on:
  workflow_dispatch:

permissions:
  contents: read

jobs:
  call-shared-python-ci:
    name: Call shared reusable Python CI
    uses: avishni01/gha-lab-shared-workflows/.github/workflows/reusable-python-ci.yml@main
    with:
      python-version: "3.12"
      test-command: pytest
```

## Part 5 - Commit and push

```bash
git add .github/workflows/07-reusable-workflow-consumer.yml
git commit -m "Use shared reusable Python CI workflow"
git push -u origin day4/use-shared-reusable-workflow
```

Open a pull request.

## Part 6 - Review the PR

PR review checklist:

| Check | Done |
| --- | --- |
| The workflow still has `workflow_dispatch` | |
| The job uses the shared repo path | |
| The reference is explicit: `@main` | |
| Inputs are still passed correctly | |
| Read-only permissions are configured | |
| No unrelated files changed | |

## Part 7 - Run the workflow

After the PR is open, run:

```text
Actions -> 07 Reusable Workflow Consumer -> Run workflow
```

Expected result:

```text
The consumer workflow calls the reusable workflow from gha-lab-shared-workflows and runs the tests.
```

Record:

| Item | Notes |
| --- | --- |
| Workflow run URL | |
| Did the reusable workflow start? | |
| Did checkout run? | |
| Did Python setup run? | |
| Did dependency install run? | |
| Did tests pass? | |

## Part 8 - Understand the tradeoff of `@main`

For this lab, `@main` is acceptable.

For production, discuss alternatives:

| Reference | Pros | Cons |
| --- | --- | --- |
| `@main` | Easy, always latest | Changes can break consumers immediately |
| `@v1` | Stable and readable | Requires release process |
| Commit SHA | Immutable and safest | Harder to read and update |

Record your recommendation:

| Scenario | Recommended reference |
| --- | --- |
| Personal lab | |
| Small internal team | |
| Client production repos | |
| Regulated environment | |

## Part 9 - Optional improvement: expose the output

The shared workflow returns an output named `build-status`.

Try adding a second job that prints the output.

Example:

```yaml
jobs:
  call-shared-python-ci:
    name: Call shared reusable Python CI
    uses: avishni01/gha-lab-shared-workflows/.github/workflows/reusable-python-ci.yml@main
    with:
      python-version: "3.12"
      test-command: pytest

  print-reusable-output:
    name: Print reusable workflow output
    runs-on: ubuntu-latest
    needs: call-shared-python-ci
    steps:
      - name: Print build status
        run: echo "Build status: ${{ needs.call-shared-python-ci.outputs.build-status }}"
```

If this does not work as expected, record the error and debug it.

## Part 10 - Optional exercise: version tag discussion

Do not create a tag yet unless you want to practice release management.

Instead, write a short proposal:

```markdown
# Shared Workflow Versioning Proposal

## Current reference

@main

## Recommended production reference

@v1 or commit SHA

## Why

## How updates should be reviewed

## How breaking changes should be announced
```

## Troubleshooting guide

| Symptom | Likely cause | What to check |
| --- | --- | --- |
| Workflow cannot find reusable workflow | Wrong repo/path/ref | Check `uses:` path |
| Workflow says reusable workflow not accessible | Permissions or repo visibility | Confirm shared repo is public or accessible |
| Inputs not accepted | Input name mismatch | Check `workflow_call.inputs` |
| Tests fail | App/test issue | Review reusable workflow logs |
| Checkout confusing | Reusable workflow checks out caller repo | Understand checkout behavior |

## Reflection questions

| Question | Your answer |
| --- | --- |
| Why is the shared workflow better than local copy-paste? | |
| What risk does centralization introduce? | |
| Who should own shared workflow changes? | |
| What should be configurable with inputs? | |
| What should not be configurable? | |
| How would this help Jenkins migration? | |

## Completion criteria

This exercise is complete when:

- The consumer workflow calls the shared workflow repo.
- A PR exists for the change.
- The workflow was run manually.
- You understand what `workflow_call` does.
- You can explain why production should avoid uncontrolled `@main` dependencies.
