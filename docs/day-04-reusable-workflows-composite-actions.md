# Day 4 - Reusable Workflows and Composite Actions

## Purpose

Day 4 focuses on reducing duplication and creating reusable GitHub Actions building blocks.

This is one of the most important topics for pipeline migration work. When many Jenkins pipelines are migrated to GitHub Actions, copy-pasting full workflows across repositories becomes hard to maintain. Reusable workflows and composite actions help create a shared standard.

## Lab repositories

Day 4 uses two repositories:

| Repo | Purpose |
| --- | --- |
| `gha-lab-app` | Consumer repo that calls reusable workflow logic |
| `gha-lab-shared-workflows` | Shared workflow and composite action repo |

Repository URLs:

```text
https://github.com/avishni01/gha-lab-app
https://github.com/avishni01/gha-lab-shared-workflows
```

## Day 4 outcomes

By the end of Day 4, you should be able to:

1. Explain why reusable workflows are useful.
2. Explain why composite actions are useful.
3. Explain the difference between reusable workflows and composite actions.
4. Read a workflow that uses `workflow_call`.
5. Pass inputs to a reusable workflow.
6. Understand reusable workflow outputs.
7. Call a reusable workflow from another repository.
8. Understand basic versioning choices such as `@main`, tags, and SHAs.
9. Identify when not to centralize workflow logic.
10. Design a simple shared workflow pattern for migration projects.

## Recommended time plan

| Block | Duration | Focus |
| --- | ---: | --- |
| 1 | 30-45 min | Reuse concepts and migration motivation |
| 2 | 45-60 min | Review shared workflow repo |
| 3 | 45-60 min | Review consumer workflow in app repo |
| 4 | 60-90 min | Convert local placeholder to shared workflow call |
| 5 | 45-60 min | Composite action review and usage planning |
| 6 | 30 min | Notes, checklist, and design discussion |

## Day 4 topics

### Reusable workflow topics

| Topic | What to understand |
| --- | --- |
| `workflow_call` | Makes a workflow callable from another workflow |
| Inputs | Parameters passed into the reusable workflow |
| Outputs | Values returned from the reusable workflow |
| Secrets | Secrets can be explicitly passed or inherited, depending on design |
| Calling repo | Repo that consumes the reusable workflow |
| Shared repo | Repo that stores reusable workflow definitions |
| Version pinning | Selecting `@main`, a tag, or a commit SHA |
| Governance | Who owns and approves shared workflow changes |

### Composite action topics

| Topic | What to understand |
| --- | --- |
| Composite action | Reusable group of steps stored as an action |
| `action.yml` | Metadata file that defines the action |
| `runs.using: composite` | Declares a composite action |
| Step reuse | Best for repeated step sequences |
| Workflow reuse | Best for repeated job or pipeline structure |

## Reusable workflow vs composite action

| Question | Reusable workflow | Composite action |
| --- | --- | --- |
| Reuses full jobs? | Yes | No |
| Can define `runs-on`? | Yes | No, caller job defines runner |
| Can contain multiple jobs? | Yes | No |
| Can be called as a job? | Yes | No |
| Can be used as a step? | No | Yes |
| Good for standard CI pipelines? | Yes | Sometimes |
| Good for repeated shell steps? | Sometimes | Yes |
| Good for enterprise pipeline templates? | Yes | Sometimes |

Simple rule:

```text
Use reusable workflows for shared pipeline/job structure.
Use composite actions for repeated step logic.
```

## Current shared reusable workflow

Repo:

```text
gha-lab-shared-workflows
```

File:

```text
.github/workflows/reusable-python-ci.yml
```

The reusable workflow is enabled by:

```yaml
on:
  workflow_call:
```

It accepts these inputs:

| Input | Default | Purpose |
| --- | --- | --- |
| `python-version` | `3.12` | Python version to install |
| `test-command` | `pytest` | Command that runs tests |

It returns this output:

| Output | Purpose |
| --- | --- |
| `build-status` | Simple status string for downstream jobs |

## Current app consumer workflow

Repo:

```text
gha-lab-app
```

File:

```text
.github/workflows/07-reusable-workflow-consumer.yml
```

Current behavior:

```yaml
uses: ./.github/workflows/reusable-python-ci-placeholder.yml
```

This means the app repo currently calls a local placeholder reusable workflow.

Day 4 practice changes it to call the shared repo:

```yaml
uses: avishni01/gha-lab-shared-workflows/.github/workflows/reusable-python-ci.yml@main
```

## Important versioning note

For learning, using `@main` is okay.

For production, prefer one of these:

| Option | Example | Why |
| --- | --- | --- |
| Version tag | `@v1` | Stable and readable |
| Commit SHA | `@1a2b3c...` | Strongest immutability |
| Protected branch | `@main` | Convenient, but changes can affect consumers immediately |

For client migration projects, avoid uncontrolled changes to shared workflows. Shared workflow updates should be reviewed carefully because one change can affect many repositories.

## Task 1 - Review the shared workflow

Open:

```text
gha-lab-shared-workflows/.github/workflows/reusable-python-ci.yml
```

Answer:

| Question | Your answer |
| --- | --- |
| What makes this workflow reusable? | |
| Which inputs does it accept? | |
| Which input is required? | |
| What is the default Python version? | |
| What command runs tests by default? | |
| What output does it return? | |
| Which repository will be checked out when it runs? | |

## Task 2 - Review the local placeholder workflow

Open in `gha-lab-app`:

```text
.github/workflows/reusable-python-ci-placeholder.yml
```

Answer:

| Question | Your answer |
| --- | --- |
| Why does the app repo have a local placeholder? | |
| How is it similar to the shared workflow? | |
| How is it different from the shared workflow? | |
| Which approach is better for many repositories? | |

## Task 3 - Review the consumer workflow

Open in `gha-lab-app`:

```text
.github/workflows/07-reusable-workflow-consumer.yml
```

Answer:

| Question | Your answer |
| --- | --- |
| What triggers this workflow? | |
| Which reusable workflow does it currently call? | |
| What inputs are passed? | |
| Does it currently use the shared repo? | |
| What should be changed on Day 4? | |

## Task 4 - Convert the consumer to the shared workflow

Use the exercise file:

```text
docs/exercises/day-04-shared-workflow-consumer-lab.md
```

The exercise walks through updating the consumer workflow from local placeholder to shared reusable workflow.

## Task 5 - Run the consumer workflow

After updating the consumer workflow, go to:

```text
GitHub -> gha-lab-app -> Actions -> 07 Reusable Workflow Consumer -> Run workflow
```

Expected result:

```text
The workflow calls the reusable workflow from gha-lab-shared-workflows and runs the app tests.
```

Record:

| Question | Your answer |
| --- | --- |
| Did the workflow start? | |
| Did it call the shared workflow? | |
| Did checkout run? | |
| Did Python setup run? | |
| Did tests pass? | |
| Where did you see the reusable workflow job in the UI? | |

## Task 6 - Review the composite action

Open in `gha-lab-shared-workflows`:

```text
actions/print-build-info/action.yml
```

Answer:

| Question | Your answer |
| --- | --- |
| What makes this a composite action? | |
| Which values does it print? | |
| Are the printed values safe? | |
| Would this be better as a reusable workflow or composite action? | |
| Where could this action be used? | |

## Task 7 - Design a shared workflow standard

Create a short design note in your learning notes.

Answer:

| Question | Your answer |
| --- | --- |
| What CI steps should be standard across repos? | |
| Which inputs should be configurable? | |
| Which secrets should be allowed? | |
| Who should approve shared workflow changes? | |
| Should consumers use `@main`, `@v1`, or commit SHA? | |
| How would you announce breaking changes? | |

## Recommended migration pattern

For Jenkins migration projects:

| Jenkins pattern | GitHub Actions reuse option |
| --- | --- |
| Shared library for CI | Reusable workflow |
| Shared shell helper | Composite action or script |
| Standard build/test pipeline | Reusable workflow |
| Standard deployment sequence | Reusable workflow with environment inputs |
| Repeated metadata printing | Composite action |
| Repeated cloud login step | Composite action or reusable workflow, depending on scope |

## Notes template

Create or update:

```text
learning-notes/day-04-notes.md
```

Use this template:

```markdown
# Day 4 Notes - Reusable Workflows and Composite Actions

## Why reusable workflows matter

## Why composite actions matter

## Difference between reusable workflows and composite actions

## Shared workflow inputs reviewed

## Consumer workflow change made

## Workflow run result

## Versioning decision notes

## Migration project standards

## Questions for later
```

## Day 4 completion checklist

| Check | Done |
| --- | --- |
| I reviewed the shared reusable workflow | |
| I reviewed the local placeholder workflow | |
| I reviewed the consumer workflow | |
| I understand `workflow_call` | |
| I understand reusable workflow inputs | |
| I understand reusable workflow outputs | |
| I converted the consumer to use the shared repo | |
| I ran the consumer workflow | |
| I reviewed the composite action | |
| I understand when to use reusable workflow vs composite action | |
| I documented a versioning recommendation | |

## What not to cover on Day 4

Avoid these topics for now:

- Large-scale runner autoscaling
- Organization-wide required workflows
- Advanced GitHub API automation
- Publishing marketplace actions
- Full production deployment
- OIDC implementation

These are later enterprise topics.

## Day 4 deliverables

| Deliverable | Location |
| --- | --- |
| Shared workflow review notes | Learning notes |
| Updated consumer workflow PR | GitHub PR |
| Successful consumer workflow run | GitHub Actions |
| Composite action review notes | Learning notes |
| Reuse decision table | Learning notes |

## Success criteria

Day 4 is complete when you can explain:

- Why shared workflows reduce duplicate pipeline code.
- How `workflow_call` makes a workflow reusable.
- How a repo calls a reusable workflow from another repo.
- Why version pinning matters.
- When to use a composite action instead of a reusable workflow.
- What governance is needed before many repos depend on one shared workflow.
