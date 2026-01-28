# 混合架构设计

> **本文档摘自 ADR 001，详见在线完整版本**
> **完整版本**: [ADR 001: MCP Server + Agent-Skill 混合架构](https://github.com/your-repo/blob/main/docs/adr/001-hybrid-architecture.md)

---

## 架构概述

Skills-Creator 采用 **混合架构**：MCP Server + Agent-Skill

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
│  │  - 原子操作工具 (18 Tools)                             │ │
│  │  - 只读资源 (4 Resources)                              │ │
│  │  - 可重用模板 (3 Prompts)                              │ │
│  └─────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────┘
```

---

## 职责边界

| 组件 | 职责 | 边界 |
|------|------|------|
| **MCP Server** | - 执行原子操作<br>- 处理文件 I/O<br>- 数据验证 | - 不包含工作流逻辑<br>- 不传递业务知识 |
| **Agent-Skill** | - 编排工作流程<br>- 传递最佳实践<br>- 渐进式披露 | - 不直接执行文件 I/O<br>- 不重复实现工具功能 |

---

## 核心优势

### 1. 职责分离
- MCP Server 专注于可执行的原子操作
- Agent-Skill 专注于工作流编排和知识传递
- 两者可独立开发、测试、部署

### 2. Token 效率
- Agent-Skill 保持轻量 (SKILL.md ≤150行)
- MCP Server 代码不加载到上下文
- 引用文件按需加载

### 3. 符合 MCP 生态
- 遵循 MCP 协议标准
- 可被 MCP Inspector 测试
- 可集成到 Claude Desktop

---

## MCP Server 组件

**工具列表**（18个核心工具）:
- 技能工具（4个）: `init_skill`, `validate_skill`, `analyze_skill`, `refactor_skill`
- 打包工具（2个）: `package_skill`, `package_agent_skill`
- 需求收集（7个）: 会话管理、问题获取、验证工具
- 批量操作（2个）: `batch_validate_skills`, `batch_analyze_skills`
- 健康检查（3个）: `health_check`, `quick_status`, `is_healthy`

**资源列表**（4个只读资源）:
- `skill://schema/templates` - 模板列表
- `skill://schema/templates/{type}` - 特定模板内容
- `skill://schema/best-practices` - 最佳实践指南
- `skill://schema/validation-rules` - 验证规则详情

---

## Agent-Skill 组件

**触发词**:
- 技能创建
- 技能验证
- 技能分析
- 技能重构
- 需求澄清

**工作流编排**:
1. 理解用户意图
2. 调用相应的 MCP 工具
3. 解读工具返回结果
4. 结合最佳实践知识
5. 提供可执行建议

---

## 使用示例

### 技能初始化流程

```
用户: "创建一个新技能"
  ↓
Agent-Skill: 理解意图，询问技能名称和类型
  ↓
MCP Server: 执行 init_skill(name, template)
  ↓
Agent-Skill: 解读结果，提供后续指导
```

### 技能验证流程

```
用户: "验证我的技能"
  ↓
Agent-Skill: 分析技能结构
  ↓
MCP Server: 执行 validate_skill(skill_path)
  ↓
Agent-Skill: 解读验证报告，提供修复建议
```

---

## 质量指标

| 组件 | 覆盖率 | 测试数 |
|------|--------|--------|
| MCP Server | 96% | 594 |
| Agent-Skill | 100% | 文档验证 |

| 检查项 | 结果 |
|--------|------|
| Ruff | 0 错误 ✅ |
| Mypy | 0 错误 ✅ |
| Bandit | 0 高危 ✅ |

---

## 相关文档

- [MCP 集成指南](mcp-integration.md) - MCP 工具使用和资源访问
- [最佳实践 - 核心](best-practices-core.md) - 基础架构和规范
- [需求收集工作流](requirement-workflow.md) - 需求收集完整流程

---

**最后更新**: 2026-01-28
**版本**: v0.3.3
