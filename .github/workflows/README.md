# Remote Workflows

This directory contains reusable GitHub Actions workflows that can be called from other repositories.

## Overview

These workflows use `workflow_call` triggers, which allows them to be invoked from other repositories. Each workflow is self-contained and designed to perform specific tasks when called.

## Available Workflows

- **github-issues-discord-integration.yml** - Monitors GitHub issue events and sends formatted notifications to Discord

## How to Integrate a Remote Workflow

To use one of these workflows in your repository, follow these steps:

### Step 1: Set Up Required Secrets

Ensure your repository has any required secrets configured. For example:

- `DISCORD_WEBHOOK_URL` - Required for Discord integration workflows

To add secrets:

1. Go to your repository on GitHub
2. Navigate to **Settings** → **Secrets and variables** → **Actions**
3. Click **New repository secret**
4. Add the secret name and value

### Step 2: Create a Workflow File in Your Repository

Create a new workflow file in your repository's `.github/workflows/` directory (e.g., `.github/workflows/use-remote-workflow.yml`).

### Step 3: Define Your Triggers

Define which events should trigger the workflow using the `on:` clause. For example, if using the GitHub Issues Discord Integration workflow:

```yaml
name: GitHub Issues to Discord

on:
  issues:
    types:
      - opened
      - closed
      - reopened
      - edited
      - deleted
      - assigned
      - unassigned
      - labeled
      - unlabeled
      - milestoned
      - demilestoned
  issue_comment:
    types:
      - created
      - edited
      - deleted
```

You can customize which event types trigger the workflow based on your needs.

### Step 4: Call the Remote Workflow

Add a `jobs:` section that calls the remote workflow using the `uses:` keyword:

```yaml
jobs:
  call_remote_workflow:
    uses: scondo-prof/theToolKit/.github/workflows/workflow-name.yml@branch-or-tag
```

**Important Path Format:**

- Replace `scondo-prof/theToolKit` with the repository where the workflow is located
- Replace `workflow-name.yml` with the actual workflow filename (e.g., `github-issues-discord-integration.yml`)
- Replace `branch-or-tag` with the branch, tag, or commit SHA you want to use (e.g., `@main`, `@v1.0.0`, `@abc123def`)

### Complete Example

Here's a complete example workflow file that calls the GitHub Issues Discord Integration workflow:

```yaml
name: GitHub Issues to Discord

on:
  issues:
    types:
      - opened
      - closed
      - reopened
      - edited

jobs:
  notify_discord:
    uses: scondo-prof/theToolKit/.github/workflows/github-issues-discord-integration.yml@main
```

### Example: Calling from Different Repositories

**Repository A** - Only wants to log new and closed issues:

```yaml
on:
  issues:
    types: [opened, closed]
jobs:
  notify_discord:
    uses: scondo-prof/theToolKit/.github/workflows/github-issues-discord-integration.yml@main
```

**Repository B** - Wants to monitor all issue changes:

```yaml
on:
  issues:
    types:
      - opened
      - closed
      - reopened
      - edited
      - deleted
      - assigned
      - unassigned
      - labeled
      - unlabeled
      - milestoned
      - demilestoned
  issue_comment:
    types: [created, edited, deleted]
jobs:
  notify_discord:
    uses: scondo-prof/theToolKit/.github/workflows/github-issues-discord-integration.yml@main
```

## Path Reference Options

When calling a remote workflow, you have several options for the `uses:` path:

1. **From a different repository (same organization):**

   ```yaml
   uses: scondo-prof/theToolKit/.github/workflows/workflow-name.yml@main
   ```

2. **From a different repository (different organization/user):**

   ```yaml
   uses: other-org/repo/.github/workflows/workflow-name.yml@main
   ```

3. **From the same repository (relative path):**

   ```yaml
   uses: ./.github/workflows/workflow-name.yml
   ```

4. **Using a specific tag or version:**

   ```yaml
   uses: scondo-prof/theToolKit/.github/workflows/workflow-name.yml@v1.0.0
   ```

5. **Using a specific commit SHA:**
   ```yaml
   uses: scondo-prof/theToolKit/.github/workflows/workflow-name.yml@abc123def456
   ```

## Requirements

- GitHub Actions must be enabled in your repository
- The source repository (where the workflow is located) must be accessible:
  - If it's a public repository, any repository can call it
  - If it's a private repository, your repository must have access (same organization or appropriate permissions)
- All required secrets must be configured in the calling repository
- Workflows must be located directly in `.github/workflows/` (subdirectories are not supported)

## Troubleshooting

### Workflow Not Running

- Verify the workflow file is in `.github/workflows/` directory in your repository
- Check that the `uses:` path is correct (repository, path, and branch/tag)
- Ensure GitHub Actions is enabled in your repository settings
- Verify you have access to the source repository (if it's private)

### Secrets Not Found

- Check that all required secrets are configured in your repository
- Verify secret names match exactly what the workflow expects
- Ensure secrets are set in **Settings** → **Secrets and variables** → **Actions** → **Repository secrets**

### Permission Errors

- If calling from a private repository, ensure your repository has access to the source repository
- Check that the workflow file has the correct permissions set
- Verify the branch/tag/commit SHA exists in the source repository

## Related Documentation

- [GitHub Actions Reusable Workflows](https://docs.github.com/en/actions/using-workflows/reusing-workflows)
- [GitHub Actions Workflow Syntax](https://docs.github.com/en/actions/using-workflows/workflow-syntax-for-github-actions)
- [GitHub Events Documentation](https://docs.github.com/en/actions/using-workflows/events-that-trigger-workflows)
- [GitHub Secrets Documentation](https://docs.github.com/en/actions/security-guides/encrypted-secrets)
