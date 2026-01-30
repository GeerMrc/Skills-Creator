# skill-creator 全面审核与优化计划

**计划类型**: 重构/优化
**创建日期**: 2026-01-30
**优先级**: P0
**计划状态**: planning

---

## 一、问题背景

### 当前问题

基于项目核心定位**"为用户进行 Agent-Skills 高效/规范/最佳实践标准化开发"**，对 skill-creator/ Agent-Skill 进行全面审核发现以下问题：

### 审核发现

#### 严重问题（偏离核心定位）

1. **SKILL.md 混入外部 MCP 声明**
   - Line 24: `mcp_servers: ["skill-creator", "GitHub", "Thinking"]`
   - 影响：用户误认为 GitHub/Thinking 是必需组件

2. **SKILL.md 包含 MCP 集成章节**
   - Lines 123-136: "MCP 集成说明" 章节
   - 影响：占用 15% 核心内容，稀释定位

3. **4个示例文件偏离核心定位**（占示例总量30%）
   - `examples/mcp-github-integration-example.md` (170行)
   - `examples/mcp-thinking-integration-example.md` (240行)
   - `examples/github-integration.md` (353行)
   - `examples/packaging-examples.md` (374行，过长且含GitHub内容)

4. **引用文件偏离核心**
   - `references/mcp-integration-guide.md` (228行) - 通用 MCP 集成方法论

#### 中等问题（冗长重复）

1. **3个 reference 文件超过300行建议值**
   - `requirement-collection-guide.md` (300行)
   - `troubleshooting-advanced.md` (282行)
   - `validation-guide.md` (278行)

2. **SKILL.md 重复描述**
   - MCP 工具列表重复 3 次 (lines 67-86)
   - 打包规范链接重复 2 次

3. **examples/README.md 过于详细** (110行)

### 用户要求

1. 确保 skill-creator/ 100% 符合项目核心定位
2. 遵循 Agent-Skills 最佳实践（渐进式披露、职责分离、Token 优化）
3. 移除所有偏离核心定位的内容
4. 精简冗长文件至规范大小

---

## 二、改进/实施方案

### 2.1 方案概述

**核心原则**: 回归项目核心定位，100%聚焦于"Agent-Skills 标准化开发"

**优化目标**:
- P0: 核心定位修正（移除所有偏离核心的内容）
- P1: 内容精简优化（压缩至规范大小）
- P2: 结构优化（改进文档组织）

### 2.2 技术细节

#### SKILL.md 修改清单

| 行号 | 修改类型 | 修改内容 |
|------|----------|----------|
| 24 | 修改 | `mcp_servers: ["skill-creator"]` (移除GitHub/Thinking) |
| 45, 51 | 移除 | 指向 mcp-integration-guide.md 的引用 |
| 67-86 | 精简 | MCP 工具列表合并为简洁表格 |
| 123-136 | 删除 | "MCP 集成说明" 整个章节 |
| 新增 | 添加 | 外部 MCP 可选说明注释 |

#### 文件移除清单

| 文件路径 | 行数 | 移除原因 |
|----------|------|----------|
| `examples/mcp-github-integration-example.md` | 170 | 偏离核心（GitHub集成） |
| `examples/mcp-thinking-integration-example.md` | 240 | 偏离核心（Thinking集成） |
| `examples/github-integration.md` | 353 | 偏离核心（GitHub工作流） |
| `references/mcp-integration-guide.md` | 228 | 偏离核心（通用MCP方法论） |

#### 文件精简清单

| 文件路径 | 当前行数 | 目标行数 | 精简策略 |
|----------|----------|----------|----------|
| `requirement-collection-guide.md` | 300 | 250 | 移除冗余示例，合并重复章节 |
| `troubleshooting-advanced.md` | 282 | 250 | 移除边缘案例，保留常见问题 |
| `validation-guide.md` | 278 | 250 | 简化示例代码，合并等级说明 |
| `packaging-examples.md` | 374 | 200 | 移除GitHub集成示例，简化高级用法 |
| `examples/README.md` | 110 | 80 | 移除高级集成章节，简化表格 |

---

## 三、执行任务清单

### 任务列表

| 任务ID | 任务名称 | 优先级 | 预计时间 | 执行状态 | 完成时间 | Commit |
|--------|----------|--------|----------|----------|----------|--------|
| T-20260130-01 | 修改 SKILL.md 核心定位 | P0 | 15分钟 | pending | - | - |
| T-20260130-02 | 移除偏离核心的文件 | P0 | 20分钟 | pending | - | - |
| T-20260130-03 | 更新所有交叉引用 | P0 | 25分钟 | pending | - | - |
| T-20260130-04 | 精简过长 reference 文件 | P1 | 70分钟 | pending | - | - |
| T-20260130-05 | 重命名并精简 packaging 示例 | P1 | 45分钟 | pending | - | - |
| T-20260130-06 | 简化 examples/README.md | P1 | 15分钟 | pending | - | - |
| T-20260130-07 | 验证文档完整性和一致性 | P0 | 20分钟 | pending | - | - |

**状态说明**:
- `pending`: 待执行
- `in_progress`: 执行中（同时只能有一个）
- `completed`: 已完成

---

## 四、执行进度

**当前状态**: planning
**开始时间**: 2026-01-30
**最后更新**: 2026-01-30

**任务完成情况**:
- P0: 0/4 (0%) ⏸️
- P1: 0/3 (0%) ⏸️

**总体进度**: 0/7 (0%)

**最近更新**:
- [2026-01-30] 计划创建

---

## 五、归档检查清单

### 必须达成（全部完成才能归档）

- [ ] **P0任务**
  - [ ] T-20260130-01: 修改 SKILL.md 核心定位
  - [ ] T-20260130-02: 移除偏离核心的文件
  - [ ] T-20260130-03: 更新所有交叉引用
  - [ ] T-20260130-07: 验证文档完整性和一致性

- [ ] **P1任务**
  - [ ] T-20260130-04: 精简过长 reference 文件
  - [ ] T-20260130-05: 重命名并精简 packaging 示例
  - [ ] T-20260130-06: 简化 examples/README.md

- [ ] **验收标准**
  - [ ] SKILL.md ≤120行，无外部MCP声明
  - [ ] 4个偏离核心的文件已移除
  - [ ] 所有reference文件 ≤250行
  - [ ] 所有example文件 ≤200行
  - [ ] 无失效链接
  - [ ] 100%内容聚焦Agent-Skills开发

### 追溯记录

- [ ] 有完整的Git commit记录
- [ ] 有阶段性进度报告
- [ ] 未完成任务已处理

---

## 六、验收标准

### P0验收标准（必须100%达成）

1. **SKILL.md核心定位验证**
   - [ ] frontmatter中不包含GitHub、Thinking外部MCP声明
   - [ ] 内容中不包含"MCP集成说明"章节
   - [ ] 所有MCP工具列表仅出现一次
   - [ ] SKILL.md总行数 ≤120行

2. **文件移除验证**
   - [ ] 4个偏离核心的example文件已移除
   - [ ] mcp-integration-guide.md已移除
   - [ ] examples/目录剩余17个文件
   - [ ] references/目录剩余15个文件

3. **引用完整性验证**
   - [ ] 所有指向已移除文件的链接已更新
   - [ ] SKILL.md中无失效链接
   - [ ] grep搜索无失效链接

4. **核心定位验证**
   - [ ] 100%内容聚焦于Agent-Skills开发
   - [ ] 外部MCP仅作为可选项存在
   - [ ] 无通用MCP方法论内容

### P1验收标准（建议100%达成）

1. **文件大小验证**
   - [ ] requirement-collection-guide.md ≤250行
   - [ ] troubleshooting-advanced.md ≤250行
   - [ ] validation-guide.md ≤250行
   - [ ] packaging.md ≤200行
   - [ ] examples/README.md ≤80行

2. **内容质量验证**
   - [ ] 无重复描述
   - [ ] 核心信息保留完整
   - [ ] 渐进式披露效果改善

### 质量指标目标

| 指标 | 当前值 | 目标值 | 改善 |
|------|--------|--------|------|
| SKILL.md行数 | 137 | ≤120 | -12% |
| 核心定位偏离文件数 | 5 | 0 | -100% |
| 超过300行的reference文件 | 3 | 0 | -100% |
| 超过200行的example文件 | 2 | 0 | -100% |
| 重复描述次数 | 3 | 0 | -100% |

---

## 七、相关文件路径

### 需要修改的文件

**SKILL.md** (137→120行)
- Line 24: 修改 mcp_servers
- Lines 45, 51: 移除引用
- Lines 67-86: 精简工具列表
- Lines 123-136: 删除章节

**examples/README.md** (110→80行)
- 移除"高级集成示例"章节
- 更新"打包与GitHub集成"章节
- 更新快速查找表格

**references/README.md**
- 移除 mcp-integration-guide 引用

### 需要移除的文件

- `skill-creator/examples/mcp-github-integration-example.md`
- `skill-creator/examples/mcp-thinking-integration-example.md`
- `skill-creator/examples/github-integration.md`
- `skill-creator/references/mcp-integration-guide.md`

### 需要精简的文件

- `skill-creator/references/requirement-collection-guide.md` (300→250行)
- `skill-creator/references/troubleshooting-advanced.md` (282→250行)
- `skill-creator/references/validation-guide.md` (278→250行)
- `skill-creator/examples/packaging-examples.md` → `packaging.md` (374→200行)

---

## 八、关键规范变更对照

| 变更项 | 旧规范 | 新规范 |
|--------|--------|--------|
| SKILL.md mcp_servers | ["skill-creator", "GitHub", "Thinking"] | ["skill-creator"] |
| SKILL.md 行数 | 137行 | ≤120行 |
| 外部MCP集成 | 混入核心内容 | 独立文档或移除 |
| reference 文件行数 | 最长300行 | ≤250行 |
| example 文件行数 | 最长374行 | ≤200行 |

---

## 九、风险与注意事项

### 风险

- **移除GitHub/Thinking内容影响现有用户**: 中等影响，低概率
- **精简导致信息丢失**: 中等影响，中概率
- **破坏现有引用链接**: 高影响，中概率

### 缓解措施

- 备份所有移除的文件到 /tmp/ 目录
- 在 CHANGELOG.md 中记录移除原因和迁移指南
- 严格测试所有交叉引用链接
- 保留核心信息，通过渐进式披露到引用文件

---

## 十、相关计划

### 前置计划
无

### 后续计划
无（待确定）

---

## 附录：详细任务说明

### T-20260130-01: 修改 SKILL.md 核心定位

**目标**: 修改SKILL.md frontmatter和内容，移除外部MCP声明和章节

**具体步骤**:
1. 修改frontmatter第24行:
   ```yaml
   # 修改前
   mcp_servers: ["skill-creator", "GitHub", "Thinking"]
   # 修改后
   mcp_servers: ["skill-creator"]
   ```

2. 删除lines 123-136 "MCP集成说明"章节

3. 精简lines 67-86 MCP工具列表，合并为简洁表格

4. 添加说明注释:
   ```markdown
   > **注意**: Skill-Creator 专注于 Agent-Skills 开发核心功能。外部 MCP（如 GitHub、Thinking）集成属于可选的高级用法。
   ```

5. 移除指向mcp-integration-guide.md的引用 (lines 45, 51)

**验证标准**:
- SKILL.md总行数 ≤120行
- frontmatter中无GitHub、Thinking
- 内容中无"MCP集成说明"章节

### T-20260130-02: 移除偏离核心的文件

**目标**: 移除4个偏离核心定位的example文件和1个reference文件

**具体步骤**:
1. 创建备份目录
2. 移除文件
3. 验证结果

**验证标准**:
- examples/剩余17个文件
- references/剩余15个文件

### T-20260130-03: 更新所有交叉引用

**目标**: 更新所有指向已移除文件的链接

**具体步骤**:
1. 搜索所有失效链接
2. 更新SKILL.md、examples/README.md、references/README.md
3. 验证无失效链接

### T-20260130-04: 精简过长 reference 文件

**目标**: 将3个超过300行的reference文件精简至≤250行

### T-20260130-05: 重命名并精简 packaging 示例

**目标**: 将packaging-examples.md重命名并精简至200行

### T-20260130-06: 简化 examples/README.md

**目标**: 将examples/README.md从110行简化至80行

### T-20260130-07: 验证文档完整性和一致性

**目标**: 全面验证所有修改的文档完整性和一致性

---

**计划状态**: planning → in_progress
**下一步**: 等待用户批准后开始执行
