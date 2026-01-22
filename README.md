# Skills-Creator

> **版本**: v0.1.0-alpha
> **项目类型**: MCP Server + Agent-Skill 混合架构
> **测试覆盖率**: 98% (297 tests)

---

## 项目概述

**Skills-Creator** 是一个基于 **MCP Server + Agent-Skill 混合架构**的完整解决方案，用于开发、验证和优化 Agent-Skills。

本项目包含两个核心组件：
1. **skill-creator-mcp** - MCP Server，提供原子操作工具
2. **skill-creator** - Agent-Skill，提供工作流编排和最佳实践

### 核心功能

- ✅ **技能初始化**: 创建符合规范的技能目录结构
- ✅ **规范验证**: 自动检查命名、结构、内容符合最佳实践
- ✅ **质量分析**: Token效率分析、反模式识别、改进建议
- ✅ **重构建议**: 基于最佳实践生成可执行的重构方案
- ✅ **打包发布**: 质量检查 + 分发包生成

---

## 快速开始

### 前置要求

- Python >= 3.10
- uv (推荐) 或 pip
- Claude Code / Desktop (用于使用 Agent-Skill)

### 安装 MCP Server

```bash
cd skill-creator-mcp
uv sync --dev
```

### 配置 Claude Code

在 Claude Code 配置文件中添加：

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

### 基本使用

在 Claude Code 中使用：

```
使用 skill-creator 创建一个名为 "docker-manager" 的技能
```

或直接调用 MCP 工具：

```
调用 mcp__skill_creator__init_skill，参数：
- name: "docker-manager"
- template: "tool-based"
```

---

## 项目结构

```
Skills-Creator/
├── skill-creator-mcp/          # MCP Server (Python)
│   ├── src/skill_creator_mcp/
│   │   ├── server.py           # MCP Server 入口
│   │   ├── tools/              # 5个工具
│   │   ├── resources/          # 3个资源
│   │   ├── prompts/            # 3个提示模板
│   │   └── utils/              # 工具函数
│   ├── tests/                  # 测试套件 (98% 覆盖率)
│   └── pyproject.toml          # 项目配置
├── SKILL.md                    # Agent-Skill 入口
├── references/                 # 详细文档
├── examples/                   # 使用示例
├── CLAUDE.md                   # 开发指南
├── ARCHITECTURE_AUDIT_REPORT_v2.md
├── ROADMAP.md
├── ISSUES.md
├── CHANGELOG.md
└── .claude/
    └── plans/                  # 开发计划
```

---

## 文档

### 核心文档

| 文档 | 说明 |
|------|------|
| [SKILL.md](SKILL.md) | Agent-Skill 主入口 |
| [CLAUDE.md](CLAUDE.md) | 项目开发指南和规范 |
| [skill-creator-mcp/README.md](skill-creator-mcp/README.md) | MCP Server 文档 |

### 引用文档

| 文档 | 说明 |
|------|------|
| [MCP 集成指南](references/mcp-integration.md) | MCP 工具和资源使用 |
| [最佳实践](references/best-practices.md) | 渐进式披露和描述规范 |
| [验证规范](references/validation.md) | 命名、结构、内容验证规则 |
| [验证指南](references/validation-guide.md) | 详细验证指南 |

### 示例文档

| 文档 | 说明 |
|------|------|
| [创建技能](examples/creating-a-skill.md) | 如何创建新技能 |
| [验证技能](examples/validating-a-skill.md) | 如何验证技能 |
| [分析技能](examples/analyzing-a-skill.md) | 如何分析技能 |
| [MCP 使用示例](examples/mcp-usage-examples.md) | MCP 工具详细示例 |

---

## MCP 工具列表

| 工具 | 功能 |
|------|------|
| `init_skill` | 初始化新技能结构 |
| `validate_skill` | 验证技能规范 |
| `analyze_skill` | 分析技能质量 |
| `refactor_skill` | 生成重构建议 |
| `package_skill` | 打包技能为分发格式 |

---

## 开发

### 运行测试

```bash
cd skill-creator-mcp
uv run pytest --cov
```

### 代码检查

```bash
uv run ruff check .
uv run mypy src/
```

### 启动服务器

```bash
# STDIO 模式
uv run python -m skill_creator_mcp

# HTTP/SSE 模式
uv run python -m skill_creator_mcp.http
```

---

## 质量保证

| 指标 | 当前值 | 目标值 |
|------|--------|--------|
| 测试覆盖率 | 98% | ≥95% |
| 代码规范 | ✅ 通过 | 0错误 |
| 类型检查 | ✅ 通过 | 0错误 |
| 安全检查 | ✅ 通过 | 0高危 |

---

## 路线图

当前版本为 v0.1.0-alpha，主要开发计划参见 [ROADMAP.md](ROADMAP.md)。

---

## 许可证

MIT License - 详见 [LICENSE](skill-creator-mcp/LICENSE)

---

## 贡献

欢迎贡献！请查看 [CLAUDE.md](CLAUDE.md) 了解开发规范。

---

## 联系方式

- 问题反馈: [GitHub Issues](https://github.com/yourusername/Skills-Creator/issues)
- 功能建议: [GitHub Discussions](https://github.com/yourusername/Skills-Creator/discussions)
