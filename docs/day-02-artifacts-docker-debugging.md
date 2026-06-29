# Day 2 - Artifacts, Docker Builds, and Debugging

## Purpose

Day 2 builds on the basic CI workflow from Day 1. The focus is to understand how workflows create files, upload artifacts, build Docker images, and expose enough safe diagnostic information to troubleshoot failures.

This day is still not about real deployment. It is about packaging, container build practice, workflow observability, and controlled failure analysis.

## Lab repository

Main repository:

```text
https://github.com/avishni01/gha-lab-app
```

Day 2 uses these workflows:

| Workflow | Purpose |
| --- | --- |
| `.github/workflows/02-build-and-artifact.yml` | Create and upload a source artifact |
| `.github/workflows/03-docker-build.yml` | Build a Docker image on the runner |
| `.github/workflows/04-broken-workflow.yml` | Practice fixing realistic workflow failures |
| `.github/workflows/05-debug-practice.yml` | Practice safe diagnostics and conditional steps |

## Day 2 outcomes

By the end of Day 2, you should be able to:

1. Explain what a GitHub Actions artifact is.
2. Create a package directory during a workflow.
3. Upload and download a workflow artifact.
4. Understand where artifacts appear in the GitHub Actions UI.
5. Build a Docker image on a GitHub-hosted runner.
6. Understand the difference between building and publishing an image.
7. Use safe debug output without exposing secrets.
8. Understand `if: success()`, `if: failure()`, and `if: always()`.
9. Debug common workflow failures one step at a time.

## Recommended time plan

| Block | Duration | Focus |
| --- | ---: | --- |
| 1 | 30-45 min | Review Day 1 and workflow run history |
| 2 | 45-60 min | Artifact workflow |
| 3 | 45-60 min | Docker build workflow |
| 4 | 45-60 min | Safe diagnostics workflow |
| 5 | 60-90 min | Broken workflow debugging lab |
| 6 | 30 min | Notes and checklist |

## Day 2 topics

### Artifact topics

| Topic | What to understand |
| --- | --- |
| Artifact | A file or folder uploaded from a workflow run |
| `actions/upload-artifact` | Standard action for uploading workflow artifacts |
| Artifact name | User-facing name in the workflow run UI |
| Artifact path | Local path on the runner that should be uploaded |
| `if-no-files-found` | Controls whether missing files fail or warn |
| Retention | How long GitHub keeps artifacts; can be configured later |

### Docker topics

| Topic | What to understand |
| --- | --- |
| Dockerfile | Instructions for building the image |
| Docker image build | Local image build on the runner |
| Image tag | Name/version assigned to the image |
| `github.sha` | Commit SHA used as a unique image tag |
| Build vs push | Day 2 only builds the image; it does not publish it |
| Registry | Destination for published images; covered later |

### Debugging topics

| Topic | What to understand |
| --- | --- |
| Step logs | First place to check failures |
| Exit code | Non-zero exit code usually fails the step |
| `success()` | Runs only if prior required steps succeeded |
| `failure()` | Runs only if a prior required step failed |
| `always()` | Runs even if earlier steps failed |
| Safe diagnostics | Print useful context without printing secrets |
| Sensitive data | Never echo secrets or tokens for debugging |

## Workflow 02 - Build and artifact

File:

```text
.github/workflows/02-build-and-artifact.yml
```

What it does:

1. Runs manually using `workflow_dispatch`.
2. Checks out the repository.
3. Creates a `dist` directory.
4. Copies app files and metadata into `dist`.
5. Creates a compressed archive.
6. Uploads the archive as a GitHub Actions artifact.

Important lines to understand:

```yaml
- name: Create package directory
  run: |
    mkdir -p dist
    cp -R app requirements.txt README.md dist/

- name: Create archive
  run: tar -czf gha-lab-app-source.tar.gz -C dist .

- name: Upload artifact
  uses: actions/upload-artifact@v4
  with:
    name: gha-lab-app-source
    path: gha-lab-app-source.tar.gz
    if-no-files-found: error
```

## Workflow 03 - Docker build

File:

```text
.github/workflows/03-docker-build.yml
```

What it does:

1. Runs manually using `workflow_dispatch`.
2. Checks out the repository.
3. Builds a Docker image on the runner.
4. Lists the image.

Important command:

```yaml
run: docker build -t gha-lab-app:${{ github.sha }} .
```

This creates a local image on the GitHub-hosted runner. The image disappears after the job finishes unless you push it to a registry or export it as an artifact. Publishing images is not part of Day 2.

## Workflow 05 - Debug practice

File:

```text
.github/workflows/05-debug-practice.yml
```

This workflow intentionally prints safe runner context and then fails intentionally so that `failure()` and `always()` behavior can be observed.

Safe values printed include:

- Runner OS
- Workspace
- Repository
- Branch/ref
- Event name
- Commit SHA

Do not add secrets to this output.

## Task 1 - Run the artifact workflow

Go to:

```text
GitHub -> gha-lab-app -> Actions -> 02 Build And Artifact -> Run workflow
```

Run it from the selected branch.

Expected result:

```text
The workflow completes successfully and creates an artifact named gha-lab-app-source.
```

Record:

| Question | Your answer |
| --- | --- |
| What job ran? | |
| What artifact was created? | |
| Where did you find the artifact in the UI? | |
| What file was uploaded? | |
| Did the artifact download successfully? | |

## Task 2 - Download and inspect the artifact

Download the artifact from the workflow run UI.

Inspect it locally:

```bash
tar -tzf gha-lab-app-source.tar.gz
```

Expected contents include:

```text
app/
requirements.txt
README.md
```

Record:

| Question | Your answer |
| --- | --- |
| Which files were included? | |
| Was anything missing? | |
| What would you add for a more complete release artifact? | |

## Task 3 - Modify the artifact content

Create a practice branch:

```bash
git checkout -b day2/artifact-improvement
```

Modify `.github/workflows/02-build-and-artifact.yml` to also include the Dockerfile in the artifact:

```bash
cp Dockerfile dist/
```

Commit and push:

```bash
git add .github/workflows/02-build-and-artifact.yml
git commit -m "Include Dockerfile in source artifact"
git push -u origin day2/artifact-improvement
```

Open a pull request and confirm the workflow behavior.

## Task 4 - Run the Docker build workflow

Go to:

```text
GitHub -> gha-lab-app -> Actions -> 03 Docker Build -> Run workflow
```

Expected result:

```text
The Docker image builds successfully and appears in the docker images output.
```

Record:

| Question | Your answer |
| --- | --- |
| What image name was built? | |
| What tag was used? | |
| Why is `github.sha` useful as a tag? | |
| Was the image pushed anywhere? | |

## Task 5 - Run the same Docker build locally

From your local repo:

```bash
docker build -t gha-lab-app:local .
docker images gha-lab-app
```

Optional local run:

```bash
docker run --rm -p 8000:8000 -e APP_ENV=docker gha-lab-app:local
```

Then test:

```bash
curl http://127.0.0.1:8000/health
curl http://127.0.0.1:8000/config-check
```

Record:

| Question | Your answer |
| --- | --- |
| Did the image build locally? | |
| Did the container start? | |
| Did `/health` respond? | |
| Did `APP_ENV` appear as configured? | |

## Task 6 - Run the debug practice workflow

Go to:

```text
GitHub -> gha-lab-app -> Actions -> 05 Debug Practice -> Run workflow
```

Expected result:

```text
The workflow fails intentionally, but the failure(), always(), and diagnostic steps demonstrate useful behavior.
```

Record:

| Question | Your answer |
| --- | --- |
| Which step intentionally failed? | |
| Did the `failure()` step run? | |
| Did the `always()` step run? | |
| Which printed values are useful for debugging? | |
| Did any output include secrets? | |

## Task 7 - Broken workflow debugging lab

Use the separate exercise file:

```text
docs/exercises/day-02-broken-workflow-lab.md
```

The goal is to fix `.github/workflows/04-broken-workflow.yml` one failure at a time.

Do not fix everything blindly. Learn to read the logs and identify the first actual blocking error.

## Notes template

Create or update:

```text
learning-notes/day-02-notes.md
```

Use this template:

```markdown
# Day 2 Notes - Artifacts, Docker, and Debugging

## Artifact workflow notes

## Docker build notes

## Debug practice workflow notes

## Broken workflow failures found

## Commands used

## What I fixed

## What I still need to understand
```

## Day 2 completion checklist

| Check | Done |
| --- | --- |
| I ran the artifact workflow | |
| I downloaded and inspected an artifact | |
| I understand artifact name vs artifact path | |
| I understand `if-no-files-found: error` | |
| I ran the Docker build workflow | |
| I understand build vs push | |
| I ran the debug practice workflow | |
| I understand `success()`, `failure()`, and `always()` | |
| I inspected a failed workflow log | |
| I fixed at least one broken workflow issue | |

## What not to cover on Day 2

Avoid these topics for now:

- Publishing Docker images to a registry
- Production deployment
- Real cloud credentials
- GitHub environments
- OIDC
- Self-hosted runners
- Jenkins migration

## Day 2 deliverables

| Deliverable | Location |
| --- | --- |
| Artifact workflow run | GitHub Actions run |
| Downloaded artifact | Local machine |
| Docker build workflow run | GitHub Actions run |
| Debug workflow observations | Notes file |
| Broken workflow findings | Exercise file or notes |
| Optional artifact improvement PR | GitHub PR |

## Success criteria

Day 2 is complete when you can explain:

- What file was created by a workflow.
- How it was uploaded as an artifact.
- How to find and download that artifact.
- How a Docker image is built in GitHub Actions.
- Why the image is not available after the job unless it is pushed or exported.
- How to use logs and conditional steps to troubleshoot failures.
