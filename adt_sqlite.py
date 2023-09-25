import pandas as pd
import sqlite3

# Specify the file path
file_path = '/Users/jasmined/Desktop/HL7-Project/Archive/Modified/ADT_2023-09-25_Modified_file.csv'

# Read the CSV data
df = pd.read_csv(file_path)

# Alternatively, use loc to replace both empty/whitespace-only strings and NaN values in one line
df.loc[df['patient_state'].isna() | (df['patient_state'].str.strip() == ''), 'patient_state'] = 'Unknown'

# Connect to SQLite database (if the database does not exist, it will be created)
conn = sqlite3.connect('adt_data.db')

# Write the data to a sqlite table named 'patient_data'
df.to_sql('adt_records', conn, if_exists='replace', index=False)

# Close the connection
conn.close()
