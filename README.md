# GPT Real Estate Asset Management Agent

This is a prototype GPT-based assistant designed to help manage real estate assets using natural language instructions. It can answer questions about property details, profit & loss (P&L), comparisons, and more.

---

## Features

Natural language understanding  
GPT-based function routing and reasoning  
Smart fallback to a general pandas agent for flexible queries  
Modular and extensible design  
Graceful error handling for edge cases and vague input

---

## Setup Instructions

### 1. Clone the repository

```bash
git clone https://github.com/sgotteiner/real-estate-agent.git
cd real-estate-agent
python -m venv real_estate_venv  # Work on Python 3.11 or below because of Langchain support.
real_estate_venv\Scripts\activate  # On Linux: source real_estate_venv/bin/activate
pip install -r requirements.txt
```

### 2. Create the virtual environment and install the dependencies

```bash
python -m venv real_estate_venv  # Work on Python 3.11 or below because of Langchain support.
real_estate_venv\Scripts\activate  # On Linux: source real_estate_venv/bin/activate
pip install -r requirements.txt
```

### 3. Set your OpenAI API key

Create a .env file in the directory of the project and write "OPENAI_API_KEY=your-openai-key-here"

### 4. Place your dataset in the resources folder

For example resources/cortex.parquet

---

## How to use

### 1. Run the system

```bash
Python main.py
```

### 2. You'll be prompted to enter natural language questions like:

```bash
You: What is my total profit in 2023?
You: Show me details for Building 180
You: Compare profits between Building 1 and Building 2
You: Which property had the most tenants?
```

### 3. The system will automatically:

* Route the query to the correct handler using GPT
* Extract parameters if necessary
* Use specialized tools or a general-purpose pandas agent for flexible data exploration

### 4. To exit type exit or quit

---

## How it works

### 1. User Query

The user types a natural language question (e.g. “Compare profits between Building A and B”).

### 2. Routing with GPT

A custom GPT-based router analyzes the query and decides:
If it matches a specific tool (like P&L calculation or property comparison), and all parameters are provided → it uses that tool.
Otherwise → it routes the query to a flexible pandas agent.

### 3. Argument Extraction (if needed)

If a tool is selected, GPT also extracts the required arguments (e.g. year or property names) from the user input.

### 4. Execution

If routed to a tool → a structured function (wrapped by GPTAgentTools) is called.
If routed to the pandas agent → a LangChain agent runs a general-purpose DataFrame analysis.

### 5. Result

The final answer is shown clearly and handles vague or incomplete input by falling back safely.

---

## Architecture

                                                    +-----------------+
                                                    |   User Query    |
                                                    +--------+--------+
                          
                                                             |
                                                    +--------v--------+
                                                    |   RouteAgent    |
                                                    | (uses GPT to    |
                                                    |  decide path)   |
                                                    +----+-----+------+
                                                         |     |
                               +-------------------------+     +-------------------------+
                               |                                                   |
                          +----v----+                                      +--------v--------+
                          | GPTAgent|  <- Handles specific tasks           | LangChainPandas |
                          |  Tools  |     (like P&L, comparisons)          | Agent            |
                          +---------+                                      +------------------+

---

## Challenges and How I Solved Them

### 1. LangChain Pandas Agent Limitations

Sometimes the LangChain Pandas agent didn't behave as expected or failed to format the response in a way I needed.
To handle this, I built a flexible architecture that supports both a smart fallback agent (Pandas) and custom tool functions for well-defined tasks.
I introduced a router agent that decides, per query, whether to use a specific tool or delegate the task to the Pandas agent.

### 2. Routing Sensitivity and GPT Behavior

Determining whether a request should go to a tool or the Pandas agent was challenging.
I used GPT to classify the user's intent, but early on it preferred tools even when the input was vague or didn’t match tool requirements.
This happened because GPT tends to confidently pick an option that sounds relevant—even when it isn’t.
I resolved this by crafting a strict routing prompt that forces GPT to choose a tool only if all required details are clearly present.
If not, it defaults to the more flexible Pandas agent.