import asyncio

from mcp.server import Server
from mcp.types import ListToolsResult, CallToolResult, CallToolRequestParams, TextContent
from mcp.server.stdio import stdio_server
from mcp.types import Tool as MCPTool

from pwsh_agent.tools.base import Tool
from pwsh_agent.tools.registry import register_tools

register_tools()

async def list_tools(ctx, params) -> ListToolsResult:
    return ListToolsResult(
        tools=[
            MCPTool(name=tool.name, description=tool.description, input_schema=tool.input_schema)
            for tool in Tool.registry.values()
        ]
    )


async def call_tool(ctx, params: CallToolRequestParams) -> CallToolResult:
    tool = Tool.get(params.name)
    if not tool:
        return CallToolResult(
            content=[
                TextContent(
                    text=(f"Tool '{params.name}' not found.")
                )
            ],
            is_error=True
        )
    result = tool.execute(**(params.arguments or {}))
    return CallToolResult(
        content=[
            TextContent(
                text=result.json
            )
        ]
    )


server = Server(
    name="powershell-mcp-agent",
    on_list_tools=list_tools,
    on_call_tool=call_tool,
)


async def run():
    async with stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            server.create_initialization_options()
        )


if __name__ == "__main__":
    asyncio.run(run())