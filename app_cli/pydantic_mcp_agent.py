'''MCP Agent for Pydantic AI'''
import os
import pathlib
import asyncio
import logging
from dotenv import load_dotenv
import logfire

from pydantic_ai.models.openai import OpenAIModel
from pydantic_ai.providers.openai import OpenAIProvider
from pydantic_ai import Agent

import mcp_client

from rich.markdown import Markdown
from rich.console import Console
from rich.live import Live

load_dotenv()

# 'if-token-present' means nothing will be sent (and the example will work)
# if you don't have logfire configured
logfire.configure(
    send_to_logfire='if-token-present',
    token=os.getenv('LOGFIRE_WRITE_KEY', None))


# Get the directory where the current script is located
SCRIPT_DIR = pathlib.Path(__file__).parent.resolve()
# Define the path to the config file relative to the script directory
CONFIG_FILE = SCRIPT_DIR / "mcp_config.json"


def get_model():
    '''Get the model from environment variables'''
    llm = os.getenv('MODEL_CHOICE', 'gpt-4o-mini')
    base_url = os.getenv('BASE_URL', 'https://api.openai.com/v1')
    api_key = os.getenv('LLM_API_KEY', 'no-api-key-provided')

    model = OpenAIModel(
        llm,
        provider=OpenAIProvider(
            base_url=base_url,
            api_key=api_key
        )
    )

    return model


async def get_pydantic_ai_agent():
    '''Get the Pydantic AI agent with MCP tools'''
    client = mcp_client.MCPClient()
    client.load_servers(str(CONFIG_FILE))
    tools = await client.start()
    return client, Agent(model=get_model(), tools=tools)


async def main():
    '''Main Function with CLI Chat '''
    print("=== Pydantic AI MCP CLI Chat ===")
    print("Type 'exit' to quit the chat")

    # Initialize the agent and message history
    client, mcp_agent = await get_pydantic_ai_agent()
    console = Console()
    messages = []

    try:
        while True:
            # Get user input
            user_input = input("\n[You] ")

            # Check if user wants to exit
            if user_input.lower() in ['exit', 'quit', 'bye', 'goodbye']:
                print("Goodbye!")
                break

            try:
                # Process the user input and output the response
                print("\n[Assistant]")
                with Live(
                    '', console=console, vertical_overflow='visible'
                ) as live:
                    async with mcp_agent.run_stream(
                        user_input, message_history=messages
                    ) as result:
                        curr_message = ""
                        async for message in result.stream_text(delta=True):
                            curr_message += message
                            live.update(Markdown(curr_message))

                    # Add the new messages to the chat history
                    messages.extend(result.all_messages())

            except Exception as e:
                logging.error("An error occurred: %s", str(e))
                raise
    finally:
        # Ensure proper cleanup of MCP client resources when exiting
        await client.cleanup()

if __name__ == "__main__":
    asyncio.run(main())
