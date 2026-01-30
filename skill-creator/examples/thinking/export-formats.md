# Thinking 导出格式示例

Thinking MCP 支持将思考会话导出为多种格式。

## 概述

Thinking MCP 支持将思考会话导出为多种格式（Markdown、HTML、JSON、Text），便于存档、分享和后续查阅。

## 基本导出

```python
# 假设已有思考会话
session_id = "sess_2026-01-26_10:30:00"

# 导出为 Markdown（默认）
result = await export_session(
    session_id=session_id,
    format_type="markdown",
    output_path="./docs/analysis-thinking.md"
)

print(f"导出成功: {result['output_path']}")
```

## 输出格式详解

### Markdown 格式 (`.md`)

**特点**: 可读性好，易编辑，适合版本控制

```markdown
# 代码分析思考记录

**会话ID**: sess_2026-01-26_10:30:00
**创建时间**: 2026-01-26 10:30:00
**状态**: completed

---

## 思考过程

### 步骤 1: 初始评估

技能 `pdf-processor` 的质量评分为 75/100。

- **结构评分**: 30/40
- **文档评分**: 20/30
- **测试评分**: 25/30

总体评估: 良好，但需要改进文档和结构。

---

### 步骤 2: 问题分类

问题分类结果：
- P0（阻塞性）: 2 个
- P1（高优先级）: 5 个
- P2（中优先级）: 3 个

分析: 2 个 P0 问题需要立即处理。

---

### 步骤 3: 优先级排序

优先级排序逻辑：
1. P0 问题影响基本功能，必须优先
2. P1 问题影响代码质量，尽快处理
3. P2 问题为改进建议

---

### 步骤 4: 具体问题

P0 问题 1: 缺少错误处理
- 影响: PDF 解析失败时程序崩溃
- 建议: 添加 try-except 处理

---

### 步骤 5: 修复方案

建议修复顺序:
1. 修复所有 P0 问题
2. 修复高影响的 P1 问题
3. 逐步处理 P2 改进建议

---

### 步骤 6: 最终结论

分析完成。总体评分 75/100，需要重点修复 2 个 P0 问题。
```

### HTML 格式 (`.html`)

**特点**: 样式丰富，适合展示和分享

```html
<!DOCTYPE html>
<html>
<head>
    <title>代码分析思考记录</title>
    <style>
        body { font-family: Arial, sans-serif; max-width: 800px; margin: 0 auto; padding: 20px; }
        .step { border-left: 3px solid #007bff; padding-left: 15px; margin: 20px 0; }
        .step-number { color: #007bff; font-weight: bold; }
        .timestamp { color: #666; font-size: 0.9em; }
    </style>
</head>
<body>
    <h1>代码分析思考记录</h1>
    <p><strong>会话ID</strong>: sess_2026-01-26_10:30:00</p>
    <p><strong>创建时间</strong>: 2026-01-26 10:30:00</p>

    <h2>思考过程</h2>

    <div class="step">
        <p class="step-number">步骤 1</p>
        <p>技能 <code>pdf-processor</code> 的质量评分为 75/100。</p>
        <ul>
            <li>结构评分: 30/40</li>
            <li>文档评分: 20/30</li>
            <li>测试评分: 25/30</li>
        </ul>
    </div>

    <div class="step">
        <p class="step-number">步骤 2</p>
        <p>问题分类结果：</p>
        <ul>
            <li>P0（阻塞性）: 2 个</li>
            <li>P1（高优先级）: 5 个</li>
            <li>P2（中优先级）: 3 个</li>
        </ul>
    </div>

    <!-- 更多步骤... -->
</body>
</html>
```

### JSON 格式 (`.json`)

**特点**: 结构化，可解析，适合数据处理

```json
{
  "session_id": "sess_2026-01-26_10:30:00",
  "name": "分析-pdf-processor",
  "description": "代码质量分析和改进建议",
  "created_at": "2026-01-26T10:30:00",
  "status": "completed",
  "thoughts": [
    {
      "number": 1,
      "content": "技能 `pdf-processor` 的质量评分为 75/100...",
      "timestamp": "2026-01-26T10:30:01"
    },
    {
      "number": 2,
      "content": "问题分类结果：P0: 2个, P1: 5个, P2: 3个...",
      "timestamp": "2026-01-26T10:30:02"
    }
  ],
  "metadata": {
    "skill": "pdf-processor",
    "overall_score": 75,
    "p0_count": 2,
    "p1_count": 5,
    "p2_count": 3
  }
}
```

### Text 格式 (`.txt`)

**特点**: 兼容性最好，无格式

```
代码分析思考记录
==================

会话ID: sess_2026-01-26_10:30:00
创建时间: 2026-01-26 10:30:00
状态: completed

思考过程
--------

步骤 1: 初始评估
技能 pdf-processor 的质量评分为 75/100。
- 结构评分: 30/40
- 文档评分: 20/30
- 测试评分: 25/30

步骤 2: 问题分类
问题分类结果：
- P0（阻塞性）: 2 个
- P1（高优先级）: 5 个
- P2（中优先级）: 3 个

...
```

## 格式对比

| 格式 | 扩展名 | 优点 | 缺点 | 适用场景 |
|------|--------|------|------|----------|
| **Markdown** | `.md` | 可读性好，易编辑 | 样式有限 | 文档存档、版本控制 |
| **HTML** | `.html` | 样式丰富，可浏览 | 不可编辑 | 展示、分享 |
| **JSON** | `.json` | 结构化，可解析 | 不易读 | 数据处理、API |
| **Text** | `.txt` | 兼容性最好 | 无格式 | 简单日志 |

## 导出路径选项

```python
# 使用相对路径
await export_session(
    session_id=session_id,
    format_type="markdown",
    output_path="./docs/analysis.md"
)

# 使用绝对路径
await export_session(
    session_id=session_id,
    format_type="markdown",
    output_path="/full/path/to/analysis.md"
)

# 使用波浪号展开
await export_session(
    session_id=session_id,
    format_type="markdown",
    output_path="~/docs/analysis.md"
)

# 自动生成路径（不指定 output_path）
result = await export_session(
    session_id=session_id,
    format_type="markdown"
)
# 自动保存到 ~/exports/session-<id>.md
```

## 相关文档

- **[导出工作流](export-workflow.md)** - 批量导出和自动化
- **[导出自动化](export-automation.md)** - 高级自动化用法
- **[MCP 工具参考](../../references/mcp-tools-reference.md)** - MCP 工具配置
