---
name: skill-creator
description: |
  Agent-Skills 开发与质量保证工具。通过 MCP 工具提供技能初始化、规范验证、结构分析、重构建议和模板生成功能。

  何时使用：
  - 创建新的 Agent-Skill 项目结构
  - 验证技能是否符合渐进式披露规范
  - 分析技能的 token 效率和结构质量
  - 获取基于最佳实践的重构建议
  - 访问技能模板和最佳实践指南

  触发词：
  - 创建技能
  - 初始化技能
  - 验证技能
  - 分析技能
  - 重构技能
  - 技能模板
allowed-tools: Read, Write, Edit, Bash, Glob, Grep
mcp_servers: ["skill-creator"]
---

# Skill-Creator - Agent-Skills 开发工具

## 技能概述

Skill-Creator 是一个混合架构的元技能，结合 MCP Server 和 Agent-Skill 的优势，提供专业的 Agent-Skills 开发与质量保证能力。通过 MCP 工具执行原子操作，通过 Agent-Skill 编排工作流程。

## 核心能力

1. **技能初始化** - 一键生成符合渐进式披露架构的技能目录结构
2. **规范验证** - 自动检查命名、描述、结构是否符合最佳实践
3. **结构分析** - 分析 token 效率、识别常见反模式
4. **重构建议** - 基于官方规范提供具体的改进建议
5. **模板资源** - 访问四种预定义技能模板（minimal/tool-based/workflow-based/analyzer-based）
6. **最佳实践** - 内置完整的开发规范和验证标准

## 快速开始

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

## 工作流程

```
初始化 → 选择模板 → 生成结构 → 开发内容 → 验证规范 → 分析优化 → 重构改进
```

## MCP 工具集成

本技能通过 skill-creator-mcp 提供的 MCP 工具执行操作：

| 工具 | 功能 |
|------|------|
| `init_skill` | 初始化新技能结构 |
| `validate_skill` | 验证技能规范 |
| `analyze_skill` | 分析技能质量 |
| `refactor_skill` | 生成重构建议 |
| `package_skill` | 打包技能为分发格式 |

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

- **[MCP 集成指南](references/mcp-integration.md)** - MCP 工具使用、资源访问、配置方法
- **[最佳实践](references/best-practices.md)** - 渐进式披露、描述写作、组织原则
- **[验证规范](references/validation.md)** - 命名规则、描述标准、结构检查清单
- **[验证实施指南](references/validation-guide.md)** - 等级划分、常见问题、自动化验证示例

## 架构说明

Skill-Creator 采用混合架构：
- **skill-creator-mcp** - MCP Server，提供可执行的工具和只读资源
- **skill-creator** - Agent-Skill，编排 MCP 工具，提供工作流和知识组织
