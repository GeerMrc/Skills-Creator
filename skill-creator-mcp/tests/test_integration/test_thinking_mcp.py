"""Thinking MCP 集成测试.

测试 Thinking MCP 集成功能，验证：
1. SKILL.md 中的 mcp_servers 配置
2. Thinking 示例文档的存在性和有效性
3. 交叉引用链接的有效性
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
async def test_thinking_analysis_example_exists():
    """测试 thinking/ 目录存在并包含分析示例."""
    thinking_dir = EXAMPLES_DIR / "thinking"

    if not EXAMPLES_DIR.exists():
        pytest.skip(f"examples 目录不存在: {EXAMPLES_DIR}")

    assert thinking_dir.exists(), f"Thinking 目录不存在: {thinking_dir}"

    # 验证分析相关文件存在
    analysis_files = [
        thinking_dir / "analysis-basic.md",
        thinking_dir / "analysis-advanced.md",
        thinking_dir / "analysis-workflow.md",
    ]

    for example_file in analysis_files:
        assert example_file.exists(), f"Thinking 分析示例不存在: {example_file}"
        content = example_file.read_text(encoding="utf-8")
        assert len(content) > 100, f"{example_file.name} 内容过少"


@pytest.mark.asyncio
async def test_thinking_export_example_exists():
    """测试 thinking/ 目录存在并包含导出示例."""
    thinking_dir = EXAMPLES_DIR / "thinking"

    if not EXAMPLES_DIR.exists():
        pytest.skip(f"examples 目录不存在: {EXAMPLES_DIR}")

    assert thinking_dir.exists(), f"Thinking 目录不存在: {thinking_dir}"

    # 验证导出相关文件存在
    export_files = [
        thinking_dir / "export-formats.md",
        thinking_dir / "export-workflow.md",
        thinking_dir / "export-automation.md",
    ]

    for example_file in export_files:
        assert example_file.exists(), f"Thinking 导出示例不存在: {example_file}"
        content = example_file.read_text(encoding="utf-8")
        assert len(content) > 100, f"{example_file.name} 内容过少"


@pytest.mark.asyncio
async def test_thinking_example_content_validity():
    """测试 Thinking 示例文档内容有效性."""
    if not EXAMPLES_DIR.exists():
        pytest.skip(f"examples 目录不存在: {EXAMPLES_DIR}")

    thinking_dir = EXAMPLES_DIR / "thinking"
    if not thinking_dir.exists():
        pytest.skip(f"thinking 目录不存在: {thinking_dir}")

    # 检查所有 thinking 目录下的 Markdown 文件
    thinking_files = list(thinking_dir.glob("*.md"))

    assert len(thinking_files) >= 6, f"应该至少有6个 Thinking 示例文件，实际: {len(thinking_files)}"

    for example_file in thinking_files:
        content = example_file.read_text(encoding="utf-8")

        # 验证基本的 Markdown 结构
        assert "#" in content, f"{example_file.name} 缺少标题"

        # 验证包含 Thinking 相关关键词
        thinking_keywords = ["Thinking", "session", "MCP", "sequential_thinking", "export"]
        found_keywords = [kw for kw in thinking_keywords if kw.lower() in content.lower()]
        assert len(found_keywords) >= 1, f"{example_file.name} 应该包含 Thinking 相关关键词"


@pytest.mark.asyncio
async def test_thinking_cross_references():
    """测试 Thinking 示例中的交叉引用链接."""
    if not EXAMPLES_DIR.exists():
        pytest.skip(f"examples 目录不存在: {EXAMPLES_DIR}")

    thinking_dir = EXAMPLES_DIR / "thinking"
    if not thinking_dir.exists():
        pytest.skip(f"thinking 目录不存在: {thinking_dir}")

    # 检查所有 thinking 目录下的文件
    thinking_files = list(thinking_dir.glob("*.md"))

    for example_file in thinking_files:
        content = example_file.read_text(encoding="utf-8")

        # 检查是否有引用链接
        if "](references/" in content or "](../references/" in content:
            # 提取引用路径
            import re

            pattern = r'\]\((?:\.\./)?references/([^)]+)\)'
            matches = re.findall(pattern, content)

            for ref_path in matches:
                ref_file = SKILL_CREATOR_DIR / "references" / ref_path
                assert ref_file.exists(), f"{example_file.name} 引用的文档不存在: {ref_path}"


@pytest.mark.asyncio
async def test_thinking_examples_in_readme():
    """测试 Thinking 示例在 README 中的引用."""
    readme_file = EXAMPLES_DIR / "README.md"

    if not readme_file.exists():
        pytest.skip("examples/README.md 不存在")

    content = readme_file.read_text(encoding="utf-8")

    # 验证 Thinking 目录被提及或索引
    thinking_references = ["thinking/", "Thinking 集成", "Thinking 集成示例索引"]
    found_references = [ref for ref in thinking_references if ref in content]

    # 至少应该有一个 Thinking 相关引用被提及
    assert len(found_references) > 0, "README 应该提及 Thinking 集成示例"


@pytest.mark.asyncio
async def test_thinking_session_workflow_example():
    """测试 Thinking 示例中的会话工作流说明."""
    if not EXAMPLES_DIR.exists():
        pytest.skip(f"examples 目录不存在: {EXAMPLES_DIR}")

    thinking_dir = EXAMPLES_DIR / "thinking"
    if not thinking_dir.exists():
        pytest.skip(f"thinking 目录不存在: {thinking_dir}")

    # 检查分析相关文件包含工作流步骤
    analysis_files = [
        thinking_dir / "analysis-basic.md",
        thinking_dir / "analysis-workflow.md",
    ]

    has_workflow = False
    for analysis_file in analysis_files:
        if analysis_file.exists():
            content = analysis_file.read_text(encoding="utf-8")
            # 应该包含会话创建或分析的步骤
            workflow_keywords = ["create_session", "sequential_thinking", "get_session"]
            found_keywords = [kw for kw in workflow_keywords if kw in content]
            if len(found_keywords) > 0:
                has_workflow = True
                break

    assert has_workflow, "Thinking 分析示例应该包含工作流步骤"

    # 检查导出相关文件包含导出功能说明
    export_files = [
        thinking_dir / "export-formats.md",
        thinking_dir / "export-workflow.md",
    ]

    has_export_info = False
    for export_file in export_files:
        if export_file.exists():
            content = export_file.read_text(encoding="utf-8")
            # 应该包含导出相关关键词
            export_keywords = ["export_session", "format", "markdown", "json"]
            found_keywords = [kw for kw in export_keywords if kw.lower() in content.lower()]
            if len(found_keywords) >= 2:
                has_export_info = True
                break

    assert has_export_info, "Thinking 导出示例应该包含导出功能说明"


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
