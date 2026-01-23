# Elicit 自动模式使用示例

本文档展示如何使用 `collect_requirements` 的 Elicit 模式一键完成需求收集。

## 概述

Elicit 模式 (use_elicit=True) 通过 AI 自动调用 `ctx.elicit()` 一键完成所有输入收集：

- **自动化**：无需手动调用 action="next"
- **验证重试**：输入无效时自动重新请求
- **状态保存**：每步后自动保存会话状态
- **取消友好**：用户可随时取消

预计时间：1-2 分钟

---

## 模式对比

| 特性 | 传统模式 | Elicit 模式 |
|------|----------|------------|
| 调用次数 | 多次（每步一次） | 一次 |
| 用户交互 | 手动传递 user_input | AI 自动调用 elicit |
| 状态管理 | 手动管理 session_id | 自动保存每步 |
| 中断恢复 | 需要保存 session_id | 自动保存 |
| 适用场景 | 需要精细控制 | 快速完成需求收集 |

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

### 步骤 1：开始 Elicit 模式

**用户**: "开始收集需求"

**助手**:
```
请输入技能名称（小写字母、数字、连字符）
```

### 步骤 2：用户输入技能名称

**用户**: "pdf-helper"

**助手**:
```
✓ 已保存：skill_name = pdf-helper

请简要描述技能的主要功能
```

### 步骤 3：用户输入主要功能

**用户**: "解析 PDF 文件，提取文本和图片"

**助手**:
```
✓ 已保存：skill_function = 解析 PDF 文件，提取文本和图片

请列出技能的主要使用场景
```

### 步骤 4-5：继续输入

**用户**: "文档分析、数据提取、内容归档"

**助手**:
```
✓ 已保存：use_cases = 文档分析、数据提取、内容归档

请选择模板类型（minimal, tool-based, workflow-based, analyzer-based）
```

**用户**: "tool-based"

**助手**:
```
✓ 已保存：template_type = tool-based

是否有额外需求？（可选）
```

**用户**: "支持 OCR 文字识别"

**助手**:
```
✓ 已保存：additional_features = 支持 OCR 文字识别

✅ 需求收集完成！
进度：100% (5/5)
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

### 格式错误自动重试

**用户**: "Invalid_Skill_Name"

**助手**:
```
❌ 格式错误：只能包含小写字母、数字和连字符

请重新输入技能名称（小写字母、数字、连字符）
```

**用户**: "pdf-helper" (修正后)

**助手**:
```
✓ 已保存：skill_name = pdf-helper

继续下一步...
```

### 空输入自动重试

**用户**: "" (空字符串)

**助手**:
```
❌ 技能名称是必填项

请重新输入技能名称
```

---

## 用户取消

### 用户中途取消

**用户**: [在步骤 3 取消]

**助手**:
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

### Basic 模式 + Elicit

```json
{
  "action": "start",
  "mode": "basic",
  "use_elicit": true
}
```

5 个步骤自动收集。

### Complete 模式 + Elicit

```json
{
  "action": "start",
  "mode": "complete",
  "use_elicit": true
}
```

10 个步骤自动收集。

### Brainstorm 模式 + Elicit

```json
{
  "action": "start",
  "mode": "brainstorm",
  "use_elicit": true
}
```

默认 5 轮开放性问题。

### Progressive 模式 + Elicit

```json
{
  "action": "start",
  "mode": "progressive",
  "use_elicit": true
}
```

核心信息优先，可跳过。

---

## 最佳实践

### 1. 检查客户端支持

确保客户端支持 `ctx.elicit()` API。

### 2. 提供清晰提示

在开始前说明会自动收集所有输入。

### 3. 处理取消

用户取消时，已收集信息不会丢失。

### 4. 利用重试机制

验证失败时自动重试，无需手动处理。

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

## 完整示例对比

### 传统模式（多次调用）

```json
// 步骤 1
{"action": "start", "mode": "basic"}
// → 返回第一个问题

// 步骤 2
{"action": "next", "session_id": "...", "user_input": "pdf-helper"}
// → 返回第二个问题

// 步骤 3-5
{"action": "next", "session_id": "...", "user_input": "..."}
// → 继续问题

// 步骤 6
{"action": "complete", "session_id": "..."}
// → 完成收集
```

### Elicit 模式（一次调用）

```json
// 一步完成
{"action": "start", "mode": "basic", "use_elicit": true}
// → 自动收集所有输入
// → 返回完整结果
```

---

## 代码示例

### 检查 Elicit 支持

```python
# 检查客户端能力
capabilities = await check_client_capabilities()

if capabilities["supports_elicitation"]:
    # 使用 Elicit 模式
    result = await collect_requirements(
        action="start",
        mode="basic",
        use_elicit=True
    )
else:
    # 回退到传统模式
    result = await collect_requirements(
        action="start",
        mode="basic"
    )
```

---

## 相关文档

- **[基础模式示例](example-basic-mode.md)** - 传统手动模式
- **[完整模式示例](example-complete-mode.md)** - 10 步收集
- **[渐进模式示例](example-progressive-mode.md)** - 快速原型
- **[需求收集模式详解](../references/requirement-collection-modes.md)** - 模式对比
- **[回退机制文档](../references/fallback-mechanism.md)** - 客户端限制说明
