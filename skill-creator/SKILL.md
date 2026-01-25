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
mcp_servers: ["skill-creator"]
---

# Skill-Creator - Agent-Skills 开发工具

## 技能概述

Skill-Creator 是一个混合架构的元技能，结合 MCP Server 和 Agent-Skill 的优势，提供专业的 Agent-Skills 开发与质量保证能力。通过 MCP 工具执行原子操作，通过 Agent-Skill 编排工作流程。

## 核心能力

1. **需求澄清** - AI 驱动的对话式需求收集，支持会话恢复和进度跟踪
2. **技能初始化** - 一键生成符合渐进式披露架构的技能目录结构
3. **规范验证** - 自动检查命名、描述、结构是否符合最佳实践
4. **批量操作** - 并发验证和分析多个技能，提高效率
5. **健康检查** - 系统监控、性能指标、缓存统计
6. **结构分析** - 分析 token 效率、识别常见反模式
7. **重构建议** - 基于官方规范提供具体的改进建议
8. **模板资源** - 访问四种预定义技能模板（minimal/tool-based/workflow-based/analyzer-based）
9. **最佳实践** - 内置完整的开发规范和验证标准

## 快速开始

### 需求澄清（推荐）

```
"我想创建一个技能，帮我梳理需求"
```

通过 AI 对话逐步收集技能名称、功能、使用场景、模板类型等关键信息。

### 创建新技能

```
"创建一个名为 'git-helper' 的技能"
```

选择模板类型，自动生成目录结构和 SKILL.md 模板。

### 验证现有技能

```
"验证 /path/to/skill"
```

获取包含命名、描述、结构分析的完整验证报告。

### 分析技能质量

```
"分析 /path/to/skill"
```

识别 token 效率问题和结构反模式。

### 批量验证多个技能

```
"批量验证 /path/to/skill1 /path/to/skill2 /path/to/skill3"
```

并发验证多个技能，提高验证效率（支持并发控制）。

### 系统健康检查

```
"健康检查"
```

获取系统健康状态、CPU/内存使用率、缓存统计等性能指标。

> 详见：[批量操作示例](examples/mcp-batch-operations.md) | [健康检查示例](examples/mcp-health-check.md) | [缓存机制指南](references/cache-mechanism.md)

## 工作流程

```
需求澄清 → 技能初始化 → 选择模板 → 生成结构 → 开发内容 → 验证规范 → 分析优化 → 重构改进
```

### 需求澄清流程

AI 驱动的需求澄清工具 `collect_requirements`，支持基础/完整/头脑风暴/渐进式 4 种模式。

> 详见：[需求澄清指南](references/requirement-collection.md) | [回退机制说明](references/fallback-mechanism.md)

## MCP 工具集成

本技能通过 skill-creator-mcp 提供的 MCP 工具执行操作：

| 工具 | 功能 |
|------|------|
| `collect_requirements` | **需求澄清** - AI 对话式收集技能创建信息 |
| `init_skill` | 初始化新技能结构 |
| `validate_skill` | 验证技能规范 |
| `analyze_skill` | 分析技能质量 |
| `refactor_skill` | 生成重构建议 |
| `package_skill` | 打包技能为分发格式 |
| `batch_validate_skills_tool` | **批量验证** - 并发验证多个技能（支持并发控制） |
| `batch_analyze_skills_tool` | **批量分析** - 并发分析多个技能（支持并发控制） |
| `health_check_tool` | **健康检查** - 系统健康状态、性能指标、缓存统计 |
| `quick_status_tool` | **快速状态** - 系统状态摘要（CPU、内存、请求数） |
| `is_healthy_tool` | **健康判断** - 快速判断系统是否健康 |

## MCP 资源访问

| 资源 URI | 内容 |
|----------|------|
| `http://skills/schema/templates` | 所有可用模板列表 |
| `http://skills/schema/templates/{type}` | 指定类型技能模板内容 |
| `http://skills/schema/best-practices` | 最佳实践指南 |
| `http://skills/schema/validation-rules` | 验证规则详情 |

## MCP Prompts 模板

| Prompt 名称 | 功能 |
|-------------|------|
| `create-skill` | 创建新技能的引导提示模板 |
| `validate-skill` | 验证技能的引导提示模板 |
| `refactor-skill` | 重构技能的引导提示模板 |

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

Skill-Creator 采用混合架构：**MCP Server** 提供原子操作（11 工具 + 4 资源 + 3 Prompts），**Agent-Skill** 负责工作流编排和知识传递。

详见：[混合架构 ADR](../docs/adr/001-hybrid-architecture.md) | [协同示例](examples/mcp-skill-collaboration.md) | [需求收集示例](examples/requirement-collection-basic.md)
