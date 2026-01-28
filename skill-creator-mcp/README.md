# Skill Creator MCP Server

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![Tests](https://img.shields.io/badge/tests-533%20passed-success](#)
[![Coverage](https://img.shields.io/badge/coverage-95%25-brightgreen](#)

Agent-Skills 开发与质量保证 MCP Server。

## 📖 文档导航

### 快速导航

- **[文档索引](docs/README.md)** - 📚 完整的文档导航和快速开始指南
- **[配置参数参考](docs/configuration.md)** - ⚙️ 所有环境变量的完整参考

### 安装与配置

- **[安装指南](docs/installation.md)** - 安装步骤和配置指南
- **[IDE 配置示例](docs/ide-config.md)** - Claude Desktop/Cursor/Continue.dev 等配置
- **[Claude Code 配置指南](docs/claude-code-config.md)** - Claude Code CLI 完整配置
- **[SSE 配置指南](docs/sse-guide.md)** - SSE 远程模式详细配置

---

## 开发状态

> 🚧 **项目正在开发中**
>
> 当前版本：v0.3.3
>
> 这是 Skill-Creator 项目的 MCP Server 组件，提供创建、验证、分析和重构 Agent-Skills 的工具。

## 特性

### 核心开发工具（7个）

- ✅ **collect_requirements** - AI 驱动的需求澄清工具（支持会话恢复）
- ✅ **init_skill** - 初始化新的 Agent-Skill 项目（支持 4 种模板）
- ✅ **validate_skill** - 验证技能结构和内容规范
- ✅ **analyze_skill** - 分析代码质量和复杂度
- ✅ **refactor_skill** - 重构建议生成（P0/P1/P2 优先级）
- ✅ **package_skill** - 打包发布工具（zip/tar.gz/tar.bz2）
- ✅ **package_agent_skill** - Agent-Skill 标准打包（推荐，支持版本号）

### 批量操作（2个）

- ✅ **batch_validate_skills_tool** - 批量验证多个 Agent-Skill
- ✅ **batch_analyze_skills_tool** - 批量分析多个 Agent-Skill

### 健康检查（3个）

- ✅ **health_check_tool** - 完整健康检查
- ✅ **quick_status_tool** - 快速状态摘要
- ✅ **is_healthy_tool** - 快速健康检查

### Phase 0 验证工具（5个）

- ✅ **check_client_capabilities** - 检测 MCP 客户端能力支持情况
- ✅ **test_llm_sampling** - 测试 LLM Sampling 能力
- ✅ **test_user_elicitation** - 测试用户征询能力
- ✅ **test_conversation_loop** - 测试对话循环和状态管理能力
- ✅ **test_requirement_completeness** - 测试需求完整性判断能力

### 技能模板

| 模板类型 | 描述 | 适用场景 |
|---------|------|----------|
| `minimal` | 最小化模板 | 简单工具封装 |
| `tool-based` | 工具集成模板 | 封装现有工具 |
| `workflow-based` | 工作流模板 | 多步骤流程 |
| `analyzer-based` | 分析器模板 | 代码分析 |

*注：✅ 已实现 | 🚧 开发中*

---

## 🚀 5分钟快速开始

### 方式A：全局安装（推荐，简单）

**1. 安装**

```bash
# 使用 pip 或 uv pip 全局安装
pip install skill-creator-mcp
# 或
uv pip install skill-creator-mcp
```

**2. 配置 Claude Code**

**选项1：使用 claude mcp add（简单）**

```bash
claude mcp add skill-creator stdio python -m skill_creator_mcp --scope user
```

**选项2：使用 claude mcp add-json（推荐）**

```bash
claude mcp add-json "skill-creator" '{
  "command": "python",
  "args": ["-m", "skill_creator_mcp"]
}' --scope user
```

**选项3：手动编辑配置文件**

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

**3. 验证**

在 Claude Code 中输入：
```
使用 skill-creator MCP 工具初始化一个名为 "my-skill" 的技能
```

---

### 方式B：源码开发（仅限贡献者）

**1. 克隆并安装**

```bash
# 克隆仓库
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

**3. 验证**

同方式A

---

### 下一步

- 📖 阅读 [文档索引](docs/README.md) 了解完整功能
- 🔧 查看 [配置参数参考](docs/configuration.md) 自定义配置
- 📘 查看 [MCP 配置说明](docs/mcp-config-guide.md) 了解详细配置选项

---

## 配置

### ⚠️ 重要：根据安装方式选择配置

**您是如何安装的？**

| 安装方式 | 推荐配置 | 复杂度 |
|---------|----------|--------|
| **pip / uv pip / PyPI** | [全局安装配置](#全局安装配置) | ⭐ 简单 |
| **克隆源码仓库** | [源码开发配置](#源码开发配置) | ⭐⭐⭐ 复杂 |

---

### 全局安装配置（推荐）

**安装**：
```bash
pip install skill-creator-mcp
# 或
uv pip install skill-creator-mcp
```

**配置**：
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

---

### 源码开发配置

**仅限贡献者/开发者**：需要克隆仓库并运行 `uv sync`

**配置 A：使用 uv --directory**
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

**配置 B：使用 cwd**
```json
{
  "mcpServers": {
    "skill-creator": {
      "command": "python",
      "args": ["-m", "skill_creator_mcp"],
      "cwd": "/absolute/path/to/Skills-Creator/skill-creator-mcp"
    }
  }
}
```

> 📘 **详细说明**：查看 [MCP 配置完整指南](docs/mcp-config-guide.md)

### 环境变量配置（可选）

创建 `.env` 文件来自定义服务器行为：

```bash
# 复制模板
cp .env.template .env

# 编辑配置
vim .env
```

**可用环境变量**：

| 变量名 | 默认值 | 说明 |
|--------|--------|------|
| `MCP_SERVER_LOG_LEVEL` | INFO | 日志级别（DEBUG/INFO/WARNING/ERROR） |
| `MCP_SERVER_LOG_FORMAT` | %(asctime)s... | 日志格式字符串 |
| `CACHE_ENABLED` | true | 是否启用缓存 |
| `CACHE_TTL` | 300 | 缓存过期时间（秒） |
| `CACHE_MAX_SIZE` | 100 | 缓存最大条目数 |
| `SKILL_CREATOR_OUTPUT_DIR` | ~/skills | 默认输出目录 |
| `BATCH_CONCURRENT_LIMIT` | 5 | 批量操作并发限制 |

**配置优先级**：工具参数 > 环境变量 `SKILL_CREATOR_OUTPUT_DIR` > 默认值 `~/skills`

> ✅ **目录自动管理**：
>
> - 默认使用 `~/skills`（自动创建）
> - 支持自定义路径（如 `~/.claude/skills`）
> - 所有路径自动检测和创建目录
> - 自动验证目录可写性
>
> **推荐配置**：
> ```bash
> # 使用默认 ~/skills
> # （无需配置，自动创建）
>
> # 或自定义目录
> export SKILL_CREATOR_OUTPUT_DIR=~/.claude/skills
> ```

## 使用

### collect_requirements - 需求澄清

AI 驱动的对话式需求收集工具，支持会话状态管理。

**参数：**
- `action` (str): 执行动作（`start`/`next`/`previous`/`status`/`complete`）
- `mode` (str): 收集模式（`basic`/`complete`/`brainstorm`/`progressive`）
- `session_id` (str, 可选): 会话 ID（自动生成）
- `user_input` (str, 可选): 用户输入（用于 next/complete 动作）

**收集模式：**
- `basic` - 5 步基础收集（技能名称、功能、场景、模板、额外需求）
- `complete` - 10 步完整收集（基础 + 用户、技术栈、依赖、测试、文档）
- `brainstorm` - AI 引导的创意发散
- `progressive` - 快速开始，逐步完善

**返回：**
```json
{
  "success": true,
  "session_id": "req_20250123_abc123",
  "action": "start",
  "mode": "basic",
  "current_step": {
    "key": "skill_name",
    "title": "技能名称",
    "prompt": "请输入技能名称..."
  },
  "step_index": 0,
  "total_steps": 5,
  "progress": 0.0,
  "answers": {},
  "message": "欢迎使用需求澄清工具！当前进度：0% (0/5)",
  "completed": false
}
```

### init_skill - 初始化技能

创建新的 Agent-Skill 项目目录结构。

**参数：**
- `name` (str): 技能名称（小写字母、数字、连字符，1-64字符）
- `template` (str): 模板类型（`minimal`/`tool-based`/`workflow-based`/`analyzer-based`）
- `output_dir` (str): 输出目录路径（默认：`.`）
- `with_scripts` (bool): 是否包含示例脚本（默认：`False`）
- `with_examples` (bool): 是否包含使用示例（默认：`False`）

**返回：**
```json
{
  "success": true,
  "skill_path": "/path/to/skill",
  "skill_name": "my-skill",
  "template_type": "tool-based",
  "message": "技能初始化成功"
}
```

### validate_skill - 验证技能

验证 Agent-Skill 的结构和内容是否符合规范。

**参数：**
- `skill_path` (str): 技能目录路径
- `check_structure` (bool): 是否检查目录结构（默认：`True`）
- `check_content` (bool): 是否检查内容格式（默认：`True`）

**返回：**
```json
{
  "success": true,
  "valid": true,
  "skill_path": "/path/to/skill",
  "skill_name": "my-skill",
  "template_type": "tool-based",
  "errors": [],
  "warnings": [],
  "checks": {
    "structure": true,
    "naming": true,
    "content": true,
    "template_requirements": true
  },
  "message": "验证通过"
}
```

### analyze_skill - 分析技能

分析 Agent-Skill 的代码质量、复杂度和结构。

**参数：**
- `skill_path` (str): 技能目录路径
- `analyze_structure` (bool): 是否分析代码结构（默认：`True`）
- `analyze_complexity` (bool): 是否分析代码复杂度（默认：`True`）
- `analyze_quality` (bool): 是否分析代码质量（默认：`True`）

**返回：**
```json
{
  "success": true,
  "skill_path": "/path/to/skill",
  "skill_name": "my-skill",
  "structure": {
    "total_files": 10,
    "total_lines": 500,
    "file_breakdown": {
      "server": 1,
      "models": 2,
      "utils": 3,
      "tests": 4
    }
  },
  "complexity": {
    "cyclomatic_complexity": 5,
    "maintainability_index": 85.5
  },
  "quality": {
    "overall_score": 75.0,
    "structure_score": 30.0,
    "documentation_score": 25.0,
    "test_coverage_score": 20.0
  },
  "suggestions": ["建议1", "建议2"],
  "summary": "代码质量良好..."
}
```

## 开发

```bash
# 运行环境检查
./scripts/check-env.sh

# 运行测试
uv run pytest

# 运行 lint
uv run ruff check .

# 运行类型检查
uv run mypy src/

# 启动服务器
uv run python -m skill_creator_mcp
```

## 许可证

MIT License

## 参考资源

- [FastMCP GitHub](https://github.com/jlowin/fastmcp)
- [MCP Python SDK](https://github.com/modelcontextprotocol/python-sdk)
