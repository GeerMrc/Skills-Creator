# Claude Code 配置完整指南

> 版本: 0.3.0
> 更新日期: 2026-01-26
> 适用对象: Claude Code (VSCode) 用户

---

## 概述

Claude Code 是 Anthropic 官方的 VSCode 扩展，支持通过 MCP 协议集成 Skill Creator。

---

## 安装方式

### ⚠️ 根据使用场景选择安装方式

**方式A：全局安装（推荐，简单）**

适用场景：仅使用 MCP Server 工具

```bash
# 使用 pip 或 uv pip 全局安装
pip install skill-creator-mcp
# 或
uv pip install skill-creator-mcp
```

**方式B：源码开发（仅限贡献者）**

适用场景：从源码开发或贡献代码

```bash
# 克隆仓库
git clone https://github.com/GeerMrc/Skills-Creator.git
cd Skills-Creator/skill-creator-mcp

# 安装依赖
uv sync --dev
```

---

## 快速开始

### 全局安装用户

```bash
# 添加 MCP 服务器
claude mcp add skill-creator stdio python -m skill_creator_mcp
```

### 源码开发用户

```bash
# 添加 MCP 服务器（使用 uv）
claude mcp add skill-creator stdio uv run python -m skill_creator_mcp
```

---

## 配置方式

### 方式1：CLI 命令（推荐）

#### 1.1 claude mcp add（基础方式）

使用 `claude mcp add` 命令快速配置：

**全局安装用户**：
```bash
# 基础配置
claude mcp add skill-creator stdio python -m skill_creator_mcp

# 带环境变量
claude mcp add skill-creator stdio python -m skill_creator_mcp \
  --env SKILL_CREATOR_LOG_LEVEL=DEBUG
```

**源码开发用户**：
```bash
# 基础配置（使用 uv）
claude mcp add skill-creator stdio uv run python -m skill_creator_mcp

# 带环境变量
claude mcp add skill-creator stdio uv run python -m skill_creator_mcp \
  --env SKILL_CREATOR_LOG_LEVEL=DEBUG
```

#### 1.2 claude mcp add-json（复杂配置推荐）

使用 `claude mcp add-json` 命令直接传递 JSON 配置：

**全局安装用户**：
```bash
# 基础配置
claude mcp add-json "skill-creator" '{"command": "python", "args": ["-m", "skill_creator_mcp"]}' --scope user

# 带环境变量
claude mcp add-json "skill-creator" '{
  "command": "python",
  "args": ["-m", "skill_creator_mcp"],
  "env": {
    "SKILL_CREATOR_LOG_LEVEL": "DEBUG"
  }
}' --scope user
```

**源码开发用户**：
```bash
# 使用 uv --directory 配置（推荐）
claude mcp add-json "skill-creator" '{
  "command": "uv",
  "args": [
    "--directory",
    "/absolute/path/to/Skills-Creator/skill-creator-mcp",
    "run",
    "python",
    "-m",
    "skill_creator_mcp"
  ]
}' --scope user

# 使用 cwd 配置
claude mcp add-json "skill-creator" '{
  "command": "python",
  "args": ["-m", "skill_creator_mcp"],
  "cwd": "/absolute/path/to/Skills-Creator/skill-creator-mcp"
}' --scope user
```

**命令对比**：

| 特性 | `claude mcp add` | `claude mcp add-json` |
|------|-----------------|----------------------|
| **适用场景** | 简单配置 | 复杂配置 |
| **环境变量** | `--env KEY=VALUE` | JSON 中配置 |
| **源码配置** | 需要多行转义 | JSON 格式清晰 |
| **配置范围** | `--scope <scope>` | `--scope <scope>` |

**scope 参数说明**：

| scope | 存储位置 | 可提交VC | 适用场景 |
|-------|----------|----------|----------|
| `project` | `.mcp.json` | ✅ | 团队协作开发 |
| `user` | `~/.claude/settings.json` | ❌ | 跨项目使用（推荐） |
| `local` | `.claude/settings.json` | ❌ | 临时测试 |

### 方式2：配置文件

编辑配置文件：

| 配置范围 | 文件位置 |
|---------|----------|
| **project** | `.mcp.json`（项目根目录） |
| **user** | `~/.claude/settings.json` |
| **local** | `.claude/settings.json`（项目目录） |

**全局安装配置**：
```json
{
  "mcpServers": {
    "skill-creator": {
      "command": "python",
      "args": ["-m", "skill_creator_mcp"],
      "env": {
        "SKILL_CREATOR_LOG_LEVEL": "INFO"
      }
    }
  }
}
```

**源码开发配置**：
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
      ],
      "env": {
        "SKILL_CREATOR_LOG_LEVEL": "INFO"
      }
    }
  }
}
```

---

## CLI 命令参考

### 基础命令

```bash
# 方式1：claude mcp add（简单配置）
claude mcp add <name> stdio <command> [args...]

# 方式2：claude mcp add-json（复杂配置）
claude mcp add-json <name> '<JSON配置>' --scope <scope>

# 示例：简单配置
claude mcp add skill-creator stdio python -m skill_creator_mcp

# 示例：复杂配置（推荐使用 add-json）
claude mcp add-json "skill-creator" '{
  "command": "python",
  "args": ["-m", "skill_creator_mcp"],
  "env": {"SKILL_CREATOR_LOG_LEVEL": "DEBUG"}
}' --scope user

# 列出所有服务器
claude mcp list

# 删除服务器
claude mcp remove skill-creator

# 查看帮助
claude mcp --help
```

### 配置范围命令

```bash
# 项目级配置（团队共享）
claude mcp add skill-creator stdio python -m skill_creator_mcp --scope project

# 用户级配置（跨项目）
claude mcp add skill-creator stdio python -m skill_creator_mcp --scope user

# 本地配置（临时测试）
claude mcp add skill-creator stdio python -m skill_creator_mcp --scope local
```

### 带环境变量的配置

```bash
# 带日志级别
claude mcp add skill-creator stdio python -m skill_creator_mcp \
  --env SKILL_CREATOR_LOG_LEVEL=DEBUG

# 带输出目录
claude mcp add skill-creator stdio python -m skill_creator_mcp \
  --env SKILL_CREATOR_OUTPUT_DIR=~/skills-output

# 多个环境变量
claude mcp add skill-creator stdio python -m skill_creator_mcp \
  --env SKILL_CREATOR_LOG_LEVEL=DEBUG \
  --env SKILL_CREATOR_OUTPUT_DIR=~/skills-output \
  --env SKILL_CREATOR_MAX_RETRIES=5
```

---

## 配置范围详解

### 配置范围对比

| 范围 | 存储位置 | 可提交VC | 共享范围 | 适用场景 | 命令参数 |
|------|---------|---------|---------|---------|----------|
| **project** | `.mcp.json` | ✅ | 团队 | 团队协作开发 | `--scope project` |
| **user** | `~/.claude/settings.json` | ❌ | 个人 | 跨项目使用 | `--scope user` |
| **local** | `.claude/settings.json` | ❌ | 个人 | 临时测试 | `--scope local`（默认） |

### 项目级配置（推荐团队使用）

**全局安装用户**：
```bash
cd /path/to/Skills-Creator
claude mcp add skill-creator stdio python -m skill_creator_mcp --scope project
```

**生成的文件**：`.mcp.json`
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

**源码开发用户**：
```bash
cd /path/to/Skills-Creator
claude mcp add skill-creator stdio uv run python -m skill_creator_mcp --scope project
```

**优点**：
- ✅ 配置可提交到版本控制
- ✅ 团队成员共享配置
- ✅ 项目特定配置

### 用户级配置（推荐个人使用）

**全局安装用户**：
```bash
claude mcp add skill-creator stdio python -m skill_creator_mcp --scope user
```

**生成的文件**：`~/.claude/settings.json`
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

**源码开发用户**：
```bash
cd /path/to/Skills-Creator
claude mcp add skill-creator stdio uv run python -m skill_creator_mcp --scope user
```

**优点**：
- ✅ 跨项目使用
- ✅ 个人配置统一管理
- ✅ 一次配置，所有项目可用

### 本地配置（临时测试）

**全局安装用户**：
```bash
cd /path/to/Skills-Creator
claude mcp add skill-creator stdio python -m skill_creator_mcp --scope local
```

**源码开发用户**：
```bash
cd /path/to/Skills-Creator/skill-creator-mcp
claude mcp add skill-creator stdio uv run python -m skill_creator_mcp --scope local
```

**生成的文件**：`.claude/settings.json`
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

**优点**：
- ✅ 项目本地配置
- ✅ 不干扰其他配置
- ✅ 适合临时测试

---

## 常用配置场景

### 场景1：项目级配置（团队协作）

**全局安装用户**：
```bash
cd /path/to/Skills-Creator
claude mcp add skill-creator stdio python -m skill_creator_mcp \
  --scope project \
  --env SKILL_CREATOR_LOG_LEVEL=INFO
```

**源码开发用户**：
```bash
cd /path/to/Skills-Creator
claude mcp add skill-creator stdio uv run python -m skill_creator_mcp \
  --scope project \
  --env SKILL_CREATOR_LOG_LEVEL=INFO
```

提交到版本控制：
```bash
git add .mcp.json
git commit -m "docs: 添加 Skill Creator MCP 配置"
```

### 场景2：用户级配置（跨项目使用）

**全局安装用户**：
```bash
claude mcp add skill-creator stdio python -m skill_creator_mcp \
  --scope user \
  --env SKILL_CREATOR_LOG_LEVEL=DEBUG \
  --env SKILL_CREATOR_OUTPUT_DIR=~/skills-output
```

**源码开发用户**：
```bash
cd /path/to/Skills-Creator
claude mcp add skill-creator stdio uv run python -m skill_creator_mcp \
  --scope user \
  --env SKILL_CREATOR_LOG_LEVEL=DEBUG \
  --env SKILL_CREATOR_OUTPUT_DIR=~/skills-output
```

### 场景3：本地开发（调试模式）

**全局安装用户**：
```bash
cd /path/to/Skills-Creator
claude mcp add skill-creator stdio python -m skill_creator_mcp \
  --scope local \
  --env SKILL_CREATOR_LOG_LEVEL=DEBUG
```

**源码开发用户**：
```bash
cd /path/to/Skills-Creator/skill-creator-mcp
claude mcp add skill-creator stdio uv run python -m skill_creator_mcp \
  --scope local \
  --env SKILL_CREATOR_LOG_LEVEL=DEBUG
```

---

## 环境变量配置

### 常用环境变量

| 变量 | 默认值 | 说明 |
|------|--------|------|
| `SKILL_CREATOR_LOG_LEVEL` | INFO | 日志级别（DEBUG/INFO/WARNING/ERROR/CRITICAL） |
| `SKILL_CREATOR_LOG_FORMAT` | default | 日志格式（default/simple/detailed） |
| `SKILL_CREATOR_OUTPUT_DIR` | . | 输出目录 |
| `SKILL_CREATOR_MAX_RETRIES` | 3 | 最大重试次数 |
| `SKILL_CREATOR_TIMEOUT_SECONDS` | 30 | 超时时间（秒） |

详细的环境变量配置请参考：[配置参数参考](./configuration.md)

---

## 验证配置

### 检查连接

```bash
# 列出所有 MCP 服务器
claude mcp list

# 应该看到 skill-creator 在列表中
```

### 测试工具

在 Claude Code 中：

1. 打开命令面板 (`Cmd/Ctrl + Shift + P`)
2. 输入 "MCP"
3. 选择 "skill-creator" 相关工具
4. 验证工具可用（应显示 16 个工具）

### 可用工具列表

**核心开发工具（6个）**：
- `init_skill` - 初始化新的 Agent-Skill
- `validate_skill` - 验证技能结构和内容
- `analyze_skill` - 分析代码质量和复杂度
- `refactor_skill` - 生成重构建议
- `package_skill` - 打包发布工具
- `collect_requirements` - AI 驱动的需求澄清

**批量操作（2个）**：
- `batch_validate_skills_tool` - 批量验证多个技能
- `batch_analyze_skills_tool` - 批量分析多个技能

**健康检查（3个）**：
- `health_check_tool` - 完整健康检查
- `quick_status_tool` - 快速状态摘要
- `is_healthy_tool` - 快速健康检查

**Phase 0验证工具（5个）**：
- `check_client_capabilities` - 检测客户端能力
- `test_llm_sampling` - 测试 LLM Sampling
- `test_user_elicitation` - 测试用户征询
- `test_conversation_loop` - 测试对话循环
- `test_requirement_completeness` - 测试需求完整性

---

## 故障排除

### 常见问题

**问题：服务器未找到**
```bash
# 检查配置
claude mcp list

# 重新添加
claude mcp remove skill-creator
claude mcp add skill-creator stdio python -m skill_creator_mcp
```

**问题：模块导入失败**
```bash
# 确认安装
cd skill-creator-mcp
uv sync --dev

# 或使用开发模式安装
pip install -e .
```

**问题：权限错误**
```bash
# 使用用户安装
pip install --user -e .
```

**问题：工具数量不对**
```bash
# 确认最新版本
cd skill-creator-mcp
git pull
uv sync --dev

# 重启 VSCode
```

---

## 配置文件示例

### 全局安装配置示例

**完整的 .mcp.json 示例**：
```json
{
  "mcpServers": {
    "skill-creator": {
      "command": "python",
      "args": ["-m", "skill_creator_mcp"],
      "env": {
        "SKILL_CREATOR_LOG_LEVEL": "INFO",
        "SKILL_CREATOR_OUTPUT_DIR": "./skills-output",
        "SKILL_CREATOR_MAX_RETRIES": "3"
      }
    }
  }
}
```

### 源码开发配置示例

**使用 uv 的 .mcp.json 示例**：
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
      ],
      "env": {
        "SKILL_CREATOR_LOG_LEVEL": "INFO",
        "SKILL_CREATOR_OUTPUT_DIR": "./skills-output",
        "SKILL_CREATOR_MAX_RETRIES": "3"
      }
    }
  }
}
```

---

## 完整配置快速参考

### 所有支持的环境变量

| 环境变量 | 默认值 | 说明 |
|---------|--------|------|
| **日志配置** |
| `SKILL_CREATOR_LOG_LEVEL` | INFO | 日志级别（DEBUG/INFO/WARNING/ERROR/CRITICAL） |
| `SKILL_CREATOR_LOG_FORMAT` | default | 日志格式（default/simple/detailed） |
| `SKILL_CREATOR_LOG_FILE` | 无 | 日志文件路径 |
| **输出配置** |
| `SKILL_CREATOR_OUTPUT_DIR` | . | 默认输出目录 |
| **操作配置** |
| `SKILL_CREATOR_MAX_RETRIES` | 3 | 最大重试次数 |
| `SKILL_CREATOR_TIMEOUT_SECONDS` | 30 | 超时时间（秒） |

> 💡 **提示**：完整的配置说明请参考 [配置参数参考](./configuration.md)

---

## 相关文档

- [配置参数参考](./configuration.md) - 完整的环境变量配置
- [IDE 集成配置](./ide-config.md) - 其他 IDE 配置示例
- [安装指南](./installation.md) - 安装和验证
