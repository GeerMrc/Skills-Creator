# 需求澄清指南

`collect_requirements` 是 Skill-Creator 提供的 AI 驱动需求澄清工具，通过对话式交互逐步收集技能创建所需信息。

## 快速开始

```python
# 基础模式 - 5步快速收集
result = await collect_requirements(
    action="start",
    mode="basic"
)

# Elicit 自动模式 - 一键完成所有收集
result = await collect_requirements(
    action="start",
    mode="basic",
    use_elicit=True
)
```

## 文档导航

| 文档 | 说明 | 行数 |
|------|------|------|
| **[需求澄清基础指南](requirement-collection-basics.md)** | 核心概念、模式概览、快速开始 | ~150 |
| **[需求收集模式详解](requirement-collection-modes.md)** | 各种模式的详细说明和对比 | ~150 |
| **[需求收集 API 参考](requirement-collection-api.md)** | 完整的 API 文档和错误处理 | ~170 |

## 核心特性

- **会话状态管理**：使用 FastMCP Context API，支持中断后恢复
- **AI 驱动引导**：通过 `ctx.sample()` 获取 AI 生成的响应
- **输入验证**：实时验证格式、长度、选项
- **4 种收集模式**：basic、complete、brainstorm、progressive
- **Elicit 自动模式**：设置 `use_elicit=True` 一键完成收集

## 收集模式对比

| 模式 | 步骤 | 适用场景 |
|------|------|----------|
| **basic** | 5 | 明确需求的用户 |
| **complete** | 10 | 复杂技能，需要详细规格 |
| **brainstorm** | 动态 | AI 引导的创意发散 |
| **progressive** | 动态 | 快速原型，后续完善 |
| **elicit** | 自动 | 一键完成所有收集 |

## 示例代码

查看 [需求收集示例](../examples/requirement-collection-basic.md) 获取完整的代码示例和用法。

## 相关文档

- **[MCP 集成指南](mcp-integration.md)** - MCP 工具使用和配置
- **[最佳实践](best-practices-core.md)** - Agent-Skill 开发规范
- **[验证规范](validation.md)** - 技能验证规则
