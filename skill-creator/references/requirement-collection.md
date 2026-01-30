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
| **[需求收集工作流](requirement-workflow.md)** | 实践工作流编排指南 | ~280 |
| **[需求收集模式详解](requirement-collection-modes.md)** | 各种模式的详细说明和对比 | ~150 |
| **[需求收集 API 参考](requirement-collection-api.md)** | API 文档索引 | ~70 |
| **[API 核心参考](requirement-collection-api-core.md)** | 完整的 API 技术文档 | ~180 |
| **[API 使用示例](requirement-collection-api-examples.md)** | 实际使用场景和最佳实践 | ~150 |

---

## 核心概念

### 7个原子化工具

需求收集功能由7个独立的MCP工具提供：

| 工具 | 功能 |
|------|------|
| `create_requirement_session_tool` | 创建需求收集会话 |
| `get_requirement_session_tool` | 获取会话状态 |
| `update_requirement_answer_tool` | 更新答案 |
| `get_static_question_tool` | 获取预定义问题（basic/complete模式） |
| `generate_dynamic_question_tool` | 生成动态问题（brainstorm/progressive模式） |
| `validate_answer_format_tool` | 验证答案格式 |
| `check_requirement_completeness_tool` | 检查需求完整性 |

### 会话状态管理

通过 `create_requirement_session_tool` 和 `get_requirement_session_tool` 管理会话状态：

- **状态存储**：持久化会话数据
- **自动恢复**：中断后可从上次步骤继续
- **会话隔离**：不同会话互不影响

### AI 驱动引导

使用 LLM 动态生成问题和引导对话：

- **智能采样**：通过 `generate_dynamic_question_tool` 获取 AI 生成的响应
- **上下文感知**：根据已收集信息调整后续问题
- **完整性检查**：通过 `check_requirement_completeness_tool` 使用 LLM 判断需求是否完整

### 输入验证

实时验证用户输入：

- **格式检查**：正则表达式、长度限制
- **选项验证**：确保输入在可选项范围内
- **即时反馈**：通过 `validate_answer_format_tool` 错误时返回具体帮助文本

---

## 收集模式概览

需求收集功能支持 4 种收集模式 + 1 种自动化模式：

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

#### 未来重构方向

- **短期（v0.3.x）**: 保持现有API，改进内部实现 ✅ 已完成
  - 简化函数结构（224行 → 114行）
  - 提取状态管理（SessionStateManager类）
  - 完善文档说明

- **长期（v0.5+）**: 评估FastMCP新API，考虑迁移到理想架构

---

## 示例代码

查看 [需求收集示例](../examples/requirement-collection-basic.md) 获取完整的代码示例和用法。

## 相关文档

- **[MCP 集成指南](mcp-tools-reference.md)** - MCP 工具使用和配置
- **[最佳实践](best-practices-core.md)** - Agent-Skill 开发规范
- **[验证规范](validation.md)** - 技能验证规则
