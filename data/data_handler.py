import pandas as pd

class DataHandler:
    def __init__(self, file_path):
        self.file_path = file_path
        self.df = None

    def load_data(self):
        try:
            self.df = pd.read_parquet(self.file_path)
            print("File loaded successfully into a DataFrame!")
        except FileNotFoundError:
            print(f"Error: The file '{self.file_path}' was not found. Please check the file path.")
        except Exception as e:
            print(f"An error occurred while reading the file: {e}")

    def print_head_and_info(self, n=5):
        if self.df is not None:
            pd.set_option('display.max_columns', None)
            print(f"\nFirst {n} rows of the dataset:")
            print(self.df.head(n))
            print("\nDataFrame Info:")
            self.df.info()
        else:
            print("Data not loaded. Please call load_data() first.")