# 删除向后兼容逻辑，统一环境变量配置

> **计划日期**: 2026-01-26
> **计划类型**: 重构计划
> **核心原则**: **禁止向后兼容性开发**，以规范统一、易维护为目标

---

## 一、任务概述

### 1.1 问题诊断

当前代码存在**双参数混乱架构**：

| 参数名 | 状态 | 实际优先级 | 文档说明 |
|--------|------|------------|----------|
| `SKILL_CREATOR_OUTPUT_DIR` | 旧参数 | **最高** | 文档声称"已废弃" |
| `SKILL_CREATOR_DEFAULT_OUTPUT_DIR` | 新参数 | 较低 | 文档声称"推荐使用" |

**实际代码优先级** (config.py:61-71):
```python
default_output = os.getenv("SKILL_CREATOR_DEFAULT_OUTPUT_DIR", "~/skills")
output_dir_value = os.getenv("SKILL_CREATOR_OUTPUT_DIR", default_output)
# 实际：SKILL_CREATOR_OUTPUT_DIR > SKILL_CREATOR_DEFAULT_OUTPUT_DIR > ~/skills
```

**文档矛盾**：
- `.env.example:31` 声称 DEFAULT 已废弃
- `configuration.md:23` 声称 DEFAULT 已废弃
- 但代码仍然读取 DEFAULT 参数

### 1.2 规范统一决策

**只保留**: `SKILL_CREATOR_OUTPUT_DIR`
- 默认值：`~/skills`（自动创建）
- 优先级：工具参数 > `SKILL_CREATOR_OUTPUT_DIR` > `~/skills`

**删除**: `SKILL_CREATOR_DEFAULT_OUTPUT_DIR` 及所有向后兼容逻辑

---

## 二、代码修改清单

### 2.1 config.py

**文件**: `skill-creator-mcp/src/skill_creator_mcp/config.py`

| 行号 | 操作 | 说明 |
|------|------|------|
| 12-17 | 修改注释 | 删除 DEFAULT 参数说明，简化为单一参数 |
| 56-71 | 修改实现 | 删除双参数逻辑，直接读取 SKILL_CREATOR_OUTPUT_DIR |
| 117-119 | **删除** | 删除 `default_output_dir` 属性 |

**修改后代码** (第56-71行):
```python
# 工作目录配置
# 优先级：工具参数 > SKILL_CREATOR_OUTPUT_DIR > ~/skills
# 注意：
# 1. ~/skills 会被自动创建（如果不存在）
# 2. 推荐使用绝对路径避免混淆
# 3. 相对路径将基于 MCP Server 启动目录解析
output_dir_value = os.getenv("SKILL_CREATOR_OUTPUT_DIR", "~/skills")
self._output_dir: Path = Path(output_dir_value).expanduser().resolve(strict=False)
```

### 2.2 path_helpers.py

**文件**: `skill-creator-mcp/src/skill_creator_mcp/utils/path_helpers.py`

| 行号 | 操作 | 说明 |
|------|------|------|
| 78-93 | **删除** | 删除 `get_default_output_dir()` 函数 |
| 96-116 | 修改 | 简化 `get_output_dir()`，删除对 `get_default_output_dir()` 的调用 |

**修改后代码** (第96-116行):
```python
def get_output_dir(fallback: bool = True) -> Path:
    """获取输出目录.

    Args:
        fallback: 如果未设置，是否使用默认值 ~/skills

    Returns:
        输出目录路径

    Raises:
        ValueError: 如果未设置且 fallback=False
    """
    import os

    output_dir_value = os.getenv("SKILL_CREATOR_OUTPUT_DIR")
    if output_dir_value:
        return Path(output_dir_value).expanduser().resolve(strict=False)
    if fallback:
        return Path("~/skills").expanduser().resolve(strict=False)
    raise ValueError("必须设置 SKILL_CREATOR_OUTPUT_DIR 环境变量")
```

---

## 三、测试修改清单

### 3.1 test_path_helpers.py

**文件**: `skill-creator-mcp/tests/test_utils/test_path_helpers.py`

| 操作 | 测试函数 | 行号 |
|------|----------|------|
| **删除** | `test_get_default_output_dir_uses_env_var` | 80-98 |
| **删除** | `test_get_default_output_dir_creates_home_skills` | 100-131 |
| **新增** | `test_get_output_dir_with_env_var` | - |
| **新增** | `test_get_output_dir_fallback_to_home_skills` | - |
| 修改 | import 语句 | 8-12 |

**新增测试代码**:
```python
def test_get_output_dir_with_env_var():
    """测试 get_output_dir 读取 SKILL_CREATOR_OUTPUT_DIR."""
    import os

    original_value = os.environ.get("SKILL_CREATOR_OUTPUT_DIR")
    os.environ["SKILL_CREATOR_OUTPUT_DIR"] = "/tmp/test_skills"

    try:
        result = get_output_dir()
        assert "test_skills" in str(result)
    finally:
        if original_value is None:
            del os.environ["SKILL_CREATOR_OUTPUT_DIR"]
        else:
            os.environ["SKILL_CREATOR_OUTPUT_DIR"] = original_value


def test_get_output_dir_fallback_to_home_skills():
    """测试 get_output_dir 回退到 ~/skills."""
    import os

    original_value = os.environ.get("SKILL_CREATOR_OUTPUT_DIR")
    if "SKILL_CREATOR_OUTPUT_DIR" in os.environ:
        del os.environ["SKILL_CREATOR_OUTPUT_DIR"]

    try:
        result = get_output_dir(fallback=True)
        assert "skills" in str(result).lower()
        assert str(Path.home()) in str(result)
    finally:
        if original_value is not None:
            os.environ["SKILL_CREATOR_OUTPUT_DIR"] = original_value
```

### 3.2 test_config.py

**文件**: `skill-creator-mcp/tests/test_tools/test_config.py`

| 操作 | 测试函数 | 行号 |
|------|----------|------|
| **删除** | `test_default_output_dir_is_home_skills` | 227-233 |
| 修改 | `test_custom_output_dir_from_env` | 254-267 |

**修改后的测试**:
```python
def test_custom_output_dir_from_env():
    """测试从环境变量读取自定义目录."""
    import os

    custom_dir = "~/.claude/skills"
    os.environ["SKILL_CREATOR_OUTPUT_DIR"] = custom_dir

    try:
        reload_config()
        config = Config()
        assert ".claude" in str(config.output_dir)
        assert "skills" in str(config.output_dir).lower()
    finally:
        del os.environ["SKILL_CREATOR_OUTPUT_DIR"]
        reload_config()
```

### 3.3 test_config_integration.py

**文件**: `skill-creator-mcp/tests/test_integration/test_config_integration.py`

| 操作 | 测试函数 | 行号 |
|------|----------|------|
| **删除** | `test_default_output_dir_fallback` | 39-57 |
| 修改 | `test_config_new_properties` | 120-135 |

---

## 四、文档修改清单

### 4.1 .env.example

**文件**: `skill-creator-mcp/.env.example`

| 行号 | 操作 |
|------|------|
| 31 | **删除** 整行（废弃说明注释） |

### 4.2 configuration.md

**文件**: `skill-creator-mcp/docs/configuration.md`

| 行号 | 操作 |
|------|------|
| 23 | **删除** `SKILL_CREATOR_DEFAULT_OUTPUT_DIR` 表格行 |
| 158 | 修改优先级说明，删除 DEFAULT 引用 |

---

## 五、验证方案

### 5.1 代码验证

```bash
# 1. 确保没有残留的 DEFAULT_OUTPUT_DIR 引用
grep -r "SKILL_CREATOR_DEFAULT_OUTPUT_DIR" skill-creator-mcp/src/
# 预期：无结果

# 2. 确保没有残留的 default_output_dir 引用
grep -r "default_output_dir" skill-creator-mcp/src/
# 预期：无结果

# 3. 确保没有残留的 get_default_output_dir 引用
grep -r "get_default_output_dir" skill-creator-mcp/
# 预期：无结果
```

### 5.2 测试验证

```bash
cd skill-creator-mcp

# 运行完整测试套件
uv run pytest tests/ --cov

# 预期结果：
# - 所有测试通过
# - 覆盖率 ≥95%
# - 无测试引用 DEFAULT_OUTPUT_DIR
```

### 5.3 功能验证

```bash
# 测试1: 默认行为（未设置环境变量）
unset SKILL_CREATOR_OUTPUT_DIR
# 预期：使用 ~/skills

# 测试2: 自定义目录
export SKILL_CREATOR_OUTPUT_DIR=/tmp/test-skills
# 预期：使用 /tmp/test-skills

# 测试3: 工具参数覆盖
export SKILL_CREATOR_OUTPUT_DIR=/tmp/env-skills
# 调用工具时指定 output_dir 参数
# 预期：使用参数值，而非环境变量
```

---

## 六、关键文件清单

**代码文件** (2个):
- `skill-creator-mcp/src/skill_creator_mcp/config.py`
- `skill-creator-mcp/src/skill_creator_mcp/utils/path_helpers.py`

**测试文件** (3个):
- `skill-creator-mcp/tests/test_utils/test_path_helpers.py`
- `skill-creator-mcp/tests/test_tools/test_config.py`
- `skill-creator-mcp/tests/test_integration/test_config_integration.py`

**文档文件** (2个):
- `skill-creator-mcp/.env.example`
- `skill-creator-mcp/docs/configuration.md`

---

## 七、成功标准

- ✅ 所有测试通过（≥610个测试）
- ✅ 覆盖率保持 ≥95%
- ✅ 代码中无 `SKILL_CREATOR_DEFAULT_OUTPUT_DIR` 引用
- ✅ 文档中无 `SKILL_CREATOR_DEFAULT_OUTPUT_DIR` 引用
- ✅ ruff check 0 错误
- ✅ mypy 0 错误

---

## 八、验收测试清单

- [ ] 代码修改完成（config.py, path_helpers.py）
- [ ] 测试修改完成（3个测试文件）
- [ ] 文档修改完成（.env.example, configuration.md）
- [ ] 无残留引用验证通过
- [ ] 所有测试通过
- [ ] 覆盖率验证通过
- [ ] 手动功能测试通过
- [ ] CHANGELOG.md 更新

---

**计划状态**: 待审批
**下一步**: 审批后执行九步法开发流程
