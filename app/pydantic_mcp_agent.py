'''MCP Agent for Pydantic AI'''
import os
import pathlib
from dotenv import load_dotenv
import logfire


from pydantic_ai.models.openai import OpenAIModel
from pydantic_ai.providers.openai import OpenAIProvider
from pydantic_ai import Agent

import mcp_client

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
    return Agent(model=get_model(), tools=tools)
