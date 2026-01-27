# 开发计划：拆分 requirement_collection 模块 (Phase 1.3)

> **计划日期**: 2026-01-27
> **优先级**: P1
> **预估时间**: 2-3天
> **关联计划**: feat-requirement-collection-refactor.md (已完成 Phase 1.1 & 1.2)

---

## 执行摘要

将 `requirement_collection.py` (1387行) 拆分为子包结构，提高可维护性和可测试性，同时保持100%向后兼容。

---

## 目标

| 指标 | 当前 | 目标 | 验收标准 |
|------|------|------|----------|
| 主文件行数 | 1387行 | 0行 (删除) | 拆分为子包 |
| 子模块数量 | 1个 | 6个 | 功能清晰分离 |
| 最大文件行数 | 1387行 | <450行 | 可维护 |
| 测试通过率 | 100% | 100% | 0测试失败 |
| API兼容性 | N/A | 100% | 无破坏性变更 |

---

## 技术方案

### 目标结构

```
skill-creator-mcp/src/skill_creator_mcp/utils/
├── requirement_collection/
│   ├── __init__.py              # 重导出公共API (~40行)
│   ├── session_manager.py       # SessionStateManager类 (~130行)
│   ├── elicit_workflow.py       # Elicit模式收集流程 (~425行)
│   ├── actions.py               # 操作处理器 (~110行)
│   ├── questions.py             # 问题生成 (~102行)
│   ├── validation.py            # 答案验证和处理 (~159行)
│   └── llm_services.py          # LLM分析服务 (~256行)
└── requirement_collection.py    # 旧文件 (删除)
```

### 模块职责

| 子模块 | 职责 | 主要函数/类 |
|--------|------|-------------|
| `session_manager.py` | 会话状态管理 | `SessionStateManager` |
| `elicit_workflow.py` | Elicit模式主流程 | `_collect_with_elicit` 及辅助函数 |
| `actions.py` | 操作处理器 | `_handle_requirement_*_action` |
| `questions.py` | 问题生成 | `_get_requirement_next_question` |
| `validation.py` | 答案验证和处理 | `_validate_requirement_answer`, `_process_requirement_user_answer` |
| `llm_services.py` | LLM分析服务 | `_check_requirement_completeness`, `_generate_*_question` |

### 向后兼容性保证

通过 `__init__.py` 重导出所有公共API：

```python
# utils/requirement_collection/__init__.py
from .session_manager import SessionStateManager
from .elicit_workflow import _collect_with_elicit
from .actions import (
    _get_requirement_mode_steps,
    _handle_requirement_status_action,
    _handle_requirement_previous_action,
    _handle_requirement_start_action,
)
from .questions import _get_requirement_next_question
from .validation import (
    _process_requirement_user_answer,
    _validate_requirement_answer,
    _validate_and_init_requirement_session,
)
from .llm_services import (
    _check_requirement_completeness,
    _generate_brainstorm_question,
    _generate_progressive_question,
)

__all__ = [ ... ]
```

---

## 任务清单

### 任务1: 创建子包结构
**优先级**: P0
**预估**: 1小时

- [ ] 创建 `utils/requirement_collection/` 目录
- [ ] 创建 `__init__.py` 文件（空模板）
- [ ] 验证目录结构正确

**文件**: `skill-creator-mcp/src/skill_creator_mcp/utils/requirement_collection/__init__.py`

---

### 任务2: 拆分 SessionStateManager 类
**优先级**: P0
**预估**: 30分钟

- [ ] 创建 `session_manager.py`
- [ ] 移动 `SessionStateManager` 类 (16-129行)
- [ ] 添加必要的导入语句
- [ ] 验证类功能正常

**文件**: `skill-creator-mcp/src/skill_creator_mcp/utils/requirement_collection/session_manager.py`

---

### 任务3: 拆分 LLM 服务模块
**优先级**: P0
**预估**: 1小时

- [ ] 创建 `llm_services.py`
- [ ] 移动以下函数:
  - `_check_requirement_completeness` (1132-1183行)
  - `_generate_brainstorm_question` (1205-1283行)
  - `_generate_progressive_question` (1284-1387行)
- [ ] 添加必要的导入语句
- [ ] 验证函数功能正常

**文件**: `skill-creator-mcp/src/skill_creator_mcp/utils/requirement_collection/llm_services.py`

---

### 任务4: 拆分验证模块
**优先级**: P0
**预估**: 1小时

- [ ] 创建 `validation.py`
- [ ] 移动以下函数:
  - `_validate_requirement_answer` (1059-1129行)
  - `_process_requirement_user_answer` (899-1057行)
  - `_validate_and_init_requirement_session` (557-639行)
- [ ] 处理对 `llm_services` 的导入依赖
- [ ] 验证函数功能正常

**文件**: `skill-creator-mcp/src/skill_creator_mcp/utils/requirement_collection/validation.py`

---

### 任务5: 拆分问题生成模块
**优先级**: P0
**预估**: 1小时

- [ ] 创建 `questions.py`
- [ ] 移动 `_get_requirement_next_question` (795-896行)
- [ ] 处理对 `llm_services` 的导入依赖
- [ ] 验证函数功能正常

**文件**: `skill-creator-mcp/src/skill_creator_mcp/utils/requirement_collection/questions.py`

---

### 任务6: 拆分操作处理器模块
**优先级**: P0
**预估**: 1小时

- [ ] 创建 `actions.py`
- [ ] 移动以下函数:
  - `_get_requirement_mode_steps` (633-650行)
  - `_handle_requirement_status_action` (641-670行)
  - `_handle_requirement_previous_action` (671-750行)
  - `_handle_requirement_start_action` (752-793行)
- [ ] 添加必要的导入语句
- [ ] 验证函数功能正常

**文件**: `skill-creator-mcp/src/skill_creator_mcp/utils/requirement_collection/actions.py`

---

### 任务7: 拆分 Elicit 工作流模块
**优先级**: P0
**预估**: 1.5小时

- [ ] 创建 `elicit_workflow.py`
- [ ] 移动以下函数:
  - `_initialize_session` (131-147行)
  - `_get_question_data` (149-257行)
  - `_elicit_with_retry` (258-350行)
  - `_save_answer_and_advance` (351-555行)
  - `_build_completion_result` (内置函数，需提取)
  - `_collect_with_elicit` (441-555行)
- [ ] 处理跨子模块导入依赖
- [ ] 验证函数功能正常

**文件**: `skill-creator-mcp/src/skill_creator_mcp/utils/requirement_collection/elicit_workflow.py`

---

### 任务8: 配置 __init__.py 重导出
**优先级**: P0
**预估**: 30分钟

- [ ] 编写 `__init__.py` 重导出逻辑
- [ ] 确保 `__all__` 列表完整
- [ ] 添加模块级文档字符串
- [ ] 验证所有公共API可正常导入

**文件**: `skill-creator-mcp/src/skill_creator_mcp/utils/requirement_collection/__init__.py`

---

### 任务9: 更新 server.py 导入
**优先级**: P0
**预估**: 15分钟

- [ ] 更新 `server.py` 中的导入语句
- [ ] 验证导入路径正确
- [ ] 运行 `pytest` 验证测试通过

**文件**: `skill-creator-mcp/src/skill_creator_mcp/server.py`

---

### 任务10: 删除旧文件
**优先级**: P1
**预估**: 5分钟

- [ ] 备份原始 `requirement_collection.py`
- [ ] 删除旧文件
- [ ] 验证所有测试仍通过

**文件**: `skill-creator-mcp/src/skill_creator_mcp/utils/requirement_collection.py`

---

## 验收标准

### 功能测试
```bash
# 运行完整测试套件
cd skill-creator-mcp
uv run pytest --cov

# 预期结果
# - 608/608 测试通过
# - 覆盖率 ≥95%
```

### 代码质量检查
```bash
# Ruff 检查
uv run ruff check src/skill_creator_mcp/utils/requirement_collection/

# MyPy 检查
uv run mypy src/skill_creator_mcp/utils/requirement_collection/

# 预期结果
# - 0 错误
```

### API 兼容性测试
```python
# 验证旧导入仍可工作
from skill_creator_mcp.utils.requirement_collection import (
    _collect_with_elicit,
    _get_requirement_mode_steps,
    _get_requirement_next_question,
    _handle_requirement_previous_action,
    _handle_requirement_start_action,
    _handle_requirement_status_action,
    _process_requirement_user_answer,
    _validate_and_init_requirement_session,
)
```

---

## 风险与缓解

| 风险 | 影响 | 概率 | 缓解措施 |
|------|------|------|----------|
| 循环导入 | 高 | 中 | 使用延迟导入或重构依赖关系 |
| 测试失败 | 高 | 低 | 使用 `__init__.py` 重导出保持兼容性 |
| 破坏性变更 | 高 | 低 | 完整的向后兼容性测试 |
| 导入路径错误 | 中 | 中 | 逐步验证每个子模块 |

---

## 关键文件

**需要修改的文件**:
1. `skill-creator-mcp/src/skill_creator_mcp/utils/requirement_collection.py` (删除)
2. `skill-creator-mcp/src/skill_creator_mcp/server.py` (更新导入)

**需要创建的文件**:
1. `skill-creator-mcp/src/skill_creator_mcp/utils/requirement_collection/__init__.py`
2. `skill-creator-mcp/src/skill_creator_mcp/utils/requirement_collection/session_manager.py`
3. `skill-creator-mcp/src/skill_creator_mcp/utils/requirement_collection/llm_services.py`
4. `skill-creator-mcp/src/skill_creator_mcp/utils/requirement_collection/validation.py`
5. `skill-creator-mcp/src/skill_creator_mcp/utils/requirement_collection/questions.py`
6. `skill-creator-mcp/src/skill_creator_mcp/utils/requirement_collection/actions.py`
7. `skill-creator-mcp/src/skill_creator_mcp/utils/requirement_collection/elicit_workflow.py`

**测试文件**（无需修改，验证兼容性）:
1. `skill-creator-mcp/tests/test_utils/test_requirement_collection.py`
2. `skill-creator-mcp/tests/test_tools/test_collect_requirements.py`
3. `skill-creator-mcp/tests/test_integration/test_requirement_collection.py`

---

## 参考文档

- 架构审计报告: `ARCHITECTURE_AUDIT_REPORT_v2.md`
- 需求收集架构文档: `skill-creator/references/requirement-collection-architecture.md`
- 阶段汇报: `.claude/plans/archive/2026-01-27-requirement-collection-refactor-report.md`

---

**计划状态**: 待审核
**下一步**: 用户批准后开始执行任务1
