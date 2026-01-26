# 硬编码路径问题全面修复计划

> **计划日期**: 2026-01-26
> **计划类型**: 全面重构 - 消除所有硬编码路径
> **优先级**: P0 (阻塞性问题)
> **相关 Issue**: 用户反馈 - generating-presentations Agent-Skill 开发时输出目录配置未生效
> **修复策略**: 激进修复 - 不考虑向后兼容，全面统一配置机制

---

## 一、问题概述

### 1.1 用户报告的问题

用户在 `~/test/tmp/` 目录下开发 `generating-presentations` Agent-Skill 时发现：

1. **Git 仓库未初始化** - 开发目录下没有 Git 仓库
2. **目标目录不存在** - `~/.claude/skills/generating-presentations/` 不存在
3. **python-pptx 未安装** - 缺少依赖包
4. **核心问题**: 虽然期望在当前项目目录下开发，但实际仍然操作的是 `~/.claude/skills/` 目录

### 1.2 用户期望

- 在当前项目开发目录（如 `~/test/tmp/`）下创建和开发 Agent-Skill
- 通过设置环境变量 `SKILL_CREATOR_OUTPUT_DIR` 统一管理输出位置
- 不需要在 `~/.claude/skills/` 目录下操作

### 1.3 修复原则

**用户明确指示**:
- ✅ 不考虑向后兼容问题（有 git commit 可以回退）
- ✅ 必须全面审核避免还有类似硬编码导致类似的 bug
- ✅ 优化完善计划后再推进

---

## 二、全面审核结果

### 2.1 问题统计

| 严重程度 | 数量 | 类型 |
|----------|------|------|
| P0 | 3 | Pydantic 模型硬编码、环境变量默认值、文档路径 |
| P1 | 3 | 测试路径、缓存配置、日志路径 |
| P2 | 2 | 配置文件路径、虚拟环境名称 |
| P3 | 2 | 打包排除模式、文档占位符 |
| **额外发现** | **12** | 路径分隔符硬编码（4处）、f-string 路径拼接（8处） |
| **总计** | **22** | - |

### 2.2 P0 严重问题详情

#### 问题 1: Pydantic 模型中硬编码的默认值

**文件**: `skill-creator-mcp/src/skill_creator_mcp/models/skill_config.py`

**位置**: 3 处
- `InitSkillInput` (line 27-30)
- `PackageSkillInput` (line 464-467)
- `PackageAgentSkillInput` (line 563-566)

**问题代码**:
```python
output_dir: str = Field(
    default=".",  # ❌ 硬编码
    description="输出目录路径",
)
```

**影响**:
- 模型默认值与 `SKILL_CREATOR_OUTPUT_DIR` 环境变量不一致
- 当用户不提供参数时，模型默认使用 "." 而不是读取环境变量
- 导致环境变量配置在 Pydantic 验证层面失效

---

#### 问题 2: 环境变量默认值硬编码为当前目录

**文件**: `skill-creator-mcp/src/skill_creator_mcp/config.py:43`

**问题代码**:
```python
self._output_dir: Path = Path(os.getenv("SKILL_CREATOR_OUTPUT_DIR", "."))
```

**影响**:
- 默认值 "." 依赖于 MCP Server 启动时的当前工作目录
- 在不同工作目录启动时行为不一致
- 无法预测默认输出位置

---

#### 问题 3: 文档中硬编码的示例路径

**文件**:
- `skill-creator-mcp/docs/mcp-config-guide.md`
- `skill-creator/references/mcp-integration.md`

**问题代码**:
```markdown
/home/user/projects/my-skill/
/home/user/Skills-Creator/
"SKILL_CREATOR_OUTPUT_DIR": "/home/user/development/shared-skills"
```

**影响**:
- 用户可能直接复制使用这些路径
- 在不同操作系统或用户环境下无效
- 误导用户配置

---

### 2.3 P1 高优先级问题详情

#### 问题 4: 测试中硬编码的临时路径

**文件**: `skill-creator-mcp/tests/test_tools/test_config.py:50`

**问题代码**:
```python
os.environ["SKILL_CREATOR_LOG_FILE"] = "/tmp/test.log"
```

**影响**:
- 测试在某些环境下可能失败（权限问题）
- 可能污染系统临时目录
- 跨平台兼容性问题（Windows 没有 /tmp）

---

#### 问题 5: 缓存大小硬编码

**文件**: `skill-creator-mcp/src/skill_creator_mcp/utils/cache.py:36`

**问题代码**:
```python
def __init__(self, max_size: int = 128, default_ttl: int = 3600):
```

**影响**:
- 无法根据环境调整缓存大小
- 128 个条目可能不足或过多
- TTL 3600 秒（1小时）可能不适合所有场景

---

#### 问题 6: 日志文件路径示例硬编码

**文件**: `skill-creator-mcp/.env.example:12`

**问题代码**:
```bash
SKILL_CREATOR_LOG_FILE=/var/log/skill-creator-mcp.log
```

**影响**:
- /var/log 需要特殊权限
- 用户可能无法创建日志文件
- 跨平台兼容性差

---

### 2.4 路径分隔符硬编码（额外发现）

**文件**: `skill-creator-mcp/src/skill_creator_mcp/utils/packagers.py`

**位置**: 4 处 (line 218, 224, 227, 233)

**问题代码**:
```python
# line 218
parts = path_str.split("/") if "/" in path_str else path_str.split(os.sep)

# line 224
if pattern in path_str or pattern in path_str.replace("/", os.sep):

# line 227
parts = path_str.split("/") if "/" in path_str else path_str.split(os.sep)

# line 233
parts = path_str.split("/") if "/" in path_str else path_str.split(os.sep)
```

**影响**:
- 硬编码了 Unix 风格的路径分隔符
- 在 Windows 系统上可能产生意外行为
- 虽然有 `os.sep` 的回退逻辑，但不优雅

---

### 2.5 f-string 路径拼接（额外发现）

**文件**:
- `skill-creator/examples/github-automation.md`
- `skill-creator/examples/thinking-analysis.md`
- `skill-creator/examples/thinking-export.md`

**问题代码**:
```python
"content": read_file(f"{skill_name}/SKILL.md")
"content": read_file(f"{skill_name}/references/README.md")
output_path=f"{skill_path}/docs/analysis-thinking.md"
archive_dir = f"{skill_path}/docs/thinking"
```

**影响**:
- 硬编码了 `/` 分隔符
- 在 Windows 上会失败
- 示例代码没有展示最佳实践

---

### 2.6 特殊发现

**文件**: `skill-creator-mcp/src/skill_creator_mcp/utils/packagers.py:401`

**问题代码**:
```python
".claude/plans/archive",
```

**影响**:
- 计划归档目录路径硬编码
- 无法自定义归档位置

---

## 三、全面修复方案

### 3.1 修复策略

**采用激进修复策略**（不考虑向后兼容）:

1. **统一配置机制** - 所有代码路径都通过配置类获取默认值
2. **消除硬编码** - 移除所有硬编码的路径和默认值
3. **环境变量优先** - 确保环境变量在所有场景下生效
4. **路径工具函数** - 创建统一的路径处理辅助模块
5. **改进默认行为** - 使用更合理的默认值（如 `~/agent-skills`）

### 3.2 配置架构重构

**新增配置项**:
```python
class Config:
    # 现有配置
    _output_dir: Path
    _log_file: str | None

    # 新增配置
    _default_output_dir: Path      # 默认输出目录（~/agent-skills）
    _cache_size: int               # 缓存大小（默认 128）
    _cache_ttl: int                # 缓存 TTL（默认 3600）
    _plan_archive_dir: Path        # 计划归档目录
```

**环境变量支持**:
```bash
SKILL_CREATOR_OUTPUT_DIR          # 输出目录
SKILL_CREATOR_DEFAULT_OUTPUT_DIR  # 默认输出目录（当 OUTPUT_DIR 未设置时）
SKILL_CREATOR_CACHE_SIZE          # 缓存大小
SKILL_CREATOR_CACHE_TTL           # 缓存 TTL
SKILL_CREATOR_PLAN_ARCHIVE_DIR    # 计划归档目录
```

### 3.3 路径工具模块

**新增文件**: `skill-creator-mcp/src/skill_creator_mcp/utils/path_helpers.py`

```python
"""路径处理辅助函数.

提供统一的路径处理工具，确保跨平台兼容性和配置一致性。
"""

from pathlib import Path
from typing import Union

from ..config import get_config


def normalize_path(path: Union[str, Path]) -> Path:
    """规范化路径，处理 ~ 和相对路径."""
    return Path(path).expanduser().resolve()


def get_default_output_dir() -> Path:
    """获取默认输出目录.

    优先级:
    1. SKILL_CREATOR_DEFAULT_OUTPUT_DIR 环境变量
    2. ~/agent-skills
    """
    config = get_config()
    if hasattr(config, 'default_output_dir') and config.default_output_dir:
        return config.default_output_dir
    return Path("~/agent-skills").expanduser()


def get_output_dir(fallback: bool = True) -> Path:
    """获取输出目录.

    Args:
        fallback: 如果未设置，是否使用默认值

    Returns:
        输出目录路径

    Raises:
        ValueError: 如果未设置且 fallback=False
    """
    config = get_config()
    if config.output_dir:
        return config.output_dir
    if fallback:
        return get_default_output_dir()
    raise ValueError("必须设置 SKILL_CREATOR_OUTPUT_DIR 环境变量")


def join_paths(*parts: Union[str, Path]) -> Path:
    """安全地拼接多个路径部分."""
    result = Path(parts[0])
    for part in parts[1:]:
        result = result / part
    return result


def split_path_parts(path: Union[str, Path]) -> tuple[str, ...]:
    """获取路径的各个部分."""
    return Path(path).parts
```

---

## 四、详细修复任务清单

### 任务 1: 修复 Pydantic 模型硬编码（P0）

**文件**: `skill-creator-mcp/src/skill_creator_mcp/models/skill_config.py`

**修改内容**:

#### 1.1 修改 InitSkillInput (line 27-30)

```python
# 修改前
output_dir: str = Field(
    default=".",
    description="输出目录路径",
)

# 修改后
output_dir: str | None = Field(
    default=None,
    description="输出目录路径（默认使用 SKILL_CREATOR_OUTPUT_DIR 环境变量）",
)
```

#### 1.2 添加字段验证器

```python
@field_validator("output_dir", mode="before")
@classmethod
def apply_default_output_dir(cls, v: str | None) -> str:
    """应用默认输出目录."""
    if v is None:
        from ...utils.path_helpers import get_output_dir
        return str(get_output_dir(fallback=True))
    return v
```

#### 1.3 修改 PackageSkillInput (line 464-467)

```python
# 修改前
output_dir: str = Field(
    default=".",
    description="输出目录路径",
)

# 修改后
output_dir: str | None = Field(
    default=None,
    description="输出目录路径（默认使用 SKILL_CREATOR_OUTPUT_DIR 环境变量）",
)

# 添加相同的字段验证器
```

#### 1.4 修改 PackageAgentSkillInput (line 563-566)

```python
# 修改前
output_dir: str = Field(
    default=".",
    description="输出目录路径",
)

# 修改后
output_dir: str | None = Field(
    default=None,
    description="输出目录路径（默认使用 SKILL_CREATOR_OUTPUT_DIR 环境变量）",
)

# 添加相同的字段验证器
```

---

### 任务 2: 改进配置类默认值（P0）

**文件**: `skill-creator-mcp/src/skill_creator_mcp/config.py`

**修改内容**:

#### 2.1 添加新的环境变量文档

```python
"""
SKILL_CREATOR_DEFAULT_OUTPUT_DIR: 默认输出目录（当 OUTPUT_DIR 未设置时）
    - 推荐值：~/agent-skills
    - 优先级：环境变量 > ~/agent-skills

SKILL_CREATOR_CACHE_SIZE: 缓存最大条目数
    - 默认值：128
    - 推荐值：根据内存调整（64-512）

SKILL_CREATOR_CACHE_TTL: 缓存过期时间（秒）
    - 默认值：3600（1小时）
    - 推荐值：根据数据更新频率调整

SKILL_CREATOR_PLAN_ARCHIVE_DIR: 计划归档目录
    - 默认值：.claude/plans/archive
"""
```

#### 2.2 更新 Config 类

```python
class Config:
    """配置类，从环境变量读取设置."""

    def __init__(self) -> None:
        """初始化配置，从环境变量读取所有设置."""
        # 日志配置
        self._log_level: LogLevel = os.getenv(  # type: ignore[assignment]
            "SKILL_CREATOR_LOG_LEVEL", "INFO"
        )
        self._log_format: LogFormat = os.getenv(  # type: ignore[assignment]
            "SKILL_CREATOR_LOG_FORMAT", "default"
        )
        self._log_file: str | None = os.getenv("SKILL_CREATOR_LOG_FILE")

        # 工作目录配置
        # 新逻辑：优先使用 SKILL_CREATOR_OUTPUT_DIR，否则使用 SKILL_CREATOR_DEFAULT_OUTPUT_DIR 或 ~/agent-skills
        default_output = os.getenv(
            "SKILL_CREATOR_DEFAULT_OUTPUT_DIR",
            "~/agent-skills"
        )
        output_dir_value = os.getenv("SKILL_CREATOR_OUTPUT_DIR", default_output)
        self._output_dir: Path = Path(output_dir_value).expanduser().resolve()

        # 新增：默认输出目录
        self._default_output_dir: Path = Path(default_output).expanduser().resolve()

        # 操作配置
        self._max_retries: int = int(os.getenv("SKILL_CREATOR_MAX_RETRIES", "3"))
        self._timeout_seconds: int = int(os.getenv("SKILL_CREATOR_TIMEOUT_SECONDS", "30"))

        # 新增：缓存配置
        self._cache_size: int = int(os.getenv("SKILL_CREATOR_CACHE_SIZE", "128"))
        self._cache_ttl: int = int(os.getenv("SKILL_CREATOR_CACHE_TTL", "3600"))

        # 新增：计划归档目录
        plan_archive_value = os.getenv("SKILL_CREATOR_PLAN_ARCHIVE_DIR", ".claude/plans/archive")
        self._plan_archive_dir: Path = Path(plan_archive_value).expanduser().resolve()
```

#### 2.3 添加属性方法

```python
@property
def default_output_dir(self) -> Path:
    """获取默认输出目录."""
    return self._default_output_dir

@property
def cache_size(self) -> int:
    """获取缓存大小."""
    return self._cache_size

@property
def cache_ttl(self) -> int:
    """获取缓存过期时间（秒）."""
    return self._cache_ttl

@property
def plan_archive_dir(self) -> Path:
    """获取计划归档目录."""
    return self._plan_archive_dir
```

---

### 任务 3: 修复内部函数硬编码（P0）

**文件**: `skill-creator-mcp/src/skill_creator_mcp/utils/packagers.py`

**修改内容**:

#### 3.1 修改 package_agent_skill 函数 (line 456-463)

```python
# 修改前
def package_agent_skill(
    skill_path: str,
    output_dir: str = ".",  # ❌ 硬编码
    version: str | None = None,
    package_format: str = "zip",
    include_tests: bool = False,
    validate_before_package: bool = True,
) -> "PackageResult":

# 修改后
def package_agent_skill(
    skill_path: str,
    output_dir: str | None = None,  # ✅ 可选
    version: str | None = None,
    package_format: str = "zip",
    include_tests: bool = False,
    validate_before_package: bool = True,
) -> "PackageResult":
    from ..config import get_config
    from .path_helpers import normalize_path

    # 优先级：参数 > 环境变量 > 默认值
    if output_dir is None:
        output_dir = str(get_config().output_dir)

    # 规范化路径
    skill_dir = normalize_path(skill_path)
    out_dir = normalize_path(output_dir)
```

---

### 任务 4: 修复路径分隔符硬编码（P0）

**文件**: `skill-creator-mcp/src/skill_creator_mcp/utils/packagers.py`

**修改内容**:

#### 4.1 修改 line 218-234 的路径处理逻辑

```python
# 修改前
parts = path_str.split("/") if "/" in path_str else path_str.split(os.sep)

if pattern in path_str or pattern in path_str.replace("/", os.sep):
    # ...

# 修改后
from .path_helpers import split_path_parts

parts = split_path_parts(relative_path)

# 对于路径比较，使用 Path 对象
path_obj = Path(path_str)
pattern_obj = Path(pattern)
if pattern in str(path_obj) or pattern_obj in path_obj.parents:
    # ...
```

---

### 任务 5: 修复计划归档目录硬编码（P0）

**文件**: `skill-creator-mcp/src/skill_creator_mcp/utils/packagers.py:401`

**修改内容**:

```python
# 修改前
".claude/plans/archive",

# 修改后
from ..config import get_config
str(get_config().plan_archive_dir),
```

---

### 任务 6: 修复测试硬编码（P1）

**文件**: `skill-creator-mcp/tests/test_tools/test_config.py:50`

**修改内容**:

```python
# 修改前
os.environ["SKILL_CREATOR_LOG_FILE"] = "/tmp/test.log"

# 修改后
import tempfile
temp_log = tempfile.NamedTemporaryFile(delete=False, suffix=".log")
os.environ["SKILL_CREATOR_LOG_FILE"] = temp_log.name
try:
    # 测试代码
finally:
    temp_log.close()
    os.unlink(temp_log.name)
```

---

### 任务 7: 修复缓存配置硬编码（P1）

**文件**: `skill-creator-mcp/src/skill_creator_mcp/utils/cache.py`

**修改内容**:

```python
# 修改前 (line 36)
def __init__(self, max_size: int = 128, default_ttl: int = 3600):
    self._max_size = max_size
    self._default_ttl = default_ttl

_global_cache = MemoryCache(max_size=128, default_ttl=3600)

# 修改后
from ..config import get_config

def __init__(self, max_size: int | None = None, default_ttl: int | None = None):
    config = get_config()
    self._max_size = max_size if max_size is not None else config.cache_size
    self._default_ttl = default_ttl if default_ttl is not None else config.cache_ttl

_global_cache = MemoryCache()  # 使用配置默认值
```

---

### 任务 8: 修复日志路径示例（P1）

**文件**: `skill-creator-mcp/.env.example:12`

**修改内容**:

```bash
# 修改前
SKILL_CREATOR_LOG_FILE=/var/log/skill-creator-mcp.log

# 修改后
# 使用用户目录（推荐）
SKILL_CREATOR_LOG_FILE=~/.skill-creator-mcp.log

# 或使用相对路径
# SKILL_CREATOR_LOG_FILE=./logs/skill-creator-mcp.log

# 或留空使用默认（stderr）
# SKILL_CREATOR_LOG_FILE=
```

---

### 任务 9: 更新文档硬编码路径（P0）

**文件**:
- `skill-creator-mcp/docs/mcp-config-guide.md`
- `skill-creator/references/mcp-integration.md`

**修改内容**:

```markdown
# 修改前
/home/user/projects/my-skill/
/home/user/Skills-Creator/
"SKILL_CREATOR_OUTPUT_DIR": "/home/user/development/shared-skills"

# 修改后
~/projects/my-skill/
~/Skills-Creator/
"SKILL_CREATOR_OUTPUT_DIR": "~/development/shared-skills"
```

---

### 任务 10: 修复示例文档中的路径拼接（P1）

**文件**:
- `skill-creator/examples/github-automation.md`
- `skill-creator/examples/thinking-analysis.md`
- `skill-creator/examples/thinking-export.md`

**修改内容**:

```python
# 修改前
"content": read_file(f"{skill_name}/SKILL.md")
output_path=f"{skill_path}/docs/analysis-thinking.md"

# 修改后
from pathlib import Path
"content": read_file(str(Path(skill_name) / "SKILL.md"))
output_path=str(Path(skill_path) / "docs" / "analysis-thinking.md")
```

---

### 任务 11: 创建路径工具模块（P0）

**新增文件**: `skill-creator-mcp/src/skill_creator_mcp/utils/path_helpers.py`

**完整内容**: 见上文 3.3 节

---

### 任务 12: 更新 .env.example（P1）

**文件**: `skill-creator-mcp/.env.example`

**添加**:

```bash
# 新增：默认输出目录（当 OUTPUT_DIR 未设置时）
SKILL_CREATOR_DEFAULT_OUTPUT_DIR=~/agent-skills

# 新增：缓存配置
SKILL_CREATOR_CACHE_SIZE=128
SKILL_CREATOR_CACHE_TTL=3600

# 新增：计划归档目录
SKILL_CREATOR_PLAN_ARCHIVE_DIR=.claude/plans/archive
```

---

### 任务 13: 添加集成测试（P0）

**新增测试文件**: `skill-creator-mcp/tests/test_integration/test_config_integration.py`

**测试内容**:

```python
"""配置集成测试."""

import os
import tempfile
from pathlib import Path

import pytest

from skill_creator_mcp.config import get_config, reload_config
from skill_creator_mcp.utils.packagers import package_agent_skill
from skill_creator_mcp.models.skill_config import InitSkillInput


class TestConfigIntegration:
    """配置集成测试."""

    def test_env_var_priority(self, monkeypatch, tmp_path):
        """测试环境变量优先级."""
        env_dir = tmp_path / "env-output"
        monkeypatch.setenv("SKILL_CREATOR_OUTPUT_DIR", str(env_dir))
        reload_config()

        config = get_config()
        assert env_dir in config.output_dir.parents or config.output_dir == env_dir

    def test_default_output_dir_fallback(self, monkeypatch, tmp_path):
        """测试默认输出目录回退."""
        # 不设置 SKILL_CREATOR_OUTPUT_DIR
        monkeypatch.delenv("SKILL_CREATOR_OUTPUT_DIR", raising=False)

        # 设置 SKILL_CREATOR_DEFAULT_OUTPUT_DIR
        default_dir = tmp_path / "default-output"
        monkeypatch.setenv("SKILL_CREATOR_DEFAULT_OUTPUT_DIR", str(default_dir))
        reload_config()

        config = get_config()
        assert str(default_dir) in str(config.output_dir)

    def test_pydantic_model_respects_config(self, monkeypatch, tmp_path):
        """测试 Pydantic 模型正确读取配置."""
        env_dir = tmp_path / "pydantic-test"
        monkeypatch.setenv("SKILL_CREATOR_OUTPUT_DIR", str(env_dir))
        reload_config()

        # 不传递 output_dir，应使用环境变量
        input_data = InitSkillInput.model_validate({
            "name": "test-skill",
            # output_dir=None（使用默认）
        })

        assert str(env_dir) in input_data.output_dir

    def test_internal_function_respects_config(self, monkeypatch, tmp_path):
        """测试内部函数正确读取配置."""
        env_dir = tmp_path / "internal-test"
        monkeypatch.setenv("SKILL_CREATOR_OUTPUT_DIR", str(env_dir))
        reload_config()

        # 创建测试技能
        skill_dir = tmp_path / "test-skill"
        skill_dir.mkdir()
        (skill_dir / "SKILL.md").write_text("# Test")

        # 不传递 output_dir，应使用环境变量
        result = package_agent_skill(str(skill_dir))

        assert result.success
        assert str(env_dir) in result.package_path

    def test_path_helpers_cross_platform(self, tmp_path):
        """测试路径工具跨平台兼容性."""
        from skill_creator_mcp.utils.path_helpers import (
            normalize_path,
            join_paths,
            split_path_parts,
        )

        # 测试路径规范化
        path = normalize_path(tmp_path / "test" / "path")
        assert path.is_absolute()

        # 测试路径拼接
        joined = join_paths(tmp_path, "subdir", "file.txt")
        assert "subdir" in str(joined)
        assert "file.txt" in str(joined)

        # 测试路径分割
        parts = split_path_parts(joined)
        assert len(parts) >= 2
```

---

### 任务 14: 运行完整测试套件（P0）

**命令**:

```bash
cd skill-creator-mcp
uv run pytest --cov
uv run ruff check .
uv run ruff format --check .
uv run mypy src/
uv run bandit -r src/
```

**验收标准**:
- 所有测试通过
- 覆盖率 ≥95%
- 代码检查 0 错误
- 类型检查 0 错误
- 安全检查 0 高危

---

### 任务 15: 更新 CHANGELOG.md（P0）

**文件**: `CHANGELOG.md`

**添加**:

```markdown
## [Unreleased]

### Fixed

- **P0**: 修复 Pydantic 模型中硬编码的 `output_dir` 默认值
- **P0**: 修复内部函数 `package_agent_skill()` 硬编码默认值
- **P0**: 修复路径分隔符硬编码（`packagers.py`）
- **P0**: 修复计划归档目录硬编码
- **P1**: 修复测试中硬编码的临时路径
- **P1**: 修复缓存配置硬编码
- **P1**: 修复日志路径示例硬编码
- **P0**: 更新文档中的硬编码路径示例

### Added

- 新增 `SKILL_CREATOR_DEFAULT_OUTPUT_DIR` 环境变量
- 新增 `SKILL_CREATOR_CACHE_SIZE` 环境变量
- 新增 `SKILL_CREATOR_CACHE_TTL` 环境变量
- 新增 `SKILL_CREATOR_PLAN_ARCHIVE_DIR` 环境变量
- 新增路径处理辅助模块 `path_helpers.py`
- 新增配置集成测试

### Changed

- **BREAKING**: Pydantic 模型 `output_dir` 参数改为可选（`str | None`）
- **BREAKING**: 默认输出目录从 `.` 改为 `~/agent-skills`
- **BREAKING**: 当未设置 `SKILL_CREATOR_OUTPUT_DIR` 时，使用 `SKILL_CREATOR_DEFAULT_OUTPUT_DIR` 或 `~/agent-skills`
- 改进配置类，支持更多可配置项
- 统一配置机制，所有代码路径都通过配置类获取默认值

### Migration Notes

如果您的代码直接使用 Pydantic 模型或内部函数，需要更新：

```python
# 旧代码
input_data = InitSkillInput.model_validate({
    "name": "my-skill",
    "output_dir": ".",  # 必须显式提供
})

# 新代码
input_data = InitSkillInput.model_validate({
    "name": "my-skill",
    # output_dir 可以省略，自动使用环境变量
})
```

或者设置环境变量：

```bash
export SKILL_CREATOR_OUTPUT_DIR=~/my-skills
export SKILL_CREATOR_DEFAULT_OUTPUT_DIR=~/agent-skills
```
```

---

## 五、验证方案

### 5.1 功能验证

#### 场景 1: 使用环境变量

```bash
# 设置环境变量
export SKILL_CREATOR_OUTPUT_DIR=~/test-skills

# 调用 init_skill（不传递 output_dir）
await init_skill(ctx, name="test-skill")
# 预期: 在 ~/test-skills/test-skill/ 创建
```

#### 场景 2: 使用默认输出目录

```bash
# 不设置任何环境变量
unset SKILL_CREATOR_OUTPUT_DIR

# 调用 init_skill
await init_skill(ctx, name="test-skill")
# 预期: 在 ~/agent-skills/test-skill/ 创建
```

#### 场景 3: 覆盖环境变量

```bash
# 设置环境变量
export SKILL_CREATOR_OUTPUT_DIR=~/test-skills

# 调用 init_skill（传递 output_dir）
await init_skill(ctx, name="test-skill", output_dir="/tmp")
# 预期: 在 /tmp/test-skill/ 创建
```

#### 场景 4: 直接调用内部函数

```python
from skill_creator_mcp.utils.packagers import package_agent_skill

# 设置环境变量
os.environ["SKILL_CREATOR_OUTPUT_DIR"] = "/tmp/output"

# 不传递 output_dir
result = package_agent_skill(skill_path="/path/to/skill")
# 预期: 输出到 /tmp/output/
```

### 5.2 跨平台验证

```bash
# Linux
python -m pytest

# Windows (如有)
python -m pytest

# macOS (如有)
python -m pytest
```

### 5.3 集成验证

```bash
# 1. 设置环境变量
export SKILL_CREATOR_OUTPUT_DIR=~/test-output
export SKILL_CREATOR_DEFAULT_OUTPUT_DIR=~/agent-skills

# 2. 启动 MCP Server
uv run python -m skill_creator_mcp

# 3. 在 Claude Code 中调用
await init_skill(ctx, name="integration-test")

# 4. 验证输出位置
ls ~/test-output/integration-test/
```

---

## 六、风险评估

| 风险 | 概率 | 影响 | 缓解措施 |
|------|------|------|----------|
| 破坏向后兼容 | 高 | 高 | 用户明确表示不考虑向后兼容 |
| 现有测试失败 | 中 | 中 | 运行完整测试套件，修复失败用例 |
| 文档不准确 | 低 | 中 | 仔细审查所有文档 |
| 环境变量未生效 | 低 | 高 | 添加集成测试验证 |
| 跨平台兼容性 | 中 | 中 | 使用 pathlib 确保兼容性 |

---

## 七、验收标准

### 7.1 代码质量

- [ ] 所有测试通过（pytest --cov）
- [ ] 测试覆盖率 ≥95%
- [ ] 代码检查通过（ruff check）
- [ ] 类型检查通过（mypy）
- [ ] 安全检查通过（bandit）

### 7.2 功能完整性

- [ ] MCP 工具正确读取环境变量
- [ ] Pydantic 模型正确读取环境变量
- [ ] 内部函数正确读取环境变量
- [ ] 参数可以覆盖环境变量
- [ ] 默认输出目录为 `~/agent-skills`

### 7.3 文档完整性

- [ ] SKILL.md 更新环境配置说明
- [ ] CHANGELOG.md 记录变更和迁移说明
- [ ] .env.example 更新
- [ ] 代码注释清晰

### 7.4 跨平台兼容性

- [ ] Linux 测试通过
- [ ] 路径处理使用 pathlib
- [ ] 无硬编码路径分隔符
- [ ] 临时文件使用 tempfile

---

## 八、开发规范流程

### 8.1 九步法执行

```
步骤0: 前置任务审核  → ✅ 已完成（本审核报告）
步骤1: 制定开发计划  → ✅ 已完成（本计划文档）
步骤2: 拆分任务清单  → ✅ 已完成（15个任务）
步骤3: 执行开发工作  → ⏳ 待执行
步骤4: 测试验证      → ⏳ 待执行
步骤5: 交叉验证      → ⏳ 待执行
步骤6: 更新文档      → ⏳ 待执行
步骤7: 阶段性审计    → ⏳ 待执行
步骤8: Git提交       → ⏳ 待执行
步骤9: 阶段性汇报    → ⏳ 待执行
```

### 8.2 TODO 状态管理

**任务清单**: 15 个任务

| 任务 | 优先级 | 状态 |
|------|--------|------|
| 任务 1: Pydantic 模型 | P0 | pending |
| 任务 2: 配置类 | P0 | pending |
| 任务 3: 内部函数 | P0 | pending |
| 任务 4: 路径分隔符 | P0 | pending |
| 任务 5: 归档目录 | P0 | pending |
| 任务 6: 测试硬编码 | P1 | pending |
| 任务 7: 缓存配置 | P1 | pending |
| 任务 8: 日志路径 | P1 | pending |
| 任务 9: 文档路径 | P0 | pending |
| 任务 10: 示例路径 | P1 | pending |
| 任务 11: 路径工具模块 | P0 | pending |
| 任务 12: .env.example | P1 | pending |
| 任务 13: 集成测试 | P0 | pending |
| 任务 14: 测试套件 | P0 | pending |
| 任务 15: CHANGELOG | P0 | pending |

---

## 九、总结

### 9.1 问题本质

用户遇到的是**配置硬编码导致的传播不完整**：
- MCP 工具层已支持环境变量
- 但 Pydantic 模型、内部函数、配置默认值仍有硬编码
- 路径处理存在平台兼容性问题
- 文档和示例存在误导性硬编码

### 9.2 修复策略

采用**激进重构策略**：
- 完全统一配置机制
- 消除所有硬编码
- 创建路径工具模块
- 改进默认行为
- 不考虑向后兼容

### 9.3 预期效果

修复后：
- ✅ 所有代码路径都支持环境变量
- ✅ 统一的配置机制
- ✅ 跨平台兼容性
- ✅ 更合理的默认值
- ✅ 完整的测试覆盖

### 9.4 关键文件清单

**修改文件**:
1. `models/skill_config.py` - 3 个模型
2. `config.py` - 配置类
3. `utils/packagers.py` - 打包函数
4. `utils/cache.py` - 缓存配置
5. `.env.example` - 环境变量示例
6. 文档文件 - 5 个文件

**新增文件**:
1. `utils/path_helpers.py` - 路径工具模块
2. `tests/test_integration/test_config_integration.py` - 集成测试

---

**计划状态**: 待用户批准
**下一步**: 用户确认后进入实施阶段
**预计工作量**: 4-6小时
**任务数量**: 15个（P0: 9个, P1: 6个）
