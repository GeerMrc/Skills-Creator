"""Thinking MCP 集成测试.

测试 Thinking MCP 集成功能，验证：
1. SKILL.md 中的 mcp_servers 配置
2. Thinking 示例文档的存在性和有效性
3. 交叉引用链接的有效性

注意：2026-01-30 内容优化后，thinking/ 示例子目录已被删除（偏离定位）。
现在的 Thinking 示例位于 examples/ 目录下作为高级集成示例。
"""

from pathlib import Path

import pytest
import yaml

from skill_creator_mcp.utils.validators import _validate_skill_md

# 项目根目录
PROJECT_ROOT = Path("/models/claude-glm/Skills-Creator")
SKILL_CREATOR_DIR = PROJECT_ROOT / "skill-creator"
EXAMPLES_DIR = SKILL_CREATOR_DIR / "examples"
SKILL_MD = SKILL_CREATOR_DIR / "SKILL.md"


@pytest.mark.asyncio
async def test_thinking_mcp_servers_config():
    """测试 SKILL.md 中的 Thinking MCP 配置."""
    if not SKILL_MD.exists():
        pytest.skip(f"SKILL.md 不存在于 {SKILL_MD}")

    content = SKILL_MD.read_text(encoding="utf-8")

    # 解析 YAML frontmatter
    if not content.startswith("---"):
        pytest.fail("SKILL.md 缺少 YAML frontmatter")

    # 提取 YAML 内容
    yaml_end = content.find("---", 3)
    if yaml_end == -1:
        pytest.fail("SKILL.md YAML frontmatter 格式错误")

    yaml_content = content[3:yaml_end].strip()
    frontmatter = yaml.safe_load(yaml_content)

    # 验证 mcp_servers 字段存在
    assert "mcp_servers" in frontmatter, "SKILL.md 缺少 mcp_servers 字段"

    # 验证 Thinking 在 mcp_servers 列表中
    mcp_servers = frontmatter["mcp_servers"]
    assert isinstance(mcp_servers, list), "mcp_servers 应该是列表类型"
    assert "Thinking" in mcp_servers, "Thinking 应该在 mcp_servers 列表中"


@pytest.mark.asyncio
async def test_thinking_integration_example_exists():
    """测试 Thinking MCP 集成示例文档存在.

    2026-01-30 内容优化：thinking/ 示例子目录已被删除（偏离定位）。
    现在的 Thinking 示例位于 examples/mcp-thinking-integration-example.md
    """
    example_file = EXAMPLES_DIR / "mcp-thinking-integration-example.md"

    if not EXAMPLES_DIR.exists():
        pytest.skip(f"examples 目录不存在: {EXAMPLES_DIR}")

    assert example_file.exists(), f"Thinking MCP 集成示例不存在: {example_file}"

    # 验证文件内容非空
    content = example_file.read_text(encoding="utf-8")
    assert len(content) > 150, "示例文档内容过少"


@pytest.mark.asyncio
async def test_thinking_example_content_validity():
    """测试 Thinking 示例文档内容有效性."""
    if not EXAMPLES_DIR.exists():
        pytest.skip(f"examples 目录不存在: {EXAMPLES_DIR}")

    # 2026-01-30 内容优化：使用新的 mcp-thinking-integration-example.md
    example_file = EXAMPLES_DIR / "mcp-thinking-integration-example.md"

    if not example_file.exists():
        pytest.skip(f"Thinking MCP 集成示例不存在: {example_file}")

    content = example_file.read_text(encoding="utf-8")

    # 验证基本的 Markdown 结构
    assert "#" in content, f"{example_file.name} 缺少标题"

    # 验证包含 Thinking 相关关键词
    thinking_keywords = ["Thinking", "session", "MCP", "sequential_thinking", "集成"]
    found_keywords = [kw for kw in thinking_keywords if kw.lower() in content.lower()]
    assert len(found_keywords) >= 2, f"{example_file.name} 应该包含 Thinking 相关关键词"


@pytest.mark.asyncio
async def test_thinking_examples_in_readme():
    """测试 Thinking 示例在 README 中的引用."""
    readme_file = EXAMPLES_DIR / "README.md"

    if not readme_file.exists():
        pytest.skip("examples/README.md 不存在")

    content = readme_file.read_text(encoding="utf-8")

    # 2026-01-30 内容优化：检查新的 mcp-thinking-integration-example 引用
    thinking_examples = ["mcp-thinking-integration", "Thinking MCP 集成示范"]
    found_examples = [ex for ex in thinking_examples if ex in content]

    # 应该有 Thinking 集成示例被提及
    assert len(found_examples) > 0, "README 应该提及 Thinking MCP 集成示例"


@pytest.mark.asyncio
async def test_skill_creator_valid_with_thinking_mcp():
    """测试 skill-creator 技能在添加 Thinking MCP 后仍然有效."""
    if not SKILL_CREATOR_DIR.exists():
        pytest.skip(f"skill-creator 目录不存在: {SKILL_CREATOR_DIR}")

    # 使用现有的验证器验证技能
    structure_errors = []
    content_errors = []
    content_warnings = []

    # 检查基本结构
    required_dirs = ["references", "examples"]
    for dir_name in required_dirs:
        dir_path = SKILL_CREATOR_DIR / dir_name
        if not dir_path.exists():
            structure_errors.append(f"缺少必需目录: {dir_name}")

    # 检查 SKILL.md
    if SKILL_MD.exists():
        content_errors, content_warnings, _ = _validate_skill_md(SKILL_CREATOR_DIR)
    else:
        content_errors.append("缺少 SKILL.md 文件")

    # 验证结果
    assert len(structure_errors) == 0, f"结构错误: {structure_errors}"
    assert len(content_errors) == 0, f"内容错误: {content_errors}"
