"""需求收集辅助函数.

此模块包含 `collect_requirements` 工具的辅助函数。
这些函数处理需求收集的各种模式（basic/complete/brainstorm/progressive）和操作。
"""

import json
import re
from datetime import datetime
from datetime import timezone as tz
from typing import Any

from fastmcp import Context


class SessionStateManager:
    """会话状态管理器.

    集中管理会话状态的加载、保存和更新操作。
    """

    def __init__(self, ctx: Context, session_id: str, state_prefix: str = "requirement_"):
        """初始化会话状态管理器.

        Args:
            ctx: MCP 上下文
            session_id: 会话ID
            state_prefix: 状态键前缀，默认为 "requirement_"
        """
        self.ctx = ctx
        self.session_id = session_id
        self.state_prefix = state_prefix
        self._state: Any | None = None
        self._state_key = f"{state_prefix}{session_id}"

    async def load(self) -> Any:
        """加载会话状态.

        Returns:
            会话状态对象，如果不存在则返回 None
        """
        if self._state is None:
            state_data = await self.ctx.get_state(self._state_key)
            if state_data:
                from ..models.skill_config import SessionState

                self._state = SessionState.model_validate(state_data)
        return self._state

    async def save(self) -> None:
        """保存会话状态."""
        if self._state:
            await self.ctx.set_state(  # type: ignore[func-returns-value]
                self._state_key, self._state.model_dump()
            )

    async def create(
        self,
        mode: str,
        total_steps: int,
        current_step_index: int = 0,
    ) -> Any:
        """创建新的会话状态.

        Args:
            mode: 收集模式
            total_steps: 总步骤数
            current_step_index: 当前步骤索引

        Returns:
            新创建的会话状态对象
        """
        from ..models.skill_config import SessionState

        self._state = SessionState(
            current_step_index=current_step_index,
            answers={},
            started_at=datetime.now(tz.utc).isoformat(),
            completed=False,
            mode=mode,  # type: ignore[arg-type]
            total_steps=total_steps,
        )
        await self.save()
        return self._state

    async def get_or_create(
        self,
        mode: str,
        total_steps: int,
        current_step_index: int = 0,
    ) -> Any:
        """获取或创建会话状态.

        Args:
            mode: 收集模式
            total_steps: 总步骤数
            current_step_index: 当前步骤索引

        Returns:
            会话状态对象
        """
        state = await self.load()
        if state is None:
            state = await self.create(mode, total_steps, current_step_index)
        return state

    async def update(self, **updates: Any) -> None:
        """更新会话状态字段.

        Args:
            **updates: 要更新的字段和值
        """
        state = await self.load()
        if state:
            for key, value in updates.items():
                if hasattr(state, key):
                    setattr(state, key, value)
            await self.save()

    @property
    def state(self) -> Any | None:
        """获取当前会话状态（不触发加载）."""
        return self._state

    @property
    def key(self) -> str:
        """获取状态键."""
        return self._state_key


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
    from ..models.skill_config import RequirementStep, ValidationRule

    if is_dynamic_mode:
        # 动态模式：使用 LLM 生成问题
        if input_data.mode == "brainstorm":
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
    from datetime import datetime
    from datetime import timezone as tz

    from ..models.skill_config import RequirementCollectionInput

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
        from ..constants import BASIC_REQUIREMENT_STEPS, COMPLETE_REQUIREMENT_STEPS

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


def _get_requirement_mode_steps(mode: str) -> list[dict[str, Any]]:
    """获取指定模式的步骤列表.

    Args:
        mode: 收集模式 (basic/complete/brainstorm/progressive)

    Returns:
        步骤列表（动态模式返回空列表）
    """
    if mode in ("brainstorm", "progressive"):
        return []

    from ..constants import BASIC_REQUIREMENT_STEPS, COMPLETE_REQUIREMENT_STEPS

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
    from ..models.skill_config import RequirementStep, ValidationRule

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
    from datetime import datetime
    from datetime import timezone as tz

    from ..models.skill_config import SessionState

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
    from ..models.skill_config import RequirementStep, ValidationRule

    # 动态模式：使用 LLM 生成问题
    if is_dynamic_mode:
        if mode == "brainstorm":
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
    from ..models.skill_config import RequirementStep, ValidationRule

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
