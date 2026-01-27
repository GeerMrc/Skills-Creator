"""批量操作工具模块.

包含批量操作的 MCP 工具函数。
"""

from typing import Any

from fastmcp import Context
from fastmcp import FastMCP


async def batch_validate_skills_tool(
    ctx: Context,
    mcp: FastMCP,
    skill_paths: list[str],
    check_structure: bool = True,
    check_content: bool = True,
    concurrent_limit: int = 5,
) -> dict[str, Any]:
    """批量验证多个Agent-Skill.

    并发验证多个技能的结构和内容，提高验证效率。

    Args:
        ctx: MCP 上下文
        mcp: FastMCP 实例
        skill_paths: 技能目录路径列表
        check_structure: 是否检查目录结构（默认 True）
        check_content: 是否检查内容格式（默认 True）
        concurrent_limit: 并发限制（默认 5）

    Returns:
        包含批量验证结果的字典，包括每个技能的验证结果和汇总信息
    """
    from .batch_operations import batch_validate_skills

    try:
        result = await batch_validate_skills(
            skill_paths=skill_paths,
            check_structure=check_structure,
            check_content=check_content,
            concurrent_limit=concurrent_limit,
        )
        return {
            "success": True,
            "results": result.results,
            "summary": result.summary,
        }
    except Exception as e:
        return {
            "success": False,
            "error": f"批量验证出错: {e}",
            "error_type": "internal_error",
        }


async def batch_analyze_skills_tool(
    ctx: Context,
    mcp: FastMCP,
    skill_paths: list[str],
    analyze_structure: bool = True,
    analyze_complexity: bool = True,
    analyze_quality: bool = True,
    concurrent_limit: int = 5,
) -> dict[str, Any]:
    """批量分析多个Agent-Skill.

    并发分析多个技能的代码质量、复杂度和结构。

    Args:
        ctx: MCP 上下文
        mcp: FastMCP 实例
        skill_paths: 技能目录路径列表
        analyze_structure: 是否分析代码结构（默认 True）
        analyze_complexity: 是否分析代码复杂度（默认 True）
        analyze_quality: 是否分析代码质量（默认 True）
        concurrent_limit: 并发限制（默认 5）

    Returns:
        包含批量分析结果的字典，包括每个技能的分析结果和汇总信息
    """
    from .batch_operations import batch_analyze_skills

    try:
        result = await batch_analyze_skills(
            skill_paths=skill_paths,
            analyze_structure=analyze_structure,
            analyze_complexity=analyze_complexity,
            analyze_quality=analyze_quality,
            concurrent_limit=concurrent_limit,
        )
        return {
            "success": True,
            "results": result.results,
            "summary": result.summary,
        }
    except Exception as e:
        return {
            "success": False,
            "error": f"批量分析出错: {e}",
            "error_type": "internal_error",
        }


__all__ = ["batch_validate_skills_tool", "batch_analyze_skills_tool"]
