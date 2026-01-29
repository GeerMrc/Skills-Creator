# 需求收集 API 高级示例

> **架构说明**：需求收集基于 **7个原子化MCP工具 + Agent-Skill工作流编排** 的混合架构。本文档展示高级使用场景。

> **相关文档**：
> - [API 核心参考](requirement-collection-api-core.md) - 完整 API 文档
> - [基础示例](requirement-collection-api-examples.md) - basic/complete 模式

---

## 场景 1：brainstorm模式探索想法

AI 引导的创意发散，探索技能可能性。

```python
# 创建会话
session_result = await create_requirement_session_tool(mode="brainstorm")
session_id = session_result["session_id"]

conversation_history = []

# 默认5轮对话
for i in range(5):
    # 生成动态问题
    question_result = await generate_dynamic_question_tool(
        mode="brainstorm",
        answers=session_result.get("answers", {}),
        conversation_history=conversation_history
    )

    # 获取用户回答
    answer = "<用户提供的答案>"

    # 保存答案
    await update_requirement_answer_tool(
        session_id=session_id,
        question_key=question_result["question_key"],
        answer=answer
    )

    # 更新对话历史
    conversation_history.append({
        "question": question_result["question"],
        "answer": answer
    })
```

**适用场景**：
- 只有模糊的想法
- 需要灵感启发
- 探索多种可能性

---

## 场景 2：progressive模式快速原型

核心信息优先，后续逐步完善。

```python
# 创建会话
session_result = await create_requirement_session_tool(mode="progressive")
session_id = session_result["session_id"]

# 动态生成问题，直到没有更多问题
while True:
    # 根据已收集信息生成针对性问题
    question_result = await generate_dynamic_question_tool(
        mode="progressive",
        answers=session_result.get("answers", {})
    )

    # 检查是否还有问题
    if not question_result.get("question"):
        break  # 没有更多问题

    # 获取并保存答案
    answer = "<用户提供的答案>"
    await update_requirement_answer_tool(
        session_id=session_id,
        question_key=question_result["question_key"],
        answer=answer
    )

    # 更新会话状态
    session_result = await get_requirement_session_tool(session_id=session_id)
```

**适用场景**：
- 快速原型开发
- 需求逐步明确
- 迭代式开发

---

## 场景 3：答案验证和重试

验证答案格式，失败时自动重试。

```python
# 获取问题（包含验证规则）
question = await get_static_question_tool(mode="basic", step_index=0)
validation = question.get("validation", {})

# 循环直到验证通过
while True:
    answer = "<用户提供的答案>"

    # 验证答案
    validation_result = await validate_answer_format_tool(
        answer=answer,
        validation=validation
    )

    if validation_result["valid"]:
        # 验证通过，保存答案
        await update_requirement_answer_tool(
            session_id=session_id,
            question_key=question["key"],
            answer=answer
        )
        break
    else:
        # 验证失败，显示错误并重试
        print(f"验证失败: {validation_result.get('error')}")
        print(f"帮助: {validation_result.get('help_text')}")
        # 继续循环，重新获取输入
```

---

## 场景 4：完整性检查和建议

检查需求完整性，获取补充建议。

```python
# 获取所有答案
session_data = await get_requirement_session_tool(session_id=session_id)
answers = session_data["answers"]

# 检查完整性
completeness_result = await check_requirement_completeness_tool(answers=answers)

if completeness_result["is_complete"]:
    print("需求完整，可以继续")
else:
    print(f"需求不完整，缺少: {completeness_result['missing_info']}")
    print(f"建议补充: {completeness_result['suggestions']}")

    # 可以继续收集缺失信息
    for missing_item in completeness_result["missing_info"]:
        print(f"请补充 {missing_item}")
```

---

## 最佳实践

### 1. 错误处理

```python
try:
    result = await create_requirement_session_tool(mode="basic")
    if not result.get("success"):
        print(f"创建失败: {result.get('error')}")
except Exception as e:
    print(f"发生异常: {e}")
```

### 2. 会话管理

```python
# 保存 session_id 以便后续恢复
session_id = result["session_id"]
print(f"会话ID: {session_id}，请保存以便后续恢复")
```

### 3. 状态查询

```python
# 随时查询会话状态
session_data = await get_requirement_session_tool(session_id=session_id)
print(f"当前步骤: {session_data['current_step']}")
print(f"已完成: {session_data['completed_steps']}")
```

---

## 相关文档

- **[API 核心参考](requirement-collection-api-core.md)** - 完整 API 文档
- **[基础示例](requirement-collection-api-examples.md)** - basic/complete 模式
- **[需求澄清模式详解](requirement-collection-modes.md)** - 模式对比
