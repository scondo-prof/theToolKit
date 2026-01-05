# GitHub Issues Integration Workflow

## Overview

This is a GitHub Actions workflow that monitors issue events in your repository and logs detailed information about them. The workflow is triggered when issues are opened, closed, reopened, edited, deleted, assigned/unassigned, labeled/unlabeled, milestoned/demilestoned, or when issue comments are created, edited, or deleted. It extracts and displays issue metadata including basic fields, labels, assignees, milestone, and the full issue body.

## File Structure

- `action.yml` - The GitHub Actions workflow definition (note: this file should be placed in `.github/workflows/` directory in your repository)

## Workflow Details

### Triggers

The workflow is triggered by the following issue event types:

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

This workflow runs on `ubuntu-latest` and performs two main steps:

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

### Installation

1. Copy the `action.yml` file to your repository's `.github/workflows/` directory
2. Rename it to something descriptive like `github-issues-discord.yml` (or any `.yml` or `.yaml` extension)
3. Commit and push the file to your repository
4. The workflow will automatically trigger on the configured issue events

### Alternative: Use as Reusable Workflow

If you want to use this workflow from another repository, you can convert it to a reusable workflow by adding `workflow_call` to the `on:` clause:

```yaml
on:
  workflow_call: # Allows it to be called from other repos
  issues:
    types: [...]
  issue_comment:
    types: [...]
```

Then reference it from another repository's workflow:

```yaml
jobs:
  call-remote-workflow:
    uses: owner/repo/.github/workflows/github-issues-discord.yml@main
```

**Note**: The current `action.yml` file is a standalone workflow that will trigger automatically when placed in `.github/workflows/` directory.

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

- Ensure the workflow file is in `.github/workflows/` directory
- Check that the file has a `.yml` or `.yaml` extension
- Verify the repository has GitHub Actions enabled
- Make sure you're triggering one of the supported event types
- Check the Actions tab in GitHub to see if there are any error messages

### jq Command Fails

The `jq` command is pre-installed on GitHub-hosted runners. If you see errors:

- Check that the syntax is correct (note the `|| true` at the end prevents failures if fields are empty)
- Ensure `EVENT_PATH` environment variable is set correctly

## Related Documentation

- [GitHub Actions Workflow Syntax](https://docs.github.com/en/actions/using-workflows/workflow-syntax-for-github-actions)
- [GitHub Events Documentation](https://docs.github.com/en/actions/using-workflows/events-that-trigger-workflows#issues)
- [GitHub Contexts and Expression Syntax](https://docs.github.com/en/actions/learn-github-actions/contexts)
- [Reusable Workflows](https://docs.github.com/en/actions/using-workflows/reusing-workflows)
