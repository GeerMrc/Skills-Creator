"""端到端集成测试 - 完整工作流场景.

测试完整的 Agent-Skills 开发工作流场景：
- 创建技能 → 验证 → 分析
- 迭代改进场景
- 多技能对比场景
"""

import pytest

from skill_creator_mcp.server import _generate_skill_md_content
from skill_creator_mcp.utils.analyzers import (
    _analyze_complexity,
    _analyze_quality,
    _analyze_structure,
)
from skill_creator_mcp.utils.file_ops import create_directory_structure_async, write_file_async
from skill_creator_mcp.utils.validators import validate_skill_name, validate_template_type


@pytest.mark.asyncio
async def test_iterative_improvement_scenario(temp_dir):
    """测试迭代改进场景：逐步改进技能质量."""
    # 1. 创建基础技能
    validate_skill_name("iterative-skill")
    validate_template_type("workflow-based")

    skill_dir = await create_directory_structure_async(
        name="iterative-skill",
        template_type="workflow-based",
        output_dir=temp_dir,
    )

    skill_md_content = _generate_skill_md_content("iterative-skill", "workflow-based")
    await write_file_async(skill_dir / "SKILL.md", skill_md_content)

    # 2. 初始质量分析
    initial_quality = await _analyze_quality(skill_dir)
    initial_score = initial_quality.overall_score

    # 3. 添加改进（在 examples 目录添加文件）
    example_file = skill_dir / "examples" / "advanced_usage.md"
    example_file.write_text("# Advanced Usage\n\nAdvanced example here.")

    # 4. 重新分析质量
    improved_quality = await _analyze_quality(skill_dir)
    improved_score = improved_quality.overall_score

    # 改进后的分数应该更高或相等
    assert improved_score >= initial_score


@pytest.mark.asyncio
async def test_multi_template_comparison_scenario(temp_dir):
    """测试多模板对比场景：比较不同模板类型的技能."""
    results = {}

    # 创建三种不同类型的技能
    for template_type in ["minimal", "tool-based", "workflow-based"]:
        validate_skill_name(f"test-{template_type}")
        validate_template_type(template_type)

        skill_dir = await create_directory_structure_async(
            name=f"test-{template_type}",
            template_type=template_type,
            output_dir=temp_dir,
        )

        skill_md_content = _generate_skill_md_content(f"test-{template_type}", template_type)
        await write_file_async(skill_dir / "SKILL.md", skill_md_content)

        # 分析质量
        quality = await _analyze_quality(skill_dir)
        results[template_type] = {
            "score": quality.overall_score,
            "structure_score": quality.structure_score,
        }

    # minimal 应该有最少的结构分数
    # tool-based 和 workflow-based 应该有更高的结构分数
    assert results["minimal"]["structure_score"] <= results["tool-based"]["structure_score"]
    assert results["minimal"]["structure_score"] <= results["workflow-based"]["structure_score"]


@pytest.mark.asyncio
async def test_complete_lifecycle_scenario(temp_dir):
    """测试完整生命周期场景：从创建到分析."""
    # 1. 创建技能
    validate_skill_name("lifecycle-skill")
    validate_template_type("tool-based")

    skill_dir = await create_directory_structure_async(
        name="lifecycle-skill",
        template_type="tool-based",
        output_dir=temp_dir,
    )

    skill_md_content = _generate_skill_md_content("lifecycle-skill", "tool-based")
    await write_file_async(skill_dir / "SKILL.md", skill_md_content)

    # 2. 验证必需文件存在
    assert (skill_dir / "SKILL.md").exists()
    assert (skill_dir / "references").exists()

    # 3. 质量分析
    quality = await _analyze_quality(skill_dir)

    # 应该有有效的分数
    assert quality.overall_score > 0
    assert quality.structure_score > 0
    assert quality.documentation_score > 0
