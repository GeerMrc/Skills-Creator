# MCP 配置参数说明与最佳实践

> **版本**: v0.3.0
> **更新日期**: 2026-01-26
> **审核状态**: ✅ 已验证

---

## 审核结论

### `uv --directory` 参数验证结果

✅ **有效参数** - `uv --directory` 在 uv 0.5.0+ 版本中是官方支持的参数

**官方说明**：
```
--directory <DIRECTORY>
    Change to the given directory prior to running the command
```

**版本要求**：uv >= 0.5.0

**验证命令**：
```bash
# 检查 uv 版本
uv --version

# 验证参数支持
uv --help | grep "directory"
```

---

## 工作目录机制详解

### ⚠️ 重要概念区分

MCP 配置中有**两个不同的目录概念**：

| 配置项 | 作用范围 | 控制对象 | 默认值 |
|--------|----------|----------|--------|
| `uv --directory` | MCP Server | Server 启动位置 | 无 |
| `cwd` | MCP Server | Server 工作目录 | 无 |
| `output_dir` | 工具参数 | 技能创建位置 | `"."` |
| `SKILL_CREATOR_OUTPUT_DIR` | 环境变量 | 全局默认输出目录 | `"."` |

### 工作流程图

```
┌─────────────────────────────────────────────────────────────┐
│                    Claude Code 启动目录                      │
│                  (如 /path/to/Skills-Creator)                │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  ┌──────────────────────────────────────────────────────┐  │
│  │   MCP Server 启动目录                                 │  │
│  │   (--directory 指定)                                  │  │
│  │                                                      │  │
│  │   /path/to/Skills-Creator/skill-creator-mcp          │  │
│  │                                                      │  │
│  │   Python 进程运行在此                                │  │
│  └──────────────────────────────────────────────────────┘  │
│                                                              │
│  ┌──────────────────────────────────────────────────────┐  │
│  │   技能创建目录 (output_dir=".")                        │  │
│  │                                                      │  │
│  │   技能创建在 Claude Code 启动目录下                    │  │
│  │                                                      │  │
│  │   /path/to/Skills-Creator/my-skill/                  │  │
│  └──────────────────────────────────────────────────────┘  │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

### 实际行为分析

**配置 A：使用 `--directory`（推荐）**

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

| 操作 | 执行位置 | 说明 |
|------|----------|------|
| MCP Server 启动 | `skill-creator-mcp/` | ✅ 正确位置 |
| 导入 `skill_creator_mcp` | ✅ 成功 | 在正确目录 |
| 创建技能 (默认) | Claude Code 启动目录 | ✅ 用户期望位置 |
| 创建技能 (指定 output_dir) | 指定目录 | ✅ 灵活控制 |

---

**配置 B：不使用 `--directory`（有问题）**

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

| 操作 | 执行位置 | 说明 |
|------|----------|------|
| MCP Server 启动 | Claude Code 启动目录 | ❌ 可能错误 |
| 导入 `skill_creator_mcp` | ❌ 可能失败 | 模块找不到 |
| 创建技能 (默认) | Claude Code 启动目录 | ⚠️ 取决于启动位置 |

**问题**：
- 如果不在 `skill-creator-mcp/` 目录启动 Claude Code，模块导入失败
- 依赖 `PYTHONPATH` 或系统 Python 安装

---

**配置 C：使用 `cwd`（替代方案）**

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

| 操作 | 执行位置 | 说明 |
|------|----------|------|
| MCP Server 启动 | `cwd` 指定目录 | ✅ 类似 `--directory` |
| 导入 `skill_creator_mcp` | ✅ 成功 | 在正确目录 |
| 创建技能 (默认) | Claude Code 启动目录 | ✅ 用户期望位置 |

---

### 推荐的项目结构

**标准项目布局**：

```
/path/to/Skills-Creator/          ← Claude Code 启动目录
├── skill-creator/                 ← Agent-Skill
├── skill-creator-mcp/             ← MCP Server (--directory 指向这里)
└── my-skills/                     ← 新技能创建在这里
    ├── my-first-skill/
    └── my-second-skill/
```

**配置示例**：

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
        "SKILL_CREATOR_OUTPUT_DIR": "/path/to/Skills-Creator/my-skills"
      }
    }
  }
}
```

**效果**：
- ✅ MCP Server 在 `skill-creator-mcp/` 启动
- ✅ 新技能默认创建在 `my-skills/` 目录
- ✅ 与项目代码分离，结构清晰

---

## 推荐配置方案

### 方案一：使用 uv（推荐）

**适用场景**：开发环境，已安装 uv 0.5.0+

**优点**：
- ✅ 自动管理虚拟环境
- ✅ 依赖隔离
- ✅ 快速启动

**配置示例**：

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

**注意事项**：
- 路径必须是绝对路径
- Windows 路径使用正斜杠 `/` 或双反斜杠 `\\`
- 确保 uv 版本 >= 0.5.0

---

### 方案二：使用虚拟环境

**适用场景**：使用传统 venv/virtualenv

**优点**：
- ✅ 兼容性好
- ✅ 无需额外工具

**配置示例**：

```json
{
  "mcpServers": {
    "skill-creator": {
      "command": "/absolute/path/to/.venv/bin/python",
      "args": ["-m", "skill_creator_mcp"],
      "cwd": "/absolute/path/to/Skills-Creator/skill-creator-mcp",
      "env": {
        "PYTHONPATH": "/absolute/path/to/Skills-Creator/skill-creator-mcp/src",
        "SKILL_CREATOR_LOG_LEVEL": "INFO"
      }
    }
  }
}
```

**Windows 虚拟环境配置**：

```json
{
  "mcpServers": {
    "skill-creator": {
      "command": "C:\\path\\to\\.venv\\Scripts\\python.exe",
      "args": ["-m", "skill_creator_mcp"],
      "cwd": "C:\\path\\to\\Skills-Creator\\skill-creator-mcp"
    }
  }
}
```

---

### 方案三：使用全局 Python

**适用场景**：已将 skill-creator-mcp 安装到系统 Python

**优点**：
- ✅ 配置最简单
- ✅ 无需指定路径

**前提条件**：

```bash
# 进入 MCP Server 目录
cd skill-creator-mcp

# 安装到系统 Python
pip install -e .
```

**配置示例**：

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

### 方案四：使用 uv run（简化版）

**适用场景**：在项目目录下运行 MCP 客户端

**配置示例**：

```json
{
  "mcpServers": {
    "skill-creator": {
      "command": "uv",
      "args": [
        "run",
        "--no-config",
        "-m",
        "skill_creator_mcp"
      ],
      "cwd": "/absolute/path/to/Skills-Creator/skill-creator-mcp"
    }
  }
}
```

---

## 路径配置最佳实践

### 绝对路径 vs 相对路径

| 路径类型 | 推荐度 | 说明 |
|---------|--------|------|
| **绝对路径** | ✅ 推荐 | 明确、无歧义 |
| **相对路径** | ⚠️ 谨慎使用 | 依赖工作目录，可能出错 |
| **~/ 路径** | ❌ 不支持 | MCP 客户端通常不展开 |

### 跨平台路径处理

**推荐**：始终使用正斜杠 `/`

```json
// ✅ 正确（所有平台）
"directory": "C:/Users/username/Skills-Creator/skill-creator-mcp"

// ✅ 正确（Unix）
"directory": "/home/username/Skills-Creator/skill-creator-mcp"

// ❌ 错误（Windows 反斜杠需要转义）
"directory": "C:\Users\username\Skills-Creator\skill-creator-mcp"

// ✅ 正确（Windows 双反斜杠）
"directory": "C:\\Users\\username\\Skills-Creator\\skill-creator-mcp"
```

---

## 常见问题排查

### 问题1: uv --directory 不工作

**可能原因**：
1. uv 版本过低（< 0.5.0）
2. 路径不正确
3. 权限问题

**解决方案**：

```bash
# 1. 检查 uv 版本
uv --version

# 2. 如果版本过低，更新 uv
curl -LsSf https://astral.sh/uv/install.sh | sh

# 3. 验证路径
ls -la /path/to/skill-creator-mcp

# 4. 测试配置
cd /tmp
uv --directory /path/to/skill-creator-mcp run python -c "print('OK')"
```

### 问题2: 模块找不到

**错误信息**：`ModuleNotFoundError: No module named 'skill_creator_mcp'`

**解决方案**：

1. **方案一**：设置 PYTHONPATH
```json
{
  "env": {
    "PYTHONPATH": "/path/to/skill-creator-mcp/src"
  }
}
```

2. **方案二**：使用 cwd 参数
```json
{
  "cwd": "/path/to/skill-creator-mcp"
}
```

3. **方案三**：安装到虚拟环境
```bash
cd /path/to/skill-creator-mcp
uv pip install -e .
```

### 问题3: 权限错误

**错误信息**：`Permission denied`

**解决方案**：

```bash
# 确保 Python 路径可执行
chmod +x /path/to/.venv/bin/python

# 或使用绝对路径
ls -la /path/to/.venv/bin/python
```

---

## IDE 特定配置

### Claude Code (VSCode)

```bash
# 推荐使用 claude mcp add 命令
cd /path/to/Skills-Creator
claude mcp add skill-creator stdio python -m skill_creator_mcp
```

### Claude Desktop

**macOS/Linux**：`~/.config/Claude/claude_desktop_config.json`
**Windows**：`%APPDATA%/Claude/claude_desktop_config.json`

### Cursor

**配置文件**：Settings → MCP Servers

### Continue.dev

**配置文件**：`~/.continue/config.json`

---

## 配置验证清单

- [ ] uv 版本 >= 0.5.0（如使用 uv）
- [ ] 路径使用绝对路径
- [ ] 路径使用正斜杠或正确转义
- [ ] PYTHONPATH 正确设置（如需要）
- [ ] 虚拟环境存在（如使用 venv）
- [ ] 测试配置：手动运行命令验证

---

## 参考资源

- [uv 官方文档](https://github.com/astral-sh/uv)
- [MCP 规范](https://modelcontextprotocol.io/)
- [FastMCP 文档](https://jlowin.github.io/fastmcp/)
