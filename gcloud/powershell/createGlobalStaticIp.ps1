# Prompt the user for the static IP name
$staticIpName = Read-Host -Prompt "Enter the name for your static IP"

# Run the gcloud command with the user-provided IP name
gcloud compute addresses create $staticIpName --global