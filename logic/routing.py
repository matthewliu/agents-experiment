import asyncio
import uuid
import time

from openai.types.responses import ResponseContentPartDoneEvent, ResponseTextDeltaEvent

from agents import Agent, RawResponsesStreamEvent, Runner, TResponseInputItem, trace, set_default_openai_key
from config.constants import OPENAI_API_KEY
set_default_openai_key(OPENAI_API_KEY)

"""
This example shows the handoffs/routing pattern. The triage agent receives the first message, and
then hands off to the appropriate agent based on the language of the request. Responses are
streamed to the user.
"""

french_agent = Agent(
    name="french_agent",
    instructions="You only speak French",
)

spanish_agent = Agent(
    name="spanish_agent",
    instructions="You only speak Spanish",
)

english_agent = Agent(
    name="english_agent",
    instructions="You only speak English",
)

triage_agent = Agent(
    name="triage_agent",
    instructions="Handoff to the appropriate agent based on the language of the request.",
    handoffs=[french_agent, spanish_agent, english_agent],
)


async def main():
    conversation_id = str(uuid.uuid4().hex[:16])
    print(f"Starting conversation with ID: {conversation_id}")

    msg = input("Hi! We speak French, Spanish and English. How can I help? ")
    agent = triage_agent
    inputs: list[TResponseInputItem] = [{"content": msg, "role": "user"}]

    while True:
        print("\n" + "="*50)
        print(f"Processing with agent: {agent.name}")
        print("="*50)
        
        with trace("Routing example", group_id=conversation_id):
            print("\nStarting streaming response...")
            start_time = time.time()
            delta_count = 0
            full_response = ""
            
            result = Runner.run_streamed(
                agent,
                input=inputs,
            )
            
            async for event in result.stream_events():
                # Log the event type
                print(f"\nEvent type: {type(event).__name__}", flush=True)
                
                if not isinstance(event, RawResponsesStreamEvent):
                    print(f"  Skipping non-RawResponsesStreamEvent: {event}", flush=True)
                    continue
                
                data = event.data
                print(f"  Data type: {type(data).__name__}", flush=True)
                
                if isinstance(data, ResponseTextDeltaEvent):
                    delta_count += 1
                    delta_text = data.delta
                    full_response += delta_text
                    
                    # Log delta details
                    print(f"  Delta #{delta_count}: '{delta_text}' (length: {len(delta_text)})", flush=True)
                    
                    # Print the delta to simulate the streaming effect
                    print(delta_text, end="", flush=True)
                    
                elif isinstance(data, ResponseContentPartDoneEvent):
                    print("\n  Content part complete", flush=True)
                    print("\n")
            
            end_time = time.time()
            print("\n" + "-"*50)
            print(f"Streaming complete in {end_time - start_time:.2f} seconds")
            print(f"Received {delta_count} deltas")
            print(f"Total response length: {len(full_response)} characters")
            print("-"*50)
            
            # Check if a handoff occurred
            if agent.name != result.current_agent.name:
                print(f"\nHandoff detected: {agent.name} → {result.current_agent.name}")
            
            # Update for next iteration
            inputs = result.to_input_list()
            print("\nCurrent conversation history:")
            for i, msg in enumerate(inputs):
                print(f"  Message {i+1}: [{msg['role']}] {msg['content'][:50]}...")
            
        user_msg = input("\nEnter a message: ")
        inputs.append({"content": user_msg, "role": "user"})
        agent = result.current_agent


if __name__ == "__main__":
    asyncio.run(main())