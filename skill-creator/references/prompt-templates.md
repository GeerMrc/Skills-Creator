# Prompt 模板

本文档包含需求收集工作流中使用的Prompt模板。根据ADR 001架构原则，业务知识（包括Prompt模板）应在Agent-Skill中管理，MCP Server只提供原子操作。

## 需求完整性检查Prompt

用于检查需求收集是否完整，识别缺失信息。

**适用场景**: basic/complete模式结束时，检查是否收集到所有必要信息

**Prompt模板**:

```
分析以下技能创建需求，判断是否包含所有必要信息：

已收集的信息：
{answers}

必要信息包括：
1. skill_name - 技能名称
2. skill_function - 主要功能
3. use_cases - 使用场景
4. template_type - 模板类型

请返回 JSON 格式，包含：
- complete: bool（是否完整）
- missing_items: list[str]（缺失的信息列表）
- suggestions: list[str]（补充建议列表）

只返回 JSON，不要其他内容。
```

**变量说明**:
- `{answers}`: JSON格式的已收集答案

**返回格式**:
```json
{
  "complete": true,
  "missing_items": [],
  "suggestions": []
}
```

---

## 头脑风暴问题生成Prompt

用于在brainstorm模式下生成探索性问题。

**适用场景**: brainstorm/progressive模式，动态生成探索性问题

**Prompt模板**:

```
你是一个技能创建顾问，正在帮助用户通过头脑风暴方式探索技能需求。

{context}

请生成一个开放性的探索性问题，帮助用户深入思考他们的技能需求。问题应该：
1. 基于已收集的信息进行深入
2. 探索用户可能未曾考虑的角度
3. 鼓励创造性思考
4. 避免重复已问过的内容

请只返回问题文本，不要其他内容。
```

**变量说明**:
- `{context}`: 包含已收集答案和对话历史的上下文信息

**返回格式**:
```
一个开放性的探索性问题文本
```

---

## 使用方式

### 基本模式（使用MCP默认Prompt）

```python
# 直接调用MCP工具，无需传递prompt参数
result = await check_requirement_completeness_tool(ctx, answers={
    "skill_name": "my-skill",
    "skill_function": "数据验证"
})
```

### 自定义模式（高级用户）

```python
# 从模板文件加载Prompt
template = load_prompt_template("requirement-completeness")
prompt = template.format(answers=json.dumps(answers))

# 传递自定义Prompt
result = await check_requirement_completeness_tool(
    ctx,
    answers={...},
    prompt_template=prompt
)
```

---

## MCP工具参数说明

### check_requirement_completeness_tool

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| answers | dict[str, str] | ✅ | 已收集的答案 |
| prompt_template | str | ❌ | 自定义Prompt模板（可选） |

**默认行为**: 如果不提供prompt_template，MCP将使用内置默认Prompt（向后兼容）

---

## 相关文档

- [需求收集工作流指南](requirement-workflow.md)
- [MCP集成指南](mcp-tools-reference.md)
- [最佳实践 - 核心](best-practices-core.md)
