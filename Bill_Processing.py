import csv
from collections import defaultdict
import os

# input CSV file
file_path = "/Users/jasmined/Desktop/HL7-Project/Archive/Original/sampledata.csv"

# Initialize a defaultdict to store the total bill amount for each state
total_bill_per_state = defaultdict(float)

# Initialize a variable to store the overall total bill amount
overall_total_bill = 0.0

# Open the CSV file and create a DictReader object
with open(file_path, mode='r') as file:
    csv_reader = csv.DictReader(file)
    
    # Process each row in the CSV data
    for row in csv_reader:
        # Get the state and bill amount from the row
        state = row['patient_state'].strip()  # strip() is used to remove leading and trailing whitespaces
        bill_amount = float(row['bill_amount'])
        
        # Handle missing state 
        if not state:
            state = "Unknown"
        
        # Add the bill amount to the total for the state
        total_bill_per_state[state] += bill_amount
        
        # Add the bill amount to the overall total bill amount
        overall_total_bill += bill_amount

# Specify the report file path
report_file_path = "/Users/jasmined/Desktop/HL7-Project/Archive/Modified/Sampledata_Bill_Amount.txt"

# Create the directory if it does not exist
os.makedirs(os.path.dirname(report_file_path), exist_ok=True)

# Create and write to the report file
with open(report_file_path, 'w') as report_file:
    # Write the total bill amount for each state to the report file
    for state, total_bill in total_bill_per_state.items():
        report_file.write(f'{state}: {total_bill}\n')
    
    # Write the overall total bill amount to the report file
    report_file.write(f'Total Bill Amount: {overall_total_bill}\n')

print(f'Report file has been created successfully at {report_file_path}.')
