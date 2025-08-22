# from autogen_core.models import UserMessage
# from autogen_ext.models.ollama import OllamaChatCompletionClient

# # Assuming your Ollama server is running locally on port 11434.
# ollama_model_client = OllamaChatCompletionClient(model="llama3.2")

# response = await ollama_model_client.create([UserMessage(content="What is the capital of France?", source="user")])
# print(response)
# await ollama_model_client.close()



from autogen_core.models import UserMessage
from autogen_ext.models.ollama import OllamaChatCompletionClient

# Start the client; this assumes your Ollama server is running on localhost:11434
ollama_client = OllamaChatCompletionClient(
    model="llama3.2",  # or whatever model you pulled
    # model="gemma3",  # or whatever model you pulled
    # host="http://localhost:11434",
)
# Make sure to run this code in an async-compatible environment
import asyncio

async def main():
    result = await ollama_client.create([
        UserMessage(content="What is the capital of France?", source="user")
    ])  # type: ignore
    print(result)
    await ollama_client.close()

asyncio.run(main())
