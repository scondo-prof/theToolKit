#!/bin/bash

# Base directory to start the search
base_dir=$(pwd)
has_state=()
no_state=()

# Find all .tfvars files recursively
mapfile -t tfvars_files < <(find "$base_dir" -type f -name "*.tfvars")
total=${#tfvars_files[@]}
index=1

# Loop through each .tfvars file
for tfvars_file in "${tfvars_files[@]}"; do
    dir=$(dirname "$tfvars_file")

    echo "[$index / $total] Checking: $tfvars_file"

    # Enter the directory
    pushd "$dir" >/dev/null

    # Attempt to run `terraform show` and check for state
    output=$(terraform show -json 2>/dev/null)
    if [[ $? -eq 0 && "$output" == *'"values"'* ]]; then
        has_state+=("$tfvars_file")
    else
        no_state+=("$tfvars_file")
    fi

    # Return to previous directory
    popd >/dev/null
    ((index++))
done

# Print results
echo -e "\n===================="
echo ".tfvars WITH state:"
echo "===================="
for file in "${has_state[@]}"; do
    echo "$file"
done

echo -e "\n======================"
echo ".tfvars WITHOUT state:"
echo "======================"
for file in "${no_state[@]}"; do
    echo "$file"
done
