# 需求收集 API 参考

本文档提供需求收集功能的 API 参考索引，基于7个原子化MCP工具。

> **相关文档**：
> - [需求澄清基础指南](requirement-collection-basics.md) - 核心概念和快速开始
> - [需求收集模式详解](requirement-collection-modes.md) - 各种模式详细说明

---

## 工具列表

需求收集功能由7个独立的MCP工具提供：

| 工具 | 功能 | 详细文档 |
|------|------|----------|
| `create_requirement_session_tool` | 创建需求收集会话 | [API 核心参考](requirement-collection-api-core.md) |
| `get_requirement_session_tool` | 获取会话状态 | [API 核心参考](requirement-collection-api-core.md) |
| `update_requirement_answer_tool` | 更新答案 | [API 核心参考](requirement-collection-api-core.md) |
| `get_static_question_tool` | 获取预定义问题 | [API 核心参考](requirement-collection-api-core.md) |
| `generate_dynamic_question_tool` | 生成动态问题 | [API 核心参考](requirement-collection-api-core.md) |
| `validate_answer_format_tool` | 验证答案格式 | [API 核心参考](requirement-collection-api-core.md) |
| `check_requirement_completeness_tool` | 检查需求完整性 | [API 核心参考](requirement-collection-api-core.md) |

---

## 文档结构

API 参考已拆分为两个部分：

### [API 核心参考](requirement-collection-api-core.md)

完整的 API 技术文档，包括：

- 7个工具的签名和参数说明
- 返回值结构
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
