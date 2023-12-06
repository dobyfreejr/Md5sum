#!/bin/bash

# Define the source directory you want to monitor
SOURCE_DIR="/path/to/source_directory"

# Define the backup directory
BACKUP_DIR="/path/to/backup_directory"

# Check if the script is running as root; if not, rerun with sudo
if [ "$(id -u)" -ne 0 ]; 
    sudo "$0" "$@"
    exit $?
fi

# Create the backup directory if it doesn't exist
mkdir -p "$BACKUP_DIR"

# Filename to store the last MD5 checksums
LAST_CHECKSUMS_FILE="$BACKUP_DIR/last_checksums.txt"

# Function to calculate MD5 checksums
calculate_md5() {
    md5sum "$1" | awk '{print $1}'
}

# Check if the last checksums file exists, and if not, create it
if [ ! -e "$LAST_CHECKSUMS_FILE" ]; then
    sudo find "$SOURCE_DIR" -type f -exec md5sum {} \; > "$LAST_CHECKSUMS_FILE"
fi

# Calculate the current checksums
sudo find "$SOURCE_DIR" -type f -exec md5sum {} \; > "$BACKUP_DIR/current_checksums.txt"

# Compare the current checksums with the last ones
diff -u "$LAST_CHECKSUMS_FILE" "$BACKUP_DIR/current_checksums.txt" > "$BACKUP_DIR/changes.txt"

# Move the current checksums to the last checksums file
mv "$BACKUP_DIR/current_checksums.txt" "$LAST_CHECKSUMS_FILE"

# Copy the changed files to the backup directory
awk '/^\+/{print $2}' "$BACKUP_DIR/changes.txt" | xargs -I {} cp --parents {} "$BACKUP_DIR"

# Clean up temporary files
rm "$BACKUP_DIR/changes.txt"

# Optionally, you can log the changes to a log file
echo "Backup script run on $(date)" >> "$BACKUP_DIR/backup_log.txt"
echo "Changes:" >> "$BACKUP_DIR/backup_log.txt"
cat "$BACKUP_DIR/changes.txt" >> "$BACKUP_DIR/backup_log.txt"

