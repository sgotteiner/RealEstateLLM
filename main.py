from agent import GPTAgent
from data import DataHandler


def main():
    # Initialize and load data
    data_handler = DataHandler('resources/cortex.parquet')
    data_handler.load_data()

    # Create the GPT agent
    agent = GPTAgent(data_handler, is_runtime=True)  # Set to False to avoid using tokens

    print("GPT Real Estate Agent ready. Type 'exit' to quit.\n")

    while True:
        user_input = input("You: ")
        if user_input.lower() in ["exit", "quit"]:
            break

        response = agent.handle_request(user_input)
        print(f"Agent: {response}\n")

        break


if __name__ == "__main__":
    main()
