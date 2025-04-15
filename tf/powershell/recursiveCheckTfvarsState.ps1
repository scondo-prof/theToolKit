# Check-TfvarsState.ps1

$baseDir = Get-Location
$hasState = @()
$noState = @()

# Get all .tfvars files
$tfvarsFiles = Get-ChildItem -Path $baseDir -Recurse -Filter *.tfvars
$total = $tfvarsFiles.Count
$index = 1

# Loop through each .tfvars file
foreach ($file in $tfvarsFiles) {
    $tfvarsFile = $file.FullName
    $dir = Split-Path $tfvarsFile

    Write-Host "[$index / $total] Checking: $tfvarsFile"

    Push-Location $dir

    try {
        $output = terraform show -json 2>$null
        if ($LASTEXITCODE -eq 0 -and $output -match '"values"') {
            $hasState += $tfvarsFile
        }
        else {
            $noState += $tfvarsFile
        }
    }
    catch {
        $noState += $tfvarsFile
    }

    Pop-Location
    $index++
}

# Print results
Write-Host "`n===================="
Write-Host ".tfvars WITH state:"
Write-Host "===================="
$hasState | ForEach-Object { Write-Host $_ }

Write-Host "`n======================"
Write-Host ".tfvars WITHOUT state:"
Write-Host "======================"
$noState | ForEach-Object { Write-Host $_ }