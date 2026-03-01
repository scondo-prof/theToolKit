# Docker Workflow

## Overview

This reusable GitHub Actions workflow builds and pushes Docker images to a container registry (e.g., GitHub Container Registry). It uses the **registry-auth** composite action for authentication, keeping the workflow concise and promoting reuse.

## What It Does

When called from another repository or workflow, this workflow:

1. **Runs the build job only when requested** – The `docker-build-image` job runs only when the `trigger-docker-build-image` input is `true`.
2. **Authenticates to the registry** – Uses the registry-auth composite action to log in (supports GHCR)
3. **Checks out the repository** – Gets the source code for the Docker build
4. **Navigates to project path** – Changes to the directory specified by `project-path` (default `"."`) before building
5. **Builds the Docker image** – Runs `docker build` with the specified image name and tag (build args and context are planned for a future update).
6. **Pushes the image** – Pushes the built image to the registry

## Prerequisites

- A **Dockerfile** in the repository root (or adjust the build context path in the workflow)
- **Secrets** passed to the workflow for registry authentication (required):
  - `GH_TOKEN` – A GitHub token with `write:packages` permission (for GHCR) or equivalent for other registries
  - `GH_USERNAME` – Registry username (for GHCR, typically the GitHub actor)
- The workflow expects Docker to be available on the runner (`ubuntu-latest` includes Docker)

## Workflow Inputs

| Input                     | Type    | Required | Default     | Description                                                                 |
| ------------------------- | ------- | -------- | ----------- | --------------------------------------------------------------------------- |
| `trigger-docker-build-image` | boolean | false    | `false`     | When `true`, runs the docker-build-image job. When `false`, the job is skipped. |
| `project-path`            | string  | false    | `"."`       | Path to the project (directory containing the Dockerfile) for build context. |
| `build-image`             | string  | false    | `""`        | Full image name (e.g., `ghcr.io/owner/repo`). Must be set.                   |
| `build-image-tag`         | string  | false    | *(see note)*| Tag for the image. Default uses ref and SHA.                                |
| `auth-registry-build`     | string  | true     | `"ghcr.io"` | Registry URL for login (e.g., `ghcr.io`).                                   |
| `auth-registry-push`      | string  | false    | `"ghcr.io"` | Registry identifier used by registry-auth for push logic.                   |

## Workflow Secrets

| Secret         | Required | Description                                                              |
| -------------- | -------- | ------------------------------------------------------------------------ |
| `GH_TOKEN`    | yes      | Token for registry authentication (e.g. `secrets.GITHUB_TOKEN` for GHCR).|
| `GH_USERNAME` | yes      | Registry username (e.g. `github.actor` or a service account username).   |

**Note:** The docker-build-image job runs only when `trigger-docker-build-image` is `true`. Callers must pass `GH_TOKEN` and `GH_USERNAME` via the `secrets` mapping. `build-image-tag` default expressions in `workflow_call` inputs are limited; callers should explicitly pass `build-image` and `build-image-tag` when using this workflow.

## Usage

### Basic Example

```yaml
name: Build and Push Docker Image

on:
  push:
    branches: [main]

jobs:
  build:
    uses: ./.github/workflows/docker-wf.yml
    with:
      trigger-docker-build-image: true
      project-path: .
      build-image: ghcr.io/${{ github.repository }}
      build-image-tag: ${{ github.sha }}
    secrets:
      GH_TOKEN: ${{ secrets.GITHUB_TOKEN }}
      GH_USERNAME: ${{ github.actor }}
```

### With Custom Registry and Token

```yaml
jobs:
  build:
    uses: ./.github/workflows/docker-wf.yml
    with:
      trigger-docker-build-image: true
      build-image: ghcr.io/myorg/my-app
      build-image-tag: v1.0.0
      auth-registry-build: ghcr.io
    secrets:
      GH_TOKEN: ${{ secrets.GITHUB_TOKEN }}
      GH_USERNAME: ${{ github.actor }}
```

### From Another Repository

```yaml
jobs:
  build:
    uses: owner/repo/.github/workflows/docker-wf.yml@main
    with:
      trigger-docker-build-image: true
      build-image: ghcr.io/owner/repo
      build-image-tag: ${{ github.ref_name }}-${{ github.sha }}
    secrets:
      GH_TOKEN: ${{ secrets.GITHUB_TOKEN }}
      GH_USERNAME: ${{ github.actor }}
```

## Composite Actions Used

This workflow uses **registry-auth** (`.github/workflows/composite_actions/registry-auth.yml`) to handle registry login. This keeps authentication logic in one place and avoids duplicating login steps across workflows.

See [registry-auth documentation](../composite_actions/docs/registry-auth.md) for details on inputs and behavior.

## Permissions

For pushing to GitHub Container Registry, ensure the workflow has `packages: write`:

```yaml
jobs:
  build:
    uses: ./.github/workflows/docker-wf.yml
    permissions:
      contents: read
      packages: write
    with:
      trigger-docker-build-image: true
      build-image: ghcr.io/${{ github.repository }}
      build-image-tag: ${{ github.sha }}
    secrets:
      GH_TOKEN: ${{ secrets.GITHUB_TOKEN }}
      GH_USERNAME: ${{ github.actor }}
```

## Related Documentation

- [Composite Actions (registry-auth)](../composite_actions/README.md)
- [GitHub Container Registry](https://docs.github.com/en/packages/working-with-a-github-packages-registry/working-with-the-container-registry)
