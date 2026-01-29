# 需求收集模式详解

> **架构说明**：需求收集基于 **7个原子化MCP工具 + Agent-Skill工作流编排** 的混合架构（符合ADR 001）。本文档展示各种收集模式的概念和用法，实际使用通过skill-creator Agent-Skill调用。

本文档详细说明需求收集功能的各种收集模式，基于7个原子化MCP工具。

> **相关文档**：
> - [需求澄清基础指南](requirement-collection-basics.md) - 核心概念和快速开始
> - [需求收集 API 参考](requirement-collection-api.md) - API 文档索引
> - [API 核心参考](requirement-collection-api-core.md) - 完整的 API 技术文档
> - [API 使用示例](requirement-collection-api-examples.md) - 实际使用场景和最佳实践

## 目录



- [基础模式 (basic)](#基础模式-basic)
- [完整模式 (complete)](#完整模式-complete)
- [头脑风暴模式 (brainstorm)](#头脑风暴模式-brainstorm)
- [渐进式模式 (progressive)](#渐进式模式-progressive)
- [Elicit 自动模式](#elicit-自动模式)

---

## 基础模式 (basic)



5 步快速收集，适合明确需求的用户。

### 步骤详情



| 步骤 | 键名 | 标题 | 验证规则 |
|------|------|------|----------|
| 1 | `skill_name` | 技能名称 | 必填，1-64字符，小写字母+数字+连字符 |
| 2 | `skill_function` | 主要功能 | 必填，简短描述 |
| 3 | `use_cases` | 使用场景 | 必填，列出2-3个场景 |
| 4 | `template_type` | 模板类型 | 必填，4选1 |
| 5 | `additional_features` | 额外需求 | 可选 |

### 适用场景



- 已清楚知道要创建什么技能
- 不需要复杂的技术规格
- 希望快速开始开发

### 示例对话

```python
# 基础模式使用示例（由 Agent-Skill 层编排）
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

---

## 完整模式 (complete)



10 步全面收集，包含所有技术细节。

### 步骤详情



基础模式 (1-5) + 额外步骤：

| 步骤 | 键名 | 标题 | 说明 |
|------|------|------|------|
| 6 | `target_users` | 目标用户 | 谁会使用这个技能 |
| 7 | `tech_stack` | 技术栈 | Python、Node.js 等 |
| 8 | `dependencies` | 外部依赖 | API、库、服务 |
| 9 | `testing_requirements` | 测试要求 | 单元测试、集成测试 |
| 10 | `documentation_level` | 文档级别 | 基础/完整/详细 |

### 适用场景



- 复杂技能，需要详细规划
- 团队协作，需要明确的规格
- 生产环境部署

### 示例对话

```python
# 完整模式使用示例（同基础模式，但 total_steps=10）
session = await create_requirement_session_tool(mode="complete")
# ... 后续流程同基础模式
```

---

## 头脑风暴模式 (brainstorm)



AI 引导的创意发散，探索技能可能性。

### 模式特点



- **开放性问题**：引导思考各种可能性
- **多角度探索**：从不同视角分析
- **记录想法**：保存所有创意
- **动态长度**：默认 5 轮对话

### 适用场景



- 只有模糊的想法
- 需要灵感启发
- 探索多种可能性

### 示例对话

```python
# 头脑风暴模式使用示例
session = await create_requirement_session_tool(mode="brainstorm")
conversation_history = []

for i in range(5):  # 默认5轮对话
    # 生成动态问题
    question = await generate_dynamic_question_tool(
        mode="brainstorm",
        answers=session["answers"],
        conversation_history=conversation_history
    )

    # 收集用户回答（由 Agent-Skill 层处理）
    answer = "<由用户提供的答案>"
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

### 注意事项



- 不强制要求填写所有字段
- 鼓励自由表达想法
- AI 会引导但不会限制

---

## 渐进式模式 (progressive)



快速开始，后续逐步完善。

### 模式特点



- **核心信息优先**：先收集关键信息
- **允许跳过**：非关键步骤可跳过
- **后续补充**：稍后可添加细节
- **动态长度**：根据需要调整

### 适用场景



- 快速原型开发
- 需求逐步明确
- 迭代式开发

### 示例对话

```python
# 渐进式模式使用示例
session = await create_requirement_session_tool(mode="progressive")

while True:
    # 根据已收集信息生成针对性问题
    question = await generate_dynamic_question_tool(
        mode="progressive",
        answers=session["answers"]
    )

    if not question.get("question"):
        break  # 没有更多问题

    # answer 由 Agent-Skill 层通过用户交互获取
    answer = "<由用户提供的答案>"
    await update_requirement_answer_tool(
        session_id=session["session_id"],
        question_key=question["question_key"],
        answer=answer
    )
```

### 与基础模式的区别



| 特性 | basic | progressive |
|------|-------|-------------|
| 必填步骤 | 全部 5 步 | 仅核心 2-3 步 |
| 可跳过 | ❌ | ✅ |
| 速度 | 中等 | 快 |
| 完整性 | 高 | 中 |

---

## Agent-Skill 层编排

**工作原理**：需求收集通过 Agent-Skill 工作流自动处理。

在新的7工具架构中，用户交互由 skill-creator Agent-Skill 自动管理，无需手动处理。

```python
# 新架构：使用 Agent-Skill (推荐)
# skill-creator 会自动处理用户交互和工作流编排

# 展示工作流概念：
session = await create_requirement_session_tool(mode="basic")
for i in range(session["total_steps"]):
    question = await get_static_question_tool(mode="basic", step_index=i)
    # Agent-Skill 层负责获取用户输入
    answer = "<由用户提供的答案>"
    await update_requirement_answer_tool(
        session_id=session["session_id"],
        question_key=question["key"],
        answer=answer
    )
```

**职责分工**：
- **MCP工具**：提供原子操作（创建会话、获取问题、验证答案等）
- **Agent-Skill**：编排工作流、处理用户交互、管理状态

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

## 相关文档



- **[需求澄清基础指南](requirement-collection-basics.md)** - 核心概念和快速开始
- **[需求收集 API 参考](requirement-collection-api.md)** - API 文档索引
- **[API 核心参考](requirement-collection-api-core.md)** - 完整的 API 技术文档
- **[API 使用示例](requirement-collection-api-examples.md)** - 实际使用场景和最佳实践
- **[需求收集示例](../examples/requirement-collection-basic.md)** - 代码示例
