"""需求收集辅助函数.

此模块包含 `collect_requirements` 工具的辅助函数。
这些函数处理需求收集的各种模式（basic/complete/brainstorm/progressive）和操作。

这是子包的入口点，重导出所有公共 API 以保持向后兼容性。
"""

# 会话状态管理
# 操作处理器
from .actions import (
    _get_requirement_mode_steps,
    _handle_requirement_previous_action,
    _handle_requirement_start_action,
    _handle_requirement_status_action,
)

# Elicit 工作流
from .elicit_workflow import _collect_with_elicit

# LLM 服务（内部使用，但需要重导出）
from .llm_services import (
    _check_requirement_completeness,
    _generate_brainstorm_question,
    _generate_progressive_question,
)

# 问题生成
from .questions import _get_requirement_next_question
from .session_manager import SessionStateManager

# 验证和答案处理
from .validation import (
    _process_requirement_user_answer,
    _validate_and_init_requirement_session,
    _validate_requirement_answer,
)

__all__ = [
    # 会话状态管理
    "SessionStateManager",
    # Elicit 工作流
    "_collect_with_elicit",
    # 操作处理器
    "_get_requirement_mode_steps",
    "_handle_requirement_previous_action",
    "_handle_requirement_start_action",
    "_handle_requirement_status_action",
    # 问题生成
    "_get_requirement_next_question",
    # 验证和答案处理
    "_process_requirement_user_answer",
    "_validate_and_init_requirement_session",
    "_validate_requirement_answer",
    # LLM 服务
    "_check_requirement_completeness",
    "_generate_brainstorm_question",
    "_generate_progressive_question",
]
