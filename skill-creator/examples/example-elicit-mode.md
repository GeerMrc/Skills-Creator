# Elicit 自动模式使用示例

本文档展示如何使用需求收集功能的 Elicit 模式一键完成需求收集。

## 概述

Elicit 模式 (use_elicit=True) 通过 AI 自动调用 `ctx.elicit()` 一键完成所有输入收集：

- **自动化**：无需手动调用 action="next"
- **验证重试**：输入无效时自动重新请求
- **状态保存**：每步后自动保存会话状态
- **取消友好**：用户可随时取消

预计时间：1-2 分钟

---

## 基本用法

### 一键完成所有收集

**请求**:
```json
{
  "action": "start",
  "mode": "basic",
  "use_elicit": true
}
```

**后台行为**:
1. AI 自动调用 `ctx.elicit()`
2. 显示："请输入技能名称" → 等待输入
3. 验证输入 → 保存状态
4. 显示："请描述主要功能" → 等待输入
5. ... (继续所有步骤)
6. 返回完整结果

---

## 用户交互流程

Elicit 模式自动完成5步收集，每步验证并保存：

```
步骤1: 请输入技能名称（小写字母、数字、连字符）
输入: "pdf-helper"
→ ✓ 已保存：skill_name = pdf-helper

步骤2: 请简要描述技能的主要功能
输入: "解析 PDF 文件，提取文本和图片"
→ ✓ 已保存：skill_function = 解析 PDF 文件，提取文本和图片

步骤3: 请列出技能的主要使用场景
输入: "文档分析、数据提取、内容归档"
→ ✓ 已保存：use_cases = 文档分析、数据提取、内容归档

步骤4: 请选择模板类型（minimal, tool-based, workflow-based, analyzer-based）
输入: "tool-based"
→ ✓ 已保存：template_type = tool-based

步骤5: 是否有额外需求？（可选）
输入: "支持 OCR 文字识别"
→ ✓ 已保存：additional_features = 支持 OCR 文字识别

✅ 需求收集完成！进度：100% (5/5)
```

---

## 自动完成结果

**最终响应**:
```json
{
  "success": true,
  "completed": true,
  "progress": 100.0,
  "answers": {
    "skill_name": "pdf-helper",
    "skill_function": "解析 PDF 文件，提取文本和图片",
    "use_cases": "文档分析、数据提取、内容归档",
    "template_type": "tool-based",
    "additional_features": "支持 OCR 文字识别"
  },
  "is_complete": true,
  "suggestions": [
    "考虑添加 PDF 元数据提取功能",
    "可以支持加密 PDF 的处理"
  ]
}
```

---

## 错误自动重试

### 格式验证

输入 `Invalid_Skill_Name`：
```
❌ 格式错误：只能包含小写字母、数字和连字符
请重新输入技能名称
```
修正为 `pdf-helper` 后自动继续。

### 必填验证

输入空字符串：
```
❌ 技能名称是必填项
请重新输入技能名称
```
输入有效值后自动继续。

---

## 用户取消

用户中途取消时：
```
⚠️ 用户取消了输入

已收集信息（可继续使用）：
- skill_name: pdf-helper
- skill_function: 解析 PDF 文件

状态：cancelled
已收集信息已保存，可以随时恢复
```

---

## 不同模式使用 Elicit

| 模式 | 步骤数 | 用途 |
|------|--------|------|
| `basic` | 5 | 核心信息收集 |
| `complete` | 10 | 完整信息收集 |
| `brainstorm` | 5轮 | 开放性创意发散 |
| `progressive` | 可变 | 快速原型，可跳过 |

所有模式都支持 `use_elicit: true` 参数。

---

## 最佳实践

1. **检查客户端支持**：确保客户端支持 `ctx.elicit()` API
2. **提供清晰提示**：在开始前说明会自动收集所有输入
3. **处理取消**：用户取消时，已收集信息不会丢失
4. **利用重试机制**：验证失败时自动重试，无需手动处理

---

## 限制说明

### 客户端要求

Elicit 模式需要客户端支持 `ctx.elicit()` API：
- FastMCP 3.0+
- 支持 MCP 协议的用户输入功能

### 回退模式

如果客户端不支持，自动回退到传统模式：

```json
{
  "success": true,
  "message": "Elicit 模式不可用，已切换到传统模式",
  "fallback_mode": true
}
```

---

## 模式对比

| 特性 | 传统模式 | Elicit 模式 |
|------|----------|------------|
| 调用次数 | 多次（每步一次） | 一次 |
| 用户交互 | 手动传递 user_input | AI 自动调用 elicit |
| 状态管理 | 手动管理 session_id | 自动保存每步 |
| 示例调用 | `{"action": "next", "user_input": "..."}` | `{"action": "start", "use_elicit": true}` |

---

## 代码示例

### 检查 Elicit 支持

```python
# 注意：根据新的架构设计，需求收集通过Agent-Skill工作流编排
# 以下展示如何使用7个原子化MCP工具

# 步骤1：创建需求收集会话
session_result = await create_requirement_session_tool(
    ctx=ctx,
    mode="basic"
)
session_id = session_result["session_id"]

# 步骤2：获取第一个问题
question = await get_static_question_tool(
    ctx=ctx,
    mode="basic",
    step_index=0
)

# 步骤3：循环收集用户输入（通过Agent-Skill工作流编排）
# Elicit模式下，Agent-Skill会自动调用ctx.elicit()收集所有输入
# 这里展示的是手动模式，实际使用时通过skill-creator Agent-Skill调用

# 步骤4：验证每个答案
for step_index in range(5):  # basic模式有5个步骤
    question = await get_static_question_tool(ctx=ctx, mode="basic", step_index=step_index)
    user_input = await ctx.elicit(question["prompt"])  # 自动获取用户输入

    # 验证输入格式
    validation = question.get("validation", {})
    is_valid = await validate_answer_format_tool(
        ctx=ctx,
        answer=user_input,
        validation=validation
    )

    if not is_valid["valid"]:
        # 处理验证错误
        continue

    # 保存答案
    await update_requirement_answer_tool(
        ctx=ctx,
        session_id=session_id,
        question_key=question["key"],
        answer=user_input
    )

# 步骤5：检查完整性
completeness = await check_requirement_completeness_tool(
    ctx=ctx,
    answers=collected_answers
)
```

---

## 相关文档

- **[基础模式示例](example-basic-mode.md)** - 传统手动模式
- **[完整模式示例](example-complete-mode.md)** - 10 步收集
- **[渐进模式示例](example-progressive-mode.md)** - 快速原型
- **[需求收集模式详解](../references/requirement-collection-modes.md)** - 模式对比
- **[需求收集工作流](../references/requirement-workflow.md)** - 客户端限制和回退机制说明
