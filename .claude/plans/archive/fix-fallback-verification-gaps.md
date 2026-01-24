# 修复回退功能测试覆盖缺陷计划

> **创建日期**: 2026-01-23
> **状态**: planning
> **优先级**: P0
> **类型**: 测试补充/代码修复

---

## 一、背景与问题概述

### 1.1 审核发现

根据《回退功能完整性审核报告》，发现以下关键问题：

| 问题 | 严重程度 | 影响 |
|------|----------|------|
| **capability_detection.py 0% 测试覆盖** | **高** | **关键回退逻辑未验证** |
| **仅 Mock 测试，无真实异常测试** | **高** | **无法验证真实行为** |
| 异常返回格式不一致 | 中 | Progressive 返回 success:False，Brainstorm 返回 success:True |
| 缺少集成测试 | 中 | 端到端回退场景未验证 |

### 1.2 影响范围

**核心回退模块** - `utils/capability_detection.py`:
- `check_sampling_capability()` - 检测 LLM sampling 支持
- `check_elicitation_capability()` - 检测用户交互支持
- `get_client_capabilities()` - 综合能力检测

**回退逻辑函数** - `server.py`:
- `_check_requirement_completeness()` - 完整性检查回退
- `_generate_brainstorm_question()` - Brainstorm 模式回退
- `_generate_progressive_question()` - Progressive 模式回退

---

## 二、目标

### 2.1 主要目标

1. **补充 capability_detection.py 单元测试** (P0)
   - 达到 80%+ 测试覆盖率
   - 覆盖所有正常和异常分支
   - 验证正确的错误消息格式

2. **添加真实异常场景集成测试** (P0)
   - 测试真实 ctx.sample() 失败时的回退行为
   - 测试真实 ctx.elicit() 失败时的处理
   - 验证 collect_requirements 的能力检测流程

3. **统一异常返回格式** (P1)
   - 统一 Progressive 和 Brainstorm 的异常处理
   - 确保所有回退路径返回一致的响应结构

4. **补充文档** (P1)
   - 更新 SKILL.md 说明回退机制
   - 添加故障排除指南

### 2.2 成功标准

| 验收标准 | 说明 |
|---------|------|
| capability_detection.py 测试覆盖 ≥80% | 当前 0% |
| 集成测试覆盖真实异常场景 | 当前仅 Mock 测试 |
| 异常返回格式统一 | Progressive 和 Brainstorm 一致 |
| 总体测试覆盖率保持 ≥85% | 当前 85% |
| 所有测试通过 | 0 失败 |

---

## 三、技术依赖

### 3.1 现有代码

- `skill-creator-mcp/src/skill_creator_mcp/utils/capability_detection.py` - 待测试模块
- `skill-creator-mcp/src/skill_creator_mcp/server.py` - 回退逻辑实现
- `skill-creator-mcp/tests/test_tools/test_phase0_validation.py` - 现有 Mock 测试

### 3.2 测试框架

- pytest - 测试运行器
- pytest-asyncio - 异步测试支持
- unittest.mock - Mock 对象（用于单元测试）
- pytest-cov - 覆盖率报告

---

## 四、任务清单

### Phase 1: capability_detection.py 单元测试 (P0)

- [ ] 1.1 创建测试文件
  - [ ] `tests/test_utils/test_capability_detection.py`
  - [ ] 导入所有待测试函数

- [ ] 1.2 实现 check_sampling_capability 测试
  - [ ] test_sampling_supported - Mock 成功响应
  - [ ] test_sampling_unsupported_not_declared - 客户端未声明能力
  - [ ] test_sampling_unsupported_error - 其他异常
  - [ ] test_sampling_unexpected_error - 未知错误

- [ ] 1.3 实现 check_elicitation_capability 测试
  - [ ] test_elicitation_supported - Mock 成功响应
  - [ ] test_elicitation_unsupported_method_not_found - 方法不存在
  - [ ] test_elicitation_unsupported_error - 其他异常
  - [ ] test_elicitation_unexpected_error - 未知错误

- [ ] 1.4 实现 get_client_capabilities 测试
  - [ ] test_both_supported - 两者都支持
  - [ ] test_both_unsupported - 两者都不支持
  - [ ] test_only_sampling_supported - 仅 sampling 支持
  - [ ] test_only_elicitation_supported - 仅 elicitation 支持
  - [ ] test_summary_advanced_apis_supported - 正确计算 summary
  - [ ] test_summary_fallback_required - 正确设置 fallback_required

- [ ] 1.5 验证测试覆盖
  - [ ] 运行 `pytest tests/test_utils/test_capability_detection.py --cov`
  - [ ] 确认 coverage ≥80%
  - [ ] 检查未覆盖的代码行

### Phase 2: 真实异常场景集成测试 (P0)

- [ ] 2.1 创建集成测试文件
  - [ ] `tests/test_integration/test_fallback_scenarios.py`
  - [ ] 设置测试夹具和 Mock 环境

- [ ] 2.2 实现 collect_requirements 回退场景测试
  - [ ] test_collect_requirements_with_elicit_unsupported - elicitation 不可用时的行为
  - [ ] test_collect_requirements_fallback_to_traditional - 降级到传统模式
  - [ ] test_collect_requirements_brainstorm_fallback - brainstorm 模式回退
  - [ ] test_collect_requirements_progressive_fallback - progressive 模式回退
  - [ ] test_collect_requirements_completeness_fallback - 完整性检查回退

- [ ] 2.3 实现端到端回退流程测试
  - [ ] test_e2e_fallback_workflow_basic - basic 模式完整流程（无 LLM）
  - [ ] test_e2e_fallback_workflow_complete - complete 模式完整流程（无 LLM）
  - [ ] test_e2e_fallback_with_session_recovery - 会话中断恢复（回退模式）

### Phase 3: 统一异常返回格式 (P1)

- [ ] 3.1 分析当前不一致性
  - [ ] 检查 `_generate_progressive_question` 异常返回
  - [ ] 检查 `_generate_brainstorm_question` 异常返回
  - [ ] 文档化差异

- [ ] 3.2 统一异常处理
  - [ ] 修改 `_generate_progressive_question` 异常返回为 success:True
  - [ ] 确保所有回退返回包含 `source: "fallback"`
  - [ ] 添加 `error` 字段说明原始异常

- [ ] 3.3 更新相关测试
  - [ ] 更新 test_generate_progressive_question_fallback
  - [ ] 添加新测试验证统一格式

### Phase 4: 文档更新 (P1)

- [ ] 4.1 更新 SKILL.md
  - [ ] 添加"回退机制"章节
  - [ ] 说明当前客户端限制
  - [ ] 提供故障排除指南

- [ ] 4.2 更新示例文档
  - [ ] 更新 requirement-collection-basic.md
  - [ ] 添加回退场景示例

- [ ] 4.3 更新 CHANGELOG.md
  - [ ] 记录测试改进
  - [ ] 记录异常处理统一

### Phase 5: 验证与合并 (P0)

- [ ] 5.1 运行完整测试套件
  - [ ] `pytest --cov` - 全部测试通过
  - [ ] 确认覆盖率 ≥85%
  - [ ] capability_detection.py 覆盖率 ≥80%

- [ ] 5.2 代码质量检查
  - [ ] `ruff check .` - 0 错误
  - [ ] `mypy src/` - 0 错误

- [ ] 5.3 创建提交
  - [ ] 提交测试代码
  - [ ] 提交修复代码
  - [ ] 提交文档更新

- [ ] 5.4 合并到 develop
  - [ ] 创建 Pull Request
  - [ ] Code Review
  - [ ] 合并

---

## 五、执行计划

### 5.1 执行顺序

```
┌─────────────────────────────────────────────────────────────────┐
│                        执行流程图                                │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  Phase 1: capability_detection.py 单元测试 (1-2天)               │
│    ├─ 创建测试文件                                              │
│    ├─ 实现 17+ 个测试用例                                       │
│    └─ 验证 80%+ 覆盖率                                          │
│                          ↓                                      │
│  Phase 2: 真实异常场景集成测试 (1-2天)                           │
│    ├─ 创建集成测试文件                                          │
│    ├─ 实现回退场景测试                                          │
│    └─ 实现端到端流程测试                                        │
│                          ↓                                      │
│  Phase 3: 统一异常返回格式 (0.5天)                              │
│    ├─ 分析不一致性                                              │
│    ├─ 修改代码                                                  │
│    └─ 更新测试                                                  │
│                          ↓                                      │
│  Phase 4: 文档更新 (0.5天)                                      │
│    ├─ 更新 SKILL.md                                             │
│    ├─ 更新示例文档                                              │
│    └─ 更新 CHANGELOG.md                                         │
│                          ↓                                      │
│  Phase 5: 验证与合并 (0.5天)                                    │
│    ├─ 运行完整测试套件                                          │
│    ├─ 代码质量检查                                              │
│    └─ 合并到 develop                                            │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### 5.2 时间估算

| Phase | 预估时间 | 说明 |
|-------|----------|------|
| Phase 1: 单元测试 | 1-2 天 | 17+ 测试用例 |
| Phase 2: 集成测试 | 1-2 天 | 8+ 测试用例 |
| Phase 3: 代码修复 | 0.5 天 | 异常格式统一 |
| Phase 4: 文档更新 | 0.5 天 | 3-4 个文档 |
| Phase 5: 验证合并 | 0.5 天 | 测试 + PR |
| **总计** | **3.5-5.5 天** | 含测试验证 |

---

## 六、验收标准

### 6.1 必须满足 (P0)

- [x] capability_detection.py 测试覆盖率 ≥80%
- [ ] 集成测试覆盖真实异常场景
- [ ] 所有测试通过 (369+ 新增测试)
- [ ] 代码质量检查 0 错误
- [ ] 分支已合并到 develop

### 6.2 建议满足 (P1)

- [ ] 异常返回格式已统一
- [ ] 文档已更新
- [ ] 总体测试覆盖率保持 ≥85%

---

## 七、参考资料

- [审核报告](./archive/phase-0-validation-fix-2026-01-23.md)
- [Phase 0 验证结果](./phase-0-verification-results.md)
- [项目开发规范](../CLAUDE.md)

---

**计划状态**: 待执行
**创建人**: Claude Code
**下一步**: Phase 1.1 - 创建测试文件
