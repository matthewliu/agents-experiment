from agents import Agent, Runner, set_default_openai_key
import asyncio
from config.constants import OPENAI_API_KEY

# Set default key
set_default_openai_key(OPENAI_API_KEY)

translation_agent = Agent(
    name="Translation agent",
    handoff_description="Translates content to Mandarin Chinese",
    instructions="You will translate whatever is being said to Mandarin Chinese. Always respond in Chinese characters.",
)

spanish_agent = Agent(
    name="Spanish agent",
    handoff_description="Handles Spanish language queries",
    instructions="""You only speak Spanish. 
    
    IMPORTANT: After providing your Spanish response, you MUST hand off to the Translation agent.
    
    Do not attempt to translate to Chinese yourself - only respond in Spanish, then hand off.
    
    The handoff to Translation agent is MANDATORY for EVERY interaction.""",
    handoffs=[translation_agent],
)

english_agent = Agent(
    name="English agent",
    handoff_description="Handles English language queries",
    instructions="You only speak English. After responding in English, ALWAYS hand off to the Translation agent so your response can be translated to Chinese.",
    handoffs=[translation_agent],
)

triage_agent = Agent(
    name="Triage agent",
    instructions="""Examine the language of the input and hand off to the appropriate language agent.
    If input is in Spanish, ONLY hand off to Spanish agent.
    If input is in English, ONLY hand off to English agent.
    Never respond directly - always use a handoff.""",
    handoffs=[spanish_agent, english_agent],
)

async def main():
    # Spanish input example
    spanish_result = await Runner.run(triage_agent, input="Hola, ¿cómo estás?")
    print("Spanish input → Chinese output:")
    print(spanish_result.final_output)
    print()
    
    # English input example
    english_result = await Runner.run(triage_agent, input="Hello, how are you?")
    print("English input → Chinese output:")
    print(english_result.final_output)

if __name__ == "__main__":
    asyncio.run(main())