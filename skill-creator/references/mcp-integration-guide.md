# MCP 集成扩展指南

> **文档定位**：本文档提供为 Agent-Skills 集成外部 MCP 的**通用方法论和最佳实践**。

## 概述

### 什么是 MCP 集成？

MCP（Model Context Protocol）集成是指在 Agent-Skill 中使用外部 MCP Server 提供的工具和资源，扩展 Agent-Skill 的能力。

**核心概念**：

- **MCP Server**：提供工具（Tools）和资源（Resources）的服务
- **Agent-Skill**：使用 MCP 工具的技能工作流
- **集成声明**：在 SKILL.md 中声明需要哪些 MCP Server

### 为什么需要 MCP 集成？

**1. 能力扩展**

Agent-Skill 自身只能处理文本交互，MCP 集成可以提供：
- 文件系统操作（FileSystem MCP）
- 数据库访问（Database MCP）
- 网络搜索（Web Search MCP）
- 版本控制（GitHub MCP）
- 思考记录（Thinking MCP）

**2. 工作流增强**

- 自动化重复操作
- 持久化数据存储
- 外部服务集成
- 团队协作支持

### Skill-Creator 的示范案例

Skill-Creator 提供两个核心 MCP 集成示范：

| 示范 | MCP 类型 | 核心功能 | 适用场景 |
|------|----------|----------|----------|
| **[GitHub MCP 集成示范](mcp-github-integration.md)** | 任务自动化 | 需求跟踪、Git 自动化、PR 管理 | 需要 GitHub 集成的 Agent-Skills |
| **[Thinking MCP 集成示范](mcp-thinking-integration.md)** | 思考记录 | 分析记录、决策追溯、知识传递 | 需要思考追踪的 Agent-Skills |

> **提示**：参考这些示范了解具体实现方式，本指南提供通用方法论。

---

## 集成决策框架

### 决策树：我的 Agent-Skill 需要集成哪些 MCP？

```
你的 Agent-Skill 是否需要访问外部系统？
├─ 否 → 不需要 MCP 集成
└─ 是 → 继续

你的 Agent-Skill 需要哪种能力？
├─ 数据持久化 → Database MCP, FileSystem MCP
├─ 外部信息 → Web Search MCP, Weather MCP
├─ 任务自动化 → GitHub MCP, Jira MCP
├─ 思考追踪 → Thinking MCP
└─ 其他 → 查找对应的 MCP Server
```

### MCP 评估标准

**选择 MCP 时考虑**：

1. **必要性** - 是否没有替代方案？
2. **可用性** - 用户环境是否容易安装？
3. **稳定性** - MCP Server 是否稳定可靠？
4. **兼容性** - 是否与你使用的 Claude Code 版本兼容？

**优先级建议**：

| 优先级 | MCP 类型 | 说明 |
|--------|----------|------|
| P0 | 核心功能 MCP | Agent-Skill 的核心能力依赖此 MCP |
| P1 | 增强功能 MCP | 提升用户体验，但非必需 |
| P2 | 可选功能 MCP | 锦上添花的功能 |

### 常见 MCP 功能对照表

| MCP 类型 | 主要功能 | 典型工具 | 适用 Agent-Skills |
|----------|----------|----------|-------------------|
| **FileSystem** | 文件读写、目录操作 | read_file, write_file, list_directory | 数据处理、文件转换 |
| **Database** | 数据库查询、事务管理 | query, execute, transaction | 数据分析、报表生成 |
| **Web Search** | 网络搜索、内容获取 | search, fetch, scrape | 信息收集、知识问答 |
| **GitHub** | 仓库操作、Issue/PR 管理 | create_issue, create_pr, list_commits | 开发工具、项目管理 |
| **Thinking** | 思考记录、会话管理 | create_session, sequential_thinking, export | 分析工具、决策支持 |
| **Weather** | 天气查询、预报 | get_weather, get_forecast | 旅行规划、户外活动 |
| **Calendar** | 日程管理、事件提醒 | create_event, list_events | 助手工具、时间管理 |

---

## 五步集成方法论

### Step 1: 需求分析

**问题清单**：需要处理哪些数据？数据来源？是否需要持久化？是否需要外部服务交互？

**输出**：能力需求清单

---

### Step 2: MCP 选择

**选择流程**：列出候选 MCP → 评估（必要性、可用性、稳定性）→ 确定优先级（P0/P1/P2）→ 选择 P0 集成

**决策表**：

| 能力需求 | 候选 MCP | 优先级 |
|----------|----------|--------|
| 读取远程文件 | FileSystem, HTTP | P0 |
| 保存结果 | Database, FileSystem | P1 |
| 网络搜索 | Web Search | P2 |

---

### Step 3: 配置声明

在 SKILL.md frontmatter 中声明：

```yaml
mcp_servers:
  required: ["skill-creator"]
  optional: ["GitHub", "Thinking"]
```

---

### Step 4: 工作流集成

**直接调用**：
```python
result = await mcp_github_create_issue(owner="org", repo="repo", title="Issue")
```

**条件调用**：
```python
if "GitHub" in available_mcps:
    issue = await mcp_github_create_issue(...)
else:
    log("GitHub MCP 不可用，跳过")
```

---

### Step 5: 测试验证

测试 MCP 可用性、工具调用、错误处理、端到端工作流。

---

## 集成模式库

### 模式1: 数据获取模式

**场景**：从外部获取数据（Web Search、Weather 等）

**实现**：
```python
search_results = await mcp_websearch_search(query="Python tutorial")
content = await mcp_webreader_webReader(url=search_results[0]["url"])
```

---

### 模式2: 数据存储模式

**场景**：持久化数据（Database、FileSystem 等）

**实现**：
```python
await mcp_database_execute(
    sql="INSERT INTO results (id, data) VALUES (?, ?)",
    params=[result_id, json.dumps(data)]
)
```

---

### 模式3: 任务自动化模式

**场景**：自动化重复操作（GitHub、Jira 等）

**实现**：
```python
issue = await mcp_github_create_issue(
    owner="org", repo="repo", title="Issue", body="Description"
)
```

---

### 模式4: 思考记录模式

**场景**：记录分析或决策过程（Thinking 等）

**实现**：
```python
session = await mcp_thinking_create_session(name="分析会话")
await mcp_thinking_sequential_thinking(
    thought="分析结果", session_id=session["id"],
    thoughtNumber=1, totalThoughts=3, nextThoughtNeeded=True
)
```

---

## 参考示范详解

### GitHub MCP 集成示范解析

**核心功能**：需求跟踪、Git 自动化、PR 管理、问题跟踪

**集成方式**：
```python
await mcp_github_create_issue(
    title=f"[Skill] {result['skill_name']}",
    body=format_requirements(result),
    labels=["skill-requirement"]
)
```

**完整文档**：[GitHub MCP 集成示范](mcp-github-integration.md)

---

### Thinking MCP 集成示范解析

**核心功能**：分析思考记录、思考会话导出、思考模板应用、思考可视化

**集成方式**：
```python
session = await mcp_thinking_create_session(name="分析会话")
await mcp_thinking_sequential_thinking(
    thought=f"质量评分: {score}/100",
    session_id=session["id"],
    thoughtNumber=1, totalThoughts=5, nextThoughtNeeded=True
)
```

**完整文档**：[Thinking MCP 集成示范](mcp-thinking-integration.md)

---

## 最佳实践

### 渐进式集成原则

先集成 P0 MCP（必需），验证后再集成 P1/P2 MCP（增强/可选）。

### 错误处理和降级

检查 MCP 可用性，不可用时提供降级方案：
```python
if "GitHub" not in available_mcps:
    logger.warning("GitHub MCP 不可用，跳过")
    return
```

### Token 优化策略

批量操作、缓存结果、选择性输出：
```python
# 批量查询（推荐）
ids = [item.id for item in items]
results = await mcp_database_query(sql="SELECT * FROM items WHERE id IN (?)", params=[ids])
```

---

## FAQ

### Q1: 如果用户没有安装某个 MCP，我的 Agent-Skill 还能工作吗？

**A**：取决于声明方式。`required` MCP 必须安装，`optional` MCP 可提供降级方案。建议将核心功能声明为 required，增强功能声明为 optional。

### Q2: 如何声明 MCP 为可选依赖？

**A**：在 SKILL.md frontmatter 中分级声明：
```yaml
mcp_servers:
  required: ["skill-creator"]
  optional: ["GitHub", "Thinking"]
```

### Q3: 集成多个 MCP 会导致性能问题吗？

**A**：通常不会。MCP 调用是异步的，可并行执行。优化建议：合并小调用、使用缓存、并行执行独立调用。

### Q4: 如何测试 MCP 集成？

**A**：使用单元测试（Mock MCP）、集成测试（真实 MCP）、端到端测试（完整工作流）。

### Q5: 我创建的 MCP 集成示范可以贡献给 Skill-Creator 吗？

**A**：可以！在 `skill-creator/references/` 创建 `mcp-{name}-integration.md`，参考现有示范格式，提交 PR。文档行数控制在 200-300 行。

---

## 参考资料

**示范案例**：

- **[GitHub MCP 集成示范](mcp-github-integration.md)** - 需求跟踪、Git 自动化
- **[Thinking MCP 集成示范](mcp-thinking-integration.md)** - 思考记录、决策追溯

**核心参考**：

- **[MCP 工具参考](mcp-tools-reference.md)** - skill-creator MCP 工具完整参考
- **[最佳实践 - 核心](best-practices-core.md)** - Agent-Skills 核心最佳实践
- **[最佳实践 - 高级](best-practices-advanced.md)** - Agent-Skills 高级最佳实践

**示例代码**：

- **[examples/](../examples/)** - 更多集成示例

**外部资源**：

- **[MCP 规范](https://modelcontextprotocol.io/)** - Model Context Protocol 官方规范
- **[FastMCP 文档](https://jlowin.github.io/fastmcp/)** - FastMCP SDK 文档
