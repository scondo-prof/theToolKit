#example usecase:
#.\openssl_encrypt_pem_to_p8.ps1 -PemFilePath "path/to/pem" -OutputP8FilePath "path/to/p8" -Passphrase "wowTest!"

param (
    [string]$PemFilePath,         # Path to input .pem file
    [string]$OutputP8FilePath,    # Path to output .p8 file
    [string]$Passphrase           # Passphrase for encryption
)

# Check if OpenSSL is installed
$opensslPath = Get-Command openssl -ErrorAction SilentlyContinue
if (-not $opensslPath) {
    Write-Host "Error: OpenSSL is not installed or not in PATH. Please install OpenSSL." -ForegroundColor Red
    exit 1
}

# Validate input file
if (-not (Test-Path $PemFilePath)) {
    Write-Host "Error: Input PEM file '$PemFilePath' not found." -ForegroundColor Red
    exit 1
}

# Construct OpenSSL command
$opensslCommand = "openssl pkcs8 -topk8 -inform PEM -outform PEM -in `"$PemFilePath`" -out `"$OutputP8FilePath`" -passout pass:`"$Passphrase`" -v2 aes-256-cbc"

# Execute OpenSSL command
Write-Host "Executing OpenSSL command..."
Invoke-Expression $opensslCommand

# Check if the output file was created successfully
if (Test-Path $OutputP8FilePath) {
    Write-Host "Success: Encrypted P8 key generated at '$OutputP8FilePath'" -ForegroundColor Green
} else {
    Write-Host "Error: Failed to create encrypted .p8 file." -ForegroundColor Red
}
