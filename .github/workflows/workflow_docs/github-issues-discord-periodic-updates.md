# GitHub Issues Discord Periodic Updates Workflow

## Overview

This reusable GitHub Actions workflow periodically fetches all issues from a repository and sends them to Discord. This workflow is designed to be called on a schedule (e.g., daily, weekly) to provide periodic updates about all issues in a repository.

## What It Does

When called from another repository, this reusable workflow runs on `ubuntu-latest` and performs the following:

### Step 1: Get All Issues

Fetches all issues from the repository using the GitHub API:

- Uses `curl` to make a GET request to the GitHub API
- Authenticates using `secrets.GITHUB_TOKEN`
- Retrieves all issues for the repository
- Saves the response as JSON to `ISSUES_JSON.json`

### Step 2: Read and Process Issues

- Reads the `ISSUES_JSON.json` file
- Displays the issue data in workflow logs
- Can be extended to send formatted information to Discord

## Prerequisites

- The workflow must be called from a repository that has GitHub Actions enabled
- `GITHUB_TOKEN` must have appropriate permissions to read repository issues
  - By default, `GITHUB_TOKEN` has read-only permissions
  - For this workflow, read-only permissions are sufficient
  - If you need write permissions, you must modify the workflow permissions in repository settings

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

## Technical Details

The workflow uses the GitHub REST API to fetch issues:

- **API Endpoint**: `GET /repos/{owner}/{repo}/issues`
- **Authentication**: Uses `secrets.GITHUB_TOKEN` (automatically provided by GitHub Actions)
- **Output**: Saves all issues as JSON to `ISSUES_JSON.json` file
- **Runner**: Uses `ubuntu-latest` runner

The workflow requires read permissions on the repository, which is the default for `GITHUB_TOKEN`.

## Related Documentation

- [GitHub Actions Reusable Workflows](https://docs.github.com/en/actions/using-workflows/reusing-workflows)
- [Scheduled Events](https://docs.github.com/en/actions/using-workflows/events-that-trigger-workflows#schedule)
- [Discord Webhook Action](https://github.com/marketplace/actions/discord-webhook-action)
