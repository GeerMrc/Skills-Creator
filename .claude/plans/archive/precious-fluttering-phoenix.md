# 架构合规性修复计划

> **计划ID**: precious-fluttering-phoenix
> **创建日期**: 2026-01-26
> **完成日期**: 2026-01-26
> **状态**: completed
> **优先级**: P0（阻塞）

---

## 一、问题概述

### 1.1 审核发现

基于实际代码审核，发现**46处违规交叉引用**：

| 违规类型 | 数量 | 文件数 | 严重性 |
|---------|------|--------|--------|
| Agent-Skill 引用 MCP 文档 | 8处 | 3个 | 🔴 严重 |
| Agent-Skill 包含 Claude Code 配置 | 16处 | 6个 | 🔴 严重 |
| Agent-Skill 引用 MCP 技术实现 | 12处 | 10个 | 🟠 中等 |
| MCP 反向引用 Agent-Skill | 8处 | 5个 | 🟠 中等 |
| 脚本直接导入 MCP 源码 | 2处 | 2个 | 🟡 低 |
| **总计** | **46处** | **20个** | - |

### 1.2 架构违规核心问题

1. **破坏单向依赖原则**: MCP → Agent-Skill 反向引用
2. **职责边界混乱**: Agent-Skill 包含 MCP 配置细节
3. **文档引用断链**: `claude-code-configuration.md` 不存在

---

## 二、修复方案

### 2.1 核心原则

- ✅ **单向依赖**: Agent-Skill 可以引用 MCP，MCP 不可引用 Agent-Skill
- ✅ **职责分离**:
  - Agent-Skill: 工作流编排、使用指南、最佳实践
  - MCP Server: 技术 API、工具定义、配置说明
- ✅ **无断开引用**: 所有链接目标必须存在

### 2.2 修复策略

| 问题 | 修复方案 |
|------|----------|
| Agent-Skill 引用 MCP 文档 | **保留**（符合单向依赖） |
| Agent-Skill 包含 Claude Code 配置 | **移除**（移到 MCP 文档或保留引用） |
| MCP 反向引用 Agent-Skill | **删除**（违反单向依赖） |
| 脚本直接导入 MCP 源码 | **保留**（工具需要）|
| 断开的引用 | **修复**（移除或更正目标）|

---

## 三、详细任务清单

### 任务 1: 修复 MCP Server 反向引用（P0）

**目标**: 删除所有 MCP 对 Agent-Skill 的引用

**文件**:
- `skill-creator-mcp/README.md:338`
- `skill-creator-mcp/docs/README.md:66,83,165`
- `skill-creator-mcp/docs/installation.md:315,328`
- `skill-creator-mcp/docs/claude-code-config.md:415`
- `skill-creator-mcp/docs/ide-config.md:341`

**操作**: 删除所有 `../skill-creator/` 引用

### 任务 2: 清理 Agent-Skill 中的 Claude Code 配置章节（P0）

**目标**: 移除 SKILL.md 中的完整配置内容

**文件**:
- `skill-creator/SKILL.md:96-158` - 完整 Claude Code 配置章节

**操作**: 删除配置内容，替换为 MCP 文档引用

### 任务 3: 修复断开的引用（P1）

**目标**: 解决 claude-code-configuration.md 缺失问题

**文件**:
- `skill-creator/references/README.md:19,64`
- `skill-creator/examples/README.md:74`
- `skill-creator-mcp/docs/ide-config.md:341`

**操作**: 更新为正确的 MCP 文档路径

### 任务 4: 清理 MCP 技术实现细节（P1）

**目标**: 移除 Agent-Skill 中对 MCP 源码的引用

**文件**:
- `references/brainstorming-techniques.md:231-233`
- `references/requirement-collection-api-core.md:24`
- `references/troubleshooting.md`（多处）
- `examples/requirement-collection-brainstorm.md:154`

**操作**: 删除源码路径和函数实现细节引用

### 任务 5: 验证所有交叉引用（P1）

**目标**: 确保所有链接有效

**操作**: 运行引用检查，修复所有 404 链接

### 任务 6: 更新 CHANGELOG.md（P2）

**目标**: 记录本次修复

**操作**: 在 CHANGELOG 中添加修复条目

### 任务 7: 测试验证（P2）

**目标**: 确保修复后文档结构正确

**操作**: 手动验证所有关键链接

---

## 四、验收标准

1. ✅ MCP 文档中无 `../skill-creator/` 引用
2. ✅ Agent-Skill SKILL.md 无 Claude Code 配置章节
3. ✅ 所有断开的引用已修复
4. ✅ 无技术实现细节泄露到用户文档
5. ✅ CHANGELOG 已更新

---

## 五、关键文件清单

| 文件 | 修改类型 | 优先级 |
|------|----------|--------|
| `skill-creator-mcp/README.md` | 删除引用 | P0 |
| `skill-creator-mcp/docs/README.md` | 删除引用 | P0 |
| `skill-creator-mcp/docs/installation.md` | 删除引用 | P0 |
| `skill-creator-mcp/docs/claude-code-config.md` | 删除引用 | P0 |
| `skill-creator-mcp/docs/ide-config.md | 删除引用 + 修复断链 | P0 |
| `skill-creator/SKILL.md` | 删除配置章节 | P0 |
| `skill-creator/references/README.md` | 修复断链 | P1 |
| `skill-creator/examples/README.md` | 修复断链 | P1 |
| `skill-creator/references/brainstorming-techniques.md` | 清理技术细节 | P1 |
| `skill-creator/references/requirement-collection-api-core.md` | 清理技术细节 | P1 |
| `CHANGELOG.md` | 更新记录 | P2 |

---

## 六、风险评估

| 风险 | 影响 | 缓解措施 |
|------|------|----------|
| 用户体验中断 | 中 | 保留 MCP 文档引用 |
| 文档链接断开 | 低 | 全面测试验证 |
| 遗漏违规引用 | 低 | 交叉验证检查 |

---

## 七、参考资料

- `CLAUDE.md` - 项目开发规范（第3.1节：Git规范、第4.3节：文档放置规则）
- `ARCHITECTURE_AUDIT_REPORT_v2.md` - 架构审计报告
- `docs/adr/001-hybrid-architecture.md` - 混合架构设计决策
