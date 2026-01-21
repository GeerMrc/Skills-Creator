#!/usr/bin/env python3
"""
Skill-Creator 验证脚本

黑盒化原则：
- 使用 argparse 处理命令行参数
- 支持 --help 查看用法
- 支持输出格式（json/text）
"""

import argparse
import json
import sys
from pathlib import Path


def main():
    parser = argparse.ArgumentParser(
        description="验证 Agent-Skills 规范",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例：
  %(prog)s /path/to/skill
  %(prog)s /path/to/skill --format json
  %(prog)s /path/to/skill --check-structure --check-content
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
        help="输出格式"
    )

    parser.add_argument(
        "--check-structure",
        action="store_true",
        default=True,
        help="检查目录结构"
    )

    parser.add_argument(
        "--check-content",
        action="store_true",
        default=True,
        help="检查内容格式"
    )

    args = parser.parse_args()

    # TODO: 集成 MCP validate_skill 工具或本地验证逻辑
    skill_path = Path(args.skill_path)

    if not skill_path.exists():
        result = {
            "valid": False,
            "errors": [f"路径不存在: {skill_path}"]
        }
    else:
        result = {
            "valid": True,
            "skill_path": str(skill_path),
            "message": "验证通过"
        }

    if args.format == "json":
        print(json.dumps(result, indent=2, ensure_ascii=False))
    else:
        print(f"验证结果: {'✓ 通过' if result['valid'] else '✗ 失败'}")
        if not result["valid"]:
            for error in result.get("errors", []):
                print(f"  - {error}")

    return 0 if result["valid"] else 1


if __name__ == "__main__":
    sys.exit(main())
