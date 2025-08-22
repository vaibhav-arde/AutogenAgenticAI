import asyncio
import os

from autogen_agentchat.agents import AssistantAgent, UserProxyAgent
from autogen_agentchat.conditions import TextMentionTermination
from autogen_agentchat.teams import RoundRobinGroupChat
from autogen_agentchat.ui import Console
from autogen_ext.models.ollama import OllamaChatCompletionClient


async def main():
    model_client = OllamaChatCompletionClient( model="llama3" )

    assistant = AssistantAgent( name="MathTutor", model_client=model_client,
                                system_message="You are helpful math tutor.Help the user solve math problems step by step"
                                               "When the user says 'THANKS DONE' or similar, acknowledge and say 'LESSON COMPLETE' to end session." )

    user_proxy = UserProxyAgent( name="Student" )

    team = RoundRobinGroupChat( participants=[user_proxy, assistant],
                                termination_condition=TextMentionTermination( "LESSON COMPLETE" ) )
    await Console(team.run_stream(task = "I need help with algebra problem"))


asyncio.run( main() )


#Human - Agent-(save)  ,Agent2 (save)
