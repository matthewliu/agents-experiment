from agents import Agent, Runner, set_default_openai_key, function_tool
import asyncio
from config.constants import OPENAI_API_KEY

# Set default key
set_default_openai_key(OPENAI_API_KEY)

@function_tool
def get_weather(city: str) -> str:
    return f"The weather in {city} is sunny."

@function_tool
def get_news(topic: str) -> str:
    return f"The news about {topic} is that is bad for the world."

agent = Agent(
    name="Hello world",
    instructions="You are a helpful agent.",
    tools=[get_weather, get_news],
)


async def main():
    result = await Runner.run(agent, input="What's the weather in Tokyo?")
    print(result.final_output)
    # The weather in Tokyo is sunny.

    result = await Runner.run(agent, input="What's the news about AI?")
    print(result.final_output)
    # The news about AI is that it life blows.


if __name__ == "__main__":
    asyncio.run(main())