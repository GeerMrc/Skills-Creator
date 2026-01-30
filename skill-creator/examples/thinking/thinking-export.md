# Thinking 导出示例完整指南

> **本文档整合了导出格式、工作流程和自动化最佳实践**

Thinking MCP 支持将思考会话导出为多种格式，便于存档、分享和后续查阅。

---

## 一、导出格式详解

### 1.1 概述

Thinking MCP 支持将思考会话导出为多种格式（Markdown、HTML、JSON、Text）。

### 1.2 Markdown 格式 (`.md`)

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
```

### 1.3 HTML 格式 (`.html`)

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
</body>
</html>
```

### 1.4 JSON 格式 (`.json`)

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

### 1.5 Text 格式 (`.txt`)

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
```

### 1.6 格式对比

| 格式 | 扩展名 | 优点 | 缺点 | 适用场景 |
|------|--------|------|------|----------|
| **Markdown** | `.md` | 可读性好，易编辑 | 样式有限 | 文档存档、版本控制 |
| **HTML** | `.html` | 样式丰富，可浏览 | 不可编辑 | 展示、分享 |
| **JSON** | `.json` | 结构化，可解析 | 不易读 | 数据处理、API |
| **Text** | `.txt` | 兼容性最好 | 无格式 | 简单日志 |

---

## 二、导出工作流程

### 2.1 完整工作流

```python
# 1. 分析并记录
analysis = await analyze_skill(skill_path="pdf-processor")

session = await create_session(
    name="分析-pdf-processor",
    description="代码质量分析"
)

# 记录思考过程
for i, thought in enumerate(generate_thoughts(analysis), 1):
    await sequential_thinking(
        thought=thought,
        session_id=session["id"],
        thoughtNumber=i,
        totalThoughts=len(analysis["suggestions"]) + 2,
        nextThoughtNeeded=True
    )

# 2. 多格式导出
session_id = session["id"]

# 导出为 Markdown
md_result = await export_session(
    session_id=session_id,
    format_type="markdown",
    output_path="./docs/analysis-thinking.md"
)

# 导出为 HTML
html_result = await export_session(
    session_id=session_id,
    format_type="html",
    output_path="./docs/analysis-thinking.html"
)

# 导出为 JSON
json_result = await export_session(
    session_id=session_id,
    format_type="json",
    output_path="./docs/analysis-thinking.json"
)

print(f"Markdown: {md_result['output_path']}")
print(f"HTML: {html_result['output_path']}")
print(f"JSON: {json_result['output_path']}")
```

### 2.2 自动归档

```python
async def auto_archive_session(session_id, skill_path):
    """自动归档思考会话"""

    # 生成归档路径
    archive_dir = f"{skill_path}/docs/thinking"
    os.makedirs(archive_dir, exist_ok=True)

    # 导出多种格式
    formats = ["markdown", "html", "json"]
    results = []

    for fmt in formats:
        result = await export_session(
            session_id=session_id,
            format_type=fmt,
            output_path=f"{archive_dir}/analysis.{fmt}"
        )
        results.append(result)

    return results
```

### 2.3 批量导出

```python
async def batch_export_sessions(session_ids, output_dir):
    """批量导出多个会话"""

    os.makedirs(output_dir, exist_ok=True)
    results = []

    for session_id in session_ids:
        # 获取会话信息
        session = await get_session(session_id)

        # 生成文件名
        filename = f"{session['name']}-{session_id[:8]}.md"

        # 导出
        result = await export_session(
            session_id=session_id,
            format_type="markdown",
            output_path=f"{output_dir}/{filename}"
        )

        results.append(result)

    return results
```

### 2.4 导出路径选项

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

### 2.5 命名规范

```python
def generate_export_name(session, format_type):
    """生成导出文件名"""
    timestamp = datetime.now().strftime("%Y%m%d")
    session_name = session["name"].replace(" ", "-")
    ext = {"markdown": "md", "html": "html", "json": "json"}[format_type]

    return f"{session_name}-{timestamp}.{ext}"

# 示例
# analysis-pdf-processor-20260126.md
# refactoring-git-helper-20260126.html
```

### 2.6 目录组织

```
skill-processor/
├── docs/
│   └── thinking/           # 思考记录归档目录
│       ├── 2026-01/        # 按月份组织
│       │   ├── analysis-20260115.md
│       │   ├── analysis-20260120.md
│       │   └── refactoring-20260126.md
│       └── 2026-02/
├── SKILL.md
└── references/
```

---

## 三、导出自动化最佳实践

### 3.1 版本控制集成

```python
# 导出后自动提交到 Git
async def export_and_commit(session_id, skill_path):
    """导出并提交到 Git"""

    # 导出
    result = await export_session(
        session_id=session_id,
        format_type="markdown",
        output_path=f"{skill_path}/docs/analysis.md"
    )

    # 提交到 Git
    await bash_command(
        f"git add {result['output_path']} && "
        f"git commit -m 'docs(thinking): add analysis record' && "
        f"git push"
    )

    return result
```

### 3.2 定期归档

```python
async def scheduled_archive(session_ids, archive_base_dir):
    """定期归档思考会话"""

    # 按月归档
    current_month = datetime.now().strftime("%Y-%m")
    archive_dir = f"{archive_base_dir}/{current_month}"
    os.makedirs(archive_dir, exist_ok=True)

    results = []
    for session_id in session_ids:
        result = await export_session(
            session_id=session_id,
            format_type="markdown",
            output_path=f"{archive_dir}/session-{session_id[:8]}.md"
        )
        results.append(result)

    return results
```

### 3.3 自动清理

```python
async def cleanup_old_exports(archive_dir, keep_months=3):
    """清理旧的导出文件"""

    cutoff = datetime.now() - timedelta(days=keep_months * 30)

    for filename in os.listdir(archive_dir):
        filepath = os.path.join(archive_dir, filename)

        # 检查文件时间
        file_time = datetime.fromtimestamp(os.path.getmtime(filepath))

        if file_time < cutoff:
            # 备份到长期存储
            await archive_to_storage(filepath)
            # 删除本地文件
            os.remove(filepath)
```

### 3.4 导出验证

```python
async def verify_export(session_id, output_path):
    """验证导出结果"""

    # 检查文件存在
    if not os.path.exists(output_path):
        raise Exception(f"导出文件不存在: {output_path}")

    # 检查文件大小
    file_size = os.path.getsize(output_path)
    if file_size == 0:
        raise Exception(f"导出文件为空: {output_path}")

    # 检查文件内容（Markdown 格式）
    if output_path.endswith('.md'):
        with open(output_path, 'r') as f:
            content = f.read()
            if '## 思考过程' not in content:
                raise Exception(f"导出内容不完整: {output_path}")

    return True
```

### 3.5 完整自动化流程

```python
async def full_auto_workflow(skill_path):
    """完整的自动化工作流"""

    # 1. 分析
    analysis = await analyze_skill(skill_path=skill_path)

    # 2. 创建会话并记录
    session = await create_session(name=f"auto-{skill_path}")
    for i, thought in enumerate(auto_generate_thoughts(analysis)):
        await sequential_thinking(
            thought=thought,
            session_id=session["id"],
            thoughtNumber=i+1,
            totalThoughts=len(analysis["suggestions"])+1,
            nextThoughtNeeded=(i < len(analysis["suggestions"]))
        )

    # 3. 导出（多格式）
    export_base = f"{skill_path}/docs/thinking"
    os.makedirs(export_base, exist_ok=True)

    for fmt in ["markdown", "json"]:
        await export_session(
            session_id=session["id"],
            format_type=fmt,
            output_path=f"{export_base}/analysis.{fmt}"
        )

    # 4. 验证
    await verify_export(session["id"], f"{export_base}/analysis.md")

    # 5. 提交到 Git
    await export_and_commit(session["id"], skill_path)

    return session
```

---

## 四、相关文档

- **[Thinking 分析示例](thinking-analysis.md)** - 分析集成和高级模式
- **[MCP 工具参考](../../references/mcp-tools-reference.md)** - MCP 工具配置
- **[MCP Thinking 集成示范](../../references/mcp-thinking-integration.md)** - 集成最佳实践
