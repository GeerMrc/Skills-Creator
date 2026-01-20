"""验证器工具函数."""

import re
from pathlib import Path


def validate_skill_name(name: str) -> None:
    """验证技能名称符合规范.

    规范：
    - 只能包含小写字母、数字、连字符
    - 不能以连字符开头或结尾
    - 不能有连续的连字符

    Args:
        name: 技能名称

    Raises:
        ValueError: 名称不符合规范时抛出
    """
    pattern = r'^[a-z0-9]+(?:-[a-z0-9]+)*$'
    if not re.match(pattern, name):
        raise ValueError(
            f"技能名称 '{name}' 不符合规范。"
            "要求：小写字母、数字、单个连字符，不能以连字符开头或结尾，不能有连续连字符"
        )


def validate_skill_directory(skill_dir: Path) -> None:
    """验证技能目录是否存在且结构正确.

    Args:
        skill_dir: 技能目录路径

    Raises:
        ValueError: 目录结构不正确时抛出
    """
    if not skill_dir.exists():
        raise ValueError(f"技能目录不存在: {skill_dir}")

    skill_md = skill_dir / "SKILL.md"
    if not skill_md.exists():
        raise ValueError(f"SKILL.md 不存在于: {skill_dir}")


def validate_template_type(template: str) -> str:
    """验证模板类型是否有效.

    Args:
        template: 模板类型

    Returns:
        验证通过的模板类型

    Raises:
        ValueError: 模板类型无效时抛出
    """
    valid_templates = ["minimal", "tool-based", "workflow-based", "analyzer-based"]
    if template not in valid_templates:
        raise ValueError(
            f"无效的模板类型: {template}。"
            f"有效值: {', '.join(valid_templates)}"
        )
    return template
