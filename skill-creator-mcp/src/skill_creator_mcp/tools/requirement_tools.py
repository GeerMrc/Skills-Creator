"""需求收集工具模块.

包含需求收集的 MCP 工具函数。
"""

from typing import Any

from fastmcp import Context


async def collect_requirements(
    ctx: Context,
    mcp,
    action: str = "start",
    mode: str = "basic",
    session_id: str | None = None,
    user_input: str | None = None,
    use_elicit: bool = False,
) -> dict[str, Any]:
    """
    AI 驱动的需求澄清/收集工具.

    通过对话方式逐步收集创建 Agent-Skill 所需的关键信息。
    支持 session state 管理，可以中断后恢复。

    Args:
        ctx: MCP 上下文
        mcp: FastMCP 实例
        action: 执行动作（start=开始，next=下一步，previous=上一步，status=查询状态，complete=完成）
        mode: 收集模式（basic=基础5步，complete=完整10步，brainstorm=头脑风暴，progressive=渐进式）
        session_id: 会话ID（自动生成，用于多轮对话）
        user_input: 用户输入（用于 next/complete 动作，use_elicit=False 时使用）
        use_elicit: 是否使用 ctx.elicit() 自动收集输入（默认 False）。True 时会自动调用
                   ctx.elicit() 收集所有必需的输入，无需手动调用 action="next"。

    Returns:
        包含收集结果的字典

    Examples:
        传统模式（两步调用）:
            # 获取第一个问题
            result = await collect_requirements(ctx, mcp, action="start", mode="basic")
            # 提供答案并获取下一个问题
            result = await collect_requirements(ctx, mcp, action="next", user_input="my-skill")

        Elicit 模式（一步调用）:
            # 自动收集所有输入
            result = await collect_requirements(ctx, mcp, action="start", mode="basic", use_elicit=True)
    """
    from ..utils.requirement_collection import (
        _collect_with_elicit,
        _get_requirement_mode_steps,
        _get_requirement_next_question,
        _handle_requirement_previous_action,
        _handle_requirement_start_action,
        _handle_requirement_status_action,
        _process_requirement_user_answer,
        _validate_and_init_requirement_session,
    )

    try:
        # 1. 验证输入参数并初始化会话状态
        (
            input_data,
            is_dynamic_mode,
            total_steps,
            current_session_id,
            session_state,
        ) = await _validate_and_init_requirement_session(ctx, action, mode, session_id, user_input)

        # 获取当前模式的步骤（静态模式）
        all_steps = _get_requirement_mode_steps(input_data.mode) if not is_dynamic_mode else None

        # 2. Elicit 模式：自动收集所有输入
        if use_elicit and input_data.action == "start":
            # 首先检测客户端是否支持 elicitation
            from ..utils.capability_detection import check_elicitation_capability
            capability = await check_elicitation_capability(ctx)
            if not capability.get("supported"):
                return {
                    "success": False,
                    "error": "elicit_mode_not_supported",
                    "message": "当前 MCP 客户端不支持交互式输入模式 (use_elicit=True)。",
                    "fallback_mode": "traditional",
                    "traditional_usage": {
                        "step_1": "调用 collect_requirements(action='start', mode='basic')",
                        "step_2": "使用返回的 session_id 调用 collect_requirements(action='next', session_id='...', user_input='...')",
                        "step_3": "重复步骤 2 直到所有问题完成",
                        "example": {
                            "start": "collect_requirements(action='start', mode='basic')",
                            "next": "collect_requirements(action='next', session_id='req_xxx', user_input='my-skill')",
                        }
                    },
                    "capability_error": capability.get("error"),
                    "details": capability.get("details"),
                }
            return await _collect_with_elicit(
                ctx=ctx,
                session_state=session_state,
                current_session_id=current_session_id,
                is_dynamic_mode=is_dynamic_mode,
                all_steps=all_steps,
                input_data=input_data,
            )

        # 3. 处理不同的 action
        if input_data.action == "status":
            return _handle_requirement_status_action(
                session_state, current_session_id, is_dynamic_mode
            )

        elif input_data.action == "previous":
            return await _handle_requirement_previous_action(
                ctx, session_state, current_session_id, is_dynamic_mode, all_steps
            )

        elif input_data.action == "start":
            # 开始新会话或重置
            await _handle_requirement_start_action(
                ctx, session_state, current_session_id, total_steps, input_data.mode
            )

        # 4. 处理用户输入（next/complete action）
        if input_data.action in ("next", "complete") and input_data.user_input:
            # 获取当前步骤（仅静态模式需要）
            current_step = None
            if not is_dynamic_mode and all_steps:
                from ..models.skill_config import RequirementStep, ValidationRule
                if session_state.current_step_index < len(all_steps):
                    step_data = all_steps[session_state.current_step_index]
                    validation_data: dict[str, Any] = dict(step_data["validation"])  # type: ignore[arg-type]
                    current_step = RequirementStep(
                        key=str(step_data["key"]),
                        title=str(step_data["title"]),
                        prompt=str(step_data["prompt"]),
                        validation=ValidationRule(**validation_data),
                    )

            result = await _process_requirement_user_answer(
                ctx=ctx,
                session_state=session_state,
                current_session_id=current_session_id,
                action=input_data.action,
                user_input=input_data.user_input,
                is_dynamic_mode=is_dynamic_mode,
                mode=input_data.mode,
                all_steps=all_steps,
                current_step=current_step.model_dump() if current_step else None,
            )

            # 如果处理完成或验证失败，直接返回
            if result.get("completed") or not result.get("success"):
                return result

            # 如果只是处理了用户输入（非完成），继续获取下一个问题
            if result.get("processed"):
                # 继续获取下一个问题
                pass

        # 5. 获取并返回下一个问题
        question_result = await _get_requirement_next_question(
            ctx=ctx,
            session_state=session_state,
            is_dynamic_mode=is_dynamic_mode,
            mode=input_data.mode,
            all_steps=all_steps,
        )

        # 添加会话信息到问题结果
        question_result["session_id"] = current_session_id
        question_result["action"] = input_data.action
        question_result["mode"] = session_state.mode

        return question_result

    except Exception as e:
        return {
            "success": False,
            "error": f"需求收集出错: {e}",
            "error_type": "internal_error",
            "message": f"内部错误: {e}",
        }


__all__ = ["collect_requirements"]
