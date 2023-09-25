import csv
from datetime import date
import os
from collections import defaultdict
from output_files_creation import create_output_files, modified_dir, oru_modified_file
import pandas as pd
import numpy as np

# -------Add Sample CSV's Lines with ORU type------------

# Path to sample CSV file.
sample_csv_path = '/Users/jasmined/Desktop/HL7-Project/Archive/Original/sampledata.csv'  

# Read the sample CSV file using pandas.
df = pd.read_csv(sample_csv_path)

# Filter rows where the 'message_type' column starts with 'ORU'.
oru_df = df[df['message_type'].str.startswith('ORU')]

# Add the 'date_of_service' column with today's date.
today_date = date.today().strftime("%Y-%m-%d") # Get today's date in the format YYYY-MM-DD
oru_df['date_of_service'] = today_date

# Check if 'patient_first_name' and 'patient_last_name' columns exist in the DataFrame
if 'patient_first_name' in oru_df.columns and 'patient_last_name' in oru_df.columns:
    # Fill NaN values with an empty string for 'patient_middle_name' column
    oru_df['patient_middle_name'] = oru_df.get('patient_middle_name', '').fillna('')
    
    # Create the 'patient_name' column by concatenating the name fields.
    oru_df['patient_name'] = oru_df[['patient_last_name', 'patient_first_name', 'patient_middle_name']].apply(lambda x: ' '.join(x), axis=1)
else:
    print("First name and/or last name columns are not present in the DataFrame.")

# Reinitialize the "#" column with sequential numbers starting from 1.
oru_df["#"] = range(1, len(oru_df) + 1)

# Define the path to the output CSV file 
output_csv_path = create_output_files('ORU')

# Write the filtered DataFrame to the output CSV file.
oru_df.to_csv(output_csv_path, index=False)

print(f"ORU data with added columns has been written to {output_csv_path}")

# ---------------------

# ------Mapping----------

# Path to the ORU file
oru_file_path = "/Users/jasmined/Desktop/HL7-Project/Archive/Original/Sample ORU.txt"

# Read the ORU data from the file
with open(oru_file_path, 'r') as file:
    oru_data = file.read()

# Split the ORU data into segments
segments = oru_data.strip().split('\n')


# Define the CSV column headers
csv_columns = [
    "#", "patient_id", "site_id", "service_location", "message_type", "message_time", "message_id",
    "account_number", "discharge_disposition", "financial_class", "patient_first_name",
    "patient_last_name", "patient_middle_name", "patient_address_1", "patient_address_2",
    "patient_city", "patient_state", "patient_zip", "patient_zip4", "patient_date_of_birth",
    "patient_deceased_date", "patient_sex", "patient_ssn", "referring_doctor_id",
    "attending_doctor_id", "patient_ethnicity", "patient_race", "patient_language",
    "patient_smoking_status", "patient_email_address", "patient_cell_phone_area_code",
    "patient_cell_phone_number", "patient_marital_status", "bill_amount",
    "patient_drivers_license_number", "guarantor_first_name", "guarantor_last_name",
    "guarantor_middle_name", "guarantor_address_1", "guarantor_address_2", "guarantor_city",
    "guarantor_state", "guarantor_zip", "date_of_service", "patient_name"
]

# Initialize a dictionary to store the extracted data with blank values
csv_data = {column: "" for column in csv_columns}

# Extract common information from MSH segment
msh_segment = segments[0].split('|')

# Initialize a variable for patient ID
patient_id = ""

# Initialize a count for the records
record_count = oru_df["#"].iloc[-1]

# Bill amount = 1234
csv_data["bill_amount"] = 1234

# New column date_of_service, add today's date
today_date = date.today().strftime("%Y-%m-%d") # Get today's date in the format YYYY-MM-DD
csv_data["date_of_service"] = today_date

# Iterate through segments to extract data
for segment in segments:

##### MSH Segment
    if segment.startswith("MSH"):
        fields = segment.split('|')

        # message type
        message_type_field = fields[8].split('^')
        csv_data["message_type"] = message_type_field[0] +'-'+ message_type_field[1]

        # message time in HHMMSS format
        csv_data["message_time"] = fields[6]
        message_time = csv_data["message_time"]
        # Initialize hours, minutes, and seconds
        hours = ""
        minutes = ""
        seconds = ""
        if len(message_time) == 14:
            # Extract hours, minutes, and seconds
            hours = message_time[8:10]
            minutes = message_time[10:12]
            seconds = message_time[12:14]
        elif len(message_time) == 12:
            hours = message_time[8:10]
            minutes = message_time[10:12]
            seconds = "00"
        else:
            print("Invalid timestamp format")
        # Handle the case where the timestamp format is invalid
        # Create the HHMMSS format
        hhmmss_format = f"{hours}:{minutes}:{seconds}"
        # Assign the converted value back to the "message_time" field
        csv_data["message_time"] = hhmmss_format

        # message id
        csv_data["message_id"] = fields[9]

        csv_data["site_id"] = fields[3]

##### PID Segment
    if segment.startswith("PID"):
        fields = segment.split('|')
        csv_data["patient_id"] = fields[2]

        # patient name
        name_fields = fields[5].split('^')
        csv_data["patient_first_name"] = name_fields[1]
        csv_data["patient_last_name"] = name_fields[0]
        csv_data["patient_middle_name"] = name_fields[2]
        csv_data['patient_name'] = name_fields[0] +' '+ name_fields[1] +' '+ name_fields[2]

        # patient address
        address_fields = fields[11].split('^')
        csv_data["patient_address_1"] = address_fields[0]
        csv_data["patient_address_2"] = address_fields[1]
        csv_data["patient_city"] = address_fields[2]
        
        # Check if there are enough components in the PID segment for state and zip
        if len(address_fields) >= 4:
            csv_data["patient_state"] = address_fields[3]
            csv_data["patient_zip"] = address_fields[4]

        # patient dob
        csv_data["patient_date_of_birth"] = fields[7]
        dob = csv_data["patient_date_of_birth"]
        if len(dob) != 14:
            csv_data["patient_date_of_birth"] = "00:00:00"
        else:
            # Extract hours, minutes, and seconds
            hours = dob[8:10]
            minutes = dob[10:12]
            seconds = dob[12:14]
            # Create the HHMMSS format
            hhmmss_format = f"{hours}:{minutes}:{seconds}"
            # Assign the converted value back to the "patient_date_of_birth" field
            csv_data["patient_date_of_birth"] = hhmmss_format

        # sex
        csv_data["patient_sex"] = fields[8]

        # race
        csv_data["patient_race"] = fields[10]

        # ssn
        ssn_fields = fields[19].split('^')

        # patient ssn
        csv_data["patient_ssn"] = ssn_fields[0]

        # patient email
        email_fields = fields[13].split('^')
        csv_data["patient_email_address"] = email_fields[9] if len(email_fields) > 4 else ""

        # patient phone
        phone_fields = fields[13].split('^')
        translation_table = str.maketrans('', '', '()\-')
        cleaned_phone_number = phone_fields[0].translate(translation_table)
        csv_data["patient_cell_phone_area_code"] = cleaned_phone_number[:3]
        csv_data["patient_cell_phone_number"] = cleaned_phone_number[3:]

        # Increment the record count for each PID segment
        record_count += 1

        # account number
        csv_data['account_number'] = fields[18]

        # language
        csv_data['patient_language'] = fields[15]

        # marriage status
        csv_data['patient_marital_status'] = fields[16]

        # Driver's License Number
        csv_data["patient_drivers_license_number"] = fields[20]


#### PV1 Segment
    if segment.startswith("PV1"):
        fields = segment.split('|')
        csv_data["service_location"] = fields[3]

csv_data["#"] = record_count
    
# -----------------------

# --------Output---------
# Print the extracted data for verification
for column, value in csv_data.items():
    print(f"{column}: {value}")

# Create or open the output CSV file for writing
output_csv_file_path = os.path.join(modified_dir, oru_modified_file)
# Write the extracted data to the output CSV file
with open(output_csv_path, 'a', newline='') as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=csv_columns)
    # Check if the file is empty and write the header only if it is
    if csvfile.tell() == 0:
        writer.writeheader()
    writer.writerow(csv_data)

print(f"Data has been successfully extracted and saved to {output_csv_path}")

import pandas as pd

# --- Bill Amount ----
# Read the generated CSV file
df = pd.read_csv(output_csv_path)

# Replace both NaN values and whitespace-only strings in 'patient_state' with 'Unknown'
df['patient_state'].replace('', 'Unknown', inplace=True)
df['patient_state'].replace(np.nan, 'Unknown', inplace=True)

# Alternatively, use loc to replace both empty/whitespace-only strings and NaN values in one line
df.loc[df['patient_state'].isna() | (df['patient_state'].str.strip() == ''), 'patient_state'] = 'Unknown'


# Group by 'patient_state' and sum 'bill_amount'
bill_amount_by_state = df.groupby('patient_state')['bill_amount'].sum()

# Calculate total bill amount
total_bill_amount = bill_amount_by_state.sum()

# Write the aggregated bill amounts to a txt file
report_file_path = "/Users/jasmined/Desktop/HL7-Project/Archive/Modified/ORU_Bill_Report.txt"

with open(report_file_path, 'w') as report_file:
    report_file.write("State\tTotal Bill Amount\n")
    for state, amount in bill_amount_by_state.items():
        report_file.write(f"{state}\t{amount}\n")
    report_file.write(f"\nTotal\t{total_bill_amount}")

print(f"Report has been successfully generated at {report_file_path}")
