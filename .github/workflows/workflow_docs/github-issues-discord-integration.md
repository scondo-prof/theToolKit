# GitHub Issues Discord Integration Workflow

## Overview

This reusable GitHub Actions workflow provides two independent jobs for monitoring GitHub issues and sending notifications to Discord:

1. **Real-time Issue Events**: Monitors GitHub issue events and sends formatted notifications to Discord as they happen
2. **Periodic Updates**: Fetches all issues from a repository and processes them into Discord notifications

**Important**: Each job runs **only when its corresponding input is set to `true` AND its conditional check passes**. Jobs are independent and will not run simultaneously unless explicitly configured to do so in the calling workflow with appropriate conditional logic.

## What It Does

When called from another repository, this reusable workflow runs on `ubuntu-latest` and contains two independent jobs that execute **only when their conditions are met**:

### Job 1: Log Issue Details (Real-time Events)

**Conditional Execution**: This job **only runs** when `trigger-log-issue-details` input is set to `true` AND the job's `if` condition evaluates to true. It performs two main steps:

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

**Conditional Execution**: This job **only runs** when `trigger-periodic-issues-updates` input is set to `true` AND the job's `if` condition evaluates to true. It performs the following:

#### Step 1: Checkout Repository

Checks out the repository to access the Python formatting script:

- Uses `actions/checkout@v4` to check out the repository code
- This step is necessary because reusable workflows need explicit checkout to access files from the repository

#### Step 2: Set Up Python

Configures the Python environment:

- Uses `actions/setup-python@v5` to set up Python 3.11
- Ensures the correct Python version is available for running the formatting script

#### Step 3: Format and Send Discord Notification

Formats the issues data and sends Discord messages directly using the `periodic_issues_notification.py` script:

**The Script's Role:**

The `periodic_issues_notification.py` script (located in `.github/workflows/workflow_assets/`) is a critical component of the periodic updates job. It performs the following operations:

1. **Fetches Issues Data**: Uses the GitHub API to fetch all issues directly from the repository with automatic pagination support (handles repositories with any number of issues)
2. **Filters and Formats Open Issues**: For each issue in the JSON array:
   - **Filters closed issues**: Only open issues are included in the detailed Discord message (closed issues are counted separately)
   - **Formats open issues** with:
     - Issue number and title (as a header)
     - Issue state (open) with markdown formatting
     - Creator username
     - Creation timestamp (`created_at`)
     - Last update timestamp (`updated_at`)
3. **Batch Sending**: Sends messages to Discord in batches of 3 issues per message to avoid Discord message length limits
4. **Counts Issues**: Tracks the total number of both open and closed issues separately
5. **Creates a Date Header**: Adds a formatted date header showing when the notification was generated
6. **Sends Summary Message**: After all issue batches are sent, sends a final summary message with:
   - Total open issues count (as a clickable link to filtered open issues)
   - Total closed issues count (as a clickable link to filtered closed issues)

**How It Integrates with the Workflow:**

- The script is executed directly and fetches all issues via the GitHub API internally
- It processes the issue data and transforms it into human-readable Discord messages
- Messages are sent directly to Discord via the `httpx` library using the `DISCORD_WEBHOOK_URL` environment variable
- No separate workflow step is needed for fetching issues or sending to Discord - the script handles everything internally

**Technical Details:**

- The script uses the GitHub API with automatic pagination (fetches up to 100 issues per page and continues until all are retrieved)
- Uses `httpx` library for both GitHub API requests and Discord webhook requests
- It formats timestamps using Python's `datetime` module
- Sends messages directly to Discord using `httpx` library with POST requests
- Messages are sent in batches of 3 issues to prevent Discord message length limits
- The script ensures proper encoding (UTF-8) for international characters in issue titles and descriptions
- Requires both `GITHUB_TOKEN` and `DISCORD_WEBHOOK_URL` environment variables to be set

## Prerequisites

- A Discord webhook URL configured as a repository secret named `DISCORD_WEBHOOK_URL` (required for jobs that send Discord notifications)
- The workflow must be called from a repository that has GitHub Actions enabled
- **For Periodic Updates**: The Python formatting script (`.github/workflows/workflow_assets/periodic_issues_notification.py`) must exist in the repository where the workflow is defined (the repository containing the reusable workflow, not the calling repository)
  - The workflow checks out the repository containing the workflow definition to access this script
  - The script is part of the `workflow_assets/` directory, which contains supporting files for workflows
- `GITHUB_TOKEN` must have appropriate permissions to read repository issues
  - By default, `GITHUB_TOKEN` has read-only permissions
  - For this workflow, read-only permissions are sufficient for all jobs

## Workflow Inputs

The workflow accepts the following optional inputs. **Important**: Each job only runs when its corresponding input is set to `true` AND the job's `if` condition in the workflow evaluates to true:

| Input                             | Type    | Required | Default | Description                                                                                                                                                |
| --------------------------------- | ------- | -------- | ------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `trigger-log-issue-details`       | boolean | false    | `false` | Set to `true` to enable real-time issue event monitoring and Discord notifications. Job only runs when this is `true` AND the job's `if` condition passes. |
| `trigger-periodic-issues-updates` | boolean | false    | `false` | Set to `true` to enable periodic fetching and processing of all issues. Job only runs when this is `true` AND the job's `if` condition passes.             |

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

To use the workflow for periodic issue updates, set up `workflow_dispatch` in your workflow and trigger it externally (e.g., via AWS Lambda with EventBridge cron, or any scheduled job service):

```yaml
name: Daily Issues Update

on:
  workflow_dispatch:

jobs:
  periodic_update:
    uses: scondo-prof/theToolKit/.github/workflows/github-issues-discord-integration.yml@main
    with:
      trigger-periodic-issues-updates: true
```

**Note**: Instead of using GitHub Actions' `schedule` clause (which has limitations and inefficiencies), this workflow is designed to be triggered remotely via `workflow_dispatch`. You can use external schedulers like:

- **AWS Lambda with EventBridge cron**: Create a Lambda function triggered by an EventBridge cron rule that calls the GitHub API to trigger `workflow_dispatch`
- **Any scheduled job service**: Any service capable of making HTTP requests can trigger the workflow via GitHub's workflow dispatch API

This approach provides better reliability, more flexible scheduling, and avoids the limitations of GitHub Actions' schedule triggers.

### Complete Example: Real-time Events + Manual Trigger

This example demonstrates a production-ready setup that combines real-time issue notifications with manual periodic updates via `workflow_dispatch`:

```yaml
name: GitHub Issues to Discord Integration

on:
  issues:
    types:
      - opened
      - closed
      - reopened
      - deleted

  issue_comment:
    types:
      - created

  workflow_dispatch:

jobs:
  trigger-periodic-issues-updates:
    if: github.event_name == 'workflow_dispatch'
    uses: scondo-prof/theToolKit/.github/workflows/github-issues-discord-integration.yml@main
    secrets: inherit
    with:
      trigger-periodic-issues-updates: true

  trigger-log-issue-details:
    if: github.event_name == 'issues' || github.event_name == 'issue_comment'
    uses: scondo-prof/theToolKit/.github/workflows/github-issues-discord-integration.yml@main
    secrets: inherit
    with:
      trigger-log-issue-details: true
```

**Key Features of This Example:**

- **Conditional Job Execution**: Each job **only runs when its conditions are met**:
  - `trigger-periodic-issues-updates` job runs **only** when `github.event_name == 'workflow_dispatch'` (manual trigger)
  - `trigger-log-issue-details` job runs **only** when `github.event_name == 'issues' || github.event_name == 'issue_comment'`
  - Jobs are independent and will not run unless their specific conditions are true
- **Multiple Trigger Types**: Responds to issue events, issue comments, and manual workflow dispatch
- **Secrets Inheritance**: Uses `secrets: inherit` to automatically pass all repository secrets to the reusable workflow (cleaner than explicitly listing each secret)
- **Main Branch Reference**: Uses `@main` to reference the main branch of the workflow repository
- **Selective Issue Events**: Monitors specific issue event types (`opened`, `closed`, `reopened`, `deleted`) and issue comment creation to reduce noise
- **Issue Comment Monitoring**: Also tracks when comments are created on issues for comprehensive issue activity tracking

This pattern allows you to:

- Get real-time notifications when issues are created, closed, reopened, or deleted
- Get real-time notifications when comments are added to issues
- Manually trigger periodic updates on-demand using workflow dispatch

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

**Note:** The script filters out closed issues from the detailed display and only shows open issues. Messages are sent in batches of 3 issues per message. A final summary message includes clickable links to both open and closed issue counts.

```
---
# Issues as of 2024-01-15
---------------------------------------------------


## Issue Title: 1 - Example Issue

__Issue State__: `open`
__Created By__: `username`
__Issue Created At__: `2024-01-15T10:30:00Z`
__Issue Last Update__: `2024-01-15T12:00:00Z`


[__Total Open Issues__](https://github.com/owner/repo/issues?q=is%3Aissue%20state%3Aopen): `3`
[__Total Closed Issues__](https://github.com/owner/repo/issues?q=is%3Aissue%20state%3Aclosed): `5`
---------------------------------------------------
```

## Technical Details

### Real-time Issue Events

- **Discord Integration**: Uses `tsickert/discord-webhook@v7.0.0` action for sending messages
- **Format**: Messages are formatted with markdown for Discord compatibility
- **Conditional Execution**: **Job only runs when** `trigger-log-issue-details` input is set to `true` **AND** the job's `if` condition evaluates to true. If either condition is false, the job will be skipped.

### Periodic Updates

- **Checkout**: Uses `actions/checkout@v4` to check out the repository containing the workflow definition (required to access the Python script from `workflow_assets/`)
- **Python Setup**: Uses `actions/setup-python@v5` to configure Python 3.11 environment
- **API Endpoint**: `GET /repos/{owner}/{repo}/issues?state=all` (includes both open and closed issues)
- **Authentication**: Uses `secrets.GITHUB_TOKEN` (automatically provided by GitHub Actions)
- **Processing**: Uses Python script (`.github/workflows/workflow_assets/periodic_issues_notification.py`) to fetch, format issues, and send Discord messages
  - The script fetches all issues directly from the GitHub API with automatic pagination support (handles repositories with any number of issues)
  - Filters out closed issues from the detailed display and sends messages directly to Discord
  - Messages are sent in batches of 3 issues per message to avoid Discord message length limits
  - The formatted messages include a date header, detailed information for open issues (numbers, titles, states, creators, timestamps), and a final summary message with total counts of both open and closed issues as clickable links
- **Discord Integration**: The Python script sends messages directly to Discord using `httpx` library via the `DISCORD_WEBHOOK_URL` environment variable
- **Runner**: Uses `ubuntu-latest` runner
- **Conditional Execution**: **Job only runs when** `trigger-periodic-issues-updates` input is set to `true` **AND** the job's `if` condition evaluates to true. If either condition is false, the job will be skipped.

### Workflow Assets

This workflow uses assets from the `workflow_assets/` directory:

- **periodic_issues_notification.py**: A Python script that fetches GitHub issues via API, formats them into Discord-compatible markdown messages, and sends them directly to Discord. The script:
  - Fetches all issues directly from the GitHub API with automatic pagination (handles any number of issues by fetching up to 100 per page and continuing until all are retrieved)
  - Filters closed issues from the detailed display (only open issues are shown with full details)
  - Counts both open and closed issues separately
  - Formats each open issue with structured markdown (headers, metadata)
  - Generates a timestamped header for the notification
  - Sends messages in batches of 3 issues per message to avoid Discord message length limits
  - Sends a final summary message with total open and closed issue counts as clickable links
  - Sends messages directly to Discord using `httpx` library via `DISCORD_WEBHOOK_URL` environment variable
  - Handles UTF-8 encoding to support international characters

The workflow checks out the repository where it's defined (not the calling repository) to access this script, ensuring the asset is available during workflow execution.

The workflow requires read permissions on the repository, which is the default for `GITHUB_TOKEN`.

## Related Documentation

- [GitHub Actions Reusable Workflows](https://docs.github.com/en/actions/using-workflows/reusing-workflows)
- [GitHub Events Documentation](https://docs.github.com/en/actions/using-workflows/events-that-trigger-workflows#issues)
- [Scheduled Events](https://docs.github.com/en/actions/using-workflows/events-that-trigger-workflows#schedule)
- [Discord Webhook Action](https://github.com/marketplace/actions/discord-webhook-action)
