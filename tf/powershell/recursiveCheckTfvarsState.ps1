# Check-TfvarsWithWorkspaces.ps1

$baseDir = Get-Location
$withState = @()
$noState = @()

# Find all unique directories that contain .tfvars files
$tfvarsDirs = Get-ChildItem -Path $baseDir -Recurse -Filter *.tfvars |
ForEach-Object { $_.Directory.FullName } |
Sort-Object -Unique

$total = $tfvarsDirs.Count
$index = 1

foreach ($dir in $tfvarsDirs) {
    Write-Host "[$index / $total] Checking directory: $dir"
    Push-Location $dir

    # Initialize Terraform if .terraform is missing
    if (-not (Test-Path ".terraform")) {
        Write-Host "  Initializing Terraform..."
        terraform init -input=false | Out-Null
    }

    # Get list of workspaces
    $workspaces = terraform workspace list 2>$null |
    ForEach-Object { $_.Trim().TrimStart('*').Trim() } |
    Where-Object { $_ -ne "" }

    if ($workspaces.Count -eq 0) {
        Write-Host "  No workspaces found. Skipping."
        Pop-Location
        $index++
        continue
    }

    foreach ($ws in $workspaces) {
        Write-Host "  Workspace: $ws"
        terraform workspace select $ws | Out-Null

        $output = terraform show -json 2>$null

        if ($LASTEXITCODE -eq 0 -and $output -match '"values"') {
            $withState += "$dir | workspace: $ws"
        }
        else {
            $noState += "$dir | workspace: $ws"
        }
    }

    Pop-Location
    $index++
}

# Print results
Write-Host "`n===================="
Write-Host ".tfvars directories WITH state:"
Write-Host "===================="
$withState | ForEach-Object { Write-Host $_ }

Write-Host "`n======================"
Write-Host ".tfvars directories WITHOUT state:"
Write-Host "======================"
$noState | ForEach-Object { Write-Host $_ }