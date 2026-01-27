"""工具验证辅助函数.

提供通用的 Pydantic 输入验证和错误处理辅助函数。
"""

from typing import Any, TypeVar

from pydantic import BaseModel, ValidationError

# 泛型类型，用于 Pydantic 模型
T = TypeVar("T", bound=BaseModel)


def validate_input(
    model_class: type[T],
    **kwargs: Any,
) -> T:
    """验证输入参数并返回 Pydantic 模型实例.

    通用的输入验证辅助函数，避免在每个工具中重复
    model_validate 调用。

    Args:
        model_class: Pydantic 模型类
        **kwargs: 要验证的输入参数

    Returns:
        验证后的模型实例

    Raises:
        ValidationError: 输入验证失败时抛出
        ValueError: 其他验证错误时抛出

    Examples:
        >>> input_data = validate_input(
        ...     InitSkillInput,
        ...     name="my-skill",
        ...     template="minimal"
        ... )
    """
    try:
        return model_class.model_validate(kwargs)
    except ValidationError as e:
        # 转换为 ValueError 以便统一处理
        raise ValueError(f"输入验证失败: {e}") from e


def format_validation_error(
    error: Exception,
    error_type: str = "validation_error",
) -> dict[str, Any]:
    """格式化验证错误为统一返回格式.

    Args:
        error: 异常对象
        error_type: 错误类型标识

    Returns:
        统一格式的错误返回字典
    """
    return {
        "success": False,
        "error": str(error),
        "error_type": error_type,
    }


def format_internal_error(
    error: Exception,
    context: str = "操作",
) -> dict[str, Any]:
    """格式化内部错误为统一返回格式.

    Args:
        error: 异常对象
        context: 错误上下文描述

    Returns:
        统一格式的错误返回字典
    """
    return {
        "success": False,
        "error": f"{context}过程出错: {error}",
        "error_type": "internal_error",
    }


__all__ = [
    "validate_input",
    "format_validation_error",
    "format_internal_error",
]
