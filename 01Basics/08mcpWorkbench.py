import asyncio
import os

from autogen_agentchat.agents import AssistantAgent, UserProxyAgent
from autogen_agentchat.conditions import TextMentionTermination
from autogen_agentchat.teams import RoundRobinGroupChat
from autogen_agentchat.ui import Console
from autogen_ext.models.ollama import OllamaChatCompletionClient
from autogen_ext.tools.mcp import StdioServerParams, McpWorkbench


async def main():
    filesystem_server_params = StdioServerParams( command="npx",
                                                  args=[
                                                      "-y",
                                                      "@modelcontextprotocol/server-filesystem",
                                                      "/Users/vaibhavarde/Desktop/Autogen/AutogenAgenticAI/01Basics"],
                                                  read_timeout_seconds=60
                                                  )

    fs_workbench = McpWorkbench( filesystem_server_params )

    async with fs_workbench as fs_wb:
        model_client = OllamaChatCompletionClient( model="llama3.2" )

        math_tutor = AssistantAgent( name="MathTutor", model_client=model_client, workbench=fs_wb,
                                    system_message="You are helpful math tutor. Help the user solve math problems step "
                                                   "by step, You have to access file system"
                                                   "When the user says 'THANKS DONE' or similar, acknowledge and say "
                                                   "'LESSON COMPLETE' to end session." )

        user_proxy = UserProxyAgent( name="Student" )

        # Create team with text termination
        team = RoundRobinGroupChat(
            participants=[user_proxy, math_tutor],
            termination_condition=TextMentionTermination( "LESSON COMPLETE" )
        )

        await Console( team.run_stream( task="I need help with algebra problem. Tutor, feel free to create"
                                             "files to help with student learning " ) )

    await model_client.close()
asyncio.run( main() )
