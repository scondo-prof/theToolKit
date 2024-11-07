# Prompt the user for necessary information
$negName = Read-Host -Prompt "Enter the name for your NEG"
$regionName = Read-Host -Prompt "Enter the name for your GCP Region"
$cloudRunServiceName = Read-Host -Prompt "Enter the name for your Cloud Run Service"

# Run the gcloud command with the user-provided values
gcloud compute network-endpoint-groups create $negName `
  --region=$regionName `
  --network-endpoint-type=serverless `
  --cloud-run-service=$cloudRunServiceName
