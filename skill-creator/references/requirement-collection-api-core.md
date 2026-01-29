# 需求收集 API 参考 - 核心

本文档提供需求收集功能的7个原子化MCP工具的核心API参考。

> **架构说明**：需求收集功能已重构为7个原子化工具，符合ADR 001架构原则。

> **相关文档**：
> - [需求澄清基础指南](requirement-collection-basics.md) - 核心概念和快速开始
> - [需求收集模式详解](requirement-collection-modes.md) - 各种模式详细说明
> - [API 使用示例](requirement-collection-api-examples.md) - 实际使用场景和最佳实践

## 目录

- [7个原子化工具](#7个原子化工具)
- [参数说明](#参数说明)
- [返回值](#返回值)
- [验证规则](#验证规则)
- [错误处理](#错误处理)

---

## 7个原子化工具

需求收集功能由以下7个独立的MCP工具提供：

### 1. create_requirement_session_tool

创建需求收集会话。

```
create_requirement_session_tool(
    mode: str = "basic",
    total_steps: int | None = None,
) -> dict[str, Any]
```

### 2. get_requirement_session_tool

获取会话状态。

```
get_requirement_session_tool(
    session_id: str,
) -> dict[str, Any]
```

### 3. update_requirement_answer_tool

更新答案。

```
update_requirement_answer_tool(
    session_id: str,
    question_key: str,
    answer: str,
) -> dict[str, Any]
```

### 4. get_static_question_tool

获取预定义问题（basic/complete模式）。

```
get_static_question_tool(
    mode: str,
    step_index: int,
) -> dict[str, Any]
```

### 5. generate_dynamic_question_tool

生成动态问题（brainstorm/progressive模式）。

```
generate_dynamic_question_tool(
    mode: str,
    answers: dict[str, str],
    conversation_history: list[dict] | None = None,
) -> dict[str, Any]
```

### 6. validate_answer_format_tool

验证答案格式。

```
validate_answer_format_tool(
    answer: str,
    validation: dict[str, Any],
) -> dict[str, Any]
```

### 7. check_requirement_completeness_tool

检查需求完整性。

```
check_requirement_completeness_tool(
    answers: dict[str, str],
) -> dict[str, Any]
```

---

## 参数说明

### mode

**类型**: `string`
**默认值**: `"basic"`
**可选值**: `basic` | `complete` | `brainstorm` | `progressive`

收集模式，详见 [需求收集模式详解](requirement-collection-modes.md)。

### session_id

**类型**: `string`
**默认值**: 自动生成 (格式: `uuid-xxxx`)

会话唯一标识符，用于恢复中断的会话。

---

## 返回值

### 成功响应

```python
{
    "success": True,              # 操作是否成功
    "session_id": str,            # 会话 ID
    "action": str,                # 执行的动作
    "mode": str,                  # 收集模式
    "current_step": {             # 当前步骤信息
        "key": str,               # 步骤键名
        "title": str,             # 步骤标题
        "prompt": str,            # 提示文本
        "required": bool,         # 是否必填
        "validation": dict,       # 验证规则
    },
    "step_index": int,            # 当前步骤索引（从 0 开始）
    "total_steps": int,           # 总步骤数
    "progress": float,            # 进度百分比（0-100）
    "answers": dict,              # 已收集的答案 {key: value}
    "message": str,               # 响应消息
    "completed": bool,            # 是否已完成收集
    "is_complete": bool,          # 需求是否完整（LLM 判断）
    "missing_info": list,         # 缺失的关键信息
    "suggestions": list,          # 补充建议
}
```

### 错误响应

```python
{
    "success": False,
    "error": str,                 # 错误消息
    "error_type": str,            # 错误类型
}
```

---

## 验证规则

每个步骤都有验证规则，确保输入质量。

### 必填验证

```python
{
    "field": "skill_name",
    "required": True,
    "help_text": "技能名称是必填项"
}
```

### 长度验证

```python
{
    "field": "skill_name",
    "min_length": 1,
    "max_length": 64,
    "help_text": "技能名称长度需要在 1-64 个字符之间"
}
```

### 格式验证

```python
{
    "field": "skill_name",
    "pattern": "^[a-z0-9]+(?:-[a-z0-9]+)*$",
    "help_text": "只能包含小写字母、数字和连字符"
}
```

### 选项验证

```python
{
    "field": "template_type",
    "options": ["minimal", "tool-based", "workflow-based", "analyzer-based"],
    "help_text": "请选择有效的模板类型"
}
```

---

## 错误处理

### 常见错误

| 错误 | 原因 | 解决方案 |
|------|------|----------|
| `Session not found` | 会话 ID 不存在 | 检查 session_id 是否正确，或使用 start 创建新会话 |
| `Validation failed` | 输入不符合验证规则 | 根据 help_text 修正输入 |
| `Empty required field` | 必填字段为空 | 提供非空输入 |

### 故障排除

**检查会话状态**:
```python
result = await get_requirement_session_tool(session_id="...")
print(result["answers"])
print(result["progress"])
```

**重新开始收集**:
```python
# 使用新的 session_id 或不指定（自动生成）
result = await create_requirement_session_tool(mode="basic")
```

---

## 相关文档

- **[API 使用示例](requirement-collection-api-examples.md)** - 实际使用场景和最佳实践
- **[需求澄清基础指南](requirement-collection-basics.md)** - 核心概念和快速开始
- **[需求收集模式详解](requirement-collection-modes.md)** - 各种模式详细说明
- **[MCP 集成指南](mcp-integration.md)** - MCP 工具使用和配置
