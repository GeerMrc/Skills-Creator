---
name: skill-creator
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
  - 批量验证
  - 技能分析
  - 批量分析
  - 技能重构
  - 技能模板
  - 健康检查
  - 系统监控
allowed-tools: Read, Write, Edit, Bash, Glob, Grep
mcp_servers: ["skill-creator", "GitHub", "Thinking"]
---

# Skill-Creator - Agent-Skills 开发工具

## 技能概述

Skill-Creator 是一个混合架构的元技能，结合 MCP Server 和 Agent-Skill 的优势，提供专业的 Agent-Skills 开发与质量保证能力。通过 MCP 工具执行原子操作，通过 Agent-Skill 编排工作流程。

## 核心能力

需求澄清 | 技能初始化 | 规范验证 | 批量操作 | 健康检查 | 结构分析 | 重构建议 | 模板资源 | 最佳实践

## 快速开始

**需求澄清**: "我想创建一个技能，帮我梳理需求"
**创建技能**: "创建一个名为 'git-helper' 的技能"
**验证技能**: "验证 /path/to/skill"
**分析质量**: "分析 /path/to/skill"
**批量操作**: "批量验证 /path/to/skill1 /path/to/skill2"
**健康检查**: "健康检查"
**打包分发**: "打包 /path/to/skill" 或 "标准打包 /path/to/skill"

> 详见：[批量操作示例](examples/mcp-batch-operations.md) | [健康检查示例](examples/mcp-health-check.md) | [打包规范](references/packaging.md)

### 环境配置（推荐）

设置 `SKILL_CREATOR_OUTPUT_DIR` 环境变量，统一管理技能输出位置：

```bash
# 添加到 ~/.bashrc 或 ~/.zshrc
export SKILL_CREATOR_OUTPUT_DIR=~/my-skills
```

这样所有通过 `init_skill`、`package_skill`、`package_agent_skill` 创建的技能都会输出到指定目录。

> 详见：[MCP 集成指南 - 路径解析规则](references/mcp-integration.md#路径解析规则)

## 工作流程

```
需求澄清 → 技能初始化 → 选择模板 → 生成结构 → 开发内容 → 验证规范 → 分析优化 → 重构改进
```

### 需求澄清流程

当用户说"帮我收集需求"时：

**1. 基础模式（5步）**
- 调用 `create_requirement_session(mode="basic")` 创建会话
- 循环调用 `get_static_question()` 获取预定义问题
- 验证答案：`validate_answer_format()`
- 保存答案：`update_requirement_answer()`
- 完成后检查：`check_requirement_completeness()`

**2. 完整模式（10步）**
- 与基础模式相同，但包含更多问题

**3. 动态模式（Brainstorm/Progressive）**
- 调用 `generate_dynamic_question()` 使用 LLM 生成问题
- 开放式探索（Brainstorm）或自适应提问（Progressive）
- 结合对话历史和已收集信息

**4. 结合最佳实践知识**
- 根据收集到的需求提供可执行建议
- 参考 `references/requirement-workflow.md` 获取完整工作流指南

> 详见：[需求收集工作流指南](references/requirement-workflow.md) | [需求澄清指南](references/requirement-collection.md) | [回退机制说明](references/fallback-mechanism.md)

## MCP 组件

**原子工具 (23)**:

**会话管理 (3)**:
- create_requirement_session_tool - 创建需求收集会话
- get_requirement_session_tool - 获取会话状态
- update_requirement_answer_tool - 更新会话答案

**问题获取 (2)**:
- get_static_question_tool - 获取静态问题（basic/complete模式）
- generate_dynamic_question_tool - 生成动态问题（brainstorm/progressive模式）

**验证工具 (2)**:
- validate_answer_format_tool - 验证答案格式
- check_requirement_completeness_tool - 检查需求完整性（LLM）

**技能工具 (4)**: init_skill | validate_skill | analyze_skill | refactor_skill

**打包工具 (2)**: package_skill | package_agent_skill

**批量操作 (2)**: batch_validate_skills_tool | batch_analyze_skills_tool

**健康检查 (3)**: health_check_tool | quick_status_tool | is_healthy_tool

**技术验证 (5)**: check_client_capabilities | test_llm_sampling | test_user_elicitation | test_conversation_loop | test_requirement_completeness

> 注：7个需求收集原子工具 + 16个其他工具

**资源 (4)**: templates列表 | template内容 | best_practices | validation_rules

**Prompts (3)**: create-skill | validate-skill | refactor-skill

## 详细文档

### 文档索引

- **[引用文档索引](references/README.md)** - 所有引用文档的分类导航
- **[示例文档索引](examples/README.md)** - 所有使用示例的分类导航

### 核心文档

- **[回退机制说明](references/fallback-mechanism.md)** - 客户端限制与自动降级策略
- **[需求澄清指南](references/requirement-collection.md)** - AI 对话式需求收集流程详解
- **[MCP 集成指南](references/mcp-integration.md)** - MCP 工具使用、资源访问、配置方法
- **[最佳实践 - 核心原则](references/best-practices-core.md)** - 渐进式披露架构、描述写作规范
- **[最佳实践 - 高级技巧](references/best-practices-advanced.md)** - Token 优化、脚本黑盒化、反模式
- **[验证规范](references/validation.md)** - 命名规则、描述标准、结构检查清单
- **[验证实施指南](references/validation-guide.md)** - 等级划分、常见问题、自动化验证示例

## 架构说明

Skill-Creator 采用混合架构：**MCP Server** 提供原子操作（18 工具 + 4 资源 + 3 Prompts），**Agent-Skill** 负责工作流编排和知识传递。

**职责边界**（符合 ADR 001）：
- **MCP Server**: 原子操作 + 文件I/O + 数据验证（不包含工作流逻辑、不传递业务知识）
- **Agent-Skill**: 工作流编排 + 最佳实践 + 渐进式披露（不直接执行文件I/O）

**需求收集工作流示例**：
- MCP 提供 7 个原子工具（会话管理、问题获取、验证）
- Agent-Skill 编排完整收集流程（循环、验证、重试、提供建议）
- 详见：[需求收集工作流指南](references/requirement-workflow.md)

详见：[混合架构 ADR](../docs/adr/001-hybrid-architecture.md) | [协同示例](examples/mcp-skill-collaboration.md)

## 配置与安装

> 📘 完整的配置和安装指南请参考 [MCP Server 文档](../skill-creator-mcp/docs/README.md)
