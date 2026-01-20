"""初始化技能工具.

提供创建新 Agent-Skill 的功能，包括目录结构生成、模板渲染等。
"""

from pathlib import Path
from typing import Any

from fastmcp import Context

from ..utils.file_ops import create_directory_structure_async, write_file_async
from ..utils.validators import validate_skill_name, validate_template_type


async def init_skill_tool(
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
