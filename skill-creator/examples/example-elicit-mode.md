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
