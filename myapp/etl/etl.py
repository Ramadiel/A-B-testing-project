"""
ETL Module

This module is responsible for extracting data from CSV files and loading it into a database. It leverages `pandas` for data manipulation, 
`sqlalchemy` for database interactions, and `loguru` for logging activities.

Functions:
    - load_csv_to_table(table_name, csv_path): Load a CSV file into a specified database table.
    - main(): Main execution process for batch loading multiple CSV files.

Dependencies:
    - pandas: Used for handling CSV file data.
    - sqlalchemy: Used for database connection and table interaction.
    - loguru: Used for logging information and errors.
"""


# Import necessary modules
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database import engine, Base
from loguru import logger
import pandas as pd
import glob
from os import path

# Define a function to load CSV data into a database table
def load_csv_to_table(table_name: str, csv_path: str) -> None:
    """
    Load data from a CSV file into a database table.

    Args:
        table_name (str): The name of the database table where data will be inserted.
        csv_path (str): Path to the CSV file containing the data.

    Returns:
        None

    Exceptions:
        :raises ValueError: If the CSV file cannot be read or the data cannot be loaded into the database.
        :raises SQLAlchemyError: If a database connection or query fails.
    
    Usage:
        >>> load_csv_to_table("users", "data/users.csv")
        INFO: Loaded data for table users from data/users.csv
    """
    # Read the CSV file into a DataFrame
    df = pd.read_csv(csv_path)
    # Load DataFrame into the specified database table
    df.to_sql(table_name, con=engine, if_exists="append", index=False)
    logger.info(f"Loaded data for table {table_name} from {csv_path}")

# Specify the path to the folder containing CSV files
folder_path = "data/*.csv"

# Use glob to get a list of CSV file paths in the specified folder
files = glob.glob(folder_path)

# Extract table names from CSV file names and load each file into its respective table
for file_path in files:
    """
    For each CSV file in the specified folder, extract the base name (used as the table name)
    and attempt to load the data into the corresponding database table.
    """    
    table_name = path.splitext(path.basename(file_path))[0]
    try:
        # Load the CSV data into the table
        load_csv_to_table(table_name, file_path)
    except Exception as e:
        logger.error(f"Failed to ingest table {table_name}. Error: {e}")

logger.info("All tables have been populated.")

