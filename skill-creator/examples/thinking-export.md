# Thinking 会话导出示例

演示如何使用 Thinking MCP 的会话导出功能，将思考过程保存为文档。

## 概述

Thinking MCP 支持将思考会话导出为多种格式（Markdown、HTML、JSON），便于存档、分享和后续查阅。

## 场景：导出思考会话

### 基本导出

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

### 输出格式

#### Markdown 格式 (`analysis-thinking.md`)

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

#### HTML 格式 (`analysis-thinking.html`)

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

#### JSON 格式 (`analysis-thinking.json`)

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

## 完整工作流

### 1. 分析并记录

```python
# 执行代码分析
analysis = await analyze_skill(skill_path="pdf-processor")

# 创建思考会话
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
```

### 2. 多格式导出

```python
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

### 3. 自动归档

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

## 高级用法

### 1. 自定义输出路径

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

### 2. 批量导出

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

### 3. 模板化导出

```python
async def export_with_template(session_id, template_path):
    """使用自定义模板导出"""

    # 获取会话数据
    session = await get_session(session_id)

    # 读取模板
    with open(template_path) as f:
        template = f.read()

    # 填充模板
    content = template.format(**session)

    # 写入文件
    output_path = f"./docs/{session['name']}.md"
    with open(output_path, 'w') as f:
        f.write(content)

    return output_path
```

### 4. 导出并分享

```python
async def export_and_share(session_id, share_method="github"):
    """导出并分享思考会话"""

    # 导出
    result = await export_session(
        session_id=session_id,
        format_type="markdown"
    )

    output_path = result['output_path']

    if share_method == "github":
        # 推送到 GitHub
        await git_commit_and_push(output_path)
        # 创建 GitHub Gist
        gist_url = await create_gist(output_path)
        return gist_url

    elif share_method == "email":
        # 通过邮件分享
        await send_email_attachment(output_path)
        return "Email sent"

    elif share_method == "slack":
        # 上传到 Slack
        await slack_upload_file(output_path)
        return "Uploaded to Slack"
```

## 格式对比

| 格式 | 扩展名 | 优点 | 缺点 | 适用场景 |
|------|--------|------|------|----------|
| **Markdown** | `.md` | 可读性好，易编辑 | 样式有限 | 文档存档、版本控制 |
| **HTML** | `.html` | 样式丰富，可浏览 | 不可编辑 | 展示、分享 |
| **JSON** | `.json` | 结构化，可解析 | 不易读 | 数据处理、API |
| **Text** | `.txt` | 兼容性最好 | 无格式 | 简单日志 |

## 最佳实践

### 1. 命名规范

```python
def generate_export_name(session, format_type):
    """生成导出文件名"""
    timestamp = datetime.now().strftime("%Y%m%d")
    session_name = session["name"].replace(" ", "-")
    ext = {"markdown": "md", "html": "html", "json": "json"}[format_type]

    return f"{session_name}-{timestamp}.{ext}"

# 示例
# analysis-pdf-processor-20260126.md
# analysis-git-helper-20260126.html
```

### 2. 目录组织

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

### 3. 版本控制

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

### 4. 自动清理

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

## 相关文档

- **[Thinking 分析示例](thinking-analysis.md)** - 思考记录使用
- **[analyze_skill 示例](mcp-analyze-examples.md)** - 代码分析详解
- **[MCP 集成指南](../references/mcp-tools-reference.md)** - MCP 工具配置
