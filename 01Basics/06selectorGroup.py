import asyncio
import os

from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.conditions import MaxMessageTermination, TextMentionTermination
from autogen_agentchat.teams import SelectorGroupChat
from autogen_agentchat.ui import Console
from autogen_ext.models.ollama import OllamaChatCompletionClient


async def main():
    model_client = OllamaChatCompletionClient( model="llama3.2" )
    researcher = AssistantAgent(
        "ResearcherAgent",
        model_client=model_client,
        system_message="You are a researcher. Your role is to gather information and provide research findings ONLY. "
                       "Do not write articles or create content - just provide research data and facts."
    )

    writer = AssistantAgent(
        "WriterAgent",
        model_client=model_client,
        system_message="You are a writer. Your role is to take research information and "
                       "create well-written articles. Wait for research to be provided, then write the content."
    )

    critic = AssistantAgent(
        "CriticAgent",
        model_client=model_client,
        system_message="You are a critic. Review written content and provide feedback."
                       " Say 'TERMINATE' when satisfied with the final result."
    )
    text_termination = TextMentionTermination("TERMINATE")

    max_messages_termination = MaxMessageTermination( max_messages=15 )

    termination = text_termination |max_messages_termination

    team = SelectorGroupChat( participants=[critic, writer, researcher],
                       model_client=model_client, termination_condition=termination,
                       allow_repeated_speaker=True )

    await Console(team.run_stream(task ="Research renewable energy trends and write a brief article about the future of solar power." ))


asyncio.run(main())