# Git 工作流自动化集成示例

演示如何将 `init_skill` 与 GitHub MCP 集成，自动化 Git 工作流程。

## 概述

当使用 `init_skill` 创建技能后，可以自动创建 feature 分支、提交初始文件、创建 PR，简化 Git 操作流程。

---

## 场景1：技能初始化 → 自动创建分支

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
result = init_skill(name="pdf-processor", template="tool-based")

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

## 场景2：开发完成 → 自动创建 PR

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

## 场景3：需求跟踪 → 自动创建 Issue

### 集成需求收集与 GitHub

```python
# 需求收集完成后
session = await create_requirement_session_tool(mode="complete")
# ... 收集用户输入 ...

# 自动创建 Issue 跟踪
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

### 技术规格
- **模板类型**: {answers.get('template_type', 'minimal')}
- **技术栈**: {answers.get('tech_stack', '待定')}

### 自动生成
- 收集模式: complete
- 会话ID: {session['session_id']}
""",
        labels=["skill-requirement"],
        assignees=["developer"]
    )
```

---

## 完整工作流

### 1. 初始化阶段

```python
# 创建技能
result = init_skill(name="data-validator", template="tool-based")

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
validation = validate_skill("data-validator")

if validation["valid"]:
    analysis = analyze_skill("data-validator")
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

| 维度 | 集成前 | 集成后 |
|------|--------|--------|
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

### 条件创建 PR

```python
async def smart_create_pr(skill_path, owner, repo):
    """智能创建 PR，满足条件才创建"""

    # 验证必须通过
    validation = await validate_skill(skill_path)
    if not validation["valid"]:
        await create_validation_issue(validation)
        return None

    # 质量评分必须达标
    analysis = await analyze_skill(skill_path)
    if analysis["quality"]["overall_score"] < 70:
        print(f"质量评分不达标，建议改进")
        return None

    # 满足条件，创建 PR
    return await create_pull_request(...)
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

### 验证失败

```python
validation = await validate_skill(skill_path)

if not validation["valid"]:
    # 不创建 PR，创建 Issue 跟踪
    issue = await create_issue(
        title=f"[Validation] {skill_path} 验证失败",
        body=format_validation_errors(validation),
        labels=["validation-failed"]
    )
    return None
```

---

## 相关文档

- **[init_skill 示例](mcp-init-examples.md)** - 技能初始化详解
- **[validate_skill 示例](mcp-validate-examples.md)** - 技能验证详解
- **[analyze_skill 示例](mcp-analyze-examples.md)** - 技能分析详解
- **[GitHub 需求跟踪](github-requirement-tracking.md)** - 需求跟踪集成
- **[MCP 集成指南](../references/mcp-tools-reference.md)** - MCP 工具配置
