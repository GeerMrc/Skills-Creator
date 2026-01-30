# v0.3.6 发布说明

## 发布状态：已完成 ✅

### 1. Git Tag 推送
```bash
git push origin v0.3.6  # ✅ 已成功
```

### 2. GitHub Release 创建
```
https://github.com/GeerMrc/Skills-Creator/releases/tag/v0.3.6  # ✅ 已创建
```

### 3. PyPI 发布
```bash
uv publish --token $PYPI_API_TOKEN dist/skill_creator_mcp-0.3.6-py3-none-any.whl dist/skill_creator_mcp-0.3.6.tar.gz
```
**验证**: https://pypi.org/project/skill-creator-mcp/0.3.6/ ✅

### 4. 发布产物

| 产物 | 路径 | 大小 | 状态 |
|------|------|------|------|
| Agent-Skill | `skill-creator-v0.3.6.zip` | 68KB (35文件) | ✅ |
| MCP Wheel | PyPI: `skill-creator-mcp==0.3.6` | 86KB | ✅ |
| MCP Source | PyPI: `skill-creator-mcp==0.3.6` | 442KB | ✅ |

---

## 用户安装说明

### 从 PyPI 安装（推荐）

**MCP Server:**
```bash
pip install skill-creator-mcp==0.3.6
```

**Agent-Skill:**
```bash
# 从 GitHub Release 下载
wget https://github.com/GeerMrc/Skills-Creator/releases/download/v0.3.6/skill-creator-v0.3.6.zip

# 解压到 Claude Desktop skills 目录
unzip skill-creator-v0.3.6.zip -d ~/.config/claude/skills/
```

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

### 安装步骤

**1. 安装 MCP Server**

```bash
# 使用 pip
pip install skill-creator-mcp

# 或使用 uv pip
uv pip install skill-creator-mcp
```

**2. 配置 Claude Code**

**方式1：使用 claude mcp add-json（推荐）**

```bash
claude mcp add-json "skill-creator" '{
  "command": "python",
  "args": ["-m", "skill_creator_mcp"]
}' --scope user
```

**方式2：手动编辑配置文件**

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

**3. 验证安装**

在 Claude Code 中输入：
```
使用 skill-creator MCP 工具初始化一个名为 "my-skill" 的技能
```

---

## 质量指标

- **测试覆盖率**: 97% (553个测试用例)
- **工具数量**: 12个 (4技能+7需求+1打包)
- **代码质量**: ruff 0错误, mypy 0错误, bandit 0高危

---

## 创建时间
2026-01-30
