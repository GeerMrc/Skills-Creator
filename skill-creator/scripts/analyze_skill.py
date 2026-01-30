#!/usr/bin/env python3
"""
Skill-Creator 分析脚本

黑盒化原则：
- 使用 argparse 处理命令行参数
- 支持 --help 查看用法
- 支持输出格式（json/text）
- 集成 MCP analyze_skill 工具的分析逻辑
"""

import argparse
import json
import sys
from pathlib import Path

# 添加 skill-creator-mcp 到 Python 路径
script_dir = Path(__file__).parent.parent.parent
mcp_src = script_dir / "skill-creator-mcp" / "src"
sys.path.insert(0, str(mcp_src))

from skill_creator_mcp.utils.analyzers import (  # noqa: E402
    _analyze_complexity,
    _analyze_quality,
    _analyze_structure,
    _generate_analysis_summary,
    _generate_suggestions,
)


def analyze_skill(
    skill_path: Path,
    analyze_structure: bool = True,
    analyze_complexity: bool = True,
    analyze_quality: bool = True,
) -> dict:
    """分析技能代码质量.

    Args:
        skill_path: 技能目录路径
        analyze_structure: 是否分析代码结构
        analyze_complexity: 是否分析代码复杂度
        analyze_quality: 是否分析代码质量

    Returns:
        分析结果字典
    """
    # 检查目录是否存在
    if not skill_path.exists():
        return {
            "success": False,
            "error": f"目录不存在: {skill_path}",
            "error_type": "path_error",
        }

    if not skill_path.is_dir():
        return {
            "success": False,
            "error": f"路径不是目录: {skill_path}",
            "error_type": "path_error",
        }

    # 1. 结构分析
    if analyze_structure:
        structure = _analyze_structure(skill_path)
    else:
        from skill_creator_mcp.models.skill_config import StructureAnalysis
        structure = StructureAnalysis(total_files=0, total_lines=0, file_breakdown={})

    # 2. 复杂度分析
    if analyze_complexity:
        complexity = _analyze_complexity(skill_path)
    else:
        from skill_creator_mcp.models.skill_config import ComplexityMetrics
        complexity = ComplexityMetrics(
            cyclomatic_complexity=None,
            maintainability_index=None,
            code_duplication=None
        )

    # 3. 质量分析
    if analyze_quality:
        quality = _analyze_quality(skill_path)
    else:
        from skill_creator_mcp.models.skill_config import QualityScore
        quality = QualityScore(
            overall_score=0.0,
            structure_score=0.0,
            documentation_score=0.0,
            test_coverage_score=0.0
        )

    # 4. 生成改进建议
    suggestions = _generate_suggestions(structure, complexity, quality)

    return {
        "success": True,
        "skill_path": str(skill_path),
        "skill_name": skill_path.name,
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


def main():
    parser = argparse.ArgumentParser(
        description="分析 Agent-Skills 代码质量",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例：
  %(prog)s /path/to/skill
  %(prog)s /path/to/skill --format json
  %(prog)s /path/to/skill --detailed
  %(prog)s .                    # 分析当前目录
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
        "--detailed", "-d",
        action="store_true",
        help="显示详细分析"
    )

    parser.add_argument(
        "--no-structure",
        action="store_false",
        dest="analyze_structure",
        help="跳过结构分析"
    )

    parser.add_argument(
        "--no-complexity",
        action="store_false",
        dest="analyze_complexity",
        help="跳过复杂度分析"
    )

    parser.add_argument(
        "--no-quality",
        action="store_false",
        dest="analyze_quality",
        help="跳过质量分析"
    )

    args = parser.parse_args()

    skill_path = Path(args.skill_path).resolve()

    result = analyze_skill(
        skill_path,
        analyze_structure=getattr(args, 'analyze_structure', True),
        analyze_complexity=getattr(args, 'analyze_complexity', True),
        analyze_quality=getattr(args, 'analyze_quality', True),
    )

    if not result.get("success"):
        print(f"错误: {result.get('error', '未知错误')}")
        return 1

    if args.format == "json":
        print(json.dumps(result, indent=2, ensure_ascii=False))
    else:
        # 文本格式输出
        print(f"分析报告: {result['skill_path']}")
        print(f"技能名称: {result['skill_name']}\n")

        # 结构分析
        structure = result.get('structure', {})
        print("=" * 50)
        print("结构分析")
        print("=" * 50)
        print(f"总文件数: {structure.get('total_files', 0)}")
        print(f"总代码行数: {structure.get('total_lines', 0)}")

        if args.detailed and structure.get('file_breakdown'):
            print("\n文件分类:")
            for category, count in structure.get('file_breakdown', {}).items():
                print(f"  {category}: {count}")

        # 复杂度分析
        complexity = result.get('complexity', {})
        print("\n" + "=" * 50)
        print("复杂度分析")
        print("=" * 50)
        if complexity.get('cyclomatic_complexity') is not None:
            print(f"圈复杂度: {complexity['cyclomatic_complexity']:.2f}")
        if complexity.get('maintainability_index') is not None:
            print(f"可维护性指数: {complexity['maintainability_index']:.2f}")
        if complexity.get('code_duplication') is not None:
            print(f"代码重复率: {complexity['code_duplication']:.2f}%")

        # 质量评分
        quality = result.get('quality', {})
        print("\n" + "=" * 50)
        print("质量评分")
        print("=" * 50)
        print(f"综合评分: {quality.get('overall_score', 0):.1f}/100")
        print(f"结构评分: {quality.get('structure_score', 0):.1f}/100")
        print(f"文档评分: {quality.get('documentation_score', 0):.1f}/100")
        print(f"测试覆盖: {quality.get('test_coverage_score', 0):.1f}/100")

        # 改进建议
        suggestions = result.get('suggestions', [])
        if suggestions:
            print("\n" + "=" * 50)
            print("改进建议")
            print("=" * 50)
            for i, suggestion in enumerate(suggestions, 1):
                print(f"{i}. {suggestion}")

        # 总结
        summary = result.get('summary', '')
        if summary:
            print("\n" + "=" * 50)
            print("分析总结")
            print("=" * 50)
            print(summary)

    return 0


if __name__ == "__main__":
    sys.exit(main())
