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
| **[需求收集 API 参考](requirement-collection-api.md)** | API 文档索引 | ~70 |
| **[API 核心参考](requirement-collection-api-core.md)** | 完整的 API 技术文档 | ~180 |
| **[API 使用示例](requirement-collection-api-examples.md)** | 实际使用场景和最佳实践 | ~150 |

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

---

## 架构说明

### 为什么循环逻辑在MCP层？

`collect_requirements` 工具的内部实现包含了循环逻辑（`while not session_state.completed`），这看起来违反了"MCP提供原子操作"的原则。这个设计是**技术约束下的权衡决策**。

#### 技术原因

1. **`ctx.elicit()` 只能在MCP层调用**
   - FastMCP的elicit API是MCP Server级别的
   - Agent-Skill无法直接访问ctx对象

2. **会话状态管理需要MCP能力**
   - `ctx.set_state` / `ctx.get_state` 是MCP Server的能力
   - 状态持久化需要MCP Server支持

3. **LLM采样需要MCP上下文**
   - `ctx.sample()` 用于动态问题生成
   - 需要MCP Server的LLM集成

#### 架构权衡

| 维度 | 理想架构 | 实际架构 | 权衡原因 |
|------|----------|----------|----------|
| 循环逻辑 | Agent-Skill层 | MCP层 | elicit API限制 |
| 状态管理 | Agent-Skill层 | MCP层 | ctx.set_state API |
| LLM采样 | Agent-Skill层 | MCP层 | ctx.sample API |

**详细说明**: 参见 [需求收集架构设计文档](requirement-collection-architecture.md)

#### 未来重构方向

- **短期（v0.3.x）**: 保持现有API，改进内部实现 ✅ 已完成
  - 简化函数结构（224行 → 114行）
  - 提取状态管理（SessionStateManager类）
  - 完善文档说明

- **长期（v0.5+）**: 评估FastMCP新API，考虑迁移到理想架构

**参考**: [工作流编排示例](../examples/workflow-orchestration.md) - 详解MCP与Agent-Skill职责分工
