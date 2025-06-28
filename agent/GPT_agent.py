import openai
from agent import OpenAIAgent


class GPTAgent(OpenAIAgent):
    def __init__(self, data_handler, is_runtime=True):
        super().__init__(is_runtime)
        self.data_handler = data_handler

    def handle_request(self, user_input: str) -> str:
        if not self.is_runtime:
            return "GPT mode is disabled. Enable runtime to use GPT reasoning."

        system_prompt = (
            "You are an intelligent planner for real estate asset management. "
            "You must choose the best data function to call based on user input. "
            "Use one of the following functions:\n"
            "- get_property_details(property_name)\n"
            "- compare_property_profits(property1, property2)\n"
            "- calculate_total_pnl(year)\n\n"
            "Respond only with:\nCALL <function_name> | ARGS <comma-separated arguments>"
        )

        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_input}
        ]

        try:
            response = openai.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=messages
            )
            content = response.choices[0].message.content.strip()
        except Exception as e:
            return f"GPT API error: {e}"

        print(f"GPT raw response: {content}")

        # Parse GPT response
        if content.startswith("CALL"):
            try:
                call_line = content.replace("CALL", "").strip()
                func_name, args_raw = call_line.split("|")
                func_name = func_name.strip()
                args = [arg.strip() for arg in args_raw.replace("ARGS", "").strip().split(",")]

                if func_name == "get_property_details" and len(args) == 1:
                    return self.data_handler.get_property_details(args[0])

                elif func_name == "compare_property_profits" and len(args) == 2:
                    return self.data_handler.compare_property_profits(args[0], args[1])

                elif func_name == "calculate_total_pnl":
                    year = args[0] if args else None
                    return self.data_handler.calculate_total_pnl(year)

                else:
                    return f"Invalid function or argument count: {func_name}({', '.join(args)})"
            except Exception as e:
                return f"Failed to parse GPT response: {e}"
        else:
            return "GPT did not return a recognizable function call."