import os
import random
from dotenv import load_dotenv

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.agents import create_react_agent, AgentExecutor
from langchain.tools import Tool
from langchain.prompts import PromptTemplate

# ================== 1. TOOLS ==================
def mock_weather_api(location: str) -> str:
    """Returns fake weather data."""
    conditions = ["Sunny", "Rainy", "Cloudy", "Windy", "Stormy"]
    temp = random.randint(20, 38)
    cond = random.choice(conditions)
    return f"Weather in {location.title()}: {cond}, {temp}°C"

mock_dictionary = {
    "computer": "An electronic device used for computation.",
    "network": "A group of connected devices that communicate.",
    "protocol": "A set of rules governing data communication.",
    "ai": "Artificial Intelligence, machine-simulated intelligence."
}

def dictionary_lookup(word: str) -> str:
    """Looks up words in a local dictionary."""
    return mock_dictionary.get(word.lower().strip(), "Word not found in dictionary.")

# Wrap functions in LangChain Tools
tools = [
    Tool(
        name="weather_api",
        func=mock_weather_api,
        description="Useful for when you need to answer questions about the weather in a specific city."
    ),
    Tool(
        name="dictionary",
        func=dictionary_lookup,
        description="Useful for when you need to find the meaning of a word."
    )
]

# ================== 2. LLM & PROMPT ==================
load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")

llm = ChatGoogleGenerativeAI(
    model="gemini-1.5-flash", 
    temperature=0, 
    google_api_key=api_key
)

# Robust ReAct Prompt Template
template = """Answer the following questions as best you can. You have access to the following tools:

{tools}

Use the following format:

Question: the input question you must answer
Thought: you should always think about what to do
Action: the action to take, should be one of [{tool_names}]
Action Input: the input to the action
Observation: the result of the action
... (this Thought/Action/Action Input/Observation can repeat N times)
Thought: I now know the final answer
Final Answer: the final answer to the original input question

Begin!

Question: {input}
Thought: {agent_scratchpad}"""

prompt = PromptTemplate.from_template(template)

# ================== 3. INITIALIZE AGENT ==================
agent = create_react_agent(llm, tools, prompt)

agent_executor = AgentExecutor(
    agent=agent,
    tools=tools,
    verbose=True, # Set to True to see the "Thinking" process
    handle_parsing_errors=True,
    max_iterations=5
)

# ================== 4. EXECUTION ==================
if __name__ == "__main__":
    print("\n✅ LangChain Agent Ready")
    print("Type 'exit' to stop.\n")

    while True:
        try:
            user_input = input("You: ")
            if user_input.strip().lower() == "exit":
                print("Agent: Goodbye!")
                break
            
            response = agent_executor.invoke({"input": user_input})
            print(f"\nAgent: {response['output']}\n")
            
        except Exception as e:
            print(f"Error: {e}")
