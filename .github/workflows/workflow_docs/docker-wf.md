# Docker Workflow

## Overview

This reusable GitHub Actions workflow builds and pushes Docker images to a container registry (e.g., GitHub Container Registry). It uses the **registry-auth** composite action for authentication, keeping the workflow concise and promoting reuse.

## What It Does

When called from another repository or workflow, this workflow:

1. **Authenticates to the registry** – Uses the registry-auth composite action to log in (supports GHCR)
2. **Checks out the repository** – Gets the source code for the Docker build
3. **Builds the Docker image** – Runs `docker build` with the specified image name and tag
4. **Pushes the image** – Pushes the built image to the registry

## Prerequisites

- A **Dockerfile** in the repository root (or adjust the build context path in the workflow)
- **Secrets** passed to the workflow for registry authentication:
  - `gh-token` – A GitHub token with `write:packages` permission (for GHCR) or equivalent for other registries
- The workflow expects Docker to be available on the runner (`ubuntu-latest` includes Docker)

## Workflow Inputs

| Input                | Type   | Required | Default                     | Description                                                |
| -------------------- | ------ | -------- | --------------------------- | ---------------------------------------------------------- |
| `build-image`        | string | false    | `""`                        | Full image name (e.g., `ghcr.io/owner/repo`). Must be set. |
| `build-image-tag`    | string | false    | *(see note)*                | Tag for the image. Default uses ref and SHA.               |
| `gh-username`        | string | false    | `${{ github.actor }}`       | Registry username (for GHCR, typically the GitHub actor).  |
| `gh-token`           | string | false    | -                           | Token for registry authentication. Pass via `secrets`.     |
| `auth-registry-build`| string | true     | `"ghcr.io"`                 | Registry URL for login (e.g., `ghcr.io`).                  |
| `auth-registry-push` | string | false    | `"ghcr"`                    | Registry identifier used by registry-auth for push logic.  |

**Note:** `build-image-tag` default expressions in `workflow_call` inputs are limited; callers should explicitly pass `build-image` and `build-image-tag` when using this workflow.

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
      build-image: ghcr.io/${{ github.repository }}
      build-image-tag: ${{ github.sha }}
    secrets:
      gh-token: ${{ secrets.GITHUB_TOKEN }}
```

### With Custom Registry and Token

```yaml
jobs:
  build:
    uses: ./.github/workflows/docker-wf.yml
    with:
      build-image: ghcr.io/myorg/my-app
      build-image-tag: v1.0.0
      auth-registry-build: ghcr.io
    secrets:
      gh-token: ${{ secrets.GITHUB_TOKEN }}
```

### From Another Repository

```yaml
jobs:
  build:
    uses: owner/repo/.github/workflows/docker-wf.yml@main
    with:
      build-image: ghcr.io/owner/repo
      build-image-tag: ${{ github.ref_name }}-${{ github.sha }}
    secrets:
      gh-token: ${{ secrets.GITHUB_TOKEN }}
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
      build-image: ghcr.io/${{ github.repository }}
      build-image-tag: ${{ github.sha }}
    secrets:
      gh-token: ${{ secrets.GITHUB_TOKEN }}
```

## Related Documentation

- [Composite Actions (registry-auth)](../composite_actions/README.md)
- [GitHub Container Registry](https://docs.github.com/en/packages/working-with-a-github-packages-registry/working-with-the-container-registry)
