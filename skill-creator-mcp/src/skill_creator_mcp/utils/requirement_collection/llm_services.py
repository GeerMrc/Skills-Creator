"""LLM 分析服务模块.

提供基于 LLM 的需求分析服务，包括完整性检查和问题生成。
"""

import json
import re
from typing import Any

from fastmcp import Context


async def _check_requirement_completeness(
    ctx: Context,
    answers: dict[str, str],
) -> dict[str, Any]:
    """使用 LLM 检查需求完整性.

    Args:
        ctx: MCP 上下文
        answers: 已收集的答案

    Returns:
        包含完整性检查结果的字典
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
- is_complete: bool（是否完整）
- missing_info: list[str]（缺失的信息列表）
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
                    return parsed  # type: ignore[no-any-return]
            except json.JSONDecodeError:
                pass

        # 默认返回（如果 LLM 解析失败）
        required_keys = ["skill_name", "skill_function", "use_cases", "template_type"]
        missing = [k for k in required_keys if k not in answers or not answers[k]]

        return {
            "is_complete": len(missing) == 0,
            "missing_info": missing,
            "suggestions": [] if len(missing) == 0 else ["请补充缺失的关键信息"],
        }

    except Exception:
        # 如果 LLM 调用失败，进行简单的完整性检查
        required_keys = ["skill_name", "skill_function", "use_cases", "template_type"]
        missing = [k for k in required_keys if k not in answers or not answers[k]]

        return {
            "is_complete": len(missing) == 0,
            "missing_info": missing,
            "suggestions": ["请补充缺失的关键信息"] if missing else [],
        }


async def _generate_brainstorm_question(
    ctx: Context,
    answers: dict[str, str],
    conversation_history: list[dict[str, str]] | None = None,
) -> dict[str, Any]:
    """使用 LLM 为 brainstorm 模式动态生成探索性问题.

    Args:
        ctx: MCP 上下文
        answers: 已收集的答案
        conversation_history: 对话历史记录

    Returns:
        包含生成问题的字典
    """
    try:
        # 构建上下文
        context_parts = []
        if answers:
            context_parts.append("已收集的信息:")
            for key, value in answers.items():
                context_parts.append(f"- {key}: {value}")

        if conversation_history:
            context_parts.append("\n之前的对话:")
            for msg in conversation_history[-4:]:  # 只保留最近4条
                context_parts.append(f"{msg.get('role', '')}: {msg.get('content', '')}")

        context = "\n".join(context_parts) if context_parts else "这是对话的开始。"

        # 生成探索性问题
        prompt = f"""你是一个技能创建顾问，正在帮助用户通过头脑风暴方式探索技能需求。

{context}

请生成一个开放性的探索性问题，帮助用户深入思考他们的技能需求。问题应该：
1. 基于已收集的信息进行深入
2. 探索用户可能未曾考虑的角度
3. 鼓励创造性思考
4. 避免重复已问过的内容

请只返回问题文本，不要其他内容。"""

        result = await ctx.sample(
            messages=prompt,
            system_prompt="You are a creative skill development consultant specializing in brainstorming and exploration.",
            temperature=0.8,  # 更高的温度以产生更多样化的问题
        )

        question = result.text.strip() if result.text else "请描述您希望这个技能实现什么独特价值？"

        return {
            "success": True,
            "question": question,
            "is_dynamic": True,
            "source": "llm_generated",
        }

    except Exception as e:
        # 降级到预定义问题
        fallback_questions = [
            "这个技能的核心价值主张是什么？",
            "它与现有解决方案有什么不同？",
            "用户最痛的场景是什么？",
            "您希望用户使用后有什么感受？",
        ]

        # 基于已收集答案数量选择问题
        index = min(len(answers), len(fallback_questions) - 1)

        return {
            "success": True,
            "question": fallback_questions[index],
            "is_dynamic": False,
            "source": "fallback",
            "error": str(e),
        }


async def _generate_progressive_question(
    ctx: Context,
    answers: dict[str, str],
) -> dict[str, Any]:
    """使用 LLM 为 progressive 模式生成针对性的下一个问题.

    Args:
        ctx: MCP 上下文
        answers: 已收集的答案

    Returns:
        包含生成问题的字典和问题类型
    """
    try:
        # 分析已收集的答案，确定下一个最相关的问题
        context = json.dumps(answers, indent=2, ensure_ascii=False)

        prompt = f"""分析以下已收集的技能需求信息，确定下一个应该询问的最相关问题。

已收集的信息：
{context}

可选问题类型（按优先级排序）：
1. 如果缺少 skill_name，询问技能名称
2. 如果缺少 skill_function，询问主要功能
3. 如果缺少 use_cases，询问使用场景
4. 如果缺少 template_type，询问模板类型
5. 如果基本信息齐全，询问更深入的问题（target_users, tech_stack 等）

请返回 JSON 格式：
{{
    "next_question": "具体的问题文本",
    "question_key": "问题标识（如 skill_name, skill_function 等）",
    "reasoning": "选择这个问题的原因"
}}"""

        result = await ctx.sample(
            messages=prompt,
            system_prompt="You are a skill requirements analyst. Determine the most relevant next question based on collected information.",
            temperature=0.3,
        )

        # 尝试解析 JSON
        json_match = re.search(r"\{.*\}", result.text or "", re.DOTALL)
        if json_match:
            try:
                parsed = json.loads(json_match.group())
                return {
                    "success": True,
                    "next_question": parsed.get("next_question", "请提供更多关于技能功能的细节？"),
                    "question_key": parsed.get("question_key", "follow_up"),
                    "reasoning": parsed.get("reasoning", ""),
                    "is_dynamic": True,
                }
            except json.JSONDecodeError:
                pass

        # 降级：根据答案数量选择基础问题
        basic_questions = [
            ("skill_name", "请提供技能名称（小写字母、数字、连字符）"),
            ("skill_function", "请描述这个技能的主要功能"),
            ("use_cases", "请描述这个技能的使用场景"),
            (
                "template_type",
                "选择技能模板类型：minimal、tool-based、workflow-based、analyzer-based",
            ),
        ]

        index = min(len(answers), len(basic_questions) - 1)
        key, question = basic_questions[index]

        return {
            "success": True,
            "next_question": question,
            "question_key": key,
            "is_dynamic": False,
            "source": "fallback",
        }

    except Exception as e:
        # 统一返回格式：即使异常也返回 success:True 和 fallback 问题
        # 这样与 brainstorm 模式行为一致
        basic_questions = [
            ("skill_name", "请提供技能名称（小写字母、数字、连字符）"),
            ("skill_function", "请描述这个技能的主要功能"),
            ("use_cases", "请描述这个技能的使用场景"),
            (
                "template_type",
                "选择技能模板类型：minimal、tool-based、workflow-based、analyzer-based",
            ),
        ]

        # 根据已收集答案数量选择问题
        index = min(len(answers), len(basic_questions) - 1)
        key, question = basic_questions[index]

        return {
            "success": True,  # 与 brainstorm 保持一致
            "next_question": question,
            "question_key": key,
            "is_dynamic": False,
            "source": "fallback",
            "error": str(e),  # 保留原始错误信息供调试
        }
