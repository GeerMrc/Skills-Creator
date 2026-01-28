# 需求收集工作流指南

> **文档版本**: v1.0.0
> **创建日期**: 2026-01-28
> **适用范围**: Agent-Skill 需求收集工作流编排

---

## 工作流概述

需求收集工作流由 Agent-Skill 编排，调用 MCP 原子工具完成。

**架构原则**（符合 ADR 001）：
- **MCP Server**: 只提供原子操作工具（会话CRUD、问题生成、答案验证、LLM调用）
- **Agent-Skill**: 编排工作流程、传递最佳实践、提供渐进式披露

---

## 模式1：基础模式（Basic Mode - 5步）

### 工作流程

```yaml
1. 调用 create_requirement_session(mode="basic")
   → 返回: session_id, total_steps=5

2. 循环直到完成：
   a. 调用 get_static_question(mode="basic", step_index=i)
      → 返回: question_key, question_text, validation

   b. 向用户展示问题

   c. 获取用户输入

   d. 调用 validate_answer_format(answer, validation)
      → 返回: valid, error, formatted_answer

   e. 如果验证失败：
      - 显示错误信息
      - 返回步骤 c

   f. 调用 update_requirement_answer(session_id, question_key, answer)
      → 返回: success, updated

   g. i += 1

3. 调用 check_requirement_completeness(answers)
   → 返回: complete, missing_items, suggestions

4. 结合最佳实践知识，提供可执行建议
```

### 示例对话

**用户**: "帮我收集需求"

**Agent-Skill**:
1. 创建会话: `create_requirement_session(mode="basic")`
2. 获取第一个问题: `get_static_question(mode="basic", step_index=0)`
3. 展示问题: "请输入技能名称（小写字母、数字、连字符，如：pdf-parser、git-helper）"
4. 等待用户输入...
5. 验证答案: `validate_answer_format(answer, validation)`
6. 保存答案: `update_requirement_answer(session_id, "skill_name", answer)`
7. 重复步骤 2-6，直到完成 5 个问题
8. 检查完整性: `check_requirement_completeness(answers)`
9. 提供建议: "根据您的需求，建议使用 tool-based 模板..."

---

## 模式2：完整模式（Complete Mode - 10步）

### 工作流程

与基础模式相同，但 `total_steps=10`，包含更多问题：

1. 基础问题（5个）：skill_name, skill_function, use_cases, template_type, additional_features
2. 额外问题（5个）：target_users, tech_stack, dependencies, testing_requirements, documentation_level

### 调用方式

```yaml
create_requirement_session(mode="complete")
→ 返回: session_id, total_steps=10
```

---

## 模式3：动态模式（Brainstorm/Progressive）

### 3.1 Brainstorm 模式（头脑风暴）

**特点**: 开放式探索，无固定步骤数

```yaml
1. 调用 create_requirement_session(mode="brainstorm")
   → 返回: session_id, total_steps=100（虚拟值）

2. 循环（默认5轮）：
   a. 调用 generate_dynamic_question(
         mode="brainstorm",
         answers=当前答案,
         conversation_history=对话历史
      )
      → 返回: question_key, question_text, is_llm_generated

   b. 向用户展示开放性问题

   c. 获取用户输入

   d. 调用 update_requirement_answer(session_id, question_key, answer)

   e. 更新对话历史（包含用户输入）

3. 调用 check_requirement_completeness(answers)

4. 提供探索性建议
```

**示例问题**:
- "这个技能的核心价值主张是什么？"
- "它与现有解决方案有什么不同？"
- "用户最痛的场景是什么？"

### 3.2 Progressive 模式（渐进式）

**特点**: 根据已收集信息自适应生成问题

```yaml
1. 调用 create_requirement_session(mode="progressive")

2. 循环直到完成：
   a. 调用 generate_dynamic_question(
         mode="progressive",
         answers=当前答案
      )
      → LLM 分析缺失信息，生成针对性问题

   b. 展示问题并获取答案

   c. 调用 validate_answer_format() 验证

   d. 调用 update_requirement_answer() 保存

3. 检查完整性并提供建议
```

**示例问题序列**:
1. "请提供技能名称"（缺少 skill_name）
2. "请描述这个技能的主要功能"（缺少 skill_function）
3. "请描述这个技能的使用场景"（缺少 use_cases）
4. "选择技能模板类型：minimal、tool-based、workflow-based、analyzer-based"（缺少 template_type）
5. "这个技能的目标用户是谁？"（基本信息齐全，深入挖掘）

---

## 最佳实践

### 1. 验证失败处理

```yaml
当 validate_answer_format() 返回 valid=False 时：
- 清晰显示错误信息
- 提供正确格式示例
- 允许用户重新输入
- 不推进到下一个问题
```

**示例**:
```
❌ 输入验证失败: 技能名称只能包含小写字母、数字和连字符
正确示例: pdf-parser, git-helper, data-analyzer
请重新输入：
```

### 2. 动态模式问题类型

**Brainstorm 模式**:
- 使用开放性问题
- 鼓励创造性思考
- 探索用户可能未曾考虑的角度

**Progressive 模式**:
- 使用针对性问题
- 基于已收集信息确定下一步
- 优先补充缺失的关键信息

### 3. 完成时检查

**必需信息**:
1. `skill_name` - 技能名称
2. `skill_function` - 主要功能
3. `use_cases` - 使用场景
4. `template_type` - 模板类型

**检查方法**:
```yaml
调用 check_requirement_completeness(answers)
→ 返回: complete, missing_items, suggestions

如果 complete=False:
- 显示缺失信息列表
- 提供补充建议
- 可选择继续补充或基于现有信息生成建议
```

### 4. 结合最佳实践知识

Agent-Skill 应根据收集到的需求，结合 references/ 中的最佳实践知识，提供可执行建议：

```yaml
示例：
如果 template_type="tool-based":
  → 建议: "您的技能将封装现有工具，建议在 SKILL.md 中明确列出工具依赖"

如果 use_cases 包含 "文件处理":
  → 建议: "考虑添加 Glob 和 Grep 工具来支持文件操作"

如果 additional_features 包含 "错误处理":
  → 建议: "建议在 examples/ 中添加错误处理示例"
```

---

## Prompt 模板管理

根据 ADR 001 架构原则，业务知识（包括 Prompt 模板）应在 Agent-Skill 中管理，MCP Server 只提供原子操作。

### Prompt 模板位置

**主文档**: [`prompt-templates.md`](prompt-templates.md)

包含完整的 Prompt 模板定义和使用说明。

### 使用方式

**基本模式**（使用 MCP 默认 Prompt）:
```python
# 直接调用 MCP 工具，无需传递 prompt 参数
result = await check_requirement_completeness_tool(ctx, answers={
    "skill_name": "my-skill",
    "skill_function": "数据验证"
})
```

**自定义模式**（高级用户）:
```python
# 从模板文件加载 Prompt
template = load_prompt_template("requirement-completeness")
prompt = template.format(answers=json.dumps(answers))

# 传递自定义 Prompt
result = await check_requirement_completeness_tool(
    ctx,
    answers={...},
    prompt_template=prompt
)
```

### 可用 Prompt 模板

| 模板名称 | 用途 | 适用场景 |
|---------|------|----------|
| `requirement-completeness` | 检查需求完整性 | basic/complete 模式结束时 |
| `brainstorm-question` | 生成探索性问题 | brainstorm/progressive 模式 |

### MCP 工具参数说明

**check_requirement_completeness_tool**:
- `answers`: dict[str, str] (必填) - 已收集的答案
- `prompt_template`: str (可选) - 自定义 Prompt 模板

**默认行为**: 如果不提供 `prompt_template`，MCP 将使用内置默认 Prompt（向后兼容）。

---

## MCP 原子工具列表

| 工具 | 功能 | 返回值 |
|------|------|--------|
| `create_requirement_session` | 创建新会话 | session_id, mode, total_steps, current_step |
| `get_requirement_session` | 获取会话状态 | mode, current_step, answers, completed |
| `update_requirement_answer` | 更新答案 | success, updated, current_step |
| `get_static_question` | 获取静态问题 | question_key, question_text, validation |
| `generate_dynamic_question` | 生成动态问题 | question_key, question_text, is_llm_generated |
| `validate_answer_format` | 验证答案格式 | valid, error, formatted_answer |
| `check_requirement_completeness` | 检查完整性 | complete, missing_items, suggestions |

---

## 错误处理

### 会话不存在

```yaml
调用 get_requirement_session(session_id) 时：
- 如果返回 success=False，error="会话不存在"
- 提示用户: "会话已过期，请重新开始"
- 返回步骤 1（创建新会话）
```

### LLM 调用失败

```yaml
generate_dynamic_question() 或 check_requirement_completeness() 失败时：
- 自动降级到预定义问题/简单检查
- 返回 fallback=True
- 继续工作流，不中断用户
```

---

## 完整示例（Basic Mode）

```python
# Agent-Skill 伪代码
async def collect_requirements_basic_mode():
    # 1. 创建会话
    session = await create_requirement_session(mode="basic")
    session_id = session["session_id"]
    answers = {}

    # 2. 循环收集
    for i in range(5):  # total_steps=5
        # 获取问题
        question = await get_static_question(mode="basic", step_index=i)
        question_key = question["question_key"]
        question_text = question["question_text"]
        validation = question["validation"]

        # 展示问题并获取答案
        print(f"问题 {i+1}/5: {question_text}")
        answer = await get_user_input()

        # 验证答案
        validate_result = await validate_answer_format(answer, validation)
        while not validate_result["valid"]:
            print(f"验证失败: {validate_result['error']}")
            answer = await get_user_input()
            validate_result = await validate_answer_format(answer, validation)

        # 保存答案
        await update_requirement_answer(session_id, question_key, answer)
        answers[question_key] = answer

    # 3. 检查完整性
    completeness = await check_requirement_completeness(answers)

    # 4. 提供建议
    return {
        "answers": answers,
        "complete": completeness["complete"],
        "suggestions": completeness["suggestions"],
    }
```

---

**文档维护**: 请在架构变更后更新本文档。
**最后更新**: 2026-01-28 (v1.0.0 - 架构重构后创建)
