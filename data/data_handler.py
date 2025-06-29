import pandas as pd

class DataHandler:
    def __init__(self, path="resources/cortex.parquet"):
        self.path = path
        self.df = pd.read_parquet(self.path)

    def calculate_total_pnl(self, year=None):
        import datetime
        if self.df is None:
            return "Data not loaded."

        if year is None or str(year).lower() in ["this year", "year", "current year"]:
            year = str(datetime.datetime.now().year)
        elif str(year).lower() in ["last year", "previous year"]:
            year = str(datetime.datetime.now().year - 1)
        else:
            year = str(year)

        if year not in self.df['year'].astype(str).unique():
            return f"No data for year {year}."

        total = self.df[self.df['year'].astype(str) == year]['profit'].sum()
        return f"Total P&L for {year}: ${total:,.2f}"

    def get_property_details(self, property_name):
        if self.df is None:
            return "Data not loaded."
        results = self.df[self.df['property_name'].str.lower() == property_name.lower()]
        if results.empty:
            return f"No data for property '{property_name}'."
        return results.head().to_string(index=False)

    def compare_property_profits(self, p1, p2):
        if self.df is None:
            return "Data not loaded."

        df = self.df
        p1_total = df[df['property_name'] == p1]['profit'].sum()
        p2_total = df[df['property_name'] == p2]['profit'].sum()

        return (f"{p1}: ${p1_total:,.2f}\n"
                f"{p2}: ${p2_total:,.2f}\n"
                f"{'-'*25}\n"
                f"Difference: ${p1_total - p2_total:,.2f}")