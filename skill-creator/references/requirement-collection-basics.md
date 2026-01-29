# 需求澄清基础指南

> **重要迁移说明（2026-01-29）**：
>
> 本文档中部分代码示例使用旧的 `collect_requirements` 工具（已弃用）。
>
> **新架构（推荐）**：需求收集功能已重构为 **7个原子化MCP工具 + Agent-Skill工作流编排**。
>
> **旧代码示例（仅用于理解概念）**：
> ```python
> # 旧的单个工具（已弃用）
> result = await collect_requirements(action="start", mode="basic")
> ```
>
> **新代码（推荐）**：
> ```python
> # 使用7个原子化工具（通过 Agent-Skill 层编排）
> session = await create_requirement_session_tool(mode="basic")
> question = await get_static_question_tool(mode="basic", step_index=0)
> # answer 由 Agent-Skill 层通过用户交互获取
> answer = "<由用户提供的答案>"
> await update_requirement_answer_tool(session_id=session["session_id"], ...)
> ```
>
> **详见**：[需求收集 API 核心](requirement-collection-api-core.md) | [API 使用示例](requirement-collection-api-examples.md)

---

> **架构说明**：需求收集功能基于 **7个原子化MCP工具 + Agent-Skill工作流编排** 的混合架构（符合ADR 001）。本文档展示概念和用法，实际使用通过skill-creator Agent-Skill调用。

## 概述

Skill-Creator 提供 AI 驱动的需求澄清功能，基于 **7个原子化MCP工具 + Agent-Skill工作流编排** 的混合架构。

> **相关文档**：
> - [需求收集模式详解](requirement-collection-modes.md) - 各种收集模式的详细说明
> - [需求收集 API 参考](requirement-collection-api.md) - API 文档索引
> - [API 核心参考](requirement-collection-api-core.md) - 完整的 API 技术文档
> - [API 使用示例](requirement-collection-api-examples.md) - 实际使用场景和最佳实践
> - [需求收集示例](../examples/requirement-collection-basic.md) - 代码示例和用法

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

### 注意事项

**关于用户输入**：
- 用户输入由 Agent-Skill 层处理，MCP 工具只提供原子操作
- 实际使用时通过 skill-creator Agent-Skill 进行工作流编排
- MCP 工具不包含用户交互逻辑

## 快速开始



### 基础用法



```python
# 1. 创建会话
session = await create_requirement_session_tool(mode="basic")
# 返回: {"session_id": "uuid-123", "total_steps": 5, "status": "in_progress"}

# 2. 获取第一个问题
question = await get_static_question_tool(mode="basic", step_index=0)
# 返回: {"question": "请输入技能名称", "key": "skill_name", ...}

# 3. 收集用户答案（由 Agent-Skill 层处理）
# 注意：以下代码展示工作流逻辑，实际需要通过 Agent-Skill 层编排
answer = "<由用户提供的答案>"  # 实际由 Agent-Skill 层获取

# 4. 更新答案
await update_requirement_answer_tool(
    session_id=session["session_id"],
    question_key=question["key"],
    answer=answer
)

# 5. 验证答案格式（可选）
validation = question.get("validation")
if validation:
    result = await validate_answer_format_tool(answer=answer, validation=validation)
    if not result["valid"]:
        # 返回错误信息并重新收集
        help_text = result.get("help_text", "输入格式不正确")
        # 重新获取用户输入（由 Agent-Skill 层处理）
        answer = f"{help_text}\n\n{question['prompt']}"

# 6. 重复步骤2-5直到所有问题完成
# ...

# 7. 检查完整性（可选）
completeness = await check_requirement_completeness_tool(answers=session["answers"])
if not completeness["is_complete"]:
    # 可以继续补充收集
    pass
```

### Agent-Skill 层编排

```python
# 通过 skill-creator Agent-Skill 自动处理工作流
# Agent-Skill 负责用户交互和状态管理
# MCP 工具提供原子操作支持

# 示例：展示工作流概念（实际使用 Agent-Skill）
session = await create_requirement_session_tool(mode="basic")
for i in range(session["total_steps"]):
    question = await get_static_question_tool(mode="basic", step_index=i)
    # answer 由 Agent-Skill 层通过用户交互获取
    answer = "<由用户提供的答案>"
    await update_requirement_answer_tool(
        session_id=session["session_id"],
        question_key=question["key"],
        answer=answer
    )
```

## 相关文档



- **[需求收集模式详解](requirement-collection-modes.md)** - 各种模式的详细说明和对比
- **[需求收集 API 参考](requirement-collection-api.md)** - API 文档索引
- **[API 核心参考](requirement-collection-api-core.md)** - 完整的 API 文档和错误处理
- **[API 使用示例](requirement-collection-api-examples.md)** - 实际使用场景和最佳实践
- **[需求收集示例](../examples/requirement-collection-basic.md)** - 完整的代码示例
- **[MCP 集成指南](mcp-integration.md)** - MCP 工具使用和配置
