# GitHub 需求跟踪集成示例

> **重要说明（2026-01-29）**：
>
> 本文档中的示例使用7个原子化需求收集工具。
>
> **新代码**：详见 [需求收集 API 核心](../references/requirement-collection-api-core.md)

---

演示如何将需求收集功能与 GitHub MCP 集成，自动创建需求跟踪 Issue。

## 概述

当使用 **7个原子化需求收集工具** 收集技能需求后，可以自动创建 GitHub Issue 来跟踪需求，确保需求不会遗失且可追溯。

## 场景：需求自动跟踪

### 1. 收集需求

```python
# 使用 complete 模式收集完整需求（新API）
session = await create_requirement_session_tool(mode="complete")
session_id = session["session_id"]

# 获取并回答问题（10步）
answers = {}
for i in range(10):
    question = await get_static_question_tool(mode="complete", step_index=i)
    # answer = 由 Agent-Skill 层通过用户交互获取
    answer = "<用户提供的答案>"
    answers[question["key"]] = answer
    await update_requirement_answer_tool(
        session_id=session_id,
        question_key=question["key"],
        answer=answer
    )

# 检查完整性
completeness = await check_requirement_completeness_tool(answers=answers)

# 需求收集完成
if completeness["is_complete"]:
    result = {
        "is_complete": True,
        "answers": {
            "skill_name": "pdf-processor",
            "skill_function": "处理PDF文档，支持提取文本、合并页面",
            "use_cases": "数据分析师需要批量处理PDF报告",
            "template_type": "tool-based",
            "target_users": "数据分析师、研究人员",
            "tech_stack": "Python, PyPDF2, pdfplumber",
            "dependencies": "无外部依赖"
        },
        "session_id": "req_2026-01-26T10:30:00"
    }
```

### 2. 自动创建 GitHub Issue

```python
# 需求收集完成后，自动创建 Issue
if result["is_complete"]:
    answers = result["answers"]

    issue = await create_issue(
        owner="your-org",
        repo="your-repo",
        title=f"[Skill] {answers['skill_name']} - 需求跟踪",
        body=f"""## 技能需求

### 基本信息
- **技能名称**: {answers['skill_name']}
- **主要功能**: {answers['skill_function']}
- **使用场景**: {answers['use_cases']}
- **目标用户**: {answers['target_users']}

### 技术规格
- **模板类型**: {answers.get('template_type', 'minimal')}
- **技术栈**: {answers.get('tech_stack', '待定')}
- **外部依赖**: {answers.get('dependencies', '无')}

### 自动生成
- 需求收集时间: {datetime.now().isoformat()}
- 收集模式: complete
- 会话ID: {result['session_id']}
""",
        labels=["skill-requirement", "priority-p1"],
        assignees=["developer"]
    )

    print(f"Issue created: {issue['html_url']}")
```

### 3. 输出结果

```
Issue created: https://github.com/your-org/your-repo/issues/123

Issue详情:
- 标题: [Skill] pdf-processor - 需求跟踪
- 标签: skill-requirement, priority-p1
- 负责人: @developer
```

### 4. 跟踪开发进度

```python
# 需求在 Issue 中讨论和跟踪
# 开发完成后，可通过关联 Issue 来关闭

pr = await create_pull_request(
    owner="your-org",
    repo="your-repo",
    title="feat(skill): implement pdf-processor",
    body="Closes #123",  # 关联需求 Issue
    head="feature/add-pdf-processor",
    base="develop"
)
```

## 增强能力

| 维度 | 无集成 | 有集成 |
|------|--------|--------|
| 需求跟踪 | 手动笔记 | GitHub Issue |
| 需求追溯 | 翻聊天记录 | Issue 永久记录 |
| 团队协作 | 口头/文档 | GitHub 原生协作 |
| 优先级管理 | 无 | Labels 自动添加 |
| 进度跟踪 | 手动更新 | Issue 状态 |

## 最佳实践

### 1. Issue 模板

```python
issue_template = """## 技能需求

### 基本信息
- **技能名称**: {skill_name}
- **主要功能**: {skill_function}

### 技术规格
- **模板类型**: {template_type}
- **技术栈**: {tech_stack}

### 验收标准
- [ ] 需求收集完成
- [ ] 技能初始化
- [ ] 规范验证通过
- [ ] 测试覆盖达标
"""
```

### 2. Labels 策略

```python
# 根据需求类型添加不同 Labels
labels = ["skill-requirement"]

# 添加优先级
if answers.get("priority") == "high":
    labels.append("priority-p1")

# 添加技能类型
if answers.get("template_type") == "tool-based":
    labels.append("type-tool")
```

### 3. Assignees 自动分配

```python
# 根据技能类型自动分配负责人
assignees = []
tech_stack = answers.get("tech_stack", "")
if "python" in tech_stack.lower():
    assignees.append("python-dev")
```

## 错误处理

```python
# 需求不完整
if not result["is_complete"]:
    print("需求不完整，请继续收集")

# GitHub API 错误
try:
    issue = await create_issue(...)
except GitHubError as e:
    print(f"创建 Issue 失败: {e}")
    save_to_local_file(result)  # 回退到本地记录
```

## 相关文档

- **[MCP 工具参考](../references/mcp-tools-reference.md)** - MCP 工具完整参考
- **[GitHub 集成指南](../references/mcp-github-integration.md)** - GitHub MCP 集成
- **[GitHub 自动化示例](github-automation.md)** - Git 工作流自动化
