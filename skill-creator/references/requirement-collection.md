# 需求澄清指南

> **重要更新**：需求收集功能已重构为7个原子化工具，符合ADR 001架构原则。

Skill-Creator 提供的需求收集功能基于 **MCP原子化工具 + Agent-Skill工作流编排** 的混合架构。

## 快速开始

```python
# 通过 Agent-Skill 工作流使用需求收集
# 详见 skill-creator/SKILL.md 的需求收集章节

# MCP 层原子化工具（7个）：
# - create_requirement_session_tool   # 创建会话
# - get_requirement_session_tool      # 获取会话状态
# - update_requirement_answer_tool    # 更新答案
# - get_static_question_tool          # 获取静态问题
# - generate_dynamic_question_tool    # 生成动态问题
# - validate_answer_format_tool       # 验证答案格式
# - check_requirement_completeness_tool  # 检查完整性
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

- **原子化工具**：7个独立的MCP工具，职责单一，符合ADR 001原则
- **工作流编排**：Agent-Skill负责业务流程编排
- **会话状态管理**：通过 `create_requirement_session_tool` 和 `get_requirement_session_tool` 管理
- **AI 驱动引导**：通过 `generate_dynamic_question_tool` 获取 AI 生成的动态问题
- **输入验证**：通过 `validate_answer_format_tool` 实时验证格式、长度、选项
- **4 种收集模式**：basic、complete、brainstorm、progressive
- **完整性检查**：通过 `check_requirement_completeness_tool` 确保需求完整性

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

### MCP + Agent-Skill 混合架构

需求收集功能采用符合ADR 001原则的原子化架构：

**MCP Server层（skill-creator-mcp）**：
- 提供7个原子化工具，每个工具职责单一
- 处理文件I/O、数据验证、状态管理等原子操作
- 返回结构化结果

**Agent-Skill层（skill-creator）**：
- 编排工作流程，管理业务逻辑
- 传递知识和最佳实践
- 提供渐进式披露的内容

**架构优势**：
1. **职责分离**：MCP提供原子操作，Agent-Skill编排工作流
2. **符合MCP规范**：遵循Model Context Protocol最佳实践
3. **易于维护**：每个工具独立，便于测试和更新
4. **灵活扩展**：可单独替换某个工具而不影响整体

#### 架构权衡

| 维度 | 理想架构 | 实际架构 | 权衡原因 |
|------|----------|----------|----------|
| 循环逻辑 | Agent-Skill层 | MCP层 | elicit API限制 |
| 状态管理 | Agent-Skill层 | MCP层 | ctx.set_state API |
| LLM采样 | Agent-Skill层 | MCP层 | ctx.sample API |

**详细说明**: 参见 [需求收集模式](requirement-collection-modes.md) 了解7个原子工具的设计理念

#### 未来重构方向

- **短期（v0.3.x）**: 保持现有API，改进内部实现 ✅ 已完成
  - 简化函数结构（224行 → 114行）
  - 提取状态管理（SessionStateManager类）
  - 完善文档说明

- **长期（v0.5+）**: 评估FastMCP新API，考虑迁移到理想架构

**参考**: [工作流编排示例](../examples/workflow-orchestration.md) - 详解MCP与Agent-Skill职责分工
