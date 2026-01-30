# Thinking 导出自动化

高级自动化导出功能和最佳实践。

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

## 最佳实践

### 1. 版本控制

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

### 2. 定期归档

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

### 3. 自动清理

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

### 4. 导出验证

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

## 完整自动化流程

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

## 相关文档

- **[导出格式示例](export-formats.md)** - 格式详细说明
- **[导出工作流](export-workflow.md)** - 完整工作流程
- **[MCP 工具参考](../../references/mcp-tools-reference.md)** - MCP 工具配置
