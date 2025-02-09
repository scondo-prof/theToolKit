# Get list of remotes
$upstream = git remote -v | Select-String "upstream.*\(fetch\)" | ForEach-Object { ($_ -split "\s+")[0] } | Select-Object -First 1

# Check if an upstream remote exists
if (-not $upstream) {
    Write-Host "No upstream remote found!" -ForegroundColor Red
    Write-Host "Please set an upstream using: `n git remote add upstream <repo-url>" -ForegroundColor Yellow
    exit 1
}

Write-Host "Using upstream: $upstream" -ForegroundColor Cyan

# Fetch the latest changes from upstream
Write-Host "`nFetching changes from '$upstream'..."
git fetch $upstream

# Merge upstream changes into the current branch, allowing unrelated histories
$currentBranch = git branch --show-current
Write-Host "Merging changes from '$upstream/$currentBranch' into '$currentBranch'..."
git merge --allow-unrelated-histories $upstream/$currentBranch

# Push changes to the origin repository
Write-Host "Pushing changes to 'origin/$currentBranch'..."
git push origin $currentBranch

Write-Host "`n✅ Sync completed successfully!" -ForegroundColor Green
