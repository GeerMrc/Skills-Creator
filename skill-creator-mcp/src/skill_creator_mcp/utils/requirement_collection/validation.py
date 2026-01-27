"""验证和答案处理模块.

提供需求验证、答案处理和会话初始化功能。
"""

import re
from datetime import datetime
from datetime import timezone as tz
from typing import Any

from fastmcp import Context

from .session_manager import SessionStateManager


def _validate_requirement_answer(
    answer: str,
    validation: Any,
) -> dict[str, Any]:
    """验证需求收集的用户答案.

    Args:
        answer: 用户输入的答案
        validation: 验证规则（dict 或 ValidationRule 对象）

    Returns:
        包含验证结果的字典
    """
    # 提取验证字段
    field = validation.get("field") if isinstance(validation, dict) else validation.field
    required = validation.get("required") if isinstance(validation, dict) else validation.required
    min_length = (
        validation.get("min_length") if isinstance(validation, dict) else validation.min_length
    )
    max_length = (
        validation.get("max_length") if isinstance(validation, dict) else validation.max_length
    )
    options = validation.get("options") if isinstance(validation, dict) else validation.options
    pattern = validation.get("pattern") if isinstance(validation, dict) else validation.pattern
    help_text = (
        validation.get("help_text") if isinstance(validation, dict) else validation.help_text
    )

    # 检查必填
    if required and not answer.strip():
        return {
            "valid": False,
            "error": f"{field} 是必填项",
        }

    # 如果答案为空且非必填，直接通过
    if not answer.strip():
        return {"valid": True}

    # 检查长度
    if min_length and len(answer) < min_length:
        return {
            "valid": False,
            "error": help_text or f"最少需要 {min_length} 个字符",
        }

    if max_length and len(answer) > max_length:
        return {
            "valid": False,
            "error": help_text or f"最多允许 {max_length} 个字符",
        }

    # 检查选项
    if options:
        normalized_answer = answer.strip().lower()
        valid_options = [opt.lower() for opt in options]
        if normalized_answer not in valid_options:
            return {
                "valid": False,
                "error": f"无效的选项，请选择: {', '.join(options)}",
            }

    # 检查正则表达式
    if pattern:
        if not re.match(pattern, answer.strip()):
            return {
                "valid": False,
                "error": help_text or "格式不正确",
            }

    return {"valid": True}


async def _process_requirement_user_answer(
    ctx: Context,
    session_state: Any,
    current_session_id: str,
    action: str,
    user_input: str,
    is_dynamic_mode: bool,
    mode: str,
    all_steps: list[dict[str, Any]] | None,
    current_step: Any,
) -> dict[str, Any]:
    """处理用户输入（next/complete action）.

    Args:
        ctx: MCP 上下文
        session_state: 会话状态
        current_session_id: 会话ID
        action: 操作类型
        user_input: 用户输入
        is_dynamic_mode: 是否为动态模式
        mode: 收集模式
        all_steps: 预定义步骤列表
        current_step: 当前步骤对象（仅静态模式）

    Returns:
        处理结果字典
    """
    from ...models.skill_config import RequirementStep, ValidationRule

    if is_dynamic_mode:
        # 动态模式：直接保存答案并继续
        answer_key = f"answer_{session_state.current_step_index}"
        session_state.answers[answer_key] = user_input

        # 更新对话历史（用于 brainstorm 模式）
        if mode == "brainstorm":
            session_state.conversation_history.append({"role": "user", "content": user_input})

        # 移动到下一步
        if action == "next":
            session_state.current_step_index += 1

        # 检查是否完成
        if action == "complete":
            session_state.completed = True

        await ctx.set_state(
            f"requirement_{current_session_id}", session_state.model_dump()
        )  # type: ignore[func-returns-value]

        # 如果完成，返回结果
        if session_state.completed:
            return {
                "success": True,
                "session_id": current_session_id,
                "action": action,
                "mode": mode,
                "step_index": session_state.current_step_index,
                "total_steps": session_state.total_steps,
                "progress": 100.0,
                "answers": session_state.answers,
                "conversation_history": session_state.conversation_history,
                "completed": True,
                "message": f"{mode.upper()} 模式需求收集完成！",
                "is_dynamic_mode": True,
            }
        else:
            # 返回成功，等待用户继续
            return {
                "success": True,
                "session_id": current_session_id,
                "action": action,
                "mode": mode,
                "step_index": session_state.current_step_index,
                "total_steps": session_state.total_steps,
                "progress": min(session_state.current_step_index * 5, 95),
                "answers": session_state.answers,
                "conversation_history": session_state.conversation_history,
                "message": "答案已保存，请继续使用 'next' action",
                "is_dynamic_mode": True,
            }
    else:
        # basic/complete 模式的验证逻辑
        if current_step is None:
            return {
                "success": False,
                "error": "没有当前步骤",
                "message": "请先使用 'start' 开始会话",
            }

        # 重建 RequirementStep 对象以获取验证规则
        step_data = current_step
        validation_data: dict[str, Any] = dict(step_data["validation"])  # type: ignore[arg-type]
        step_obj = RequirementStep(
            key=str(step_data["key"]),
            title=str(step_data["title"]),
            prompt=str(step_data["prompt"]),
            validation=ValidationRule(**validation_data),
        )

        validation_result = _validate_requirement_answer(
            user_input,
            step_obj.validation,
        )

        if not validation_result["valid"]:
            return {
                "success": False,
                "session_id": current_session_id,
                "action": action,
                "error": validation_result["error"],
                "message": f"输入验证失败: {validation_result['error']}",
            }

        # 保存答案
        session_state.answers[step_obj.key] = user_input

        # 移动到下一步
        if action == "next":
            session_state.current_step_index += 1

        # 检查是否完成
        if action == "complete" or (all_steps and session_state.current_step_index >= len(all_steps)):
            session_state.completed = True

        await ctx.set_state(
            f"requirement_{current_session_id}", session_state.model_dump()
        )  # type: ignore[func-returns-value]

        # 如果完成，使用 LLM 生成总结
        if session_state.completed:
            from .llm_services import _check_requirement_completeness

            completeness_check = await _check_requirement_completeness(
                ctx, session_state.answers
            )

            return {
                "success": True,
                "session_id": current_session_id,
                "action": action,
                "mode": mode,
                "step_index": session_state.current_step_index,
                "total_steps": session_state.total_steps,
                "progress": 100.0,
                "answers": session_state.answers,
                "completed": True,
                "is_complete": completeness_check["is_complete"],
                "missing_info": completeness_check["missing_info"],
                "suggestions": completeness_check["suggestions"],
                "message": "需求收集完成！",
            }

        # 未完成，返回空结果表示继续
        return {
            "success": True,
            "session_id": current_session_id,
            "action": action,
            "processed": True,
        }


async def _validate_and_init_requirement_session(
    ctx: Context,
    action: str,
    mode: str,
    session_id: str | None,
    user_input: str | None,
) -> tuple[Any, bool, int, str, Any]:
    """验证输入参数并初始化/获取会话状态.

    Args:
        ctx: MCP 上下文
        action: 执行动作
        mode: 收集模式
        session_id: 会话ID
        user_input: 用户输入

    Returns:
        (input_data, is_dynamic_mode, total_steps, current_session_id, session_state)
    """
    from ...models.skill_config import RequirementCollectionInput

    # 1. 验证输入参数
    input_data = RequirementCollectionInput.model_validate(
        {
            "action": action,
            "mode": mode,
            "session_id": session_id,
            "user_input": user_input,
        }
    )

    # 2. 确定收集模式
    is_dynamic_mode = input_data.mode in ("brainstorm", "progressive")

    # 3. 计算总步骤数
    if is_dynamic_mode:
        total_steps = 100  # 开放式收集，没有固定步骤数
    else:
        from ...constants import BASIC_REQUIREMENT_STEPS, COMPLETE_REQUIREMENT_STEPS

        all_steps = BASIC_REQUIREMENT_STEPS.copy()
        if input_data.mode == "complete":
            all_steps.extend(COMPLETE_REQUIREMENT_STEPS)
        total_steps = len(all_steps)

    # 4. 处理会话ID
    current_session_id = (
        input_data.session_id or ctx.session_id or f"req_{datetime.now(tz.utc).isoformat()}"
    )

    # 5. 使用 SessionStateManager 获取或创建会话状态
    state_manager = SessionStateManager(ctx, current_session_id)
    session_state = await state_manager.get_or_create(
        mode=input_data.mode,
        total_steps=total_steps,
        current_step_index=0,
    )

    return input_data, is_dynamic_mode, total_steps, current_session_id, session_state
