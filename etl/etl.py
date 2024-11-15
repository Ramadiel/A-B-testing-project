# Import necessary modules
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database import engine, Base
from loguru import logger
import pandas as pd
import glob
from os import path

# Define a function to load CSV data into a database table
def load_csv_to_table(table_name, csv_path):
    """
    Load data from a CSV file into a database table.

    Args:
    - table_name: Name of the database table.
    - csv_path: Path to the CSV file containing data.

    Returns:
    - None
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
    # Extract the base name of the file without the extension to use as the table name
    table_name = path.splitext(path.basename(file_path))[0]
    try:
        # Load the CSV data into the table
        load_csv_to_table(table_name, file_path)
    except Exception as e:
        logger.error(f"Failed to ingest table {table_name}. Error: {e}")

logger.info("All tables have been populated.")

