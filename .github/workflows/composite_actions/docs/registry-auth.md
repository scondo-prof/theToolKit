# Registry Auth Composite Action

## Overview

The **registry-auth** composite action authenticates Docker to a container registry. It currently supports **GitHub Container Registry (GHCR)** and is designed to be reused by workflows that build and push Docker images.

## What It Does

When invoked, the action:

1. **Detects the registry type** – Checks whether the provided registry URL contains `"ghcr"` (indicating GitHub Container Registry)
2. **Validates credentials** – If GHCR is detected, uses `gh-username` and `gh-token` for authentication; otherwise exits with an error
3. **Logs in** – Runs `docker login` using `--password-stdin` for secure token handling

## Inputs

| Input               | Type   | Required | Description                                                                 |
| ------------------- | ------ | -------- | --------------------------------------------------------------------------- |
| `auth-registry-url` | string | true     | The registry URL to authenticate against (e.g., `ghcr.io`).                 |
| `gh-username`       | string | false    | Username for the registry. For GHCR, this is typically `github.actor`.      |
| `gh-token`          | string | false    | Authentication token. For GHCR, use a token with `write:packages` scope. Pass via secrets. |

## Behavior

### Supported Registries

- **GitHub Container Registry (ghcr.io)** – Detected when `auth-registry-url` contains the substring `"ghcr"` (e.g., `ghcr.io`).

### Unsupported Registries

If the registry URL does not contain `"ghcr"`, the action exits with:

```
No registry credentials provided
exit 1
```

Support for additional registries (Docker Hub, AWS ECR, etc.) can be added by extending the conditional logic in the action.

## Usage

### Basic Usage (GHCR)

```yaml
steps:
  - name: Registry Auth
    uses: ./.github/workflows/composite_actions/registry-auth.yml
    with:
      auth-registry-url: ghcr.io
      gh-username: ${{ github.actor }}
      gh-token: ${{ secrets.GITHUB_TOKEN }}
```

### From a Reusable Workflow

When called from a `workflow_call` workflow, pass inputs from the workflow inputs and secrets:

```yaml
steps:
  - name: Registry Auth
    uses: ./.github/workflows/composite_actions/registry-auth.yml
    with:
      auth-registry-url: ${{ inputs.auth-registry-build }}
      gh-username: ${{ inputs.gh-username }}
      gh-token: ${{ secrets.gh-token }}
```

### Prerequisites

- **Docker** must be available on the runner (e.g., `ubuntu-latest` includes Docker)
- The **checkout** step is not required before registry-auth; it only runs `docker login`
- For GHCR, the token must have `write:packages` (and `read:packages` if pulling) permissions

## Security

- **Password stdin** – The action uses `echo "$registry_auth_password" | docker login ... --password-stdin` instead of `-p` to avoid exposing the token in process listings (`ps`, `top`).
- **Secrets** – Always pass tokens via `secrets.GITHUB_TOKEN` or repository secrets. Never hardcode tokens or pass them as plain text.
- **Minimal scope** – Use tokens with the minimum required scope for the workflow (e.g., `write:packages` for push-only).

## Implementation Details

The action uses bash `[[ ]]` for substring matching:

```bash
if [[ "${{ inputs.auth-registry-url }}" == *"ghcr"* ]]; then
  # Use gh-username and gh-token
else
  echo "No registry credentials provided"
  exit 1
fi
```

Variables use underscores (e.g., `registry_auth_username`) because bash variable names cannot contain hyphens.

## Related Workflows

- **docker-wf.yml** – Uses this action for authentication before building and pushing Docker images to GHCR.

## Related Documentation

- [GitHub Container Registry](https://docs.github.com/en/packages/working-with-a-github-packages-registry/working-with-the-container-registry)
- [docker login](https://docs.docker.com/engine/reference/commandline/login/)
