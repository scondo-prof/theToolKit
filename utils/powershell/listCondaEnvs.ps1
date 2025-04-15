# ListCondaEnvs.ps1
# Lists all conda environments

# Ensure conda is available in the session
$condaCmd = "conda"
if (-not (Get-Command $condaCmd -ErrorAction SilentlyContinue)) {
    Write-Host "Conda not found in PATH. Trying to initialize Conda..."

    $condaInit = "$env:USERPROFILE\miniconda3\shell\condabin\conda-hook.ps1"
    if (Test-Path $condaInit) {
        . $condaInit
        conda activate base
    } else {
        Write-Error "Unable to locate Conda. Please ensure Conda is installed and added to PATH."
        exit 1
    }
}

# List environments
Write-Host "`nConda Environments:"
conda env list | ForEach-Object {
    if ($_ -match "^\s*(\*?)\s*(\S+)\s+(.*)$") {
        $active = if ($matches[1]) { "(Active)" } else { "" }
        Write-Host "$($matches[2]) - $($matches[3]) $active"
    }
}