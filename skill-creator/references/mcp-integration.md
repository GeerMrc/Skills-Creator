# MCP 集成指南

## 概述

Skill-Creator 采用混合架构：MCP Server 提供工具和资源，Agent-Skill 负责工作流编排。本文档说明如何配置和使用 MCP 组件。

> **示例代码**：查看 [MCP 使用示例](../examples/mcp-usage-examples.md) 获取完整的代码示例和用法。

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
        "/path/to/Skills-Creator/skill-creator-mcp",
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

可通过环境变量自定义行为：

| 环境变量 | 说明 | 默认值 |
|---------|------|--------|
| `SKILL_CREATOR_LOG_LEVEL` | 日志级别 | INFO |
| `SKILL_CREATOR_LOG_FORMAT` | 日志格式 | default |
| `SKILL_CREATOR_LOG_FILE` | 日志文件路径 | 无（输出到 stderr） |
| `SKILL_CREATOR_OUTPUT_DIR` | 默认输出目录 | 当前目录 |

### 验证连接

启动 Claude Code 后，MCP Server 会自动连接。验证方法：

**方法 1：MCP Inspector**
```bash
npx @modelcontextprotocol/inspector /path/to/skill-creator-mcp/src/skill_creator_mcp
```

**方法 2：检查工具可用性**
在 Claude Code 对话中尝试调用 MCP 工具。

## MCP 工具

### 可用工具列表

| 工具 | 功能 |
|------|------|
| `init_skill` | 初始化新技能结构 |
| `validate_skill` | 验证技能规范 |
| `analyze_skill` | 分析技能质量 |
| `refactor_skill` | 生成重构建议 |
| `package_skill` | 打包技能为分发格式 |

### init_skill

**功能**：创建符合规范的技能目录结构

**参数**：
- `name` (string): 技能名称，使用 kebab-case
- `template` (string): 模板类型 (minimal/tool-based/workflow-based/analyzer-based)
- `path` (string, 可选): 创建路径，默认当前目录

**返回**：创建的文件列表

### validate_skill

**功能**：检查技能是否符合最佳实践

**参数**：
- `skill_path` (string): 技能目录路径
- `check_structure` (bool, 可选): 是否检查目录结构（默认 True）
- `check_content` (bool, 可选): 是否检查内容格式（默认 True）

**返回**：验证报告，包含问题列表和建议

### analyze_skill

**功能**：分析技能的 token 效率和结构质量

**参数**：
- `skill_path` (string): 技能目录路径

**返回**：分析报告，包含指标和改进建议

**报告内容**：
- Token 效率评分
- 文件大小统计
- 反模式识别
- 优化建议

### refactor_skill

**功能**：基于最佳实践生成重构建议

**参数**：
- `skill_path` (string): 技能目录路径
- `focus` (list, 可选): 重点关注领域

**返回**：重构建议报告

### package_skill

**功能**：打包 Agent-Skill 为分发格式

**参数**：
- `skill_path` (string): 技能目录路径
- `output_dir` (string, 可选): 输出目录路径（默认：当前目录）
- `format` (string, 可选): 打包格式（zip/tar.gz/tar.bz2，默认：zip）
- `include_tests` (bool, 可选): 是否包含测试文件（默认：True）
- `validate_before_package` (bool, 可选): 打包前是否验证（默认：True）

**返回**：打包结果

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

## MCP Prompts

### 可用 Prompts

| Prompt | 用途 |
|--------|------|
| `create-skill` | 指导 AI 创建新技能 |
| `validate-skill` | 指导 AI 验证技能质量 |
| `refactor-skill` | 指导 AI 生成重构建议 |

### create-skill Prompt

**参数**：
- `name` - 技能名称
- `template` - 模板类型

### validate-skill Prompt

**参数**：
- `skill_path` - 技能路径
- `template` - 模板类型（可选）

### refactor-skill Prompt

**参数**：
- `skill_path` - 技能路径
- `focus` - 重点关注领域（可选）

## 工作流集成

### 标准开发流程

```
1. init_skill(name, template)    # 初始化结构
2. 编写 SKILL.md 和引用文件
3. validate_skill(skill_path)    # 验证规范
4. analyze_skill(skill_path)     # 分析质量
5. refactor_skill(skill_path)    # 获取改进建议
6. 修改并重复验证
```

### Claude Code 中使用

**创建技能**：
```
你：创建一个名为 pdf-helper 的技能
Claude：[调用 init_skill 工具]
```

**验证技能**：
```
你：验证 /path/to/skill
Claude：[调用 validate_skill 工具]
```

**分析质量**：
```
你：分析 /path/to/skill 的质量
Claude：[调用 analyze_skill 工具]
```

## 错误处理

### 常见错误及解决

| 错误 | 原因 | 解决方案 |
|------|------|----------|
| `Tool 'init_skill' not found` | MCP Server 未连接 | 检查配置，确保 MCP Server 已启动 |
| `Skill path not found` | 技能路径不存在 | 确认路径正确，使用绝对路径 |
| `Unknown template type` | 模板类型无效 | 使用有效模板：minimal/tool-based/workflow-based/analyzer-based |

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

## 高级用法

### 批量验证

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

### 缓存资源

频繁访问的资源可以缓存：
```python
# 首次读取
best_practices = await session.read_resource("skill://best-practices")

# 后续使用缓存内容
cached_practices = best_practices.contents[0].text
```

## 相关文档

- **[MCP 使用示例](../examples/mcp-usage-examples.md)** - 完整代码示例
- **[最佳实践 - 核心](best-practices-core.md)** - 开发规范
- **[最佳实践 - 高级](best-practices-advanced.md)** - Token 优化和高级技巧
- **[验证规范](validation.md)** - 验证规则
- **[验证实施指南](validation-guide.md)** - 等级划分和 CI/CD 集成
