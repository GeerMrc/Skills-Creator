"""路径处理辅助函数测试."""

import tempfile

import pytest
from pathlib import Path

from skill_creator_mcp.utils.path_helpers import (
    ensure_output_dir,
    get_default_output_dir,
    normalize_path,
)


def test_normalize_path():
    """测试路径规范化."""
    # 测试 ~ 展开
    path = normalize_path("~/test")
    assert path.is_absolute()
    assert str(path) == str(Path.home() / "test")

    # 测试相对路径
    path = normalize_path("./test")
    assert path.is_absolute()


def test_ensure_output_dir_creates_missing_directory():
    """测试 ensure_output_dir 自动创建缺失目录."""
    with tempfile.TemporaryDirectory() as tmpdir:
        missing_dir = Path(tmpdir) / "a" / "b" / "skills"
        assert not missing_dir.exists()

        result = ensure_output_dir(missing_dir)

        assert result.exists()
        assert result.is_dir()


def test_ensure_output_dir_expands_tilde():
    """测试 ensure_output_dir 展开 ~."""
    result = ensure_output_dir("~/test_skills")
    assert str(Path.home()) in str(result)
    assert "test_skills" in str(result)


def test_ensure_output_dir_validates_existing_dir():
    """测试 ensure_output_dir 验证现有目录."""
    with tempfile.TemporaryDirectory() as tmpdir:
        # 测试目录
        result = ensure_output_dir(tmpdir)
        assert result == Path(tmpdir).resolve()

        # 测试文件（应报错）
        test_file = Path(tmpdir) / "not_a_dir"
        test_file.write_text("content")

        with pytest.raises(ValueError, match="不是目录"):
            ensure_output_dir(test_file)


def test_ensure_output_dir_raises_on_not_writable():
    """测试 ensure_output_dir 对不可写目录报错."""
    import stat

    with tempfile.TemporaryDirectory() as tmpdir:
        readonly_dir = Path(tmpdir) / "readonly"
        readonly_dir.mkdir()

        try:
            # 设置只读权限
            readonly_dir.chmod(stat.S_IRUSR | stat.S_IXUSR)

            with pytest.raises(ValueError, match="不可写"):
                ensure_output_dir(readonly_dir)
        finally:
            # 恢复权限以便清理
            readonly_dir.chmod(stat.S_IRWXU)


def test_get_default_output_dir_uses_env_var():
    """测试 get_default_output_dir 读取环境变量."""
    import os

    # 设置环境变量
    original_value = os.environ.get("SKILL_CREATOR_DEFAULT_OUTPUT_DIR")
    os.environ["SKILL_CREATOR_DEFAULT_OUTPUT_DIR"] = "/tmp/test_skills"

    try:
        result = get_default_output_dir()
        # 验证路径包含 test_skills
        assert "test_skills" in str(result)
    finally:
        # 恢复原始值
        if original_value is None:
            del os.environ["SKILL_CREATOR_DEFAULT_OUTPUT_DIR"]
        else:
            os.environ["SKILL_CREATOR_DEFAULT_OUTPUT_DIR"] = original_value


def test_get_default_output_dir_creates_home_skills():
    """测试 get_default_output_dir 创建 ~/skills."""
    import os
    import shutil

    # 清除环境变量，使用默认值
    original_value = os.environ.get("SKILL_CREATOR_DEFAULT_OUTPUT_DIR")
    if "SKILL_CREATOR_DEFAULT_OUTPUT_DIR" in os.environ:
        del os.environ["SKILL_CREATOR_DEFAULT_OUTPUT_DIR"]

    test_skills_dir = Path.home() / "test_skills_for_unit_test"

    try:
        # 确保测试目录开始时不存在
        if test_skills_dir.exists():
            shutil.rmtree(test_skills_dir)

        result = get_default_output_dir()

        # 验证路径包含 skills
        assert "skills" in str(result).lower()
        # 验证目录已创建
        assert result.exists()
        assert result.is_dir()
    finally:
        # 清理测试目录
        if test_skills_dir.exists():
            shutil.rmtree(test_skills_dir)
        # 恢复环境变量
        if original_value is not None:
            os.environ["SKILL_CREATOR_DEFAULT_OUTPUT_DIR"] = original_value
