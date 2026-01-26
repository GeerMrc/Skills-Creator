# Examples 示例文档索引

本目录包含 Skill-Creator 的使用示例，按功能组织。

## 文档导航

### 快速开始示例

| 示例 | 说明 | 行数 |
|------|------|------|
| **[创建技能](creating-a-skill.md)** | 如何创建新技能 | ~25 |
| **[验证技能](validating-a-skill.md)** | 如何验证技能 | ~20 |
| **[分析技能](analyzing-a-skill.md)** | 如何分析技能 | ~20 |

### 需求澄清示例

| 示例 | 模式 | 步骤 | 行数 |
|------|------|------|------|
| **[基础模式](example-basic-mode.md)** | basic | 5 | ~250 |
| **[完整模式](example-complete-mode.md)** | complete | 10 | ~320 |
| **[渐进模式](example-progressive-mode.md)** | progressive | 动态 | ~350 |
| **[Elicit 模式](example-elicit-mode.md)** | elicit | 自动 | ~350 |
| **[示例导航](requirement-collection-basic.md)** | 模式对比 | - | ~75 |

### MCP 工具示例

| 示例 | 工具 | 说明 | 行数 |
|------|------|------|------|
| **[init_skill 示例](mcp-init-examples.md)** | init_skill | 初始化技能结构 | ~140 |
| **[validate_skill 示例](mcp-validate-examples.md)** | validate_skill | 验证技能规范 | ~180 |
| **[analyze_skill 示例](mcp-analyze-examples.md)** | analyze_skill | 分析代码质量 | ~170 |
| **[refactor_skill 示例](mcp-refactor-examples.md)** | refactor_skill | 生成重构建议 | ~180 |
| **[package_skill 示例](mcp-package-examples.md)** | package_skill | 打包技能 | ~170 |
| **[MCP 使用示例](mcp-usage-examples.md)** | 全部工具 | 综合使用示例 | ~210 |

### 协作示例

| 示例 | 说明 | 行数 |
|------|------|------|
| **[MCP 协作](mcp-skill-collaboration.md)** | Agent-Skill 与 MCP 协同工作流 | ~300 |

### GitHub MCP 集成示例

| 示例 | 说明 | 行数 |
|------|------|------|
| **[需求追踪](github-requirement-tracking.md)** | 使用 GitHub MCP 追踪和管理 Issues | ~260 |
| **[自动化工作流](github-automation.md)** | GitHub PR/Issue 自动化操作 | ~450 |

### Thinking MCP 集成示例

| 示例 | 说明 | 行数 |
|------|------|------|
| **[深度分析](thinking-analysis.md)** | 使用 Thinking MCP 进行顺序思考分析 | ~460 |
| **[导出会话](thinking-export.md)** | Thinking 会话导出和可视化 | ~460 |

---

## 快速查找

### 我想...

| 需求 | 推荐示例 |
|------|---------|
| 快速创建技能 | [基础模式](example-basic-mode.md) |
| 一键完成收集 | [Elicit 模式](example-elicit-mode.md) |
| 了解如何初始化 | [init_skill 示例](mcp-init-examples.md) |
| 验证我的技能 | [validate_skill 示例](mcp-validate-examples.md) |
| 分析代码质量 | [analyze_skill 示例](mcp-analyze-examples.md) |
| 获取重构建议 | [refactor_skill 示例](mcp-refactor-examples.md) |
| 打包发布技能 | [package_skill 示例](mcp-package-examples.md) |
| 批量操作多个技能 | [批量操作示例](mcp-batch-operations.md) |
| 系统健康检查 | [健康检查示例](mcp-health-check.md) |
| 看综合工作流 | [MCP 协作](mcp-skill-collaboration.md) |
| 配置 Claude Code | [Claude Code 配置指南](../docs/claude-code-configuration.md) |

---

## 需求澄清模式对比

| 模式 | 步骤 | 速度 | 完整性 | 适合场景 |
|------|------|------|--------|---------|
| **basic** | 5 | ⭐⭐⭐ | ⭐⭐⭐⭐ | 快速验证概念 |
| **complete** | 10 | ⭐⭐ | ⭐⭐⭐⭐⭐ | 复杂技能开发 |
| **progressive** | 动态 | ⭐⭐⭐⭐ | ⭐⭐⭐ | 快速原型 |
| **elicit** | 自动 | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | 一键完成 |

---

## 示例阅读顺序建议

### 初学者

1. [创建技能](creating-a-skill.md) - 了解基本流程
2. [基础模式](example-basic-mode.md) - 学习需求收集
3. [init_skill 示例](mcp-init-examples.md) - 初始化技能
4. [验证技能](validating-a-skill.md) - 验证创建的技能

### 进阶用户

1. [完整模式](example-complete-mode.md) - 深入需求收集
2. [analyze_skill 示例](mcp-analyze-examples.md) - 分析代码质量
3. [refactor_skill 示例](mcp-refactor-examples.md) - 获取重构建议
4. [MCP 协作](mcp-skill-collaboration.md) - 完整工作流

---

## 相关文档

- **[SKILL.md](../SKILL.md)** - Agent-Skill 主入口
- **[References](../references/README.md)** - 引用文档索引
