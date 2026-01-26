# Agent-Skill Claude Code 配置指南

> 版本: 0.3.0
> 更新日期: 2026-01-26
> 适用对象: Claude Code 用户

---

## 概述

本文档详细介绍如何在 Claude Code 中配置和使用 Skill-Creator Agent-Skill。

---

## 配置方式对比

### 三种配置范围

| 范围 | 存储位置 | 可提交VC | 共享范围 | 适用场景 | 命令参数 |
|------|---------|---------|---------|---------|----------|
| **project** | `.mcp.json` | ✅ | 团队 | 团队协作开发 | `--scope project` |
| **user** | `~/.claude/settings.json` | ❌ | 个人 | 跨项目使用 | `--scope user` |
| **local** | `.claude/settings.json` | ❌ | 个人 | 临时测试 | `--scope local` |

---

## 配置方式详解

### 方式1：项目级配置（推荐团队使用）

#### 配置步骤

```bash
# 1. 进入项目根目录
cd /path/to/Skills-Creator

# 2. 添加 MCP 服务器（项目级）
claude mcp add skill-creator stdio python -m skill_creator_mcp --scope project

# 3. 验证配置
claude mcp list
```

#### 生成的配置文件

**文件位置**：`Skills-Creator/.mcp.json`

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

#### 优点

- ✅ 配置可提交到版本控制
- ✅ 团队成员共享配置
- ✅ 项目特定配置
- ✅ 适合团队协作

#### 提交到版本控制

```bash
git add .mcp.json
git commit -m "docs: 添加 Skill Creator MCP 项目配置"
```

---

### 方式2：用户级配置（推荐个人使用）

#### 配置步骤

```bash
# 1. 添加 MCP 服务器（用户级）
claude mcp add skill-creator stdio python -m skill_creator_mcp --scope user

# 2. 验证配置
claude mcp list
```

#### 生成的配置文件

**文件位置**：`~/.claude/settings.json`

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

#### 优点

- ✅ 跨项目使用
- ✅ 个人配置统一管理
- ✅ 一次配置，所有项目可用
- ✅ 适合个人开发

---

### 方式3：本地配置（临时测试）

#### 配置步骤

```bash
# 1. 进入项目目录
cd /path/to/Skills-Creator

# 2. 添加 MCP 服务器（本地级）
claude mcp add skill-creator stdio python -m skill_creator_mcp --scope local

# 3. 验证配置
claude mcp list
```

#### 生成的配置文件

**文件位置**：`Skills-Creator/.claude/settings.json`

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

#### 优点

- ✅ 项目本地配置
- ✅ 不干扰其他配置
- ✅ 适合临时测试
- ✅ 不会被提交到版本控制

---

## 环境变量配置

### 带环境变量的配置

```bash
# 基础配置 + 环境变量
claude mcp add skill-creator stdio python -m skill_creator_mcp \
  --env SKILL_CREATOR_LOG_LEVEL=DEBUG \
  --env SKILL_CREATOR_OUTPUT_DIR=~/skills-output
```

### 常用环境变量

| 变量 | 默认值 | 说明 |
|------|--------|------|
| `SKILL_CREATOR_LOG_LEVEL` | INFO | 日志级别（DEBUG/INFO/WARNING/ERROR/CRITICAL） |
| `SKILL_CREATOR_LOG_FORMAT` | default | 日志格式（default/simple/detailed） |
| `SKILL_CREATOR_OUTPUT_DIR` | . | 输出目录 |
| `SKILL_CREATOR_MAX_RETRIES` | 3 | 最大重试次数 |
| `SKILL_CREATOR_TIMEOUT_SECONDS` | 30 | 超时时间（秒） |

详细的环境变量配置请参考：[MCP Server 配置参数参考](../../skill-creator-mcp/docs/configuration.md)

---

## 验证配置

### 检查 MCP 连接

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

---

## 常见配置场景

### 场景1：团队协作开发

```bash
cd /path/to/Skills-Creator
claude mcp add skill-creator stdio python -m skill_creator_mcp \
  --scope project \
  --env SKILL_CREATOR_LOG_LEVEL=INFO
```

提交到版本控制：
```bash
git add .mcp.json
git commit -m "docs: 添加团队共享的 MCP 配置"
```

### 场景2：个人跨项目使用

```bash
claude mcp add skill-creator stdio python -m skill_creator_mcp \
  --scope user \
  --env SKILL_CREATOR_LOG_LEVEL=DEBUG \
  --env SKILL_CREATOR_OUTPUT_DIR=~/skills-output
```

### 场景3：本地调试

```bash
cd /path/to/Skills-Creator/skill-creator-mcp
claude mcp add skill-creator stdio uv run python -m skill_creator_mcp \
  --scope local \
  --env SKILL_CREATOR_LOG_LEVEL=DEBUG
```

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

**问题：工具数量不对**
```bash
# 确认最新版本
cd skill-creator-mcp
git pull
uv sync --dev

# 重启 VSCode
```

**问题：配置冲突**
```bash
# 检查多个配置文件
cat .mcp.json
cat .claude/settings.json
cat ~/.claude/settings.json

# 删除冲突的配置
claude mcp remove skill-creator --scope local
```

---

## 配置迁移

### 从 local 迁移到 project

```bash
# 1. 删除 local 配置
claude mcp remove skill-creator --scope local

# 2. 添加 project 配置
claude mcp add skill-creator stdio python -m skill_creator_mcp --scope project

# 3. 提交到版本控制
git add .mcp.json
git commit -m "chore: 将 MCP 配置迁移到项目级"
```

### 从 user 迁移到 project

```bash
# 1. 删除 user 配置
claude mcp remove skill-creator --scope user

# 2. 添加 project 配置
claude mcp add skill-creator stdio python -m skill_creator_mcp --scope project

# 3. 提交到版本控制
git add .mcp.json
git commit -m "chore: 将 MCP 配置迁移到项目级"
```

---

## 完整配置示例

### 带环境变量的项目配置

**命令**：
```bash
claude mcp add skill-creator stdio python -m skill_creator_mcp \
  --scope project \
  --env SKILL_CREATOR_LOG_LEVEL=INFO \
  --env SKILL_CREATOR_OUTPUT_DIR=./skills-output \
  --env SKILL_CREATOR_MAX_RETRIES=3
```

**生成的 `.mcp.json`**：
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

### 使用 uv 的配置

**命令**：
```bash
claude mcp add skill-creator stdio uv run python -m skill_creator_mcp \
  --scope project \
  --env SKILL_CREATOR_LOG_LEVEL=DEBUG
```

**生成的 `.mcp.json`**：
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
      ],
      "env": {
        "SKILL_CREATOR_LOG_LEVEL": "DEBUG"
      }
    }
  }
}
```

---

## 相关文档

- [MCP Server Claude Code 配置指南](../../skill-creator-mcp/docs/claude-code-config.md) - MCP Server 详细配置
- [MCP Server 配置参数参考](../../skill-creator-mcp/docs/configuration.md) - 完整的环境变量配置
- [MCP Server IDE 集成配置](../../skill-creator-mcp/docs/ide-config.md) - 其他 IDE 配置示例
- [Agent-Skill 入口](../SKILL.md) - Agent-Skill 使用指南
