# Get a list of all local branches except the main branch
$branches = git branch --format="%(refname:short)" | Where-Object { $_ -ne "main" }

# Iterate through each branch and delete it
foreach ($branch in $branches) {
    Write-Host "Deleting branch: $branch"
    git branch -D $branch
}

Write-Host "Pruning complete. Only the main branch remains."
