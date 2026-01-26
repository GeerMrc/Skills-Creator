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
