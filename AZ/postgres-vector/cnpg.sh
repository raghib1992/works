#!/bin/bash


KUSTOMIZATION_FILE="kustomization.yaml"
NEW_RESOURCE="new-2-file.yaml"

if [[ -f $KUSTOMIZATION_FILE ]]; then
    echo "File is available"
else
    echo "File not exist"
    echo -e "apiVersion: v1\nkind: Kustomization\nresources: " > "$KUSTOMIZATION_FILE"
fi
sed -i "/^resources:/a\  - $NEW_RESOURCE" $KUSTOMIZATION_FILE
