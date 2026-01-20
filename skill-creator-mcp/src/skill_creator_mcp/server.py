"""Skill Creator MCP Server.

这是一个基于 FastMCP SDK 开发的 MCP Server，用于创建、验证、
分析和重构 Agent-Skills。
"""

from fastmcp import FastMCP

# 创建 MCP Server
mcp = FastMCP(
    name="skill-creator",
    instructions="""
    Skill Creator MCP Server - Agent-Skills 开发工具

    这个服务器提供创建、验证、分析和重构 Agent-Skills 的工具。

    ## TODO: 添加更多工具说明

    当前处于开发阶段，工具和资源正在逐步实现中。
    """
)

# TODO: 注册 Tools
# mcp.add_tool(init_skill_tool)
# mcp.add_tool(validate_skill_tool)
# mcp.add_tool(analyze_skill_tool)
# mcp.add_tool(refactor_skill_tool)
# mcp.add_tool(package_skill_tool)

# TODO: 注册 Resources
# mcp.add_resource(templates_resource)
# mcp.add_resource(best_practices_resource)
# mcp.add_resource(validation_rules_resource)

# TODO: 注册 Prompts
# mcp.add_prompt(create_skill_prompt)
# mcp.add_prompt(validate_skill_prompt)
# mcp.add_prompt(refactor_skill_prompt)

# 创建服务器实例
server = mcp.get_server()


__all__ = ["mcp", "server"]
