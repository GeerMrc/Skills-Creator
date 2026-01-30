# Examples 示例文档索引

本目录包含 Skill-Creator 的使用示例，按功能组织。

## 文档导航

### 快速开始示例

| 示例 | 说明 | 行数 |
|------|------|------|
| **[创建技能](creating-a-skill.md)** | 如何创建新技能 | ~40 |
| **[验证技能](validating-a-skill.md)** | 如何验证技能 | ~40 |
| **[分析技能](analyzing-a-skill.md)** | 如何分析技能 | ~30 |

### 需求澄清示例

| 示例 | 模式 | 步骤 | 行数 |
|------|------|------|------|
| **[基础模式](example-basic-mode.md)** | basic | 5 | ~250 |
| **[完整模式](example-complete-mode.md)** | complete | 10 | ~120 |
| **[渐进模式](example-progressive-mode.md)** | progressive | 动态 | ~180 |

### MCP 工具示例

| 示例 | 工具 | 说明 | 行数 |
|------|------|------|------|
| **[init_skill 示例](mcp-init-examples.md)** | init_skill | 初始化技能结构 | ~260 |
| **[validate_skill 示例](mcp-validate-examples.md)** | validate_skill | 验证技能规范 | ~120 |
| **[analyze_skill 示例](mcp-analyze-examples.md)** | analyze_skill | 分析代码质量 | ~120 |
| **[refactor_skill 示例](mcp-refactor-examples.md)** | refactor_skill | 生成重构建议 | ~135 |
| **[package_skill 示例](mcp-package-examples.md)** | package_skill | 打包技能 | ~200 |
| **[MCP 使用示例](mcp-usage-examples.md)** | 全部工具 | 综合使用示例 | ~300 |

### 协作示例

| 示例 | 说明 | 行数 |
|------|------|------|
| **[MCP 协作](mcp-skill-collaboration.md)** | Agent-Skill 与 MCP 协同工作流 | ~180 |
| **[工作流编排](workflow-orchestration.md)** | 完整工作流编排 | ~260 |

### 高级集成示例

> **注意**：以下示例展示如何为 Agent-Skill 集成外部 MCP，属于可选的高级用法。

| 示例 | 说明 | 行数 |
|------|------|------|
| **[GitHub MCP 集成示范](mcp-github-integration-example.md)** | GitHub MCP 集成最佳实践示范 | ~170 |
| **[Thinking MCP 集成示范](mcp-thinking-integration-example.md)** | Thinking MCP 集成最佳实践示范 | ~240 |

### 打包与 GitHub 集成

| 示例 | 说明 | 行数 |
|------|------|------|
| **[打包示例](packaging-examples.md)** | 打包基础和高级用法 | ~375 |
| **[GitHub 集成示例](github-integration.md)** | 需求跟踪、分支自动化、PR 管理 | ~355 |
| **[需求收集基础](requirement-collection-basic.md)** | 需求收集基础示例 | ~85 |
| **[需求收集头脑风暴](requirement-collection-brainstorm.md)** | brainstorm/progressive 模式 | ~170 |

---

## 快速查找

### 我想...

| 需求 | 推荐示例 |
|------|---------|
| 快速创建技能 | [基础模式](example-basic-mode.md) |
| 了解如何初始化 | [init_skill 示例](mcp-init-examples.md) |
| 验证我的技能 | [validate_skill 示例](mcp-validate-examples.md) |
| 分析代码质量 | [analyze_skill 示例](mcp-analyze-examples.md) |
| 获取重构建议 | [refactor_skill 示例](mcp-refactor-examples.md) |
| 打包发布技能 | [打包示例](packaging-examples.md) |
| GitHub 集成 | [GitHub 集成示例](github-integration.md) |
| 看综合工作流 | [MCP 协作](mcp-skill-collaboration.md) |

---

## 需求澄清模式对比

| 模式 | 步骤 | 速度 | 完整性 | 适合场景 |
|------|------|------|--------|---------|
| **basic** | 5 | ⭐⭐⭐ | ⭐⭐⭐⭐ | 快速验证概念 |
| **complete** | 10 | ⭐⭐ | ⭐⭐⭐⭐⭐ | 复杂技能开发 |
| **progressive** | 动态 | ⭐⭐⭐⭐ | ⭐⭐⭐ | 快速原型 |

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
3. [GitHub 集成示例](github-integration.md) - Git 工作流自动化
4. [MCP 协作](mcp-skill-collaboration.md) - 完整工作流

---

## 相关文档

- **[SKILL.md](../SKILL.md)** - Agent-Skill 主入口
- **[References](../references/README.md)** - 引用文档索引

