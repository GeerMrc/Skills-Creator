# 需求收集使用示例

## 基础模式示例

使用 `collect_requirements` 工具创建一个技能：

### 步骤 1：开始收集

```json
{
  "action": "start",
  "mode": "basic"
}
```

**响应**：
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

### 步骤 2：回答技能名称

```json
{
  "action": "next",
  "session_id": "req_20250123_abc123",
  "user_input": "pdf-helper"
}
```

**响应**：
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

### 步骤 3-5：继续回答

重复步骤 2 的操作，依次回答：
- 主要功能：解析 PDF 文件，提取文本和图片
- 使用场景：文档分析、数据提取、内容归档
- 模板类型：tool-based
- 额外需求：支持 OCR 文字识别

### 步骤 6：完成收集

```json
{
  "action": "complete",
  "session_id": "req_20250123_abc123"
}
```

**响应**：
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

## 完整模式示例

10 步全面收集，包含技术细节：

### 开始完整模式

```json
{
  "action": "start",
  "mode": "complete"
}
```

### 额外收集的信息

完成基础 5 步后，继续收集：

| 步骤 | 问题 | 示例答案 |
|------|------|----------|
| 6 | 目标用户 | 数据分析师、研究人员、文档管理员 |
| 7 | 技术栈 | Python, PyPDF2, pytesseract |
| 8 | 外部依赖 | tesseract-ocr, poppler-utils |
| 9 | 测试要求 | 单元测试覆盖率 ≥80%，集成测试 |
| 10 | 文档级别 | 完整文档：API 文档 + 使用示例 |

## 中断后恢复示例

### 场景：用户在第 3 步中断

**中断前的状态**：
```json
{
  "step_index": 2,
  "answers": {
    "skill_name": "git-helper",
    "skill_function": "简化 Git 操作"
  }
}
```

### 恢复会话

```json
{
  "action": "status",
  "session_id": "req_20250123_xyz789"
}
```

**响应**：
```json
{
  "success": true,
  "step_index": 2,
  "total_steps": 5,
  "progress": 40.0,
  "answers": {
    "skill_name": "git-helper",
    "skill_function": "简化 Git 操作"
  },
  "message": "会话已恢复，当前进度：40% (2/5)"
}
```

### 从第 3 步继续

```json
{
  "action": "next",
  "session_id": "req_20250123_xyz789",
  "user_input": "自动化提交、分支管理、远程同步"
}
```

## 修改之前答案示例

### 返回上一步

```json
{
  "action": "previous",
  "session_id": "req_20250123_abc123"
}
```

**响应**：返回上一个问题，允许重新输入

### 重新输入答案

```json
{
  "action": "next",
  "session_id": "req_20250123_abc123",
  "user_input": "修正后的答案"
}
```

## 验证错误处理示例

### 格式错误

**输入**：
```json
{
  "action": "next",
  "session_id": "req_20250123_abc123",
  "user_input": "Invalid_Skill_Name"  // 包含大写字母和下划线
}
```

**响应**：
```json
{
  "success": false,
  "error": "只能包含小写字母、数字和连字符"
}
```

### 选项错误

**输入**：
```json
{
  "action": "next",
  "session_id": "req_20250123_abc123",
  "user_input": "custom-template"  // 无效的模板类型
}
```

**响应**：
```json
{
  "success": false,
  "error": "无效的选项，请从以下选项中选择：minimal, tool-based, workflow-based, analyzer-based"
}
```

## 完整工作流示例

### 1. 收集需求

```json
{"action": "start", "mode": "basic"}
```

### 2. 逐个回答问题

```json
{"action": "next", "session_id": "...", "user_input": "answer1"}
{"action": "next", "session_id": "...", "user_input": "answer2"}
{"action": "next", "session_id": "...", "user_input": "answer3"}
{"action": "next", "session_id": "...", "user_input": "answer4"}
{"action": "next", "session_id": "...", "user_input": "answer5"}
```

### 3. 完成收集

```json
{"action": "complete", "session_id": "..."}
```

### 4. 使用结果初始化技能

```json
{
  "name": "pdf-helper",
  "template": "tool-based",
  "output_dir": "./skills"
}
```

## 进度跟踪示例

### 查询当前状态

```json
{
  "action": "status",
  "session_id": "req_20250123_abc123"
}
```

**响应**：
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

## 不同模式对比

### Basic 模式 (5 步)

适合用户已有明确想法：

```
预计时间：3-5 分钟
收集信息：名称、功能、场景、模板、额外需求
```

### Complete 模式 (10 步)

适合复杂技能或团队项目：

```
预计时间：10-15 分钟
收集信息：基础信息 + 用户、技术栈、依赖、测试、文档
```

### Brainstorm 模式

适合探索性项目：

```
预计时间：不确定
特点：开放性问题，鼓励多角度思考
```

### Progressive 模式

适合快速原型：

```
预计时间：2-3 分钟（核心信息）
特点：可跳过非关键步骤，后续补充
```

## 最佳实践

### 1. 简洁明确的输入

```json
// 好的输入
"user_input": "pdf-parser"

// 不好的输入
"user_input": "嗯，我想做一个解析 PDF 的工具，名字叫 pdf-parser 吧..."
```

### 2. 保存会话 ID

```python
# 保存会话 ID 以便后续使用
session_id = result["session_id"]
```

### 3. 处理完整性检查

```json
{
  "completed": true,
  "is_complete": false,  // 需求可能不完整
  "missing_info": ["未说明是否需要处理加密 PDF"],
  "suggestions": ["建议添加加密 PDF 处理功能说明"]
}
```

### 4. 利用 previous 修改答案

发现之前输入有误时，使用 `previous` 返回并重新输入。

## 错误排查

### 会话不存在

```json
{
  "action": "status",
  "session_id": "non_existent_id"
}
```

**响应**：
```json
{
  "success": false,
  "error": "会话不存在，请使用 start 创建新会话"
}
```

### 验证失败

```json
{
  "action": "next",
  "session_id": "...",
  "user_input": ""  // 空字符串
}
```

**响应**：
```json
{
  "success": false,
  "error": "技能名称是必填项"
}
```

## 相关文档

- **[需求澄清指南](../references/requirement-collection.md)** - 详细文档
- **[MCP 集成指南](../references/mcp-integration.md)** - MCP 工具配置
