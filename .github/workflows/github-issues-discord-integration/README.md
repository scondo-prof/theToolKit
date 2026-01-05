# GitHub Issues Integration Workflow

## Overview

This is a **reusable** GitHub Actions workflow that logs detailed information about GitHub issue events. It extracts and displays issue metadata including basic fields, labels, assignees, milestone, and the full issue body. This workflow is designed to be called from other repositories, where each repository defines its own trigger events.

## File Structure

- `action.yml` - The GitHub Actions reusable workflow definition (must be in `.github/workflows/` directory to be callable)

## Workflow Details

### How It Works

This is a **reusable workflow** that uses `workflow_call` as its trigger. The calling repository defines which issue events trigger the workflow. This allows each repository to customize which issue events they want to monitor.

### Supported Event Types

The calling repository can trigger this workflow for any of the following issue event types:

**Issue Events:**

- `opened` - When a new issue is created
- `closed` - When an issue is closed
- `reopened` - When a closed issue is reopened
- `edited` - When an existing issue is modified
- `deleted` - When an issue is deleted
- `assigned` - When an issue is assigned to someone
- `unassigned` - When an assignee is removed from an issue
- `labeled` - When a label is added to an issue
- `unlabeled` - When a label is removed from an issue
- `milestoned` - When an issue is added to a milestone
- `demilestoned` - When an issue is removed from a milestone

**Issue Comment Events:**

- `created` - When a comment is created on an issue
- `edited` - When an issue comment is edited
- `deleted` - When an issue comment is deleted

### What It Does

When called from another repository, this reusable workflow runs on `ubuntu-latest` and performs two main steps:

#### Step 1: Echo Key Issue Fields

Logs the following basic issue information:

- **Action**: The type of event that triggered the action
- **Repo**: The repository where the issue exists
- **Issue number**: The issue number (with # prefix)
- **Issue title**: The title of the issue
- **Issue state**: Current state (open/closed)
- **Issue URL**: Direct link to the issue
- **Author login**: GitHub username of the issue creator
- **Created at**: Timestamp when the issue was created
- **Updated at**: Timestamp of the last update
- **Is locked**: Whether the issue is locked
- **Comments**: Number of comments on the issue
- **Issue body**: The full body content of the issue

#### Step 2: Echo Labels and Assignees

Extracts and displays structured information from the event JSON payload:

- **Labels**: List of all labels applied to the issue (displayed as bullet points)
- **Assignees**: List of all users assigned to the issue (displayed as bullet points)
- **Milestone**: The milestone associated with the issue (if any)

This step uses `jq` to parse the event payload JSON file located at `${{ github.event_path }}`.

## Usage

### As a Reusable Workflow (Recommended)

This workflow is designed to be called from other repositories. The calling repository defines which issue events trigger it.

#### Step 1: Place the Workflow in the Source Repository

**Important**: Reusable workflows MUST be located in the `.github/workflows/` directory to be callable.

1. The workflow file is located at `.github/workflows/github-issues-discord-integration/workflow.yml`
   - Note: GitHub Actions supports subdirectories within `.github/workflows/` for better organization
2. The workflow uses `workflow_call`, which makes it callable from other repositories
3. The file is already in the correct location and ready to use

#### Step 2: Call from Another Repository

In your calling repository, create a workflow file (e.g., `.github/workflows/github-issues-discord.yml`) with the following content:

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

jobs:
  log_issue_details:
    uses: owner/repo/.github/workflows/github-issues-discord-integration/workflow.yml@main
    # If the workflow is in a different repo, specify the full path:
    # uses: your-org/tools/.github/workflows/github-issues-discord-integration/workflow.yml@main
    # Or if using the relative path within the same repo:
    # uses: ./.github/workflows/github-issues-discord-integration/workflow.yml
```

**Important Path Notes**:

- The `uses:` path must reference `.github/workflows/` directory - this is where reusable workflows must be located
- The workflow is organized in a subdirectory: `github-issues-discord-integration/workflow.yml`
- Subdirectories are supported and help organize multiple workflows
- Replace `owner/repo` with the actual repository path (e.g., `your-org/tools`)
- You can specify a branch (e.g., `@main`), tag (e.g., `@v1.0.0`), or commit SHA (e.g., `@abc123def`)

### Example: Calling from Different Repositories

Each repository can customize which events trigger the workflow:

**Repository A** - Only wants to log new and closed issues:

```yaml
on:
  issues:
    types: [opened, closed]
jobs:
  log_issue_details:
    uses: owner/repo/.github/workflows/github-issues-discord-integration/workflow.yml@main
```

**Repository B** - Wants to monitor all issue changes:

```yaml
on:
  issues:
    types:
      [
        opened,
        closed,
        reopened,
        edited,
        deleted,
        assigned,
        unassigned,
        labeled,
        unlabeled,
        milestoned,
        demilestoned,
      ]
  issue_comment:
    types: [created, edited, deleted]
jobs:
  log_issue_details:
    uses: owner/repo/.github/workflows/github-issues-discord-integration/workflow.yml@main
```

### Prerequisites

- A GitHub repository with Actions enabled
- No additional secrets or permissions required (this workflow only reads public issue data)
- The `jq` command (pre-installed on GitHub-hosted runners)

## Event Payload

The workflow uses `${{ github.event_path }}` which contains the full event payload as JSON. This allows access to all issue data including:

- Issue body (full markdown content)
- Labels (array of objects with `name`, `color`, etc.)
- Assignees (array of user objects)
- Milestone (object with `title`, `number`, etc.)
- And all other issue properties

## Example Output

```
Action:        opened
Repo:          owner/repo-name
Issue number:  #123
Issue title:   Example Issue Title
Issue state:   open
Issue URL:     https://github.com/owner/repo-name/issues/123
Author login:  username
Created at:    2024-01-15T10:30:00Z
Updated at:    2024-01-15T10:30:00Z
Is locked:     false
Comments:      0

--------------------------------

Issue body:     This is the full body content of the issue. It can contain multiple lines and markdown formatting.

--------------------------------

Event payload path: /home/runner/work/_temp/_github_workflow/event.json

Labels:
  • bug
  • high-priority

Assignees:
  • assignee1
  • assignee2

Milestone:
  Sprint 1
```

## Future Enhancements

This workflow currently only logs issue information. Future enhancements could include:

- Sending notifications to Discord webhooks
- Sending notifications to Slack
- Creating automated responses
- Updating external tracking systems
- Processing and formatting issue body content

## Troubleshooting

### Workflow Not Triggering

**For the source repository (where action.yml lives):**

- Ensure the workflow file is in `.github/workflows/` directory
- Check that the file has a `.yml` or `.yaml` extension
- Verify the repository has GitHub Actions enabled

**For the calling repository:**

- Ensure the calling workflow file is in `.github/workflows/` directory
- Verify the `uses:` path is correct (check repository, path, and branch/tag)
- Make sure you've defined the `on:` clause with the issue events you want to trigger on
- Verify the repository has GitHub Actions enabled and has permission to call reusable workflows
- Check the Actions tab in GitHub to see if there are any error messages
- If calling from a different organization, ensure the workflow is public or the organizations have proper permissions

### jq Command Fails

The `jq` command is pre-installed on GitHub-hosted runners. If you see errors:

- Check that the syntax is correct (note the `|| true` at the end prevents failures if fields are empty)
- Ensure `EVENT_PATH` environment variable is set correctly

## Related Documentation

- [GitHub Actions Workflow Syntax](https://docs.github.com/en/actions/using-workflows/workflow-syntax-for-github-actions)
- [GitHub Events Documentation](https://docs.github.com/en/actions/using-workflows/events-that-trigger-workflows#issues)
- [GitHub Contexts and Expression Syntax](https://docs.github.com/en/actions/learn-github-actions/contexts)
- [Reusable Workflows](https://docs.github.com/en/actions/using-workflows/reusing-workflows)
