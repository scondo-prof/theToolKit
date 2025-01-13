# Prompt the user for the static IP name and region
$staticIpName = Read-Host -Prompt "Enter the name for your static IP"
$regionName = Read-Host -Prompt "Enter the region for your IP address"

# Run the gcloud command with the user-provided IP name and region
gcloud compute addresses create $staticIpName --region=$regionName
