# MCP 高级用法

## 概述

本文档介绍 MCP Server 的高级用法，包括错误处理、性能优化、调试技巧和扩展集成。

> **基础配置**：查看 [MCP 集成指南](mcp-integration.md) 了解基础配置和工具列表。

---

## 错误处理

### 常见错误及解决

| 错误 | 原因 | 解决方案 |
|------|------|----------|
| `Tool 'init_skill' not found` | MCP Server 未连接 | 检查配置，确保 MCP Server 已启动 |
| `Skill path not found` | 技能路径不存在 | 确认路径正确，使用绝对路径 |
| `Unknown template type` | 模板类型无效 | 使用有效模板：minimal/tool-based/workflow-based/analyzer-based |
| `Validation failed` | 技能不符合规范 | 查看验证报告，修复问题 |
| `Permission denied` | 目录无写权限 | 检查目录权限 |

### 故障排除

**检查 MCP Server 状态**：
```bash
# 启动服务器测试
uv run python -m skill_creator_mcp

# 使用 Inspector 检查
npx @modelcontextprotocol/inspector ./skill-creator-mcp/src/skill_creator_mcp
```

**查看日志**：
MCP Server 日志输出到 stderr，可在 Claude Code 日志中查看。

**重启 MCP Server**：
如果遇到连接问题，重启 Claude Code 会自动重连 MCP Server。

### 调试模式

启用详细日志：
```bash
export SKILL_CREATOR_LOG_LEVEL=DEBUG
export SKILL_CREATOR_LOG_FILE=/tmp/skill-creator-debug.log
```

---

## 性能优化

### 批量操作

验证多个技能的脚本模式：
```python
skills = ["skill1", "skill2", "skill3"]
for skill in skills:
    result = validate_skill(skill_path=f"./skills/{skill}")
    print(f"{skill}: {result['score']}/100")
```

### 并发操作

独立操作可以并发执行：
```python
import asyncio

results = await asyncio.gather(
    validate_skill(skill_path="./skill1"),
    validate_skill(skill_path="./skill2"),
    validate_skill(skill_path="./skill3")
)
```

### 资源缓存

频繁访问的资源可以缓存：
```python
# 首次读取
best_practices = await session.read_resource("skill://best-practices")

# 后续使用缓存内容
cached_practices = best_practices.contents[0].text
```

---

## 高级配置

### 自定义输出目录

通过环境变量统一管理：
```bash
# ~/.bashrc 或 ~/.zshrc
export SKILL_CREATOR_OUTPUT_DIR=~/projects/skills
```

### 日志配置

**日志级别**：
- `DEBUG`: 详细调试信息
- `INFO`: 一般信息（默认）
- `WARNING`: 警告信息
- `ERROR`: 仅错误信息

**日志格式**：
- `default`: 文本格式（默认）
- `json`: JSON 格式（便于日志分析）

---

## 扩展 MCP 集成

### GitHub MCP 集成

GitHub MCP 提供 GitHub 操作能力，实现需求跟踪、Git 工作流自动化和问题跟踪。

**主要功能**：
- 需求自动跟踪（Issue 创建）
- Git 工作流自动化（分支、PR 创建）
- 验证失败自动创建 Issue

> **详见**：[GitHub 自动化示例](../examples/github-automation.md)

### 集成工作流

**完整流程**（结合所有 MCP）：

```
1. create_requirement_session    # 创建需求收集会话
   → get_static_question         # 获取静态问题
   → update_requirement_answer   # 更新答案
   → check_requirement_completeness  # 检查完整性
   → create_issue (GitHub)       # 创建需求跟踪 Issue

2. init_skill                    # 初始化技能
   → create_branch (GitHub)      # 自动创建 feature 分支

3. 开发技能内容

4. validate_skill                # 验证技能
   → create_issue (GitHub)       # 失败则自动创建 Issue

5. analyze_skill                 # 分析技能

6. create_pull_request (GitHub)  # 创建 PR
```

---

## 相关文档

### 集成示例
- **[GitHub 需求跟踪](../examples/github-requirement-tracking.md)** - 需求 Issue 自动创建
- **[Git 自动化](../examples/github-automation.md)** - 分支和 PR 自动化
- **[MCP 协作](../examples/mcp-skill-collaboration.md)** - MCP 与 Agent-Skill 协同

### 核心文档
- **[MCP 集成指南](mcp-integration.md)** - 基础配置和工具列表
- **[最佳实践 - 高级](best-practices-advanced.md)** - Token 优化和高级技巧
