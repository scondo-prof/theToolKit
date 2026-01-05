# GitHub Issues Integration Action

## Overview

This is a GitHub Actions composite action that logs detailed information about GitHub issue events. It extracts and displays issue metadata including basic fields, labels, assignees, milestone, and the full issue body. This action is designed to be used within a workflow that monitors issue events.

## File Structure

- `action.yml` - The GitHub Actions composite action definition

## Action Details

### What It Does

This composite action performs two main steps:

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

This is a composite action that should be used within a GitHub Actions workflow. To use it:

1. Reference this action in your workflow file (`.github/workflows/*.yml`)
2. Set up the workflow to trigger on issue events

### Example Workflow

Create a workflow file (e.g., `.github/workflows/github-issues-discord.yml`) with the following content:

```yaml
name: GitHub Issues to Discord

on:
  issues:
    types:
      - opened
      - edited
      - closed
      - reopened

jobs:
  log_issue_details:
    runs-on: ubuntu-latest
    steps:
      - name: Use GitHub Issues Integration Action
        uses: ./remote_github_actions/discord/github_issues_integration
```

**Note**: The path `./remote_github_actions/discord/github_issues_integration` assumes the action is in your repository at that location. Adjust the path accordingly, or reference it via a repository path if it's in a separate repo.

### Prerequisites

- A GitHub repository with Actions enabled
- No additional secrets or permissions required (this action only reads public issue data)
- The `jq` command (pre-installed on GitHub-hosted runners)

## Event Payload

The action uses `${{ github.event_path }}` which contains the full event payload as JSON. This allows access to all issue data including:

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

This action currently only logs issue information. Future enhancements could include:

- Sending notifications to Discord webhooks
- Sending notifications to Slack
- Creating automated responses
- Updating external tracking systems
- Processing and formatting issue body content

## Troubleshooting

### Action Not Running

- Ensure the action is being called from within a workflow file
- Check that the workflow file is in `.github/workflows/` directory
- Verify the repository has GitHub Actions enabled
- Make sure your workflow is configured to trigger on issue events
- Verify the path to the action is correct (if using a local action)

### jq Command Fails

The `jq` command is pre-installed on GitHub-hosted runners. If you see errors:

- Check that the syntax is correct (note the `|| true` at the end prevents failures if fields are empty)
- Ensure `EVENT_PATH` environment variable is set correctly

## Related Documentation

- [GitHub Actions Composite Actions](https://docs.github.com/en/actions/creating-actions/creating-a-composite-action)
- [GitHub Actions Workflow Syntax](https://docs.github.com/en/actions/using-workflows/workflow-syntax-for-github-actions)
- [GitHub Events Documentation](https://docs.github.com/en/actions/using-workflows/events-that-trigger-workflows#issues)
- [GitHub Contexts and Expression Syntax](https://docs.github.com/en/actions/learn-github-actions/contexts)
