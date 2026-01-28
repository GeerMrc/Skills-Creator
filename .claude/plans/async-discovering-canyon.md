# 计划管理清理计划

**计划ID**: async-discovering-canyon
**创建日期**: 2026-01-28
**计划类型**: 清理 + 测试补充
**优先级**: P2

---

## 执行摘要

### 问题背景

基于**100%代码审核**（非仅依据文档或commit摘要），发现以下需要处理的问题：

| 问题ID | 严重性 | 问题描述 | 来源 |
|--------|--------|----------|------|
| **ISSUE-001** | ⚠️ P2 | `generic-seeking-toast.md` (916行) 审核报告未归档 | 计划目录审核 |
| **ISSUE-002** | ⚠️ P2 | 新增7个原子工具缺少单元测试 | 测试覆盖率审核 |
| **ISSUE-003** | ⚠️ P3 | 测试覆盖率从96%降至95% | 测试验证审核 |

### 已确认通过的内容

| 审核项 | 结果 | 证据 |
|--------|------|------|
| 架构重构代码完整性 | ✅ 100% | 旧文件删除、新工具完整、行数符合预期 |
| ADR 001合规性 | ✅ 100% | MCP提供原子操作，职责边界清晰 |
| Git提交规范 | ✅ 100% | 提交序列符合九步法，格式正确 |
| 文档更新完整性 | ✅ 100% | 新增308行工作流指南，更新到位 |
| 技术债务修复 | ✅ 100% | TD-008/009/010已修复，评分0分 |
| 前置计划归档 | ✅ 基本符合 | magical-kindling-raccoon.md 已归档 |

---

## 一、计划目标

### 1.1 主要目标

1. **清理计划目录**: 归档 `generic-seeking-toast.md` 审核报告
2. **补充单元测试**: 为7个新增原子工具添加单元测试
3. **验证测试覆盖**: 确保测试覆盖率恢复到≥95%

### 1.2 非目标

- 不修改已完成的架构重构代码
- 不修改现有的集成测试
- 不添加新的功能

---

## 二、任务清单

### P2 任务（核心）

| 任务ID | 任务名称 | 状态 | 优先级 | 预估时间 | 完成时间 | Commit |
|--------|----------|------|--------|----------|----------|--------|
| T-201 | 归档审核报告 generic-seeking-toast.md | pending | P2 | 15分钟 | - | - |
| T-202 | 创建 test_requirement_session_tools.py | pending | P2 | 2小时 | - | - |
| T-203 | 创建 test_requirement_question_tools.py | pending | P2 | 2小时 | - | - |
| T-204 | 创建 test_requirement_validation_tools.py | pending | P2 | 2小时 | - | - |

### P3 任务（次要）

| 任务ID | 任务名称 | 状态 | 优先级 | 预估时间 | 完成时间 | Commit |
|--------|----------|------|--------|----------|----------|--------|
| T-301 | 运行测试验证覆盖率≥95% | pending | P3 | 10分钟 | - | - |
| T-302 | 更新 ISSUES.md 和 CHANGELOG.md | pending | P3 | 15分钟 | - | - |

**总计**: 6个任务，预估6小时40分钟

---

## 三、详细实施步骤

### T-201: 归档审核报告

**文件位置**: `.claude/plans/generic-seeking-toast.md`

**操作步骤**:
```bash
# 1. 移动到归档目录
git mv .claude/plans/generic-seeking-toast.md \
   .claude/plans/archive/2026-01-27-audit-generic-seeking-toast.md

# 2. 提交变更
git commit -m "chore(plans): 归档项目全面审核报告

- 审核报告已完成历史使命
- 报告中的重构建议已由 magical-kindling-raccoon.md 执行
- 保留审核报告作为历史参考

Closes ISSUE-001"
```

**验收标准**:
- [ ] 文件已移动到 `archive/` 目录
- [ ] Git commit 已创建
- [ ] `.claude/plans/` 目录整洁

---

### T-202: 创建会话管理工具单元测试

**文件位置**: `skill-creator-mcp/tests/test_tools/test_requirement_session_tools.py`

**测试工具** (3个):
1. `create_requirement_session` - 创建会话
2. `get_requirement_session` - 获取会话状态
3. `update_requirement_answer` - 更新答案

**参考文件**: `tests/test_tools/test_init_skill.py`

**测试用例清单** (预计12个):
- [ ] `test_create_requirement_session_basic_mode`
- [ ] `test_create_requirement_session_complete_mode`
- [ ] `test_create_requirement_session_brainstorm_mode`
- [ ] `test_create_requirement_session_invalid_mode`
- [ ] `test_create_requirement_session_custom_total_steps`
- [ ] `test_get_requirement_session_success`
- [ ] `test_get_requirement_session_not_found`
- [ ] `test_update_requirement_answer_success`
- [ ] `test_update_requirement_answer_session_not_found`
- [ ] `test_update_requirement_answer_invalid_step`
- [ ] `test_update_requirement_answer_preserves_history`
- [ ] `test_session_state_management_flow`

**验收标准**:
- [ ] 测试文件已创建
- [ ] 所有测试用例通过
- [ ] 使用 pytest + fastmcp Context Mock

---

### T-203: 创建问题获取工具单元测试

**文件位置**: `skill-creator-mcp/tests/test_tools/test_requirement_question_tools.py`

**测试工具** (2个):
1. `get_static_question` - 获取静态问题
2. `generate_dynamic_question` - 生成动态问题

**参考文件**: `tests/test_tools/test_validate_skill.py`

**测试用例清单** (预计13个):
- [ ] `test_get_static_question_basic_mode_step_0_to_4`
- [ ] `test_get_static_question_complete_mode_all_steps`
- [ ] `test_get_static_question_invalid_mode`
- [ ] `test_get_static_question_invalid_step_index`
- [ ] `test_get_static_question_returns_valid_structure`
- [ ] `test_generate_dynamic_question_brainstorm_mode`
- [ ] `test_generate_dynamic_question_progressive_mode`
- [ ] `test_generate_dynamic_question_with_context`
- [ ] `test_generate_dynamic_question_invalid_mode`
- [ ] `test_generate_dynamic_question_llm_failure_handling`
- [ ] `test_generate_dynamic_question_returns_valid_structure`
- [ ] `test_generate_dynamic_question_context_integration`
- [ ] `test_question_tools_maintain_atomicity`

**验收标准**:
- [ ] 测试文件已创建
- [ ] 所有测试用例通过
- [ ] LLM mock 正确实现

---

### T-204: 创建验证工具单元测试

**文件位置**: `skill-creator-mcp/tests/test_tools/test_requirement_validation_tools.py`

**测试工具** (2个):
1. `validate_answer_format` - 验证答案格式
2. `check_requirement_completeness` - 检查完整性

**参考文件**: `tests/test_utils/test_testing.py`

**测试用例清单** (预计12个):
- [ ] `test_validate_answer_format_valid_text`
- [ ] `test_validate_answer_format_valid_json`
- [ ] `test_validate_answer_format_invalid_json`
- [ ] `test_validate_answer_format_custom_rules`
- [ ] `test_validate_answer_format_returns_bool`
- [ ] `test_check_requirement_completeness_basic_mode`
- [ ] `test_check_requirement_completeness_complete_mode`
- [ ] `test_check_requirement_completeness_brainstorm_mode`
- [ ] `test_check_requirement_completeness_incomplete_session`
- [ ] `test_check_requirement_completeness_llm_failure`
- [ ] `test_check_requirement_completeness_returns_valid_structure`
- [ ] `test_validation_tools_error_handling`

**验收标准**:
- [ ] 测试文件已创建
- [ ] 所有测试用例通过
- [ ] LLM mock 正确实现

---

### T-301: 运行测试验证覆盖率

**操作步骤**:
```bash
# 进入 MCP Server 目录
cd skill-creator-mcp

# 运行完整测试套件并生成覆盖率报告
uv run pytest --cov --cov-report=term-missing

# 检查覆盖率是否 ≥95%
```

**验收标准**:
- [ ] 所有测试通过
- [ ] 测试覆盖率 ≥95%
- [ ] 无新的测试失败

---

### T-302: 更新文档

**更新文件**:
1. `ISSUES.md` - 关闭 ISSUE-001/002/003
2. `CHANGELOG.md` - 添加 v0.3.4 条目

**CHANGELOG 条目**:
```markdown
## [0.3.4] - 2026-01-28

### Added
- 为需求收集原子工具补充单元测试（37个测试用例）

### Fixed
- 归档项目审核报告，清理计划目录

### Test
- 测试覆盖率恢复到 95%+
```

**验收标准**:
- [ ] ISSUES.md 已更新
- [ ] CHANGELOG.md 已更新
- [ ] 无过时引用

---

## 四、关键文件清单

### 需要归档
- `.claude/plans/generic-seeking-toast.md` - 916行审核报告

### 需要创建（单元测试）
- `skill-creator-mcp/tests/test_tools/test_requirement_session_tools.py`
- `skill-creator-mcp/tests/test_tools/test_requirement_question_tools.py`
- `skill-creator-mcp/tests/test_tools/test_requirement_validation_tools.py`

### 需要更新
- `ISSUES.md`
- `CHANGELOG.md`

### 参考文件（测试模式）
- `skill-creator-mcp/tests/test_tools/test_init_skill.py` (9098行)
- `skill-creator-mcp/tests/test_tools/test_validate_skill.py`
- `skill-creator-mcp/tests/test_integration/test_e2e_workflow.py`

### 被测试文件
- `skill-creator-mcp/src/skill_creator_mcp/tools/requirement_session_tools.py` (227行)
- `skill-creator-mcp/src/skill_creator_mcp/tools/requirement_question_tools.py` (279行)
- `skill-creator-mcp/src/skill_creator_mcp/tools/requirement_validation_tools.py` (206行)

---

## 五、风险评估与缓解

### 风险1: 测试编写耗时超预期

**概率**: 中
**影响**: 中
**缓解措施**:
- 参考现有测试模式，减少设计时间
- 分批实现，先完成会话管理工具测试
- 如果时间不足，优先完成P2任务

### 风险2: Mock LLM调用复杂度高

**概率**: 低
**影响**: 中
**缓解措施**:
- 使用 `unittest.mock.AsyncMock`
- 参考现有 LLM mock 实现
- 预留1小时处理Mock问题

### 风险3: 测试覆盖率可能未达标

**概率**: 低
**影响**: 低
**缓解措施**:
- 当前覆盖率95%，目标≥95%
- 如果未达标，补充边界情况测试
- 必要时接受95%的覆盖率（符合规范）

---

## 六、验收标准

### 总体验收

- [ ] **P2任务全部完成**: 审核报告已归档，3个单元测试文件已创建
- [ ] **所有测试通过**: pytest 无失败
- [ ] **覆盖率达标**: ≥95%
- [ ] **文档已更新**: ISSUES.md 和 CHANGELOG.md

### 分项验收

| 任务 | 验收标准 |
|------|----------|
| T-201 | 文件归档到 archive/，commit 已创建 |
| T-202 | 12个测试用例，全部通过 |
| T-203 | 13个测试用例，全部通过 |
| T-204 | 12个测试用例，全部通过 |
| T-301 | pytest --cov 通过，覆盖率≥95% |
| T-302 | ISSUES.md 和 CHANGELOG.md 已更新 |

---

## 七、进度追踪

### 当前状态
- **状态**: planning
- **开始时间**: 待定
- **任务完成**: 0/6 (0%)
- **最近更新**: 2026-01-28

### 状态流转

```
planning → in_progress → partially_completed → completed → archived
```

### 归档检查清单

- [ ] P2任务全部完成 (4/4)
- [ ] P3任务全部完成 (2/2)
- [ ] 所有验收标准满足
- [ ] 代码已通过测试验证
- [ ] Git commit 已创建
- [ ] 进度报告已生成

---

## 八、相关文档

**前置计划**:
- [magical-kindling-raccoon.md](archive/magical-kindling-raccoon.md) - 架构边界彻底重构（已归档）

**规范文档**:
- [CLAUDE.md](../CLAUDE.md) - 项目开发指南
- [docs/adr/001-hybrid-architecture.md](../docs/adr/001-hybrid-architecture.md) - 混合架构决策

**计划模板**:
- [.templates/plan-template.md](.templates/plan-template.md) - 计划模板

---

## 九、变更历史

| 日期 | 变更内容 | 变更人 |
|------|----------|--------|
| 2026-01-28 | 计划创建 | Claude |

---

**计划版本**: v1.0
**最后更新**: 2026-01-28
