# 需求收集指南

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

需求收集功能支持 4 种收集模式：

| 模式 | 步骤 | 适用场景 |
|------|------|----------|
| **basic** | 5 步 | 明确需求的用户 |
| **complete** | 10 步 | 复杂技能，需要详细技术规格 |
| **brainstorm** | 动态 | AI 引导的创意发散 |
| **progressive** | 动态 | 快速开始，后续逐步完善 |

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

## 工作流指南

### 模式1：基础模式（Basic Mode - 5步）

```yaml
1. 调用 create_requirement_session_tool(mode="basic")
   → 返回: session_id, total_steps=5

2. 循环（5步）：
   a. 调用 get_static_question_tool(mode="basic", step_index=i)
   b. 向用户展示问题
   c. 获取用户输入
   d. 调用 validate_answer_format_tool(answer, validation)
   e. 如果验证失败，显示错误并重新获取
   f. 调用 update_requirement_answer_tool(session_id, question_key, answer)

3. 调用 check_requirement_completeness_tool(answers)
   → 返回: complete, missing_items, suggestions
```

### 模式2：完整模式（Complete Mode - 10步）

与基础模式相同，但 `total_steps=10`，包含额外问题：

1. 基础问题（5个）：skill_name, skill_function, use_cases, template_type, additional_features
2. 额外问题（5个）：target_users, tech_stack, dependencies, testing_requirements, documentation_level

### 模式3：动态模式（Brainstorm/Progressive）

#### Brainstorm 模式（头脑风暴）

```python
session = await create_requirement_session_tool(mode="brainstorm")
conversation_history = []

for i in range(5):  # 默认5轮对话
    question = await generate_dynamic_question_tool(
        mode="brainstorm",
        answers=session["answers"],
        conversation_history=conversation_history
    )
    answer = "<用户提供的答案>"
    await update_requirement_answer_tool(
        session_id=session["session_id"],
        question_key=question["question_key"],
        answer=answer
    )
    conversation_history.append({
        "question": question["question"],
        "answer": answer
    })
```

#### Progressive 模式（渐进式）

```python
session = await create_requirement_session_tool(mode="progressive")

while True:
    question = await generate_dynamic_question_tool(
        mode="progressive",
        answers=session["answers"]
    )
    if not question.get("question"):
        break  # 没有更多问题
    answer = "<用户提供的答案>"
    await update_requirement_answer_tool(
        session_id=session["session_id"],
        question_key=question["question_key"],
        answer=answer
    )
```

### 中断恢复

```python
# 恢复之前的会话
session = await get_requirement_session_tool(
    session_id="previous_session_id"
)
# 从当前步骤继续
current_step = session["current_step"]
```

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

---

## 模式选择指南

### 决策树

```
需求明确度？
├─ 非常明确 → Basic 模式
├─ 需要细节 → Complete 模式
├─ 只有想法 → Brainstorm 模式
└─ 快速原型 → Progressive 模式
```

### 对比总结

| 模式 | 步骤 | 速度 | 完整性 | 灵活性 |
|------|------|------|--------|--------|
| **basic** | 5 | ⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐ |
| **complete** | 10 | ⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐ |
| **brainstorm** | 动态 | ⭐⭐⭐ | ⭐⭐ | ⭐⭐⭐⭐⭐ |
| **progressive** | 动态 | ⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐⭐ |

---

## 最佳实践

### 1. 错误处理

```python
# 验证答案时处理错误
validation = await validate_answer_format_tool(
    answer=answer,
    validation=question.get("validation", {})
)

if not validation["valid"]:
    # 显示错误信息
    print(f"验证失败: {validation.get('error')}")
    # 显示帮助文本
    if validation.get('help_text'):
        print(f"提示: {validation['help_text']}")
    # 重新获取输入
    continue
```

### 2. 完整性检查

```python
# 检查需求完整性
completeness = await check_requirement_completeness_tool(
    answers=session["answers"]
)

if completeness["is_complete"]:
    print("需求完整")
else:
    print(f"缺少信息: {completeness['missing_info']}")
    print(f"建议: {completeness['suggestions']}")
```

### 3. 答案修改

```python
# 可以修改之前保存的答案
await update_requirement_answer_tool(
    session_id=session_id,
    question_key="skill_name",
    answer="new-skill-name"  # 新值覆盖旧值
)
```

---

## 示例代码

查看 [需求收集示例](../examples/requirement-collection-basic.md) 获取完整的代码示例和用法。

## 相关文档

- **[需求收集 API 参考](requirement-collection-api.md)** - 完整 API 文档
- **[MCP 集成指南](mcp-tools-reference.md)** - MCP 工具使用和配置
- **[最佳实践](best-practices-core.md)** - Agent-Skill 开发规范
- **[验证规范](validation.md)** - 技能验证规则
