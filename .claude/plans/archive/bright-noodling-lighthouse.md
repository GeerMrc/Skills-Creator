# MCP Server 代码质量与文档一致性全面修复计划

> **计划类型**: 代码质量修复与文档同步
> **创建日期**: 2026-01-29
> **状态**: planning
> **审核原则**: 100%基于实际代码审核（严禁虚假审核）

---

## 一、执行摘要

### 1.1 问题背景

在审核已归档的 `2026-01-28-mcp-audit-rustling-prancing-rabin.md` 计划时，发现了**严重的虚假审核问题**：

| 指标 | 已归档计划声称 | 实际代码情况 | 差距 |
|------|---------------|-------------|------|
| 测试数量 | 601个 | **613个** | +12 |
| 测试覆盖率 | 96% | **95%** | -1% |
| Ruff错误 | 0个 | **18个** | +18 |
| MyPy错误 | 0个 | **7个** | +7 |

### 1.2 根本原因分析

**违反开发规范**：
- ❌ **违反九步法步骤5**：未执行交叉验证，未基于实际代码审核
- ❌ **违反禁止虚假审核规定**（CLAUDE.md 2.5节）：仅依赖文档/commit摘要
- ❌ **文档未与代码同步**：测试数量增加后未更新文档

### 1.3 计划目标

**P0目标**（必须完成）：
1. 修复所有代码质量问题（25个静态分析错误）
2. 同步所有文档与实际代码
3. 验证所有测试与最新实现一致

**P1目标**（应该完成）：
1. 更新示例代码为新的7个原子工具
2. 清理过时的引用文档

---

## 二、实际代码审核结果（基于实际运行）

### 2.1 测试统计（实际运行）

```bash
uv run pytest --cov
========================= 613 passed, 2 skipped in 6.58s ========================
TOTAL coverage: 2201 lines, 95%
```

**实际数据**：
- 测试总数：**615个**（pytest --collect-only）
- 通过：**613个**
- 跳过：**2个**
- 覆盖率：**95%**

### 2.2 代码质量检查（实际运行）

**Ruff检查**（18个错误）：
```
11  E402  [ ] module-import-not-at-top-of-file
3   W293  [*] blank-line-with-whitespace
2   F401  [*] unused-import
1   I001  [*] unsorted-imports
1   UP035 [*] deprecated-import
```

**MyPy检查**（7个错误）：
```
src/skill_creator_mcp/server.py:32: error: Function is missing a return type annotation
src/skill_creator_mcp/server.py:49: error: Argument "cache" to "AppContext" has incompatible type
src/skill_creator_mcp/server.py:204: error: Function is missing a return type annotation
src/skill_creator_mcp/server.py:255: error: Function is missing a return type annotation
src/skill_creator_mcp/server.py:288: error: Argument 1 to "add_middleware" has incompatible type
src/skill_creator_mcp/server.py:294: error: Argument 1 has incompatible type
src/skill_creator_mcp/server.py:313: error: Argument 1 has incompatible type
```

### 2.3 文档一致性检查

**不一致项**：
1. README.md 第5行：`601 passed` → 应为 `613 passed`
2. README.md 第6行：`coverage-96%` → 应为 `coverage-95%`
3. CLAUDE.md：多处测试数量引用需要更新
4. 12个文件仍包含旧的 `collect_requirements` 引用（有警告但未更新代码）

---

## 三、核心定位与开发规范概述

### 3.1 项目核心定位（必读）

**Skills-Creator** 项目的核心定位是：

**"为用户提出的需求进行 Agent-Skills 技能开发（高效/规范/最佳实践标准化开发）"**

这是项目的唯一目标定位。

### 3.2 开发流程九步法（概要）

```
步骤0: 前置任务审核  → 检查前置任务、确认Git环境
步骤1: 制定开发计划  → .claude/plans/feat-xxx.md
步骤2: 拆分任务清单  → TodoWrite 工具 (3-10个任务)
步骤3: 执行开发工作  → 编码 + 测试
步骤4: 测试验证      → pytest --cov
步骤5: 交叉验证      → 对照计划检查（**禁止跳过**）
步骤6: 更新文档      → CHANGELOG.md
步骤7: 阶段性审计    → 内部审查
步骤8: Git提交       → 版本控制
步骤9: 阶段性汇报    → 生成汇报并归档计划
```

### 3.3 禁止行为（CLAUDE.md 第二章）

| 禁止行为 | 后果 |
|----------|------|
| ❌ 虚假审核 | 计划被拒绝或恢复 |
| ❌ 基于文档审核（不审核实际代码） | 技术债务 |
| ❌ 跳过步骤5交叉验证 | 遗漏问题 |
| ❌ 归档前未验证任务状态 | 计划不完整 |

---

## 四、修复方案（分阶段）

### Phase 1: 代码质量修复（P0 - 必须完成）

#### 任务1.1: 修复Ruff错误（18个）

**可自动修复**（7个）：
```bash
uv run ruff check . --fix
```

**手动修复**（11个E402错误）：
位置：`server.py` 中11个模块导入不在顶部

**修复方法**：重构导入顺序，将所有导入移到文件顶部

#### 任务1.2: 修复MyPy错误（7个）

**问题**：3个函数缺少返回类型注解 + 4个类型不兼容

**修复方法**：
1. 为缺少返回类型的函数添加 `-> None` 或适当的返回类型
2. 修复中间件类型兼容性问题（可能需要 FastMCP SDK 更新或类型忽略）

**验收标准**：
```bash
uv run ruff check .  # 必须 0 错误
uv run mypy src/     # 必须 0 错误
```

#### 任务1.3: 验证测试覆盖率

**当前状态**：95%（615个测试）

**行动**：保持当前覆盖率，不需要强制提升到96%

**验收标准**：
```bash
uv run pytest --cov  # 通过率 100%，覆盖率 ≥95%
```

---

### Phase 2: 文档同步更新（P0 - 必须完成）

#### 任务2.1: 更新测试数量

**受影响文件**：
1. `skill-creator-mcp/README.md` 第5行
   ```markdown
   # Before
   [![Tests](https://img.shields.io/badge/tests-601%20passed-success)(#)

   # After
   [![Tests](https://img.shields.io/badge/tests-613%20passed-success)(#)
   ```

2. `skill-creator-mcp/README.md` 第6行
   ```markdown
   # Before
   [![Coverage](https://img.shields.io/badge/coverage-96%25-brightgreen](#)

   # After
   [![Coverage](https://img.shields.io/badge/coverage-95%25-brightgreen](#)
   ```

3. `CLAUDE.md` 中所有测试数量引用

4. 根目录 `README.md` 中所有测试数量引用

#### 任务2.2: 更新覆盖率数据

将所有 `96%` 覆盖率引用更新为 `95%`

#### 任务2.3: 验证版本号一致性

确认所有文档版本号与 `pyproject.toml` 一致（v0.3.3）

**验收标准**：
- [ ] README.md 测试数量 = 613
- [ ] README.md 覆盖率 = 95%
- [ ] CLAUDE.md 测试数量 = 613
- [ ] 所有文档版本号 = v0.3.3

---

### Phase 3: 示例代码更新（P1 - 应该完成）

#### 任务3.1: 更新核心示例文件（5个）

**目标文件**：
1. `examples/example-elicit-mode.md`
2. `examples/requirement-collection-brainstorm.md`
3. `examples/example-progressive-mode.md`
4. `examples/example-basic-mode.md`
5. `examples/example-complete-mode.md`

**更新内容**：将旧的 `collect_requirements` 调用更新为7个原子工具调用

**示例**：
```python
# Before
await collect_requirements(ctx=ctx, action="start", mode="basic")

# After
await create_requirement_session(mode="basic")
```

#### 任务3.2: 更新参考文档（7个）

**目标文件**：
1. `references/requirement-collection-basics.md`
2. `references/requirement-collection-modes.md`
3. `references/requirement-collection-api-examples.md`
4. `references/requirement-workflow.md`
5. `references/brainstorming-techniques.md`
6. `references/troubleshooting.md`
7. `references/troubleshooting-advanced.md`

**更新策略**：
- 保留概念说明部分
- 更新代码示例为新的7个原子工具调用
- 移除或更新"架构更新警告"（因为示例已更新）

---

## 五、任务清单（TODO）

### P0 - 必须完成（阻塞性）

| ID | 任务 | 依赖 | 状态 | Commit |
|----|------|------|------|--------|
| T-101 | 修复Ruff错误（18个） | - | completed | ec1d3fc |
| T-102 | 修复MyPy错误（7个） | - | completed | ec1d3fc |
| T-103 | 更新README测试数量 | - | completed | 0960beb |
| T-104 | 更新CLAUDE.md测试数据 | - | completed | 0960beb |
| T-105 | 更新覆盖率数据（96%→95%） | - | completed | 0960beb |
| T-106 | 验证所有测试通过 | T-101, T-102 | completed | - |

### P1 - 应该完成（重要）

| ID | 任务 | 依赖 | 状态 | Commit |
|----|------|------|------|--------|
| T-201 | 更新核心示例文件（5个） | - | completed | 55b4789 |
| T-202 | 更新参考文档（7个） | - | completed | 55b4789 |
| T-203 | 验证示例代码可运行 | T-201 | completed | 55b4789 |

---

## 六、进度追踪

### 当前状态
- **状态**: completed
- **开始时间**: 2026-01-29
- **完成时间**: 2026-01-29
- **任务完成**: 9/9 (100%)
- **P0完成**: 6/6 (100%)
- **P1完成**: 3/3 (100%)

### 最近更新
- 2026-01-29: 所有任务完成
  - P0：修复所有Ruff和MyPy错误（25个）
  - P0：同步所有文档测试数据
  - P0：验证所有测试通过（613 passed, 95% coverage）
  - P1：更新示例代码为新的7个原子工具
  - P1：更新7个参考文档，移除架构警告
  - P1：验证示例代码可运行

---

## 七、验收标准

### 7.1 功能验收
- [x] 所有工具功能正常
- [x] 测试覆盖率≥95%
- [x] ruff 0错误
- [x] mypy 0错误

### 7.2 质量验收
- [x] 工具数量保持18个
- [x] 文档一致性100%
- [x] 代码质量达标
- [x] 无过时引用（已更新所有参考文档）

### 7.3 文档验收
- [x] README.md 测试数量 = 613
- [x] README.md 覆盖率 = 95%
- [x] CLAUDE.md 测试数量 = 613
- [x] 所有版本号 = v0.3.3

### 7.4 归档检查清单
- [x] P0任务全部完成
- [x] P1任务全部完成（或用户同意跳过）
- [x] 所有验收标准满足
- [x] 有完整的Git commit记录
- [x] 100%基于实际代码审核

---

## 八、风险与缓解措施

| 风险 | 影响 | 概率 | 缓解措施 |
|------|------|------|---------|
| MyPy类型错误修复困难 | 中 | 低 | 添加类型忽略注释（作为最后手段） |
| 文档更新遗漏 | 低 | 中 | 交叉检查，逐一验证 |
| 示例代码更新量大 | 低 | 低 | 分阶段更新，优先核心示例 |

---

## 九、开发规范要点

### 9.1 禁止虚假审核（强制）

**定义**：
- 仅依赖文档或commit摘要进行审核
- 不运行实际代码进行验证
- 声称的数据与实际不符

**后果**：
- 计划被恢复
- 技术债务累积
- 项目信誉受损

### 9.2 交叉验证要求（步骤5）

**必须执行的验证**：
1. 读取实际代码文件
2. 运行测试验证
3. 运行代码质量检查
4. 对比验收标准

**禁止行为**：
- ❌ 跳过交叉验证
- ❌ 仅检查文档
- ❌ 仅查看commit摘要

---

## 十、参考文档

### 项目文档
- `CLAUDE.md`: 项目开发规范（第二章：开发流程九步法）
- `ARCHITECTURE_AUDIT_REPORT_v2.md`: 架构审计报告
- `ROADMAP.md`: 项目发展规划

### 审核报告
- 本次审核基于3个并行Explore agents
- 100%基于实际代码运行结果
- 不依赖任何文档或commit摘要作为事实依据

---

**计划负责人**: Claude (GLM-4.7)
**最后更新**: 2026-01-29
**计划版本**: 1.0

---

## 修订记录

| 版本 | 日期 | 变更原因 | 主要变更 |
|------|------|---------|---------|
| 1.0 | 2026-01-29 | 初版 | 基于实际代码审核发现虚假审核问题，制定修复计划 |
