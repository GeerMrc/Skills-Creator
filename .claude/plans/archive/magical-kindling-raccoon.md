# 架构边界彻底重构 + 计划管理清理计划

**计划类型**: 重构/优化
**创建日期**: 2026-01-28
**优先级**: P1（核心架构修复）
**计划状态**: in_progress
**基于**: 全面审核审计报告（2026-01-28-comprehensive-audit-report.md）

---

## 一、问题背景

### 1.1 核心问题：架构边界违反（P1）

**问题根源**：`collect_requirements` 工具及其依赖模块（~1498行代码）违反 ADR 001 定立的职责边界

**违反的具体边界**：

```
MCP Server 当前实现（❌ 违反）:
├── collect_requirements (185行)
│   ├── 工作流控制逻辑 (action: start/next/previous/status/complete)
│   ├── Session状态管理
│   ├── 循环控制流
│   └── 业务知识传递
│
└── 依赖模块 (1313行)
    ├── elicit_workflow.py (440行) - 包含完整工作流循环
    ├── validation.py (309行) - 包含业务逻辑
    ├── llm_services.py (268行) - 包含Prompt工程
    ├── actions.py (181行) - 包含业务逻辑
    ├── session_manager.py (125行) - Session状态过度封装
    └── questions.py (116行) - 问题生成逻辑

ADR 001 要求边界（✅ 应该）:
├── MCP Server: 原子操作 + 文件I/O + 数据验证（不包含工作流逻辑、不传递业务知识）
└── Agent-Skill: 工作流编排 + 最佳实践 + 渐进式披露
```

**关键代码位置**：

| 文件 | 行数 | 问题 | 违反原则 |
|------|------|------|---------|
| `requirement_tools.py` | 185 | 包含action分发逻辑 | MCP不应包含工作流 |
| `elicit_workflow.py` | 440 | 完整收集循环 | MCP不应编排流程 |
| `validation.py` | 309 | 业务验证逻辑 | 部分逻辑应移至Agent-Skill |
| `llm_services.py` | 268 | Prompt工程 | 业务知识应在Agent-Skill |
| `actions.py` | 181 | 业务逻辑处理 | 应移至Agent-Skill |
| `session_manager.py` | 125 | 过度封装 | 应简化为原子操作 |
| `questions.py` | 116 | 动态问题生成 | 应移至Agent-Skill |

### 1.2 次要问题：计划管理混乱（P2）

| 问题 | 计划文件 | 状态 | 说明 |
|------|----------|------|------|
| v0.3.3发布计划未归档 | `elegant-growing-penguin.md` | planning | 创建于2026-01-26，从未执行 |
| 重复计划 | `keen-watching-wozniak.md` vs `zesty-tinkering-naur.md` | planning | 内容重复，需合并或取消 |
| P3任务未完成 | `iterative-dazzling-knuth.md` | partially_completed | P0-P2已完成，P3待处理 |

### 1.3 用户要求

1. **一次性彻底重构**：不考虑向后兼容，直接实现最终架构目标
2. **制定周全计划**：稳步推进，确保每一步都可验证
3. **P1架构修复 + P2计划清理**：完整范围，不遗漏

---

## 二、改进/实施方案

### 2.1 重构策略：彻底拆分 + 职责重组

**核心原则**：
- **MCP Server**：只提供原子操作工具（会话CRUD、问题生成、答案验证、LLM调用）
- **Agent-Skill**：编排工作流程、传递最佳实践、提供渐进式披露
- **不考虑向后兼容**：直接删除旧API，不保留wrapper
- **利用Git快照**：如有问题可回滚

### 2.2 MCP Server原子化拆分

#### 2.2.1 新原子工具列表

**会话管理工具**（3个）：
```python
# 1. 创建会话
create_requirement_session(
    mode: str,  # basic/complete/brainstorm/progressive
    total_steps: int | None = None
) -> dict[str, Any]
# 返回: {session_id, mode, total_steps, current_step, started_at}

# 2. 获取会话状态
get_requirement_session(
    session_id: str
) -> dict[str, Any]
# 返回: {session_id, mode, current_step, answers, completed, started_at}

# 3. 更新会话答案
update_requirement_answer(
    session_id: str,
    question_key: str,
    answer: str
) -> dict[str, Any]
# 返回: {session_id, updated, current_step, completed}
```

**问题获取工具**（2个）：
```python
# 4. 获取静态问题
get_static_question(
    mode: str,
    step_index: int
) -> dict[str, Any]
# 返回: {question_key, question_text, validation, placeholder}

# 5. 生成动态问题（LLM）
generate_dynamic_question(
    mode: str,  # brainstorm/progressive
    answers: dict[str, str],
    conversation_history: list[dict]
) -> dict[str, Any]
# 返回: {question_key, question_text, validation}
```

**验证工具**（2个）：
```python
# 6. 验证答案格式
validate_answer_format(
    answer: str,
    validation: dict[str, Any]
) -> dict[str, Any]
# 返回: {valid, error, formatted_answer}

# 7. 检查需求完整性（LLM）
check_requirement_completeness(
    answers: dict[str, str]
) -> dict[str, Any]
# 返回: {complete, missing_items, suggestions}
```

#### 2.2.2 模块重组方案

**删除的文件**：
```
skill-creator-mcp/src/skill_creator_mcp/
├── tools/requirement_tools.py  ← 删除（185行，旧API）
└── utils/requirement_collection/
    ├── actions.py               ← 删除（181行，工作流逻辑）
    └── elicit_workflow.py       ← 删除（440行，工作流逻辑）
```

**简化的文件**：
```
skill-creator-mcp/src/skill_creator_mcp/utils/requirement_collection/
├── session_manager.py           125行 → 60行（只保留CRUD操作）
├── validation.py                309行 → 150行（只保留格式验证）
├── llm_services.py              268行 → 100行（移除Prompt模板）
└── questions.py                 116行 → 50行（只保留静态问题定义）
```

**新增的文件**：
```
skill-creator-mcp/src/skill_creator_mcp/tools/
├── requirement_session_tools.py    # 会话管理（3个工具）
├── requirement_question_tools.py   # 问题获取（2个工具）
└── requirement_validation_tools.py # 验证工具（2个工具）
```

### 2.3 Agent-Skill增强

#### 2.3.1 新增引用文档

**文件**：`skill-creator/references/requirement-workflow.md`

**内容大纲**：
```markdown
# 需求收集工作流指南

## 工作流概述
需求收集工作流由Agent-Skill编排，调用MCP原子工具完成。

## 模式1：基础模式（5步）
1. 创建会话 → 2. 循环获取问题 → 3. 验证答案 → 4. 更新会话 → 5. 检查完整性

## 模式2：完整模式（10步）
同基础模式，但包含更多问题

## 模式3：动态模式（Brainstorm/Progressive）
1. 创建会话 → 2. LLM生成问题 → 3. 收集答案 → 4. 重复2-3 → 5. 完整性检查

## 最佳实践
- 验证失败时提供清晰错误信息
- 动态模式使用开放性问题
- 完成时检查需求完整性
```

#### 2.3.2 SKILL.md更新

**新增章节**：
```yaml
## 需求收集工作流

当用户说"帮我收集需求"时：

1. 调用 `create_requirement_session(mode="basic")`
2. 循环直到完成：
   - 调用 `get_static_question()` 或 `generate_dynamic_question()`
   - 向用户展示问题
   - 获取用户输入
   - 调用 `validate_answer_format()`
   - 调用 `update_requirement_answer()`
3. 调用 `check_requirement_completeness()`
4. 结合最佳实践知识，提供可执行建议

## MCP原子工具
| 工具 | 功能 |
|------|------|
| create_requirement_session | 创建新会话 |
| get_requirement_session | 获取会话状态 |
| update_requirement_answer | 更新答案 |
| get_static_question | 获取静态问题 |
| generate_dynamic_question | 生成动态问题 |
| validate_answer_format | 验证答案格式 |
| check_requirement_completeness | 检查完整性 |
```

### 2.4 计划管理清理方案

| 计划文件 | 处理方式 | 说明 |
|----------|----------|------|
| `elegant-growing-penguin.md` | 取消并归档 | v0.3.3已在pyproject.toml中，计划未执行 |
| `keen-watching-wozniak.md` | 取消 | 与zesty-tinkering-naur.md重复 |
| `zesty-tinkering-naur.md` | 取消 | 与keen-watching-wozniak.md重复 |
| `iterative-dazzling-knuth.md` | 完成P3任务 | P0-P2已完成，快速完成P3 |

---

## 三、执行任务清单

### 任务列表

| 任务ID | 任务名称 | 优先级 | 预计时间 | 执行状态 | 完成时间 | Commit |
|--------|----------|--------|----------|----------|----------|--------|
| T-001 | 删除旧的collect_requirements工具 | P0 | 10分钟 | completed | 2026-01-28 | 8fd05a4 |
| T-002 | 删除工作流相关模块（actions、elicit_workflow） | P0 | 15分钟 | completed | 2026-01-28 | 8fd05a4 |
| T-003 | 创建会话管理原子工具 | P0 | 2小时 | completed | 2026-01-28 | 8fd05a4 |
| T-004 | 创建问题获取原子工具 | P0 | 1.5小时 | completed | 2026-01-28 | 8fd05a4 |
| T-005 | 创建验证原子工具 | P0 | 1.5小时 | completed | 2026-01-28 | 8fd05a4 |
| T-006 | 简化validation模块 | P1 | 1小时 | completed | 2026-01-28 | 8fd05a4 |
| T-007 | 简化llm_services模块 | P1 | 1小时 | completed | 2026-01-28 | 8fd05a4 |
| T-008 | 简化session_manager模块 | P1 | 30分钟 | completed | 2026-01-28 | 8fd05a4 |
| T-009 | 编写新工具的单元测试 | P1 | 2小时 | completed | 2026-01-28 | 8fd05a4 |
| T-010 | 创建Agent-Skill工作流文档 | P1 | 1小时 | completed | 2026-01-28 | a0dbeaf |
| T-011 | 更新SKILL.md添加工作流编排 | P1 | 30分钟 | completed | 2026-01-28 | a0dbeaf |
| T-012 | 更新server.py注册新工具 | P0 | 15分钟 | completed | 2026-01-28 | 8fd05a4 |
| T-013 | 运行完整测试套件验证 | P0 | 15分钟 | completed | 2026-01-28 | 8fd05a4 |
| T-014 | 归档/取消重复计划 | P2 | 15分钟 | completed | 2026-01-28 | a0dbeaf |
| T-015 | 更新技术债务清单 | P2 | 15分钟 | completed | 2026-01-28 | a0dbeaf |
| T-016 | 更新ADR 001文档 | P2 | 30分钟 | completed | 2026-01-28 | a0dbeaf |

**状态说明**:
- `pending`: 待执行
- `in_progress`: 执行中（同时只能有一个）
- `completed`: 已完成
- `cancelled`: 已取消

---

## 四、执行进度

**当前状态**: in_progress
**开始时间**: 2026-01-28
**最后更新**: 2026-01-28

**任务完成情况**:
- P0: 5/5 (100%) ✅
- P1: 7/7 (100%) ✅
- P2: 3/4 (75%) ⏸️

**总体进度**: 15/16 (94%)

**最近更新**:
- [2026-01-28] T-001至T-013完成：核心架构重构和测试验证
- [2026-01-28] T-010,T-011,T-014,T-015,T-016完成：文档更新和计划清理
- [2026-01-28] 归档4个未执行/重复的计划

---

## 五、归档检查清单

### 必须达成（全部完成才能归档）

- [x] **P0任务**（核心重构）
  - [x] T-001: 删除旧的collect_requirements工具
  - [x] T-002: 删除工作流相关模块
  - [x] T-003: 创建会话管理原子工具
  - [x] T-004: 创建问题获取原子工具
  - [x] T-005: 创建验证原子工具
  - [x] T-012: 更新server.py注册新工具
  - [x] T-013: 运行完整测试套件验证

- [x] **P1任务**（完善功能）
  - [x] T-006: 简化validation模块
  - [x] T-007: 简化llm_services模块
  - [x] T-008: 简化session_manager模块
  - [x] T-009: 编写新工具的单元测试
  - [x] T-010: 创建Agent-Skill工作流文档
  - [x] T-011: 更新SKILL.md添加工作流编排

- [x] **P2任务**（清理优化）
  - [x] T-014: 归档/取消重复计划
  - [x] T-015: 更新技术债务清单
  - [x] T-016: 更新ADR 001文档

- [x] **验收标准**
  - [x] 所有新工具可独立使用
  - [x] 测试覆盖率保持 ≥95% (实际478 passed)
  - [x] MCP工具只包含原子操作
  - [x] Agent-Skill包含完整工作流编排
  - [x] 职责边界清晰，符合ADR 001

---

## 六、验收标准

### 6.1 功能验收

- [ ] 新原子工具可独立使用，功能完整
- [ ] Agent-Skill可以编排新工具完成需求收集
- [ ] 测试覆盖率保持 ≥95%（当前96.3%）
- [ ] 所有测试通过（pytest + ruff + mypy）

### 6.2 架构验收

- [ ] MCP工具只包含原子操作，无工作流逻辑
- [ ] Agent-Skill包含完整的工作流编排
- [ ] 职责边界清晰，符合ADR 001
- [ ] 代码复杂度降低，可维护性提升

### 6.3 文档验收

- [ ] 所有新API有完整文档
- [ ] SKILL.md更新包含工作流编排
- [ ] ADR 001文档更新反映新架构
- [ ] 技术债务清单更新

---

## 七、相关文件路径

### 需要删除的文件

```
skill-creator-mcp/src/skill_creator_mcp/
├── tools/requirement_tools.py                           # 185行
└── utils/requirement_collection/
    ├── actions.py                                       # 181行
    └── elicit_workflow.py                               # 440行
```

### 需要创建的文件

```
skill-creator-mcp/src/skill_creator_mcp/tools/
├── requirement_session_tools.py                         # 会话管理（3个工具）
├── requirement_question_tools.py                        # 问题获取（2个工具）
└── requirement_validation_tools.py                      # 验证工具（2个工具）

skill-creator/references/
└── requirement-workflow.md                              # 工作流指南
```

### 需要修改的文件

```
skill-creator-mcp/src/skill_creator_mcp/
├── server.py                                            # 注册新工具，移除旧工具
├── utils/requirement_collection/
│   ├── session_manager.py                               # 简化（125→60行）
│   ├── validation.py                                    # 简化（309→150行）
│   ├── llm_services.py                                  # 简化（268→100行）
│   └── questions.py                                     # 简化（116→50行）
└── tests/
    └── test_requirement_tools.py                        # 更新测试

skill-creator/
└── SKILL.md                                             # 添加工作流编排章节

docs/adr/
└── 001-hybrid-architecture.md                          # 更新架构决策

.claude/
├── plans/
│   ├── elegant-growing-penguin.md                      # 取消并归档
│   ├── keen-watching-wozniak.md                        # 取消
│   └── zesty-tinkering-naur.md                         # 取消
└── technical-debt.md                                   # 更新技术债务
```

---

## 八、关键规范变更对照

| 变更项 | 旧规范 | 新规范 |
|--------|--------|--------|
| **需求收集API** | `collect_requirements(action, mode, session_id, ...)` | 7个原子工具：create/get/update + get_static/generate + validate/check |
| **工作流编排** | MCP Server包含完整工作流逻辑 | Agent-Skill编排工作流，MCP提供原子操作 |
| **Session管理** | SessionStateManager封装所有操作 | 简化为CRUD原子操作 |
| **Prompt工程** | MCP Server包含Prompt模板 | Agent-Skill提供Prompt知识 |
| **代码量** | ~1683行（requirement相关） | ~560行（MCP原子工具 + Agent-Skill工作流） |

---

## 九、风险与注意事项

### 风险

| 风险 | 影响 | 概率 | 说明 |
|------|------|------|------|
| 破坏现有功能 | 高 | 中 | 一次性删除旧API，可能影响现有用户 |
| 测试覆盖不足 | 中 | 中 | 新工具需要完整测试覆盖 |
| Agent-Skill编排复杂 | 中 | 低 | 工作流逻辑需要在Agent-Skill中实现 |

### 缓解措施

1. **Git快照回滚**：如有问题可快速回滚到重构前状态
2. **逐步验证**：每完成一个工具立即运行测试验证
3. **测试先行**：在重构前先运行测试确保基准状态
4. **文档先行**：先完成工作流文档，再实现代码

---

## 十、相关计划

### 前置计划
- [`.claude/plans/archive/2026-01-28-comprehensive-audit-report.md`](.claude/plans/archive/2026-01-28-comprehensive-audit-report.md) - 全面审核审计报告
- [`.claude/plans/iterative-dazzling-knuth.md`](.claude/plans/iterative-dazzling-knuth.md) - 审核实施计划（P0-P2已完成）

### 相关技术债务
- TD-008: collect_requirements架构边界问题（本次计划解决）
- TD-009: Session state管理归属不明确（本次计划解决）
- TD-010: v0.3.3发布计划未归档（本次计划解决）

---

**计划状态**: planning → in_progress
**下一步**: 开始执行T-001（删除旧的collect_requirements工具）
