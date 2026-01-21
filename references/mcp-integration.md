# MCP 集成指南

## 概述

Skill-Creator 采用混合架构：MCP Server 提供工具和资源，Agent-Skill 负责工作流编排。本文档说明如何使用 MCP 组件。

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

### 验证连接

启动 Claude Code 后，MCP Server 会自动连接。可通过 MCP Inspector 验证：

```bash
npx @modelcontextprotocol/inspector /path/to/skill-creator-mcp/src/skill_creator_mcp
```

## MCP 工具使用

### init_skill - 初始化技能

**功能**：创建符合规范的技能目录结构

**参数**：
- `name` (string): 技能名称，使用 kebab-case
- `template` (string): 模板类型 (minimal/tool-based/workflow-based/analyzer-based)
- `path` (string, 可选): 创建路径，默认当前目录

**返回**：创建的文件列表

**示例**：
```python
# 创建最小技能
init_skill(name="git-helper", template="minimal")

# 创建工具集成型技能
init_skill(name="container-manager", template="tool-based", path="./skills")
```

### validate_skill - 验证技能

**功能**：检查技能是否符合最佳实践

**参数**：
- `skill_path` (string): 技能目录路径
- `template` (string, 可选): 验证使用的模板类型

**返回**：验证报告，包含问题列表和建议

**示例**：
```python
# 验证技能
validate_skill(skill_path="/path/to/skill")

# 验证特定模板类型
validate_skill(skill_path="/path/to/skill", template="tool-based")
```

**报告结构**：
```json
{
  "valid": true,
  "issues": [],
  "warnings": [
    {
      "category": "description",
      "message": "描述缺少使用场景",
      "suggestion": "添加 '何时使用' 章节"
    }
  ],
  "score": 85
}
```

### analyze_skill - 分析技能

**功能**：分析技能的 token 效率和结构质量

**参数**：
- `skill_path` (string): 技能目录路径

**返回**：分析报告，包含指标和改进建议

**示例**：
```python
# 分析技能
analyze_skill(skill_path="/path/to/skill")
```

**报告内容**：
- Token 效率评分
- 文件大小统计
- 反模式识别
- 优化建议

### refactor_skill - 重构建议

**功能**：基于最佳实践生成重构建议

**参数**：
- `skill_path` (string): 技能目录路径
- `focus` (list, 可选): 重点关注领域

**返回**：重构建议报告

**示例**：
```python
# 获取全面重构建议
refactor_skill(skill_path="/path/to/skill")

# 专注特定领域
refactor_skill(
    skill_path="/path/to/skill",
    focus=["structure", "token-efficiency"]
)
```

## MCP 资源访问

### 技能模板

**URI 格式**：`skill://templates/{type}`

**可用类型**：
- `minimal` - 最小技能模板
- `tool-based` - 工具集成型模板
- `workflow-based` - 工作流型模板
- `analyzer-based` - 分析型模板

**使用方式**：
```python
# 通过 MCP Client 读取模板
resource = await session.read_resource("skill://templates/minimal")
template_content = resource.contents[0].text
```

### 最佳实践指南

**URI**：`skill://best-practices`

**内容**：渐进式披露、描述写作、组织原则等最佳实践

**使用方式**：
```python
resource = await session.read_resource("skill://best-practices")
practices = resource.contents[0].text
```

### 验证规则

**URI**：`skill://validation-rules`

**内容**：命名规则、描述标准、结构检查清单

**使用方式**：
```python
resource = await session.read_resource("skill://validation-rules")
rules = resource.contents[0].text
```

## MCP Prompts 使用

### create-skill 提示

**用途**：指导 AI 创建新技能

**参数**：
- `name` - 技能名称
- `template` - 模板类型

**使用方式**：
```python
prompt = await session.get_prompt("create-skill", arguments={
    "name": "my-skill",
    "template": "tool-based"
})
```

### validate-skill 提示

**用途**：指导 AI 验证技能质量

**参数**：
- `skill_path` - 技能路径
- `template` - 模板类型（可选）

### refactor-skill 提示

**用途**：指导 AI 生成重构建议

**参数**：
- `skill_path` - 技能路径
- `focus` - 重点关注领域（可选）

## 工作流集成

### 完整开发流程

```
1. init_skill(name, template)    # 初始化结构
2. 编写 SKILL.md 和引用文件
3. validate_skill(skill_path)    # 验证规范
4. analyze_skill(skill_path)     # 分析质量
5. refactor_skill(skill_path)    # 获取改进建议
6. 修改并重复验证
```

### Claude Code 中使用

在 Claude Code 对话中直接使用：

```
你：创建一个名为 pdf-helper 的技能

Claude：[调用 init_skill 工具]
已创建 pdf-helper 技能结构...

你：验证这个技能

Claude：[调用 validate_skill 工具]
验证报告：命名规范 ✓，描述完整 ✓，结构良好 ✓
```

## 错误处理

### 常见错误

**1. MCP Server 未连接**
```
错误：Tool 'init_skill' not found
解决：检查 Claude Code 配置，确保 MCP Server 已启动
```

**2. 技能路径不存在**
```
错误：Skill path not found: /path/to/skill
解决：确认路径正确，使用绝对路径
```

**3. 模板类型无效**
```
错误：Unknown template type: custom
解决：使用 valid 模板：minimal/tool-based/workflow-based/analyzer-based
```

## 高级用法

### 自定义模板

基于现有模板创建自定义变体：

```python
# 1. 初始化基础模板
init_skill(name="my-skill", template="tool-based")

# 2. 修改 SKILL.md
# 3. 添加自定义引用文件
# 4. 验证修改后的技能
validate_skill(skill_path="./my-skill")
```

### 批量验证

验证多个技能：

```python
skills = ["skill1", "skill2", "skill3"]
for skill in skills:
    result = validate_skill(skill_path=f"./skills/{skill}")
    print(f"{skill}: {result['score']}/100")
```

## 性能优化

### 缓存资源

频繁访问的资源可以缓存：

```python
# 首次读取
best_practices = await session.read_resource("skill://best-practices")

# 后续使用缓存内容
cached_practices = best_practices.contents[0].text
```

### 并发操作

独立操作可以并发执行：

```python
# 并发验证多个技能
import asyncio

results = await asyncio.gather(
    validate_skill(skill_path="./skill1"),
    validate_skill(skill_path="./skill2"),
    validate_skill(skill_path="./skill3")
)
```

## 故障排除

### 检查 MCP Server 状态

```bash
# 启动服务器测试
uv run python -m skill_creator_mcp

# 使用 Inspector 检查
npx @modelcontextprotocol/inspector ./skill-creator-mcp/src/skill_creator_mcp
```

### 查看日志

MCP Server 日志输出到 stderr，可在 Claude Code 日志中查看。

### 重启 MCP Server

如果遇到连接问题，重启 Claude Code 会自动重连 MCP Server。
