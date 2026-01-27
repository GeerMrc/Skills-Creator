"""Elicit 模式收集工作流模块.

提供使用 ctx.elicit() 的自动收集功能。
"""

from typing import Any

from fastmcp import Context


async def _initialize_session(
    ctx: Context,
    session_state: Any,
    current_session_id: str,
) -> None:
    """初始化会话状态.

    Args:
        ctx: MCP 上下文
        session_state: 会话状态对象
        current_session_id: 会话ID
    """
    if session_state.current_step_index == 0 and not session_state.answers:
        await ctx.set_state(  # type: ignore[func-returns-value]
            f"requirement_{current_session_id}", session_state.model_dump()
        )


async def _get_question_data(
    ctx: Context,
    session_state: Any,
    is_dynamic_mode: bool,
    all_steps: list[dict[str, Any]] | None,
    input_data: Any,
) -> dict[str, Any]:
    """获取当前问题数据.

    Args:
        ctx: MCP 上下文
        session_state: 会话状态对象
        is_dynamic_mode: 是否为动态模式
        all_steps: 预定义步骤列表
        input_data: 输入数据对象

    Returns:
        包含问题数据的字典: {
            "question_text": str,
            "prompt_text": str,
            "validation": ValidationRule | None,
            "answer_key": str,
            "step_title": str,
            "should_break": bool,
            "error": str | None
        }
    """
    from ...models.skill_config import RequirementStep, ValidationRule

    if is_dynamic_mode:
        # 动态模式：使用 LLM 生成问题
        if input_data.mode == "brainstorm":
            from .llm_services import _generate_brainstorm_question

            history: list[dict[str, str]] = session_state.conversation_history
            question_result = await _generate_brainstorm_question(
                ctx, session_state.answers, history
            )
            question_text = question_result.get("question", "")
            return {
                "question_text": question_text,
                "prompt_text": question_text,
                "validation": None,
                "answer_key": f"answer_{session_state.current_step_index}",
                "step_title": f"Brainstorm 问题 {session_state.current_step_index + 1}",
                "should_break": False,
                "error": None,
            }

        elif input_data.mode == "progressive":
            from .llm_services import _generate_progressive_question

            question_result = await _generate_progressive_question(
                ctx, session_state.answers
            )
            question_text = question_result.get("next_question", "")
            return {
                "question_text": question_text,
                "prompt_text": question_text,
                "validation": None,
                "answer_key": question_result.get(
                    "question_key", f"answer_{session_state.current_step_index}"
                ),
                "step_title": f"Progressive 问题 {session_state.current_step_index + 1}",
                "should_break": False,
                "error": None,
            }

        else:
            return {
                "question_text": "",
                "prompt_text": "",
                "validation": None,
                "answer_key": "",
                "step_title": "",
                "should_break": True,
                "error": f"未知的动态模式: {input_data.mode}",
            }

    else:
        # 静态模式：使用预定义步骤
        if all_steps is None or session_state.current_step_index >= len(all_steps):
            # 所有步骤已完成
            return {
                "question_text": "",
                "prompt_text": "",
                "validation": None,
                "answer_key": "",
                "step_title": "",
                "should_break": True,
                "error": None,
            }

        current_step_data = all_steps[session_state.current_step_index]
        validation_data: dict[str, Any] = dict(current_step_data["validation"])  # type: ignore[arg-type]
        step = RequirementStep(
            key=str(current_step_data["key"]),
            title=str(current_step_data["title"]),
            prompt=str(current_step_data["prompt"]),
            validation=ValidationRule(**validation_data),
        )

        return {
            "question_text": step.prompt,
            "prompt_text": step.prompt,
            "validation": step.validation,
            "answer_key": step.key,
            "step_title": step.title,
            "should_break": False,
            "error": None,
        }


async def _elicit_with_retry(
    ctx: Context,
    prompt_text: str,
    step_title: str,
    validation: Any | None,
    is_dynamic_mode: bool,
    max_retries: int = 3,
) -> dict[str, Any]:
    """带重试的 elicit 调用.

    Args:
        ctx: MCP 上下文
        prompt_text: 提示文本
        step_title: 步骤标题
        validation: 验证规则
        is_dynamic_mode: 是否为动态模式
        max_retries: 最大重试次数

    Returns:
        包含结果的字典: {
            "success": bool,
            "answer": str | None,
            "error": str | None,
            "action": str | None
        }
    """
    from .validation import _validate_requirement_answer

    user_answer = None
    retry_count = 0
    validation_error = None

    while retry_count <= max_retries:
        # 构建提示文本
        if validation_error and not is_dynamic_mode:
            elicit_prompt = (
                f"{prompt_text}\n\n⚠️ 输入验证失败: {validation_error}\n请重新输入："
            )
        else:
            elicit_prompt = f"{step_title}\n\n{prompt_text}"

        # 调用 elicit
        try:
            result = await ctx.elicit(elicit_prompt)  # type: ignore[call-arg]

            # 检查用户是否接受了输入请求
            if hasattr(result, "accepted") and not result.accepted:  # type: ignore[union-attr]
                return {
                    "success": False,
                    "answer": None,
                    "error": "用户取消了输入",
                    "action": "cancelled",
                }

            # 获取用户输入
            user_answer = (
                str(getattr(result, "data", "")) if hasattr(result, "data") else ""
            )

        except Exception as e:
            return {
                "success": False,
                "answer": None,
                "error": f"elicit 调用失败: {e}",
                "action": None,
            }

        # 验证输入（仅非动态模式）
        if not is_dynamic_mode and validation:
            validation_result = _validate_requirement_answer(user_answer, validation)
            if not validation_result["valid"]:
                validation_error = validation_result["error"]
                retry_count += 1
                continue

        # 验证通过或动态模式，退出重试循环
        break

    # 检查是否超过最大重试次数
    if retry_count > max_retries:
        return {
            "success": False,
            "answer": None,
            "error": f"输入验证失败超过 {max_retries} 次",
            "action": None,
        }

    return {
        "success": True,
        "answer": user_answer,
        "error": None,
        "action": None,
    }


async def _save_answer_and_advance(
    ctx: Context,
    session_state: Any,
    current_session_id: str,
    answer_key: str,
    user_answer: str,
    is_dynamic_mode: bool,
    input_data: Any,
    all_steps: list[dict[str, Any]] | None,
) -> bool:
    """保存答案并前进到下一步.

    Args:
        ctx: MCP 上下文
        session_state: 会话状态对象
        current_session_id: 会话ID
        answer_key: 答案键
        user_answer: 用户答案
        is_dynamic_mode: 是否为动态模式
        input_data: 输入数据对象
        all_steps: 预定义步骤列表

    Returns:
        是否应该继续收集
    """
    # 保存答案
    session_state.answers[answer_key] = user_answer  # type: ignore[index]

    # 更新对话历史（用于 brainstorm 模式）
    if is_dynamic_mode and input_data.mode == "brainstorm":
        session_state.conversation_history.append({"role": "user", "content": str(user_answer)})

    # 移动到下一步
    session_state.current_step_index += 1

    # 保存会话状态
    await ctx.set_state(  # type: ignore[func-returns-value]
        f"requirement_{current_session_id}", session_state.model_dump()
    )

    # 检查是否完成
    if is_dynamic_mode:
        # 动态模式：检查是否达到足够的轮次
        if session_state.current_step_index >= 5:  # 默认收集 5 轮
            session_state.completed = True
    else:
        # 静态模式：检查是否完成所有步骤
        if session_state.current_step_index >= len(all_steps):  # type: ignore[arg-type]
            session_state.completed = True

    return not session_state.completed


def _build_completion_result(
    session_state: Any,
    current_session_id: str,
    is_dynamic_mode: bool,
) -> dict[str, Any]:
    """构建完成结果.

    Args:
        session_state: 会话状态对象
        current_session_id: 会话ID
        is_dynamic_mode: 是否为动态模式

    Returns:
        完成结果字典
    """
    progress = (
        100.0
        if session_state.completed
        else (session_state.current_step_index / session_state.total_steps) * 100
    )

    return {
        "success": True,
        "session_id": current_session_id,
        "action": "complete",
        "mode": session_state.mode,
        "step_index": session_state.current_step_index,
        "total_steps": session_state.total_steps,
        "progress": progress,
        "answers": session_state.answers,
        "conversation_history": session_state.conversation_history,
        "completed": session_state.completed,
        "message": "需求收集完成（使用 elicit 模式）",
        "is_dynamic_mode": is_dynamic_mode,
    }


async def _collect_with_elicit(
    ctx: Context,
    session_state: Any,
    current_session_id: str,
    is_dynamic_mode: bool,
    all_steps: list[dict[str, Any]] | None,
    input_data: Any,
    max_retries: int = 3,
) -> dict[str, Any]:
    """使用 ctx.elicit() 自动收集所有用户输入.

    这是一个内部辅助函数，实现了完整的 elicit 循环逻辑：
    1. 生成或获取下一个问题
    2. 调用 ctx.elicit() 获取用户输入
    3. 验证输入
    4. 保存答案并继续，或重新请求输入（验证失败时）

    Args:
        ctx: MCP 上下文
        session_state: 会话状态对象
        current_session_id: 会话ID
        is_dynamic_mode: 是否为动态模式（brainstorm/progressive）
        all_steps: 预定义步骤列表（仅 basic/complete 模式）
        input_data: 输入数据对象
        max_retries: 验证失败时的最大重试次数

    Returns:
        包含收集结果的字典
    """
    try:
        # 初始化会话
        await _initialize_session(ctx, session_state, current_session_id)

        # 主收集循环
        while not session_state.completed:
            # 获取当前问题数据
            question_data = await _get_question_data(
                ctx, session_state, is_dynamic_mode, all_steps, input_data
            )

            # 检查是否需要中断
            if question_data["should_break"]:
                if question_data["error"]:
                    return {
                        "success": False,
                        "error": question_data["error"],
                        "session_id": current_session_id,
                    }
                # 所有步骤完成，退出循环
                break

            # 调用 elicit 获取用户输入（带验证重试）
            elicit_result = await _elicit_with_retry(
                ctx,
                question_data["prompt_text"],
                question_data["step_title"],
                question_data["validation"],
                is_dynamic_mode,
                max_retries,
            )

            # 处理 elicit 结果
            if not elicit_result["success"]:
                if elicit_result["action"] == "cancelled":
                    await ctx.set_state(  # type: ignore[func-returns-value]
                        f"requirement_{current_session_id}", session_state.model_dump()
                    )
                    return {
                        "success": False,
                        "action": "cancelled",
                        "message": elicit_result["error"],
                        "session_id": current_session_id,
                        "step_index": session_state.current_step_index,
                        "answers": session_state.answers,
                        "conversation_history": session_state.conversation_history,
                        "progress": (
                            session_state.current_step_index / session_state.total_steps
                        )
                        * 100,
                    }
                # 其他错误
                return {
                    "success": False,
                    "error": elicit_result["error"],
                    "session_id": current_session_id,
                    "message": elicit_result["error"],
                }

            # 保存答案并前进到下一步
            should_continue = await _save_answer_and_advance(
                ctx,
                session_state,
                current_session_id,
                question_data["answer_key"],
                elicit_result["answer"],
                is_dynamic_mode,
                input_data,
                all_steps,
            )

            if not should_continue:
                break

        # 返回完成结果
        return _build_completion_result(session_state, current_session_id, is_dynamic_mode)

    except Exception as e:
        return {
            "success": False,
            "error": f"elicit 模式收集出错: {e}",
            "error_type": "elicit_error",
            "message": f"内部错误: {e}",
            "session_id": current_session_id,
        }
