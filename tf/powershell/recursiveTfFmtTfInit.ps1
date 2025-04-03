# PowerShell script to recursively run terraform fmt and terraform init in subdirectories
$baseDir = Get-Location

# Find all subdirectories containing Terraform configuration files
$terraformDirs = Get-ChildItem -Path $baseDir -Recurse -Directory | Where-Object { Test-Path "$($_.FullName)\*.tf" }

foreach ($dir in $terraformDirs) {
    $relativePath = $dir.FullName.Replace($baseDir, '.')
    Write-Host "Processing directory: ${relativePath}"

    # Run terraform fmt
    Write-Host "Running 'terraform fmt' in ${relativePath}..."
    Push-Location $dir.FullName
    $fmtOutput = terraform fmt -recursive 2>&1
    if ($?) {
        Write-Host "✅ terraform fmt succeeded in ${relativePath}"
    }
    else {
        Write-Host "❌ terraform fmt failed in ${relativePath}: $fmtOutput"
    }
    
    # Run terraform init
    Write-Host "Running 'terraform init' in ${relativePath}..."
    $initOutput = terraform init -no-color 2>&1
    if ($?) {
        Write-Host "✅ terraform init succeeded in ${relativePath}"
    }
    else {
        Write-Host "⚠️ terraform init failed in ${relativePath}: $initOutput"
        
        # Check if the error suggests a provider version issue
        if ($initOutput -match "does not match configured version constraint|must use terraform init -upgrade") {
            Write-Host "🔄 Retrying with 'terraform init -upgrade' in ${relativePath}..."
            $upgradeOutput = terraform init -upgrade -no-color 2>&1
            if ($?) {
                Write-Host "✅ terraform init -upgrade succeeded in ${relativePath}"
            }
            else {
                Write-Host "❌ terraform init -upgrade failed in ${relativePath}: $upgradeOutput"
            }
        }
    }
    Pop-Location
}

Write-Host "Terraform formatting and initialization complete."