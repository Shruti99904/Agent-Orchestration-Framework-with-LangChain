import os
import random
from dotenv import load_dotenv

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.tools import Tool
from langchain.agents import initialize_agent, AgentType


# =====================================================
# LOAD ENV
# =====================================================
load_dotenv()
api_key = os.getenv("AIzaSyAgmqnYB77zUGNkS4OqQMiTToBF_CwKLzc")

# =====================================================
# TOOLS
# =====================================================

# -------- WEATHER TOOL --------
def mock_weather_api(location: str) -> str:
    try:
        conditions = ["Sunny", "Rainy", "Cloudy", "Windy", "Stormy"]
        temp = random.randint(20, 38)
        cond = random.choice(conditions)
        return f"Weather in {location.title()}: {cond}, {temp}°C"
    except:
        return "Weather API error."

# -------- DICTIONARY TOOL --------
mock_dictionary = {
    "computer": "An electronic device used for computation.",
    "network": "A group of connected devices that communicate.",
    "protocol": "A set of rules governing data communication.",
    "ai": "Artificial Intelligence, machine-simulated intelligence."
}

def dictionary_lookup(word: str) -> str:
    try:
        return mock_dictionary.get(word.lower(), "Word not found in dictionary.")
    except:
        return "Dictionary lookup error."

# =====================================================
# LLM
# =====================================================
llm = ChatGoogleGenerativeAI(
    model="models/gemini-flash-lite-latest",
    temperature=0.2,
    api_key=api_key
)

# =====================================================
# TOOLS REGISTRATION
# =====================================================
tools = [
    Tool(
        name="weather_api",
        func=mock_weather_api,
        description="Get weather information for a location"
    ),
    Tool(
        name="dictionary",
        func=dictionary_lookup,
        description="Get meaning of a word"
    )
]

# =====================================================
# PROMPT
# =====================================================
prompt = PromptTemplate(
    input_variables=["input", "tools", "tool_names", "agent_scratchpad"],
    template="""
You are a helpful AI agent.

TOOLS:
{tools}
Tool names: {tool_names}

RULES:
- Weather → weather_api
- Word meaning → dictionary
- NEVER create your own questions
- NEVER loop
- If a tool cannot answer, say so clearly

Question: {input}

Thought: what do I need?
Action: <tool name if needed>
Action Input: <input>
Observation: <tool result>
Final Answer: <answer>

{agent_scratchpad}
"""
)

# =====================================================
# AGENT
# =====================================================
agent_executor = initialize_agent(
    tools=tools,
    llm=llm,
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    verbose=True,
    handle_parsing_errors=True
)


# =====================================================
# MAIN LOOP
# =====================================================
print("\nLangChain Agent Ready")
print("Type 'exit' to stop.\n")

while True:
    user_input = input("You: ")

    if user_input.lower() == "exit":
        print("Agent: Goodbye!")
        break

    try:
        response = agent_executor.invoke({"input": user_input})
        print("Agent:", response["output"], "\n")
    except Exception as e:
        print("Agent Error:", e, "\n")
