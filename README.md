# 🌟 HL7 Project

Welcome to the HL7 Project, developed by @jazzmynd! 

## 📌 Table of Contents

- [Project Overview](#-project-overview)
- [Prerequisites](#-prerequisites)
- [Installation and Setup](#-installation-and-setup)
- [Running the Project](#-running-the-project)
- [Expected Output](#-expected-output)
- [Bonus Objective: Database Support](#-bonus-objective-database-support)
- [Contributing and Issues](#-contributing-and-issues)

## 📘 Project Overview

This Python-based project involves transferring the HL7 ADT and HL7 ORU to the csv file. The primary tasks involve manipulating data, generating modified file copies, and mapping the ADT and ORU file in to csv file followed the spec given in sample.csv. A bonus feature of the project is integrating csv file into SQLite Database.

## 🛠 Prerequisites

- **Python:** Recommended Version 3.8 or higher.
- **Git:** Required for cloning the repository.

## 🚀 Installation and Setup

1. **Clone the Repository:**
   Open your terminal and run the following command:
   ```bash
   git clone https://github.com/jazzmynd/HL7-Project
   cd HL7-Project

## 🔧 Running the Project

To run the project, follow the steps below to execute each Python script in sequence:

1. **Execute File Copy Script:**
   ```sh
   python file_copy_script.py

2. **Process ADT Data:**
   ```sh
   python ADT_processing.py

3.  **Process ORU Data::**
   ```sh
   python ORU_processing.py
   ```

## 📁 Expected Output

After successfully running the project, you should observe the following outputs:

1. **Modified CSV Files:**
   - Located in the `Archive/Modified` directory.
   - Named `ADT_(TodaysDate)_Modified_file.csv` and `ORU_(TodaysDate)_Modified_file.csv`.

2. **Text Report Files:**
   - `ADT_Bill_Report.txt` and `ORU_Bill_Report.txt` in the project directory.
   - Outlining the total bill amount for each state.

3. **SQLite Database File:**
   - `adt_data.db` file, writing the `ADT_(TodaysDate)_Modified_file.csv` file into an SQLite Database.


## 🌟 Run Database

1. ** Navigate to the Database Folder **
   ```sh
cd /path/to/your/database/folder

2. ** Open SQLite Shell**
   ```sh
sqlite3 adt_data.db

3. ** List Tables **
   ```sh
.tables
You should see "adt_records" if it has been created successfully.

## Queries for Database
1. ** Query the Table **
   ```sh
   SELECT * FROM adt_records;

2. ** Count Rows in Table **
   ```sh
   SELECT COUNT(*) FROM adt_records;

3. ** Query Specific Columns **
   ```sh
   SELECT patient_id, patient_first_name, patient_last_name FROM adt_records;

4. ** Ordering Result **
   ```sh
   SELECT * FROM adt_records ORDER BY date_of_service DESC;

5. ** Limiting Results **
   ```sh
   SELECT * FROM adt_records LIMIT 10;

6. ** Update Results **
   ```sh
   UPDATE adt_records SET patient_email_address = 'new_email@example.com' WHERE patient_id = 'some_patient_id';

7. ** Delete Duplicatee Rows **
   ```sh
   DELETE FROM adt_records WHERE rowid NOT IN (SELECT MIN(rowid) FROM adt_records GROUP BY patient_id);


