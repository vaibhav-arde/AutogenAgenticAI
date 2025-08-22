import asyncio
import os

from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.ui import Console
from autogen_ext.models.ollama import OllamaChatCompletionClient


async def main1():
    print( "I am inside function" )

    model_client = OllamaChatCompletionClient(model="llama3.2" )
    assistant = AssistantAgent( name="assistant", model_client=model_client )
    await Console( assistant.run_stream( task="What is 25 * 8?" ) )
    await model_client.close()


asyncio.run( main1() )