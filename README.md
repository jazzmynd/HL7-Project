# HL7-Project



# Execute the DELETE command to remove duplicate rows
cursor.execute('DELETE FROM adt_records WHERE rowid NOT IN (SELECT MIN(rowid) FROM adt_records GROUP BY patient_id);')