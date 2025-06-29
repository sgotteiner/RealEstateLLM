from agent import RouteAgent, LangChainPandasAgent
from data import DataHandler
from dotenv import load_dotenv
load_dotenv()


DEFAULT_DATA_PATH = "resources/cortex.parquet"


def main():
    data_handler = DataHandler(DEFAULT_DATA_PATH)

    agent = RouteAgent(data_handler)
    # agent = LangChainPandasAgent(data_handler)

    print("LangChain Real Estate Agent ready. Type 'exit' to quit.\n")

    while True:
        query = input("You: ")
        if query.lower() in ["exit", "quit"]:
            break

        answer = agent.run(query)
        print(f"Agent: {answer}\n")


if __name__ == "__main__":
    main()