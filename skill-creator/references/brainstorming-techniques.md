# 头脑风暴模式指南

> **版本**: v0.3.4
> **更新日期**: 2026-01-29
> **架构说明**：需求收集基于 **7个原子化MCP工具 + Agent-Skill工作流编排** 的混合架构（符合ADR 001）。本文档展示Brainstorm模式的概念和用法，实际使用通过skill-creator Agent-Skill调用。

---

## 概述

头脑风暴（Brainstorm）模式是需求收集功能的一种收集模式，通过 `generate_dynamic_question_tool` 工具动态生成探索性问题，专注于通过**开放性探索**和**多角度思考**来帮助用户深入理解他们的技能需求。

### 与其他模式的区别



| 模式 | 特点 | 适用场景 |
|------|------|----------|
| **basic** | 5步预定义问题 | 快速收集基本信息 |
| **complete** | 10步预定义问题 | 全面收集需求信息 |
| **brainstorm** | LLM 动态生成探索性问题 | 需求不明确、创意探索阶段 |
| **progressive** | 根据已收集信息动态调整 | 渐进式需求完善 |

---

## 核心特性



### 1. LLM 驱动的动态问题生成



**传统问卷模式**：
```
Q1: 技能名称是什么？
Q2: 主要功能是什么？
Q3: 使用场景有哪些？
...
（固定顺序，固定问题）
```

**Brainstorm 模式**：
```
Q1: 您希望这个技能解决什么核心问题？
  [用户回答] → LLM 分析 →
Q2: 有没有考虑过从用户行为数据的角度来解决这个问题？
  [用户回答] → LLM 分析 →
Q3: 这个技能与现有的解决方案有什么独特之处？
...
（动态调整，根据上下文生成新问题）
```

### 2. 上下文感知



Brainstorm 模式会维护对话历史，并利用已收集的信息生成更深入的问题：

```python
# 已收集的信息


answers = {
    "skill_name": "data-visualizer",
    "core_problem": "复杂数据难以理解",
}

# LLM 基于上下文生成的问题


question = "您主要处理哪种类型的数据？是时序数据、地理数据还是其他？"
```

### 3. 开放式探索



不限制问题的类型和范围，鼓励用户思考：
- 技术可行性
- 用户痛点
- 竞争优势
- 未来扩展方向

---

## 使用方式



### 启动 Brainstorm 模式



```python
# 开始头脑风暴会话
session = await create_requirement_session_tool(mode="brainstorm")

# 获取第一个动态生成的问题
question = await generate_dynamic_question_tool(
    mode="brainstorm",
    answers={},
    conversation_history=[]
)

# 返回结果
{
    "question": "请描述您希望这个技能实现的核心价值...",
    "question_key": "brainstorm_0",
    "is_llm_generated": true
}
```

### 提供答案并继续



```python
# 提供答案，进入下一个问题
await update_requirement_answer_tool(
    session_id=session["session_id"],
    question_key="brainstorm_0",
    answer="我希望帮助非技术人员快速理解复杂数据"
)

# 获取下一个动态生成的问题
next_question = await generate_dynamic_question_tool(
    mode="brainstorm",
    answers=session["answers"],
    conversation_history=[{"question": "...", "answer": "我希望帮助非技术人员快速理解复杂数据"}]
)

# LLM 基于答案生成新的探索性问题
{
    "question": "您认为什么样的可视化方式最能帮助用户理解？是图表、热力图还是交互式探索？",
    "question_key": "brainstorm_1",
    "is_llm_generated": true
}
```

### 完成头脑风暴



```python
# 完成收集，获取总结
result = await get_requirement_session_tool(session_id=session["session_id"])

# 返回所有收集到的信息
{
    "session_id": "uuid-xxx",
    "mode": "brainstorm",
    "answers": {
        "brainstorm_0": "我希望帮助非技术人员快速理解复杂数据",
        "brainstorm_1": "交互式图表，支持数据钻取",
        "brainstorm_2": "主要面向业务分析师"
    },
    "completed": true
}

# 可选：检查完整性
completeness = await check_requirement_completeness_tool(answers=result["answers"])
```

---

## LLM 问题生成策略



### 提示词模板



```python
prompt = f"""你是一个技能创建顾问，正在帮助用户通过头脑风暴方式探索技能需求。

已收集的信息：
{context}

请生成一个开放性的探索性问题，帮助用户深入思考他们的技能需求。"""
```

### 温度参数



使用较高温度（0.8）产生多样化问题，LMM 调用失败时使用预定义备用问题。

---

## 最佳实践



### 1. 何时使用 Brainstorm 模式



✅ **适用场景**：
- 需求模糊，需要探索性讨论
- 创意型技能，需要多角度思考
- 不确定技术方案，需要头脑风暴
- 希望发现未曾考虑的需求点

❌ **不适用场景**：
- 需求明确，只需要快速收集
- 时间紧张，需要高效完成
- 有固定的需求模板

### 2. 如何获得最佳效果



**技巧 1：充分回答问题**
- 提供详细的答案，而不是简单的"是/否"
- 解释"为什么"，帮助 LLM 更好理解

**技巧 2：主动提出想法**
- 不局限于问题本身，主动提出相关想法
- 分享您对技能的愿景和期待

**技巧 3：保持开放心态**
- 欢迎意料之外的问题
- 考虑您未曾想到的方面

### 3. 对话长度建议



| 探索深度 | 建议轮次 | 说明 |
|----------|---------|------|
| 浅层探索 | 3-5 轮 | 快速了解核心需求 |
| 中等探索 | 5-10 轮 | 深入讨论多个方面 |
| 深度探索 | 10+ 轮 | 全面挖掘需求潜力 |

---

## 与 Progressive 模式的对比



| 特性 | Brainstorm 模式 | Progressive 模式 |
|------|-----------------|-----------------|
| **目标** | 开放式探索 | 渐进式完善 |
| **问题类型** | 创意性、多角度 | 结构化、针对性 |
| **LLM 温度** | 0.8（高创造性） | 0.3（更精准） |
| **问题生成** | 基于对话历史 | 基于缺失字段 |
| **适合阶段** | 需求发现阶段 | 需求整理阶段 |

**示例对比**：

```
# Brainstorm 模式


Q: 如果您的技能可以与其他工具集成，您最希望与哪类工具集成？
  → 探索可能性，鼓励创造性思考

# Progressive 模式


Q: 根据您的描述，这个技能需要处理哪类数据格式？
  → 基于已有信息，填补缺失细节
```

---

## 常见问题



### Q1: Brainstorm 模式会一直持续吗？



**A**: 不会。您可以随时：
- 使用 `action="complete"` 完成收集
- 设置轮次限制（推荐 5-10 轮）
- 当问题开始重复时完成

### Q2: 如何查看对话历史？



**A**: 使用 `get_requirement_session_tool` 查看当前会话状态和已收集的答案：

```python
result = await get_requirement_session_tool(session_id="my_session")

# 返回所有已收集的信息
{
    "session_id": "uuid-xxx",
    "mode": "brainstorm",
    "answers": {...},
    "current_step": 3,
    "status": "in_progress"
}
```

### Q3: Brainstorm 模式的答案如何映射到正式字段？



**A**: 在完成 Brainstorm 后，可以使用 Progressive 或 Complete 模式将探索性答案结构化：

```python
# 1. Brainstorm 模式探索


# 2. 整理关键信息


# 3. 使用 basic/complete 模式正式记录


```

---

## 参考资料



- **[主文档](requirement-collection.md)** - 需求澄清概述
- **[示例](../examples/requirement-collection-basic.md)** - 使用示例
- **[MCP 集成指南](mcp-integration.md)** - MCP 工具配置
