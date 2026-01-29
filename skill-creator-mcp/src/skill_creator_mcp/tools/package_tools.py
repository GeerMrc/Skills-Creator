"""打包工具模块.

包含打包 Agent-Skill 的 MCP 工具函数。

合并后的统一打包工具，支持通用和Agent-Skill标准两种模式。
"""

import warnings
from typing import Any

from fastmcp import Context, FastMCP


async def package_skill(
    ctx: Context,
    mcp: FastMCP,
    skill_path: str,
    output_dir: str | None = None,
    version: str | None = None,
    format: str = "zip",
    include_tests: bool = False,
    strict: bool = False,
    validate_before_package: bool = True,
) -> dict[str, Any]:
    """
    打包 Agent-Skill 为分发格式.

    这是统一的打包工具，支持两种模式：
    - strict=False (默认): 通用打包模式，使用灵活排除模式
    - strict=True: Agent-Skill标准打包模式，使用严格排除模式，支持version参数

    Args:
        ctx: MCP 上下文
        mcp: FastMCP 实例
        skill_path: 技能目录路径
        output_dir: 输出目录路径（可选，优先级：参数 > 环境变量 SKILL_CREATOR_OUTPUT_DIR > 默认值）
        version: 版本号（可选，格式如 "0.3.1"，仅在strict=True时使用）
        format: 打包格式（zip/tar.gz/tar.bz2，默认：zip）
        include_tests: 是否包含测试文件（默认：False）
        strict: 是否使用Agent-Skill标准打包模式（默认：False）
        validate_before_package: 打包前是否验证（默认：True）

    Returns:
        包含打包结果的字典

    Examples:
        >>> # 通用打包模式
        >>> await package_skill(ctx, mcp, skill_path="/path/to/skill", format="zip")
        >>>
        >>> # Agent-Skill标准打包模式（带版本号）
        >>> await package_skill(ctx, mcp, skill_path="/path/to/skill",
        ...                      version="0.3.1", strict=True)
        >>> # 生成: skill-v0.3.1.zip
    """
    from pydantic import ValidationError

    from ..config import get_config
    from ..models.skill_config import PackageSkillInput
    from ..utils.packagers import (
        package_agent_skill as package_agent_skill_impl,
    )
    from ..utils.packagers import package_skill as package_skill_impl

    try:
        # 优先级：工具参数 > 环境变量 > 默认值
        config = get_config()
        if output_dir is None:
            output_dir = str(config.output_dir)

        # 根据strict参数选择打包方式
        if strict:
            # Agent-Skill标准打包模式
            # 验证version参数
            if version is None:
                return {
                    "success": False,
                    "error": "strict模式需要version参数",
                    "error_type": "validation_error",
                }

            from ..models.skill_config import PackageAgentSkillInput

            agent_skill_input_data = PackageAgentSkillInput.model_validate(
                {
                    "skill_path": skill_path,
                    "output_dir": output_dir,
                    "version": version,
                    "format": format,
                    "include_tests": include_tests,
                    "validate_before_package": validate_before_package,
                }
            )

            result = package_agent_skill_impl(
                skill_path=agent_skill_input_data.skill_path,
                output_dir=agent_skill_input_data.output_dir,
                version=agent_skill_input_data.version,
                package_format=agent_skill_input_data.format,
                include_tests=agent_skill_input_data.include_tests,
                validate_before_package=agent_skill_input_data.validate_before_package,
            )
        else:
            # 通用打包模式
            input_data = PackageSkillInput.model_validate(
                {
                    "skill_path": skill_path,
                    "output_dir": output_dir,
                    "format": format,
                    "include_tests": include_tests,
                    "validate_before_package": validate_before_package,
                }
            )

            result = package_skill_impl(
                skill_path=input_data.skill_path,
                output_dir=input_data.output_dir,
                package_format=input_data.format,
                include_tests=input_data.include_tests,
                validate_before_package=input_data.validate_before_package,
            )

        # 转换为字典格式返回
        return {
            "success": result.success,
            "skill_path": result.skill_path,
            "package_path": result.package_path,
            "format": result.format,
            "files_included": result.files_included,
            "package_size": result.package_size,
            "validation_passed": result.validation_passed,
            "validation_errors": result.validation_errors,
            "error": result.error,
            "error_type": result.error_type,
        }

    except ValidationError as e:
        # 检查是否是 format 字段的验证错误
        errors = e.errors()
        for error in errors:
            if error.get("loc") == ("format",):
                return {
                    "success": False,
                    "error": f"无效的打包格式: {format}",
                    "error_type": "format_error",
                }
        # 其他验证错误
        return {
            "success": False,
            "error": f"输入验证失败: {e}",
            "error_type": "validation_error",
        }
    except Exception as e:
        return {
            "success": False,
            "error": f"打包过程出错: {e}",
            "error_type": "internal_error",
        }


async def package_agent_skill(
    ctx: Context,
    mcp: FastMCP,
    skill_path: str,
    output_dir: str | None = None,
    version: str | None = None,
    format: str = "zip",
    include_tests: bool = False,
    validate_before_package: bool = True,
) -> dict[str, Any]:
    """
    打包 Agent-Skill 为标准分发格式 (已弃用).

    .. deprecated::
        此函数已弃用，请使用 package_skill 并设置 strict=True 和 version 参数。

    这是专门用于打包标准 Agent-Skill 的函数。
    与 package_skill 的区别：
    - 使用更严格的排除模式
    - 支持版本号参数，生成标准化包名
    - 默认不包含测试文件
    - 确保符合 Agent-Skill 规范

    Args:
        ctx: MCP 上下文
        mcp: FastMCP 实例
        skill_path: Agent-Skill 目录路径
        output_dir: 输出目录路径（可选，优先级：参数 > 环境变量 SKILL_CREATOR_OUTPUT_DIR > 默认值）
        version: 版本号（可选，格式如 "0.3.1"）
        format: 打包格式（zip/tar.gz/tar.bz2）
        include_tests: 是否包含测试文件（默认 False）
        validate_before_package: 打包前是否验证

    Returns:
        包含打包结果的字典

    Examples:
        >>> result = await package_agent_skill(
        ...     ctx,
        ...     mcp,
        ...     skill_path="/path/to/skill-creator",
        ...     output_dir="/output",
        ...     version="0.3.1",
        ...     format="zip"
        ... )
        >>> # 生成: skill-creator-v0.3.1.zip
    """
    # 发出弃用警告
    warnings.warn(
        "package_agent_skill 已弃用，请使用 package_skill 并设置 strict=True 和 version 参数。",
        DeprecationWarning,
        stacklevel=2,
    )

    # 委托给新的统一接口
    return await package_skill(
        ctx=ctx,
        mcp=mcp,
        skill_path=skill_path,
        output_dir=output_dir,
        version=version,
        format=format,
        include_tests=include_tests,
        strict=True,
        validate_before_package=validate_before_package,
    )


__all__ = ["package_skill", "package_agent_skill"]
