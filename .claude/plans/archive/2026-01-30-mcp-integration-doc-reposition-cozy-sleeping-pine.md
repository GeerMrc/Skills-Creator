# MCP 集成文档定位重构计划

## 计划概述

**计划编号**: cozy-sleeping-pine
**创建时间**: 2026-01-30
**状态**: completed
**目标**: 重新定位 `skill-creator/references/` 中 MCP 集成文档，明确"示范案例"定位，添加"扩展方法指南"，让用户能够参考核心示范为自己的 Agent-Skills 集成其他 MCP

---

## 背景分析

### 核心定位（重申）

> **Skills-Creator 核心定位**：为用户进行 Agent-Skills 高效/规范/最佳实践标准化开发

### 用户反馈

> "当前我们只专注于核心功能的一种示范，并给出用户扩展的建议方式方法指导才是合理的引导，不同的 Agent-Skills 功能需求，都会要使用到不同的 MCP 扩展加入"

### 当前问题

1. `mcp-github-integration.md` 和 `mcp-thinking-integration.md` 定位不清晰
   - 标题使用"集成指南"，容易被误解为通用教程
   - 缺少明确的"示范案例"定位说明
   - 用户不清楚如何参考这些示范集成其他 MCP

2. 缺少"如何为 Agent-Skill 集成其他 MCP 的通用方法指导"
   - 用户只有两个具体示范（GitHub、Thinking）
   - 没有通用的扩展方法论
   - 不知道如何为自己的 Agent-Skills 选择和集成合适的 MCP

3. 文档组织结构可以优化
   - references/README.md 的"MCP 集成"章节分类不够清晰
   - SKILL.md 缺少 MCP 集成相关的说明章节

---

## 分析结论

### 结论1：现有文档应该保留但需重新定位

| 文档 | 当前定位 | 新定位 | 变更内容 |
|------|----------|--------|----------|
| `mcp-github-integration.md` | "集成指南"（模糊） | "示范案例"（明确） | 添加开头定位说明，调整标题 |
| `mcp-thinking-integration.md` | "集成指南"（模糊） | "示范案例"（明确） | 添加开头定位说明，调整标题 |

**保留理由**：
- 这些文档展示了**如何将外部 MCP 集成到 Agent-Skills 开发工作流中的最佳实践**
- 提供了需求跟踪、Git 自动化、思考记录等**核心示范**
- 符合"专注核心功能的一种示范"的定位

### 结论2：需要创建扩展方法指南

**新文档**：`references/mcp-integration-guide.md`

**内容范围**：
- MCP 集成的通用方法论（决策树、评估标准）
- 如何为自己的 Agent-Skill 选择合适的 MCP
- 如何参考示范实现其他 MCP 的集成
- 集成最佳实践和常见模式
- FAQ：常见问题解答

**目标用户**：需要为自己的 Agent-Skills 集成 MCP 的开发者

### 结论3：需要添加通用集成示例

**新示例**：`examples/mcp-integration-example.md`

**内容范围**：
- 展示如何为 Agent-Skill 集成一个常见的 MCP（如 Web Search）
- 完整的配置、使用、测试流程
- 可作为其他 MCP 集成的模板

---

## 实施方案

### Phase 1: 文档重构（P0 - 必须完成）

#### 任务1：重新定位 GitHub MCP 集成文档

**文件**: `skill-creator/references/mcp-github-integration.md`

**变更内容**：
1. 标题修改：`# GitHub MCP 集成示范`
2. 添加开头定位说明：

```markdown
> **文档定位**：本文档是 GitHub MCP 与 Agent-Skills 集成的**示范案例**，展示如何将外部 MCP 集成到 Agent-Skills 开发工作流中。
>
> **适用场景**：当你的 Agent-Skill 需要 Git 自动化、需求跟踪、PR 管理等功能时，可参考本示范实现 GitHub MCP 集成。
>
> **扩展指南**：要集成其他 MCP（如 FileSystem、Database、Web Search），请参考 [MCP 集成扩展指南](mcp-integration-guide.md)。
>
> **相关示例**：[GitHub 需求跟踪示例](../examples/github-requirement-tracking.md) | [Git 自动化示例](../examples/github-automation.md)
```

3. 调整章节结构，突出"示范"性质

**验收标准**：
- 文档标题明确为"示范"而非"指南"
- 开头定位说明清晰
- 交叉引用到扩展指南
- 文档行数不超过推荐值（~200-250行）

---

#### 任务2：重新定位 Thinking MCP 集成文档

**文件**: `skill-creator/references/mcp-thinking-integration.md`

**变更内容**：
1. 标题修改：`# Thinking MCP 集成示范`
2. 添加开头定位说明（同上，替换 Thinking 相关内容）
3. 调整章节结构，突出"示范"性质

**验收标准**：同任务1

---

#### 任务3：创建 MCP 集成扩展指南

**文件**: `skill-creator/references/mcp-integration-guide.md`（新建）

**章节结构**：

```markdown
# MCP 集成扩展指南

> **文档定位**：本文档提供为 Agent-Skills 集成外部 MCP 的**通用方法论和最佳实践**。

## 概述

### 什么是 MCP 集成？

### 为什么需要 MCP 集成？

### Skill-Creator 的示范案例

## 集成决策框架

### 决策树：我的 Agent-Skill 需要集成哪些 MCP？

### MCP 评估标准

### 常见 MCP 功能对照表

## 五步集成方法论

### Step 1: 需求分析 - 确定需要哪些能力

### Step 2: MCP 选择 - 评估和选择合适的 MCP

### Step 3: 配置声明 - 在 SKILL.md 中声明 MCP

### Step 4: 工作流集成 - 在 Agent-Skill 中调用 MCP 工具

### Step 5: 测试验证 - 验证集成是否正常工作

## 集成模式库

### 模式1: 数据获取模式（如 Web Search）

### 模式2: 数据存储模式（如 Database）

### 模式3: 任务自动化模式（如 GitHub）

### 模式4: 思考记录模式（如 Thinking）

## 参考示范详解

### GitHub MCP 集成示范解析

### Thinking MCP 集成示范解析

## 最佳实践

### 渐进式集成原则

### 错误处理和降级

### Token 优化策略

## FAQ

**Q1: 如果用户没有安装某个 MCP，我的 Agent-Skill 还能工作吗？**

**Q2: 如何声明 MCP 为可选依赖？**

**Q3: 集成多个 MCP 会导致性能问题吗？**

**Q4: 如何测试 MCP 集成？**

**Q5: 我创建的 MCP 集成示范可以贡献给 Skill-Creator 吗？**

## 参考资料

- [GitHub MCP 集成示范](mcp-github-integration.md)
- [Thinking MCP 集成示范](mcp-thinking-integration.md)
- [MCP 工具参考](mcp-tools-reference.md)
- [examples/](../examples/) - 更多集成示例
```

**估算行数**: ~300-350行

**验收标准**：
- 五步集成方法论清晰可执行
- 决策树能够帮助用户判断是否需要集成 MCP
- FAQ 覆盖常见问题
- 交叉引用链接全部有效
- 文档行数在推荐范围内（~300-350行）

---

### Phase 2: 文档组织更新（P1 - 推荐完成）

#### 任务4：更新 SKILL.md 添加 MCP 集成说明

**文件**: `skill-creator/SKILL.md`

**变更内容**：在"详细文档"章节后添加新章节

```markdown
## MCP 集成说明

Skill-Creator 支持与外部 MCP Server 集成，为 Agent-Skills 开发提供增强能力。

### 集成示范

Skill-Creator 提供两个核心 MCP 集成示范：

- **[GitHub MCP 集成示范](references/mcp-github-integration.md)** - 需求跟踪、Git 自动化、PR 管理
- **[Thinking MCP 集成示范](references/mcp-thinking-integration.md)** - 思考记录、决策追溯、知识传递

### 扩展指南

要为自己的 Agent-Skill 集成其他 MCP（如 FileSystem、Database、Web Search），请参考：

- **[MCP 集成扩展指南](references/mcp-integration-guide.md)** - 通用方法论、决策框架、五步集成流程

### 配置方法

在 SKILL.md 的 frontmatter 中声明需要集成的 MCP：

```yaml
---
mcp_servers: ["skill-creator", "GitHub", "Thinking"]
---
```

> **注意**：`skill-creator` MCP 是必需的，其他 MCP（如 GitHub、Thinking）是可选增强。

> 详见：[MCP 集成扩展指南](references/mcp-integration-guide.md)
```

**插入位置**：在"## 架构说明"章节之后，SKILL.md 末尾

**验收标准**：
- 新章节清晰说明 MCP 集成的定位（示范 vs 扩展指南）
- SKILL.md 行数仍然符合 ≤150行规范
- 交叉引用链接有效

---

#### 任务5：重构 references/README.md 文档分类

**文件**: `skill-creator/references/README.md`

**变更内容**：重构"MCP 集成"章节

```markdown
### MCP 集成

**核心参考**：

| 文档 | 说明 | 定位 |
|------|------|------|
| **[MCP 工具参考](mcp-tools-reference.md)** | skill-creator MCP 的12个工具完整参考 | 核心参考 |
| **[MCP 集成扩展指南](mcp-integration-guide.md)** | 为 Agent-Skills 集成任何 MCP 的通用方法论 | 方法指南 |

**集成示范**：

| 文档 | 说明 | 用途 |
|------|------|------|
| **[GitHub MCP 集成示范](mcp-github-integration.md)** | GitHub MCP 集成最佳实践示范 | Git 自动化、需求跟踪 |
| **[Thinking MCP 集成示范](mcp-thinking-integration.md)** | Thinking MCP 集成最佳实践示范 | 思考记录、决策追溯 |

> **使用提示**：参考示范案例了解具体实现，使用扩展指南学习通用方法论。
```

**验收标准**：
- "核心参考"与"集成示范"分类清晰
- 添加"使用提示"说明两者关系
- 交叉引用链接有效

---

### Phase 3: 示例补充（P2 - 可选完成）

#### 任务6：创建通用 MCP 集成示例

**文件**: `skill-creator/examples/mcp-integration-example.md`（新建）

**内容大纲**：

```markdown
# Web Search MCP 集成示例

## 概述

本示例展示如何为 Agent-Skill 集成 Web Search MCP，实现网络搜索功能。

## 集成步骤

### Step 1: 配置声明

### Step 2: 工作流集成

### Step 3: 测试验证

## 完整示例代码

## 常见问题

## 扩展建议
```

**估算行数**: ~200-250行

**验收标准**：
- 展示完整的集成流程
- 代码可运行
- 可作为其他 MCP 集成的模板

---

#### 任务7：更新 examples/README.md

**文件**: `skill-creator/examples/README.md`

**变更内容**：添加"MCP 集成示例"分类

```markdown
### MCP 集成示例

| 示例 | 说明 |
|------|------|
| **[Web Search MCP 集成示例](mcp-integration-example.md)** | 通用 MCP 集成完整流程 |
| **[GitHub 需求跟踪示例](github-requirement-tracking.md)** | GitHub MCP 需求跟踪实现 |
| **[Git 自动化示例](github-automation.md)** | GitHub MCP Git 自动化实现 |
```

---

## 任务清单

| ID | 任务 | 优先级 | 状态 | 预估时间 | 关联文件 |
|----|------|--------|------|----------|----------|
| T-101 | 重新定位 GitHub MCP 集成文档 | P0 | completed | 20分钟 | `references/mcp-github-integration.md` |
| T-102 | 重新定位 Thinking MCP 集成文档 | P0 | completed | 20分钟 | `references/mcp-thinking-integration.md` |
| T-103 | 创建 MCP 集成扩展指南 | P0 | completed | 90分钟 | `references/mcp-integration-guide.md` |
| T-104 | 更新 SKILL.md 添加 MCP 集成说明 | P1 | completed | 30分钟 | `SKILL.md` |
| T-105 | 重构 references/README.md | P1 | completed | 20分钟 | `references/README.md` |
| T-106 | 创建通用 MCP 集成示例 | P2 | completed | 60分钟 | `examples/mcp-integration-example.md` |
| T-107 | 更新 examples/README.md | P2 | completed | 15分钟 | `examples/README.md` |

**任务完成进度**: 7/7 (100%)

---

## 验收标准

### 文档定位清晰

- ✅ 用户能够理解示范案例的目的（展示如何集成，而非通用教程）
- ✅ 用户能够理解扩展指南的用途（通用方法论）
- ✅ 文档标题和开头说明明确定位

### 用户能够扩展

- ✅ 参考示范为其他 Agent-Skill 集成 GitHub/Thinking
- ✅ 参考扩展指南为 Agent-Skill 集成其他 MCP
- ✅ 使用决策树判断是否需要集成 MCP

### 文档结构合理

- ✅ 符合渐进式披露原则（SKILL.md ≤ 150行）
- ✅ 引用文件不超过推荐行数（~300-350行）
- ✅ 交叉引用链接全部有效

### 质量检查

- ✅ 通过 ruff 格式检查
- ✅ 文档行数符合规范
- ✅ 没有无效引用链接

---

## 风险与注意事项

1. **SKILL.md 行数限制**: 添加 MCP 集成说明后需要确保不超过 150 行
   - **缓解措施**: 精简现有内容，或合并章节

2. **新文档行数控制**: `mcp-integration-guide.md` 需要控制在 300-350 行
   - **缓解措施**: 使用渐进式披露，详细内容放引用文件

3. **交叉引用链接**: 所有新增引用链接需要验证有效
   - **缓解措施**: 实施后运行链接检查脚本

---

## 实施顺序

```
T-101, T-102 (并行) → T-103 → T-104, T-105 (并行) → T-106, T-107 (并行)
```

---

## 变更影响评估

### 影响范围

- **文档变更**: 7 个文件（2 个修改，2 个新建，3 个更新）
- **代码变更**: 无
- **测试变更**: 无

### 向后兼容性

- ✅ 完全兼容，仅为文档定位澄清和新增内容
- ✅ 不影响现有功能

---

## 相关文档

- **[CLAUDE.md](../../CLAUDE.md)** - 项目开发规范
- **[混合架构设计](references/architecture.md)** - MCP + Agent-Skill 混合架构
- **[ADR 001](../../docs/adr/001-hybrid-architecture.md)** - 混合架构设计决策

---

**计划创建时间**: 2026-01-30
**计划版本**: v1.0
**下一步**: 等待用户审批后开始实施
