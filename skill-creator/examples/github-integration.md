# GitHub MCP 集成示例

演示如何将 Skill-Creator 与 GitHub MCP 集成，实现 Git 工作流自动化和需求跟踪。

## 概述

GitHub MCP 提供了丰富的 Git 操作能力，与 Skill-Creator 集成后可实现：

1. **需求跟踪** - 自动创建 GitHub Issue 跟踪需求
2. **分支自动化** - 自动创建 feature 分支
3. **PR 管理** - 自动创建 Pull Request
4. **问题跟踪** - 验证失败自动创建 Issue

---

## 场景1：需求收集 → 自动创建 Issue

### 1. 收集需求

```python
# 使用 complete 模式收集完整需求
session = await create_requirement_session_tool(mode="complete")
session_id = session["session_id"]

# 获取并回答问题（10步）
answers = {}
for i in range(10):
    question = await get_static_question_tool(mode="complete", step_index=i)
    answer = "<用户提供的答案>"
    answers[question["key"]] = answer
    await update_requirement_answer_tool(
        session_id=session_id,
        question_key=question["key"],
        answer=answer
    )

# 检查完整性
completeness = await check_requirement_completeness_tool(answers=answers)
```

### 2. 自动创建 GitHub Issue

```python
# 需求收集完成后，自动创建 Issue
if completeness["is_complete"]:
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
- 会话ID: {session_id}
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

---

## 场景2：技能初始化 → 自动创建分支

### 集成前（手动流程）

```bash
# 手动创建分支（容易出错）
git checkout develop
git pull origin develop
git checkout -b feature/add-pdf-processor
git add .
git commit -m "feat(skill): initialize pdf-processor"
git push -u origin feature/add-pdf-processor
# 然后在 GitHub Web UI 创建 PR
# 总耗时：10-15 分钟
```

### 集成后（自动化）

```python
# 1. 创建技能
result = await init_skill(name="pdf-processor", template="tool-based")

# 2. 自动创建分支并提交
if result["success"]:
    skill_name = result["skill_name"]
    branch_name = f"feature/add-{skill_name}"

    # 调用 GitHub MCP
    await create_branch(
        owner="your-org",
        repo="your-repo",
        branch=branch_name,
        from_branch="develop"
    )

    # 提交初始文件
    await push_files(
        owner="your-org",
        repo="your-repo",
        branch=branch_name,
        files=[
            {"path": f"{skill_name}/SKILL.md", "content": "..."},
            {"path": f"{skill_name}/references/README.md", "content": "..."}
        ],
        message=f"feat(skill): initialize {skill_name}"
    )
```

---

## 场景3：开发完成 → 自动创建 PR

### 自动化流程

```python
async def create_pr_for_skill(skill_path, owner, repo):
    """开发完成后自动创建 PR"""

    # 1. 验证技能
    validation = await validate_skill(skill_path)
    if not validation["valid"]:
        await create_validation_issue(validation)
        return None

    # 2. 分析质量
    analysis = await analyze_skill(skill_path)

    # 3. 生成 PR 描述
    body = f"""## 新增技能: {skill_path}

### 验证结果
- **结构验证**: {'✅ 通过' if validation['valid'] else '❌ 失败'}
- **质量评分**: {analysis['quality']['overall_score']}/100

### 测试清单
- [ ] 单元测试通过
- [ ] 文档更新完整

---

**自动生成**: 由 Skill-Creator MCP 集成创建
"""

    # 4. 创建 PR
    pr = await create_pull_request(
        owner=owner,
        repo=repo,
        title=f"[Skill] Add {skill_path}",
        head=f"feature/add-{skill_path}",
        base="develop",
        body=body,
        labels=["skill", "ready-for-review"]
    )

    return pr
```

---

## 场景4：验证失败 → 自动创建 Issue

### 错误跟踪

```python
validation = await validate_skill(skill_path)

if not validation["valid"]:
    # 不创建 PR，创建 Issue 跟踪
    issue = await create_issue(
        owner="your-org",
        repo="your-repo",
        title=f"[Validation Failed] {skill_path}",
        body=format_validation_errors(validation),
        labels=["validation-failed", "bug"]
    )
    return None
```

---

## 完整工作流

### 1. 初始化阶段

```python
# 创建技能
result = await init_skill(name="data-validator", template="tool-based")

# 自动创建分支
await setup_skill_branch(result)
```

### 2. 开发阶段

```python
# 用户开发技能内容
# 编辑 SKILL.md，添加 references/ 和 examples/
```

### 3. 验证阶段

```python
# 验证技能
validation = await validate_skill("data-validator")

if validation["valid"]:
    analysis = await analyze_skill("data-validator")
    print(f"质量评分: {analysis['quality']['overall_score']}/100")
else:
    await create_validation_issue(validation)
```

### 4. 发布阶段

```python
# 创建 PR
pr = await create_pr_for_skill(
    skill_path="data-validator",
    owner="your-org",
    repo="your-repo"
)
```

---

## 增强能力

| 维度 | 无集成 | 有集成 |
|------|--------|--------|
| 需求跟踪 | 手动笔记 | GitHub Issue |
| 分支创建 | 手动（易出错） | 自动（规范） |
| Commit 格式 | 不统一 | 自动规范化 |
| PR 创建 | 手动 Web UI | 自动 API |
| PR 描述 | 手动编写 | 自动生成 |
| 质量评分 | 需手动计算 | 自动包含 |
| 时间成本 | 10-15 分钟 | 1 分钟 |

---

## 最佳实践

### 分支命名规范

```python
def generate_branch_name(skill_name, action="add"):
    """生成规范的分支名"""
    prefix = {
        "add": "feature",
        "fix": "fix",
        "refactor": "refactor"
    }
    return f"{prefix.get(action, 'feature')}/{action}-{skill_name}"
```

### Commit Message 规范

```python
def generate_commit_message(skill_name, action="initialize"):
    """生成规范的 commit message"""
    return f"feat(skill): {action} {skill_name} skill"
```

### Labels 策略

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

### Assignees 自动分配

```python
# 根据技能类型自动分配负责人
assignees = []
tech_stack = answers.get("tech_stack", "")
if "python" in tech_stack.lower():
    assignees.append("python-dev")
```

---

## 错误处理

### 分支已存在

```python
try:
    branch = await create_branch(...)
except GitHubError as e:
    if "already exists" in str(e):
        print(f"分支已存在，继续使用现有分支")
```

### 需求不完整

```python
if not completeness["is_complete"]:
    print("需求不完整，请继续收集")
```

### GitHub API 错误

```python
try:
    issue = await create_issue(...)
except GitHubError as e:
    print(f"创建 Issue 失败: {e}")
    save_to_local_file(result)  # 回退到本地记录
```

---

## 相关文档

- **[MCP 工具参考](../references/mcp-tools-reference.md)** - MCP 工具完整参考
- **[GitHub MCP 集成示范](mcp-github-integration-example.md)** - GitHub MCP 集成最佳实践
- **[init_skill 示例](mcp-init-examples.md)** - 技能初始化详解
- **[validate_skill 示例](mcp-validate-examples.md)** - 技能验证详解
