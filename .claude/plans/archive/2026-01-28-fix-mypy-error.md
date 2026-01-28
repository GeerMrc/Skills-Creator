# mypy错误与代码重复问题修复计划

**计划类型**: 修复/重构
**创建日期**: 2026-01-28
**优先级**: P0（代码质量问题）
**计划状态**: completed
**基于**: 审核后发现的mypy错误

---

## 一、问题背景

### 1.1 发现的问题

**TD-015: mypy类型检查错误**
```
src/skill_creator_mcp/server.py:393: error: Too many arguments for "check_requirement_completeness"  [call-arg]
```

**根本原因**：
- `requirement_validation_tools.py` 中定义了 `check_requirement_completeness(ctx, answers)` - 2个参数
- `llm_services.py` 中也定义了同名函数 `check_requirement_completeness(ctx, answers, prompt_template=None)` - 3个参数
- `server.py` 从 `requirement_validation_tools` 导入并调用，传递了3个参数
- 导致mypy类型检查失败

**代码重复问题**：
- 两个函数实现了完全相同的功能（检查需求完整性）
- Prompt模板在两个地方都硬编码了
- 违反DRY原则

### 1.2 用户要求

- 全面审核，立即修复所有已发现问题
- 不留"后续建议"，逐一修复/完善
- 严格遵循规范开发流程九步法

---

## 二、执行任务清单

### 任务列表

| 任务ID | 任务名称 | 优先级 | 预计时间 | 状态 | Commit |
|--------|----------|--------|----------|------|--------|
| T-201 | 修复函数重复定义问题 | P0 | 30分钟 | pending | - |
| T-202 | 统一Prompt模板引用 | P0 | 20分钟 | pending | - |
| T-203 | 运行完整测试验证 | P0 | 10分钟 | pending | - |
| T-204 | 全面代码审核 | P1 | 1小时 | pending | - |

---

## 三、详细实施方案

### T-201: 修复函数重复定义问题 (P0)

**问题**: 两个 `check_requirement_completeness` 函数

**修复方案**:
1. 删除 `requirement_validation_tools.py` 中的函数定义
2. 从 `llm_services` 导入并使用
3. 更新 `server.py` 中的导入语句

**需要修改的文件**:
- `tools/requirement_validation_tools.py` - 删除函数，从llm_services导入
- `server.py` - 更新导入语句

---

### T-202: 统一Prompt模板引用 (P0)

**问题**: Prompt模板在两个地方硬编码

**修复方案**:
- 确保所有Prompt都通过 `prompt_template` 参数传入
- 默认Prompt在llm_services中定义
- 文档引用 `prompt-templates.md`

---

### T-203: 运行完整测试验证 (P0)

```bash
uv run pytest --cov
uv run ruff check .
uv run mypy src/
```

---

### T-204: 全面代码审核 (P1)

审核重点:
1. 检查是否有其他重复代码
2. 检查是否有其他硬编码Prompt
3. 检查是否有其他类型安全问题
4. 检查是否符合ADR 001架构原则

---

## 四、执行进度

**当前状态**: planning
**开始时间**: 2026-01-28
**最后更新**: 2026-01-28

**任务完成情况**:
- P0: 0/3 (0%) ⏸️
- P1: 0/1 (0%) ⏸️

**总体进度**: 0/4 (0%)

---

## 五、归档检查清单

- [ ] **P0任务**
  - [ ] T-201: 修复函数重复定义
  - [ ] T-202: 统一Prompt模板引用
  - [ ] T-203: 运行完整测试验证

- [ ] **P1任务**
  - [ ] T-204: 全面代码审核

- [ ] **验收标准**
  - [ ] mypy检查通过（0错误）
  - [ ] 所有测试通过
  - [ ] 无重复代码
  - [ ] Prompt外部化完整

---

## 六、相关计划

### 前置计划
- [`.claude/plans/archive/2026-01-28-fix-documentation-inconsistencies.md`](.claude/plans/archive/2026-01-28-fix-documentation-inconsistencies.md) - 文档不一致修复计划（已完成）

### 相关技术债务
- TD-015: mypy类型检查错误（本次计划解决）

---

**计划状态**: planning → in_progress
**下一步**: 开始执行T-201（修复函数重复定义）
