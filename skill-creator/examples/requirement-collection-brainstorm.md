# Brainstorm 模式使用示例

> **版本**: v0.3.0-alpha
> **工具**: `collect_requirements` - `brainstorm` 模式
> **用途**: 展示如何使用头脑风暴模式探索技能需求

---

## 示例场景

**目标**: 创建一个智能文档分析技能

**初始想法**: "我想做一个能分析文档的技能"

**使用 Brainstorm 模式**探索和完善这个想法。

---

## 完整对话流程

### 第 1 步：启动 Brainstorm 模式

```python
# 调用 collect_requirements 工具
await collect_requirements(
    ctx=ctx,
    action="start",
    mode="brainstorm",
    session_id="doc-analyzer-brainstorm"
)
```

**工具返回**：
```json
{
  "success": true,
  "session_id": "doc-analyzer-brainstorm",
  "action": "start",
  "mode": "brainstorm",
  "step_index": 0,
  "total_steps": 100,
  "progress": 0,
  "answers": {},
  "question": "请描述您希望这个技能实现的核心价值？它主要解决什么问题？",
  "is_dynamic_mode": true,
  "is_llm_generated": true,
  "message": "Brainstorm 模式 - 问题 1"
}
```

---

### 第 2 步：回答核心价值问题

```python
await collect_requirements(
    ctx=ctx,
    action="next",
    mode="brainstorm",
    session_id="doc-analyzer-brainstorm",
    user_input="帮助团队快速理解长篇技术文档的内容，提取关键决策和架构设计"
)
```

**LLM 基于答案生成下一个问题**：
```json
{
  "success": true,
  "question": "您提到要提取关键决策和架构设计，这些信息通常以什么形式出现在文档中？是设计文档、会议记录还是代码注释？",
  "is_llm_generated": true,
  "message": "Brainstorm 模式 - 问题 2"
}
```

---

### 第 3 步：继续探索 - 描述数据来源

```python
await collect_requirements(
    ctx=ctx,
    action="next",
    mode="brainstorm",
    session_id="doc-analyzer-brainstorm",
    user_input="主要是架构设计文档（ADR）和技术规范文档，有时也包括会议纪要"
)
```

**LLM 识别到新的探索方向**：
```json
{
  "success": true,
  "question": "对于架构决策文档，您最关心的是决策本身、决策背后的推理过程，还是决策的影响范围？",
  "is_llm_generated": true,
  "message": "Brainstorm 模式 - 问题 3"
}
```

---

### 第 4 步：深入分析 - 关心决策推理

```python
await collect_requirements(
    ctx=ctx,
    action="next",
    mode="brainstorm",
    session_id="doc-analyzer-brainstorm",
    user_input="最重要的是理解为什么做出某个技术选择，包括权衡考虑和替代方案"
)
```

**LLM 探索技术可行性**：
```json
{
  "success": true,
  "question": "您是否考虑过让这个技能能够跨文档关联相关决策？比如追踪某个技术选型在不同文档中的演变？",
  "is_llm_generated": true,
  "message": "Brainstorm 模式 - 问题 4"
}
```

---

### 第 5 步：创意探索 - 跨文档关联

```python
await collect_requirements(
    ctx=ctx,
    action="next",
    mode="brainstorm",
    session_id="doc-analyzer-brainstorm",
    user_input="这是个好主意！可以展示某个技术决策从提出到演变的完整时间线"
)
```

**LLM 探索用户体验**：
```json
{
  "success": true,
  "question": "对于展示决策时间线，您希望用户能够交互式探索，还是生成静态的可视化图表？",
  "is_llm_generated": true,
  "message": "Brainstorm 模式 - 问题 5"
}
```

---

### 第 6 步：明确交互方式

```python
await collect_requirements(
    ctx=ctx,
    action="next",
    mode="brainstorm",
    session_id="doc-analyzer-brainstorm",
    user_input="交互式更好，用户可以点击某个决策，查看相关的所有文档片段"
)
```

**LLM 探索差异化价值**：
```json
{
  "success": true,
  "question": "与现有的文档分析工具相比，您认为这个技能的独特优势是什么？是更好的上下文理解、更智能的关联推荐，还是更直观的可视化方式？",
  "is_llm_generated": true,
  "message": "Brainstorm 模式 - 问题 6"
}
```

---

### 第 7 步：完成头脑风暴

```python
# 收集了足够的信息，完成头脑风暴
await collect_requirements(
    ctx=ctx,
    action="complete",
    mode="brainstorm",
    session_id="doc-analyzer-brainstorm"
)
```

**工具返回所有收集到的信息**：
```json
{
  "success": true,
  "session_id": "doc-analyzer-brainstorm",
  "action": "complete",
  "mode": "brainstorm",
  "step_index": 6,
  "total_steps": 100,
  "progress": 30,
  "answers": {
    "answer_0": "帮助团队快速理解长篇技术文档的内容，提取关键决策和架构设计",
    "answer_1": "主要是架构设计文档（ADR）和技术规范文档，有时也包括会议纪要",
    "answer_2": "最重要的是理解为什么做出某个技术选择，包括权衡考虑和替代方案",
    "answer_3": "可以展示某个技术决策从提出到演变的完整时间线",
    "answer_4": "交互式更好，用户可以点击某个决策，查看相关的所有文档片段",
    "answer_5": "与现有工具相比，优势在于针对技术文档的专门理解和跨文档的智能关联"
  },
  "completed": true,
  "message": "BRAINSTORM 模式需求收集完成！",
  "is_dynamic_mode": true
}
```

---

## Brainstorm 模式输出分析

### 收集到的关键信息

| 方面 | 收集到的信息 | 原始想法的扩展 |
|------|-------------|---------------|
| **核心价值** | 提取关键决策和架构设计 | 从"分析文档"到"理解技术决策" |
| **数据来源** | ADR、技术规范、会议纪要 | 明确了具体文档类型 |
| **关注重点** | 决策背后的推理过程 | 不仅是"是什么"，更是"为什么" |
| **创新点** | 跨文档决策时间线 | 从单一文档到关联分析 |
| **交互方式** | 交互式探索 | 从静态报告到动态探索 |
| **差异化** | 针对技术文档的专门理解 | 明确了目标用户和场景 |

### 与原始想法的对比

| 维度 | 原始想法 | Brainstorm 后 | 提升 |
|------|---------|--------------|------|
| 功能范围 | 分析文档 | 提取决策+跨文档关联+时间线 | 3x |
| 目标用户 | 泛指"团队" | 技术团队、架构师 | 更精确 |
| 核心能力 | 文档分析 | 决策推理追踪 | 更深入 |
| 交互模式 | 未明确 | 交互式时间线探索 | 更具体 |

---

## 后续步骤

### 1. 将探索结果结构化

使用 `basic` 或 `complete` 模式将头脑风暴的结果整理为正式的技能规格：

```python
# 开始正式的需求收集
await collect_requirements(
    ctx=ctx,
    action="start",
    mode="complete",
    session_id="doc-analyzer-formal"
)

# 第一个问题：技能名称
→ "doc-decision-tracker"

# 第二个问题：主要功能
→ "提取、关联和可视化技术决策及其演变过程"
...
```

### 2. 选择合适的模板类型

基于头脑风暴的发现，选择 `workflow-based` 模板：
- 需要多步骤处理（提取→关联→可视化）
- 需要复杂的数据流管理
- 需要交互式输出

---

## 最佳实践总结

### DO - 推荐做法

✅ **充分表达想法**
```
好的回答：
"我希望用户能够点击某个决策，看到它在不同文档中被如何讨论，
包括最初的提议、反对意见、最终决策以及后续的调整"

不好的回答：
"支持点击查看"
```

✅ **主动提出新想法**
```
用户主动：
"我还希望能够标记决策之间的依赖关系，
比如某个基础设施的改变影响了哪些后续决策"

→ LLM 可以基于这个新方向继续探索
```

✅ **保持开放心态**
```
LLM: "您考虑过支持自然语言查询吗？比如'上个月有哪些关于数据库的决策？"

用户：欢迎意料之外的问题
→ "这个想法不错，可以作为一个高级功能"
```

### DON'T - 避免做法

❌ **过早收敛**
```
问题：您希望这个技能支持哪些文档格式？
过早的回答："就 Markdown 和 PDF"

更好：先探索不同格式的不同价值，再决定优先级
```

❌ **限制思维**
```
问题：这个技能可以有哪些创新点？
限制性的回答："就像现有的文档工具那样"

更好：描述现有工具的不足，探索突破方向
```

---

## 不同 Brainstorm 风格示例

### 风格 1：技术探索型

```
用户：关注技术实现细节
LLM：生成技术可行性问题
→ 适合技术导向的技能
```

### 风格 2：用户中心型

```
用户：关注用户需求和痛点
LLM：生成用户体验问题
→ 适合面向最终用户的技能
```

### 风格 3：创意发散型

```
用户：鼓励创新想法
LLM：生成"如果...会怎样"类型的问题
→ 适合创新型、实验性技能
```

---

## 参考资料

- **指南文档**: `references/brainstorming-techniques.md`
- **基础示例**: `examples/requirement-collection-basic.md`
- **工具实现**: `skill-creator-mcp/src/skill_creator_mcp/server.py`

---

**示例创建**: 2026-01-23
**文档版本**: v0.3.0-alpha
