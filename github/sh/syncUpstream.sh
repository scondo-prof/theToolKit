#!/bin/bash

# Get list of remotes and extract 'upstream'
upstream=$(git remote -v | grep "upstream.*(fetch)" | awk '{print $1}' | head -n 1)

# Check if an upstream remote exist
if [ -z "$upstream" ]; then
    printf "\033[31mNo upstream remote found!\033[0m\n"
    printf "\033[33mPlease set an upstream using:\n git remote add upstream <repo-url>\033[0m\n"
    exit 1
fi

printf "\033[36mUsing upstream: %s\033[0m\n" "$upstream"

# Fetch the latest changes from upstream
printf "\nFetching changes from '%s'...\n" "$upstream"
git fetch "$upstream"

# Get the current branch name
currentBranch=$(git branch --show-current)

# Merge upstream changes into the current branch, allowing unrelated histories
printf "Merging changes from '%s/%s' into '%s'...\n" "$upstream" "$currentBranch" "$currentBranch"
git merge --allow-unrelated-histories "$upstream/$currentBranch"

# Push changes to the origin repository
printf "Pushing changes to 'origin/%s'...\n" "$currentBranch"
git push origin "$currentBranch"

printf "\n✅ Sync completed successfully!\n"
