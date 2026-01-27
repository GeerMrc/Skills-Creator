"""操作处理器模块.

提供各种操作的处理函数，包括 status、previous、start 等操作。
"""

from datetime import datetime
from datetime import timezone as tz
from typing import Any

from fastmcp import Context


def _get_requirement_mode_steps(mode: str) -> list[dict[str, Any]]:
    """获取指定模式的步骤列表.

    Args:
        mode: 收集模式 (basic/complete/brainstorm/progressive)

    Returns:
        步骤列表（动态模式返回空列表）
    """
    if mode in ("brainstorm", "progressive"):
        return []

    from ...constants import BASIC_REQUIREMENT_STEPS, COMPLETE_REQUIREMENT_STEPS

    all_steps = BASIC_REQUIREMENT_STEPS.copy()
    if mode == "complete":
        all_steps.extend(COMPLETE_REQUIREMENT_STEPS)
    return all_steps  # type: ignore[no-any-return]


def _handle_requirement_status_action(
    session_state: Any,
    current_session_id: str,
    is_dynamic_mode: bool,
) -> dict[str, Any]:
    """处理 status 操作.

    Args:
        session_state: 会话状态
        current_session_id: 会话ID
        is_dynamic_mode: 是否为动态模式

    Returns:
        状态查询结果
    """
    return {
        "success": True,
        "session_id": current_session_id,
        "action": "status",
        "mode": session_state.mode,
        "step_index": session_state.current_step_index,
        "total_steps": session_state.total_steps,
        "progress": (session_state.current_step_index / session_state.total_steps) * 100,
        "answers": session_state.answers,
        "completed": session_state.completed,
        "message": "会话状态查询成功",
        "is_dynamic_mode": is_dynamic_mode,
    }


async def _handle_requirement_previous_action(
    ctx: Context,
    session_state: Any,
    current_session_id: str,
    is_dynamic_mode: bool,
    all_steps: list[dict[str, Any]] | None,
) -> dict[str, Any]:
    """处理 previous 操作.

    Args:
        ctx: MCP 上下文
        session_state: 会话状态
        current_session_id: 会话ID
        is_dynamic_mode: 是否为动态模式
        all_steps: 预定义步骤列表

    Returns:
        上一步操作结果
    """
    from ...models.skill_config import RequirementStep, ValidationRule

    # 上一步
    if session_state.current_step_index > 0:
        session_state.current_step_index -= 1
        await ctx.set_state(
            f"requirement_{current_session_id}", session_state.model_dump()
        )  # type: ignore[func-returns-value]

        # 对于动态模式，返回状态但不返回具体问题
        if is_dynamic_mode:
            return {
                "success": True,
                "session_id": current_session_id,
                "action": "previous",
                "mode": session_state.mode,
                "step_index": session_state.current_step_index,
                "total_steps": session_state.total_steps,
                "progress": (session_state.current_step_index / session_state.total_steps)
                * 100,
                "answers": session_state.answers,
                "conversation_history": session_state.conversation_history,
                "message": f"返回到第 {session_state.current_step_index + 1} 步（动态模式请继续提供新输入）",
                "is_dynamic_mode": True,
                "completed": False,
            }

    # basic/complete 模式的原有逻辑
    if not is_dynamic_mode and all_steps:
        current_step_data = all_steps[session_state.current_step_index]
        validation_data: dict[str, Any] = dict(current_step_data["validation"])  # type: ignore[arg-type]
        step = RequirementStep(
            key=str(current_step_data["key"]),
            title=str(current_step_data["title"]),
            prompt=str(current_step_data["prompt"]),
            validation=ValidationRule(**validation_data),
        )

        return {
            "success": True,
            "session_id": current_session_id,
            "action": "previous",
            "mode": session_state.mode,
            "current_step": step.model_dump(),
            "step_index": session_state.current_step_index,
            "total_steps": session_state.total_steps,
            "progress": (session_state.current_step_index / session_state.total_steps)
            * 100,
            "answers": session_state.answers,
            "message": f"返回到步骤: {step.title}",
            "completed": False,
        }
    else:
        return {
            "success": False,
            "session_id": current_session_id,
            "action": "previous",
            "error": "已经是第一步了" if session_state.current_step_index == 0 else "动态模式不支持返回上一步",
            "message": "无法返回上一步",
        }


async def _handle_requirement_start_action(
    ctx: Context,
    session_state: Any,
    current_session_id: str,
    total_steps: int,
    mode: str,
) -> None:
    """处理 start 操作 - 重置会话状态.

    Args:
        ctx: MCP 上下文
        session_state: 会话状态
        current_session_id: 会话ID
        total_steps: 总步骤数
        mode: 收集模式
    """
    from ...models.skill_config import SessionState

    # 重置会话状态
    new_state = SessionState(
        current_step_index=0,
        answers={},
        started_at=datetime.now(tz.utc).isoformat(),
        completed=False,
        mode=mode,  # type: ignore[arg-type]
        total_steps=total_steps,
    )
    # 更新传入的 session_state 对象（就地修改）
    session_state.current_step_index = new_state.current_step_index
    session_state.answers = new_state.answers
    session_state.started_at = new_state.started_at
    session_state.completed = new_state.completed
    session_state.mode = new_state.mode
    session_state.total_steps = new_state.total_steps

    await ctx.set_state(
        f"requirement_{current_session_id}", session_state.model_dump()
    )  # type: ignore[func-returns-value]
