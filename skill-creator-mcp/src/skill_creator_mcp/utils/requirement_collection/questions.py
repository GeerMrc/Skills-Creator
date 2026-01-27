"""问题生成模块.

提供动态和静态问题生成功能。
"""

from typing import Any

from fastmcp import Context


async def _get_requirement_next_question(
    ctx: Context,
    session_state: Any,
    is_dynamic_mode: bool,
    mode: str,
    all_steps: list[dict[str, Any]] | None,
) -> dict[str, Any]:
    """获取下一个问题（动态模式或静态模式）.

    Args:
        ctx: MCP 上下文
        session_state: 会话状态
        is_dynamic_mode: 是否为动态模式
        mode: 收集模式
        all_steps: 预定义步骤列表

    Returns:
        包含问题的响应字典
    """
    from ...models.skill_config import RequirementStep, ValidationRule

    # 动态模式：使用 LLM 生成问题
    if is_dynamic_mode:
        if mode == "brainstorm":
            from .llm_services import _generate_brainstorm_question

            brainstorm_history: list[dict[str, str]] = session_state.conversation_history
            question_result = await _generate_brainstorm_question(
                ctx, session_state.answers, brainstorm_history
            )

            return {
                "success": True,
                "question": question_result.get("question", ""),
                "is_dynamic_mode": True,
                "is_llm_generated": question_result.get("is_dynamic", False),
                "step_index": session_state.current_step_index,
                "total_steps": session_state.total_steps,
                "progress": min(session_state.current_step_index * 5, 95),
                "answers": session_state.answers,
                "conversation_history": session_state.conversation_history,
                "completed": False,
                "message": f"Brainstorm 模式 - 问题 {session_state.current_step_index + 1}",
            }

        elif mode == "progressive":
            from .llm_services import _generate_progressive_question

            question_result = await _generate_progressive_question(ctx, session_state.answers)

            return {
                "success": True,
                "question": question_result.get("next_question", ""),
                "question_key": question_result.get("question_key", ""),
                "is_dynamic_mode": True,
                "is_llm_generated": question_result.get("is_dynamic", False),
                "step_index": session_state.current_step_index,
                "total_steps": session_state.total_steps,
                "progress": min(session_state.current_step_index * 5, 95),
                "answers": session_state.answers,
                "completed": False,
                "message": f"Progressive 模式 - 问题 {session_state.current_step_index + 1}",
            }

    # 静态模式：获取预定义步骤
    if not is_dynamic_mode and all_steps:
        if session_state.current_step_index >= len(all_steps):
            # 所有步骤已完成
            session_state.completed = True
            return {
                "success": True,
                "step_index": session_state.current_step_index,
                "total_steps": session_state.total_steps,
                "progress": 100.0,
                "answers": session_state.answers,
                "completed": True,
                "message": "所有步骤已完成！可以使用 'complete' action 获取最终结果。",
                "current_step": None,
            }

        current_step_data = all_steps[session_state.current_step_index]
        validation_data: dict[str, Any] = dict(current_step_data["validation"])  # type: ignore[arg-type]
        current_step = RequirementStep(
            key=str(current_step_data["key"]),
            title=str(current_step_data["title"]),
            prompt=str(current_step_data["prompt"]),
            validation=ValidationRule(**validation_data),
        )

        return {
            "success": True,
            "current_step": current_step.model_dump(),
            "step_index": session_state.current_step_index,
            "total_steps": session_state.total_steps,
            "progress": (session_state.current_step_index / session_state.total_steps) * 100,
            "answers": session_state.answers,
            "completed": session_state.completed,
            "is_dynamic_mode": False,
        }

    # 默认返回
    return {
        "success": False,
        "error": "无法获取下一个问题",
        "message": "请使用 'start' 开始新会话，或使用 'next' 继续收集",
    }
