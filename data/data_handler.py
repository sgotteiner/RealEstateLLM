import pandas as pd
import datetime


class DataHandler:
    def __init__(self, file_path):
        self.file_path = file_path
        self.df = None

    def load_data(self):
        self.df = pd.read_parquet(self.file_path)
        # Ensure 'year' column is string or int for filtering
        self.df['year'] = self.df['year'].astype(str)

    def print_head_and_info(self, n=5):
        if self.df is not None:
            pd.set_option('display.max_columns', None)
            print(f"\nFirst {n} rows of the dataset:")
            print(self.df.head(n))
            print("\nDataFrame Info:")
            self.df.info()
        else:
            print("Data not loaded. Please call load_data() first.")

    def get_property_details(self, property_name: str):
        if self.df is None:
            raise RuntimeError("Data not loaded")

        prop_df = self.df[self.df['property_name'].str.lower() == property_name.lower()]

        if prop_df.empty:
            return None

        # Gather some info
        entity_names = prop_df['entity_name'].dropna().unique()
        tenant_names = prop_df['tenant_name'].dropna().unique()
        last_year = prop_df['year'].max()
        total_profit = prop_df['profit'].sum()

        details = {
            'property_name': property_name,
            'entity_names': entity_names.tolist(),
            'tenant_names': tenant_names.tolist(),
            'last_year': last_year,
            'total_profit': total_profit
        }
        return details

    def compare_property_profits(self, prop1: str, prop2: str):
        if self.df is None:
            raise RuntimeError("Data not loaded")

        prof1 = self.df[self.df['property_name'].str.lower() == prop1.lower()]['profit'].sum()
        prof2 = self.df[self.df['property_name'].str.lower() == prop2.lower()]['profit'].sum()

        if prof1 == 0 and prof2 == 0:
            return f"Neither {prop1} nor {prop2} have profit data."

        return f"Total profit for {prop1} is ${prof1:,.2f}, and for {prop2} is ${prof2:,.2f}."

    def calculate_total_pnl(self, year: str = None):
        if self.df is None:
            return "Data not loaded."

        # Normalize year
        if year is None or str(year).lower() in ["this year", "current year", "year"]:
            year = str(datetime.datetime.now().year)
        elif str(year).lower() in ["last year", "previous year"]:
            year = str(datetime.datetime.now().year - 1)
        else:
            year = str(year)

        # Check if year exists in data
        if year not in self.df['year'].astype(str).unique():
            return f"No data for year {year}."

        filtered = self.df[self.df['year'].astype(str) == year]
        total = filtered['profit'].sum()

        return total

    def list_all_properties(self):
        if self.df is None:
            raise RuntimeError("Data not loaded")
        return sorted(self.df['property_name'].dropna().unique().tolist())
