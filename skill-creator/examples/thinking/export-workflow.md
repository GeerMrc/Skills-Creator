# Thinking 导出工作流

完整的思考会话导出工作流程。

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

## 批量导出

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

## 命名规范

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

## 目录组织

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

## 相关文档

- **[导出格式示例](export-formats.md)** - 格式详细说明
- **[导出自动化](export-automation.md)** - 高级自动化用法
- **[基础分析示例](analysis-basic.md)** - 思考记录使用
- **[MCP 工具参考](../../references/mcp-tools-reference.md)** - MCP 工具配置
