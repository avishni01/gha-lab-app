# Day 2 Exercise - Broken Workflow Debugging Lab

## Purpose

This exercise uses the intentionally broken workflow:

```text
.github/workflows/04-broken-workflow.yml
```

The goal is to practice real troubleshooting behavior:

1. Run the workflow.
2. Read the first failure.
3. Fix only that failure.
4. Commit and push.
5. Run again.
6. Repeat until the workflow succeeds.

Do not fix everything at once. The learning value comes from reading logs and isolating failures.

## Workflow under test

File:

```text
.github/workflows/04-broken-workflow.yml
```

Known failure categories:

| Failure area | Example |
| --- | --- |
| Wrong working directory | Step points to a path that does not exist |
| Bad dependency command | Workflow references a missing requirements file |
| Missing environment variable | Step expects `APP_ENV` but it is not set |
| Missing secret | Step references a training secret that does not exist |
| Incorrect artifact path | Upload step points to a missing file |

## Exercise setup

Create a branch:

```bash
git checkout main
git pull
git checkout -b day2/fix-broken-workflow
```

Run the workflow manually from GitHub:

```text
Actions -> 04 Broken Workflow -> Run workflow
```

## Step 1 - Record the first failure

Do not edit anything yet.

Open the failed workflow logs and record:

| Item | Notes |
| --- | --- |
| Failed job name | |
| Failed step name | |
| Exact error message | |
| File and line involved, if shown | |
| What you think caused it | |

## Step 2 - Fix only the first failure

Make the smallest possible fix.

Commit format:

```bash
git add .github/workflows/04-broken-workflow.yml
git commit -m "Fix broken workflow working directory"
git push -u origin day2/fix-broken-workflow
```

Run the workflow again.

## Step 3 - Repeat until all failures are fixed

Use this table to track each run:

| Run | Failed step | Root cause | Fix made | Result after fix |
| --- | --- | --- | --- | --- |
| 1 | | | | |
| 2 | | | | |
| 3 | | | | |
| 4 | | | | |
| 5 | | | | |

## Suggested fixes, only after you identify the failure

Use this section only after you have read the logs.

### Working directory issue

Problem pattern:

```yaml
working-directory: ./not-the-app
```

Possible fix:

- Remove `working-directory`, or
- Change it to the repository root, or
- Use a valid path.

### Dependency command issue

Problem pattern:

```yaml
pip install -r requirements-prod.txt
```

Possible fix:

```yaml
pip install -r requirements-dev.txt
```

### Missing environment variable issue

Problem pattern:

```yaml
python -c "import os; assert os.environ['APP_ENV']"
```

Possible fix:

```yaml
env:
  APP_ENV: training
```

Apply it at the step or job level.

### Missing secret issue

Problem pattern:

```yaml
test -n "${{ secrets.DOES_NOT_EXIST_FOR_TRAINING }}"
```

Possible learning choices:

1. Create a temporary repository secret named `DOES_NOT_EXIST_FOR_TRAINING` with a placeholder value.
2. Change the step to use a repository variable instead of a secret.
3. Remove the secret check if this workflow should not depend on secrets yet.

For Day 2, prefer option 2 or 3 unless you specifically want to practice creating secrets.

### Artifact path issue

Problem pattern:

```yaml
path: dist/this-file-does-not-exist.zip
```

Possible fix:

- Create the file before upload, or
- Change the path to an actual file.

Example:

```yaml
- name: Create training artifact
  run: |
    mkdir -p dist
    echo "training artifact" > dist/training-artifact.txt

- name: Upload artifact
  uses: actions/upload-artifact@v4
  with:
    name: training-artifact
    path: dist/training-artifact.txt
    if-no-files-found: error
```

## Pull request review checklist

After the workflow succeeds, open a PR.

Review checklist:

| Check | Done |
| --- | --- |
| The PR explains each failure fixed | |
| The workflow still says it is a training workflow | |
| No real secrets were added | |
| The artifact path points to a real file | |
| The final workflow run succeeds | |
| The PR is not mixed with unrelated changes | |

## Reflection questions

| Question | Your answer |
| --- | --- |
| Which failure was easiest to find? | |
| Which failure was hardest to understand? | |
| Did GitHub show the useful error clearly? | |
| Did local testing help for any issue? | |
| What diagnostic step would you add next time? | |

## Completion criteria

This exercise is complete when:

- You fixed the workflow through at least two small commits.
- You can explain each failure and fix.
- You opened a PR with the final working version.
- You did not expose secrets in logs.
