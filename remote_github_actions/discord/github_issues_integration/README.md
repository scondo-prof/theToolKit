# GitHub Issues Integration Workflow

## Overview

This GitHub Actions workflow monitors issue events in your repository and logs detailed information about them. The workflow is triggered when issues are opened, edited, closed, or reopened.

## File Structure

- `action.yml` - The GitHub Actions workflow definition

## Workflow Details

### Triggers

The workflow is triggered by the following issue event types:

- `opened` - When a new issue is created
- `edited` - When an existing issue is modified
- `closed` - When an issue is closed
- `reopened` - When a closed issue is reopened

### What It Does

The workflow runs on `ubuntu-latest` and performs two main steps:

#### Step 1: Echo Key Issue Fields

Logs the following basic issue information:

- **Action**: The type of event that triggered the workflow
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

#### Step 2: Echo Labels and Assignees

Extracts and displays structured information from the event JSON payload:

- **Labels**: List of all labels applied to the issue (displayed as bullet points)
- **Assignees**: List of all users assigned to the issue (displayed as bullet points)
- **Milestone**: The milestone associated with the issue (if any)

This step uses `jq` to parse the event payload JSON file located at `${{ github.event_path }}`.

## Usage

### Installation

1. Copy this workflow file to your repository's `.github/workflows/` directory
2. Rename it to something like `github-issues-discord.yml` (or any `.yml` or `.yaml` extension)
3. Commit and push the file to your repository

**Note**: The current file is named `action.yml`, but it contains workflow syntax. For it to work as a GitHub Actions workflow, it should be:

- Located in `.github/workflows/` directory
- Have a `.yml` or `.yaml` extension
- Named something descriptive like `github-issues-discord.yml`

### Prerequisites

- A GitHub repository with Actions enabled
- No additional secrets or permissions required (this workflow only reads public issue data)

## Event Payload

The workflow uses `${{ github.event_path }}` which contains the full event payload as JSON. This allows access to all issue data including:

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
- Triggering other automation workflows

## Troubleshooting

### Workflow Not Triggering

- Ensure the workflow file is in `.github/workflows/` directory
- Check that the file has a `.yml` or `.yaml` extension
- Verify the repository has GitHub Actions enabled
- Make sure you're triggering one of the supported event types

### jq Command Fails

The `jq` command is pre-installed on GitHub-hosted runners. If you see errors:

- Check that the syntax is correct (note the `|| true` at the end prevents failures if fields are empty)
- Ensure `EVENT_PATH` environment variable is set correctly

## Related Documentation

- [GitHub Actions Workflow Syntax](https://docs.github.com/en/actions/using-workflows/workflow-syntax-for-github-actions)
- [GitHub Events Documentation](https://docs.github.com/en/actions/using-workflows/events-that-trigger-workflows#issues)
- [GitHub Contexts and Expression Syntax](https://docs.github.com/en/actions/learn-github-actions/contexts)
