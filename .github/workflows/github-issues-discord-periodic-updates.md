# GitHub Issues Discord Periodic Updates Workflow

## Overview

This reusable GitHub Actions workflow periodically fetches all issues from a repository and sends them to Discord. This workflow is designed to be called on a schedule (e.g., daily, weekly) to provide periodic updates about all issues in a repository.

## What It Does

When called from another repository, this reusable workflow runs and performs the following:

### Main Functionality

- Fetches all issues from the repository
- Sends formatted issue information to Discord via webhook
- Provides periodic updates about repository issues

## Prerequisites

- A Discord webhook URL configured as a repository secret named `DISCORD_WEBHOOK_URL`
- The workflow must be called from a repository that has GitHub Actions enabled
- Appropriate permissions to read repository issues

## Usage

This workflow uses `workflow_call` and should be triggered on a schedule by the calling repository. Example:

```yaml
name: Daily Issues Update

on:
  schedule:
    # Run daily at 9 AM UTC
    - cron: "0 9 * * *"

jobs:
  periodic_update:
    uses: scondo-prof/theToolKit/.github/workflows/github-issues-discord-periodic-updates.yml@main
```

## Related Documentation

- [GitHub Actions Reusable Workflows](https://docs.github.com/en/actions/using-workflows/reusing-workflows)
- [Scheduled Events](https://docs.github.com/en/actions/using-workflows/events-that-trigger-workflows#schedule)
- [Discord Webhook Action](https://github.com/marketplace/actions/discord-webhook-action)
