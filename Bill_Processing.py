import pandas as pd

# Load the CSV file into a DataFrame
file_path = "/Users/jasmined/Desktop/HL7-Project/Archive/Original/sampledata.csv"
df = pd.read_csv(file_path)

# Replace NaN, empty strings, or whitespaces in 'patient_state' with 'Unknown'
df.loc[df['patient_state'].str.strip() == '', 'patient_state'] = 'Unknown'


# Group by the 'patient_state' column and calculate the sum of 'bill_amount' for each group
total_bill_per_state = df.groupby('patient_state')['bill_amount'].sum()

# Calculate the overall total bill amount
overall_total_bill = total_bill_per_state.sum()

# Specify the report file path
report_file_path = "/Users/jasmined/Desktop/HL7-Project/Archive/Modified/sample_data_report.txt"

# Open the report file in write mode and write the results
with open(report_file_path, 'w') as report_file:
    # Write the total bill amount for each state
    for state, total_bill in total_bill_per_state.items():
        report_file.write(f'{state}: {total_bill}\n')
    
    # Write the overall total bill amount
    report_file.write(f'Total Bill Amount: {overall_total_bill}\n')

print(f'Report file has been created successfully at {report_file_path}.')
