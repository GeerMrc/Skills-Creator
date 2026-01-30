# Thinking MCP 集成指南

## 概述

Thinking MCP 提供思考记录能力，与 Skill-Creator 集成后可实现代码分析思考过程记录、决策逻辑追溯和思考会话导出。

> **示例代码**：查看 [Thinking 分析示例](../examples/thinking-analysis.md) 和 [Thinking 导出示例](../examples/thinking-export.md)

## 配置方法

在 SKILL.md 的 frontmatter 中声明 Thinking MCP：

```yaml
---
mcp_servers: ["skill-creator", "GitHub", "Thinking"]
---
```

## 功能说明

### 1. 分析思考记录

记录代码分析的完整思考过程，便于后续审查和知识传递。

**使用场景**：

```python
# 执行分析
analysis = await analyze_skill(skill_path="pdf-processor")

# 创建思考会话
session = await create_session(
    name=f"分析-{skill_path}",
    description="代码质量分析"
)

# 记录思考步骤
await sequential_thinking(
    thought=f"质量评分: {analysis['quality']['overall_score']}/100",
    session_id=session["id"],
    thoughtNumber=1,
    totalThoughts=5,
    nextThoughtNeeded=True
)

await sequential_thinking(
    thought=f"Token 效率: {analysis['token_efficiency']['score']}/100",
    session_id=session["id"],
    thoughtNumber=2,
    totalThoughts=5,
    nextThoughtNeeded=True
)

# ... 更多思考步骤
```

**收益**：
- 完整记录分析思路
- 便于团队审查
- 知识沉淀和传递

### 2. 思考会话导出

将思考过程导出为文档，支持多种格式。

**支持格式**：
- Markdown (.md) - 适合文档查看
- HTML (.html) - 带样式，适合浏览器查看
- JSON (.json) - 适合程序处理

**使用场景**：

```python
# 导出为 Markdown
await export_session(
    session_id=session["id"],
    format_type="markdown",
    output_path=f"{skill_path}/docs/analysis-thinking.md"
)

# 导出为 HTML
await export_session(
    session_id=session["id"],
    format_type="html",
    output_path=f"{skill_path}/docs/analysis-thinking.html"
)

# 导出为 JSON
await export_session(
    session_id=session["id"],
    format_type="json",
    output_path=f"{skill_path}/docs/analysis-thinking.json"
)
```

### 3. 思考模板应用

使用预定义的思考模板，系统化分析复杂问题。

**可用模板**：
- `problem_solving` - 问题求解模板
- `decision_making` - 决策模板
- `analysis` - 分析模板

**使用场景**：

```python
# 应用问题求解模板
session = await apply_template(
    template_id="problem_solving",
    context="如何优化技能的 Token 效率",
    session_name="token-efficiency-analysis"
)

# 模板会引导思考步骤
await sequential_thinking(
    thought="问题定义：当前 Token 效率低于 80%",
    session_id=session["id"],
    thoughtNumber=1,
    totalThoughts=6,
    nextThoughtNeeded=True
)
```

## 完整工作流

结合 Skill-Creator 工具的完整 Thinking 集成流程：

```
1. analyze_skill
   → create_session (Thinking)          # 创建分析会话
   → sequential_thinking (Thinking)     # 记录分析思考

2. 重构分析
   → sequential_thinking (Thinking)     # 记录重构思路

3. 决策制定
   → apply_template (Thinking)          # 应用决策模板
   → sequential_thinking (Thinking)     # 记录决策过程

4. export_session (Thinking)           # 导出思考文档
```

## 思考最佳实践

### 1. 结构化思考

使用清晰的思考步骤结构：

```python
# 步骤 1: 问题识别
await sequential_thinking(
    thought="识别到代码复杂度过高的问题",
    session_id=session["id"],
    thoughtNumber=1,
    totalThoughts=5,
    nextThoughtNeeded=True
)

# 步骤 2: 原因分析
await sequential_thinking(
    thought="原因是单一函数承担了过多职责",
    session_id=session["id"],
    thoughtNumber=2,
    totalThoughts=5,
    nextThoughtNeeded=True
)

# 步骤 3: 方案设计
await sequential_thinking(
    thought="建议拆分为多个小函数",
    session_id=session["id"],
    thoughtNumber=3,
    totalThoughts=5,
    nextThoughtNeeded=True
)
```

### 2. 思考可视化

使用可视化工具查看思考结构：

```python
# 生成思考流程图
mermaid_graph = await visualize_session(
    session_id=session["id"],
    format_type="mermaid"
)

# 生成树状结构
tree = await visualize_session(
    session_id=session["id"],
    format_type="tree"
)
```

### 3. 思考断点续传

支持长时间思考的断点续传：

```python
# 暂停思考
await update_session_status(
    session_id=session["id"],
    status="active"
)

# 恢复思考
resume_info = await resume_session(session_id=session["id"])
# 继续从上次停止的地方思考
```

## 集成收益对比

| 维度 | 无集成 | 有集成 |
|------|--------|--------|
| 决策追溯 | 无 | 完整思考文档 |
| 知识传递 | 口头/文档 | 思考过程记录 |
| 团队协作 | 讨论会 | 共享思考会话 |
| 审查效率 | 需要重新分析 | 查看思考记录 |

## 参考链接

- **[Thinking 分析示例](../examples/thinking-analysis.md)** - 思考过程记录
- **[Thinking 导出示例](../examples/thinking-export.md)** - 思考会话导出
- **[MCP 集成指南](mcp-tools-reference.md)** - MCP 基础配置
