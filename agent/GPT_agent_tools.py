from langchain_core.tools import StructuredTool
from data import DataHandler

class GPTAgentTools:
    def __init__(self, data_handler: DataHandler):
        self.data_handler = data_handler

    def get_tools(self):
        return [
            StructuredTool.from_function(
                func=self.calculate_total_pnl,
                name="calculate_total_pnl",
                description="Calculate the total profit and loss for a given year. Input: year (e.g., '2024')",
            ),
            StructuredTool.from_function(
                func=self.get_property_details,
                name="get_property_details",
                description="Get details for a property by name. Input: property_name",
            ),
            StructuredTool.from_function(
                func=self.compare_property_profits,
                name="compare_property_profits",
                description="Compare profits between two properties. Input: property1 and property2",
            ),
        ]

    def calculate_total_pnl(self, year: str = None) -> str:
        return self.data_handler.calculate_total_pnl(year)

    def get_property_details(self, property_name: str) -> str:
        return self.data_handler.get_property_details(property_name)

    def compare_property_profits(self, property1: str, property2: str) -> str:
        return self.data_handler.compare_property_profits(property1, property2)