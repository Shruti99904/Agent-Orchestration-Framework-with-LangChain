# ------------------------------
# LangChain Agent using OpenAI GPT-3.5
# ------------------------------

import os
import requests
from dotenv import load_dotenv

from langchain_classic.prompts import PromptTemplate
from langchain_classic.chains import LLMChain
from langchain_classic.tools import Tool
from langchain_classic.agents import initialize_agent, AgentType
from langchain_classic.memory import ConversationBufferMemory

# ------------------------------
# Load API key from .env if exists
# ------------------------------
load_dotenv()
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    raise RuntimeError("OPENAI_API_KEY is missing. Set it in .env or environment variables.")

# ------------------------------
# Use OpenAI GPT-3.5 as LLM
# ------------------------------
from langchain.chat_models import ChatOpenAI

def get_llm():
    return ChatOpenAI(
        model_name="gpt-3.5-turbo",
        temperature=0.3,
        openai_api_key=OPENAI_API_KEY
    )

# ------------------------------
# LLMChain for explaining topics
# ------------------------------
def build_explain_chain(llm):
    prompt = PromptTemplate(
        input_variables=["topic"],
        template=(
            "You are a friendly teacher.\n"
            "Explain the topic below in very simple words so that a beginner "
            "can understand.\n\n"
            "Topic: {topic}\n"
        ),
    )
    return LLMChain(llm=llm, prompt=prompt, verbose=False)

# ------------------------------
# Tools
# ------------------------------
def greet(name: str) -> str:
    return f"Hello {name}, I am your LangChain + GPT agent!"

def get_weather(city: str) -> str:
    try:
        url = f"https://wttr.in/{city}?format=j1"
        response = requests.get(url, timeout=10)
        data = response.json()
        temp_c = data["current_condition"][0]["temp_C"]
        return f"Current temperature in {city} is {temp_c}°C."
    except Exception as e:
        return f"Sorry, could not get weather for {city}. Error: {e}"

greet_tool = Tool(
    name="greeting_tool",
    func=greet,
    description="Use this to greet a person by name.",
)

weather_tool = Tool(
    name="weather",
    func=get_weather,
    description="Use this to get the current temperature of a city in Celsius.",
)

tools = [greet_tool, weather_tool]

# ------------------------------
# Memory for agent
# ------------------------------
memory = ConversationBufferMemory(
    memory_key="chat_history",
    return_messages=True,
)

# ------------------------------
# Create agent
# ------------------------------
def create_agent(agent_type: AgentType = AgentType.ZERO_SHOT_REACT_DESCRIPTION):
    llm = get_llm()
    agent = initialize_agent(
        tools=tools,
        llm=llm,
        agent=agent_type,
        memory=memory,
        verbose=True,
    )
    return agent

# ------------------------------
# Main program
# ------------------------------
def main():
    llm = get_llm()
    explain_chain = build_explain_chain(llm)

    # Demo: Explain a topic
    demo_topic = "What is artificial intelligence?"
    answer = explain_chain.invoke({"topic": demo_topic})
    if isinstance(answer, dict) and "text" in answer:
        output = answer["text"]
    else:
        output = answer

    print("=== LLMChain Demo ===")
    print(f"Topic: {demo_topic}")
    print("Answer:")
    print(output)
    print("=====================")

    # Interactive agent
    agent = create_agent(agent_type=AgentType.ZERO_SHOT_REACT_DESCRIPTION)
    print("\n=== GPT Agent Ready ===")
    print("Type your messages. Type 'exit' to quit.\n")

    while True:
        user_input = input("You: ").strip()
        if user_input.lower() in ("exit", "quit"):
            print("Agent: Bye! See you later.")
            break
        if not user_input:
            continue

        try:
            response = agent.run(user_input)
        except Exception as e:
            response = f"Error: {e}"
        print("Agent:", response)

# ------------------------------
# Run the program
# ------------------------------
main()
