#!/usr/bin/env python3
"""
Skill-Creator 验证脚本

黑盒化原则：
- 使用 argparse 处理命令行参数
- 支持 --help 查看用法
- 支持输出格式（json/text）
- 集成 MCP validate_skill 工具的验证逻辑
"""

import argparse
import json
import sys
from pathlib import Path

# 添加 skill-creator-mcp 到 Python 路径
script_dir = Path(__file__).parent.parent.parent
mcp_src = script_dir / "skill-creator-mcp" / "src"
sys.path.insert(0, str(mcp_src))

from skill_creator_mcp.utils.validators import (  # noqa: E402
    _validate_naming,
    _validate_skill_md,
    _validate_structure,
    _validate_template_requirements,
)


def validate_skill(
    skill_path: Path,
    check_structure: bool = True,
    check_content: bool = True,
) -> dict:
    """验证技能规范.

    Args:
        skill_path: 技能目录路径
        check_structure: 是否检查目录结构
        check_content: 是否检查内容格式

    Returns:
        验证结果字典
    """
    errors = []
    warnings = []
    checks = {}
    template_type = None

    # 检查目录是否存在
    if not skill_path.exists():
        return {
            "valid": False,
            "skill_path": str(skill_path),
            "errors": [f"目录不存在: {skill_path}"],
            "warnings": [],
            "checks": {},
        }

    if not skill_path.is_dir():
        return {
            "valid": False,
            "skill_path": str(skill_path),
            "errors": [f"路径不是目录: {skill_path}"],
            "warnings": [],
            "checks": {},
        }

    # 1. 检查目录结构
    if check_structure:
        structure_errors = _validate_structure(skill_path)
        errors.extend(structure_errors)
        checks["structure"] = len(structure_errors) == 0

    # 2. 检查命名规范
    naming_errors = _validate_naming(skill_path)
    errors.extend(naming_errors)
    checks["naming"] = len(naming_errors) == 0

    # 3. 检查内容格式
    if check_content:
        content_errors, content_warnings, detected_template = _validate_skill_md(skill_path)
        errors.extend(content_errors)
        warnings.extend(content_warnings)
        checks["content"] = len(content_errors) == 0

        if detected_template:
            template_type = detected_template

        # 4. 检查模板特定要求
        if template_type:
            template_errors = _validate_template_requirements(skill_path, template_type)
            errors.extend(template_errors)
            checks["template_requirements"] = len(template_errors) == 0

    # 判断验证是否通过
    valid = len(errors) == 0

    return {
        "valid": valid,
        "skill_path": str(skill_path),
        "skill_name": skill_path.name,
        "template_type": template_type,
        "errors": errors,
        "warnings": warnings,
        "checks": checks,
        "message": "验证通过" if valid else f"验证失败，发现 {len(errors)} 个错误",
    }


def main():
    parser = argparse.ArgumentParser(
        description="验证 Agent-Skills 规范",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例：
  %(prog)s /path/to/skill
  %(prog)s /path/to/skill --format json
  %(prog)s /path/to/skill --check-structure --check-content
  %(prog)s .                    # 验证当前目录
        """
    )

    parser.add_argument(
        "skill_path",
        type=str,
        help="技能目录路径"
    )

    parser.add_argument(
        "--format", "-f",
        choices=["text", "json"],
        default="text",
        help="输出格式（默认: text）"
    )

    parser.add_argument(
        "--check-structure",
        action="store_true",
        default=True,
        help="检查目录结构"
    )

    parser.add_argument(
        "--no-check-structure",
        action="store_false",
        dest="check_structure",
        help="跳过结构检查"
    )

    parser.add_argument(
        "--check-content",
        action="store_true",
        default=True,
        help="检查内容格式"
    )

    parser.add_argument(
        "--no-check-content",
        action="store_false",
        dest="check_content",
        help="跳过内容检查"
    )

    args = parser.parse_args()

    skill_path = Path(args.skill_path).resolve()

    result = validate_skill(
        skill_path,
        check_structure=args.check_structure,
        check_content=args.check_content,
    )

    if args.format == "json":
        print(json.dumps(result, indent=2, ensure_ascii=False))
    else:
        # 文本格式输出
        print(f"验证结果: {'✓ 通过' if result['valid'] else '✗ 失败'}")
        print(f"技能路径: {result['skill_path']}")
        print(f"技能名称: {result.get('skill_name', 'N/A')}")
        if result.get('template_type'):
            print(f"模板类型: {result['template_type']}")

        # 显示检查项
        print("\n检查项:")
        for check_name, passed in result.get('checks', {}).items():
            status = "✓" if passed else "✗"
            check_name_cn = {
                "structure": "目录结构",
                "naming": "命名规范",
                "content": "内容格式",
                "template_requirements": "模板要求"
            }.get(check_name, check_name)
            print(f"  {status} {check_name_cn}")

        # 显示错误
        if result.get('errors'):
            print(f"\n错误 ({len(result['errors'])}):")
            for error in result['errors']:
                print(f"  ✗ {error}")

        # 显示警告
        if result.get('warnings'):
            print(f"\n警告 ({len(result['warnings'])}):")
            for warning in result['warnings']:
                print(f"  ⚠ {warning}")

        print(f"\n{result.get('message', '')}")

    return 0 if result['valid'] else 1


if __name__ == "__main__":
    sys.exit(main())
