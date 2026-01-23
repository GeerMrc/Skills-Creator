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

### 第一步：开始收集

**请求**:
```json
{"action": "start", "mode": "basic"}
```

**响应**摘要:
```json
{
  "session_id": "req_20250123_abc123",
  "current_step": {"key": "skill_name", "title": "技能名称"},
  "total_steps": 5,
  "progress": 0.0
}
```

---

### 第二步至第六步：逐个回答

以下是完整的对话流程表格：

| 步骤 | 提问 | 用户输入 | 进度 |
|-----|------|---------|------|
| 1 | 技能名称 | `pdf-helper` | 20% |
| 2 | 主要功能 | `解析 PDF 文件，提取文本和图片` | 40% |
| 3 | 使用场景 | `文档分析、数据提取、内容归档` | 60% |
| 4 | 模板类型 | `tool-based` | 80% |
| 5 | 额外需求 | `支持 OCR 文字识别` | 100% |

**每次请求格式**:
```json
{
  "action": "next",
  "session_id": "req_20250123_abc123",
  "user_input": "<用户输入>"
}
```

---

### 第七步：完成收集

**请求**:
```json
{"action": "complete", "session_id": "req_20250123_abc123"}
```

**完整响应**:
```json
{
  "success": true,
  "session_id": "req_20250123_abc123",
  "progress": 100.0,
  "answers": {
    "skill_name": "pdf-helper",
    "skill_function": "解析 PDF 文件，提取文本和图片",
    "use_cases": "文档分析、数据提取、内容归档",
    "template_type": "tool-based",
    "additional_features": "支持 OCR 文字识别"
  },
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
{"action": "status", "session_id": "req_20250123_abc123"}
```

**响应**:
```json
{
  "step_index": 3,
  "total_steps": 5,
  "progress": 60.0,
  "answers": {
    "skill_name": "pdf-helper",
    "skill_function": "解析 PDF 文件",
    "use_cases": "文档分析"
  }
}
```

---

## 修改之前答案

使用 `previous` 返回上一步：

**请求**:
```json
{"action": "previous", "session_id": "req_20250123_abc123"}
```

**响应**: 返回上一个问题，允许重新输入

---

## 中断后恢复

会话 ID 自动保存，可以随时恢复：

**请求**:
```json
{"action": "status", "session_id": "req_20250123_abc123"}
```

**响应**: 返回当前进度和已收集的答案，然后可以继续用 `next`

---

## 验证错误处理

### 格式错误

**输入**: `"Invalid_Skill_Name"`

**错误**: `"只能包含小写字母、数字和连字符"`

### 选项错误

**输入**: `"custom-template"`

**错误**: `"无效的选项，请从以下选项中选择：minimal, tool-based, workflow-based, analyzer-based"`

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

```python
if not result["is_complete"]:
    print("缺失信息：", result["missing_info"])
    print("建议：", result["suggestions"])
```

---

## 完整代码示例

```python
# 步骤 1：开始收集
result = await collect_requirements(action="start", mode="basic")
session_id = result["session_id"]

# 步骤 2-5：逐个回答
questions_answers = {
    "skill_name": "docker-helper",
    "skill_function": "简化 Docker 容器管理",
    "use_cases": "开发环境部署、测试环境管理",
    "template_type": "tool-based",
    "additional_features": "支持多主机管理"
}

for answer in questions_answers.values():
    result = await collect_requirements(
        action="next",
        session_id=session_id,
        user_input=answer
    )
    print(f"进度：{result['progress']}%")

# 步骤 6：完成收集
result = await collect_requirements(action="complete", session_id=session_id)

if result["is_complete"]:
    # 创建技能
    await init_skill(
        name=result["answers"]["skill_name"],
        template=result["answers"]["template_type"]
    )
```

---

## 相关文档

- **[需求澄清指南](../references/requirement-collection.md)** - 详细文档
- **[API 核心参考](../references/requirement-collection-api-core.md)** - 完整 API 文档
- **[完整模式示例](example-complete-mode.md)** - 10 步完整收集
- **[渐进模式示例](example-progressive-mode.md)** - 快速原型
- **[Elicit 模式示例](example-elicit-mode.md)** - 自动收集
