# 基础模式使用示例

本文档展示如何使用 `collect_requirements` 的基础模式创建技能。

## 概述

基础模式 (basic) 通过 5 个步骤快速收集核心信息：
1. 技能名称
2. 主要功能
3. 使用场景
4. 模板类型
5. 额外需求

预计时间：3-5 分钟

---

## 完整对话流程

### 步骤 1：开始收集

**请求**:
```json
{
  "action": "start",
  "mode": "basic"
}
```

**响应**:
```json
{
  "success": true,
  "session_id": "req_20250123_abc123",
  "action": "start",
  "mode": "basic",
  "current_step": {
    "key": "skill_name",
    "title": "技能名称",
    "prompt": "请输入技能名称（小写字母、数字、连字符，如：pdf-parser、git-helper）"
  },
  "step_index": 0,
  "total_steps": 5,
  "progress": 0.0,
  "answers": {},
  "message": "欢迎使用需求澄清工具！当前进度：0% (0/5)",
  "completed": false
}
```

---

### 步骤 2：回答技能名称

**请求**:
```json
{
  "action": "next",
  "session_id": "req_20250123_abc123",
  "user_input": "pdf-helper"
}
```

**响应**:
```json
{
  "success": true,
  "session_id": "req_20250123_abc123",
  "action": "next",
  "mode": "basic",
  "current_step": {
    "key": "skill_function",
    "title": "主要功能",
    "prompt": "请简要描述技能的主要功能"
  },
  "step_index": 1,
  "total_steps": 5,
  "progress": 20.0,
  "answers": {
    "skill_name": "pdf-helper"
  },
  "message": "当前进度：20% (1/5)",
  "completed": false
}
```

---

### 步骤 3：回答主要功能

**请求**:
```json
{
  "action": "next",
  "session_id": "req_20250123_abc123",
  "user_input": "解析 PDF 文件，提取文本和图片"
}
```

**响应**:
```json
{
  "success": true,
  "current_step": {
    "key": "use_cases",
    "title": "使用场景",
    "prompt": "请列出技能的主要使用场景"
  },
  "step_index": 2,
  "total_steps": 5,
  "progress": 40.0,
  "answers": {
    "skill_name": "pdf-helper",
    "skill_function": "解析 PDF 文件，提取文本和图片"
  }
}
```

---

### 步骤 4：回答使用场景

**请求**:
```json
{
  "action": "next",
  "session_id": "req_20250123_abc123",
  "user_input": "文档分析、数据提取、内容归档"
}
```

**响应**:
```json
{
  "success": true,
  "current_step": {
    "key": "template_type",
    "title": "模板类型",
    "prompt": "请选择模板类型：minimal, tool-based, workflow-based, analyzer-based"
  },
  "step_index": 3,
  "total_steps": 5,
  "progress": 60.0,
  "answers": {
    "skill_name": "pdf-helper",
    "skill_function": "解析 PDF 文件，提取文本和图片",
    "use_cases": "文档分析、数据提取、内容归档"
  }
}
```

---

### 步骤 5：回答模板类型

**请求**:
```json
{
  "action": "next",
  "session_id": "req_20250123_abc123",
  "user_input": "tool-based"
}
```

**响应**:
```json
{
  "success": true,
  "current_step": {
    "key": "additional_features",
    "title": "额外需求",
    "prompt": "是否有额外需求？（可选）"
  },
  "step_index": 4,
  "total_steps": 5,
  "progress": 80.0,
  "answers": {
    "skill_name": "pdf-helper",
    "skill_function": "解析 PDF 文件，提取文本和图片",
    "use_cases": "文档分析、数据提取、内容归档",
    "template_type": "tool-based"
  }
}
```

---

### 步骤 6：回答额外需求

**请求**:
```json
{
  "action": "next",
  "session_id": "req_20250123_abc123",
  "user_input": "支持 OCR 文字识别"
}
```

**响应**:
```json
{
  "success": true,
  "step_index": 5,
  "total_steps": 5,
  "progress": 100.0,
  "answers": {
    "skill_name": "pdf-helper",
    "skill_function": "解析 PDF 文件，提取文本和图片",
    "use_cases": "文档分析、数据提取、内容归档",
    "template_type": "tool-based",
    "additional_features": "支持 OCR 文字识别"
  },
  "message": "所有步骤已完成，请使用 complete 完成收集",
  "completed": false
}
```

---

### 步骤 7：完成收集

**请求**:
```json
{
  "action": "complete",
  "session_id": "req_20250123_abc123"
}
```

**响应**:
```json
{
  "success": true,
  "session_id": "req_20250123_abc123",
  "action": "complete",
  "mode": "basic",
  "step_index": 5,
  "total_steps": 5,
  "progress": 100.0,
  "answers": {
    "skill_name": "pdf-helper",
    "skill_function": "解析 PDF 文件，提取文本和图片",
    "use_cases": "文档分析、数据提取、内容归档",
    "template_type": "tool-based",
    "additional_features": "支持 OCR 文字识别"
  },
  "message": "需求收集完成！",
  "completed": true,
  "is_complete": true,
  "missing_info": [],
  "suggestions": [
    "考虑添加 PDF 元数据提取功能",
    "可以支持加密 PDF 的处理"
  ]
}
```

---

## 使用结果初始化技能

收集完成后，使用 `init_skill` 工具创建技能：

**请求**:
```json
{
  "name": "pdf-helper",
  "template": "tool-based"
}
```

---

## 进度查询

随时查询当前状态：

**请求**:
```json
{
  "action": "status",
  "session_id": "req_20250123_abc123"
}
```

**响应**:
```json
{
  "success": true,
  "action": "status",
  "step_index": 3,
  "total_steps": 5,
  "progress": 60.0,
  "answers": {
    "skill_name": "pdf-helper",
    "skill_function": "解析 PDF 文件",
    "use_cases": "文档分析"
  },
  "completed": false,
  "message": "当前进度：60% (3/5)"
}
```

---

## 修改之前答案

使用 `previous` 返回上一步：

**请求**:
```json
{
  "action": "previous",
  "session_id": "req_20250123_abc123"
}
```

**响应**: 返回上一个问题，允许重新输入

---

## 中断后恢复

会话 ID 自动保存，可以随时恢复：

**请求**:
```json
{
  "action": "status",
  "session_id": "req_20250123_abc123"
}
```

**响应**: 返回当前进度和已收集的答案，然后可以继续用 `next`

---

## 验证错误处理

### 格式错误

**输入**:
```json
{
  "action": "next",
  "session_id": "req_20250123_abc123",
  "user_input": "Invalid_Skill_Name"
}
```

**响应**:
```json
{
  "success": false,
  "error": "只能包含小写字母、数字和连字符"
}
```

### 选项错误

**输入**:
```json
{
  "action": "next",
  "session_id": "req_20250123_abc123",
  "user_input": "custom-template"
}
```

**响应**:
```json
{
  "success": false,
  "error": "无效的选项，请从以下选项中选择：minimal, tool-based, workflow-based, analyzer-based"
}
```

---

## 最佳实践

### 简洁明确的输入

```json
// 好的输入
"user_input": "pdf-parser"

// 不好的输入
"user_input": "嗯，我想做一个解析 PDF 的工具，名字叫 pdf-parser 吧..."
```

### 保存会话 ID

```python
# 保存会话 ID 以便后续使用
session_id = result["session_id"]
```

### 检查完整性

完成收集后检查 `is_complete` 和 `missing_info`：

```python
if not result["is_complete"]:
    print("缺失信息：", result["missing_info"])
    print("建议：", result["suggestions"])
```

---

## 相关文档

- **[需求澄清指南](../references/requirement-collection.md)** - 详细文档
- **[完整模式示例](example-complete-mode.md)** - 10 步完整收集
- **[渐进模式示例](example-progressive-mode.md)** - 快速原型
- **[Elicit 模式示例](example-elicit-mode.md)** - 自动收集
