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
    """
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
        input_data = InitSkillInput.model_validate({
            "name": name,
            "template": template,
            "output_dir": output_dir,
            "with_scripts": with_scripts,
            "with_examples": with_examples,
        })

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
        包含验证结果的字典
    """
    from .models.skill_config import ValidateSkillInput

    try:
        # 使用 Pydantic 验证输入参数
        input_data = ValidateSkillInput.model_validate({
            "skill_path": skill_path,
            "check_structure": check_structure,
            "check_content": check_content,
        })

        skill_dir = Path(input_data.skill_path)

        # 初始化结果
        errors = []
        warnings = []
        checks = {}
        template_type = None

        # 检查目录是否存在
        if not skill_dir.exists():
            return {
                "success": False,
                "valid": False,
                "skill_path": skill_path,
                "errors": [f"目录不存在: {skill_path}"],
                "warnings": [],
                "checks": {},
            }

        if not skill_dir.is_dir():
            return {
                "success": False,
                "valid": False,
                "skill_path": skill_path,
                "errors": [f"路径不是目录: {skill_path}"],
                "warnings": [],
                "checks": {},
            }

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

            if detected_template:
                template_type = detected_template

            # 4. 检查模板特定要求
            if template_type:
                template_errors = _validate_template_requirements(skill_dir, template_type)
                errors.extend(template_errors)
                checks["template_requirements"] = len(template_errors) == 0

        # 判断验证是否通过
        valid = len(errors) == 0

        return {
            "success": True,
            "valid": valid,
            "skill_path": str(skill_dir),
            "skill_name": skill_dir.name,
            "template_type": template_type,
            "errors": errors,
            "warnings": warnings,
            "checks": checks,
            "message": "验证通过" if valid else f"验证失败，发现 {len(errors)} 个错误",
        }

    except Exception as e:
        return {
            "success": False,
            "valid": False,
            "skill_path": skill_path,
            "errors": [f"验证过程出错: {e}"],
            "warnings": [],
            "checks": {},
            "error_type": "internal_error",
        }


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
        input_data = AnalyzeSkillInput.model_validate({
            "skill_path": skill_path,
            "analyze_structure": analyze_structure,
            "analyze_complexity": analyze_complexity,
            "analyze_quality": analyze_quality,
        })

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
        input_data = RefactorSkillInput.model_validate({
            "skill_path": skill_path,
            "focus": focus,
            "analyze_structure": analyze_structure,
            "analyze_complexity": analyze_complexity,
            "analyze_quality": analyze_quality,
        })

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
        input_data = PackageSkillInput.model_validate({
            "skill_path": skill_path,
            "output_dir": output_dir,
            "format": format,
            "include_tests": include_tests,
            "validate_before_package": validate_before_package,
        })

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
        user_input: 用户输入（用于 next/complete 动作）

    Returns:
        包含收集结果的字典
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
        input_data = RequirementCollectionInput.model_validate({
            "action": action,
            "mode": mode,
            "session_id": session_id,
            "user_input": user_input,
        })

        # 2. 确定步骤列表
        all_steps = BASIC_REQUIREMENT_STEPS.copy()
        if input_data.mode == "complete":
            all_steps.extend(COMPLETE_REQUIREMENT_STEPS)

        # 3. 处理会话ID
        current_session_id = input_data.session_id or ctx.session_id or f"req_{datetime.now(tz.utc).isoformat()}"

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
                total_steps=len(all_steps),
            )

        # 5. 处理不同的 action
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
            }

        elif input_data.action == "previous":
            # 上一步
            if session_state.current_step_index > 0:
                session_state.current_step_index -= 1
                await ctx.set_state(f"requirement_{current_session_id}", session_state.model_dump())  # type: ignore[func-returns-value]

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
                    "progress": (session_state.current_step_index / session_state.total_steps) * 100,
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
                total_steps=len(all_steps),
            )
            await ctx.set_state(f"requirement_{current_session_id}", session_state.model_dump())  # type: ignore[func-returns-value]

        # 6. 获取当前步骤
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

        # 7. 处理用户输入（next/complete action）
        if input_data.action in ("next", "complete") and input_data.user_input:
            # 验证用户输入
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
            if input_data.action == "complete" or session_state.current_step_index >= len(all_steps):
                session_state.completed = True

            await ctx.set_state(f"requirement_{current_session_id}", session_state.model_dump())  # type: ignore[func-returns-value]

            # 如果完成，使用 LLM 生成总结
            if session_state.completed:
                completeness_check = await _check_requirement_completeness(ctx, session_state.answers)

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

        # 8. 返回当前步骤信息
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
    min_length = validation.get("min_length") if isinstance(validation, dict) else validation.min_length
    max_length = validation.get("max_length") if isinstance(validation, dict) else validation.max_length
    options = validation.get("options") if isinstance(validation, dict) else validation.options
    pattern = validation.get("pattern") if isinstance(validation, dict) else validation.pattern
    help_text = validation.get("help_text") if isinstance(validation, dict) else validation.help_text

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
