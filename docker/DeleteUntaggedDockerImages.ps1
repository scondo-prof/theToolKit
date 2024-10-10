# Get all Docker images with the tag as <none>
$UntaggedImages = docker images --filter "dangling=true" --format "{{.ID}} {{.Repository}}:{{.Tag}}" | Where-Object { $_ -match ":<none>" }

# Iterate over each untagged image and delete it
foreach ($Image in $UntaggedImages) {
    $ImageDetails = $Image -split " "
    $ImageID = $ImageDetails[0]

    Write-Host "Deleting untagged image with ID $ImageID"
    docker rmi $ImageID -f
}
