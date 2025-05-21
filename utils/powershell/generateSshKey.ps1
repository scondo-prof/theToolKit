# Prompt for key file name and passphrase
$keyName = Read-Host "Enter the name for your SSH key (no extension)"
$keyPath = "$env:USERPROFILE\.ssh\$keyName"
$email = Read-Host "Enter the email comment (e.g., jenkins@yourdomain.com)"
$passphrase = Read-Host "Enter a passphrase to protect your private key" -AsSecureString

# Convert secure string to plain text
$passBSTR = [System.Runtime.InteropServices.Marshal]::SecureStringToBSTR($passphrase)
$passPlainText = [System.Runtime.InteropServices.Marshal]::PtrToStringBSTR($passBSTR)

# Ensure .ssh directory exists
$sshDir = "$env:USERPROFILE\.ssh"
if (-not (Test-Path $sshDir)) {
    New-Item -ItemType Directory -Path $sshDir | Out-Null
}

# Use Start-Process with argument list (to avoid quoting problems)
Start-Process -FilePath "ssh-keygen" `
    -ArgumentList "-t", "ed25519", "-C", "$email", "-f", "$keyPath", "-N", "$passPlainText" `
    -NoNewWindow -Wait

# Clear sensitive data
[System.Runtime.InteropServices.Marshal]::ZeroFreeBSTR($passBSTR)

# Output results
Write-Host "`nSSH key pair created:"
Write-Host "Private key: $keyPath"
Write-Host "Public key : ${keyPath}.pub"
