"""Skill Creator MCP Server.

这是一个基于 FastMCP SDK 开发的 MCP Server，用于创建、验证、
分析和重构 Agent-Skills。
"""

from pathlib import Path
from typing import Any

from fastmcp import Context, FastMCP

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
from .utils.validators import (
    _validate_naming,
    _validate_skill_md,
    _validate_structure,
    _validate_template_requirements,
    validate_skill_name,
    validate_template_type,
)

# 创建 MCP Server
mcp = FastMCP(
    name="skill-creator",
    instructions="""
    Skill Creator MCP Server - Agent-Skills 开发工具

    这个服务器提供创建、验证、分析和重构 Agent-Skills 的工具。

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

    ## TODO: 更多工具正在开发中

    当前处于开发阶段，其他工具和资源正在逐步实现中。
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
    try:
        # 1. 验证输入参数
        validate_skill_name(name)
        validate_template_type(template)

        # 2. 创建目录结构
        skill_dir = await create_directory_structure_async(
            name=name,
            template_type=template,
            output_dir=Path(output_dir),
        )

        # 3. 生成 SKILL.md 内容
        skill_md_content = _generate_skill_md_content(name, template)
        await write_file_async(
            skill_dir / "SKILL.md",
            skill_md_content,
        )

        # 4. 创建引用文件（非 minimal 模板）
        if template != "minimal":
            await _create_reference_files(skill_dir, template)

        # 5. 创建示例脚本
        if with_scripts:
            await _create_example_scripts(skill_dir)

        # 6. 创建使用示例
        if with_examples:
            await _create_example_examples(skill_dir, name)

        return {
            "success": True,
            "skill_path": str(skill_dir),
            "skill_name": name,
            "template": template,
            "message": f"技能 '{name}' 已创建在：{skill_dir}",
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
    try:
        skill_dir = Path(skill_path)

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
        if check_structure:
            structure_errors = _validate_structure(skill_dir)
            errors.extend(structure_errors)
            checks["structure"] = len(structure_errors) == 0

        # 2. 检查命名规范
        naming_errors = _validate_naming(skill_dir)
        errors.extend(naming_errors)
        checks["naming"] = len(naming_errors) == 0

        # 3. 检查内容格式
        if check_content:
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
        QualityScore,
    )

    try:
        skill_dir = Path(skill_path)

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

        # 1. 结构分析
        if analyze_structure:
            structure = _analyze_structure(skill_dir)
        else:
            from .models.skill_config import StructureAnalysis
            structure = StructureAnalysis(total_files=0, total_lines=0, file_breakdown={})

        # 2. 复杂度分析
        if analyze_complexity:
            complexity = _analyze_complexity(skill_dir)
        else:
            from .models.skill_config import ComplexityMetrics
            complexity = ComplexityMetrics(cyclomatic_complexity=None, maintainability_index=None, code_duplication=None)

        # 3. 质量分析
        if analyze_quality:
            quality = _analyze_quality(skill_dir)
        else:
            # 如果不分析质量，使用默认值
            quality = QualityScore(overall_score=0.0, structure_score=0.0, documentation_score=0.0, test_coverage_score=0.0)

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


@mcp.resource("skill://templates")
def list_templates_resource() -> str:
    """列出所有可用的技能模板."""
    templates = list_templates()
    result = "# 技能模板列表\n\n"
    for t in templates:
        result += f"## {t['type']}\n"
        result += f"{t['description']}\n\n"
    return result


@mcp.resource("skill://templates/{type}")
def get_template_resource(type: str) -> str:
    """获取指定类型的技能模板内容."""
    from .resources.templates import TemplateType

    # 验证模板类型
    valid_types = ["minimal", "tool-based", "workflow-based", "analyzer-based"]
    if type not in valid_types:
        return f"# 错误\n\n未知的模板类型: {type}\n\n有效类型: {', '.join(valid_types)}"

    return get_template_content(TemplateType(type))  # type: ignore


@mcp.resource("skill://best-practices")
def best_practices_resource() -> str:
    """获取 Agent-Skills 开发最佳实践."""
    return get_best_practices()


@mcp.resource("skill://validation-rules")
def validation_rules_resource() -> str:
    """获取 Agent-Skills 验证规则."""
    return get_validation_rules()


__all__ = ["mcp"]
