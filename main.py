from agent import OpenAIAgent
from data import DataHandler


def main():
    # Change this to True to make real API calls
    is_runtime = False
    agent = OpenAIAgent(is_runtime=is_runtime)
    response = agent.test_call()
    print("Agent response:", response)

    dh = DataHandler('resources/cortex.parquet')
    dh.load_data()
    dh.print_head_and_info()


if __name__ == "__main__":
    main()
