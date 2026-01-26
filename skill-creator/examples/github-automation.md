# Git 工作流自动化集成示例

演示如何将 `init_skill` 与 GitHub MCP 集成，自动化 Git 工作流程。

## 概述

当使用 `init_skill` 创建技能后，可以自动创建 feature 分支、提交初始文件、创建 PR，简化 Git 操作流程。

## 场景1：技能初始化 → 自动创建分支

### 集成前（手动流程）

```bash
# 手动创建分支（容易出错）
git checkout develop
git pull origin develop
git checkout -b feature/add-pdf-processor
git add .
git commit -m "feat(skill): initialize pdf-processor"  # 格式不统一
git push -u origin feature/add-pdf-processor
# 然后在 GitHub Web UI 创建 PR
# 手动填写 PR 描述
# 总耗时：10-15 分钟
```

### 集成后（自动化）

```python
# 1. 创建技能（现有功能）
result = init_skill(
    name="pdf-processor",
    template="tool-based"
)

# 2. 自动创建 feature 分支（新增）
if result["success"]:
    skill_name = result["skill_name"]
    branch_name = f"feature/add-{skill_name}"

    # 调用 GitHub MCP 创建分支
    branch_result = await create_branch(
        owner="your-org",
        repo="your-repo",
        branch=branch_name,
        from_branch="develop"
    )

    # 3. 自动提交初始文件（新增）
    await push_files(
        owner="your-org",
        repo="your-repo",
        branch=branch_name,
        files=[
            {
                "path": f"{skill_name}/SKILL.md",
                "content": read_file(f"{skill_name}/SKILL.md")
            },
            {
                "path": f"{skill_name}/references/README.md",
                "content": read_file(f"{skill_name}/references/README.md")
            }
        ],
        message=f"feat(skill): initialize {skill_name} skill"
    )

    return {
        "skill": result,
        "branch": branch_result,
        "branch_name": branch_name,
        "next_step": "开始开发技能内容"
    }
```

### 输出结果

```json
{
  "skill": {
    "success": true,
    "skill_path": "./pdf-processor",
    "message": "技能结构已创建"
  },
  "branch": {
    "ref": "feature/add-pdf-processor",
    "success": true
  },
  "branch_name": "feature/add-pdf-processor",
  "next_step": "开始开发技能内容"
}
```

## 场景2：开发完成 → 自动创建 PR

### 集成前（手动流程）

```bash
# 开发完成后
git add .
git commit -m "add pdf processing functions"  # 格式随意
git push

# 打开 GitHub Web UI
# 手动创建 PR
# 手动填写描述（可能遗漏重要信息）
# 总耗时：10-15 分钟
```

### 集成后（自动化）

```python
# 用户开发完成后，执行：
result = await create_pr_for_skill(
    skill_path="pdf-processor",
    owner="your-org",
    repo="your-repo"
)

# 内部实现：
async def create_pr_for_skill(skill_path, owner, repo):
    """开发完成后自动创建 PR"""

    # 1. 验证技能
    validation = await validate_skill(skill_path)

    # 2. 分析技能
    analysis = await analyze_skill(skill_path)

    # 3. 生成 PR 描述
    body = f"""## 新增技能: {skill_path}

### 概述
本技能实现了 {extract_description(skill_path)} 功能。

### 验证结果
- **结构验证**: {'✅ 通过' if validation['valid'] else '❌ 失败'}
- **错误数**: {len(validation.get('errors', []))}
- **警告数**: {len(validation.get('warnings', []))}

### 质量分析
- **总分**: {analysis['quality']['overall_score']}/100
- **结构**: {analysis['quality']['structure_score']}/40
- **文档**: {analysis['quality']['documentation_score']}/30
- **测试**: {analysis['quality']['test_coverage_score']}/30

### 变更文件
- SKILL.md
- references/*
- examples/*

### 测试
- [ ] 单元测试通过
- [ ] 集成测试通过
- [ ] 文档更新完整

---

**自动生成**: 由 Skill-Creator MCP 集成创建
"""

    # 4. 创建 PR
    pr = await create_pull_request(
        owner=owner,
        repo=repo,
        title=f"[Skill] Add {skill_path} skill",
        head=f"feature/add-{skill_path}",
        base="develop",
        body=body,
        labels=["skill", "ready-for-review"],
        draft=False
    )

    return pr
```

### 输出结果

```json
{
  "number": 124,
  "html_url": "https://github.com/your-org/your-repo/pull/124",
  "title": "[Skill] Add pdf-processor skill",
  "state": "open",
  "head": {"ref": "feature/add-pdf-processor"},
  "base": {"ref": "develop"}
}
```

## 完整工作流

### 1. 初始化技能

```python
# 开始新技能开发
result = init_skill(
    name="data-validator",
    template="tool-based"
)

# 自动创建分支并提交
await setup_skill_branch(result)
```

### 2. 开发技能

```python
# 用户开发技能内容
# 编辑 SKILL.md
# 添加 references/
# 添加 examples/
```

### 3. 验证和分析

```python
# 开发完成后验证
validation = validate_skill("data-validator")

if validation["valid"]:
    # 验证通过，分析质量
    analysis = analyze_skill("data-validator")
    print(f"质量评分: {analysis['quality']['overall_score']}/100")
else:
    # 验证失败，创建 Issue 跟踪
    await create_validation_issue(validation)
```

### 4. 创建 PR

```python
# 自动创建 PR
pr = await create_pr_for_skill(
    skill_path="data-validator",
    owner="your-org",
    repo="your-repo"
)

print(f"PR 已创建: {pr['html_url']}")
```

## 增强能力

| 维度 | 集成前 | 集成后 |
|------|--------|--------|
| 分支创建 | 手动（易出错） | 自动（规范） |
| Commit 格式 | 不统一 | 自动规范化 |
| PR 创建 | 手动 Web UI | 自动 API |
| PR 描述 | 手动编写 | 自动生成 |
| 验证信息 | 需手动查询 | 自动包含 |
| 质量评分 | 需手动计算 | 自动包含 |
| 时间成本 | 10-15 分钟 | 1 分钟 |

## 实用价值

**场景**: 用户完成 "pdf-processor" 技能开发

**集成前**:
```
1. 手动创建分支（可能忘记从 develop 拉取）
2. 手动 git add/commit/push
3. 打开 GitHub Web UI
4. 手动填写 PR 描述
5. 总耗时：10-15 分钟
```

**集成后**:
```
用户: "技能开发完了，帮我创建 PR"
Claude: 自动执行：
  - 验证技能
  - 分析质量
  - 创建 PR
  - 填充描述（含验证和分析结果）
总耗时：1 分钟
```

## 最佳实践

### 1. 分支命名规范

```python
def generate_branch_name(skill_name, action="add"):
    """生成规范的分支名"""
    prefix = {
        "add": "feature",
        "fix": "fix",
        "refactor": "refactor"
    }
    return f"{prefix.get(action, 'feature')}/{action}-{skill_name}"

# 示例
# feature/add-pdf-processor
# fix/pdf-validator
# refactor/code-analyzer
```

### 2. Commit Message 规范

```python
def generate_commit_message(skill_name, action="initialize"):
    """生成规范的 commit message"""
    action_map = {
        "initialize": f"feat(skill): initialize {skill_name} skill",
        "update": f"feat(skill): update {skill_name} implementation",
        "fix": f"fix(skill): fix {skill_name} validation errors"
    }
    return action_map.get(action, f"chore(skill): {action} {skill_name}")
```

### 3. PR 描述模板

```python
PR_DESCRIPTION_TEMPLATE = """## {title}

### 概述
{description}

### 验证结果
{validation_section}

### 质量分析
{analysis_section}

### 变更文件
{file_list}

### 测试清单
- [ ] 单元测试通过
- [ ] 集成测试通过
- [ ] 文档更新完整

### 相关 Issue
Closes #{issue_number}

---

**自动生成**: 由 Skill-Creator MCP 集成创建
"""
```

### 4. 条件创建 PR

```python
async def smart_create_pr(skill_path, owner, repo):
    """智能创建 PR，满足条件才创建"""

    # 1. 验证必须通过
    validation = await validate_skill(skill_path)
    if not validation["valid"]:
        print(f"验证失败，不创建 PR")
        await create_validation_issue(validation)
        return None

    # 2. 质量评分必须达标
    analysis = await analyze_skill(skill_path)
    if analysis["quality"]["overall_score"] < 70:
        print(f"质量评分 {analysis['quality']['overall_score']} 不达标，建议改进")
        return None

    # 3. 满足条件，创建 PR
    return await create_pull_request(...)
```

## 错误处理

### 分支已存在

```python
try:
    branch = await create_branch(...)
except GitHubError as e:
    if "already exists" in str(e):
        print(f"分支已存在，继续使用现有分支")
        # 继续推送文件到现有分支
    else:
        raise
```

### PR 创建失败

```python
try:
    pr = await create_pull_request(...)
except GitHubError as e:
    print(f"PR 创建失败: {e}")
    # 回退到手动创建
    print(f"请手动创建 PR: {get_pr_url()}")
```

### 验证失败

```python
validation = await validate_skill(skill_path)

if not validation["valid"]:
    # 不创建 PR，创建 Issue 跟踪修复
    issue = await create_issue(
        title=f"[Validation] {skill_path} 验证失败",
        body=format_validation_errors(validation),
        labels=["validation-failed", "bug"]
    )
    print(f"验证失败，已创建 Issue #{issue['number']} 跟踪修复")
    return None
```

## 高级用法

### 批量创建技能 PR

```python
async def batch_create_prs(skill_paths, owner, repo):
    """批量为多个技能创建 PR"""

    results = []
    for skill_path in skill_paths:
        # 验证
        validation = await validate_skill(skill_path)
        if not validation["valid"]:
            print(f"跳过 {skill_path}：验证失败")
            continue

        # 创建 PR
        pr = await create_pr_for_skill(skill_path, owner, repo)
        results.append({
            "skill": skill_path,
            "pr": pr["html_url"],
            "status": "success"
        })

    return results
```

### 自动合并低风险 PR

```python
async def auto_merge_if_safe(pr_number, owner, repo):
    """如果 PR 低风险，自动合并"""

    # 检查 PR 是否只有文档变更
    files = await get_pr_files(pr_number, owner, repo)
    if all(f["filename"].endswith(".md") for f in files):
        # 只有文档变更，自动合并
        await merge_pull_request(
            owner=owner,
            repo=repo,
            pullNumber=pr_number,
            merge_method="squash"
        )
        return True

    return False
```

## 相关文档

- **[init_skill 示例](mcp-init-examples.md)** - 技能初始化详解
- **[validate_skill 示例](mcp-validate-examples.md)** - 技能验证详解
- **[analyze_skill 示例](mcp-analyze-examples.md)** - 技能分析详解
- **[GitHub 需求跟踪](github-requirement-tracking.md)** - 需求跟踪集成
- **[MCP 集成指南](../references/mcp-integration.md)** - MCP 工具配置
