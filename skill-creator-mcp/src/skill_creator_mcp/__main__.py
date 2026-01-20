"""STDIO 传输入口点（本地开发）.

这是用于本地开发的主入口点，通过 STDIO 与 Claude Code 通信。
"""

from .server import mcp

if __name__ == "__main__":
    mcp.run()
