#!/bin/bash
# Configuration: Set the base path according to your system setup
BASE_PATH="/home/docker-server/volumes/immich"
echo "Script started: Checking files to move..."
# Define the source file and the destination directory
SOURCE_FILE="/home/docker-server/utils/untracked.txt"
DESTINATION_DIR="/home/docker-server/volumes/immich/untracked/"
# Ensure the destination directory exists
if [ ! -d "$DESTINATION_DIR" ]; then
    mkdir -p "$DESTINATION_DIR"
    echo "Created directory: $DESTINATION_DIR"
fi
# Read each line from the source file, adjust the path, and move the file to the destination directory
while IFS= read -r file_path; do
    echo "File to remove: $file_path"
    # Adjust the base path of each file
    # usr/src/app/upload --> /home/docker-server/volumes/immich
    corrected_path=$(echo "$file_path" | sed "s|/usr/src/app/upload|${BASE_PATH}|")
    echo "Checking file: $corrected_path"
    if [ -f "$corrected_path" ]; then
        echo "File found, moving..."
        mv "$corrected_path" "$DESTINATION_DIR"
        if [ $? -eq 0 ]; then
            echo "Moved successfully."
        else
            echo "Failed to move $corrected_path"
        fi
    else
        echo "File does not exist: $corrected_path"
    fi
done < "$SOURCE_FILE"
echo "Script completed."
