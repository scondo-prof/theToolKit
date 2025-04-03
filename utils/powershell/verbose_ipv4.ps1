try {
    $ipv4 = Invoke-RestMethod -Uri 'https://api.ipify.org'
    Write-Host "Your public IPv4 address is: $ipv4"
}
catch {
    Write-Host "Failed to retrieve public IPv4 address: $_"
}
