'''Interact with MCP server using HTTP requests.'''
import os
import asyncio
from typing import Any
from dotenv import load_dotenv
from fastmcp import Client

from pydantic_ai.models.openai import OpenAIModel
from pydantic_ai.providers.openai import OpenAIProvider
from pydantic_ai import RunContext, Tool as PydanticTool
from pydantic_ai.tools import ToolDefinition
from pydantic_ai import Agent

from mcp.types import Tool as MCPTool

load_dotenv()
mcp_url = os.getenv('MCP_URL', 'http://localhost:9000/mcp/')
stream_client = Client(mcp_url)


# Print existing tools
async def use_streamable_http_client(client):
    '''Use the Streamable HTTP client to list tools'''
    async with client:
        tools = await client.list_tools()
        print(f"Connected via Streamable HTTP, found tools: {tools}")


# create an agent with the MCP tools
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


def create_tool_instance(tool: MCPTool, client) -> PydanticTool:
    """Initialize a Pydantic AI Tool from an MCP Tool."""
    async def execute_tool(**kwargs: Any) -> Any:
        return await client.call_tool(tool.name, arguments=kwargs)

    async def prepare_tool(
            _ctx: RunContext,
            tool_def: ToolDefinition) -> ToolDefinition | None:
        tool_def.parameters_json_schema = tool.inputSchema
        return tool_def

    return PydanticTool(
        execute_tool,
        name=tool.name,
        description=tool.description or "",
        takes_ctx=False,
        prepare=prepare_tool
    )


async def mcp_agent(query: str) -> str:
    '''Get the Pydantic AI agent with MCP tools'''
    client = stream_client
    async with client:
        tools = await client.list_tools()
        pyd_tools = [create_tool_instance(tool, client) for tool in tools]
        agent = Agent(model=get_model(), tools=pyd_tools)
        result = await agent.run(query)
        return result


if __name__ == "__main__":
    response = asyncio.run(mcp_agent(
        "Find latest news about Vibe coding AI developments?"))
    print(response)
