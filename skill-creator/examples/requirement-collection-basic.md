# 需求澄清示例文档导航

> **说明**：本文档为需求澄清所有示例的导航索引，帮助快速找到合适的示例文档。

> **架构更新**：需求收集功能现在基于7个原子化MCP工具，通过Agent-Skill工作流编排使用。

本文档提供需求收集功能的各种使用示例。

## 示例导航

| 示例 | 模式 | 说明 | 预计时间 |
|------|------|------|----------|
| **[基础模式](example-basic-mode.md)** | basic | 5 步快速收集核心信息 | 3-5 分钟 |
| **[完整模式](example-complete-mode.md)** | complete | 10 步全面收集技术细节 | 10-15 分钟 |
| **[渐进模式](example-progressive-mode.md)** | progressive | 核心信息优先，可跳过 | 2-3 分钟 |
| **[Elicit 模式](example-elicit-mode.md)** | elicit | 一键自动收集所有输入 | 1-2 分钟 |

## 模式对比

| 特性 | 基础 | 完整 | 渐进 | Elicit |
|------|------|------|------|--------|
| 步骤 | 5 | 10 | 动态 | 自动 |
| 速度 | ⭐⭐⭐ | ⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| 完整性 | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐⭐ |
| 灵活性 | ⭐⭐ | ⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐ |

## 快速开始

需求收集功能通过Agent-Skill工作流使用，详见 `skill-creator/SKILL.md`。

底层使用7个原子化MCP工具：
- `create_requirement_session_tool` - 创建会话
- `get_requirement_session_tool` - 获取会话状态
- `update_requirement_answer_tool` - 更新答案
- `get_static_question_tool` - 获取预定义问题
- `generate_dynamic_question_tool` - 生成动态问题
- `validate_answer_format_tool` - 验证答案格式
- `check_requirement_completeness_tool` - 检查完整性

### 最简单的方式：基础模式

通过Agent-Skill工作流启动basic模式，然后逐个回答问题。

### 最快速的方式：Elicit 模式

通过Agent-Skill工作流启动elicit模式，一键自动收集。

```json
{
  "action": "start",
  "mode": "basic",
  "use_elicit": true
}
```

一步完成所有收集。

## 核心功能演示

所有示例都演示以下核心功能：

- ✅ 会话状态管理
- ✅ 中断后恢复
- ✅ 答案修改 (previous)
- ✅ 进度查询 (status)
- ✅ 验证错误处理
- ✅ 完整性检查

## 回退机制说明

> **注意**: 由于当前客户端限制，部分功能使用回退策略：
> - 动态问题生成 → 预定义问题列表
> - 交互式输入收集 → 逐步问答模式
> - LLM 智能分析 → 固定规则检查
>
> 详见 [客户端兼容性说明](../references/requirement-workflow.md#客户端兼容性)

## 相关文档

- **[需求澄清指南](../references/requirement-collection.md)** - 详细文档
- **[需求收集模式详解](../references/requirement-collection-modes.md)** - 模式说明
- **[需求收集 API 参考](../references/requirement-collection-api.md)** - API 文档索引
- **[API 核心参考](../references/requirement-collection-api-core.md)** - 完整的 API 技术文档
- **[API 使用示例](../references/requirement-collection-api-examples.md)** - 实际使用场景和最佳实践
- **[MCP 集成指南](../references/mcp-integration.md)** - MCP 工具配置
