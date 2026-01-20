"""测试 init_skill 工具."""

import pytest
from pathlib import Path

from skill_creator_mcp.utils.validators import validate_skill_name, validate_template_type
from skill_creator_mcp.utils.file_ops import create_directory_structure_async, write_file_async


@pytest.mark.asyncio
async def test_init_skill_success(temp_dir):
    """测试成功初始化技能."""
    # 验证并创建
    validate_skill_name("test-skill")
    validate_template_type("minimal")

    skill_dir = await create_directory_structure_async(
        name="test-skill",
        template_type="minimal",
        output_dir=temp_dir,
    )

    # 生成 SKILL.md
    skill_md_content = _generate_skill_md_content("test-skill", "minimal")
    await write_file_async(skill_dir / "SKILL.md", skill_md_content)

    assert skill_dir.exists()
    assert (skill_dir / "SKILL.md").exists()
    assert (skill_dir / "references").exists()
    assert (skill_dir / "examples").exists()
    assert (skill_dir / "scripts").exists()
    assert (skill_dir / ".claude").exists()


def test_validate_skill_name():
    """测试技能名称验证."""
    # 有效名称
    validate_skill_name("test-skill")
    validate_skill_name("test123")
    validate_skill_name("test-skill-123")

    # 无效名称
    with pytest.raises(ValueError):
        validate_skill_name("Invalid_Name")

    with pytest.raises(ValueError):
        validate_skill_name("-invalid")

    with pytest.raises(ValueError):
        validate_skill_name("invalid-")


def test_validate_template_type():
    """测试模板类型验证."""
    # 有效模板
    assert validate_template_type("minimal") == "minimal"
    assert validate_template_type("tool-based") == "tool-based"
    assert validate_template_type("workflow-based") == "workflow-based"
    assert validate_template_type("analyzer-based") == "analyzer-based"

    # 无效模板
    with pytest.raises(ValueError):
        validate_template_type("invalid")


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

allowed-tools: {tools}
mcp_servers: []
---

# {skill_title}

## 技能概述

[简要描述这个技能的功能和用途]
"""
