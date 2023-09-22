# HL7-Project

# 1. The objective of this project is to match information from an HL7 ADT text file to a CSV file and, upon finding a match, add additional columns to the text file using data from the CSV.


# Execute the DELETE command to remove duplicate rows
cursor.execute('DELETE FROM adt_records WHERE rowid NOT IN (SELECT MIN(rowid) FROM adt_records GROUP BY patient_id);')