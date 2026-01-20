"""STDIO 传输入口点（本地开发）.

这是用于本地开发的主入口点，通过 STDIO 与 Claude Code 通信。
"""

import asyncio

from .server import mcp


async def main() -> None:
    """启动 STDIO 服务器."""
    from mcp.server.stdio import stdio_server

    async with stdio_server() as (read_stream, write_stream):
        await mcp.run(
            read_stream,
            write_stream,
            mcp.get_server_initialization_options(),
        )


if __name__ == "__main__":
    asyncio.run(main())
