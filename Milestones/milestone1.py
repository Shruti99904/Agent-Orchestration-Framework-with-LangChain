import os
import requests
from dotenv import load_dotenv

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate
from langchain.tools import Tool
from langchain.agents import initialize_agent, AgentType
from langchain.memory import ConversationBufferMemory

# 1. Load Environment Variables
load_dotenv()

def get_llm():
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        raise RuntimeError("GOOGLE_API_KEY is missing. Put it in your .env file first.")
    
    return ChatGoogleGenerativeAI(
        model="gemini-2.0-flash",
        google_api_key=api_key,
        temperature=0.3,
    )

# 2. Define the missing build_explain_chain function
def build_explain_chain(llm):
    template = "Explain the following topic in a simple way: {topic}"
    prompt = PromptTemplate.from_template(template)
    # Using the modern LCEL (LangChain Expression Language) syntax
    return prompt | llm

# 3. Tools Logic
def greet(name: str) -> str:
    return f"Hello {name}, I am your LangChain + Gemini agent!"

def get_weather(city: str) -> str:
    try:
        url = f"https://wttr.in/{city}?format=j1"
        response = requests.get(url, timeout=10)
        data = response.json()
        temp_c = data["current_condition"][0]["temp_C"]
        return f"Current temperature in {city} is {temp_c}°C."
    except Exception as e:
        return f"Sorry, I could not get weather for {city}. Error: {e}"

tools = [
    Tool(name="greeting_tool", func=greet, description="Use this to greet a person by name."),
    Tool(name="weather", func=get_weather, description="Use this to get the current temperature of a city in Celsius.")
]

# 4. Agent creation
def create_agent(memory):
    llm = get_llm()
    return initialize_agent(
        tools=tools,
        llm=llm,
        agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
        memory=memory,
        verbose=True,
        allow_dangerous_tools=True # Required in newer LangChain versions for custom tools
    )

# 5. Main execution
def main():
    llm = get_llm()
    
    # Simple Demo Section
    print("--- Simple LLMChain Demo (Gemini) ---")
    explain_chain = build_explain_chain(llm)
    demo_topic = "What is artificial intelligence?"
    
    # LCEL return message objects, use .content
    answer = explain_chain.invoke({"topic": demo_topic})
    print(f"Topic: {demo_topic}")
    print(f"Answer: {answer.content}\n")

    print("===================================================")

    # Agent Section
    print("\nNow starting the interactive Gemini agent...")
    memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)
    agent = create_agent(memory)
    
    print("Agent is ready! Type 'exit' to quit.\n")

    while True:
        user_input = input("You: ").strip()
        if user_input.lower() in ("exit", "quit"):
            print("Agent: Bye! See you later.")
            break
        if not user_input:
            continue 

        try:
            # agent.run is deprecated in newer versions, use .invoke or .run carefully
            response = agent.run(user_input)
            print("Agent:", response)
        except Exception as e:
            print(f"Agent Error: {e}")

if __name__ == "__main__":
    main()
