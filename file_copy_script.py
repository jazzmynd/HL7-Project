import os
import shutil

# Source directory
source_directory = "/Users/jasmined/Desktop/Interview"

# Destination directory
destination_directory = "/Users/jasmined/Desktop/HL7-Project"

# Create the "Archive/Original" directory within the destination if it doesn't exist
original_dir = os.path.join(destination_directory, "Archive/Original")
os.makedirs(original_dir, exist_ok=True)

# List of file names to copy
files_to_copy = ["ADT_sample.txt", "Sample ORU.txt", "sampledata.csv"]

# Copy the files from the source to the "Archive/Original" directory in the destination
for file_name in files_to_copy:
    source_path = os.path.join(source_directory, file_name)
    destination_path = os.path.join(original_dir, file_name)
    shutil.copy(source_path, destination_path)
