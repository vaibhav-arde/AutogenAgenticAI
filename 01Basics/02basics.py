import asyncio
import os

from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.messages import MultiModalMessage
from autogen_agentchat.ui import Console
from autogen_core import Image
from autogen_ext.models.ollama import OllamaChatCompletionClient


async def main1():
    model_client = OllamaChatCompletionClient( model="llava" )
    assistant = AssistantAgent( name="MultiModalAssistant", model_client=model_client )
    image = Image.from_file("SmapleImages/woman-giving-speech.jpg")
    multimodal_message = MultiModalMessage(
        content=["what do you see in this image", image], source="user"
    )
    await Console(assistant.run_stream(task=multimodal_message))
    await model_client.close()


asyncio.run( main1() )
