import os
import datetime

# Full path to my directory
directory_path = "/Users/jasmined/Desktop/HL7-Project"

# Create the "Archive/Modified" directory if it doesn't exist
modified_dir = os.path.join(directory_path, "Archive/Modified")

# Get today's date in the format YYYY-MM-DD
today_date = datetime.datetime.now().strftime("%Y-%m-%d")

# Create file names with today's date
adt_modified_file = f"ADT_{today_date}_Modified_file.csv"
oru_modified_file = f"ORU_{today_date}_Modified_file.csv"

def create_output_files(file_type):
    os.makedirs(modified_dir, exist_ok=True)

    if file_type == 'ADT':
        open(os.path.join(modified_dir, adt_modified_file), "w").close()
    elif file_type == 'ORU':
        open(os.path.join(modified_dir, oru_modified_file), "w").close()
    else:
        print(f"Unknown file type: {file_type}. No output file was created.")

if __name__ == "__main__":
    create_output_files()
