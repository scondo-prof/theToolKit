# GitHub Issues Discord Integration Workflow

## Overview

This reusable GitHub Actions workflow monitors GitHub issue events and sends formatted notifications to Discord. When triggered, it logs detailed issue information to the workflow logs and sends a formatted message to a Discord webhook.

## What It Does

When called from another repository, this reusable workflow runs on `ubuntu-latest` and performs two main steps:

### Step 1: Log Issue Information

Echoes key issue details to the workflow logs:

- **Trigger Action**: The event name and action that triggered the workflow (e.g., "issues opened", "issues closed")
- **Issue Title**: The title of the issue
- **Issue Number**: The issue number
- **Issue State**: Current state (open/closed)
- **Issue URL**: Direct link to the issue
- **Repository**: The repository where the issue exists
- **Trigger Reason**: Explanation of what triggered the workflow, including event name and action

### Step 2: Send to Discord

Sends a formatted message to Discord using a webhook. The Discord message includes:

- Issue title as a main header
- Trigger action
- Repository name
- Issue number
- Issue state
- Issue URL

The Discord message is formatted with markdown for better readability in Discord channels.

## Prerequisites

- A Discord webhook URL configured as a repository secret named `DISCORD_WEBHOOK_URL`
- The workflow must be called from a repository that has GitHub Actions enabled

## Supported Event Types

This workflow can be triggered by any issue-related events defined by the calling repository. Common trigger events include:

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

## Example Output

### Workflow Logs:

```
Trigger Action: issues opened
Issue Title:    Example Issue Title
Issue Number:   123
Issue State:    open
Issue URL:      https://github.com/owner/repo/issues/123
Repository:     owner/repo

Trigger Reason: The workflow was triggered by an | issues | event with action | opened |
```

### Discord Message:

```
---
# Issue Title: Example Issue Title

## Issue Details:

- **Trigger Action:** opened
- **Repository:** owner/repo
- **Issue Number:** #123
- **Issue State:** open
- **Issue URL:** https://github.com/owner/repo/issues/123
```

## Related Documentation

- [GitHub Actions Reusable Workflows](https://docs.github.com/en/actions/using-workflows/reusing-workflows)
- [GitHub Events Documentation](https://docs.github.com/en/actions/using-workflows/events-that-trigger-workflows#issues)
- [Discord Webhook Action](https://github.com/marketplace/actions/discord-webhook-action)
