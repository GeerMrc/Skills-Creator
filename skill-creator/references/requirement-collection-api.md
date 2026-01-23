# 需求收集 API 参考

本文档提供 `collect_requirements` 工具的 API 参考索引。

> **相关文档**：
> - [需求澄清基础指南](requirement-collection-basics.md) - 核心概念和快速开始
> - [需求收集模式详解](requirement-collection-modes.md) - 各种模式详细说明

---

## 文档结构

API 参考已拆分为两个部分：

### [API 核心参考](requirement-collection-api-core.md)

完整的 API 技术文档，包括：

- 工具签名和参数说明
- 返回值结构
- Action 类型详解（start/next/previous/status/complete）
- 验证规则（必填、长度、格式、选项）
- 完整性检查机制
- 错误处理
- 技术实现细节

**适合读者**：开发者、集成人员

---

### [API 使用示例](requirement-collection-api-examples.md)

实际使用场景和最佳实践，包括：

- 快速创建技能流程
- 中断后恢复会话
- 修改之前答案
- 最佳实践建议
- 完整工作流示例

**适合读者**：所有用户

---

## 快速导航

| 需求 | 推荐文档 |
|------|---------|
| 了解 API 参数 | [API 核心参考](requirement-collection-api-core.md#参数说明) |
| 查看返回值格式 | [API 核心参考](requirement-collection-api-core.md#返回值) |
| 学习如何使用 | [API 使用示例](requirement-collection-api-examples.md) |
| 处理错误情况 | [API 核心参考](requirement-collection-api-core.md#错误处理) |
| 查看最佳实践 | [API 使用示例](requirement-collection-api-examples.md#最佳实践) |

---

## 相关文档

- **[需求澄清基础指南](requirement-collection-basics.md)** - 核心概念和快速开始
- **[需求收集模式详解](requirement-collection-modes.md)** - 各种模式详细说明
- **[MCP 集成指南](mcp-integration.md)** - MCP 工具使用和配置
- **[最佳实践](best-practices-core.md)** - Agent-Skill 开发规范
