# GitHub Issues Discord Integration Workflow

## Overview

This reusable GitHub Actions workflow provides two modes of operation for monitoring GitHub issues and sending notifications to Discord:

1. **Real-time Issue Events**: Monitors GitHub issue events and sends formatted notifications to Discord as they happen
2. **Periodic Updates**: Periodically fetches all issues from a repository and processes them (can be extended to send periodic summaries to Discord)

Both modes are controlled through workflow inputs, allowing you to selectively enable the functionality you need when calling this reusable workflow.

## What It Does

When called from another repository, this reusable workflow runs on `ubuntu-latest` and can perform one or both of the following jobs based on input parameters:

### Job 1: Log Issue Details (Real-time Events)

This job is triggered when `trigger-log-issue-details` input is set to `true`. It performs two main steps:

#### Step 1: Log Issue Information

Echoes key issue details to the workflow logs:

- **Trigger Action**: The event name and action that triggered the workflow (e.g., "issues opened", "issues closed")
- **Issue Title**: The title of the issue
- **Issue Number**: The issue number
- **Issue State**: Current state (open/closed)
- **Issue URL**: Direct link to the issue
- **Repository**: The repository where the issue exists
- **User**: The GitHub username of the issue creator
- **Trigger Reason**: Explanation of what triggered the workflow, including event name and action

#### Step 2: Send to Discord

Sends a formatted message to Discord using a webhook. The Discord message includes:

- Issue title as a main header
- User who created the issue
- Trigger action
- Repository name
- Issue number
- Issue state
- Issue URL

The Discord message is formatted with markdown for better readability in Discord channels.

### Job 2: Periodic Issues Updates

This job is triggered when `trigger-periodic-issues-updates` input is set to `true`. It performs the following:

#### Step 1: Checkout Repository

Checks out the repository to access the Python formatting script:

- Uses `actions/checkout@v4` to check out the repository code
- This step is necessary because reusable workflows need explicit checkout to access files from the repository

#### Step 2: Set Up Python

Configures the Python environment:

- Uses `actions/setup-python@v5` to set up Python 3.11
- Ensures the correct Python version is available for running the formatting script

#### Step 3: Get All Issues

Fetches all issues from the repository using the GitHub API:

- Uses `curl` to make a GET request to the GitHub API
- Authenticates using `secrets.GITHUB_TOKEN`
- Retrieves all issues for the repository
- Saves the response as JSON to `issues.json`

#### Step 4: Create Discord Notification

Formats the issues data into a Discord-friendly message:

- Runs a Python script (`.github/workflows/workflow_assets/periodic_issues_notification_format.py`)
- Reads the `issues.json` file and formats each issue with:
  - Issue number and title
  - Issue state (open/closed)
  - Creator information with avatar image
  - Creation and update timestamps
  - Link to the issue on GitHub
- Creates a formatted markdown message with date header
- Sets the formatted message as a workflow output for the next step

#### Step 5: Send to Discord

Sends the formatted message to Discord:

- Uses the `tsickert/discord-webhook@v7.0.0` action
- Sends the formatted message created in the previous step
- Message is formatted with markdown for better readability in Discord channels

## Prerequisites

- A Discord webhook URL configured as a repository secret named `DISCORD_WEBHOOK_URL` (required for both real-time issue events and periodic updates)
- The workflow must be called from a repository that has GitHub Actions enabled
- The Python formatting script (`.github/workflows/workflow_assets/periodic_issues_notification_format.py`) must exist in the repository where the workflow is called
- `GITHUB_TOKEN` must have appropriate permissions to read repository issues
  - By default, `GITHUB_TOKEN` has read-only permissions
  - For this workflow, read-only permissions are sufficient for both jobs

## Workflow Inputs

The workflow accepts the following optional inputs:

| Input                             | Type    | Required | Default | Description                                                                        |
| --------------------------------- | ------- | -------- | ------- | ---------------------------------------------------------------------------------- |
| `trigger-log-issue-details`       | boolean | false    | `false` | Set to `true` to enable real-time issue event monitoring and Discord notifications |
| `trigger-periodic-issues-updates` | boolean | false    | `false` | Set to `true` to enable periodic fetching and processing of all issues             |

## Supported Event Types

For the **Log Issue Details** job, this workflow can be triggered by any issue-related events defined by the calling repository. Common trigger events include:

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

## Usage

### Real-time Issue Events

To use the workflow for real-time issue notifications, call it from a workflow that triggers on issue events:

```yaml
name: Issue Notifications

on:
  issues:
    types: [opened, closed, reopened, edited]
  issue_comment:
    types: [created, edited, deleted]

jobs:
  notify_discord:
    uses: scondo-prof/theToolKit/.github/workflows/github-issues-discord-integration.yml@main
    with:
      trigger-log-issue-details: true
    secrets:
      DISCORD_WEBHOOK_URL: ${{ secrets.DISCORD_WEBHOOK_URL }}
```

### Periodic Updates

To use the workflow for periodic issue updates, call it from a scheduled workflow:

```yaml
name: Daily Issues Update

on:
  schedule:
    # Run daily at 9 AM UTC
    - cron: "0 9 * * *"

jobs:
  periodic_update:
    uses: scondo-prof/theToolKit/.github/workflows/github-issues-discord-integration.yml@main
    with:
      trigger-periodic-issues-updates: true
```

### Using Both Modes

You can also use both modes simultaneously by setting both inputs to `true`:

```yaml
name: Complete Issue Integration

on:
  issues:
    types: [opened, closed, reopened, edited]
  schedule:
    - cron: "0 9 * * *"

jobs:
  real_time_updates:
    if: github.event_name == 'issues' || github.event_name == 'issue_comment'
    uses: scondo-prof/theToolKit/.github/workflows/github-issues-discord-integration.yml@main
    with:
      trigger-log-issue-details: true
    secrets:
      DISCORD_WEBHOOK_URL: ${{ secrets.DISCORD_WEBHOOK_URL }}

  periodic_update:
    if: github.event_name == 'schedule'
    uses: scondo-prof/theToolKit/.github/workflows/github-issues-discord-integration.yml@main
    with:
      trigger-periodic-issues-updates: true
```

## Example Output

### Real-time Issue Events

#### Workflow Logs:

```
Trigger Action: issues opened
Issue Title:    Example Issue Title
Issue Number:   123
Issue State:    open
Issue URL:      https://github.com/owner/repo/issues/123
Repository:     owner/repo

Trigger Reason: The workflow was triggered by an | issues | event with action | opened |
```

#### Discord Message:

```
---
# Issue Title: Example Issue Title

## Issue Details:

- **User:** username
- **Trigger Action:** issues opened
- **Repository:** owner/repo
- **Issue Number:** 123
- **Issue State:** open
- **Issue URL:** https://github.com/owner/repo/issues/123
```

### Periodic Updates

#### Discord Message Example:

```
---
# Issues as of 2024-01-15
---------------------------------------------------


## Issue Title: 1 - Example Issue

Issue State: open

Created By: username

![Avatar](https://avatars.githubusercontent.com/u/123?v=4)

Issue Created At: 2024-01-15T10:30:00Z
Issue Last Update: 2024-01-15T12:00:00Z

[Issue Link](https://github.com/owner/repo/issues/1)
```

## Technical Details

### Real-time Issue Events

- **Discord Integration**: Uses `tsickert/discord-webhook@v7.0.0` action for sending messages
- **Format**: Messages are formatted with markdown for Discord compatibility
- **Conditional Execution**: Job only runs when `trigger-log-issue-details` input is `true`

### Periodic Updates

- **Checkout**: Uses `actions/checkout@v4` to check out the repository (required to access Python script)
- **Python Setup**: Uses `actions/setup-python@v5` to configure Python 3.11 environment
- **API Endpoint**: `GET /repos/{owner}/{repo}/issues`
- **Authentication**: Uses `secrets.GITHUB_TOKEN` (automatically provided by GitHub Actions)
- **Output**: Saves all issues as JSON to `issues.json` file
- **Processing**: Uses Python script (`.github/workflows/workflow_assets/periodic_issues_notification_format.py`) to format issues into Discord markdown
- **Discord Integration**: Uses `tsickert/discord-webhook@v7.0.0` action for sending formatted messages
- **Runner**: Uses `ubuntu-latest` runner
- **Conditional Execution**: Job only runs when `trigger-periodic-issues-updates` input is `true`

The workflow requires read permissions on the repository, which is the default for `GITHUB_TOKEN`.

## Related Documentation

- [GitHub Actions Reusable Workflows](https://docs.github.com/en/actions/using-workflows/reusing-workflows)
- [GitHub Events Documentation](https://docs.github.com/en/actions/using-workflows/events-that-trigger-workflows#issues)
- [Scheduled Events](https://docs.github.com/en/actions/using-workflows/events-that-trigger-workflows#schedule)
- [Discord Webhook Action](https://github.com/marketplace/actions/discord-webhook-action)
