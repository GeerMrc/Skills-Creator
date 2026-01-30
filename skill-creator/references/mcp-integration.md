# MCP 集成指南

## 概述

Skill-Creator 采用混合架构：MCP Server 提供工具和资源，Agent-Skill 负责工作流编排。本文档说明如何配置和使用 MCP 组件。

> **示例代码**：查看 [MCP 使用示例](../examples/mcp-usage-examples.md) 获取完整的代码示例和用法。

> **高级用法**：查看 [MCP 高级用法](mcp-advanced-usage.md) 了解错误处理、性能优化和调试技巧。

---

## MCP Server 配置

### Claude Code 配置

在 Claude Code 配置文件中添加 skill-creator-mcp：

```json
{
  "mcpServers": {
    "skill-creator": {
      "command": "uv",
      "args": [
        "--directory",
        "$PROJECT_ROOT/skill-creator-mcp",
        "run",
        "python",
        "-m",
        "skill_creator_mcp"
      ]
    }
  }
}
```

**配置说明**：
- `command`: 使用 `uv` 作为命令运行器
- `--directory`: 指向 skill-creator-mcp 项目目录
- `run python -m`: 运行 Python 模块
- `skill_creator_mcp`: MCP Server 入口模块

### 环境变量配置

| 环境变量 | 说明 | 默认值 | 工具支持 |
|---------|------|--------|----------|
| `SKILL_CREATOR_LOG_LEVEL` | 日志级别 | INFO | - |
| `SKILL_CREATOR_LOG_FORMAT` | 日志格式 | default | - |
| `SKILL_CREATOR_LOG_FILE` | 日志文件路径 | 无（输出到 stderr） | - |
| `SKILL_CREATOR_OUTPUT_DIR` | 默认输出目录 | ~/skills（自动创建） | `init_skill_tool`, `package_skill` |

### 路径解析规则

**重要说明**: `output_dir` 参数是相对于 **MCP Server 启动目录** 的路径，而非用户当前目录。

**配置优先级**:
```
工具参数 output_dir > 环境变量 SKILL_CREATOR_OUTPUT_DIR > 默认值 "~/skills"
```

**推荐做法**:
1. 设置环境变量统一管理输出目录（推荐）:
   ```bash
   export SKILL_CREATOR_OUTPUT_DIR=~/my-skills
   ```

2. 使用绝对路径避免歧义:
   ```python
   init_skill_tool(name="test", output_dir="~/project")
   ```

### 验证连接

**方法 1：MCP Inspector**
```bash
npx @modelcontextprotocol/inspector /path/to/skill-creator-mcp/src/skill_creator_mcp
```

**方法 2：检查工具可用性**
在 Claude Code 对话中尝试调用 MCP 工具。

---

## MCP 工具

### 可用工具列表

MCP Server 提供 **12个工具**，按功能划分为3类：

#### 技能工具（4个）

| 工具 | 功能 |
|------|------|
| `init_skill_tool` | 初始化新技能结构 |
| `validate_skill_tool` | 验证技能规范 |
| `analyze_skill_tool` | 分析技能质量 |
| `refactor_skill_tool` | 生成重构建议 |

#### 需求收集原子工具（7个）

| 工具 | 功能 |
|------|------|
| `create_requirement_session_tool` | 创建需求收集会话 |
| `get_requirement_session_tool` | 获取会话状态 |
| `update_requirement_answer_tool` | 更新需求答案 |
| `get_static_question_tool` | 获取静态问题（basic/complete模式） |
| `generate_dynamic_question_tool` | 生成动态问题（brainstorm/progressive模式） |
| `validate_answer_format_tool` | 验证答案格式 |
| `check_requirement_completeness_tool` | 检查需求完整性 |

#### 打包工具（1个）

| 工具 | 功能 |
|------|------|
| `package_skill` | 打包技能为分发格式 |

### 工具命名约定

**规范**：
- MCP Server 工具函数名使用 `_tool` 后缀（如 `init_skill_tool`）
- 文档中引用工具时应使用完整工具名（带 `_tool` 后缀）
- **例外**：`package_skill` 工具为历史兼容保留，无 `_tool` 后缀

**工具名映射**：

| 简称（不推荐） | 完整工具名（推荐） |
|---------------|------------------|
| init_skill | init_skill_tool |
| validate_skill | validate_skill_tool |
| analyze_skill | analyze_skill_tool |
| refactor_skill | refactor_skill_tool |
| package_skill | package_skill（无后缀） |
| create_requirement_session | create_requirement_session_tool |
| get_requirement_session | get_requirement_session_tool |
| update_requirement_answer | update_requirement_answer_tool |
| get_static_question | get_static_question_tool |
| generate_dynamic_question | generate_dynamic_question_tool |
| validate_answer_format | validate_answer_format_tool |
| check_requirement_completeness | check_requirement_completeness_tool |

---

### 工具参数说明

#### init_skill_tool

**功能**：创建符合规范的技能目录结构

**参数**：
- `name` (string): 技能名称，使用 kebab-case
- `template` (string): 模板类型 (minimal/tool-based/workflow-based/analyzer-based)
- `output_dir` (string, 可选): 输出目录路径
- `with_examples` (bool, 可选): 是否包含示例（默认 False）
- `with_scripts` (bool, 可选): 是否包含脚本（默认 False）

**返回**：创建的文件列表

#### validate_skill_tool

**功能**：检查技能是否符合最佳实践

**参数**：
- `skill_path` (string): 技能目录路径
- `check_structure` (bool, 可选): 是否检查目录结构（默认 True）
- `check_content` (bool, 可选): 是否检查内容格式（默认 True）

**返回**：验证报告，包含问题列表和建议

#### analyze_skill_tool

**功能**：分析技能的 token 效率和结构质量

**参数**：
- `skill_path` (string): 技能目录路径
- `analyze_structure` (bool, 可选): 是否分析结构（默认 True）
- `analyze_complexity` (bool, 可选): 是否分析复杂度（默认 True）
- `analyze_quality` (bool, 可选): 是否分析质量（默认 True）

**返回**：分析报告

#### refactor_skill_tool

**功能**：基于最佳实践生成重构建议

**参数**：
- `skill_path` (string): 技能目录路径
- `focus` (list, 可选): 重点关注领域

**返回**：重构建议报告

#### package_skill

**功能**：打包 Agent-Skill 为分发格式

> **命名说明**：此工具是唯一不带 `_tool` 后缀的工具，为历史兼容保留。

**参数**：
- `skill_path` (string): 技能目录路径
- `output_dir` (string, 可选): 输出目录路径
- `version` (string, 可选): 版本号（仅在 strict=True 时使用）
- `format` (string, 可选): 打包格式（zip/tar.gz/tar.bz2）
- `include_tests` (bool, 可选): 是否包含测试文件（默认 False）
- `strict` (bool, 可选): 是否使用标准打包模式（默认 False）
- `validate_before_package` (bool, 可选): 打包前是否验证（默认 True）

**返回**：打包结果

---

## MCP 资源

### 可用资源

| URI | 内容 |
|-----|------|
| `http://skills/schema/templates/{type}` | 技能模板内容 |
| `http://skills/schema/best-practices` | 最佳实践指南 |
| `http://skills/schema/validation-rules` | 验证规则详情 |

### 技能模板

**可用类型**：
- `minimal` - 最小技能模板
- `tool-based` - 工具集成型模板
- `workflow-based` - 工作流型模板
- `analyzer-based` - 分析型模板

---

## MCP Prompts

### 可用 Prompts

| Prompt | 用途 |
|--------|------|
| `create-skill` | 指导 AI 创建新技能 |
| `validate-skill` | 指导 AI 验证技能质量 |
| `refactor-skill` | 指导 AI 生成重构建议 |

---

## 工作流集成

### 标准开发流程

```
1. init_skill_tool(name, template)    # 初始化结构
2. 编写 SKILL.md 和引用文件
3. validate_skill_tool(skill_path)    # 验证规范
4. analyze_skill_tool(skill_path)     # 分析质量
5. refactor_skill_tool(skill_path)    # 获取改进建议
6. 修改并重复验证
```

### Claude Code 中使用

**创建技能**：
```
你：创建一个名为 pdf-helper 的技能
Claude：[调用 init_skill_tool 工具]
```

**验证技能**：
```
你：验证 /path/to/skill
Claude：[调用 validate_skill_tool 工具]
```

**分析质量**：
```
你：分析 /path/to/skill 的质量
Claude：[调用 analyze_skill_tool 工具]
```

---

## 相关文档

### 核心文档
- **[MCP 使用示例](../examples/mcp-usage-examples.md)** - 完整代码示例
- **[MCP 高级用法](mcp-advanced-usage.md)** - 错误处理、性能优化、调试
- **[最佳实践 - 核心](best-practices-core.md)** - 开发规范
- **[最佳实践 - 高级](best-practices-advanced.md)** - Token 优化和高级技巧
- **[验证规范](validation.md)** - 验证规则
