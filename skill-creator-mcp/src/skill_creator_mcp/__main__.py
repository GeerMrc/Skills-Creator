"""STDIO 传输入口点（本地开发）.

这是用于本地开发的主入口点，通过 STDIO 与 Claude Code 通信。

使用方式：
    uv run python -m skill_creator_mcp

或在 Claude Code 配置中：
    {
        "mcpServers": {
            "skill-creator": {
                "command": "uv",
                "args": ["--directory", "/path/to/skill-creator-mcp", "run", "python", "-m", "skill_creator_mcp"]
            }
        }
    }
"""

import sys

from .server import mcp


def main() -> int:
    """启动 MCP Server (STDIO 模式).

    FastMCP 的 run() 方法会自动处理 STDIO 传输协议。
    这是同步入口点，内部会处理异步循环。

    Returns:
        退出码（0 表示成功，非 0 表示错误）
    """
    try:
        # FastMCP.run() 会自动检测 STDIO 环境并运行服务器
        # 这是一个同步方法，内部处理异步事件循环
        mcp.run()  # type: ignore[func-returns-value]
        return 0
    except KeyboardInterrupt:
        # 用户中断（Ctrl+C）
        return 130
    except Exception as e:
        # 其他异常
        print(f"Error: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
