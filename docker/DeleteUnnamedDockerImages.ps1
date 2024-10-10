# Get all Docker images with the repository as <none>
$UnnamedImages = docker images --filter "dangling=true" --format "{{.ID}} {{.Repository}}:{{.Tag}}" | Where-Object { $_ -match "^<none>" }

# Iterate over each unnamed image and delete it
foreach ($Image in $UnnamedImages) {
    $ImageDetails = $Image -split " "
    $ImageID = $ImageDetails[0]

    Write-Host "Deleting unnamed image with ID $ImageID"
    docker rmi $ImageID -f
}
