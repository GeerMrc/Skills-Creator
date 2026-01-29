# 需求收集 API 使用示例

> **架构说明**：需求收集基于 **7个原子化MCP工具 + Agent-Skill工作流编排** 的混合架构（符合ADR 001）。本文档展示使用场景和最佳实践，实际使用通过skill-creator Agent-Skill调用。

> **相关文档**：
> - [API 核心参考](requirement-collection-api-core.md) - 完整 API 文档
> - [需求澄清基础指南](requirement-collection-basics.md) - 核心概念和快速开始

---

## 目录

- [场景 1：快速创建技能（basic模式）](#场景-1快速创建技能basic模式)
- [场景 2：中断后恢复](#场景-2中断后恢复)
- [场景 3：修改之前答案](#场景-3修改之前答案)
- [场景 4：brainstorm模式探索想法](#场景-4brainstorm模式探索想法)
- [最佳实践](#最佳实践)

---

## 场景 1：快速创建技能（basic模式）

使用基础模式快速收集创建技能所需的核心信息。

```python
# 1. 创建会话
session_result = await create_requirement_session_tool(
    mode="basic"
)
# 返回: {"success": true, "session_id": "req_20260129_abc123", ...}
session_id = session_result["session_id"]

# 2. 获取第一个问题
question_result = await get_static_question_tool(
    mode="basic",
    step_index=0
)
# 返回: {"question": "技能名称是什么？", "key": "skill_name", ...}

# 3. 用户回答后保存答案
await update_requirement_answer_tool(
    session_id=session_id,
    question_key="skill_name",
    answer="pdf-parser"
)

# 4. 继续获取和回答问题（5个步骤）
for i in range(1, 5):
    question = await get_static_question_tool(mode="basic", step_index=i)
    answer = await get_user_input(question["prompt"])  # Agent-Skill层的交互
    await update_requirement_answer_tool(
        session_id=session_id,
        question_key=question["key"],
        answer=answer
    )

# 5. 获取会话状态和所有答案
session_data = await get_requirement_session_tool(session_id=session_id)
answers = session_data["answers"]

# 6. 检查完整性
completeness = await check_requirement_completeness_tool(answers=answers)

# 7. 使用收集的信息初始化技能
await init_skill(
    name=answers["skill_name"],
    template=answers["template_type"]
)
```

**适用场景**：
- 已有明确的技能想法
- 只需要核心信息即可开始
- 希望快速验证概念

---

## 场景 2：中断后恢复

会话状态自动保存，可以随时恢复中断的收集过程。

```python
# 用户在第 3 步中断...

# 恢复会话（查询当前状态）
session_data = await get_requirement_session_tool(
    session_id="previous_session_id"
)
# 返回: {
#   "session_id": "req_20260129_abc123",
#   "mode": "basic",
#   "current_step": 3,
#   "answers": {"skill_name": "...", "skill_function": "...", ...}
# }

# 从当前步骤继续
question = await get_static_question_tool(
    mode="basic",
    step_index=session_data["current_step"]
)
answer = await get_user_input(question["prompt"])
await update_requirement_answer_tool(
    session_id=session_id,
    question_key=question["key"],
    answer=answer
)
```

**适用场景**：
- 用户临时中断操作
- 需要分多次完成收集
- 多人协作收集需求

---

## 场景 3：修改之前答案

直接更新已保存的答案。

```python
# 用户想修改第 2 步的答案
await update_requirement_answer_tool(
    session_id="current_session_id",
    question_key="skill_function",
    answer="新的功能描述"
)

# 验证新答案
validation_result = await validate_answer_format_tool(
    answer="新的功能描述",
    validation={"min_length": 10, "max_length": 500}
)

if not validation_result["valid"]:
    print("验证失败：", validation_result["error"])
```

**适用场景**：
- 用户发现输入错误
- 需要调整之前的答案
- 想要尝试不同选项

---

## 场景 4：brainstorm模式探索想法

使用动态生成的问题探索不明确的想法。

```python
# 1. 创建brainstorm模式会话
session_result = await create_requirement_session_tool(
    mode="brainstorm"
)
session_id = session_result["session_id"]

# 2. 初始对话历史
conversation_history = []
answers = {}

# 3. 动态生成问题并收集答案
for round_num in range(5):  # 最多5轮对话
    # 生成下一个问题
    question_result = await generate_dynamic_question_tool(
        mode="brainstorm",
        answers=answers,
        conversation_history=conversation_history
    )

    question = question_result["question"]
    print(f"问题 {round_num + 1}: {question}")

    # 获取用户输入
    answer = await get_user_input(question)

    # 保存答案
    key = f"question_{round_num + 1}"
    answers[key] = answer
    await update_requirement_answer_tool(
        session_id=session_id,
        question_key=key,
        answer=answer
    )

    # 更新对话历史
    conversation_history.append({
        "role": "assistant",
        "content": question
    })
    conversation_history.append({
        "role": "user",
        "content": answer
    })

    # 检查是否应该继续
    if not question_result.get("continue_questioning", True):
        break

# 4. 检查完整性
completeness = await check_requirement_completeness_tool(answers=answers)
print("完整性：", completeness["is_complete"])
print("缺失信息：", completeness.get("missing_info", []))
```

**适用场景**：
- 技能想法不明确
- 需要探索多种可能性
- 希望获得AI引导的思考

---

## 最佳实践

### 1. 选择合适的模式

根据需求明确度选择合适的收集模式：

| 需求状态 | 推荐模式 | 步骤数 | 预计时间 | 问题类型 |
|---------|---------|-------|---------|---------|
| 明确需求 | `basic` | 5 | 3-5分钟 | 预定义静态问题 |
| 复杂技能 | `complete` | 10 | 8-10分钟 | 预定义静态问题 |
| 探索想法 | `brainstorm` | 动态 | 10-15分钟 | AI生成动态问题 |
| 快速原型 | `progressive` | 3 | 2-3分钟 | AI生成动态问题 |

### 2. 提供清晰的用户输入

确保答案简洁明确：

```python
# 好的输入
answer = "pdf-parser"

# 不好的输入
answer = "嗯，我想做一个解析 PDF 的工具，名字叫 pdf-parser 吧..."
```

### 3. 利用验证工具

使用 `validate_answer_format_tool` 验证答案格式：

```python
# 定义验证规则
validation_rules = {
    "min_length": 3,
    "max_length": 50,
    "pattern": r"^[a-z][a-z0-9-]*$",
    "pattern_description": "小写字母、数字和连字符，以字母开头"
}

# 验证答案
result = await validate_answer_format_tool(
    answer=answer,
    validation=validation_rules
)

if not result["valid"]:
    print(f"验证失败：{result['error']}")
    # 引导用户重新输入
```

### 4. 检查完整性

完成收集后检查是否缺少关键信息：

```python
completeness = await check_requirement_completeness_tool(answers=answers)

if not completeness["is_complete"]:
    print("缺失信息：", completeness["missing_info"])
    print("建议：", completeness["suggestions"])
    # 可以继续补充信息
```

### 5. 保存会话 ID

会话 ID 是恢复会话的唯一标识：

```python
# 保存会话 ID 以便后续使用
session_id = session_result["session_id"]
# 可以保存到文件、数据库或传递给用户
```

### 6. 错误处理

捕获工具错误并提供友好提示：

```python
result = await create_requirement_session_tool(mode="basic")

if not result["success"]:
    print(result["error"])
    # 根据错误类型引导用户修正
    # 例如：无效的模式、参数错误等
```

---

## 完整工作流示例

### 基础模式完整流程

```python
# 步骤 1：创建会话
session_result = await create_requirement_session_tool(mode="basic")
if not session_result["success"]:
    print(f"创建会话失败：{session_result['error']}")
    return

session_id = session_result["session_id"]
print(f"开始收集，会话ID: {session_id}")

# 步骤 2-5：逐个获取和回答问题
answers = {}
for step in range(5):
    question_result = await get_static_question_tool(
        mode="basic",
        step_index=step
    )

    question = question_result["question"]
    key = question_result["key"]
    prompt = question_result.get("prompt", question)

    # 获取用户输入（Agent-Skill层的交互）
    answer = await get_user_input(prompt)

    # 验证答案格式
    if question_result.get("validation"):
        validation_result = await validate_answer_format_tool(
            answer=answer,
            validation=question_result["validation"]
        )
        if not validation_result["valid"]:
            print(f"验证失败：{validation_result['error']}")
            continue

    # 保存答案
    await update_requirement_answer_tool(
        session_id=session_id,
        question_key=key,
        answer=answer
    )
    answers[key] = answer
    print(f"进度：{(step + 1) * 20}%")

# 步骤 6：检查完整性
completeness = await check_requirement_completeness_tool(answers=answers)

if completeness["is_complete"]:
    print("需求完整，可以开始创建技能！")
    # 使用收集的信息
    await init_skill(
        name=answers["skill_name"],
        template=answers.get("template_type", "minimal")
    )
else:
    print("需要补充信息：", completeness["missing_info"])
    print("建议：", completeness["suggestions"])
```

---

## 迁移指南

### 从旧的 collect_requirements 迁移

如果你之前使用 `collect_requirements` 工具，需要迁移到新的7个原子化工具：

**旧代码（已弃用）**:
```python
# 旧的单个工具
result = await collect_requirements(
    action="start",
    mode="basic"
)
```

**新代码（推荐）**:
```python
# 新的7个原子化工具
session = await create_requirement_session_tool(mode="basic")
question = await get_static_question_tool(mode="basic", step_index=0)
# ... 使用其他工具
```

**主要变化**：
1. 单个工具拆分为7个原子化工具
2. Agent-Skill层负责工作流编排
3. 更灵活的验证和错误处理
4. 更好的可测试性和可复用性

---

## 相关文档

- **[API 核心参考](requirement-collection-api-core.md)** - 完整 API 文档
- **[需求澄清基础指南](requirement-collection-basics.md)** - 核心概念和快速开始
- **[需求收集模式详解](requirement-collection-modes.md)** - 各种模式详细说明
- **[MCP 集成指南](mcp-integration.md)** - MCP 工具使用和配置
