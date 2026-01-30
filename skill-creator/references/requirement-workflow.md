# 需求收集工作流指南

> **文档版本**: v1.0.1
> **创建日期**: 2026-01-28
> **更新日期**: 2026-01-29
> **适用范围**: Agent-Skill 需求收集工作流编排

---

## 工作流概述

需求收集工作流由 Agent-Skill 编排，调用 MCP 原子工具完成。

**架构原则**（符合 ADR 001）：
- **MCP Server**: 只提供原子操作工具（会话CRUD、问题生成、答案验证）
- **Agent-Skill**: 编排工作流程、传递最佳实践、提供渐进式披露

---

## 模式1：基础模式（Basic Mode - 5步）

### 工作流程

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

### 示例代码

```python
# 1. 创建会话
session = await create_requirement_session_tool(mode="basic")
session_id = session["session_id"]

# 2. 循环收集答案
for i in range(5):
    question = await get_static_question_tool(mode="basic", step_index=i)
    # 获取用户输入（由 Agent-Skill 层处理）
    answer = "<用户提供的答案>"

    # 验证答案
    validation = await validate_answer_format_tool(
        answer=answer,
        validation=question.get("validation", {})
    )

    if not validation["valid"]:
        print(f"验证失败: {validation['error']}")
        continue  # 重新获取输入

    # 保存答案
    await update_requirement_answer_tool(
        session_id=session_id,
        question_key=question["key"],
        answer=answer
    )

# 3. 检查完整性
completeness = await check_requirement_completeness_tool(
    answers=session["answers"]
)
```

---

## 模式2：完整模式（Complete Mode - 10步）

### 工作流程

与基础模式相同，但 `total_steps=10`，包含额外问题：

1. 基础问题（5个）：skill_name, skill_function, use_cases, template_type, additional_features
2. 额外问题（5个）：target_users, tech_stack, dependencies, testing_requirements, documentation_level

### 调用方式

```python
session = await create_requirement_session_tool(mode="complete")
# total_steps=10
```

---

## 模式3：动态模式（Brainstorm/Progressive）

### 3.1 Brainstorm 模式（头脑风暴）

**特点**: 开放式探索，无固定步骤数

```python
# 1. 创建会话
session = await create_requirement_session_tool(mode="brainstorm")
conversation_history = []

# 2. 循环（默认5轮）
for i in range(5):
    # 生成动态问题
    question = await generate_dynamic_question_tool(
        mode="brainstorm",
        answers=session["answers"],
        conversation_history=conversation_history
    )

    # 获取并保存答案
    answer = "<用户提供的答案>"
    await update_requirement_answer_tool(
        session_id=session["session_id"],
        question_key=question["question_key"],
        answer=answer
    )

    # 更新对话历史
    conversation_history.append({
        "question": question["question"],
        "answer": answer
    })
```

### 3.2 Progressive 模式（渐进式）

**特点**: 核心信息优先，后续逐步完善

```python
# 1. 创建会话
session = await create_requirement_session_tool(mode="progressive")

# 2. 动态生成问题，直到没有更多问题
while True:
    question = await generate_dynamic_question_tool(
        mode="progressive",
        answers=session["answers"]
    )

    # 检查是否还有问题
    if not question.get("question"):
        break

    # 获取并保存答案
    answer = "<用户提供的答案>"
    await update_requirement_answer_tool(
        session_id=session["session_id"],
        question_key=question["question_key"],
        answer=answer
    )

    # 更新会话状态
    session = await get_requirement_session_tool(
        session_id=session["session_id"]
    )
```

---

## 中断恢复

### 保存 session_id

```python
# 创建会话后保存 session_id
session_id = session["session_id"]
print(f"会话ID: {session_id}，请保存以便后续恢复")
```

### 恢复会话

```python
# 恢复之前的会话
session = await get_requirement_session_tool(
    session_id="previous_session_id"
)

# 从当前步骤继续
current_step = session["current_step"]
```

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

## 客户端兼容性

> **说明**：由于不同MCP客户端（如Claude Code、Claude Desktop）的能力支持不同，部分功能使用回退策略。

### 能力限制

| 客户端能力 | 限制说明 | 回退策略 |
|-----------|----------|----------|
| **LLM Sampling** | 部分客户端不支持 | 使用预定义问题列表 |
| **用户征询** | 部分客户端不支持 | 逐步问答模式 |
| **对话循环** | 部分客户端不支持 | 固定步骤收集 |

### 回退策略

**Brainstorm/Progressive模式**：
- ✅ **有LLM Sampling**: 动态生成问题
- ⚠️ **无LLM Sampling**: 使用预定义备用问题列表

**Basic/Complete模式**：
- ✅ **有用户征询**: 交互式输入收集
- ⚠️ **无用户征询**: 静默模式或跳过

**完整性检查**：
- ✅ **有LLM Sampling**: LLM智能分析完整性
- ⚠️ **无LLM Sampling**: 固定规则检查关键字段

### 最佳实践

1. **优先使用Basic模式**：兼容性最好，5步固定流程
2. **检查客户端能力**：通过Agent-Skill层检测可用能力
3. **提供降级体验**：当高级功能不可用时，使用基础功能

---

## 相关文档

- **[API 核心参考](requirement-collection-api-core.md)** - 完整 API 文档
- **[基础示例](requirement-collection-api-examples.md)** - basic/complete 模式示例
- **[高级示例](requirement-collection-advanced-examples.md)** - brainstorm/progressive 模式示例
- **[需求澄清模式详解](requirement-collection-modes.md)** - 模式对比
