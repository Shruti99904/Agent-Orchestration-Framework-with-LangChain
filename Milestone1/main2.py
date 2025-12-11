# milestone2.py
# Milestone 2: Tool Integration & API Calling (Single-File Submission)

from langchain.agents import initialize_agent, AgentType
from langchain_openai import ChatOpenAI
from langchain.tools import tool
import random


# -----------------------------------------------------
# WEEK 3 — TOOL 1: Calculator (with error handling)
# -----------------------------------------------------
@tool
def calculator(expression: str) -> str:
    """Solves basic math expressions like '23*9'."""
    try:
        result = eval(expression)
        return f"Result: {result}"
    except Exception as e:
        return f"Calculator Error: {str(e)}"


# -----------------------------------------------------
# WEEK 3 — TOOL 2: Simulated Weather API
# -----------------------------------------------------
@tool
def get_weather(city: str) -> str:
    """Provides mock weather information for a city."""
    try:
        if not city.strip():
            raise ValueError("City name is empty")

        conditions = ["Sunny", "Cloudy", "Windy", "Rainy", "Stormy"]
        temperature = random.randint(15, 40)
        condition = random.choice(conditions)

        return f"Weather in {city}: {condition}, {temperature}°C"
    except Exception as e:
        return f"Weather API Error: {str(e)}"


# -----------------------------------------------------
# WEEK 4 — LLM SETUP + TOOL GUIDANCE PROMPT
# -----------------------------------------------------
system_prompt = """
You are a helpful assistant.
Use the Calculator tool for math.
Use the Weather tool when user asks about weather.
If tools are not needed, answer normally.
"""

llm = ChatOpenAI(
    model="gpt-4o-mini",
    temperature=0,
    max_tokens=300,
)

tools = [calculator, get_weather]

agent = initialize_agent(
    tools=tools,
    llm=llm,
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    verbose=True
)


# -----------------------------------------------------
# WEEK 4 — DEMO TESTS OF TOOL INVOCATION
# -----------------------------------------------------
def test_agent():
    print("\n--- TEST 1: Calculator Tool ---")
    print(agent.run("What is 56 * 89?"))

    print("\n--- TEST 2: Weather Tool ---")
    print(agent.run("Tell me the weather in Delhi"))

    print("\n--- TEST 3: Weather Tool Error Case ---")
    print(agent.run("Weather in '' please"))

    print("\n--- TEST 4: Normal Chat (No tool needed) ---")
    print(agent.run("Explain the use of tools in LangChain."))


if __name__ == "__main__":
    test_agent()
