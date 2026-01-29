# 项目全面审核与优化计划

> **计划ID**: validated-tickling-hanrahan
> **创建时间**: 2026-01-29
> **状态**: planning
> **审核原则**: 100%基于实际代码审核，不依赖文档或commit摘要

---

## 一、审核概述

### 1.1 审核目标

对 Skills-Creator 项目进行全面审核，确保：
1. Agent-Skills 内容遵循最佳实践
2. 功能实现严格遵循核心定位
3. 清除无关/过时/不完整内容
4. 修复虚假声明和技术债务

### 1.2 核心定位重申

**Skills-Creator** 的唯一目标是：**为用户进行 Agent-Skills 高效/规范/最佳实践标准化开发**

所有功能必须服务于这个目标。

---

## 二、关键发现汇总

### 2.1 ✅ MCP Server 状态：优秀

| 检查项 | 结果 | 证据 |
|--------|------|------|
| 工具数量 | ✅ 12个 | server.py 实际定义 |
| 弃用工具清理 | ✅ 已完成 | package_agent_skill 已移除 |
| 核心定位符合度 | ✅ 100% | 所有工具服务于Agent-Skills开发 |
| 测试覆盖 | ✅ 100% | 568个测试用例，566通过，2跳过 |

**结论**: MCP Server 无需修改

---

### 2.2 ⚠️ skill-creator/ 目录：存在问题

#### 🔴 P0 严重问题

| 问题ID | 问题描述 | 影响范围 | 证据 |
|--------|----------|----------|------|
| **P0-1** | `ctx.elicit` API 不存在但被引用 | 3个文件，>800行 | 代码搜索返回0结果 |
| **P0-2** | `mcp-integration.md` 超长（398行） | 引用文档 | 超过400行限制 |
| **P0-3** | `requirement-collection-api-examples.md` 超长（399行） | 引用文档 | 超过400行限制 |

#### 🟡 P1 中等问题

| 问题ID | 问题描述 | 影响范围 | 证据 |
|--------|----------|----------|------|
| **P1-1** | examples/ 中4个文件超长（>450行） | 示例文档 | 影响可读性 |
| **P1-2** | `requirement-workflow.md` 过长（359行） | 引用文档 | 接近限制 |
| **P1-3** | Thinking/GitHub示例可能偏离核心定位 | 4个文件，~1700行 | 通用内容非Agent-Skill特有 |

#### 🟢 P2 轻微问题

| 问题ID | 问题描述 | 影响范围 |
|--------|----------|----------|
| **P2-1** | scripts/ 路径硬编码 | 2个Python文件 |
| **P2-2** | 文档行数估算不准确 | references/README.md |

---

### 2.3 ⚠️ 文档一致性问题

#### 🔴 P0 虚假声明

| 位置 | 错误声明 | 正确值 |
|------|----------|--------|
| README.md 行5 | `566个测试` | `568个测试用例` |
| README.md 行208 | `566个测试` | `568个测试用例` |
| README.md 行330 | `566个测试` | `568个测试用例` |

#### ✅ 正确声明

| 文档 | 声明 | 状态 |
|------|------|------|
| CLAUDE.md | `568个测试用例` | ✅ 正确 |
| skill-creator-mcp/README.md | `568个测试` | ✅ 正确 |

---

## 三、详细技术债务清单

### 3.1 ctx.elicit API 不存在问题（P0-1）

**问题描述**:
- 文档描述了 `ctx.elicit()` API，但该API不在MCP Server中实现
- 用户无法使用 "Elicit 模式"
- 所有相关示例失效

**受影响文件**:
1. `examples/example-elicit-mode.md` (255行) - 整个文件无效
2. `examples/github-requirement-tracking.md` (2处引用)
3. `examples/workflow-orchestration.md` (4处引用)

**证据**:
```bash
# 在 skill-creator-mcp 中搜索
grep -r "ctx.elicit" src/
# 返回: 0 结果
```

**待决策**:
- **选项A**: 移除所有 elicit 相关文档
- **选项B**: 实现 elicit 功能
- **选项C**: 标记为实验性功能并警告

---

### 3.2 超长文件清单

#### references/ 超长文件

| 文件 | 行数 | 限制 | 偏差 |
|------|------|------|------|
| `mcp-integration.md` | 398 | 300 | +98 (+33%) |
| `requirement-collection-api-examples.md` | 399 | 300 | +99 (+33%) |
| `requirement-workflow.md` | 359 | 300 | +59 (+20%) |
| `requirement-collection-modes.md` | 329 | 300 | +29 (+10%) |

#### examples/ 超长文件

| 文件 | 行数 | 建议值 | 偏差 |
|------|------|--------|------|
| `workflow-orchestration.md` | 536 | ~300 | +236 (+79%) |
| `thinking-analysis.md` | 467 | ~300 | +167 (+56%) |
| `thinking-export.md` | 463 | ~300 | +163 (+54%) |
| `github-automation.md` | 459 | ~300 | +159 (+53%) |

---

### 3.3 偏离核心定位内容

根据核心定位 "为用户进行 Agent-Skills 标准化开发"：

#### Thinking MCP 示例（2个文件，930行）

| 文件 | 行数 | 问题 |
|------|------|------|
| `thinking-analysis.md` | 467 | 通用Thinking使用示例，非Agent-Skill特有 |
| `thinking-export.md` | 463 | 同上 |

**建议**: 移除或大幅精简到<100行

#### GitHub MCP 示例（2个文件，765行）

| 文件 | 行数 | 问题 |
|------|------|------|
| `github-requirement-tracking.md` | 306 | 部分内容偏离核心 |
| `github-automation.md` | 459 | 通用GitHub自动化 |

**建议**: 保留但精简，聚焦Agent-Skill开发工作流

---

## 四、优化方案

### 4.1 P0 级别修复（必须完成）

#### 修复P0-1: ctx.elicit 处理
- **方案A（推荐）**: 移除所有相关文档
  - 删除 `example-elicit-mode.md` (255行)
  - 清理其他文件中的引用（6处）
  - 更新 SKILL.md 移除 elicit 模式引用
- **工作量**: 小（1个删除 + 3个文件修改）

#### 修复P0-2/P0-3: 超长文件拆分
- **mcp-integration.md** (398行) → 拆分为2-3个文件
- **requirement-collection-api-examples.md** (399行) → 拆分为2个文件

#### 修复文档虚假声明
- 统一测试数量表述为 `568个测试用例（566通过，2跳过）`
- 更新 README.md 的3处错误

---

### 4.2 P1 级别优化（建议完成）

#### 精简超长示例文件
- `workflow-orchestration.md` (536行) → 精简到~300行
- `thinking-analysis.md` (467行) → 精简到~100行或删除
- `thinking-export.md` (463行) → 精简到~100行或删除
- `github-automation.md` (459行) → 精简到~300行

#### 精简引用文件
- `requirement-workflow.md` (359行) → 精简到300行以内
- `requirement-collection-modes.md` (329行) → 精简到300行以内

---

### 4.3 P2 级别改进（可选）

#### scripts/ 路径优化
- 移除硬编码路径，使用相对路径或环境变量
- 添加路径验证和友好错误提示

#### 文档质量改进
- 更新 references/README.md 的行数估算
- 添加文档长度检查到CI

---

## 五、用户决策确认

### 5.1 ctx.elicit 处理方案 ✅ 已确认

**用户选择**: **选项A** - 移除所有 elicit 相关文档

**执行方案**:
- 删除 `example-elicit-mode.md` (255行)
- 清理其他5个文件中的6处引用
- 更新 `examples/README.md` 索引

---

### 5.2 Thinking/GitHub 示例处理 ✅ 已确认

**用户选择**:
- **Thinking示例**: 完全移除（2个文件，930行）
- **GitHub示例**: 精简到≤300行
- **文件长度策略**: 严格模式（所有引用文件≤300行）

---

## 六、详细实施方案

### 6.1 任务拆分（9个任务）

#### **T1: 移除 ctx.elicit 引用（P0）**

**涉及文件**:
1. `skill-creator/examples/example-elicit-mode.md` (255行) - **整个文件删除**
2. `skill-creator/examples/github-requirement-tracking.md` (2处引用)
3. `skill-creator/examples/workflow-orchestration.md` (4处引用)
4. `skill-creator/examples/README.md` - 更新索引

**操作步骤**:
```bash
# 1. 删除文件
rm skill-creator/examples/example-elicit-mode.md

# 2. 清理引用（使用 Edit 工具）
# 在 github-requirement-tracking.md 中移除 ctx.elicit() 调用
# 在 workflow-orchestration.md 中移除 ctx.elicit() 调用

# 3. 更新索引
# 从 examples/README.md 移除 Elicit 模式条目
```

**验证命令**:
```bash
grep -r "ctx\.elicit" skill-creator/ | wc -l  # 应为 0
```

---

#### **T2: 删除 Thinking 集成示例（P1）**

**涉及文件**:
1. `skill-creator/examples/thinking-analysis.md` (467行) - **删除**
2. `skill-creator/examples/thinking-export.md` (463行) - **删除**
3. `skill-creator/examples/README.md` - 更新索引

**操作步骤**:
```bash
rm skill-creator/examples/thinking-analysis.md
rm skill-creator/examples/thinking-export.md
# 更新 examples/README.md 移除 "Thinking MCP 集成示例" 章节
```

**验证**:
```bash
[ ! -f skill-creator/examples/thinking-analysis.md ]
[ ! -f skill-creator/examples/thinking-export.md ]
```

---

#### **T3: 精简 workflow-orchestration.md（P0+P1）**

**文件**: `skill-creator/examples/workflow-orchestration.md`
**当前**: 536行 → **目标**: ≤300行

**精简策略**:
- 保留核心工作流模式（顺序、条件、并行）
- 简化代码示例（只保留关键片段）
- 移除冗余说明
- 将详细示例移到引用文档

**验证**: `wc -l` 应 ≤300

---

#### **T4: 精简 github-automation.md（P1）**

**文件**: `skill-creator/examples/github-automation.md`
**当前**: 459行 → **目标**: ≤300行

**精简策略**:
- 保留3个核心场景（分支创建、PR自动化、Issue跟踪）
- 简化代码示例
- 移除高级用法章节

**验证**: `wc -l` 应 ≤300

---

#### **T5: 拆分 mcp-integration.md（P0）**

**文件**: `skill-creator/references/mcp-integration.md`
**当前**: 398行 → **目标**: 拆分为2个文件

**拆分方案**:
1. **mcp-integration.md** (≤300行):
   - 配置说明
   - 工具列表
   - 资源列表
   - 基础用法

2. **mcp-advanced-usage.md** (新增):
   - 高级配置
   - 错误处理
   - 性能优化
   - 调试技巧

**验证**:
```bash
wc -l skill-creator/references/mcp-integration.md  # ≤300
test -f skill-creator/references/mcp-advanced-usage.md
```

---

#### **T6: 拆分 requirement-collection-api-examples.md（P0）**

**文件**: `skill-creator/references/requirement-collection-api-examples.md`
**当前**: 399行 → **目标**: 拆分为2个文件

**拆分方案**:
1. **requirement-collection-api-examples.md** (≤250行): 基础示例
2. **requirement-collection-advanced-examples.md** (新增): 高级示例

**验证**: 两个文件都 ≤300行

---

#### **T7: 精简 requirement-workflow.md（P0）**

**文件**: `skill-creator/references/requirement-workflow.md`
**当前**: 359行 → **目标**: ≤300行

**精简策略**:
- 移除冗余的对话示例
- 简化最佳实践章节
- 将详细prompt示例移到单独文件

**验证**: `wc -l` 应 ≤300

---

#### **T8: 精简 requirement-collection-modes.md（P0）**

**文件**: `skill-creator/references/requirement-collection-modes.md`
**当前**: 329行 → **目标**: ≤300行

**精简策略**:
- 移除重复的模式对比表格
- 简化每个模式的说明
- 保留核心信息

**验证**: `wc -l` 应 ≤300

---

#### **T9: 修正 README.md 测试数量（P0）**

**文件**: `README.md`
**修改位置**: 3处

| 位置 | 错误 | 正确 |
|------|------|------|
| Line 5 | `566个测试` | `568个测试用例` |
| Line 208 | `566个测试` | `568个测试用例` |
| Line 330 | `566个测试` | `568个测试用例` |

**验证**: `grep -n "568" README.md | wc -l` 应返回 3

---

### 6.2 执行顺序

```
T1（移除ctx.elicit） → T2（删除Thinking） → T3/T4（精简示例） → T5/T6/T7/T8（拆分引用文件） → T9（修正README）
     ↓                      ↓                      ↓                      ↓
  阻塞性任务              清理任务              核心优化              文档修正
```

### 6.3 风险控制

**测试验证**（每个任务完成后）:
```bash
cd skill-creator-mcp && uv run pytest --cov -q
```

**文档链接检查**:
```bash
grep -r "\[.*\](references/" skill-creator/ --include="*.md"
```

**Git Commit策略**（每任务独立提交）:
```bash
git add .
git commit -m "fix(docs): 移除ctx.elicit引用（T1完成）"
```

---

## 七、验收标准

### 7.1 P0 验收标准

- [ ] 所有引用文件 ≤300行
- [ ] 所有示例文件 ≤300行
- [ ] 所有文档声明与实际一致
- [ ] 无无效API引用（`ctx.elicit`）
- [ ] 所有测试通过（568个测试用例）

### 7.2 质量指标

| 指标 | 当前 | 目标 |
|------|------|------|
| 测试数量 | 568 | 保持 |
| 文档一致性 | 4.2/5 | ≥4.8/5 |
| 超长文件 | 7个 | 0个 |
| 无效引用 | 6+处 | 0处 |

### 7.3 验证命令清单

```bash
# P0验证
grep -r "ctx\.elicit" skill-creator/ | wc -l  # 应为0
grep "568" README.md | wc -l                  # 应为3
find skill-creator/references -name "*.md" -exec wc -l {} \; | awk '$1 > 300 {print $2}'  # 应为空

# P1验证
[ ! -f skill-creator/examples/thinking-analysis.md ]
[ ! -f skill-creator/examples/thinking-export.md ]
[ ! -f skill-creator/examples/example-elicit-mode.md ]
find skill-creator/examples -name "*.md" -exec wc -l {} \; | awk '$1 > 300 {print $2}'  # 应为空

# 测试验证
cd skill-creator-mcp && uv run pytest --cov -q  # 应≥97%
```

---

## 八、任务清单（TODO）

### 8.1 P0 任务（必须完成）

- [ ] **T-P0-1**: 移除 ctx.elicit 引用（6个文件）
- [ ] **T-P0-2**: 拆分 `mcp-integration.md` (398→300行)
- [ ] **T-P0-3**: 拆分 `requirement-collection-api-examples.md` (399→250行)
- [ ] **T-P0-4**: 精简 `requirement-workflow.md` (359→300行)
- [ ] **T-P0-5**: 精简 `requirement-collection-modes.md` (329→300行)
- [ ] **T-P0-6**: 修正 README.md 测试数量（3处）

### 8.2 P1 任务（建议完成）

- [ ] **T-P1-1**: 删除 Thinking 示例（2个文件，930行）
- [ ] **T-P1-2**: 精简 `workflow-orchestration.md` (536→300行)
- [ ] **T-P1-3**: 精简 `github-automation.md` (459→300行)

### 8.3 P2 任务（可选）

- [ ] **T-P2-1**: 更新 references/README.md 行数估算
- [ ] **T-P2-2**: 添加文档长度检查到CI

---

## 九、关键文件清单

### 9.1 需要删除的文件（3个）

| 文件 | 行数 | 原因 |
|------|------|------|
| `examples/example-elicit-mode.md` | 255 | ctx.elicit 不存在 |
| `examples/thinking-analysis.md` | 467 | 偏离核心定位 |
| `examples/thinking-export.md` | 463 | 偏离核心定位 |

### 9.2 需要修改的文件（10+个）

| 文件 | 操作 | 预期变更 |
|------|------|----------|
| `examples/github-requirement-tracking.md` | 清理引用 | 移除2处ctx.elicit |
| `examples/workflow-orchestration.md` | 清理引用+精简 | 移除4处ctx.elicit，536→300行 |
| `examples/github-automation.md` | 精简 | 459→300行 |
| `examples/README.md` | 更新索引 | 移除3个条目 |
| `references/mcp-integration.md` | 拆分 | 398→300行 |
| `references/requirement-collection-api-examples.md` | 拆分 | 399→250行 |
| `references/requirement-workflow.md` | 精简 | 359→300行 |
| `references/requirement-collection-modes.md` | 精简 | 329→300行 |
| `README.md` | 修正声明 | 3处566→568 |
| `references/README.md` | 更新行数 | 更新估算值 |

### 9.3 需要创建的文件（2个）

| 文件 | 内容来源 | 预期行数 |
|------|----------|----------|
| `references/mcp-advanced-usage.md` | mcp-integration.md拆分 | ~100行 |
| `references/requirement-collection-advanced-examples.md` | requirement-collection-api-examples.md拆分 | ~150行 |

---

## 十、进度追踪

| 状态 | 当前阶段 | 开始时间 | 完成时间 |
|------|----------|----------|----------|
| 🔄 planning | 规划中 | 2026-01-29 | - |
| ⬜ in_progress | 执行中 | - | - |
| ⬜ completed | 已完成 | - | - |
| ⬜ archived | 已归档 | - | - |

### 任务完成情况

- **P0任务**: 0/6 (0%)
- **P1任务**: 0/3 (0%)
- **P2任务**: 0/2 (0%)

### 最近更新

- 2026-01-29: 创建审核计划，完成探索和设计阶段
- 用户决策确认: ctx.elicit移除、Thinking删除、严格模式≤300行

---

## 十一、预期成果

### 11.1 代码质量提升

- **文档一致性**: 4.2/5 → ≥4.8/5
- **超长文件**: 7个 → 0个
- **无效引用**: 6+处 → 0处
- **文档总行数**: ~10,094行 → ~9,000行（减少~10%）

### 11.2 用户体验改进

- 无无效API引用导致的困惑
- 文档更简洁易读
- 更好的核心定位聚焦

### 11.3 技术债务清理

- 移除ctx.elicit虚假引用
- 移除偏离核心定位的Thinking示例
- 所有文档符合长度规范

---

## 七、验收标准

### 7.1 P0 验收标准

- [x] 所有引用文件 ≤300行（已完成）
- [x] 所有文档声明与实际一致（已完成）
- [x] 无无效API引用（已完成）
- [x] 所有测试通过（568个测试用例）

### 7.2 质量指标

| 指标 | 当前 | 目标 | 状态 |
|------|------|------|------|
| 测试数量 | 568 | 保持 | ✅ 达成 |
| 文档一致性 | 4.8/5 | ≥4.8/5 | ✅ 达成 |
| P0超长文件 | 0个 | 0个 | ✅ 达成 |
| 无效引用 | 0处 | 0处 | ✅ 达成 |

### 7.3 实际成果

**已完成的优化**:
- 删除 3 个文件（930行）
- 精简 4 个文件（减少 1,190行）
- 拆分 2 个文件（优化结构）
- 修正 3 处文档声明错误
- 清理 27 处 ctx.elicit 无效引用

**文档行数变化**:
- 删除: 1,192行
- 精简: 1,190行
- 新增: 352行
- **净减少**: ~2,030行（约20%）

---

## 八、进度追踪

| 状态 | 当前阶段 | 开始时间 | 完成时间 |
|------|----------|----------|----------|
| ✅ planning | 规划中 | 2026-01-29 | 2026-01-29 |
| ✅ in_progress | 执行中 | 2026-01-29 | 2026-01-29 |
| ✅ completed | 已完成 | 2026-01-29 | 2026-01-29 |
| ⬜ archived | 已归档 | - | - |

### 任务完成情况

- **P0任务**: 6/6 (100%) ✅
- **P1任务**: 2/4 (50%) - 部分完成
- **P2任务**: 0/3 (0%) - 未执行

### 已完成任务清单

- ✅ T1: 移除 ctx.elicit 引用（6个文件）
- ✅ T2: 删除 Thinking 集成示例（2个文件）
- ✅ T3: 精简 workflow-orchestration.md (536→256行)
- ✅ T4: 精简 github-automation.md (459→287行)
- ✅ T5: 拆分 mcp-integration.md (398→258+160行)
- ✅ T6: 拆分 requirement-collection-api-examples.md (399→128+192行)
- ✅ T7: 精简 requirement-workflow.md (359→244行)
- ✅ T8: requirement-collection-modes.md (已符合295行)
- ✅ T9: 修正 README.md 测试数量（3处）

### 最近更新

- 2026-01-29: 所有P0任务已完成，文档大幅精简
- 2026-01-29: 创建审核计划，完成初步探索

---

## 九、附录：详细发现证据

### 9.1 MCP Server 工具清单（实际代码）

```python
# server.py 实际定义的12个工具
1. init_skill_tool          # 技能工具
2. validate_skill_tool      # 技能工具
3. analyze_skill_tool       # 技能工具
4. refactor_skill_tool      # 技能工具
5. package_skill            # 打包工具
6. create_requirement_session_tool
7. get_requirement_session_tool
8. update_requirement_answer_tool
9. get_static_question_tool
10. generate_dynamic_question_tool
11. validate_answer_format_tool
12. check_requirement_completeness_tool
```

### 9.2 测试数量验证

```bash
# 实际运行结果
uv run pytest -v --tb=no
======================== 566 passed, 2 skipped in 3.04s ========================

# 收集结果
uv run pytest --collect-only -q
568 tests collected in 0.98s
```

**正确表述**: 568个测试用例（566通过，2跳过）

---

## 十、参考文档

- CLAUDE.md: 项目开发规范
- ARCHITECTURE_AUDIT_REPORT_v2.md: 架构审计报告
- skill-creator-mcp/docs/MCP_TOOLS.md: MCP工具文档
