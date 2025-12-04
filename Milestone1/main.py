import os
import requests
from dotenv import load_dotenv

from langchain_google_genai import ChatGoogleGenerativeAI

from langchain_classic.prompts import PromptTemplate
from langchain_classic.chains import LLMChain
from langchain_classic.tools import Tool
from langchain_classic.agents import initialize_agent, AgentType
from langchain_classic.memory import ConversationBufferMemory


# Load API key from .env

load_dotenv()


def get_llm():
   
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        raise RuntimeError(
            "GOOGLE_API_KEY is missing. Put it in your .env file first."
        )

    
    llm = ChatGoogleGenerativeAI(
        model="gemini-2.0-flash",
        google_api_key=api_key,
        temperature=0.3,
    )
    return llm



# Basic PromptTemplate + LLMChain

def build_explain_chain(llm):
    """
    This chain explains any topic in simple language.
    """
    prompt = PromptTemplate(
        input_variables=["topic"],
        template=(
            "You are a friendly teacher.\n"
            "Explain the topic below in very simple words so that a beginner "
            "can understand.\n\n"
            "Topic: {topic}\n"
        ),
    )

    chain = LLMChain(
        llm=llm,
        prompt=prompt,
        verbose=False,
    )
    return chain



# Tools (greeting + weather)

def greet(name: str) -> str:
    """
    Simple greeting tool.
    """
    return f"Hello {name}, I am your LangChain + Gemini agent!"


def get_weather(city: str) -> str:
    """
    Simple weather tool using wttr.in free API.
    Only current temperature in Celsius.
    """
    try:
        url = f"https://wttr.in/{city}?format=j1"
        response = requests.get(url, timeout=10)
        data = response.json()
        temp_c = data["current_condition"][0]["temp_C"]
        return f"Current temperature in {city} is {temp_c}°C."
    except Exception as e:
        return f"Sorry, I could not get weather for {city}. Error: {e}"


# Wrap Python functions into LangChain Tools
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



# Memory (short-term chat history)

memory = ConversationBufferMemory(
    memory_key="chat_history",
    return_messages=True,
)


# Agent creation (Zero-shot ReAct)

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


# Console interface (main program)

def main():
    
    llm = get_llm()
    explain_chain = build_explain_chain(llm)

    print("Simple LLMChain Demo (Gemini) ")
    demo_topic = "What is artificial intelligence?"
   
    answer = explain_chain.invoke({"topic": demo_topic})
    print(f"Topic: {demo_topic}")
    print("Answer:")
    print(answer["text"])

    print("===================================================")

    print("\nNow starting the interactive Gemini agent...")
    agent = create_agent(agent_type=AgentType.ZERO_SHOT_REACT_DESCRIPTION)
    print("Agent is ready!")
    print("Type 'exit' to quit.\n")

    print("Some ideas to try:")
    print("- Greet Amit in a friendly way.")
    print("- Use the weather tool to get the temperature in Silchar.")
    print("- Explain binary search in simple words.")

    while True:
        user_input = input("\nYou: ").strip()
        if user_input.lower() in ("exit", "quit"):
            print("Agent: Bye! See you later.")
            break

        if not user_input:
            continue 

        try:
            response = agent.run(user_input)
        except Exception as e:
            response = f"Sorry, something went wrong: {e}"

        print("Agent:", response)


if __name__ == "__main__":
    main()
