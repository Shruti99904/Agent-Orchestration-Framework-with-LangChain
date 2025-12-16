print(">>> Agent script started")
import random
import os
from dotenv import load_dotenv

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.agents import create_react_agent, AgentExecutor
from langchain.tools import Tool
from langchain.prompts import PromptTemplate


# ================== WEATHER TOOL ==================
def mock_weather_api(location: str) -> str:
    try:
        conditions = ["Sunny", "Rainy", "Cloudy", "Windy", "Stormy"]
        temp = random.randint(20, 38)
        cond = random.choice(conditions)
        return f"Weather in {location.title()}: {cond}, {temp}°C"
    except:
        return "Weather API error."


# ================== DICTIONARY TOOL ==================
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


# ================== LOAD API KEY ==================
load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")


# ================== LLM ==================
llm = ChatGoogleGenerativeAI(
    model="models/gemini-flash-lite-latest",
    temperature=0.2,
    api_key=api_key
)


# ================== TOOLS ==================
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


# ================== PROMPT ==================
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


# ================== AGENT ==================
agent = create_react_agent(llm, tools, prompt)

agent_executor = AgentExecutor(
    agent=agent,
    tools=tools,
    verbose=True,
    handle_parsing_errors=True
)


# ================== MAIN LOOP ==================
print("\n✅ LangChain Agent Ready")
print("Type 'exit' to stop.\n")

while True:
    try:
        user_input = input("You: ")
    except EOFError:
        break

    if user_input.strip().lower() == "exit":
        print("Agent: Goodbye!")
        break

    response = agent_executor.invoke({"input": user_input})
    print("Agent:", response["output"], "\n")
