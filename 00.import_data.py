#!/usr/bin/env python3
import sys
import pandas as pd
from sqlalchemy import create_engine

# Load the Excel file
file_path = sys.argv[1]
sheets = pd.read_excel(file_path, sheet_name=None)
print(sheets)

# Create a file-based SQLite engine
engine = create_engine('sqlite:///data.db')  # Saves the database as data.db

# Write each sheet to a table in SQLite
for sheet_name, df in sheets.items():
    df.to_sql(sheet_name, con=engine, index=False, if_exists='replace')
    print(f"Loaded sheet '{sheet_name}' into SQLite.")
