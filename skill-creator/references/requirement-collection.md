# 需求澄清指南

## 概述

Skill-Creator 提供 AI 驱动的需求澄清工具 `collect_requirements`，通过对话式交互逐步收集技能创建所需信息。该工具支持会话状态管理，允许中断后恢复，并提供实时进度跟踪。

> **示例代码**：查看 [需求收集示例](../examples/requirement-collection-basic.md) 获取完整的代码示例和用法。

## 核心概念

### 会话状态管理

`collect_requirements` 使用 FastMCP 的 Context API 管理会话状态：

- **状态存储**：通过 `ctx.get_state()` 和 `ctx.set_state()` 持久化会话
- **自动恢复**：中断后可从上次步骤继续
- **会话隔离**：不同会话互不影响

### AI 驱动引导

使用 LLM 动态生成问题和引导对话：

- **智能采样**：通过 `ctx.sample()` 获取 AI 生成的响应
- **上下文感知**：根据已收集信息调整后续问题
- **完整性检查**：使用 LLM 判断需求是否完整

### 输入验证

实时验证用户输入：

- **格式检查**：正则表达式、长度限制
- **选项验证**：确保输入在可选项范围内
- **即时反馈**：错误时返回具体帮助文本

## 收集模式

### 基础模式 (basic)

5 步快速收集，适合明确需求的用户：

| 步骤 | 键名 | 标题 |
|------|------|------|
| 1 | `skill_name` | 技能名称 |
| 2 | `skill_function` | 主要功能 |
| 3 | `use_cases` | 使用场景 |
| 4 | `template_type` | 模板类型 |
| 5 | `additional_features` | 额外需求 |

### 完整模式 (complete)

10 步全面收集，包含所有技术细节：

基础模式 + 以下额外步骤：

| 步骤 | 键名 | 标题 |
|------|------|------|
| 6 | `target_users` | 目标用户 |
| 7 | `tech_stack` | 技术栈 |
| 8 | `dependencies` | 外部依赖 |
| 9 | `testing_requirements` | 测试要求 |
| 10 | `documentation_level` | 文档级别 |

### 头脑风暴模式 (brainstorm)

AI 引导的创意发散，探索技能可能性：

- 开放性问题引导思考
- 鼓励多角度探索
- 记录所有想法

### 渐进式模式 (progressive)

快速开始，后续逐步完善：

- 核心信息优先
- 允许跳过非关键步骤
- 后续可补充细节

## 工具参数

### collect_requirements

```python
@mcp.tool()
async def collect_requirements(
    ctx: Context,
    action: str = "start",
    mode: str = "basic",
    session_id: str | None = None,
    user_input: str | None = None,
) -> dict[str, Any]
```

**参数说明**：

| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `action` | string | "start" | 执行动作：start/next/previous/status/complete |
| `mode` | string | "basic" | 收集模式：basic/complete/brainstorm/progressive |
| `session_id` | string | auto | 会话 ID（自动生成） |
| `user_input` | string | None | 用户输入（用于 next/complete 动作） |

**返回值**：

```python
{
    "success": bool,           # 操作是否成功
    "session_id": str,         # 会话 ID
    "action": str,             # 执行的动作
    "mode": str,               # 收集模式
    "current_step": dict,      # 当前步骤信息
    "step_index": int,         # 当前步骤索引（从 0 开始）
    "total_steps": int,        # 总步骤数
    "progress": float,         # 进度百分比（0-100）
    "answers": dict,           # 已收集的答案
    "message": str,            # 响应消息
    "completed": bool,         # 是否已完成收集
    "is_complete": bool,       # 需求是否完整（LLM 判断）
    "missing_info": list,      # 缺失的关键信息
    "suggestions": list,       # 补充建议
    "error": str | None        # 错误信息
}
```

## Action 类型

### start

开始新的需求收集会话。

```json
{
  "action": "start",
  "mode": "basic"
}
```

**响应**：返回第一个步骤的问题。

### next

进入下一步，需要提供 `user_input`。

```json
{
  "action": "next",
  "session_id": "xxx",
  "user_input": "my-skill-name"
}
```

**行为**：
1. 验证当前步骤的输入
2. 保存答案到会话状态
3. 返回下一步的问题

### previous

返回上一步，允许修改之前的答案。

```json
{
  "action": "previous",
  "session_id": "xxx"
}
```

**行为**：
1. 回退一步
2. 清除当前步骤的答案
3. 返回上一步的问题

### status

查询当前会话状态。

```json
{
  "action": "status",
  "session_id": "xxx"
}
```

**响应**：返回当前进度、已收集答案、完成状态。

### complete

完成收集并生成最终报告。

```json
{
  "action": "complete",
  "session_id": "xxx"
}
```

**行为**：
1. 使用 LLM 检查需求完整性
2. 返回缺失信息列表
3. 提供补充建议

## 验证规则

每个步骤都有验证规则，确保输入质量：

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

## 完整性检查

`_check_requirement_completeness` 函数使用 LLM 分析已收集的信息：

**检查维度**：
1. **信息完整性**：是否缺少关键信息
2. **逻辑一致性**：各项需求是否相互矛盾
3. **可实施性**：技术方案是否可行

**返回内容**：
- `is_complete`: 需求是否完整
- `missing_info`: 缺失信息列表
- `suggestions`: 补充建议列表

## 使用场景

### 场景 1：快速创建技能

```python
# 1. 开始基础模式收集
result = await collect_requirements(
    action="start",
    mode="basic"
)

# 2. 逐个回答问题
result = await collect_requirements(
    action="next",
    session_id=result["session_id"],
    user_input="pdf-parser"
)

# 3. 完成收集
result = await collect_requirements(
    action="complete",
    session_id=result["session_id"]
)

# 4. 使用收集的信息初始化技能
await init_skill(
    name=result["answers"]["skill_name"],
    template=result["answers"]["template_type"]
)
```

### 场景 2：中断后恢复

```python
# 用户在第 3 步中断...

# 恢复会话
result = await collect_requirements(
    action="status",
    session_id="previous_session_id"
)

# 从第 3 步继续
result = await collect_requirements(
    action="next",
    session_id="previous_session_id",
    user_input="..."
)
```

### 场景 3：修改之前答案

```python
# 用户想修改第 2 步的答案
result = await collect_requirements(
    action="previous",
    session_id="current_session_id"
)

# 重新输入第 2 步的答案
result = await collect_requirements(
    action="next",
    session_id="current_session_id",
    user_input="corrected_answer"
)
```

## 最佳实践

### 1. 选择合适的模式

- **明确需求** → 使用 `basic` 模式
- **复杂技能** → 使用 `complete` 模式
- **探索想法** → 使用 `brainstorm` 模式
- **快速原型** → 使用 `progressive` 模式

### 2. 提供清晰的用户输入

确保 `user_input` 简洁明确：

```python
# 好的输入
user_input="pdf-parser"

# 不好的输入
user_input="嗯，我想做一个解析 PDF 的工具，名字叫 pdf-parser 吧..."
```

### 3. 利用完整性检查

完成收集后检查 `is_complete` 和 `missing_info`：

```python
result = await collect_requirements(action="complete", session_id=...)

if not result["is_complete"]:
    print("缺失信息：", result["missing_info"])
    print("建议：", result["suggestions"])
```

### 4. 保存会话 ID

会话 ID 是恢复会话的唯一标识，需妥善保存。

### 5. 处理验证错误

捕获验证错误并提供友好提示：

```python
if not result["success"]:
    print(result["error"])
    # 根据错误类型引导用户修正
```

## 错误处理

### 常见错误

| 错误 | 原因 | 解决方案 |
|------|------|----------|
| `Invalid action` | Action 类型无效 | 使用有效的 action：start/next/previous/status/complete |
| `Session not found` | 会话 ID 不存在 | 检查 session_id 是否正确，或使用 start 创建新会话 |
| `Validation failed` | 输入不符合验证规则 | 根据 help_text 修正输入 |
| `Empty required field` | 必填字段为空 | 提供非空输入 |

### 故障排除

**检查会话状态**：
```python
result = await collect_requirements(action="status", session_id="...")
print(result["answers"])
print(result["progress"])
```

**重新开始收集**：
```python
# 使用新的 session_id 或不指定（自动生成）
result = await collect_requirements(action="start", mode="basic")
```

## 技术实现

### SessionState 模型

```python
class SessionState(BaseModel):
    current_step_index: int = 0
    answers: dict[str, str] = Field(default_factory=dict)
    started_at: str | None = None
    completed: bool = False
    mode: RequirementCollectionMode = "basic"
    total_steps: int = 0
```

### 状态持久化

```python
# 保存状态
await ctx.set_state(session_state.model_dump())

# 恢复状态
stored_state = await ctx.get_state()
if stored_state:
    session_state = SessionState.model_validate(stored_state)
```

### 进度计算

```python
progress = (current_step_index / total_steps) * 100
```

## 相关文档

- **[MCP 集成指南](mcp-integration.md)** - MCP 工具使用和配置
- **[需求收集示例](../examples/requirement-collection-basic.md)** - 完整代码示例
- **[最佳实践](best-practices-core.md)** - Agent-Skill 开发规范
- **[验证规范](validation.md)** - 技能验证规则
