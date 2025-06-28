import pandas as pd

# Define the path to your data file
# Replace 'real_estate_data.parquet' with the actual name of your file.
file_path = 'cortex.parquet'

try:
    # Read the Parquet file into a pandas DataFrame
    df = pd.read_parquet(file_path)

    print("File loaded successfully into a DataFrame!")

    # --- Verification Steps ---

    # Set the option to display all columns
    pd.set_option('display.max_columns', None)

    # 1. Print the first 5 rows to see what the data looks like
    print("\nFirst 5 rows of the dataset:")
    print(df.head())

    # 2. Print a concise summary of the DataFrame
    # This shows column names, non-null counts, and data types (Dtype).
    print("\nDataFrame Info:")
    df.info()

except FileNotFoundError:
    print(f"Error: The file '{file_path}' was not found. Please check the file path.")
except Exception as e:
    print(f"An error occurred while reading the file: {e}")