from langchain_openai import ChatOpenAI
from langchain_experimental.agents import create_pandas_dataframe_agent
from langchain.agents import AgentExecutor


class LangChainPandasAgent:
    def __init__(self, data_handler, temperature=0):
        self.df = data_handler.df
        self.llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=temperature)

        # Create the LangChain agent
        self.agent: AgentExecutor = create_pandas_dataframe_agent(
            llm=self.llm,
            df=self.df,
            verbose=True,
            return_intermediate_steps=False,
            allow_dangerous_code=True,
        )

    def run(self, query: str) -> str:
        try:
            return self.agent.invoke(query)
        except Exception as e:
            return f"Agent error: {e}"