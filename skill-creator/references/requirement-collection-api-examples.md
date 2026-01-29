# 需求收集 API 使用示例

> **架构说明**：需求收集基于 **7个原子化MCP工具 + Agent-Skill工作流编排** 的混合架构。本文档展示基础使用场景。

> **相关文档**：
> - [API 核心参考](requirement-collection-api-core.md) - 完整 API 文档
> - [高级示例](requirement-collection-advanced-examples.md) - 复杂场景和最佳实践

---

## 场景 1：快速创建技能（basic模式）

使用基础模式快速收集创建技能所需的核心信息。

```python
# 1. 创建会话
session_result = await create_requirement_session_tool(mode="basic")
session_id = session_result["session_id"]

# 2. 获取第一个问题
question_result = await get_static_question_tool(mode="basic", step_index=0)

# 3. 用户回答后保存答案
await update_requirement_answer_tool(
    session_id=session_id,
    question_key="skill_name",
    answer="pdf-parser"
)

# 4. 继续获取和回答问题（5个步骤）
for i in range(1, 5):
    question = await get_static_question_tool(mode="basic", step_index=i)
    # answer 由 Agent-Skill 层通过用户交互获取
    answer = "<用户提供的答案>"
    await update_requirement_answer_tool(
        session_id=session_id,
        question_key=question["key"],
        answer=answer
    )

# 5. 获取会话状态
session_data = await get_requirement_session_tool(session_id=session_id)
answers = session_data["answers"]

# 6. 检查完整性
completeness = await check_requirement_completeness_tool(answers=answers)
```

**适用场景**：
- 已有明确的技能想法
- 只需要核心信息即可开始
- 希望快速验证概念

---

## 场景 2：完整模式（complete模式）

收集完整的技术规格和实现细节。

```python
# 创建会话（10个步骤）
session_result = await create_requirement_session_tool(mode="complete")
session_id = session_result["session_id"]

# 获取并回答问题（10步）
for i in range(10):
    question = await get_static_question_tool(mode="complete", step_index=i)
    answer = "<用户提供的答案>"
    await update_requirement_answer_tool(
        session_id=session_id,
        question_key=question["key"],
        answer=answer
    )

# 验证答案格式
validation = await validate_answer_format_tool(
    answer=answer,
    validation={"type": "string", "min_length": 5}
)
```

**适用场景**：
- 复杂技能，需要详细规划
- 团队协作，需要明确的规格
- 生产环境部署

---

## 场景 3：中断后恢复

会话状态自动保存，可以随时恢复中断的收集过程。

```python
# 恢复会话
session_data = await get_requirement_session_tool(
    session_id="previous_session_id"
)

# 从当前步骤继续
current_step = session_data["current_step"]
question = await get_static_question_tool(
    mode="basic",
    step_index=current_step
)
```

---

## 场景 4：修改之前的答案

可以修改已保存的答案。

```python
# 更新之前保存的答案
await update_requirement_answer_tool(
    session_id=session_id,
    question_key="skill_name",
    answer="new-skill-name"  # 新值覆盖旧值
)
```

---

## 相关文档

- **[API 核心参考](requirement-collection-api-core.md)** - 完整 API 文档
- **[高级示例](requirement-collection-advanced-examples.md)** - brainstorm/progressive 模式
- **[需求澄清基础](requirement-collection-basics.md)** - 核心概念
