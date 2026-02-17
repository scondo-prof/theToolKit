# Composite Actions

This directory contains reusable composite actions used by workflows in this repository. Composite actions bundle multiple steps into a single reusable unit, reducing duplication and keeping workflows maintainable.

## Overview

Composite actions are similar to custom actions but are defined as YAML files in the repository. They:

- Accept **inputs** from the calling workflow
- Run a sequence of **steps** (shell commands or other actions)
- Promote **DRY** – write once, use in many workflows

For more on composite actions, see [GitHub: Creating a composite action](https://docs.github.com/en/actions/creating-actions/creating-a-composite-action).

## Available Composite Actions

| Action         | File             | Description                                           | Documentation                |
| -------------- | ---------------- | ----------------------------------------------------- | ---------------------------- |
| **registry-auth** | `registry-auth.yml` | Authenticates Docker to a container registry (GHCR). | [docs/registry-auth.md](docs/registry-auth.md) |

## Using Composite Actions

To use a composite action from a workflow:

```yaml
steps:
  - uses: ./.github/workflows/composite_actions/action-name.yml
    with:
      input-name: value
```

For actions that require secrets:

```yaml
steps:
  - uses: ./.github/workflows/composite_actions/registry-auth.yml
    with:
      auth-registry-url: ghcr.io
      gh-username: ${{ github.actor }}
      gh-token: ${{ secrets.GITHUB_TOKEN }}
```

See each action's documentation in the `docs/` directory for detailed inputs, behavior, and usage examples.

## Adding New Composite Actions

1. Create a new `.yml` file in this directory (e.g., `my-action.yml`)
2. Define `name`, `description`, `inputs`, and `runs.using: "composite"` with `runs.steps`
3. Add a detailed doc file in `docs/` (e.g., `docs/my-action.md`)
4. Add the action to the table above with a link to its documentation
5. Reference it from workflows that need the logic
