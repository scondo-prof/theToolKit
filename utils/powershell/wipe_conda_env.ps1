# Wipe all installed pip packages in the current Python (conda) environment

Write-Host "Detecting Python executable..."
$python = Get-Command python -ErrorAction SilentlyContinue

if (-not $python) {
    Write-Host "[ERROR] Python is not available in the current session. Please activate your conda environment first."
    exit 1
}

Write-Host "[INFO] Collecting installed pip packages..."
$packages = & python -m pip freeze

if (-not $packages) {
    Write-Host "[INFO] No packages to uninstall. Your environment is already clean."
    exit 0
}

Write-Host "[INFO] Uninstalling all pip packages..."
$packageNames = $packages -split "`n" | ForEach-Object { $_.Split('==')[0] } | Where-Object { $_ -ne '' }

foreach ($pkg in $packageNames) {
    Write-Host "[ACTION] Uninstalling $pkg..."
    & python -m pip uninstall -y $pkg
}

Write-Host "[DONE] All pip packages have been uninstalled."
