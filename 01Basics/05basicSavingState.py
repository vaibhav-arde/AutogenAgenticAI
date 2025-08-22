import asyncio
import json
import os

from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.ui import Console
from autogen_ext.models.ollama import OllamaChatCompletionClient


async def main():
    #create first assitant agent
    model_client = OllamaChatCompletionClient( model="llama3.2" )
    agent1 = AssistantAgent( name="Helper", model_client=model_client)

    agent2 = AssistantAgent( name="BackupHelper", model_client=model_client )

    await Console( agent1.run_stream( task="My favourite color is blue" ) )
    state = await agent1.save_state()
    with open("01Basics/memory.json", "w") as f:
        json.dump(state, f, default=str)

    with open("01Basics/memory.json", "r") as f:
      saved_state = json.load(f)

    await agent2.load_state(saved_state)

    await Console(agent2.run_stream(task="What is my favourite color?"))

    await model_client.close()










    await model_client.close()


asyncio.run( main() )
