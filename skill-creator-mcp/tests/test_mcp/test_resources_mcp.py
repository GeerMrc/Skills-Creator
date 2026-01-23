"""测试 MCP 资源访问."""

from skill_creator_mcp.resources import (
    get_best_practices,
    get_template_content,
    get_validation_rules,
    list_templates,
)


def test_resource_functions_available():
    """测试资源函数可用."""
    # 测试所有资源函数可以调用
    templates = list_templates()
    practices = get_best_practices()
    rules = get_validation_rules()

    assert len(templates) > 0
    assert len(practices) > 0
    assert len(rules) > 0


def test_template_content_accessible():
    """测试模板内容可访问."""
    for template_type in ["minimal", "tool-based", "workflow-based", "analyzer-based"]:
        content = get_template_content(template_type)
        assert "---" in content
        assert "name:" in content


def test_resources_in_server():
    """测试资源已在 Server 中注册."""
    from skill_creator_mcp.server import mcp

    # 检查资源管理器存在
    assert hasattr(mcp, "_resource_manager")

    # 检查有资源注册
    resources = list(mcp._resource_manager._resources.values())
    assert len(resources) > 0
