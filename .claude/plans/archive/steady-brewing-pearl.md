# 全面审核审计与优化计划

**计划类型**: 审核/优化
**创建日期**: 2026-01-28
**优先级**: P0/P1
**计划状态**: planning

---

## 一、审核背景

基于用户要求，对重构后的项目进行**100%基于实际代码**的全面审核审计：
1. 确保重构计划完整执行，旧代码清理干净
2. 审核代码与文档一致性
3. 独立审核 Agent-Skill 和 MCP Server 的最佳实践符合度
4. 审核 MCP 与 Agent-Skill 协同是否为最佳实践

---

## 二、审核发现摘要

### 2.1 MCP Server (skill-creator-mcp) 审核结果

| 维度 | 评分 | 发现 |
|------|------|------|
| 工具数量准确性 | 100% | 23个工具与文档一致 ✅ |
| 原子化实现 | 95% | 旧工具已清理，符合ADR 001 ✅ |
| Prompt外部化 | 60% | 支持自定义但默认Prompt仍在代码中 ⚠️ |
| 代码重复 | 90% | batch_operations.py可能与batch_tools.py重复 ⚠️ |
| 架构一致性 | 95% | 符合混合架构原则 ✅ |

**关键问题**：
- ⚠️ README.md 仍提及旧的 `collect_requirements` 工具
- ⚠️ Prompt 未完全外部化到文件
- ⚠️ 工具注册方式不一致（混用 `@mcp.tool()` 和 `add_tool()`）
- ⚠️ `batch_operations.py` 可能是旧版本需清理

### 2.2 Agent-Skill (skill-creator) 审核结果

| 维度 | 评分 | 发现 |
|------|------|------|
| 目录结构 | 100% | 符合最佳实践 ✅ |
| 引用文档 | 100% | 29个文档，核心文档齐全 ✅ |
| SKILL.md | 95% | 第148行工具数量错误（"18"应为"23"）⚠️ |
| 打包规范 | 100% | 排除规则正确 ✅ |

**关键问题**：
- ⚠️ SKILL.md 第148行："18 工具"应为 "23 工具"
- ⚠️ SKILL.md 第123行工具分类计算需更新

### 2.3 测试与文档一致性审核结果

| 维度 | 实际值 | 文档声明 | 状态 |
|------|--------|----------|------|
| 测试数量 | 594 | 594 (核心文档) | ✅ 一致 |
| 测试覆盖率 | 96% | 96% | ✅ 一致 |
| Git状态 | Clean | Clean | ✅ 正常 |

**发现的问题**：
- ⚠️ ISSUES.md 第426行："583个测试"应为 "594"
- ⚠️ 工具数量分类需要明确定义（23 Tools vs 20+4+3）

---

## 三、执行任务清单

### 任务列表

| 任务ID | 任务名称 | 优先级 | 预计时间 | 状态 | Commit |
|--------|----------|--------|----------|------|--------|
| T-A01 | 更新README.md移除旧工具引用 | P0 | 10分钟 | pending | - |
| T-A02 | 完全外部化Prompt到文件 | P1 | 1小时 | pending | - |
| T-A03 | 统一工具注册方式 | P2 | 30分钟 | pending | - |
| T-A04 | 验证并清理batch_operations.py | P1 | 20分钟 | pending | - |
| T-A05 | 更新SKILL.md工具数量 | P0 | 10分钟 | pending | - |
| T-A06 | 更新ISSUES.md测试数量 | P0 | 5分钟 | pending | - |
| T-A07 | 澄清工具数量分类定义 | P1 | 15分钟 | pending | - |
| T-A08 | 交叉验证MCP与Agent-Skill协同 | P0 | 30分钟 | pending | - |
| T-A09 | 运行完整测试套件验证 | P0 | 10分钟 | pending | - |
| T-A10 | 更新技术债务清单 | P2 | 10分钟 | pending | - |

**总预计时间**: ~3小时

---

## 四、详细实施方案

### T-A01: 更新README.md移除旧工具引用 (P0)

**问题**: `skill-creator-mcp/README.md` 仍提及旧的 `collect_requirements` 工具

**修复方案**:
1. 搜索所有对 `collect_requirements` 的引用
2. 替换为7个原子工具的说明
3. 更新工具分类表格

**验收标准**:
- [ ] 无残留 `collect_requirements` 引用
- [ ] 工具数量明确为23个
- [ ] 工具分类准确（会话管理3、问题获取2、验证2等）

---

### T-A02: 完全外部化Prompt到文件 (P1)

**当前状态**: 支持自定义Prompt但默认Prompt仍在代码中

**修复方案**:
1. 创建 `skill-creator-mcp/src/skill_creator_mcp/prompts/` 目录
2. 将以下Prompt外部化：
   - `requirement_completeness.txt` - 需求完整性检查
   - `brainstorm_question.txt` - 头脑风暴问题生成
   - `progressive_question.txt` - 渐进式问题生成
3. 更新工具从文件加载Prompt
4. 更新 `skill-creator/references/prompt-templates.md` 引用新文件

**验收标准**:
- [ ] Prompt文件创建在 `prompts/` 目录
- [ ] 工具从文件加载默认Prompt
- [ ] 保持向后兼容（支持参数覆盖）
- [ ] 所有测试通过

---

### T-A03: 统一工具注册方式 (P2)

**问题**: 混用 `@mcp.tool()` 装饰器和 `add_tool()` 方法

**修复方案**:
1. 将 `skill_tools.py` 中的4个工具改为使用 `@mcp.tool()` 装饰器
2. 删除 `mcp.add_tool()` 调用
3. 验证功能一致性

**验收标准**:
- [ ] 所有23个工具统一使用 `@mcp.tool()` 装饰器
- [ ] 所有测试通过
- [ ] 工具列表一致

---

### T-A04: 验证并清理batch_operations.py (P1)

**问题**: `batch_operations.py` 可能与 `batch_tools.py` 重复

**验证步骤**:
1. 对比两个文件的功能差异
2. 确认哪个是实际使用的版本
3. 删除未使用的旧文件
4. 更新导入引用

**验收标准**:
- [ ] 确认文件用途或安全删除
- [ ] 无重复代码
- [ ] 所有测试通过

---

### T-A05: 更新SKILL.md工具数量 (P0)

**问题**: SKILL.md 第148行声明 "18 工具" 应为 "23 工具"

**修复方案**:
1. 更新第148行：`MCP Server 提供原子操作（18 工具...）` → `23 工具...`
2. 更新第123行工具分类计算

**验收标准**:
- [ ] 工具数量准确为23个
- [ ] 工具分类计算正确

---

### T-A06: 更新ISSUES.md测试数量 (P0)

**问题**: ISSUES.md 第426行 "583个测试" 应为 "594"

**修复方案**:
1. 搜索所有 "583" 引用
2. 替换为 "594"

**验收标准**:
- [ ] 无残留 "583" 测试数量引用

---

### T-A07: 澄清工具数量分类定义 (P1)

**问题**: "23 Tools (8类)" 的分类需要明确定义

**修复方案**:
1. 在CLAUDE.md中明确定义工具分类标准
2. 统一文档中的描述方式
3. 澄清：23个工具 vs 20+4+3能力

**验收标准**:
- [ ] 分类标准明确
- [ ] 各文档描述一致

---

### T-A08: 交叉验证MCP与Agent-Skill协同 (P0)

**验证内容**:
1. MCP Server 只提供原子操作 ✅
2. Agent-Skill 负责工作流编排 ✅
3. Prompt模板管理是否符合ADR 001 ⚠️
4. 职责边界是否清晰 ✅

**验收标准**:
- [ ] 符合ADR 001架构原则
- [ ] 无职责混淆
- [ ] 协同流程清晰

---

### T-A09: 运行完整测试套件验证 (P0)

**验证命令**:
```bash
cd skill-creator-mcp
uv run pytest --cov
uv run ruff check .
uv run mypy src/
```

**验收标准**:
- [ ] 594个测试全部通过
- [ ] 覆盖率≥96%
- [ ] ruff 0错误
- [ ] mypy 0错误

---

### T-A10: 更新技术债务清单 (P2)

**更新内容**:
- Prompt外部化（本次修复）
- 文档不一致问题（本次修复）
- 工具注册方式统一（本次修复）

---

## 五、执行进度

**当前状态**: completed
**开始时间**: 2026-01-28
**最后更新**: 2026-01-28

**任务完成情况**:
- P0: 5/5 (100%) ✅
- P1: 3/3 (100%) ✅
- P2: 2/2 (100%) ✅

**总体进度**: 10/10 (100%) ✅

---

## 六、归档检查清单

### 必须达成（全部完成才能归档）

- [x] **P0任务**
  - [x] T-A01: 更新README.md移除旧工具引用
  - [x] T-A05: 更新SKILL.md工具数量
  - [x] T-A06: 更新ISSUES.md测试数量
  - [x] T-A08: 交叉验证MCP与Agent-Skill协同
  - [x] T-A09: 运行完整测试套件验证

- [x] **P1任务**
  - [x] T-A02: 完全外部化Prompt到文件
  - [x] T-A04: 验证并清理batch_operations.py
  - [x] T-A07: 澄清工具数量分类定义

- [x] **验收标准**
  - [x] 所有文档数据一致（测试594、覆盖率96%、工具23）
  - [x] Prompt完全外部化，符合ADR 001
  - [x] 无重复代码或旧功能残留
  - [x] MCP与Agent-Skill协同符合最佳实践
  - [x] 所有测试通过（594/594）

---

## 七、关键文件路径

### 需要修改的文件

**文档修复**:
- `skill-creator-mcp/README.md` - 移除旧工具引用
- `skill-creator/SKILL.md` (第148行) - 工具数量
- `ISSUES.md` (第426行) - 测试数量
- `CLAUDE.md` (第38行) - 工具分类定义

**代码修复**:
- `skill-creator-mcp/src/skill_creator_mcp/tools/skill_tools.py` - 统一注册方式
- `skill-creator-mcp/src/skill_creator_mcp/utils/requirement_collection/llm_services.py` - Prompt外部化
- `skill-creator-mcp/src/skill_creator_mcp/tools/requirement_question_tools.py` - Prompt外部化

### 需要创建的文件

- `skill-creator-mcp/src/skill_creator_mcp/prompts/requirement_completeness.txt`
- `skill-creator-mcp/src/skill_creator_mcp/prompts/brainstorm_question.txt`
- `skill-creator-mcp/src/skill_creator_mcp/prompts/progressive_question.txt`

### 需要验证/删除的文件

- `skill-creator-mcp/src/skill_creator_mcp/tools/batch_operations.py` - 验证是否需要

---

## 八、相关计划

### 前置计划
- [`.claude/plans/archive/magical-kindling-raccoon.md`](.claude/plans/archive/magical-kindling-raccoon.md) - 架构边界彻底重构计划
- [`.claude/plans/archive/2026-01-28-fix-documentation-inconsistencies.md`](.claude/plans/archive/2026-01-28-fix-documentation-inconsistencies.md) - 文档不一致修复计划

### 相关技术债务
- Prompt业务知识泄露（本次计划解决）
- 文档数据不一致（本次计划解决）
- 工具注册方式不一致（本次计划解决）

---

## 九、审核方法说明

本次审核严格遵循用户要求：
- ✅ 100%基于实际项目代码内容审核
- ✅ 不仅依据文档或commit摘要
- ✅ 使用3个探索代理并行分析不同维度
- ✅ 对比实际代码与文档声明的一致性

**探索代理分配**:
1. **ae0db20**: MCP Server架构状态（工具、原子化、Prompt、重复）
2. **ad03760**: Agent-Skill架构状态（目录、文档、SKILL.md、打包）
3. **a67dd09**: 测试与文档一致性（测试数量、覆盖率、Git追溯）

---

---

**计划状态**: completed → archived
**完成时间**: 2026-01-28
**Git提交**: 0afcfbb
**归档位置**: .claude/plans/archive/
