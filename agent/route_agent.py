from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain_core.runnables import Runnable
from agent import LangChainPandasAgent, GPTAgentTools
from dotenv import load_dotenv
load_dotenv()

class RouteAgent:
    def __init__(self, data_handler, temperature=0):
        self.gpt_agent = GPTAgentTools(data_handler)
        self.pandas_agent = LangChainPandasAgent(data_handler, temperature)
        self.llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=temperature)

        self.routing_prompt = ChatPromptTemplate.from_messages([
            ("system",
             "You are a routing assistant that must select exactly one function name "
             "from the list below based on the user's request:\n\n"
             "- calculate_total_pnl: Only if the user clearly asks for total profit/loss **and** provides a specific year.\n"
             "- get_property_details: Only if the user asks for information about a specific property **and** names the property.\n"
             "- compare_property_profits: Only if the user wants to compare two properties **and** provides both property names.\n"
             "- pandas: For all other general, vague, or exploratory questions (e.g., 'which property is best?', 'who are all the tenants?', 'show me all buildings').\n\n"
             "Respond strictly with one of the following words and nothing else:\n"
             "`calculate_total_pnl`, `get_property_details`, `compare_property_profits`, or `pandas`.\n\n"
             "Examples:\n"
             "User: 'What was my total profit in 2023?' → calculate_total_pnl\n"
             "User: 'Show me details for Building 180' → get_property_details\n"
             "User: 'Compare profit between Building 1 and Building 2' → compare_property_profits\n"
             "User: 'Which building made the most profit?' → pandas\n"
             "User: 'What is the profit by category?' → pandas\n\n"
             "Respond with only one word."),
            ("user", "{input}")
        ])
        self.router_chain: Runnable = self.routing_prompt | self.llm

        # Argument extractor
        self.argument_prompt = ChatPromptTemplate.from_messages([
            ("system", "You are an assistant extracting required arguments from user input.\n"
                       "If missing, return an empty string.\n"
                       "Respond in JSON format with required fields for the function '{func_name}'"),
            ("user", "{input}")
        ])
        self.argument_chain: Runnable = self.argument_prompt | self.llm

        self.tool_map = {
            "calculate_total_pnl": self.gpt_agent.calculate_total_pnl,
            "get_property_details": self.gpt_agent.get_property_details,
            "compare_property_profits": self.gpt_agent.compare_property_profits,
        }

        # Expected args per function (for validation)
        self.tool_args = {
            "calculate_total_pnl": ["year"],
            "get_property_details": ["property_name"],
            "compare_property_profits": ["property1", "property2"],
        }

    def run(self, query: str) -> str:
        try:
            decision = self.router_chain.invoke({"input": query}).content.strip().lower()
            print(f"[Routing Decision] → {decision}")

            if decision == "pandas" or decision not in self.tool_map:
                return self.pandas_agent.run(query)

            # Extract arguments
            func_args = self.tool_args[decision]
            extraction_prompt = {
                "input": query,
                "func_name": decision
            }
            arg_response = self.argument_chain.invoke(extraction_prompt).content
            print(f"[Extracted Args] → {arg_response}")

            # Try to parse JSON response
            try:
                import json
                args_dict = json.loads(arg_response)
            except Exception:
                return f"Could not parse arguments for '{decision}'. Fallback to smart agent.\n→ {self.pandas_agent.run(query)}"

            # Validate all required args are present
            if not all(k in args_dict and args_dict[k] for k in func_args):
                return f"Missing required parameters. Using fallback agent.\n→ {self.pandas_agent.run(query)}"

            # Call the correct function
            result = self.tool_map[decision](**args_dict)
            return result

        except Exception as e:
            return f"Routing error: {e}"
