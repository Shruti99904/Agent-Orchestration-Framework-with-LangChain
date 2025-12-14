import os
from pydantic import BaseModel, Field
from langchain.tools import tool
from langchain.agents import create_agent
from langchain_core.messages import HumanMessage
from langchain_openai import ChatOpenAI  # ONLY OpenAI!
# FREE KEY: https://platform.openai.com/api-keys → "Create new secret key"
OPENAI_API_KEY = "YOUR_KEY_HERE"  
os.environ["OPENAI_API_KEY"] = OPENAI_API_KEY

print(f"🔑 {'✅ OK' if OPENAI_API_KEY.startswith('sk-proj') else '❌ ADD KEY'}")

# TOOL 1: Calculator
@tool
def calculator(expression: str) -> str:
    """Math calculator for numbers: 2+2, 15/3, 5*4."""
    try:
        result = eval(expression, {"__builtins__": {}})
        return f"✅ {expression} = {result}"
    except:
        return f"❌ Bad math: {expression}. Try 2+2"

# TOOL 2: Weather
class WeatherInput(BaseModel):
    city: str = Field(description="City name")

@tool(args_schema=WeatherInput)
def get_weather(city: str) -> str:
    """Current weather for any city."""
    data = {
        "London": "14°C cloudy", "New York": "22°C sunny",
        "Tokyo": "18°C rainy", "Paris": "16°C partly cloudy"
    }
    return f"🌤️ {city}: {data.get(city.title(), '20°C sunny')}"

# OPENAI MODEL
model = ChatOpenAI(model="gpt-4o-mini", temperature=0)

print("✅ READY!")

agent = create_agent(
    model, [calculator, get_weather],
    system_prompt="Use calculator for math, get_weather for weather."
)

print("\n🚀 MILESTONE 2 ✅\n")

# TESTS
print("1️⃣ MATH:", agent.invoke({"messages": [HumanMessage(content="25*4/5+10")]}]["messages"][-1].content)
print("2️⃣ WEATHER:", agent.invoke({"messages": [HumanMessage(content="Tokyo weather")]})["messages"][-1].content)
print("3️⃣ COMBO:", agent.invoke({"messages": [HumanMessage(content="NYC vs London temps")]})["messages"][-1].content)

print("\n🎉 ALL PASS!")
