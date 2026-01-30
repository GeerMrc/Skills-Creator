# 混合架构设计

> **版本**: v0.3.4
> **架构类型**: MCP Server + Agent-Skill 混合架构
> **更新日期**: 2026-01-30

---

## 架构概述

Skills-Creator 采用 **混合架构**，结合 MCP Server 和 Agent-Skill 的优势，提供专业的 Agent-Skills 开发与质量保证能力。

```
┌─────────────────────────────────────────────────────────────┐
│                     Claude Code / Desktop                    │
│                                                              │
│  ┌────────────────────────────────────────────────────────┐ │
│  │          Agent-Skill (skill-creator)                   │ │
│  │  - 编排工作流程                                        │ │
│  │  - 渐进式披露知识                                      │ │
│  │  - 最佳实践指导                                        │ │
│  └────────────────────┬───────────────────────────────────┘ │
│                         │ 调用                                │
│  ┌────────────────────▼───────────────────────────────────┐ │
│  │         MCP Server (skill-creator-mcp)                 │ │
│  │  - 原子操作工具 (12 Tools)                              │ │
│  │  - 只读资源 (4 Resources)                               │ │
│  │  - 可重用模板 (3 Prompts)                               │ │
│  └─────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────┘
```

---

## 职责边界

### MCP Server 职责

| 功能 | 说明 | 边界 |
|------|------|------|
| **原子操作** | 执行具体的工具功能 | 不包含工作流逻辑 |
| **文件 I/O** | 处理文件读写操作 | 不传递业务知识 |
| **数据验证** | 输入输出数据验证 | 不包含业务规则 |

**边界原则**：
- ❌ 不包含工作流编排逻辑
- ❌ 不传递 Agent-Skill 特定知识
- ❌ 不依赖 Agent-Skill 存在

### Agent-Skill 职责

| 功能 | 说明 | 边界 |
|------|------|------|
| **工作流编排** | 编排多个 MCP 工具完成任务 | 不直接执行文件 I/O |
| **知识传递** | 渐进式披露最佳实践 | 不重复实现工具功能 |
| **用户交互** | 处理用户输入和反馈 | 不直接操作文件系统 |

**边界原则**：
- ❌ 不直接执行文件 I/O 操作
- ❌ 不重复实现 MCP 工具功能
- ✅ 通过 MCP 工具完成实际操作

---

## 协同示例

### 需求收集工作流

```python
# Agent-Skill 编排工作流（伪代码）

# 1. 创建会话（调用 MCP）
session = await create_requirement_session(mode="complete")

# 2. 循环获取问题（调用 MCP）
for step in range(10):
    question = await get_static_question(mode="complete", step=step)
    # Agent-Skill 处理用户输入...
    await update_requirement_answer(session_id, key, answer)

# 3. 检查完整性（调用 MCP）
completeness = await check_requirement_completeness(answers)

# 4. 提供建议（Agent-Skill 知识）
if completeness["is_complete"]:
    suggest_next_steps(answers)  # Agent-Skill 内部逻辑
```

**协同点**：
- MCP 提供：原子工具（会话管理、问题获取、验证）
- Agent-Skill 提供：循环逻辑、用户交互、最佳实践建议

---

## 架构优势

### 1. 职责分离

- **MCP Server**：专注于可执行的原子操作
- **Agent-Skill**：专注于工作流编排和知识传递
- 两者可独立开发、测试、部署

### 2. 可复用性

- MCP Server 可被其他 Agent-Skill 或直接使用
- Agent-Skill 可切换到不同的 MCP 实现
- 工具和资源可被其他项目复用

### 3. Token 效率

- Agent-Skill 保持轻量 (SKILL.md ≤150行)
- MCP Server 代码不加载到上下文
- 引用文件按需加载

### 4. 符合 MCP 生态

- 遵循 MCP 协议标准
- 可被 MCP Inspector 测试
- 可集成到 Claude Desktop

### 5. 测试友好

- MCP Server 可独立测试 (97% 覆盖率, 568个测试)
- Agent-Skill 可单独验证
- 工具和资源可被 CI/CD 集成

---

## 权衡与缓解

| 方面 | 优势 | 劣势 | 缓解措施 |
|------|------|------|----------|
| **复杂度** | 职责清晰 | 需维护两套代码 | 清晰的接口定义 |
| **部署** | MCP Server 可独立升级 | 需同时部署两组件 | 版本兼容性管理 |
| **学习曲线** | 符合 MCP 标准 | 新概念较多 | 提供完整文档 |

---

## 相关文档

- **[MCP 集成指南](mcp-tools-reference.md)** - MCP 工具使用说明
- **[最佳实践 - 核心](best-practices-core.md)** - 渐进式披露架构
- **[需求收集指南](requirement-collection-guide.md)** - 完整工作流示例
- **[MCP-Skill 协作示例](../examples/mcp-skill-collaboration.md)** - 实际集成案例
