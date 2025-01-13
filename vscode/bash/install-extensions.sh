#!/bin/bash

# Read extensions from extensions.txt and install each
while read extension; do
    code --install-extension "$extension"
done < extensions.txt
