"""路径处理辅助函数.

提供统一的路径处理工具，确保跨平台兼容性和配置一致性。
"""

from pathlib import Path


def normalize_path(path: str | Path) -> Path:
    """规范化路径，处理 ~ 和相对路径.

    Args:
        path: 输入路径

    Returns:
        规范化后的绝对路径
    """
    return Path(path).expanduser().resolve()


def get_default_output_dir() -> Path:
    """获取默认输出目录.

    优先级:
    1. SKILL_CREATOR_DEFAULT_OUTPUT_DIR 环境变量
    2. ~/agent-skills

    Returns:
        默认输出目录路径
    """
    import os

    default_output = os.getenv("SKILL_CREATOR_DEFAULT_OUTPUT_DIR", "~/agent-skills")
    return Path(default_output).expanduser().resolve()


def get_output_dir(fallback: bool = True) -> Path:
    """获取输出目录.

    Args:
        fallback: 如果未设置，是否使用默认值

    Returns:
        输出目录路径

    Raises:
        ValueError: 如果未设置且 fallback=False
    """
    import os

    output_dir_value = os.getenv("SKILL_CREATOR_OUTPUT_DIR")
    if output_dir_value:
        return Path(output_dir_value).expanduser().resolve()
    if fallback:
        return get_default_output_dir()
    raise ValueError("必须设置 SKILL_CREATOR_OUTPUT_DIR 环境变量")


def join_paths(*parts: str | Path) -> Path:
    """安全地拼接多个路径部分.

    Args:
        *parts: 路径部分

    Returns:
        拼接后的路径
    """
    result = Path(parts[0])
    for part in parts[1:]:
        result = result / part
    return result


def split_path_parts(path: str | Path) -> tuple[str, ...]:
    """获取路径的各个部分.

    Args:
        path: 输入路径

    Returns:
        路径的各个部分组成的元组
    """
    return Path(path).parts
