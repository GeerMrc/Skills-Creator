# Skill Creator MCP Server

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)

Agent-Skills 开发与质量保证 MCP Server。

## 开发状态

> 🚧 **项目正在开发中**
>
> 当前版本：v0.1.0-alpha
>
> 这是 Skill-Creator 项目的 MCP Server 组件，提供创建、验证、分析和重构 Agent-Skills 的工具。

## 特性

- ✅ 4 种技能模板（minimal, tool-based, workflow-based, analyzer-based）
- 🚧 自动化规范验证
- 🚧 Token 效率分析
- 🚧 反模式识别
- 🚧 重构建议生成
- 🚧 打包发布工具

*注：✅ 已实现 | 🚧 开发中*

## 安装

### 使用 uv（推荐）

```bash
# 克隆仓库
git clone <repository-url>
cd skill-creator-mcp

# 安装依赖
uv sync --dev
```

### 使用 pip

```bash
pip install -e ".[dev]"
```

## 配置

### Claude Code 配置

编辑 `~/.config/Claude/claude_desktop_config.json`：

```json
{
  "mcpServers": {
    "skill-creator": {
      "command": "uv",
      "args": [
        "--directory",
        "/path/to/skill-creator-mcp",
        "run",
        "python",
        "-m",
        "skill_creator_mcp"
      ]
    }
  }
}
```

## 使用

### 初始化技能

```
调用 mcp__skill_creator__init_skill，参数：
- name: "my-skill"
- template: "tool-based"
- output_dir: "./skills"
```

### 验证技能

```
调用 mcp__skill_creator__validate_skill，参数：
- path: "/path/to/skill"
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
