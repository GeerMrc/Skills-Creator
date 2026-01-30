---
name: skill-creator
version: 0.3.6
description: |
  Agent-Skills 开发与质量保证工具。通过 MCP 工具提供技能初始化、需求澄清、规范验证、结构分析、重构建议和模板生成功能。

  何时使用：
  - 需求澄清：通过 AI 对话收集技能创建所需信息
  - 创建新的 Agent-Skill 项目结构
  - 验证技能是否符合渐进式披露规范
  - 分析技能的 token 效率和结构质量
  - 获取基于最佳实践的重构建议
  - 访问技能模板和最佳实践指南

  触发词：
  - 需求澄清
  - 技能创建
  - 技能初始化
  - 技能验证
  - 技能分析
  - 技能重构
  - 技能模板
allowed-tools: Read, Write, Edit, Bash, Glob, Grep
mcp_servers: ["skill-creator"]
---

# Skill-Creator - Agent-Skills 开发工具

## 技能概述

Skill-Creator 是一个混合架构的元技能，结合 MCP Server 和 Agent-Skill 的优势，提供专业的 Agent-Skills 开发与质量保证能力。通过 MCP 工具执行原子操作，通过 Agent-Skill 编排工作流程。

## 核心能力

需求澄清 | 技能初始化 | 规范验证 | 结构分析 | 重构建议 | 模板资源 | 最佳实践

## 快速开始

**需求澄清**: "我想创建一个技能，帮我梳理需求"
**创建技能**: "创建一个名为 'git-helper' 的技能"
**验证技能**: "验证 /path/to/skill"
**分析质量**: "分析 /path/to/skill"
**打包分发**: "打包 /path/to/skill" 或 "标准打包 /path/to/skill"

> 详见：[打包规范](references/packaging.md) | [示例文档索引](examples/README.md)

### 配置选项

可通过 `SKILL_CREATOR_OUTPUT_DIR` 环境变量统一管理技能输出位置。

> **注意**: Skill-Creator 专注于 Agent-Skills 开发核心功能。外部 MCP（如 GitHub、Thinking）集成属于可选的高级用法，不包含在核心功能中。
>
> 详见：[打包规范](references/packaging.md) | [MCP 工具参考](references/mcp-tools-reference.md) | [示例文档索引](examples/README.md)

## 工作流程

```
需求澄清 → 技能初始化 → 选择模板 → 生成结构 → 开发内容 → 验证规范 → 分析优化 → 重构改进
```

### 需求澄清流程

**基础模式（5步）** | **完整模式（10步）** | **动态模式（Brainstorm/Progressive）**

> 详见：[需求收集指南](references/requirement-collection-guide.md)

## MCP 组件

**原子工具 (12)**:

| 类别 | 工具 |
|------|------|
| 会话管理 (3) | create_requirement_session, get_requirement_session, update_requirement_answer |
| 问题获取 (2) | get_static_question, generate_dynamic_question |
| 验证工具 (2) | validate_answer_format, check_requirement_completeness |
| 技能工具 (4) | init_skill, validate_skill, analyze_skill, refactor_skill |
| 打包工具 (1) | package_skill |

**资源 (4)**: templates列表 | template内容 | best_practices | validation_rules

**Prompts (3)**: create-skill | validate-skill | refactor_skill

## 详细文档

### 文档索引

- **[引用文档索引](references/README.md)** - 所有引用文档的分类导航
- **[示例文档索引](examples/README.md)** - 所有使用示例的分类导航

### 核心文档

- **[需求收集指南](references/requirement-collection-guide.md)** - AI 对话式需求收集流程详解
- **[MCP 工具参考](references/mcp-tools-reference.md)** - MCP 工具完整参考和工作流集成
- **[最佳实践 - 核心原则](references/best-practices-core.md)** - 渐进式披露架构、描述写作规范
- **[最佳实践 - 高级技巧](references/best-practices-advanced.md)** - Token 优化、脚本黑盒化、反模式
- **[验证规范](references/validation.md)** - 命名规则、描述标准、结构检查清单
- **[验证实施指南](references/validation-guide.md)** - 等级划分、常见问题、自动化验证示例

## 架构说明

Skill-Creator 采用混合架构：**MCP Server** 提供原子操作（12 工具 + 4 资源 + 3 Prompts），**Agent-Skill** 负责工作流编排和知识传递。

**职责边界**（符合 ADR 001）：
- **MCP Server**: 原子操作 + 文件I/O + 数据验证（不包含工作流逻辑、不传递业务知识）
- **Agent-Skill**: 工作流编排 + 最佳实践 + 渐进式披露（不直接执行文件I/O）

**需求收集工作流示例**：
- MCP 提供 7 个原子工具（会话管理、问题获取、验证）
- Agent-Skill 编排完整收集流程（循环、验证、重试、提供建议）
- 详见：[需求收集指南](references/requirement-collection-guide.md)

> 详见：[混合架构设计](references/architecture.md) | [协同示例](examples/mcp-skill-collaboration.md)
