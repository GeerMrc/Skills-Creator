# GitHub MCP 集成指南

## 概述

GitHub MCP 提供 GitHub 操作能力，与 Skill-Creator 集成后可实现需求跟踪、Git 工作流自动化和问题跟踪。

> **示例代码**：查看 [GitHub 需求跟踪示例](../examples/github-requirement-tracking.md) 和 [Git 自动化示例](../examples/github-automation.md)

## 配置方法

在 SKILL.md 的 frontmatter 中声明 GitHub MCP：

```yaml
---
mcp_servers: ["skill-creator", "GitHub"]
---
```

## 功能说明

### 1. 需求跟踪

需求收集后自动创建 GitHub Issue 跟踪。

**使用场景**：

```python
result = collect_requirements(action="complete", mode="complete")
if result["is_complete"]:
    issue = await create_issue(
        owner="your-org",
        repo="your-repo",
        title=f"[Skill] {result['answers']['skill_name']}",
        body=format_requirements(result),
        labels=["skill-requirement"]
    )
```

**收益**：
- 需求自动记录，避免遗漏
- 团队可见的需求跟踪
- 与开发工作流集成

### 2. Git 自动化

技能初始化后自动创建 feature 分支。

**使用场景**：

```python
result = init_skill(name="pdf-processor", template="tool-based")
branch = await create_branch(
    owner="your-org",
    repo="your-repo",
    branch=f"feature/add-{result['skill_name']}",
    from_branch="develop"
)
```

**收益**：
- 自动化分支创建，节省时间
- 统一分支命名规范
- 与需求 Issue 关联

### 3. PR 自动创建

开发完成后自动创建 Pull Request。

**使用场景**：

```python
pr = await create_pull_request(
    owner="your-org",
    repo="your-repo",
    title=f"[Skill] Add {skill_path}",
    head=f"feature/add-{skill_path}",
    base="develop",
    body=format_pr_description(validation, analysis)
)
```

**PR 模板**：

```markdown
## 技能概述

{{skill_description}}

## 验证结果

- 规范验证: {{validation.score}}/100
- 质量分析: {{analysis.quality_score}}/100
- Token 效率: {{analysis.token_efficiency}}/100

## 变更内容

- 文件变更: {{file_changes}}
- 新增功能: {{new_features}}
- 改进点: {{improvements}}
```

### 4. 问题自动跟踪

验证失败自动创建 Issue。

**使用场景**：

```python
validation = validate_skill(skill_path)
if not validation["is_valid"]:
    issue = await create_issue(
        owner="your-org",
        repo="your-repo",
        title=f"[Validation Failed] {skill_path}",
        body=format_validation_issues(validation),
        labels=["validation-failed", "bug"]
    )
```

## 完整工作流

结合 Skill-Creator 工具的完整 GitHub 集成流程：

```
1. collect_requirements
   → create_issue (GitHub)         # 创建需求跟踪 Issue

2. init_skill
   → create_branch (GitHub)        # 自动创建 feature 分支

3. 开发技能内容

4. validate_skill
   → 失败: create_issue (GitHub)  # 失败则自动创建 Issue
   → 成功: 继续

5. analyze_skill
   → 生成分析报告

6. create_pull_request (GitHub)   # 创建 PR
```

## 集成收益对比

| 维度 | 无集成 | 有集成 |
|------|--------|--------|
| 需求跟踪 | 手动笔记 | GitHub Issue |
| Git 操作 | 10-15 分钟 | 1 分钟 |
| 问题跟踪 | 手动记录 | 自动 Issue |
| 团队协作 | 口头/文档 | GitHub 原生 |

## 参考链接

- **[GitHub 需求跟踪示例](../examples/github-requirement-tracking.md)** - 需求 Issue 自动创建
- **[Git 自动化示例](../examples/github-automation.md)** - 分支和 PR 自动化
- **[MCP 集成指南](mcp-integration.md)** - MCP 基础配置
