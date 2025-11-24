import asyncio
import logging
from typing import List, Dict, Any, Optional
from contextlib import AsyncExitStack

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

logger = logging.getLogger(__name__)

class MCPClient:
    def __init__(self, config: Dict[str, Any]):
        """
        Initialize the MCP Client with configuration.
        
        Args:
            config: Dictionary containing 'mcp_servers' configuration.
        """
        self.config = config
        self.sessions: Dict[str, ClientSession] = {}
        self.exit_stack = AsyncExitStack()
        self.tools: List[Dict[str, Any]] = []

    async def start(self):
        """
        Start connections to all configured MCP servers.
        """
        servers_config = self.config.get("mcp_servers", {})
        
        for server_name, server_conf in servers_config.items():
            if not server_conf.get("enabled", False):
                continue
                
            logger.info(f"Connecting to MCP server: {server_name}")
            
            command = server_conf.get("command")
            args = server_conf.get("args", [])
            env = server_conf.get("env", None)
            
            try:
                server_params = StdioServerParameters(
                    command=command,
                    args=args,
                    env=env
                )
                
                # Connect to the server
                read, write = await self.exit_stack.enter_async_context(
                    stdio_client(server_params)
                )
                
                session = await self.exit_stack.enter_async_context(
                    ClientSession(read, write)
                )
                
                await session.initialize()
                self.sessions[server_name] = session
                logger.info(f"Connected to {server_name}")
                
            except Exception as e:
                logger.error(f"Failed to connect to MCP server {server_name}: {e}")

        await self.refresh_tools()

    async def refresh_tools(self):
        """
        Query all connected servers for their tools and aggregate them.
        """
        self.tools = []
        for name, session in self.sessions.items():
            try:
                result = await session.list_tools()
                # Add a 'server' field to each tool to know where to route the call
                for tool in result.tools:
                    tool_dict = tool.model_dump()
                    tool_dict["server"] = name
                    self.tools.append(tool_dict)
            except Exception as e:
                logger.error(f"Failed to list tools for {name}: {e}")
        
        logger.info(f"Discovered {len(self.tools)} tools across {len(self.sessions)} servers.")

    async def call_tool(self, server_name: str, tool_name: str, arguments: Dict[str, Any]) -> Any:
        """
        Call a specific tool on a specific server.
        """
        if server_name not in self.sessions:
            raise ValueError(f"Server {server_name} not connected")
            
        session = self.sessions[server_name]
        result = await session.call_tool(tool_name, arguments)
        return result

    async def stop(self):
        """
        Close all connections.
        """
        await self.exit_stack.aclose()
