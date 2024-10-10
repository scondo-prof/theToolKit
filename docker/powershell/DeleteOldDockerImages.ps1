# Get the current date and time
$CurrentDate = Get-Date

# Get all Docker images
$DockerImages = docker images --format "{{.ID}} {{.Repository}}:{{.Tag}} {{.CreatedSince}}"

# Iterate over each image and check the creation date
foreach ($Image in $DockerImages) {
    $ImageDetails = $Image -split " "
    $ImageID = $ImageDetails[0]
    $ImageTag = $ImageDetails[1]
    $ImageCreated = $ImageDetails[2] + " " + $ImageDetails[3]

    # Parse the creation date to determine if it's older than 2 days
    if ($ImageCreated -match "(\d+) (weeks|months|years|days)") {
        $TimeValue = [int]$matches[1]
        $TimeUnit = $matches[2]

        # Delete images older than 2 days
        if (($TimeUnit -eq "days" -and $TimeValue -ge 2) -or $TimeUnit -eq "weeks" -or $TimeUnit -eq "months" -or $TimeUnit -eq "years") {
            Write-Host "Deleting image $ImageTag ($ImageID), created $ImageCreated"
            docker rmi $ImageID -f
        }
    }
}