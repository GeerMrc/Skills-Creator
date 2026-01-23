# 需求澄清基础指南

## 概述

Skill-Creator 提供 AI 驱动的需求澄清工具 `collect_requirements`，通过对话式交互逐步收集技能创建所需信息。该工具支持会话状态管理，允许中断后恢复，并提供实时进度跟踪。

> **相关文档**：
> - [需求收集模式详解](requirement-collection-modes.md) - 各种收集模式的详细说明
> - [需求收集 API 参考](requirement-collection-api.md) - API 文档索引
> - [API 核心参考](requirement-collection-api-core.md) - 完整的 API 技术文档
> - [API 使用示例](requirement-collection-api-examples.md) - 实际使用场景和最佳实践
> - [需求收集示例](../examples/requirement-collection-basic.md) - 代码示例和用法

## 核心概念

### 会话状态管理

`collect_requirements` 使用 FastMCP 的 Context API 管理会话状态：

- **状态存储**：通过 `ctx.get_state()` 和 `ctx.set_state()` 持久化会话
- **自动恢复**：中断后可从上次步骤继续
- **会话隔离**：不同会话互不影响

### AI 驱动引导

使用 LLM 动态生成问题和引导对话：

- **智能采样**：通过 `ctx.sample()` 获取 AI 生成的响应
- **上下文感知**：根据已收集信息调整后续问题
- **完整性检查**：使用 LLM 判断需求是否完整

### 输入验证

实时验证用户输入：

- **格式检查**：正则表达式、长度限制
- **选项验证**：确保输入在可选项范围内
- **即时反馈**：错误时返回具体帮助文本

## 收集模式概览

`collect_requirements` 支持 4 种收集模式 + 1 种自动化模式：

| 模式 | 步骤 | 适用场景 |
|------|------|----------|
| **basic** | 5 步 | 明确需求的用户 |
| **complete** | 10 步 | 复杂技能，需要详细技术规格 |
| **brainstorm** | 动态 | AI 引导的创意发散 |
| **progressive** | 动态 | 快速开始，后续逐步完善 |
| **elicit** | 自动 | 一键自动收集所有输入 |

### 基础模式 (basic)

5 步快速收集核心信息：
1. 技能名称
2. 主要功能
3. 使用场景
4. 模板类型
5. 额外需求

### 完整模式 (complete)

10 步全面收集技术细节：
- 包含基础模式的 5 步
- 加上：目标用户、技术栈、外部依赖、测试要求、文档级别

### 头脑风暴模式 (brainstorm)

AI 引导的创意发散：
- 开放性问题引导思考
- 鼓励多角度探索
- 记录所有想法

### 渐进式模式 (progressive)

快速开始，后续完善：
- 核心信息优先
- 允许跳过非关键步骤
- 后续可补充细节

### Elicit 自动模式

设置 `use_elicit=True` 后，AI 自动调用 `ctx.elicit()` 逐个收集输入：

- **自动化**：无需手动调用 action="next"
- **验证重试**：输入无效时自动重新请求
- **状态保存**：每步后自动保存会话状态
- **取消友好**：用户可随时取消

**与传统模式的区别**：

| 特性 | 传统模式 | Elicit 模式 |
|------|----------|------------|
| 调用次数 | 多次（每步一次） | 一次（自动收集所有） |
| 用户交互 | 手动调用 next | AI 自动调用 elicit |
| 状态管理 | 手动管理 | 自动保存每步 |
| 适用场景 | 需要中断/恢复的场景 | 快速完成需求收集 |

## 快速开始

### 基础用法

```python
# 1. 开始收集
result = await collect_requirements(
    action="start",
    mode="basic"
)

# 2. 逐个回答问题
result = await collect_requirements(
    action="next",
    session_id=result["session_id"],
    user_input="pdf-parser"
)

# 3. 完成收集
result = await collect_requirements(
    action="complete",
    session_id=result["session_id"]
)
```

### Elicit 自动模式

```python
# 一步完成所有收集
result = await collect_requirements(
    action="start",
    mode="basic",
    use_elicit=True  # AI 自动收集所有输入
)
```

## 相关文档

- **[需求收集模式详解](requirement-collection-modes.md)** - 各种模式的详细说明和对比
- **[需求收集 API 参考](requirement-collection-api.md)** - API 文档索引
- **[API 核心参考](requirement-collection-api-core.md)** - 完整的 API 文档和错误处理
- **[API 使用示例](requirement-collection-api-examples.md)** - 实际使用场景和最佳实践
- **[需求收集示例](../examples/requirement-collection-basic.md)** - 完整的代码示例
- **[MCP 集成指南](mcp-integration.md)** - MCP 工具使用和配置
