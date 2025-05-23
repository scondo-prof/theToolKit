#!/bin/bash

# Base directory to start the search
base_dir=$(pwd)
with_state=()
no_state=()

# Find all directories that contain .tfvars files
mapfile -t tfvars_dirs < <(find "$base_dir" -type f -name "*.tfvars" -exec dirname {} \; | sort -u)
total=${#tfvars_dirs[@]}
index=1

# Loop through each directory
for dir in "${tfvars_dirs[@]}"; do
    echo "[$index / $total] Checking directory: $dir"

    pushd "$dir" >/dev/null

    # Initialize Terraform if needed
    if [ ! -d ".terraform" ]; then
        echo "Initializing Terraform..."
        terraform init -input=false >/dev/null 2>&1
    fi

    # Get list of workspaces
    mapfile -t workspaces < <(terraform workspace list 2>/dev/null | sed 's/^[* ]*//')

    if [ ${#workspaces[@]} -eq 0 ]; then
        echo "  No workspaces found. Skipping."
        popd >/dev/null
        ((index++))
        continue
    fi

    # Loop through each workspace
    for ws in "${workspaces[@]}"; do
        echo "  Workspace: $ws"
        terraform workspace select "$ws" >/dev/null 2>&1

        # Attempt to show state
        output=$(terraform show -json 2>/dev/null)
        if [[ $? -eq 0 && "$output" == *'"values"'* ]]; then
            with_state+=("$dir | workspace: $ws")
        else
            no_state+=("$dir | workspace: $ws")
        fi
    done

    popd >/dev/null
    ((index++))

done

# Print results
echo -e "\n===================="
echo ".tfvars directories WITH state:"
echo "===================="
for entry in "${with_state[@]}"; do
    echo "$entry"
done

echo -e "\n======================"
echo ".tfvars directories WITHOUT state:"
echo "======================"
for entry in "${no_state[@]}"; do
    echo "$entry"
done
