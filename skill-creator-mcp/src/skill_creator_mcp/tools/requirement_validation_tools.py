"""需求收集验证工具模块.

提供原子化的验证工具，不包含工作流逻辑。
符合 ADR 001: MCP Server 只提供原子操作 + 文件I/O + 数据验证。
"""

import json
import re
from typing import Any

from fastmcp import Context


async def validate_answer_format(
    ctx: Context,
    answer: str,
    validation: dict[str, Any],
) -> dict[str, Any]:
    """
    验证答案格式.

    这是一个原子操作工具，只负责验证单个答案。
    不包含重试逻辑，重试由 Agent-Skill 编排。

    Args:
        ctx: MCP 上下文
        answer: 用户输入的答案
        validation: 验证规则字典

    Returns:
        包含验证结果的字典: {
            "valid": bool,
            "error": str | None,
            "formatted_answer": str | None
        }
    """
    try:
        # 提取验证字段
        field = validation.get("field", "answer")
        required = validation.get("required", False)
        min_length = validation.get("min_length")
        max_length = validation.get("max_length")
        options = validation.get("options")
        pattern = validation.get("pattern")
        help_text = validation.get("help_text")

        # 检查必填
        if required and not answer.strip():
            return {
                "valid": False,
                "error": f"{field} 是必填项",
                "formatted_answer": None,
            }

        # 如果答案为空且非必填，直接通过
        if not answer.strip():
            return {
                "valid": True,
                "error": None,
                "formatted_answer": "",
            }

        # 检查长度
        if min_length and len(answer) < min_length:
            return {
                "valid": False,
                "error": help_text or f"最少需要 {min_length} 个字符",
                "formatted_answer": None,
            }

        if max_length and len(answer) > max_length:
            return {
                "valid": False,
                "error": help_text or f"最多允许 {max_length} 个字符",
                "formatted_answer": None,
            }

        # 检查选项
        if options:
            normalized_answer = answer.strip().lower()
            valid_options = [opt.lower() for opt in options]
            if normalized_answer not in valid_options:
                return {
                    "valid": False,
                    "error": f"无效的选项，请选择: {', '.join(options)}",
                    "formatted_answer": None,
                }

        # 检查正则表达式
        if pattern:
            if not re.match(pattern, answer.strip()):
                return {
                    "valid": False,
                    "error": help_text or "格式不正确",
                    "formatted_answer": None,
                }

        # 格式化答案
        formatted_answer = answer.strip()

        return {
            "valid": True,
            "error": None,
            "formatted_answer": formatted_answer,
        }

    except Exception as e:
        return {
            "valid": False,
            "error": f"验证过程出错: {e}",
            "formatted_answer": None,
        }


async def check_requirement_completeness(
    ctx: Context,
    answers: dict[str, str],
) -> dict[str, Any]:
    """
    检查需求完整性（使用 LLM）.

    这是一个原子操作工具，只负责完整性检查。
    不包含补充收集逻辑，补充由 Agent-Skill 编排。

    Args:
        ctx: MCP 上下文
        answers: 已收集的答案

    Returns:
        包含完整性检查结果的字典: {
            "complete": bool,
            "missing_items": list[str],
            "suggestions": list[str]
        }
    """
    try:
        prompt = f"""分析以下技能创建需求，判断是否包含所有必要信息：

已收集的信息：
{json.dumps(answers, indent=2, ensure_ascii=False)}

必要信息包括：
1. skill_name - 技能名称
2. skill_function - 主要功能
3. use_cases - 使用场景
4. template_type - 模板类型

请返回 JSON 格式，包含：
- complete: bool（是否完整）
- missing_items: list[str]（缺失的信息列表）
- suggestions: list[str]（补充建议列表）

只返回 JSON，不要其他内容。"""

        result = await ctx.sample(
            messages=prompt,
            system_prompt="你是一个技能创建顾问，负责评估需求的完整性。",
            temperature=0.3,
        )

        if result.text:
            try:
                # 提取 JSON 部分
                json_start = result.text.find("{")
                json_end = result.text.rfind("}") + 1
                if json_start >= 0 and json_end > json_start:
                    json_str = result.text[json_start:json_end]
                    parsed = json.loads(json_str)
                    return {
                        "success": True,
                        "complete": parsed.get("complete", False),
                        "missing_items": parsed.get("missing_items", []),
                        "suggestions": parsed.get("suggestions", []),
                    }
            except json.JSONDecodeError:
                pass

        # 默认返回（如果 LLM 解析失败）
        required_keys = ["skill_name", "skill_function", "use_cases", "template_type"]
        missing = [k for k in required_keys if k not in answers or not answers[k]]

        return {
            "success": True,
            "complete": len(missing) == 0,
            "missing_items": missing,
            "suggestions": [] if len(missing) == 0 else ["请补充缺失的关键信息"],
        }

    except Exception as e:
        # 如果 LLM 调用失败，进行简单的完整性检查
        required_keys = ["skill_name", "skill_function", "use_cases", "template_type"]
        missing = [k for k in required_keys if k not in answers or not answers[k]]

        return {
            "success": True,
            "complete": len(missing) == 0,
            "missing_items": missing,
            "suggestions": ["请补充缺失的关键信息"] if missing else [],
            "error": str(e),
        }


__all__ = [
    "validate_answer_format",
    "check_requirement_completeness",
]
