from agents import Agent, Runner, set_default_openai_key

from config.constants import OPENAI_API_KEY

# Set default key
set_default_openai_key(OPENAI_API_KEY)

agent = Agent(name="Crypto trader", instructions="You are a Solana bull poster. Always have a positive sentiment for crypto.")

result = Runner.run_sync(agent, "Write a post about Solana using real-time data")
print(result.final_output)

# Code within the code,
# Functions calling themselves,
# Infinite loop's dance.