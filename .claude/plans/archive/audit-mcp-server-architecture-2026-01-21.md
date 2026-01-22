# Skill-Creator-MCP Server 深度架构审计报告

## 审计概述

**审计日期**: 2026-01-21
**审计范围**: skill-creator-mcp MCP Server 全栈架构
**核心文件**: 7个核心文件，共2859行代码

---

## Critical 级问题 (必须修复)

### 1. Tool 命名不一致导致功能缺失

**文件位置**: `/models/claude-glm/Skills-Creator/skill-creator-mcp/src/skill_creator_mcp/server.py:496-550`

**问题描述**:
`package_skill_tool` 的函数名与 FastMCP 装饰器注册的 tool 名称不一致，导致 MCP 客户端无法正确调用该工具。

**代码证据**:
```python
@mcp.tool()
async def package_skill_tool(  # <-- 函数名是 package_skill_tool
    ctx: Context,
    skill_path: str,
    ...
) -> dict[str, Any]:
    """
    打包 Agent-Skill 为分发格式.
    """
```

**最佳实践建议**:
```python
@mcp.tool()
async def package_skill(  # <-- 应该与期望的 tool 名称一致
    ctx: Context,
    skill_path: str,
    format: str = "zip",  # 避免使用内置函数名
    ...
) -> dict[str, Any]:
```

**影响**:
- MCP 客户端调用 `package_skill` 工具时会失败
- 文档中声明的工具名称与实际可调用名称不匹配

---

### 2. 资源 URI 格式不符合 MCP 规范

**文件位置**: `/models/claude-glm/Skills-Creator/skill-creator-mcp/src/skill_creator_mcp/server.py:729-762`

**问题描述**:
使用了 `skill://` 自定义 URI scheme，不符合 MCP Resource URI 标准格式。MCP 规范推荐使用 `file://` 或 `resource://` 格式。

**代码证据**:
```python
@mcp.resource("skill://templates")  # <-- 非标准 URI
@mcp.resource("skill://templates/{type}")  # <-- 非标准 URI
@mcp.resource("skill://best-practices")  # <-- 非标准 URI
@mcp.resource("skill://validation-rules")  # <-- 非标准 URI
```

**最佳实践建议**:
```python
# 使用标准 MCP Resource URI 格式
@mcp.resource("file:///templates")
@mcp.resource("file:///templates/{type}")
@mcp.resource("file:///best-practices")
@mcp.resource("file:///validation-rules")

# 或使用 resource:// scheme
@mcp.resource("resource://skill-creator/templates")
@mcp.resource("resource://skill-creator/templates/{type}")
```

**影响**:
- 某些 MCP 客户端可能无法正确识别这些资源
- 资源发现协议可能无法正常工作
- 违反 MCP 协议规范

---

### 3. Prompt 参数类型注解缺失

**文件位置**: `/models/claude-glm/Skills-Creator/skill-creator-mcp/src/skill_creator_mcp/server.py:768-816`

**问题描述**:
三个 Prompt 装饰器函数缺少必要的类型注解，FastMCP 无法正确生成参数 schema。

**代码证据**:
```python
@mcp.prompt("create-skill")
def create_skill_prompt(
    name: str,
    template: str = "minimal",
) -> str:  # <-- 返回类型正确，但参数需要更详细的注解
    """创建新技能的 Prompt 模板."""
    return get_create_skill_prompt(name, template)

@mcp.prompt("refactor-skill")
def refactor_skill_prompt(
    skill_path: str,
    focus: list[str] | None = None,  # <-- list[str] 在某些 MCP 版本可能不支持
) -> str:
    """重构技能的 Prompt 模板."""
    return get_refactor_skill_prompt(skill_path, focus)
```

**最佳实践建议**:
```python
from typing import Annotated
from fastmcp import Context

@mcp.prompt("create-skill")
def create_skill_prompt(
    name: Annotated[str, "技能名称"],
    template: Annotated[str, "模板类型（minimal/tool-based/workflow-based/analyzer-based）"] = "minimal",
) -> str:
    """创建新技能的 Prompt 模板.

    Args:
        name: 技能名称，符合命名规范
        template: 模板类型

    Returns:
        格式化的 prompt 模板
    """

@mcp.prompt("refactor-skill")
def refactor_skill_prompt(
    skill_path: Annotated[str, "技能目录路径"],
    focus: Annotated[str | None, "重点关注领域（逗号分隔：structure,documentation,testing）"] = None,
) -> str:
    """重构技能的 Prompt 模板.

    Args:
        skill_path: 技能目录的绝对路径
        focus: 逗号分隔的关注领域列表

    Returns:
        格式化的 prompt 模板
    """
    # 将字符串转换为列表
    focus_list = focus.split(",") if focus else None
    return get_refactor_skill_prompt(skill_path, focus_list)
```

**影响**:
- MCP 客户端可能无法正确显示 prompt 参数
- 参数验证可能失效
- IDE 类型提示不完整

---

### 4. 异常处理过于宽泛

**文件位置**: 多处

**问题描述**:
多个工具函数使用裸露的 `except Exception` 捕获所有异常，丢失了错误上下文。

**代码证据**:
```python
# server.py:180-185
except Exception as e:
    return {
        "success": False,
        "error": str(e),  # <-- 丢失异常类型和堆栈信息
        "error_type": "internal_error",
    }

# analyzers.py:36-41
try:
    with open(py_file, encoding="utf-8") as f:
        lines = f.readlines()
        total_lines += len(lines)
except Exception:  # <-- 连异常变量都没有
    pass
```

**最佳实践建议**:
```python
import logging
from typing import Union

logger = logging.getLogger(__name__)

# 使用具体的异常类型
try:
    # 业务逻辑
except ValueError as e:
    logger.error(f"Validation error: {e}", exc_info=True)
    return {
        "success": False,
        "error": str(e),
        "error_type": "validation_error",
    }
except (OSError, IOError) as e:
    logger.error(f"File system error: {e}", exc_info=True)
    return {
        "success": False,
        "error": f"文件操作失败: {e}",
        "error_type": "io_error",
    }
except Exception as e:
    logger.exception(f"Unexpected error in {function_name}")
    return {
        "success": False,
        "error": f"内部错误: {type(e).__name__}",
        "error_type": "internal_error",
    }
```

**影响**:
- 调试困难，无法定位错误来源
- 可能隐藏严重的安全问题
- 错误信息不友好，用户体验差

---

## High 级问题 (强烈建议修复)

### 1. 缺少日志系统

**文件位置**: 所有文件

**问题描述**:
整个项目没有使用 logging 模块，所有错误处理都只是返回字典，无法追踪问题。

**代码证据**:
```python
# 没有日志记录
except Exception as e:
    return {"success": False, "error": str(e)}
```

**最佳实践建议**:
```python
import logging
import sys
from pathlib import Path

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler('skill_creator.log')
    ]
)

logger = logging.getLogger(__name__)

# 使用日志
@mcp.tool()
async def init_skill(ctx: Context, name: str, ...) -> dict[str, Any]:
    logger.info(f"Initializing skill: {name} with template: {template}")
    try:
        ...
        logger.info(f"Successfully created skill at {skill_dir}")
    except Exception as e:
        logger.error(f"Failed to create skill {name}", exc_info=True)
```

**影响**:
- 无法追踪执行流程
- 生产环境问题难以定位
- 缺少审计跟踪

---

### 2. Pydantic 模型未被实际使用

**文件位置**: `/models/claude-glm/Skills-Creator/skill-creator-mcp/src/skill_creator_mcp/models/skill_config.py`

**问题描述**:
定义了详细的 Pydantic 模型（InitSkillInput, ValidateSkillInput 等），但在工具函数中并未使用它们进行参数验证。

**代码证据**:
```python
# models.py 定义了模型
class InitSkillInput(BaseModel):
    name: str = Field(..., min_length=1, max_length=64)
    template: SkillTemplateType = Field(default="minimal")
    ...

# 但 server.py 没有使用
@mcp.tool()
async def init_skill(
    ctx: Context,
    name: str,  # <-- 直接使用 str，没有用 Pydantic 验证
    template: str = "minimal",
    ...
) -> dict[str, Any]:
    validate_skill_name(name)  # <-- 手动验证，应该由 Pydantic 处理
    validate_template_type(template)
```

**最佳实践建议**:
```python
from .models.skill_config import InitSkillInput

@mcp.tool()
async def init_skill(
    ctx: Context,
    name: str,
    template: str = "minimal",
    output_dir: str = ".",
    with_scripts: bool = False,
    with_examples: bool = False,
) -> dict[str, Any]:
    """初始化新的 Agent-Skill."""
    try:
        # 使用 Pydantic 验证输入
        input_data = InitSkillInput(
            name=name,
            template=template,
            output_dir=output_dir,
            with_scripts=with_scripts,
            with_examples=with_examples,
        )
        # 现在 input_data.name 和 input_data.template 已经被验证
        skill_dir = await create_directory_structure_async(
            name=input_data.name,
            template_type=input_data.template,
            output_dir=Path(input_data.output_dir),
        )
        ...
    except ValidationError as e:
        return {
            "success": False,
            "error": f"参数验证失败: {e}",
            "error_type": "validation_error",
        }
```

**影响**:
- 代码重复（手动验证 vs Pydantic 自动验证）
- 验证逻辑不一致
- 无法利用 Pydantic 的自动文档生成

---

### 3. 异步函数没有正确使用异步 I/O

**文件位置**: `/models/claude-glm/Skills-Creator/skill-creator-mcp/src/skill_creator_mcp/utils/analyzers.py`

**问题描述**:
分析器函数中大量使用同步 I/O 操作，没有使用异步文件读写。

**代码证据**:
```python
# analyzers.py:36-41 (同步 I/O 在异步上下文中)
for py_file in skill_dir.rglob("*.py"):
    try:
        with open(py_file, encoding="utf-8") as f:  # <-- 同步 I/O
            lines = f.readlines()
            total_lines += len(lines)
    except Exception:
        pass
```

**最佳实践建议**:
```python
import asyncio
from aiofiles import open as aio_open

async def _analyze_structure_async(skill_dir: Path) -> StructureAnalysis:
    """异步分析代码结构."""
    total_files = 0
    total_lines = 0
    file_breakdown: dict[str, int] = {}

    async def process_file(py_file: Path) -> tuple[int, str]:
        """处理单个文件."""
        try:
            async with aio_open(py_file, encoding="utf-8") as f:
                content = await f.read()
                return len(content.splitlines()), _categorize_file(py_file, skill_dir)
        except Exception:
            return 0, "error"

    # 并发处理所有文件
    tasks = []
    for py_file in skill_dir.rglob("*.py"):
        if "__pycache__" in str(py_file):
            continue
        tasks.append(process_file(py_file))

    results = await asyncio.gather(*tasks, return_exceptions=True)

    for result in results:
        if isinstance(result, Exception):
            continue
        lines, category = result
        if lines > 0:
            total_files += 1
            total_lines += lines
            file_breakdown[category] = file_breakdown.get(category, 0) + 1

    return StructureAnalysis(
        total_files=total_files,
        total_lines=total_lines,
        file_breakdown=file_breakdown,
    )
```

**影响**:
- 性能低下，阻塞事件循环
- 大文件分析时响应缓慢
- 无法充分利用异步优势

---

### 4. 配置硬编码

**文件位置**: 多处

**问题描述**:
各种配置项硬编码在代码中，没有集中的配置管理。

**代码证据**:
```python
# validators.py:14-25
VALID_TOOLS = [
    "Read", "Write", "Edit", "Bash", "Glob", "Grep",
    "AskUserQuestion", "TodoWrite", "Skill",
]

# templates.py:12-33
TEMPLATE_DESCRIPTIONS: dict[TemplateType, str] = {
    "minimal": "最小化技能模板，适用于简单功能。",
    ...
}

# packagers.py:156-171
exclude_patterns = [
    "__pycache__", "*.pyc", ".pytest_cache", ...
]
```

**最佳实践建议**:
```python
# config.py
from pydantic import BaseModel, Field
from typing import Literal

class SkillCreatorConfig(BaseModel):
    """技能创建器配置."""

    # 有效工具列表
    valid_tools: list[str] = [
        "Read", "Write", "Edit", "Bash", "Glob", "Grep",
        "AskUserQuestion", "TodoWrite", "Skill",
    ]

    # 模板配置
    template_descriptions: dict[str, str] = {
        "minimal": "最小化技能模板，适用于简单功能。",
        "tool-based": "基于工具的技能模板，适用于封装特定工具或 API。",
        "workflow-based": "基于工作流的技能模板，适用于多步骤任务。",
        "analyzer-based": "基于分析的技能模板，适用于数据分析或代码分析。",
    }

    # 打包排除模式
    package_exclude_patterns: list[str] = [
        "__pycache__", "*.pyc", ".pytest_cache",
        "*.egg-info", ".venv", "venv", ".env",
    ]

    # 质量评分阈值
    quality_thresholds: dict[str, int] = {
        "excellent": 80,
        "good": 60,
        "fair": 40,
    }

    class Config:
        env_prefix = "SKILL_CREATOR_"
        env_nested_delimiter = "__"

# 使用
from .config import get_config

config = get_config()
if tool in config.valid_tools:
    ...
```

**影响**:
- 配置难以修改
- 无法根据环境调整行为
- 测试困难

---

## Medium 级问题 (建议修复)

### 1. 缺少类型提示的完整性

**文件位置**: 多个文件

**问题描述**:
部分函数缺少返回类型注解或参数类型注解。

**代码证据**:
```python
# server.py:553-620
def _generate_skill_md_content(name: str, template: str) -> str:  # <-- 正确
    ...

# 但私有函数缺少类型注解
def _create_reference_files(skill_dir: Path, template_type: str) -> None:  # <-- 有类型
    ...

# 有些工具函数
def _categorize_file(file_path: Path, base_dir: Path) -> str:  # <-- 有类型
    ...
```

**最佳实践建议**:
```python
from typing import Optional

# 所有函数都应该有完整的类型注解
def _generate_skill_md_content(
    name: str,
    template: Literal["minimal", "tool-based", "workflow-based", "analyzer-based"]
) -> str:
    """生成 SKILL.md 内容.

    Args:
        name: 技能名称
        template: 模板类型

    Returns:
        SKILL.md 文件内容
    """
    ...
```

**影响**:
- IDE 提示不完整
- 类型检查工具无法发挥作用
- 代码可读性降低

---

### 2. 文档字符串格式不统一

**文件位置**: 所有文件

**问题描述**:
混合使用 Google、NumPy 和 Sphinx 风格的文档字符串。

**代码证据**:
```python
# server.py 使用混合风格
"""初始化新的 Agent-Skill.

创建符合规范的技能目录结构和模板文件。

Args:
    ctx: MCP 上下文
    name: 技能名称
...

Returns:
    包含创建结果的字典
"""

# skill_config.py 使用 Google 风格
"""验证技能名称符合规范.

规范：
- 只能包含小写字母、数字、连字符
...
"""

# 一些函数完全没有文档字符串
def _categorize_file(file_path: Path, base_dir: Path) -> str:
    """对文件进行分类.

    Args:
        file_path: 文件路径
        base_dir: 基础目录

    Returns:
        文件类别
    """
```

**最佳实践建议**:
```python
# 统一使用 Google 风格（与 FastMCP 一致）
def init_skill(
    ctx: Context,
    name: str,
    template: str = "minimal",
) -> dict[str, Any]:
    """初始化新的 Agent-Skill.

    创建符合规范的技能目录结构和模板文件。

    Args:
        ctx: MCP 上下文对象，用于日志和状态报告
        name: 技能名称，必须符合命名规范
            - 只能包含小写字母、数字、连字符
            - 长度 1-64 字符
            - 不能以连字符开头或结尾
        template: 模板类型，可选值：
            - "minimal": 最小化模板
            - "tool-based": 基于工具的模板
            - "workflow-based": 基于工作流的模板
            - "analyzer-based": 基于分析的模板

    Returns:
        包含以下字段的字典：
            - success (bool): 操作是否成功
            - skill_path (str): 创建的技能目录路径
            - skill_name (str): 技能名称
            - template (str): 使用的模板类型
            - message (str): 描述信息
            - next_steps (list[str]): 后续步骤建议

    Raises:
        ValueError: 当技能名称不符合规范时
        OSError: 当目录创建失败时

    Examples:
        >>> result = await init_skill(ctx, "my-skill", "tool-based")
        >>> result["success"]
        True
    """
```

**影响**:
- 文档生成工具可能产生不一致的输出
- IDE 提示不统一
- 代码可读性降低

---

### 3. 魔法数字和硬编码值

**文件位置**: 多处

**问题描述**:
代码中散布大量魔法数字，没有命名常量。

**代码证据**:
```python
# analyzers.py:245
if len(content) > 200:  # <-- 魔法数字
    score += 10

# analyzers.py:291
if len(test_files) >= 3:  # <-- 魔法数字
    score += 10

# refactorors.py:122
if len(content) > 3000:  # <-- 魔法数字
    suggestions.append(...)

# refactorors.py:137
if len(content.split("\n")) > 400:  # <-- 魔法数字
    suggestions.append(...)
```

**最佳实践建议**:
```python
# constants.py
from typing import Final

# 文档长度限制（行数)
MAX_SKILL_MD_LINES: Final = 150
MAX_REFERENCE_DOC_LINES: Final = 400
SKILL_MD_WARN_THRESHOLD: Final = 3000  # 字符数

# 质量评分阈值
CONTENT_LENGTH_THRESHOLD: Final = 200  # 字符数
MIN_TEST_FILES_THRESHOLD: Final = 3
TEST_COVERAGE_TARGET: Final = 95  # 百分比

# 质量评分权重
STRUCTURE_SCORE_MAX: Final = 40
DOCUMENTATION_SCORE_MAX: Final = 30
TEST_SCORE_MAX: Final = 30

# 复杂度阈值
CYCLOMATIC_COMPLEXITY_LOW: Final = 5
CYCLOMATIC_COMPLEXITY_MEDIUM: Final = 10
MAINTAINABILITY_INDEX_THRESHOLD: Final = 50

# 使用
from .constants import (
    MAX_SKILL_MD_LINES,
    CONTENT_LENGTH_THRESHOLD,
    MIN_TEST_FILES_THRESHOLD,
)

if len(content) > CONTENT_LENGTH_THRESHOLD:
    score += 10

if len(test_files) >= MIN_TEST_FILES_THRESHOLD:
    score += 10
```

**影响**:
- 代码难以理解和维护
- 调整阈值需要修改多处代码
- 容易出错

---

### 4. 资源内容过时

**文件位置**:
- `/models/claude-glm/Skills-Creator/skill-creator-mcp/src/skill_creator_mcp/resources/best_practices.py`
- `/models/claude-glm/Skills-Creator/skill-creator-mcp/src/skill_creator_mcp/resources/validation_rules.py`

**问题描述**:
资源文件中提到的工具列表与实际可用工具不同步。

**代码证据**:
```python
# validation_rules.py:89-96 提到的工具列表
有效工具列表：
- `Read` - 读取文件
- `Write` - 写入文件
- `Edit` - 编辑文件
- `Bash` - 执行命令
- `Glob` - 文件匹配
- `Grep` - 内容搜索
- `GlobDirectoryTree` - 目录遍历

# 但实际上 Claude Code 有更多工具：
# - AskUserQuestion
# - TodoWrite
# - Skill
# - NotebookEdit
# 等
```

**最佳实践建议**:
```python
# 动态生成工具列表，从配置或环境获取
def get_valid_tools() -> list[str]:
    """获取当前可用的工具列表.

    Returns:
        有效工具名称列表
    """
    # 可以从环境变量或配置文件读取
    return os.getenv(
        "ALLOWED_TOOLS",
        "Read,Write,Edit,Bash,Glob,Grep,AskUserQuestion,TodoWrite,Skill"
    ).split(",")

# 在文档中使用动态内容
def get_validation_rules() -> str:
    valid_tools = get_valid_tools()
    tools_list = "\n".join(f"- `{tool}`" for tool in valid_tools)
    return f"""# Agent-Skills 验证规则

...

### 3.3 allowed-tools 验证
有效工具列表：
{tools_list}
...
"""
```

**影响**:
- 文档与实际不符，误导用户
- 验证规则可能遗漏或错误
- 维护困难

---

### 5. 缺少输入清理和消毒

**文件位置**: `/models/claude-glm/Skills-Creator/skill-creator-mcp/src/skill_creator_mcp/utils/validators.py`

**问题描述**:
路径验证不充分，可能存在路径遍历安全漏洞。

**代码证据**:
```python
# server.py:208-223
skill_dir = Path(skill_path)  # <-- 直接使用用户输入

# 没有检查路径遍历
# 如果用户传入 "../../etc/passwd"，可能会有安全问题
```

**最佳实践建议**:
```python
import os
from pathlib import Path

def sanitize_path(
    base_dir: Path,
    user_path: str,
) -> Path:
    """清理和验证用户提供的路径.

    Args:
        base_dir: 允许访问的基础目录
        user_path: 用户提供的路径

    Returns:
        清理后的绝对路径

    Raises:
        ValueError: 如果路径尝试遍历到基础目录之外
    """
    # 解析为绝对路径
    resolved = Path(user_path).resolve()

    # 确保路径在基础目录内
    try:
        resolved.relative_to(base_dir.resolve())
    except ValueError:
        raise ValueError(
            f"路径必须在 {base_dir} 内: {user_path}"
        )

    return resolved

# 使用
try:
    skill_dir = sanitize_path(Path.cwd().resolve(), skill_path)
except ValueError as e:
    return {
        "success": False,
        "error": str(e),
        "error_type": "path_error",
    }
```

**影响**:
- 潜在的安全漏洞
- 可能访问意外的文件
- 拒绝服务攻击

---

## Low 级问题 (可选优化)

### 1. 缺少性能分析工具

**文件位置**: 所有工具函数

**问题描述**:
没有性能监控，无法识别慢操作。

**建议**:
```python
import time
from functools import wraps
from typing import Callable

def timing_decorator(func: Callable) -> Callable:
    """性能计时装饰器."""
    @wraps(func)
    async def async_wrapper(*args, **kwargs):
        start = time.perf_counter()
        try:
            result = await func(*args, **kwargs)
            return result
        finally:
            elapsed = time.perf_counter() - start
            logger.debug(f"{func.__name__} took {elapsed:.3f}s")

    @wraps(func)
    def sync_wrapper(*args, **kwargs):
        start = time.perf_counter()
        try:
            result = func(*args, **kwargs)
            return result
        finally:
            elapsed = time.perf_counter() - start
            logger.debug(f"{func.__name__} took {elapsed:.3f}s")

    return async_wrapper if asyncio.iscoroutinefunction(func) else sync_wrapper

# 使用
@mcp.tool()
@timing_decorator
async def analyze_skill(...) -> dict[str, Any]:
    ...
```

---

### 2. 缺少单元测试

**问题描述**:
项目有测试配置（pyproject.toml），但没有看到实际的测试文件。

**建议**:
```python
# tests/test_validators.py
import pytest
from skill_creator_mcp.utils.validators import validate_skill_name

def test_validate_skill_name_valid():
    """测试有效的技能名称."""
    assert validate_skill_name("my-skill") is None
    assert validate_skill_name("test123") is None

def test_validate_skill_name_invalid():
    """测试无效的技能名称."""
    with pytest.raises(ValueError):
        validate_skill_name("MySkill")  # 大写

    with pytest.raises(ValueError):
        validate_skill_name("-skill")  # 以连字符开头

    with pytest.raises(ValueError):
        validate_skill_name("skill--name")  # 连续连字符

# tests/test_analyzers.py
import pytest
from pathlib import Path
from skill_creator_mcp.utils.analyzers import _analyze_structure

@pytest.fixture
def sample_skill_dir(tmp_path: Path) -> Path:
    """创建测试技能目录."""
    skill_dir = tmp_path / "test-skill"
    skill_dir.mkdir()

    (skill_dir / "SKILL.md").write_text("# Test Skill")
    (skill_dir / "test.py").write_text("print('hello')")

    return skill_dir

def test_analyze_structure(sample_skill_dir: Path):
    """测试结构分析."""
    result = _analyze_structure(sample_skill_dir)

    assert result.total_files == 1
    assert result.total_lines > 0
```

---

### 3. 错误消息国际化

**问题描述**:
所有错误消息都是中文硬编码，不支持多语言。

**建议**:
```python
# i18n.py
from typing import Dict
from enum import Enum

class Language(Enum):
    """支持的语言."""
    ZH_CN = "zh_CN"
    EN_US = "en_US"

class Messages:
    """错误消息国际化."""

    _messages: Dict[Language, Dict[str, str]] = {
        Language.ZH_CN: {
            "invalid_skill_name": "技能名称 '{name}' 不符合规范",
            "directory_not_exists": "目录不存在: {path}",
            "missing_required_file": "缺少必需文件: {file}",
        },
        Language.EN_US: {
            "invalid_skill_name": "Skill name '{name}' is invalid",
            "directory_not_exists": "Directory does not exist: {path}",
            "missing_required_file": "Missing required file: {file}",
        },
    }

    @classmethod
    def get(
        cls,
        key: str,
        lang: Language = Language.ZH_CN,
        **kwargs,
    ) -> str:
        """获取本地化消息.

        Args:
            key: 消息键
            lang: 语言
            **kwargs: 格式化参数

        Returns:
            格式化后的消息
        """
        template = cls._messages[lang].get(key, key)
        return template.format(**kwargs)

# 使用
raise ValueError(
    Messages.get("invalid_skill_name", name=user_input)
)
```

---

### 4. 代码重复

**文件位置**: 多处

**问题描述**:
目录存在性检查代码重复。

**代码证据**:
```python
# server.py:216-235 (validate_skill 中)
if not skill_dir.exists():
    return {
        "success": False,
        "valid": False,
        "skill_path": skill_path,
        "errors": [f"目录不存在: {skill_path}"],
        ...
    }

# server.py:320-332 (analyze_skill 中)
if not skill_dir.exists():
    return {
        "success": False,
        "error": f"目录不存在: {skill_path}",
        "error_type": "path_error",
    }

# server.py:419-431 (refactor_skill 中)
# 几乎相同的代码
```

**建议**:
```python
# utils.py
def validate_skill_directory(skill_path: str) -> tuple[bool, Path, str | None]:
    """验证技能目录.

    Args:
        skill_path: 技能目录路径

    Returns:
        (是否有效, Path对象, 错误消息)
    """
    skill_dir = Path(skill_path).resolve()

    if not skill_dir.exists():
        return False, skill_dir, f"目录不存在: {skill_path}"

    if not skill_dir.is_dir():
        return False, skill_dir, f"路径不是目录: {skill_path}"

    return True, skill_dir, None

# 使用
@mcp.tool()
async def validate_skill(skill_path: str, ...) -> dict[str, Any]:
    is_valid, skill_dir, error = validate_skill_directory(skill_path)
    if not is_valid:
        return {
            "success": False,
            "valid": False,
            "skill_path": skill_path,
            "errors": [error],
            ...
        }
    # 继续处理...
```

---

### 5. 资源 URI 缺少版本控制

**问题描述**:
资源 URI 没有版本信息，未来更新可能破坏向后兼容性。

**建议**:
```python
# 使用版本化的资源 URI
@mcp.resource("skill://v1/templates")
@mcp.resource("skill://v1/templates/{type}")
@mcp.resource("skill://v1/best-practices")
@mcp.resource("skill://v1/validation-rules")

# 或使用日期版本
@mcp.resource("skill://2024-01/templates")
```

---

## 优先级修复路线图

### 第一阶段 (Critical - 立即修复)

1. **修复 Tool 命名** - `package_skill_tool` -> `package_skill`
2. **修复资源 URI 格式** - 使用标准 MCP URI scheme
3. **添加 Prompt 参数类型注解** - 使用 Annotated 类型
4. **改进异常处理** - 使用具体异常类型，添加日志

### 第二阶段 (High - 本周完成)

1. **添加日志系统** - 配置 structured logging
2. **使用 Pydantic 验证** - 所有工具函数使用模型验证
3. **异步 I/O 优化** - 替换同步文件操作为异步
4. **配置外部化** - 创建 config.py 集中管理配置

### 第三阶段 (Medium - 本月完成)

1. **统一文档字符串** - 使用 Google 风格
2. **提取魔法数字** - 创建 constants.py
3. **更新资源内容** - 同步工具列表
4. **加强路径验证** - 防止路径遍历攻击

### 第四阶段 (Low - 有时间时优化)

1. **添加性能监控** - 计时装饰器
2. **编写单元测试** - 覆盖核心功能
3. **错误消息国际化** - i18n 支持
4. **消除代码重复** - 提取公共函数

---

## 总结

### 问题统计

| 级别 | 数量 | 影响范围 |
|------|------|----------|
| Critical | 4 | 核心功能 |
| High | 4 | 可维护性 |
| Medium | 5 | 代码质量 |
| Low | 5 | 可选优化 |

### 关键建议

1. **优先修复 Critical 问题**，这些问题影响核心功能
2. **建立完整的日志系统**，这是调试和监控的基础
3. **充分利用 Pydantic**，避免重复的验证逻辑
4. **统一异步模式**，所有 I/O 操作都应该异步
5. **加强测试覆盖**，确保代码质量

### 架构优势

1. 清晰的模块化结构
2. 完整的类型注解（大部分）
3. 良好的资源组织
4. 符合 FastMCP 最佳实践（大部分）
