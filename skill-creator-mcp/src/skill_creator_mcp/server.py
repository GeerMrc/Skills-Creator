"""Skill Creator MCP Server.

这是一个基于 FastMCP SDK 开发的 MCP Server，用于创建、验证、
分析和重构 Agent-Skills。
"""

import json
from pathlib import Path
from typing import Any

from fastmcp import Context, FastMCP

from .prompts import (
    get_create_skill_prompt,
    get_refactor_skill_prompt,
    get_validate_skill_prompt,
)
from .resources import (
    get_best_practices,
    get_template_content,
    get_validation_rules,
    list_templates,
)
from .utils.analyzers import (
    _analyze_complexity,
    _analyze_quality,
    _analyze_structure,
    _generate_analysis_summary,
    _generate_suggestions,
)
from .utils.file_ops import create_directory_structure_async, write_file_async
from .utils.packagers import package_skill as package_skill_impl
from .utils.refactorors import (
    estimate_refactor_effort,
    generate_refactor_report,
    generate_refactor_suggestions,
)
from .utils.validators import (
    _validate_naming,
    _validate_skill_md,
    _validate_structure,
    _validate_template_requirements,
)

# 创建 MCP Server
mcp = FastMCP(
    name="skill-creator",
    instructions="""
    Skill Creator MCP Server - Agent-Skills 开发工具

    这个服务器提供创建、验证、分析、重构和打包 Agent-Skills 的工具。

    ## 可用工具

    ### init_skill
    初始化新的 Agent-Skill。

    参数：
    - name (str): 技能名称（小写字母、数字、连字符，1-64字符）
    - template (str): 模板类型（minimal/tool-based/workflow-based/analyzer-based）
    - output_dir (str): 输出目录路径
    - with_scripts (bool): 是否包含示例脚本
    - with_examples (bool): 是否包含使用示例

    ### validate_skill
    验证 Agent-Skill 的结构和内容。

    参数：
    - skill_path (str): 技能目录路径
    - check_structure (bool): 是否检查目录结构（默认 True）
    - check_content (bool): 是否检查内容格式（默认 True）

    ### analyze_skill
    分析 Agent-Skill 的代码质量、复杂度和结构。

    参数：
    - skill_path (str): 技能目录路径
    - analyze_structure (bool): 是否分析代码结构（默认 True）
    - analyze_complexity (bool): 是否分析代码复杂度（默认 True）
    - analyze_quality (bool): 是否分析代码质量（默认 True）

    ### refactor_skill
    生成 Agent-Skill 的重构建议。

    参数：
    - skill_path (str): 技能目录路径
    - focus (list[str]): 重点关注领域（可选，如 structure、documentation、testing）
    - analyze_structure (bool): 是否分析代码结构（默认 True）
    - analyze_complexity (bool): 是否分析代码复杂度（默认 True）
    - analyze_quality (bool): 是否分析代码质量（默认 True）

    ### package_skill
    打包 Agent-Skill 为分发格式。

    参数：
    - skill_path (str): 技能目录路径
    - output_dir (str): 输出目录路径（默认：当前目录）
    - format (str): 打包格式（zip/tar.gz/tar.bz2，默认：zip）
    - include_tests (bool): 是否包含测试文件（默认：True）
    - validate_before_package (bool): 打包前是否验证（默认：True）
    """,
)


@mcp.tool()
async def init_skill(
    ctx: Context,
    name: str,
    template: str = "minimal",
    output_dir: str = ".",
    with_scripts: bool = False,
    with_examples: bool = False,
) -> dict[str, Any]:
    """
    初始化新的 Agent-Skill.

    创建符合规范的技能目录结构和模板文件。

    Args:
        ctx: MCP 上下文
        name: 技能名称（小写字母、数字、连字符，1-64字符）
        template: 模板类型（minimal/tool-based/workflow-based/analyzer-based）
        output_dir: 输出目录路径
        with_scripts: 是否包含示例脚本
        with_examples: 是否包含使用示例

    Returns:
        包含创建结果的字典
    """
    from .models.skill_config import InitSkillInput

    try:
        # 使用 Pydantic model_validate 方法进行输入验证
        # 这种方法可以处理类型转换和验证，避免静态类型检查错误
        input_data = InitSkillInput.model_validate(
            {
                "name": name,
                "template": template,
                "output_dir": output_dir,
                "with_scripts": with_scripts,
                "with_examples": with_examples,
            }
        )

        # 使用验证后的数据
        skill_dir = await create_directory_structure_async(
            name=input_data.name,
            template_type=input_data.template,
            output_dir=Path(input_data.output_dir),
        )

        # 3. 生成 SKILL.md 内容
        skill_md_content = _generate_skill_md_content(input_data.name, input_data.template)
        await write_file_async(
            skill_dir / "SKILL.md",
            skill_md_content,
        )

        # 4. 创建引用文件（非 minimal 模板）
        if input_data.template != "minimal":
            await _create_reference_files(skill_dir, input_data.template)

        # 5. 创建示例脚本
        if input_data.with_scripts:
            await _create_example_scripts(skill_dir)

        # 6. 创建使用示例
        if input_data.with_examples:
            await _create_example_examples(skill_dir, input_data.name)

        return {
            "success": True,
            "skill_path": str(skill_dir),
            "skill_name": input_data.name,
            "template": input_data.template,
            "message": f"技能 '{input_data.name}' 已创建在：{skill_dir}",
            "next_steps": [
                f"1. 编辑 {skill_dir / 'SKILL.md'} 完善技能描述",
                f"2. 运行验证：python scripts/validate.py {skill_dir}",
            ],
        }

    except ValueError as e:
        return {
            "success": False,
            "error": str(e),
            "error_type": "validation_error",
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "error_type": "internal_error",
        }


@mcp.tool()
async def validate_skill(
    ctx: Context,
    skill_path: str,
    check_structure: bool = True,
    check_content: bool = True,
) -> dict[str, Any]:
    """
    验证 Agent-Skill 的结构和内容.

    Args:
        ctx: MCP 上下文
        skill_path: 技能目录路径
        check_structure: 是否检查目录结构
        check_content: 是否检查内容格式

    Returns:
        包含验证结果的字典（Pydantic 模型的 JSON 序列化）
    """
    from .models.skill_config import ValidateSkillInput, ValidationResult

    try:
        # 使用 Pydantic 验证输入参数
        input_data = ValidateSkillInput.model_validate(
            {
                "skill_path": skill_path,
                "check_structure": check_structure,
                "check_content": check_content,
            }
        )

        skill_dir = Path(input_data.skill_path)

        # 初始化结果
        errors = []
        warnings = []
        checks = {}
        template_type = None
        skill_name = skill_dir.name

        # 检查目录是否存在
        if not skill_dir.exists():
            result = ValidationResult(
                valid=False,
                skill_path=skill_path,
                skill_name=skill_name,
                errors=[f"目录不存在: {skill_path}"],
                warnings=[],
                checks={},
            )
            return {"success": False, **result.model_dump()}

        if not skill_dir.is_dir():
            result = ValidationResult(
                valid=False,
                skill_path=skill_path,
                skill_name=skill_name,
                errors=[f"路径不是目录: {skill_path}"],
                warnings=[],
                checks={},
            )
            return {"success": False, **result.model_dump()}

        # 1. 检查目录结构
        if input_data.check_structure:
            structure_errors = _validate_structure(skill_dir)
            errors.extend(structure_errors)
            checks["structure"] = len(structure_errors) == 0

        # 2. 检查命名规范
        naming_errors = _validate_naming(skill_dir)
        errors.extend(naming_errors)
        checks["naming"] = len(naming_errors) == 0

        # 3. 检查内容格式
        if input_data.check_content:
            content_errors, content_warnings, detected_template = _validate_skill_md(skill_dir)
            errors.extend(content_errors)
            warnings.extend(content_warnings)
            checks["content"] = len(content_errors) == 0

            # 确保 template_type 类型正确
            if detected_template and detected_template in ("minimal", "tool-based", "workflow-based", "analyzer-based"):
                template_type = detected_template  # type: ignore[assignment]

            # 4. 检查模板特定要求
            if template_type:
                template_errors = _validate_template_requirements(skill_dir, template_type)
                errors.extend(template_errors)
                checks["template_requirements"] = len(template_errors) == 0

        # 判断验证是否通过
        valid = len(errors) == 0

        result = ValidationResult(
            valid=valid,
            skill_path=str(skill_dir),
            skill_name=skill_name,
            template_type=template_type,
            errors=errors,
            warnings=warnings,
            checks=checks,
        )

        return {"success": True, "message": "验证通过" if valid else f"验证失败，发现 {len(errors)} 个错误", **result.model_dump()}

    except Exception as e:
        result = ValidationResult(
            valid=False,
            skill_path=skill_path,
            errors=[f"验证过程出错: {e}"],
            warnings=[],
            checks={},
        )
        return {"success": False, "error_type": "internal_error", **result.model_dump()}


@mcp.tool()
async def analyze_skill(
    ctx: Context,
    skill_path: str,
    analyze_structure: bool = True,
    analyze_complexity: bool = True,
    analyze_quality: bool = True,
) -> dict[str, Any]:
    """
    分析 Agent-Skill 的代码质量和结构.

    Args:
        ctx: MCP 上下文
        skill_path: 技能目录路径
        analyze_structure: 是否分析代码结构
        analyze_complexity: 是否分析代码复杂度
        analyze_quality: 是否分析代码质量

    Returns:
        包含分析结果的字典
    """
    from .models.skill_config import (
        AnalyzeSkillInput,
        QualityScore,
    )

    try:
        # 使用 Pydantic 验证输入参数
        input_data = AnalyzeSkillInput.model_validate(
            {
                "skill_path": skill_path,
                "analyze_structure": analyze_structure,
                "analyze_complexity": analyze_complexity,
                "analyze_quality": analyze_quality,
            }
        )

        skill_dir = Path(input_data.skill_path)

        # 检查目录是否存在
        if not skill_dir.exists():
            return {
                "success": False,
                "error": f"目录不存在: {skill_path}",
                "error_type": "path_error",
            }

        if not skill_dir.is_dir():
            return {
                "success": False,
                "error": f"路径不是目录: {skill_path}",
                "error_type": "path_error",
            }

        # 1. 结构分析（异步）
        if input_data.analyze_structure:
            structure = await _analyze_structure(skill_dir)
        else:
            from .models.skill_config import StructureAnalysis

            structure = StructureAnalysis(total_files=0, total_lines=0, file_breakdown={})

        # 2. 复杂度分析（异步）
        if input_data.analyze_complexity:
            complexity = await _analyze_complexity(skill_dir)
        else:
            from .models.skill_config import ComplexityMetrics

            complexity = ComplexityMetrics(
                cyclomatic_complexity=None,
                maintainability_index=None,
                code_duplication=None,
            )

        # 3. 质量分析（异步）
        if input_data.analyze_quality:
            quality = await _analyze_quality(skill_dir)
        else:
            # 如果不分析质量，使用默认值
            quality = QualityScore(
                overall_score=0.0,
                structure_score=0.0,
                documentation_score=0.0,
                test_coverage_score=0.0,
            )

        # 4. 生成改进建议
        suggestions = _generate_suggestions(structure, complexity, quality)

        return {
            "success": True,
            "skill_path": str(skill_dir),
            "skill_name": skill_dir.name,
            "structure": {
                "total_files": structure.total_files,
                "total_lines": structure.total_lines,
                "file_breakdown": structure.file_breakdown,
            },
            "complexity": {
                "cyclomatic_complexity": complexity.cyclomatic_complexity,
                "maintainability_index": complexity.maintainability_index,
                "code_duplication": complexity.code_duplication,
            },
            "quality": {
                "overall_score": quality.overall_score,
                "structure_score": quality.structure_score,
                "documentation_score": quality.documentation_score,
                "test_coverage_score": quality.test_coverage_score,
            },
            "suggestions": suggestions,
            "summary": _generate_analysis_summary(quality, complexity),
        }

    except Exception as e:
        return {
            "success": False,
            "error": f"分析过程出错: {e}",
            "error_type": "internal_error",
        }


@mcp.tool()
async def refactor_skill(
    ctx: Context,
    skill_path: str,
    focus: list[str] | None = None,
    analyze_structure: bool = True,
    analyze_complexity: bool = True,
    analyze_quality: bool = True,
) -> dict[str, Any]:
    """
    生成 Agent-Skill 的重构建议.

    基于代码分析生成具体的重构建议，包括优先级、影响评估和工作量估算。

    Args:
        ctx: MCP 上下文
        skill_path: 技能目录路径
        focus: 重点关注领域（可选，如 structure、documentation、testing）
        analyze_structure: 是否分析代码结构
        analyze_complexity: 是否分析代码复杂度
        analyze_quality: 是否分析代码质量

    Returns:
        包含重构建议的字典
    """
    from .models.skill_config import RefactorSkillInput

    try:
        # 使用 Pydantic 验证输入参数
        input_data = RefactorSkillInput.model_validate(
            {
                "skill_path": skill_path,
                "focus": focus,
                "analyze_structure": analyze_structure,
                "analyze_complexity": analyze_complexity,
                "analyze_quality": analyze_quality,
            }
        )

        skill_dir = Path(input_data.skill_path)

        # 检查目录是否存在
        if not skill_dir.exists():
            return {
                "success": False,
                "error": f"目录不存在: {skill_path}",
                "error_type": "path_error",
            }

        if not skill_dir.is_dir():
            return {
                "success": False,
                "error": f"路径不是目录: {skill_path}",
                "error_type": "path_error",
            }

        # 1. 结构分析（异步）
        if input_data.analyze_structure:
            structure = await _analyze_structure(skill_dir)
        else:
            from .models.skill_config import StructureAnalysis

            structure = StructureAnalysis(total_files=0, total_lines=0, file_breakdown={})

        # 2. 复杂度分析（异步）
        if input_data.analyze_complexity:
            complexity = await _analyze_complexity(skill_dir)
        else:
            from .models.skill_config import ComplexityMetrics

            complexity = ComplexityMetrics(
                cyclomatic_complexity=None,
                maintainability_index=None,
                code_duplication=None,
            )

        # 3. 质量分析（异步）
        if input_data.analyze_quality:
            quality = await _analyze_quality(skill_dir)
        else:
            from .models.skill_config import QualityScore

            quality = QualityScore(
                overall_score=0.0,
                structure_score=0.0,
                documentation_score=0.0,
                test_coverage_score=0.0,
            )

        # 4. 生成重构建议
        suggestions = generate_refactor_suggestions(
            skill_dir, structure, complexity, quality, input_data.focus
        )

        # 5. 生成重构报告
        report = generate_refactor_report(
            str(skill_dir), structure, complexity, quality, suggestions
        )

        # 6. 估算工作量
        effort = estimate_refactor_effort(suggestions)

        return {
            "success": True,
            "skill_path": str(skill_dir),
            "skill_name": skill_dir.name,
            "structure": {
                "total_files": structure.total_files,
                "total_lines": structure.total_lines,
                "file_breakdown": structure.file_breakdown,
            },
            "complexity": {
                "cyclomatic_complexity": complexity.cyclomatic_complexity,
                "maintainability_index": complexity.maintainability_index,
                "code_duplication": complexity.code_duplication,
            },
            "quality": {
                "overall_score": quality.overall_score,
                "structure_score": quality.structure_score,
                "documentation_score": quality.documentation_score,
                "test_coverage_score": quality.test_coverage_score,
            },
            "suggestions": suggestions,
            "report": report,
            "effort_estimate": effort,
        }

    except Exception as e:
        return {
            "success": False,
            "error": f"重构分析出错: {e}",
            "error_type": "internal_error",
        }


@mcp.tool()
async def package_skill(
    ctx: Context,
    skill_path: str,
    output_dir: str = ".",
    format: str = "zip",
    include_tests: bool = True,
    validate_before_package: bool = True,
) -> dict[str, Any]:
    """
    打包 Agent-Skill 为分发格式.

    创建包含技能文件的压缩包，支持 zip、tar.gz 和 tar.bz2 格式。

    Args:
        ctx: MCP 上下文
        skill_path: 技能目录路径
        output_dir: 输出目录路径
        format: 打包格式（zip/tar.gz/tar.bz2）
        include_tests: 是否包含测试文件
        validate_before_package: 打包前是否验证

    Returns:
        包含打包结果的字典
    """
    from pydantic import ValidationError

    from .models.skill_config import PackageSkillInput

    try:
        # 使用 Pydantic 验证输入参数
        # 注意：format 是 Python 保留字，在模型中映射到 format 字段
        input_data = PackageSkillInput.model_validate(
            {
                "skill_path": skill_path,
                "output_dir": output_dir,
                "format": format,
                "include_tests": include_tests,
                "validate_before_package": validate_before_package,
            }
        )

        # 调用打包函数
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


# ==================== 需求收集相关常量 ====================


# 基础模式需求收集步骤（5步）
BASIC_REQUIREMENT_STEPS = [
    {
        "key": "skill_name",
        "title": "技能名称",
        "prompt": "请输入技能名称（小写字母、数字、连字符，如：pdf-parser、git-helper）",
        "validation": {
            "field": "skill_name",
            "required": True,
            "pattern": r"^[a-z0-9]+(?:-[a-z0-9]+)*$",
            "min_length": 1,
            "max_length": 64,
            "help_text": "技能名称只能包含小写字母、数字和连字符，不能以连字符开头或结尾",
        },
        "modes": ["basic", "complete", "brainstorm", "progressive"],
    },
    {
        "key": "skill_function",
        "title": "主要功能",
        "prompt": "请描述这个技能的主要功能是什么？",
        "validation": {
            "field": "skill_function",
            "required": True,
            "min_length": 10,
            "help_text": "请详细描述技能的主要功能，至少10个字符",
        },
        "modes": ["basic", "complete", "brainstorm", "progressive"],
    },
    {
        "key": "use_cases",
        "title": "使用场景",
        "prompt": "请描述这个技能的使用场景（至少2个）",
        "validation": {
            "field": "use_cases",
            "required": True,
            "min_length": 20,
            "help_text": "请提供至少2个具体的使用场景",
        },
        "modes": ["basic", "complete", "brainstorm", "progressive"],
    },
    {
        "key": "template_type",
        "title": "模板类型",
        "prompt": "选择技能模板类型：minimal（最小化）、tool-based（工具封装）、workflow-based（工作流）、analyzer-based（分析器）",
        "validation": {
            "field": "template_type",
            "required": True,
            "options": ["minimal", "tool-based", "workflow-based", "analyzer-based"],
            "help_text": "请选择一个有效的模板类型",
        },
        "modes": ["basic", "complete", "brainstorm", "progressive"],
    },
    {
        "key": "additional_features",
        "title": "额外需求",
        "prompt": "是否有其他额外功能需求？（可选）",
        "validation": {
            "field": "additional_features",
            "required": False,
            "help_text": "可选：描述任何额外功能需求",
        },
        "modes": ["basic", "complete", "brainstorm", "progressive"],
    },
]

# 完整模式额外步骤（5步）
COMPLETE_REQUIREMENT_STEPS = [
    {
        "key": "target_users",
        "title": "目标用户",
        "prompt": "这个技能的目标用户是谁？",
        "validation": {
            "field": "target_users",
            "required": True,
            "min_length": 10,
            "help_text": "请描述目标用户群体",
        },
        "modes": ["complete"],
    },
    {
        "key": "tech_stack",
        "title": "技术栈偏好",
        "prompt": "是否有技术栈偏好或限制？（可选）",
        "validation": {
            "field": "tech_stack",
            "required": False,
            "help_text": "可选：描述技术栈偏好",
        },
        "modes": ["complete"],
    },
    {
        "key": "dependencies",
        "title": "外部依赖",
        "prompt": "是否需要外部依赖或 API？（可选）",
        "validation": {
            "field": "dependencies",
            "required": False,
            "help_text": "可选：列出所需的外部依赖",
        },
        "modes": ["complete"],
    },
    {
        "key": "testing_requirements",
        "title": "测试要求",
        "prompt": "有什么特殊的测试要求？（可选）",
        "validation": {
            "field": "testing_requirements",
            "required": False,
            "help_text": "可选：描述测试要求",
        },
        "modes": ["complete"],
    },
    {
        "key": "documentation_level",
        "title": "文档级别",
        "prompt": "期望的文档详细程度？基础/标准/详细",
        "validation": {
            "field": "documentation_level",
            "required": False,
            "options": ["基础", "标准", "详细"],
            "help_text": "选择文档详细程度",
        },
        "modes": ["complete"],
    },
]


@mcp.tool()
async def collect_requirements(
    ctx: Context,
    action: str = "start",
    mode: str = "basic",
    session_id: str | None = None,
    user_input: str | None = None,
    use_elicit: bool = False,
) -> dict[str, Any]:
    """
    AI 驱动的需求澄清/收集工具.

    通过对话方式逐步收集创建 Agent-Skill 所需的关键信息。
    支持 session state 管理，可以中断后恢复。

    Args:
        ctx: MCP 上下文
        action: 执行动作（start=开始，next=下一步，previous=上一步，status=查询状态，complete=完成）
        mode: 收集模式（basic=基础5步，complete=完整10步，brainstorm=头脑风暴，progressive=渐进式）
        session_id: 会话ID（自动生成，用于多轮对话）
        user_input: 用户输入（用于 next/complete 动作，use_elicit=False 时使用）
        use_elicit: 是否使用 ctx.elicit() 自动收集输入（默认 False）。True 时会自动调用
                   ctx.elicit() 收集所有必需的输入，无需手动调用 action="next"。

    Returns:
        包含收集结果的字典

    Examples:
        传统模式（两步调用）:
            # 获取第一个问题
            result = await collect_requirements(ctx, action="start", mode="basic")
            # 提供答案并获取下一个问题
            result = await collect_requirements(ctx, action="next", user_input="my-skill")

        Elicit 模式（一步调用）:
            # 自动收集所有输入
            result = await collect_requirements(ctx, action="start", mode="basic", use_elicit=True)
    """
    from datetime import datetime
    from datetime import timezone as tz

    from .models.skill_config import (
        RequirementCollectionInput,
        RequirementStep,
        SessionState,
        ValidationRule,
    )

    try:
        # 1. 验证输入参数
        input_data = RequirementCollectionInput.model_validate(
            {
                "action": action,
                "mode": mode,
                "session_id": session_id,
                "user_input": user_input,
            }
        )

        # 2. 确定收集模式和处理方式
        is_dynamic_mode = input_data.mode in ("brainstorm", "progressive")

        # 对于动态模式，total_steps 设置为较大值表示开放式收集
        if is_dynamic_mode:
            total_steps = 100  # 开放式收集，没有固定步骤数
        else:
            # basic 或 complete 模式使用预定义步骤
            all_steps = BASIC_REQUIREMENT_STEPS.copy()
            if input_data.mode == "complete":
                all_steps.extend(COMPLETE_REQUIREMENT_STEPS)
            total_steps = len(all_steps)

        # 3. 处理会话ID
        current_session_id = (
            input_data.session_id or ctx.session_id or f"req_{datetime.now(tz.utc).isoformat()}"
        )

        # 4. 获取或创建会话状态
        state_data = await ctx.get_state(f"requirement_{current_session_id}")
        if state_data:
            session_state = SessionState.model_validate(state_data)
        else:
            session_state = SessionState(
                current_step_index=0,
                answers={},
                started_at=datetime.now(tz.utc).isoformat(),
                completed=False,
                mode=input_data.mode,
                total_steps=total_steps,
            )

        # 5. Elicit 模式：自动收集所有输入
        if use_elicit and input_data.action == "start":
            # 首先检测客户端是否支持 elicitation
            from .utils.capability_detection import check_elicitation_capability
            capability = await check_elicitation_capability(ctx)
            if not capability.get("supported"):
                return {
                    "success": False,
                    "error": "elicit_mode_not_supported",
                    "message": "当前 MCP 客户端不支持交互式输入模式 (use_elicit=True)。",
                    "fallback_mode": "traditional",
                    "traditional_usage": {
                        "step_1": "调用 collect_requirements(action='start', mode='basic')",
                        "step_2": "使用返回的 session_id 调用 collect_requirements(action='next', session_id='...', user_input='...')",
                        "step_3": "重复步骤 2 直到所有问题完成",
                        "example": {
                            "start": "collect_requirements(action='start', mode='basic')",
                            "next": "collect_requirements(action='next', session_id='req_xxx', user_input='my-skill')",
                        }
                    },
                    "capability_error": capability.get("error"),
                    "details": capability.get("details"),
                }
            return await _collect_with_elicit(
                ctx=ctx,
                session_state=session_state,
                current_session_id=current_session_id,
                is_dynamic_mode=is_dynamic_mode,
                all_steps=all_steps if not is_dynamic_mode else None,
                input_data=input_data,
            )

        # 6. 处理不同的 action
        if input_data.action == "status":
            return {
                "success": True,
                "session_id": current_session_id,
                "action": input_data.action,
                "mode": session_state.mode,
                "step_index": session_state.current_step_index,
                "total_steps": session_state.total_steps,
                "progress": (session_state.current_step_index / session_state.total_steps) * 100,
                "answers": session_state.answers,
                "completed": session_state.completed,
                "message": "会话状态查询成功",
                "is_dynamic_mode": is_dynamic_mode,
            }

        elif input_data.action == "previous":
            # 上一步
            if session_state.current_step_index > 0:
                session_state.current_step_index -= 1
                await ctx.set_state(f"requirement_{current_session_id}", session_state.model_dump())  # type: ignore[func-returns-value]

                # 对于动态模式，需要从会话历史恢复上一个问题
                if is_dynamic_mode:
                    # 简化处理：返回状态但不返回具体问题
                    # （历史问题保存在 _conversation_history 中，但 previous 操作不需要显示）
                    return {
                        "success": True,
                        "session_id": current_session_id,
                        "action": input_data.action,
                        "mode": session_state.mode,
                        "step_index": session_state.current_step_index,
                        "total_steps": session_state.total_steps,
                        "progress": (session_state.current_step_index / session_state.total_steps)
                        * 100,
                        "answers": session_state.answers,
                        "conversation_history": session_state.conversation_history,
                        "message": f"返回到第 {session_state.current_step_index + 1} 步（动态模式请继续提供新输入）",
                        "is_dynamic_mode": True,
                        "completed": False,
                    }

            # basic/complete 模式的原有逻辑（只有非动态模式才会执行到这里）
            if not is_dynamic_mode:
                current_step_data = all_steps[session_state.current_step_index]
                validation_data: dict[str, Any] = dict(current_step_data["validation"])  # type: ignore[arg-type]
                step = RequirementStep(
                    key=str(current_step_data["key"]),
                    title=str(current_step_data["title"]),
                    prompt=str(current_step_data["prompt"]),
                    validation=ValidationRule(**validation_data),
                )

                return {
                    "success": True,
                    "session_id": current_session_id,
                    "action": input_data.action,
                    "mode": session_state.mode,
                    "current_step": step.model_dump(),
                    "step_index": session_state.current_step_index,
                    "total_steps": session_state.total_steps,
                    "progress": (session_state.current_step_index / session_state.total_steps)
                    * 100,
                    "answers": session_state.answers,
                    "message": f"返回到步骤: {step.title}",
                    "completed": False,
                }
            else:
                return {
                    "success": False,
                    "session_id": current_session_id,
                    "action": input_data.action,
                    "error": "已经是第一步了",
                    "message": "无法返回上一步",
                }

        elif input_data.action == "start":
            # 开始新会话或重置
            session_state = SessionState(
                current_step_index=0,
                answers={},
                started_at=datetime.now(tz.utc).isoformat(),
                completed=False,
                mode=input_data.mode,
                total_steps=total_steps,
            )
            await ctx.set_state(f"requirement_{current_session_id}", session_state.model_dump())  # type: ignore[func-returns-value]

        # 6. 获取当前步骤或生成动态问题
        if is_dynamic_mode:
            # 动态模式：使用 LLM 生成问题
            if input_data.mode == "brainstorm":
                # 获取对话历史
                brainstorm_history: list[dict[str, str]] = session_state.conversation_history
                question_result = await _generate_brainstorm_question(
                    ctx, session_state.answers, brainstorm_history
                )

                return {
                    "success": True,
                    "session_id": current_session_id,
                    "action": input_data.action,
                    "mode": session_state.mode,
                    "step_index": session_state.current_step_index,
                    "total_steps": session_state.total_steps,
                    "progress": min(session_state.current_step_index * 5, 95),  # 动态模式的进度估算
                    "answers": session_state.answers,
                    "conversation_history": session_state.conversation_history,
                    "question": question_result.get("question", ""),
                    "is_dynamic_mode": True,
                    "is_llm_generated": question_result.get("is_dynamic", False),
                    "completed": False,
                    "message": f"Brainstorm 模式 - 问题 {session_state.current_step_index + 1}",
                }

            elif input_data.mode == "progressive":
                question_result = await _generate_progressive_question(ctx, session_state.answers)

                return {
                    "success": True,
                    "session_id": current_session_id,
                    "action": input_data.action,
                    "mode": session_state.mode,
                    "step_index": session_state.current_step_index,
                    "total_steps": session_state.total_steps,
                    "progress": min(session_state.current_step_index * 5, 95),
                    "answers": session_state.answers,
                    "question": question_result.get("next_question", ""),
                    "question_key": question_result.get("question_key", ""),
                    "is_dynamic_mode": True,
                    "is_llm_generated": question_result.get("is_dynamic", False),
                    "completed": False,
                    "message": f"Progressive 模式 - 问题 {session_state.current_step_index + 1}",
                }

        # 7. basic/complete 模式：获取预定义步骤（只在非动态模式执行）
        if not is_dynamic_mode:
            if session_state.current_step_index >= len(all_steps):
                # 所有步骤已完成
                session_state.completed = True
                await ctx.set_state(f"requirement_{current_session_id}", session_state.model_dump())  # type: ignore[func-returns-value]

                return {
                    "success": True,
                    "session_id": current_session_id,
                    "action": input_data.action,
                    "mode": session_state.mode,
                    "step_index": session_state.current_step_index,
                    "total_steps": session_state.total_steps,
                    "progress": 100.0,
                    "answers": session_state.answers,
                    "completed": True,
                    "message": "所有步骤已完成！可以使用 'complete' action 获取最终结果。",
                }

            current_step_data = all_steps[session_state.current_step_index]
            validation_data2: dict[str, Any] = dict(current_step_data["validation"])  # type: ignore[arg-type]
            current_step = RequirementStep(
                key=str(current_step_data["key"]),
                title=str(current_step_data["title"]),
                prompt=str(current_step_data["prompt"]),
                validation=ValidationRule(**validation_data2),
            )

        # 8. 处理用户输入（next/complete action）
        if input_data.action in ("next", "complete") and input_data.user_input:
            if is_dynamic_mode:
                # 动态模式：直接保存答案并继续
                # 保存用户输入
                answer_key = f"answer_{session_state.current_step_index}"
                session_state.answers[answer_key] = input_data.user_input

                # 更新对话历史（用于 brainstorm 模式）
                if input_data.mode == "brainstorm":
                    session_state.conversation_history.append({"role": "user", "content": input_data.user_input})

                # 移动到下一步
                if input_data.action == "next":
                    session_state.current_step_index += 1

                # 检查是否完成
                if input_data.action == "complete":
                    session_state.completed = True

                await ctx.set_state(f"requirement_{current_session_id}", session_state.model_dump())  # type: ignore[func-returns-value]

                # 如果完成，返回结果
                if session_state.completed:
                    return {
                        "success": True,
                        "session_id": current_session_id,
                        "action": input_data.action,
                        "mode": session_state.mode,
                        "step_index": session_state.current_step_index,
                        "total_steps": session_state.total_steps,
                        "progress": 100.0,
                        "answers": session_state.answers,
                        "conversation_history": session_state.conversation_history,
                        "completed": True,
                        "message": f"{input_data.mode.upper()} 模式需求收集完成！",
                        "is_dynamic_mode": True,
                    }
                else:
                    # 返回成功，等待用户继续
                    return {
                        "success": True,
                        "session_id": current_session_id,
                        "action": input_data.action,
                        "mode": session_state.mode,
                        "step_index": session_state.current_step_index,
                        "total_steps": session_state.total_steps,
                        "progress": min(session_state.current_step_index * 5, 95),
                        "answers": session_state.answers,
                        "conversation_history": session_state.conversation_history,
                        "message": "答案已保存，请继续使用 'next' action",
                        "is_dynamic_mode": True,
                    }
            else:
                # basic/complete 模式的原有验证逻辑
                validation_result = _validate_requirement_answer(
                    input_data.user_input,
                    current_step.validation,
                )

                if not validation_result["valid"]:
                    return {
                        "success": False,
                        "session_id": current_session_id,
                        "action": input_data.action,
                        "error": validation_result["error"],
                        "message": f"输入验证失败: {validation_result['error']}",
                    }

                # 保存答案
                session_state.answers[current_step.key] = input_data.user_input

                # 移动到下一步
                if input_data.action == "next":
                    session_state.current_step_index += 1

                # 检查是否完成
                if input_data.action == "complete" or session_state.current_step_index >= len(
                    all_steps
                ):
                    session_state.completed = True

                await ctx.set_state(f"requirement_{current_session_id}", session_state.model_dump())  # type: ignore[func-returns-value]

                # 如果完成，使用 LLM 生成总结
                if session_state.completed:
                    completeness_check = await _check_requirement_completeness(
                        ctx, session_state.answers
                    )

                    return {
                        "success": True,
                        "session_id": current_session_id,
                        "action": input_data.action,
                        "mode": session_state.mode,
                        "step_index": session_state.current_step_index,
                        "total_steps": session_state.total_steps,
                        "progress": 100.0,
                        "answers": session_state.answers,
                        "completed": True,
                        "is_complete": completeness_check["is_complete"],
                        "missing_info": completeness_check["missing_info"],
                        "suggestions": completeness_check["suggestions"],
                        "message": "需求收集完成！",
                    }

        # 9. 返回当前步骤信息（basic/complete 模式）
        # 对于动态模式，如果执行到这里，说明需要返回默认响应
        if is_dynamic_mode:
            return {
                "success": False,
                "error": "动态模式需要使用 'start' 或 'next' action",
                "message": "请使用 'start' 开始新会话，或使用 'next' 继续收集",
                "session_id": current_session_id,
            }

        if not is_dynamic_mode:
            progress = (session_state.current_step_index / session_state.total_steps) * 100

            return {
                "success": True,
                "session_id": current_session_id,
                "action": input_data.action,
                "mode": session_state.mode,
                "current_step": current_step.model_dump(),
                "step_index": session_state.current_step_index,
                "total_steps": session_state.total_steps,
                "progress": progress,
                "answers": session_state.answers,
                "completed": session_state.completed,
                "message": f"步骤 {session_state.current_step_index + 1}/{session_state.total_steps}: {current_step.title}",
            }

    except Exception as e:
        return {
            "success": False,
            "error": f"需求收集出错: {e}",
            "error_type": "internal_error",
            "message": f"内部错误: {e}",
        }


async def _collect_with_elicit(
    ctx: Context,
    session_state: Any,
    current_session_id: str,
    is_dynamic_mode: bool,
    all_steps: list[dict[str, Any]] | None,
    input_data: Any,
    max_retries: int = 3,
) -> dict[str, Any]:
    """使用 ctx.elicit() 自动收集所有用户输入.

    这是一个内部辅助函数，实现了完整的 elicit 循环逻辑：
    1. 生成或获取下一个问题
    2. 调用 ctx.elicit() 获取用户输入
    3. 验证输入
    4. 保存答案并继续，或重新请求输入（验证失败时）

    Args:
        ctx: MCP 上下文
        session_state: 会话状态对象
        current_session_id: 会话ID
        is_dynamic_mode: 是否为动态模式（brainstorm/progressive）
        all_steps: 预定义步骤列表（仅 basic/complete 模式）
        input_data: 输入数据对象
        max_retries: 验证失败时的最大重试次数

    Returns:
        包含收集结果的字典
    """
    from .models.skill_config import RequirementStep, ValidationRule

    try:
        # 重置会话状态（如果是重新开始）
        if session_state.current_step_index == 0 and not session_state.answers:
            await ctx.set_state(f"requirement_{current_session_id}", session_state.model_dump())  # type: ignore[func-returns-value]

        # 主收集循环
        while not session_state.completed:
            # 1. 获取当前问题
            if is_dynamic_mode:
                # 动态模式：使用 LLM 生成问题
                if input_data.mode == "brainstorm":
                    history: list[dict[str, str]] = session_state.conversation_history
                    question_result = await _generate_brainstorm_question(
                        ctx, session_state.answers, history
                    )
                    question_text = question_result.get("question", "")
                    prompt_text = question_text
                    validation = None  # 动态模式不使用固定验证规则
                    answer_key = f"answer_{session_state.current_step_index}"
                    step_title = f"Brainstorm 问题 {session_state.current_step_index + 1}"

                elif input_data.mode == "progressive":
                    question_result = await _generate_progressive_question(
                        ctx, session_state.answers
                    )
                    question_text = question_result.get("next_question", "")
                    prompt_text = question_text
                    validation = None
                    answer_key = question_result.get(
                        "question_key", f"answer_{session_state.current_step_index}"
                    )
                    step_title = f"Progressive 问题 {session_state.current_step_index + 1}"

                else:
                    return {
                        "success": False,
                        "error": f"未知的动态模式: {input_data.mode}",
                    }

            else:
                # 静态模式：使用预定义步骤
                if all_steps is None or session_state.current_step_index >= len(all_steps):
                    # 所有步骤已完成
                    session_state.completed = True
                    await ctx.set_state(
                        f"requirement_{current_session_id}", session_state.model_dump()
                    )  # type: ignore[func-returns-value]
                    break

                current_step_data = all_steps[session_state.current_step_index]
                validation_data: dict[str, Any] = dict(current_step_data["validation"])  # type: ignore[arg-type]
                step = RequirementStep(
                    key=str(current_step_data["key"]),
                    title=str(current_step_data["title"]),
                    prompt=str(current_step_data["prompt"]),
                    validation=ValidationRule(**validation_data),
                )

                prompt_text = step.prompt
                validation = step.validation
                answer_key = step.key
                step_title = step.title

            # 2. 调用 elicit 获取用户输入（带验证重试）
            user_answer = None
            retry_count = 0
            validation_error = None

            while retry_count <= max_retries:
                # 构建提示文本
                if validation_error and not is_dynamic_mode:
                    elicit_prompt = (
                        f"{prompt_text}\n\n⚠️ 输入验证失败: {validation_error}\n请重新输入："
                    )
                else:
                    elicit_prompt = f"{step_title}\n\n{prompt_text}"

                # 调用 elicit
                try:
                    result = await ctx.elicit(elicit_prompt)  # type: ignore[call-arg]

                    # 检查用户是否接受了输入请求
                    # FastMCP 返回 AcceptedElicitation | DeclinedElicitation | CancelledElicitation
                    if hasattr(result, "accepted") and not result.accepted:  # type: ignore[union-attr]
                        # 用户取消输入
                        await ctx.set_state(
                            f"requirement_{current_session_id}", session_state.model_dump()
                        )  # type: ignore[func-returns-value]
                        return {
                            "success": False,
                            "action": "cancelled",
                            "message": "用户取消了输入",
                            "session_id": current_session_id,
                            "step_index": session_state.current_step_index,
                            "answers": session_state.answers,
                            "conversation_history": session_state.conversation_history,
                            "progress": (
                                session_state.current_step_index / session_state.total_steps
                            )
                            * 100,
                        }

                    # 获取用户输入
                    user_answer = (
                        str(getattr(result, "data", "")) if hasattr(result, "data") else ""
                    )

                except Exception as e:
                    # elicit 调用失败，返回错误
                    await ctx.set_state(
                        f"requirement_{current_session_id}", session_state.model_dump()
                    )  # type: ignore[func-returns-value]
                    return {
                        "success": False,
                        "error": f"elicit 调用失败: {e}",
                        "session_id": current_session_id,
                        "message": f"获取用户输入时出错: {e}",
                    }

                # 3. 验证输入（仅非动态模式）
                if not is_dynamic_mode and validation:
                    validation_result = _validate_requirement_answer(user_answer, validation)
                    if not validation_result["valid"]:
                        validation_error = validation_result["error"]
                        retry_count += 1
                        continue

                # 验证通过或动态模式，退出重试循环
                break

            # 检查是否超过最大重试次数
            if retry_count > max_retries:
                return {
                    "success": False,
                    "error": "验证失败次数过多",
                    "message": f"输入验证失败超过 {max_retries} 次，请稍后重试",
                    "session_id": current_session_id,
                }

            # 4. 保存答案
            session_state.answers[answer_key] = user_answer  # type: ignore[index]

            # 更新对话历史（用于 brainstorm 模式）
            if is_dynamic_mode and input_data.mode == "brainstorm":
                session_state.conversation_history.append({"role": "user", "content": str(user_answer)})

            # 5. 移动到下一步
            session_state.current_step_index += 1

            # 6. 保存会话状态
            await ctx.set_state(f"requirement_{current_session_id}", session_state.model_dump())  # type: ignore[func-returns-value]

            # 7. 检查是否完成
            if is_dynamic_mode:
                # 动态模式：检查是否达到足够的轮次（这里使用简单计数，实际可以更智能）
                if session_state.current_step_index >= 5:  # 默认收集 5 轮
                    session_state.completed = True
            else:
                # 静态模式：检查是否完成所有步骤
                if session_state.current_step_index >= len(all_steps):  # type: ignore[arg-type]
                    session_state.completed = True

        # 8. 返回完成结果
        progress = (
            100.0
            if session_state.completed
            else (session_state.current_step_index / session_state.total_steps) * 100
        )

        return {
            "success": True,
            "session_id": current_session_id,
            "action": "complete",
            "mode": session_state.mode,
            "step_index": session_state.current_step_index,
            "total_steps": session_state.total_steps,
            "progress": progress,
            "answers": session_state.answers,
            "conversation_history": session_state.conversation_history,
            "completed": session_state.completed,
            "message": "需求收集完成（使用 elicit 模式）",
            "is_dynamic_mode": is_dynamic_mode,
        }

    except Exception as e:
        return {
            "success": False,
            "error": f"elicit 模式收集出错: {e}",
            "error_type": "elicit_error",
            "message": f"内部错误: {e}",
            "session_id": current_session_id,
        }


def _validate_requirement_answer(
    answer: str,
    validation: Any,
) -> dict[str, Any]:
    """验证需求收集的用户答案.

    Args:
        answer: 用户输入的答案
        validation: 验证规则（dict 或 ValidationRule 对象）

    Returns:
        包含验证结果的字典
    """
    import re

    # 提取验证字段
    field = validation.get("field") if isinstance(validation, dict) else validation.field
    required = validation.get("required") if isinstance(validation, dict) else validation.required
    min_length = (
        validation.get("min_length") if isinstance(validation, dict) else validation.min_length
    )
    max_length = (
        validation.get("max_length") if isinstance(validation, dict) else validation.max_length
    )
    options = validation.get("options") if isinstance(validation, dict) else validation.options
    pattern = validation.get("pattern") if isinstance(validation, dict) else validation.pattern
    help_text = (
        validation.get("help_text") if isinstance(validation, dict) else validation.help_text
    )

    # 检查必填
    if required and not answer.strip():
        return {
            "valid": False,
            "error": f"{field} 是必填项",
        }

    # 如果答案为空且非必填，直接通过
    if not answer.strip():
        return {"valid": True}

    # 检查长度
    if min_length and len(answer) < min_length:
        return {
            "valid": False,
            "error": help_text or f"最少需要 {min_length} 个字符",
        }

    if max_length and len(answer) > max_length:
        return {
            "valid": False,
            "error": help_text or f"最多允许 {max_length} 个字符",
        }

    # 检查选项
    if options:
        normalized_answer = answer.strip().lower()
        valid_options = [opt.lower() for opt in options]
        if normalized_answer not in valid_options:
            return {
                "valid": False,
                "error": f"无效的选项，请选择: {', '.join(options)}",
            }

    # 检查正则表达式
    if pattern:
        if not re.match(pattern, answer.strip()):
            return {
                "valid": False,
                "error": help_text or "格式不正确",
            }

    return {"valid": True}


async def _check_requirement_completeness(
    ctx: Context,
    answers: dict[str, str],
) -> dict[str, Any]:
    """使用 LLM 检查需求完整性.

    Args:
        ctx: MCP 上下文
        answers: 已收集的答案

    Returns:
        包含完整性检查结果的字典
    """

    try:
        prompt = f"""分析以下技能创建需求，判断是否包含所有必要信息：

已收集的信息：
{json.dumps(answers, indent=2, ensure_ascii=False)}

必要信息包括：
1. skill_name - 技能名称
2. skill_function - 主要功能
3. use_cases - 使用场景
4. template_type - 模板类型

请返回 JSON 格式，包含：
- is_complete: bool（是否完整）
- missing_info: list[str]（缺失的信息列表）
- suggestions: list[str]（补充建议列表）

只返回 JSON，不要其他内容。"""

        result = await ctx.sample(
            messages=prompt,
            system_prompt="你是一个技能创建顾问，负责评估需求的完整性。",
            temperature=0.3,
        )

        if result.text:
            try:
                # 提取 JSON 部分
                json_start = result.text.find("{")
                json_end = result.text.rfind("}") + 1
                if json_start >= 0 and json_end > json_start:
                    json_str = result.text[json_start:json_end]
                    parsed = json.loads(json_str)
                    return parsed  # type: ignore[no-any-return]
            except json.JSONDecodeError:
                pass

        # 默认返回（如果 LLM 解析失败）
        required_keys = ["skill_name", "skill_function", "use_cases", "template_type"]
        missing = [k for k in required_keys if k not in answers or not answers[k]]

        return {
            "is_complete": len(missing) == 0,
            "missing_info": missing,
            "suggestions": [] if len(missing) == 0 else ["请补充缺失的关键信息"],
        }

    except Exception:
        # 如果 LLM 调用失败，进行简单的完整性检查
        required_keys = ["skill_name", "skill_function", "use_cases", "template_type"]
        missing = [k for k in required_keys if k not in answers or not answers[k]]

        return {
            "is_complete": len(missing) == 0,
            "missing_info": missing,
            "suggestions": ["请补充缺失的关键信息"] if missing else [],
        }


async def _generate_brainstorm_question(
    ctx: Context,
    answers: dict[str, str],
    conversation_history: list[dict[str, str]] | None = None,
) -> dict[str, Any]:
    """使用 LLM 为 brainstorm 模式动态生成探索性问题.

    Args:
        ctx: MCP 上下文
        answers: 已收集的答案
        conversation_history: 对话历史记录

    Returns:
        包含生成问题的字典
    """
    try:
        # 构建上下文
        context_parts = []
        if answers:
            context_parts.append("已收集的信息:")
            for key, value in answers.items():
                context_parts.append(f"- {key}: {value}")

        if conversation_history:
            context_parts.append("\n之前的对话:")
            for msg in conversation_history[-4:]:  # 只保留最近4条
                context_parts.append(f"{msg.get('role', '')}: {msg.get('content', '')}")

        context = "\n".join(context_parts) if context_parts else "这是对话的开始。"

        # 生成探索性问题
        prompt = f"""你是一个技能创建顾问，正在帮助用户通过头脑风暴方式探索技能需求。

{context}

请生成一个开放性的探索性问题，帮助用户深入思考他们的技能需求。问题应该：
1. 基于已收集的信息进行深入
2. 探索用户可能未曾考虑的角度
3. 鼓励创造性思考
4. 避免重复已问过的内容

请只返回问题文本，不要其他内容。"""

        result = await ctx.sample(
            messages=prompt,
            system_prompt="You are a creative skill development consultant specializing in brainstorming and exploration.",
            temperature=0.8,  # 更高的温度以产生更多样化的问题
        )

        question = result.text.strip() if result.text else "请描述您希望这个技能实现什么独特价值？"

        return {
            "success": True,
            "question": question,
            "is_dynamic": True,
            "source": "llm_generated",
        }

    except Exception as e:
        # 降级到预定义问题
        fallback_questions = [
            "这个技能的核心价值主张是什么？",
            "它与现有解决方案有什么不同？",
            "用户最痛的场景是什么？",
            "您希望用户使用后有什么感受？",
        ]

        # 基于已收集答案数量选择问题
        index = min(len(answers), len(fallback_questions) - 1)

        return {
            "success": True,
            "question": fallback_questions[index],
            "is_dynamic": False,
            "source": "fallback",
            "error": str(e),
        }


async def _generate_progressive_question(
    ctx: Context,
    answers: dict[str, str],
) -> dict[str, Any]:
    """使用 LLM 为 progressive 模式生成针对性的下一个问题.

    Args:
        ctx: MCP 上下文
        answers: 已收集的答案

    Returns:
        包含生成问题的字典和问题类型
    """
    try:
        # 分析已收集的答案，确定下一个最相关的问题
        context = json.dumps(answers, indent=2, ensure_ascii=False)

        prompt = f"""分析以下已收集的技能需求信息，确定下一个应该询问的最相关问题。

已收集的信息：
{context}

可选问题类型（按优先级排序）：
1. 如果缺少 skill_name，询问技能名称
2. 如果缺少 skill_function，询问主要功能
3. 如果缺少 use_cases，询问使用场景
4. 如果缺少 template_type，询问模板类型
5. 如果基本信息齐全，询问更深入的问题（target_users, tech_stack 等）

请返回 JSON 格式：
{{
    "next_question": "具体的问题文本",
    "question_key": "问题标识（如 skill_name, skill_function 等）",
    "reasoning": "选择这个问题的原因"
}}"""

        result = await ctx.sample(
            messages=prompt,
            system_prompt="You are a skill requirements analyst. Determine the most relevant next question based on collected information.",
            temperature=0.3,
        )

        # 尝试解析 JSON
        import re

        json_match = re.search(r"\{.*\}", result.text or "", re.DOTALL)
        if json_match:
            try:
                parsed = json.loads(json_match.group())
                return {
                    "success": True,
                    "next_question": parsed.get("next_question", "请提供更多关于技能功能的细节？"),
                    "question_key": parsed.get("question_key", "follow_up"),
                    "reasoning": parsed.get("reasoning", ""),
                    "is_dynamic": True,
                }
            except json.JSONDecodeError:
                pass

        # 降级：根据答案数量选择基础问题
        basic_questions = [
            ("skill_name", "请提供技能名称（小写字母、数字、连字符）"),
            ("skill_function", "请描述这个技能的主要功能"),
            ("use_cases", "请描述这个技能的使用场景"),
            (
                "template_type",
                "选择技能模板类型：minimal、tool-based、workflow-based、analyzer-based",
            ),
        ]

        index = min(len(answers), len(basic_questions) - 1)
        key, question = basic_questions[index]

        return {
            "success": True,
            "next_question": question,
            "question_key": key,
            "is_dynamic": False,
            "source": "fallback",
        }

    except Exception as e:
        # 统一返回格式：即使异常也返回 success:True 和 fallback 问题
        # 这样与 brainstorm 模式行为一致
        basic_questions = [
            ("skill_name", "请提供技能名称（小写字母、数字、连字符）"),
            ("skill_function", "请描述这个技能的主要功能"),
            ("use_cases", "请描述这个技能的使用场景"),
            (
                "template_type",
                "选择技能模板类型：minimal、tool-based、workflow-based、analyzer-based",
            ),
        ]

        # 根据已收集答案数量选择问题
        index = min(len(answers), len(basic_questions) - 1)
        key, question = basic_questions[index]

        return {
            "success": True,  # 与 brainstorm 保持一致
            "next_question": question,
            "question_key": key,
            "is_dynamic": False,
            "source": "fallback",
            "error": str(e),  # 保留原始错误信息供调试
        }


# ============================================================================
# Phase 0: 技术验证工具
# 这些工具用于验证 FastMCP Context API 的可用性
# ============================================================================


@mcp.tool()
async def check_client_capabilities(ctx: Context) -> dict[str, Any]:
    """检测 MCP 客户端的能力支持情况.

    检测客户端是否支持高级 MCP 功能，如 sampling 和 elicitation。

    Returns:
        包含客户端能力检测结果的字典
    """
    from .utils.capability_detection import get_client_capabilities

    return await get_client_capabilities(ctx)


@mcp.tool()
async def test_llm_sampling(ctx: Context, prompt: str) -> dict[str, Any]:
    """测试 LLM Sampling 能力.

    验证 MCP Server 可以通过 ctx.sample() 调用客户端 LLM。

    Args:
        ctx: MCP 上下文
        prompt: 要发送给 LLM 的提示文本

    Returns:
        包含测试结果的字典，包括 LLM 响应文本和历史记录
    """
    try:
        result = await ctx.sample(
            messages=prompt,
            system_prompt="You are a helpful assistant for skill creation.",
            temperature=0.7,
        )

        return {
            "success": True,
            "test": "test_llm_sampling",
            "has_response": result.text is not None,
            "response_text": result.text or "",
            "has_history": result.history is not None,
            "history_length": len(result.history) if result.history else 0,
            "message": "LLM Sampling 能力验证通过",
        }
    except Exception as e:
        return {
            "success": False,
            "test": "test_llm_sampling",
            "error": str(e),
            "message": f"LLM Sampling 验证失败: {e}",
        }


@mcp.tool()
async def test_user_elicitation(
    ctx: Context, prompt: str = "请提供技能名称（小写字母、数字、连字符）"
) -> dict[str, Any]:
    """测试用户征询 (User Elicitation) 能力.

    验证可以通过 ctx.elicit() 请求用户输入结构化数据。

    Args:
        ctx: MCP 上下文
        prompt: 向用户显示的提示文本

    Returns:
        包含测试结果的字典
    """
    try:
        result = await ctx.elicit(prompt)  # type: ignore[call-arg]

        # FastMCP 返回 AcceptedElicitation | DeclinedElicitation | CancelledElicitation
        if hasattr(result, "accepted") and result.accepted:  # type: ignore[union-attr]
            return {
                "success": True,
                "test": "test_user_elicitation",
                "action": "accept",
                "user_input": str(getattr(result, "data", "")) if hasattr(result, "data") else "",
                "message": "User Elicitation 能力验证通过 - 用户接受了输入请求",
            }
        else:
            return {
                "success": True,
                "test": "test_user_elicitation",
                "action": "cancel",
                "message": "User Elicitation 能力验证通过 - 用户取消了输入请求",
            }
    except Exception as e:
        return {
            "success": False,
            "test": "test_user_elicitation",
            "error": str(e),
            "message": f"User Elicitation 验证失败: {e}",
        }


@mcp.tool()
async def test_conversation_loop(ctx: Context, user_input: str) -> dict[str, Any]:
    """测试对话循环和状态管理能力.

    验证可以在对话循环中使用 session state 保存历史，
    并且 LLM 可以利用对话历史生成更连贯的响应。

    Args:
        ctx: MCP 上下文
        user_input: 用户输入的文本

    Returns:
        包含测试结果的字典，包括 LLM 响应和会话状态
    """
    try:
        # 获取历史对话
        history_data = await ctx.get_state("test_conversation_history")
        history = list(history_data) if history_data else []

        # 添加用户输入
        history.append({"role": "user", "content": user_input})

        # 调用 LLM 生成响应
        result = await ctx.sample(
            messages=history,
            system_prompt="You are a skill creation consultant. Help users clarify their requirements.",
        )

        # 添加 AI 响应
        if result.text:
            history.append({"role": "assistant", "content": result.text})

        # 保存历史
        await ctx.set_state("test_conversation_history", history)  # type: ignore[func-returns-value]

        return {
            "success": True,
            "test": "test_conversation_loop",
            "has_llm_response": result.text is not None,
            "llm_response": result.text or "",
            "conversation_length": len(history),
            "history_saved": True,
            "message": "对话循环和状态管理验证通过",
        }
    except Exception as e:
        return {
            "success": False,
            "test": "test_conversation_loop",
            "error": str(e),
            "message": f"对话循环验证失败: {e}",
        }


@mcp.tool()
async def test_requirement_completeness(ctx: Context, requirement: str) -> dict[str, Any]:
    """测试需求完整性判断能力.

    验证 LLM 能够判断需求是否完整，并识别缺失的关键信息。

    Args:
        ctx: MCP 上下文
        requirement: 技能创建需求描述

    Returns:
        包含测试结果的字典，包括完整性分析和缺失信息列表
    """
    try:
        prompt = f"""分析以下技能创建需求，判断是否包含所有必要信息：

{requirement}

必要信息包括：
1. skill_name - 技能名称
2. skill_function - 主要功能
3. use_cases - 使用场景
4. template_type - 模板类型

请返回 JSON 格式，包含：
- is_complete: bool（是否完整）
- missing_info: list[str]（缺失的信息列表）
- suggestions: list[str]（补充建议列表）
"""

        result = await ctx.sample(
            messages=prompt,
            system_prompt="You are a skill creation consultant. Analyze requirements for completeness.",
            temperature=0.3,
        )

        # 尝试解析 LLM 返回的 JSON
        import re

        json_match = re.search(r"\{.*\}", result.text or "", re.DOTALL)
        if json_match:
            try:
                analysis = json.loads(json_match.group())
                return {
                    "success": True,
                    "test": "test_requirement_completeness",
                    "llm_analysis": analysis,
                    "has_missing_info": "missing_info" in analysis,
                    "message": "需求完整性判断验证通过",
                }
            except json.JSONDecodeError:
                pass

        # 如果无法解析 JSON，返回原始响应
        return {
            "success": True,
            "test": "test_requirement_completeness",
            "llm_response": result.text or "",
            "json_parse_failed": True,
            "message": "需求完整性判断验证通过（但 JSON 解析失败）",
        }
    except Exception as e:
        return {
            "success": False,
            "test": "test_requirement_completeness",
            "error": str(e),
            "message": f"需求完整性判断验证失败: {e}",
        }


def _generate_skill_md_content(name: str, template: str) -> str:
    """生成 SKILL.md 内容."""
    skill_title = name.replace("-", " ").replace("_", " ").title()

    descriptions = {
        "minimal": "最小化技能模板，适用于简单功能。",
        "tool-based": "基于工具的技能模板，适用于封装特定工具或 API。",
        "workflow-based": "基于工作流的技能模板，适用于多步骤任务。",
        "analyzer-based": "基于分析的技能模板，适用于数据分析或代码分析。",
    }

    description = descriptions.get(template, descriptions["minimal"])

    allowed_tools = {
        "minimal": "Read, Write, Edit, Bash",
        "tool-based": "Read, Write, Edit, Bash",
        "workflow-based": "Read, Write, Edit, Bash, Glob, Grep",
        "analyzer-based": "Read, Glob, Grep, Bash",
    }

    tools = allowed_tools.get(template, allowed_tools["minimal"])

    return f"""---
name: {name}
description: |
  {description}

  何时使用：
  - [描述使用场景 1]
  - [描述使用场景 2]

  触发词：[列出触发词]
allowed-tools: {tools}
mcp_servers: []
---

# {skill_title}

## 技能概述

[简要描述这个技能的功能和用途]

## 核心能力

1. **[能力 1]**：[描述]
2. **[能力 2]**：[描述]
3. **[能力 3]**：[描述]

## 使用方法

### 基本用法

[描述基本使用方法]

### 高级用法

[描述高级使用方法]

## 注意事项

- [注意事项 1]
- [注意事项 2]

## 参考资源

- [相关链接 1]
- [相关链接 2]
"""


async def _create_reference_files(skill_dir: Path, template_type: str) -> None:
    """创建引用文件."""
    refs_dir = skill_dir / "references"

    ref_mapping = {
        "tool-based": [
            ("tool-integration.md", "# 工具集成\n\nTODO: 添加工具集成说明"),
            ("usage-examples.md", "# 使用示例\n\nTODO: 添加使用示例"),
        ],
        "workflow-based": [
            ("workflow-steps.md", "# 工作流步骤\n\nTODO: 添加工作流步骤说明"),
            ("decision-points.md", "# 决策点\n\nTODO: 添加决策点说明"),
        ],
        "analyzer-based": [
            ("analysis-methods.md", "# 分析方法\n\nTODO: 添加分析方法说明"),
            ("metrics.md", "# 指标\n\nTODO: 添加指标说明"),
        ],
    }

    refs = ref_mapping.get(template_type, [])

    for filename, content in refs:
        await write_file_async(refs_dir / filename, content)


async def _create_example_scripts(skill_dir: Path) -> None:
    """创建示例脚本."""
    scripts_dir = skill_dir / "scripts"

    helper_content = '''#!/usr/bin/env python3
"""示例辅助脚本"""

import argparse


def main():
    parser = argparse.ArgumentParser(description="示例辅助脚本")
    parser.add_argument("--option", help="选项说明")
    args = parser.parse_args()

    print(f"执行示例脚本，选项: {args.option}")


if __name__ == "__main__":
    main()
'''
    await write_file_async(scripts_dir / "helper.py", helper_content)

    validate_content = '''#!/usr/bin/env python3
"""技能验证脚本"""

import sys
from pathlib import Path


def validate_skill():
    """验证技能结构"""
    skill_dir = Path(__file__).parent.parent

    required_files = ["SKILL.md"]
    missing_files = []

    for file in required_files:
        if not (skill_dir / file).exists():
            missing_files.append(file)

    if missing_files:
        print(f"缺少必需文件: {', '.join(missing_files)}")
        return False

    print("技能结构验证通过")
    return True


if __name__ == "__main__":
    sys.exit(0 if validate_skill() else 1)
'''
    await write_file_async(scripts_dir / "validate.py", validate_content)


async def _create_example_examples(skill_dir: Path, name: str) -> None:
    """创建使用示例."""
    examples_dir = skill_dir / "examples"

    skill_title = name.replace("-", " ").replace("_", " ").title()

    example_content = f"""# {skill_title} 使用示例

## 示例 1：基本用法

描述基本使用方法和预期结果。

## 示例 2：高级用法

描述高级使用方法和预期结果。

## 示例 3：错误处理

描述错误情况的处理方式。
"""
    await write_file_async(examples_dir / "basic-usage.md", example_content)


# ==================== MCP Resources ====================


@mcp.resource("http://skills/schema/templates")
def list_templates_resource() -> str:
    """列出所有可用的技能模板."""
    templates = list_templates()
    result = "# 技能模板列表\n\n"
    for t in templates:
        result += f"## {t['type']}\n"
        result += f"{t['description']}\n\n"
    return result


@mcp.resource("http://skills/schema/templates/{type}")
def get_template_resource(type: str) -> str:
    """获取指定类型的技能模板内容."""
    from .resources.templates import TemplateType

    # 验证模板类型
    valid_types = ["minimal", "tool-based", "workflow-based", "analyzer-based"]
    if type not in valid_types:
        return f"# 错误\n\n未知的模板类型: {type}\n\n有效类型: {', '.join(valid_types)}"

    return get_template_content(TemplateType(type))  # type: ignore


@mcp.resource("http://skills/schema/best-practices")
def best_practices_resource() -> str:
    """获取 Agent-Skills 开发最佳实践."""
    return get_best_practices()


@mcp.resource("http://skills/schema/validation-rules")
def validation_rules_resource() -> str:
    """获取 Agent-Skills 验证规则."""
    return get_validation_rules()


# ==================== MCP Prompts ====================


@mcp.prompt("create-skill")
def create_skill_prompt(
    name: str,
    template: str = "minimal",
) -> str:
    """创建新技能的 Prompt 模板.

    Args:
        name: 技能名称
        template: 模板类型（默认：minimal）

    Returns:
        Prompt 模板内容
    """
    return get_create_skill_prompt(name, template)


@mcp.prompt("validate-skill")
def validate_skill_prompt(
    skill_path: str,
    template: str | None = None,
) -> str:
    """验证技能的 Prompt 模板.

    Args:
        skill_path: 技能目录路径
        template: 模板类型（可选）

    Returns:
        Prompt 模板内容
    """
    return get_validate_skill_prompt(skill_path, template)


@mcp.prompt("refactor-skill")
def refactor_skill_prompt(
    skill_path: str,
    focus: list[str] | None = None,
) -> str:
    """重构技能的 Prompt 模板.

    Args:
        skill_path: 技能目录路径
        focus: 重点关注领域（可选）

    Returns:
        Prompt 模板内容
    """
    return get_refactor_skill_prompt(skill_path, focus)


__all__ = ["mcp"]
