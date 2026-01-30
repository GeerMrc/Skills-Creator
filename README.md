# Skills-Creator

> **版本**: v0.3.4
> **项目类型**: MCP Server + Agent-Skill 混合架构
> **测试覆盖率**: 97% (568个测试用例，562通过，4失败，2跳过)

> **📢 目录结构变更通知 (v0.2.0)**: Agent-Skill 相关代码已统一到 `skill-creator/` 目录。如果您直接引用 `SKILL.md`、`examples/` 或 `references/`，请参阅 [迁移指南](MIGRATION.md) 更新您的路径配置。

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
- Claude Code / Desktop

### 使用模式

本项目支持两种使用模式：

#### 模式1：仅使用 MCP Server（独立模式）

直接调用 MCP 工具，手动控制工作流。

#### 模式2：完整模式（Agent-Skill + MCP Server）推荐

使用 Agent-Skill 编排工作流，获得渐进式披露的知识传递和最佳实践指导。

### 安装步骤

> ⚠️ **重要**：根据您的使用方式选择安装方法

---

#### 方式A：全局安装（推荐，简单）

**适用场景**：仅使用 MCP Server 工具

**1. 安装 MCP Server**

```bash
# 方式1：使用 pip
pip install skill-creator-mcp

# 方式2：使用 uv pip
uv pip install skill-creator-mcp
```

**2. 配置 Claude Code**

**方式1：使用 claude mcp add-json（推荐）**

```bash
# 用户级配置（跨项目使用）
claude mcp add-json "skill-creator" '{
  "command": "python",
  "args": ["-m", "skill_creator_mcp"]
}' --scope user
```

**方式2：使用 claude mcp add**

```bash
claude mcp add skill-creator stdio python -m skill_creator_mcp --scope user
```

**方式3：手动编辑配置文件**

编辑 `~/.config/Claude/claude_desktop_config.json`：

```json
{
  "mcpServers": {
    "skill-creator": {
      "command": "python",
      "args": ["-m", "skill_creator_mcp"]
    }
  }
}
```

**3. 安装 Agent-Skill（可选，完整模式）**

如果想要使用工作流编排功能：

```bash
# 复制 Agent-Skill 到 Claude skills 目录
cp -r skill-creator ~/.claude/skills/skill-creator

# 验证安装
ls ~/.claude/skills/skill-creator/SKILL.md
```

---

#### 方式B：源码开发（仅限贡献者）

**适用场景**：从源码开发或贡献代码

**1. 克隆仓库并安装依赖**

```bash
# 克隆仓库（如果还没有）
git clone https://github.com/GeerMrc/Skills-Creator.git
cd Skills-Creator/skill-creator-mcp

# 安装依赖
uv sync --dev
```

**2. 配置 Claude Code**

编辑 `~/.config/Claude/claude_desktop_config.json`：

```json
{
  "mcpServers": {
    "skill-creator": {
      "command": "uv",
      "args": [
        "--directory",
        "/absolute/path/to/Skills-Creator/skill-creator-mcp",
        "run",
        "python",
        "-m",
        "skill_creator_mcp"
      ]
    }
  }
}
```

**3. 安装 Agent-Skill（完整模式）**

同方式A

---

### 安装方式对比

| 维度 | 全局安装 | 源码开发 |
|------|----------|----------|
| **安装复杂度** | ⭐ 简单 | ⭐⭐⭐ 复杂 |
| **配置复杂度** | ⭐ 简单 | ⭐⭐ 中等 |
| **更新方式** | `pip install -U` | `git pull` |
| **适用场景** | 使用工具 | 开发/贡献 |

> 📘 **详细配置**：查看 [MCP 配置说明](skill-creator-mcp/docs/mcp-config-guide.md)

---

### 基本使用

**完整模式（Agent-Skill + MCP Server）**：

```
使用 skill-creator 创建一个名为 "docker-manager" 的技能
```

**独立模式（仅 MCP Server）**：

```
调用 mcp__skill_creator__init_skill，参数：
- name: "docker-manager"
- template: "tool-based"
```

**推荐使用完整模式**，Agent-Skill 会自动编排工作流程并提供最佳实践指导。

---

## 项目结构

```
Skills-Creator/
├── skill-creator/              # Agent-Skill 代码统一目录
│   ├── SKILL.md                # Agent-Skill 入口
│   ├── examples/               # 使用示例
│   ├── scripts/                # 辅助脚本
│   └── references/             # 引用文档
├── skill-creator-mcp/          # MCP Server (Python)
│   ├── src/skill_creator_mcp/
│   │   ├── server.py           # MCP Server 入口
│   │   ├── tools/              # 5个工具
│   │   ├── resources/          # 3个资源
│   │   ├── prompts/            # 3个提示模板
│   │   └── utils/              # 工具函数
│   ├── tests/                  # 测试套件 (97% 覆盖率, 568个测试用例)
│   └── pyproject.toml          # 项目配置
├── docs/                       # 项目文档
│   └── adr/
│       └── 001-hybrid-architecture.md
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
| [SKILL.md](skill-creator/SKILL.md) | Agent-Skill 主入口 |
| [CLAUDE.md](CLAUDE.md) | 项目开发指南和规范 |
| [skill-creator-mcp/README.md](skill-creator-mcp/README.md) | MCP Server 文档 |

### 引用文档

| 文档 | 说明 |
|------|------|
| [MCP 集成指南](skill-creator/references/mcp-integration.md) | MCP 工具和资源使用 |
| [最佳实践 - 核心](skill-creator/references/best-practices-core.md) | 基础架构和规范 |
| [最佳实践 - 高级](skill-creator/references/best-practices-advanced.md) | 高级技巧和优化 |
| [验证规范](skill-creator/references/validation.md) | 命名、结构、内容验证规则 |
| [验证指南](skill-creator/references/validation-guide.md) | 详细验证指南 |

### 示例文档

| 文档 | 说明 |
|------|------|
| [创建技能](skill-creator/examples/creating-a-skill.md) | 如何创建新技能 |
| [验证技能](skill-creator/examples/validating-a-skill.md) | 如何验证技能 |
| [分析技能](skill-creator/examples/analyzing-a-skill.md) | 如何分析技能 |
| [MCP 使用示例](skill-creator/examples/mcp-usage-examples.md) | MCP 工具详细示例 |

---

## MCP 工具列表

MCP Server 提供 **12个工具**，按功能划分为 **3类**：

### 技能生命周期（4个）

| 工具 | 功能 |
|------|------|
| `init_skill` | 初始化新技能结构 |
| `validate_skill` | 验证技能规范 |
| `analyze_skill` | 分析技能质量 |
| `refactor_skill` | 生成重构建议 |

### 打包工具（1个）

| 工具 | 功能 |
|------|------|
| `package_skill` | 统一打包工具（支持通用和Agent-Skill标准两种模式） |

### 需求收集原子工具（7个）

| 工具 | 功能 |
|------|------|
| `create_requirement_session` | 创建需求收集会话 |
| `get_requirement_session` | 获取会话状态 |
| `update_requirement_answer` | 更新答案 |
| `get_static_question` | 获取静态问题 |
| `generate_dynamic_question` | 生成动态问题 |
| `validate_answer_format` | 验证答案格式 |
| `check_requirement_completeness` | 检查完整性 |

**package_skill** 统一打包工具，支持两种模式：
- `strict=False` (默认): 通用打包模式
- `strict=True`: Agent-Skill 标准打包模式，需要 `version` 参数

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
| 测试覆盖率 | 97% (568个测试用例) | ≥95% |
| 代码规范 | ✅ 通过 | 0错误 |
| 类型检查 | ✅ 通过 | 0错误 |
| 安全检查 | ✅ 通过 | 0高危 |

---

## 路线图

当前版本为 v0.3.3，主要开发计划参见 [ROADMAP.md](ROADMAP.md)。

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
