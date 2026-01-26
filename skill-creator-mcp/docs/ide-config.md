# Skill Creator MCP IDE 配置指南

> 版本: 0.3.0
> 更新日期: 2026-01-26
> 适用对象: Claude Desktop、Claude Code、Cursor、Continue.dev 等 MCP 客户端用户

---

## 概述

Skill Creator MCP 支持通过 MCP (Model Context Protocol) 协议与各种 IDE 和代码编辑器集成。

**环境变量配置**：请参考 [配置参数参考](./configuration.md)

### 支持的 IDE

| IDE / 编辑器 | 支持状态 | 传输模式 |
|-------------|---------|----------|
| Claude Desktop | ✅ 完全支持 | STDIO |
| Claude Code (VSCode) | ✅ 完全支持 | STDIO |
| Cursor | ✅ 完全支持 | STDIO |
| Continue.dev | ✅ 完全支持 | STDIO |

---

## Claude Desktop 配置

### 配置文件位置

| 操作系统 | 配置文件路径 |
|---------|-------------|
| **macOS** | `~/Library/Application Support/Claude/claude_desktop_config.json` |
| **Windows** | `%APPDATA%/Claude/claude_desktop_config.json` |
| **Linux** | `~/.config/Claude/claude_desktop_config.json` |

### 基础 STDIO 配置

**使用 uv（推荐）**：
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
        "SKILL_CREATOR_LOG_LEVEL": "INFO"
      }
    }
  }
}
```

**使用虚拟环境**：
```json
{
  "mcpServers": {
    "skill-creator": {
      "command": "/path/to/.venv/bin/python",
      "args": ["-m", "skill_creator_mcp"],
      "env": {
        "SKILL_CREATOR_LOG_LEVEL": "INFO"
      }
    }
  }
}
```

**使用已安装的包**：
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

---

## Claude Code (VSCode) 配置

> 💡 **详细配置**：请参考 [Claude Code 配置完整指南](./claude-code-config.md)

### 快速开始

```bash
# 进入项目目录
cd /path/to/Skills-Creator

# 添加 MCP 服务器
claude mcp add skill-creator stdio python -m skill_creator_mcp
```

### 配置文件方式

编辑 `~/.claude/settings.json` 或项目的 `.mcp.json`：

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

### 配置范围说明

| 范围 | 存储位置 | 可提交VC | 共享范围 | 适用场景 |
|------|---------|---------|---------|---------|
| **project** | `.mcp.json` | ✅ | 团队 | 团队协作开发 |
| **user** | `~/.claude/settings.json` | ❌ | 个人 | 跨项目使用 |
| **local** | `.claude/settings.json` | ❌ | 个人 | 临时测试 |

**项目级配置示例**（推荐团队使用）：
```bash
cd /path/to/Skills-Creator
claude mcp add skill-creator stdio python -m skill_creator_mcp --scope project
```

---

## Cursor 配置

### 配置文件位置

| 操作系统 | 配置文件路径 |
|---------|-------------|
| **macOS** | `~/Library/Application Support/Cursor/User/globalStorage/mcp_servers_config.json` |
| **Windows** | `%APPDATA%/Cursor/User/globalStorage/mcp_servers_config.json` |
| **Linux** | `~/.config/Cursor/User/globalStorage/mcp_servers_config.json` |

### STDIO 模式配置

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

### 使用 uv 配置

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

---

## Continue.dev 配置

### 配置文件位置

`~/.continue/config.json`

### STDIO 模式配置

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

---

## 通用配置选项

### 环境变量

所有 IDE 都支持通过 `env` 字段传递环境变量：

```json
{
  "env": {
    "SKILL_CREATOR_LOG_LEVEL": "DEBUG",
    "SKILL_CREATOR_OUTPUT_DIR": "~/skills-output",
    "SKILL_CREATOR_MAX_RETRIES": "5"
  }
}
```

**常用环境变量**：
- `SKILL_CREATOR_LOG_LEVEL` - 日志级别（DEBUG/INFO/WARNING/ERROR/CRITICAL）
- `SKILL_CREATOR_OUTPUT_DIR` - 输出目录
- `SKILL_CREATOR_MAX_RETRIES` - 最大重试次数
- `SKILL_CREATOR_TIMEOUT_SECONDS` - 超时时间

详细的环境变量配置请参考：[配置参数参考](./configuration.md)

### 使用虚拟环境

确保使用正确的 Python 解释器：

```json
{
  "command": "/path/to/.venv/bin/python"
}
```

或使用工作目录：

```json
{
  "command": "python",
  "args": ["-m", "skill_creator_mcp"],
  "cwd": "/path/to/skill-creator-mcp"
}
```

---

## 验证配置

### 检查 MCP 连接

1. 重启 IDE
2. 查看 MCP 日志
3. 验证工具列表（应显示 16 个工具）

### 可用工具列表

**核心开发工具（6个）**：
1. `init_skill` - 初始化新的 Agent-Skill
2. `validate_skill` - 验证技能结构和内容
3. `analyze_skill` - 分析代码质量和复杂度
4. `refactor_skill` - 生成重构建议
5. `package_skill` - 打包发布工具
6. `collect_requirements` - AI 驱动的需求澄清

**批量操作（2个）**：
7. `batch_validate_skills_tool` - 批量验证多个技能
8. `batch_analyze_skills_tool` - 批量分析多个技能

**健康检查（3个）**：
9. `health_check_tool` - 完整健康检查
10. `quick_status_tool` - 快速状态摘要
11. `is_healthy_tool` - 快速健康检查

**Phase 0验证工具（5个）**：
12. `check_client_capabilities` - 检测客户端能力
13. `test_llm_sampling` - 测试 LLM Sampling
14. `test_user_elicitation` - 测试用户征询
15. `test_conversation_loop` - 测试对话循环
16. `test_requirement_completeness` - 测试需求完整性

### 常见问题

**问题：找不到模块**
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
- 确认已安装最新版本
- 重启 IDE 使配置生效

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
- [Claude Code 配置完整指南](./claude-code-config.md) - Claude Code 详细配置
- [安装指南](./installation.md) - 安装和验证
- [SSE 配置指南](./sse-guide.md) - SSE 远程模式详细配置
