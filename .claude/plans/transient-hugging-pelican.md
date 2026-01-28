# 审核发现修复计划 - 文档数据一致性修复

> **计划ID**: transient-hugging-pelican
> **创建日期**: 2026-01-28
> **状态**: planning
> **审核范围**: Skills-Creator 项目全面审核审计

---

## 执行摘要

基于对项目的全面审核审计，发现以下核心问题需要修复：

| 问题类型 | 数量 | 优先级 |
|---------|------|--------|
| 文档数据不一致 | 7 处 | P0 |
| 孤立测试文件 | 1 个 | P1 |
| 测试覆盖率缺口 | 0% (88行代码) | P1 |

---

## 一、问题详情

### P0-1: 测试数量声明不一致 (7处)

**实际测试数量**: 533 个（已验证）

| 文件 | 行号 | 错误值 | 正确值 |
|------|------|--------|--------|
| CLAUDE.md | 20 | "95% (614个测试用例)" | "92% (533个测试用例)" |
| CLAUDE.md | 61 | "95% 覆盖率, 614个测试" | "92% 覆盖率, 533个测试" |
| README.md | 5 | "96% (619 tests)" | "92% (533 tests)" |
| skill-creator-mcp/README.md | 5 | "619 passed" | "533 passed" |

### P0-2: 工具数量声明不一致 (3处)

**实际工具数量**: 20 个（已验证 server.py 中 @mcp.tool() 装饰器）

| 文件 | 行号 | 错误值 | 正确值 |
|------|------|--------|--------|
| SKILL.md | 98 | "**原子工具 (18)**:" | "**原子工具 (20)**:" |
| SKILL.md | 121 | "**技术验证 (2)**:" | "**技术验证 (5)**:" |
| SKILL.md | 123 | "7个需求收集原子工具 + 11个其他工具" | "7个需求收集原子工具 + 13个其他工具" |
| CLAUDE.md | 38 | "17 Tools (5类)" | "20 Tools (5类)" |

### P1-1: 孤立的测试文件

**文件路径**: `/models/claude-glm/Skills-Creator/skill-creator-mcp/test_phase0_direct.py`

**问题**:
- 位置错误（应在 `tests/` 目录而非根目录）
- 尝试导入不存在的函数（`_generate_brainstorm_question`）
- 造成测试收集时的 ImportError

### P1-2: requirement_collection 模块 0% 测试覆盖率

**模块路径**: `src/skill_creator_mcp/utils/requirement_collection/`

**未覆盖的文件**（共 88 行代码）:
| 文件 | 行数 | 覆盖率 |
|------|------|--------|
| `__init__.py` | 5 | 0% |
| `llm_services.py` | 25 | 0% |
| `questions.py` | 17 | 0% |
| `session_manager.py` | 13 | 0% |
| `validation.py` | 28 | 0% |

---

## 二、任务清单

### 任务 T-01: 修复测试数量数据不一致

**优先级**: P0
**预计工作量**: 15 分钟

**涉及文件**:
- `CLAUDE.md` (第20行, 第61行)
- `README.md` (第5行)
- `skill-creator-mcp/README.md` (第5行)

**修改内容**:
```markdown
# CLAUDE.md 第20行
- **测试覆盖率**: 95% (614个测试用例)
+ **测试覆盖率**: 92% (533个测试用例)

# CLAUDE.md 第61行
- │   ├── tests/                  # 测试套件 (95% 覆盖率, 614个测试)
+ │   ├── tests/                  # 测试套件 (92% 覆盖率, 533个测试)

# README.md 第5行
- > **测试覆盖率**: 96% (619 tests)
+ > **测试覆盖率**: 92% (533 tests)

# skill-creator-mcp/README.md 第5行
- [![Tests](https://img.shields.io/badge/tests-619%20passed-success](#)
+ [![Tests](https://img.shields.io/badge/tests-533%20passed-success](#)
```

---

### 任务 T-02: 修复工具数量数据不一致

**优先级**: P0
**预计工作量**: 20 分钟

**涉及文件**:
- `skill-creator/SKILL.md` (第98行, 第121行, 第123行)
- `CLAUDE.md` (第38行)

**修改内容**:
```markdown
# SKILL.md 第98行
- **原子工具 (18)**:
+ **原子工具 (20)**:

# SKILL.md 第121行
- **技术验证 (2)**: check_client_capabilities | test_llm_sampling | test_user_elicitation | test_conversation_loop | test_requirement_completeness
+ **技术验证 (5)**: check_client_capabilities | test_llm_sampling | test_user_elicitation | test_conversation_loop | test_requirement_completeness

# SKILL.md 第123行
- > 注：7个需求收集原子工具 + 11个其他工具
+ > 注：7个需求收集原子工具 + 13个其他工具

# CLAUDE.md 第38行
- │  │  - 17 Tools (5类)                  │  │
+ │  │  - 20 Tools (5类)                  │  │
```

---

### 任务 T-03: 移除孤立的测试文件

**优先级**: P1
**预计工作量**: 10 分钟

**涉及文件**:
- 删除: `skill-creator-mcp/test_phase0_direct.py`

**操作**:
```bash
rm /models/claude-glm/Skills-Creator/skill-creator-mcp/test_phase0_direct.py
```

**验证**:
```bash
# 1. 确认文件已删除
ls skill-creator-mcp/test_phase0_direct.py  # 应报错

# 2. 确认测试收集无错误
cd skill-creator-mcp && uv run pytest --collect-only -q 2>&1 | grep -i error
```

---

### 任务 T-04: 添加 requirement_collection 测试覆盖

**优先级**: P1
**预计工作量**: 2-3 小时

**新建目录**: `skill-creator-mcp/tests/test_utils/test_requirement_collection/`

**测试文件清单**:

| 测试文件 | 测试用例数 | 预计行数 |
|---------|-----------|---------|
| `test_init.py` | 5 | 50 |
| `test_session_manager.py` | 12 | 150 |
| `test_questions.py` | 10 | 120 |
| `test_validation.py` | 8 | 100 |
| `test_llm_services.py` | 6 | 100 |

**关键测试用例**:
- `test_create_session_basic_mode`
- `test_get_session_success`
- `test_update_answer_success`
- `test_get_static_question_basic_mode`
- `test_generate_dynamic_question_brainstorm_mode`
- `test_validate_answer_format_success`
- `test_check_requirement_completeness_complete`
- `test_generate_brainstorm_question_success`

**目标覆盖率**: ≥90%

---

## 三、执行计划

### 推荐执行顺序

```
T-03 (清理孤立文件)
    ↓
T-01 (修复测试数量)
    ↓
T-02 (修复工具数量)
    ↓
T-04 (添加测试覆盖)
```

### 步骤 0: 前置任务审核

- [x] 已理解三个审核报告的内容
- [x] 已确认所有数据不一致问题
- [x] 已验证实际测试数量（533）
- [x] 已验证实际工具数量（20）
- [x] 当前分支: `develop`
- [x] Git状态: Working tree clean, 领先远程 23 个提交

### 步骤 1-9: 按九步法执行

遵循 CLAUDE.md 第二章九步法执行开发工作。

---

## 四、验收标准

### P0 任务验收（必须 100% 完成）

| 验收项 | 检查命令 | 通过标准 |
|--------|----------|----------|
| 测试数量一致性 | `grep -n "533" CLAUDE.md README.md skill-creator-mcp/README.md` | 所有文档显示 533 |
| 无旧测试数量 | `! grep -r "614\|619" CLAUDE.md README.md skill-creator-mcp/README.md` | 无 614 或 619 |
| 工具数量一致性 | `grep -n "20 Tools\|原子工具 (20)" SKILL.md CLAUDE.md` | 显示 20 |
| 技术验证工具数 | `grep -n "技术验证 (5)" SKILL.md` | 显示 5 |

### P1 任务验收

| 验收项 | 检查命令 | 通过标准 |
|--------|----------|----------|
| 孤立文件已移除 | `ls skill-creator-mcp/test_phase0_direct.py` | 文件不存在 |
| 测试收集无错误 | `pytest --collect-only -q` | 无 ERROR |
| 覆盖率提升 | `pytest --cov=src/skill_creator_mcp/utils/requirement_collection` | ≥90% |

### 质量标准

| 指标 | 当前值 | 目标值 |
|------|--------|--------|
| 测试数量 | 533 | 600+ |
| 测试覆盖率 | 92% | ≥93% |
| ruff 检查 | 0 错误 | 0 错误 |
| mypy 检查 | 0 错误 | 0 错误 |

---

## 五、关键文件清单

### 需要修改的文件

1. `/models/claude-glm/Skills-Creator/CLAUDE.md`
2. `/models/claude-glm/Skills-Creator/README.md`
3. `/models/claude-glm/Skills-Creator/skill-creator/SKILL.md`
4. `/models/claude-glm/Skills-Creator/skill-creator-mcp/README.md`

### 需要删除的文件

1. `/models/claude-glm/Skills-Creator/skill-creator-mcp/test_phase0_direct.py`

### 需要新建的目录

1. `/models/claude-glm/Skills-Creator/skill-creator-mcp/tests/test_utils/test_requirement_collection/`

### 验证参考文件

1. `/models/claude-glm/Skills-Creator/skill-creator-mcp/src/skill_creator_mcp/server.py` (20 个工具的来源)
2. `/models/claude-glm/Skills-Creator/skill-creator-mcp/src/skill_creator_mcp/utils/requirement_collection/` (需测试覆盖的模块)

---

## 六、进度追踪

**当前状态**: completed
**开始时间**: 2026-01-28
**完成时间**: 2026-01-28
**任务完成进度**: 4/4 (100%)
**最近更新**: 2026-01-28

### 任务状态表

| 任务ID | 任务名称 | 优先级 | 状态 | 完成时间 | Commit |
|--------|----------|--------|------|----------|--------|
| T-01 | 修复测试数量数据不一致 | P0 | completed | 2026-01-28 | cf16b90 |
| T-02 | 修复工具数量数据不一致 | P0 | completed | 2026-01-28 | cf16b90 |
| T-03 | 移除孤立的测试文件 | P1 | completed | 2026-01-28 | cf16b90 |
| T-04 | 添加 requirement_collection 测试覆盖 | P1 | completed | 2026-01-28 | cf16b90 |

---

## 七、风险评估

| 风险 | 可能性 | 影响 | 缓解措施 |
|------|--------|------|----------|
| 文档修改引入新错误 | 低 | 中 | 修改后使用 grep 验证 |
| 测试编写时间超出预期 | 中 | 低 | 先写核心测试，逐步完善 |
| 覆盖率未达 90% | 低 | 低 | 调整测试范围，优先覆盖关键路径 |

---

## 八、附录

### 工具分类清单（20个工具）

```
1. 会话管理 (3个):
   - create_requirement_session_tool
   - get_requirement_session_tool
   - update_requirement_answer_tool

2. 问题获取 (2个):
   - get_static_question_tool
   - generate_dynamic_question_tool

3. 验证工具 (2个):
   - validate_answer_format_tool
   - check_requirement_completeness_tool

4. 技能工具 (4个):
   - init_skill
   - validate_skill
   - analyze_skill
   - refactor_skill

5. 打包工具 (2个):
   - package_skill
   - package_agent_skill

6. 批量操作 (2个):
   - batch_validate_skills_tool
   - batch_analyze_skills_tool

7. 健康检查 (3个):
   - health_check_tool
   - quick_status_tool
   - is_healthy_tool

8. 技术验证 (5个):
   - check_client_capabilities
   - test_llm_sampling
   - test_user_elicitation
   - test_conversation_loop
   - test_requirement_completeness
```
