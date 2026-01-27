# Phase 2.2 测试修复计划

> **创建时间**: 2026-01-27
> **状态**: planning
> **前置任务**: Phase 2.2 重构已完成

---

## 一、任务概述

### 1.1 背景

Phase 2.2 重构将 `server.py` (1,354行) 中的工具函数拆分到专门的模块中，新增了 `tools/` 目录下的5个模块文件。重构后：

- **代码行数**: server.py 减少 60% (1,354行 → 550行)
- **测试通过**: 599/619 (96.8%)
- **测试覆盖率**: 87% → 94% (+7%)

### 1.2 问题分析

有 **20 个测试失败**，分为三类：

| 类别 | 数量 | 问题 | 修复优先级 |
|------|------|------|-----------|
| 错误类型不一致 | 5 | 期望 `internal_error`，实际 `path_error` | P1 |
| 导入路径错误 | 12 | 函数移到 `utils/requirement_collection.py` | P0 |
| 批量工具导入错误 | 3 | 函数移到 `tools/batch_operations.py` | P0 |

### 1.3 目标

1. 修复所有 20 个失败测试
2. 运行代码质量检查 (ruff, mypy)
3. 确保 100% 测试通过
4. 完成 Git 提交

---

## 二、失败测试详细清单

### 2.1 类别1: 错误类型不一致 (5个)

| 测试文件 | 测试用例 | 当前期望 | 实际返回 |
|---------|---------|---------|---------|
| `test_mcp/test_analyze_skill_mcp.py` | `test_analyze_skill_mcp_internal_error` | `internal_error` | `path_error` |
| `test_mcp/test_init_skill_mcp.py` | `test_init_skill_mcp_tool_internal_error` | `internal_error` | `path_error` |
| `test_mcp/test_package_skill_mcp.py` | `test_package_skill_mcp_internal_error` | `internal_error` | `path_error` |
| `test_mcp/test_refactor_skill_mcp.py` | `test_refactor_skill_mcp_internal_error` | `internal_error` | `path_error` |
| `test_mcp/test_validate_skill_mcp.py` | `test_validate_skill_mcp_internal_error` | `internal_error` | `path_error` |

**根本原因**: Phase 2.2 重构后，`skill_tools.py` 改进了错误类型区分，当 `Path()` 构造失败时返回更精确的 `path_error`。

**修复方案**: 更新测试期望值，接受新的精确错误类型。

### 2.2 类别2: 导入路径错误 (12个)

**文件**: `tests/test_tools/test_server_helpers.py`

| 测试类 | 测试用例 | 需要更新的导入 |
|--------|---------|---------------|
| `TestGetRequirementModeSteps` | 2个测试 | `_get_requirement_mode_steps` |
| `TestProcessRequirementUserAnswer` | 4个测试 | `_process_requirement_user_answer` |
| `TestHandleRequirementPreviousAction` | 3个测试 | `_handle_requirement_previous_action` |
| `TestCollectRequirementsErrorHandling` | 1个测试 | `_validate_and_init_requirement_session` |
| `TestGetRequirementNextQuestion` | 1个测试 | `_get_requirement_next_question` |
| `TestCollectWithElicitErrorCases` | 1个测试 | `_collect_with_elicit` |

**修复方案**: 更新导入路径：
```python
# 从
from skill_creator_mcp.server import _xxx

# 改为
from skill_creator_mcp.utils.requirement_collection import _xxx
```

### 2.3 类别3: 批量工具导入错误 (3个)

**文件**: `tests/test_tools/test_health_check.py`

| 测试用例 | 需要更新的 mock 路径 |
|---------|---------------------|
| `test_batch_validate_skills_tool_exception_handling` | `tools.batch_operations.batch_validate_skills` |
| `test_batch_analyze_skills_tool_exception_handling` | `tools.batch_operations.batch_analyze_skills` |
| `test_package_agent_skill_internal_error_handling` | (需要进一步确认) |

**修复方案**: 更新 mock 路径：
```python
# 从
with patch("skill_creator_mcp.server.batch_validate_skills", ...):

# 改为
with patch("skill_creator_mcp.tools.batch_operations.batch_validate_skills", ...):
```

---

## 三、实施计划

### 3.1 任务拆分

| ID | 任务 | 优先级 | 文件 | 修改数量 |
|----|------|--------|------|---------|
| T1 | 修复 test_server_helpers.py 导入路径 | P0 | `tests/test_tools/test_server_helpers.py` | 12处 |
| T2 | 修复 test_health_check.py mock 路径 | P0 | `tests/test_tools/test_health_check.py` | 2处 |
| T3 | 更新 MCP 工具测试的错误类型期望 | P1 | `tests/test_mcp/*.py` (5个文件) | 5处 |
| T4 | 运行完整测试套件验证修复 | P0 | - | - |
| T5 | 运行代码质量检查 | P0 | ruff, mypy | - |

### 3.2 详细修复步骤

#### T1: 修复 test_server_helpers.py (12处导入)

**行号和函数映射**:

| 行号 | 原导入 | 新导入 |
|------|--------|--------|
| 155, 162 | `from skill_creator_mcp.server import _get_requirement_mode_steps` | `from skill_creator_mcp.utils.requirement_collection import _get_requirement_mode_steps` |
| 193, 226, 259, 290 | `from skill_creator_mcp.server import _process_requirement_user_answer` | `from skill_creator_mcp.utils.requirement_collection import _process_requirement_user_answer` |
| 328, 357, 384 | `from skill_creator_mcp.server import _handle_requirement_previous_action` | `from skill_creator_mcp.utils.requirement_collection import _handle_requirement_previous_action` |
| 416 | `from skill_creator_mcp.server import collect_requirements` | `from skill_creator_mcp.tools.requirement_tools import collect_requirements` |
| 445 | `from skill_creator_mcp.server import _get_requirement_next_question` | `from skill_creator_mcp.utils.requirement_collection import _get_requirement_next_question` |
| 478 | `from skill_creator_mcp.server import _collect_with_elicit` | `from skill_creator_mcp.utils.requirement_collection import _collect_with_elicit` |

**验证**: 修改后运行 `pytest tests/test_tools/test_server_helpers.py -v`

#### T2: 修复 test_health_check.py (2处mock)

**行号和内容**:

| 行号 | 原内容 | 新内容 |
|------|--------|--------|
| 568 | `"skill_creator_mcp.server.batch_validate_skills"` | `"skill_creator_mcp.tools.batch_operations.batch_validate_skills"` |
| 595 | `"skill_creator_mcp.server.batch_analyze_skills"` | `"skill_creator_mcp.tools.batch_operations.batch_analyze_skills"` |

**验证**: 修改后运行 `pytest tests/test_tools/test_health_check.py::TestServerBatchToolsExceptionHandling -v`

#### T3: 更新 MCP 工具测试的错误类型期望 (5处)

**文件和行号**:

| 文件 | 测试函数 | 修改内容 |
|------|---------|---------|
| `test_mcp/test_analyze_skill_mcp.py` | `test_analyze_skill_mcp_internal_error` (第281行) | `assert result["error_type"] == "path_error"` |
| `test_mcp/test_init_skill_mcp.py` | `test_init_skill_mcp_tool_internal_error` | `assert result["error_type"] == "path_error"` |
| `test_mcp/test_package_skill_mcp.py` | `test_package_skill_mcp_internal_error` | `assert result["error_type"] == "path_error"` |
| `test_mcp/test_refactor_skill_mcp.py` | `test_refactor_skill_mcp_internal_error` | `assert result["error_type"] == "path_error"` |
| `test_mcp/test_validate_skill_mcp.py` | `test_validate_skill_mcp_internal_error` | `assert result["error_type"] == "path_error"` |

**验证**: 修改后运行 `pytest tests/test_mcp/ -v -k internal_error`

### 3.3 执行顺序

```
T1 (修复 test_server_helpers.py - 12处导入)
  ↓ 验证: pytest tests/test_tools/test_server_helpers.py -v
T2 (修复 test_health_check.py - 2处mock)
  ↓ 验证: pytest tests/test_tools/test_health_check.py::TestServerBatchToolsExceptionHandling -v
T3 (更新错误类型期望 - 5处)
  ↓ 验证: pytest tests/test_mcp/ -v -k internal_error
T4 (运行完整测试套件验证)
  ↓ 验证: uv run pytest --cov
T5 (代码质量检查)
  ↓ 验证: uv run ruff check . && uv run mypy src/
```

---

## 四、验收标准

### 4.1 测试通过

- [ ] 所有 619 个测试通过
- [ ] 无跳过测试
- [ ] 测试覆盖率 ≥ 94%

### 4.2 代码质量

- [ ] `uv run ruff check .` 返回 0 错误
- [ ] `uv run mypy src/` 返回 0 错误
- [ ] `uv run bandit -r src/` 无高危问题

### 4.3 文档更新

- [ ] 更新 CHANGELOG.md

---

## 五、关键文件路径

### 5.1 需要修改的测试文件

```
tests/test_tools/test_server_helpers.py       # 12个失败测试
tests/test_tools/test_health_check.py         # 3个失败测试
tests/test_mcp/test_analyze_skill_mcp.py      # 1个失败测试
tests/test_mcp/test_init_skill_mcp.py         # 1个失败测试
tests/test_mcp/test_package_skill_mcp.py      # 1个失败测试
tests/test_mcp/test_refactor_skill_mcp.py     # 1个失败测试
tests/test_mcp/test_validate_skill_mcp.py     # 1个失败测试
```

### 5.2 相关源代码文件

```
src/skill_creator_mcp/tools/skill_tools.py           # 新增，537行
src/skill_creator_mcp/tools/package_tools.py         # 新增，215行
src/skill_creator_mcp/tools/requirement_tools.py     # 新增，186行
src/skill_creator_mcp/tools/test_tools.py            # 新增，110行
src/skill_creator_mcp/tools/batch_tools.py           # 新增，105行
src/skill_creator_mcp/utils/requirement_collection.py # 已存在
src/skill_creator_mcp/tools/batch_operations.py      # 已存在
```

---

## 六、风险与依赖

### 6.1 风险

| 风险 | 概率 | 影响 | 缓解措施 |
|------|------|------|---------|
| 测试修复引入新问题 | 低 | 中 | 每次修改后运行测试 |
| 代码质量检查失败 | 低 | 低 | 遵循现有代码风格 |

### 6.2 依赖

- 无外部依赖
- Python 环境: conda base

---

## 七、后续步骤

完成后，进入下一个开发阶段。

---

**计划状态**: waiting for approval
