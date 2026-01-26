# 添加 claude mcp add-json 配置方式说明

> **计划ID**: generic-wiggling-rossum
> **创建日期**: 2026-01-26
> **计划类型**: 文档更新
> **优先级**: P1

---

## 一、任务概述

### 1.1 目标

在相关配置说明文档中添加 `claude mcp add-json` 方式配置说明，参考用户提供的 Time 服务器示例。

### 1.2 参考示例

```json
{
  "command": "python",
  "args": ["-m", "mcp_server_time", "--local-timezone=Asia/Shanghai"]
}
```

```bash
# claude mcp add-json 方式添加 --scope user
claude mcp add-json "Time" '{"command": "python", "args": ["-m", "mcp_server_time", "--local-timezone=Asia/Shanghai"]}' --scope user
```

### 1.3 需求分析

`claude mcp add-json` 是 Claude Code CLI 的一个命令，允许直接传递 JSON 配置来添加 MCP 服务器，相比于 `claude mcp add` 命令：

| 对比项 | `claude mcp add` | `claude mcp add-json` |
|--------|-----------------|----------------------|
| **配置方式** | 命令行参数 | JSON 字符串 |
| **复杂配置** | 需要多行转义 | 简洁明了 |
| **适用场景** | 简单配置 | 复杂配置（如源码开发） |

---

## 二、步骤0：前置任务审核

### 2.1 Git 环境检查

```bash
git branch --show-current  # develop
git status --short         # clean
```

### 2.2 前置任务

- ✅ 无前置任务
- ✅ 当前分支: develop
- ✅ 工作区: clean

---

## 三、需要更新的文档

| 优先级 | 文档路径 | 更新内容 |
|--------|----------|----------|
| P0 | `skill-creator-mcp/docs/claude-code-config.md` | 添加 add-json 命令详细说明 |
| P1 | `skill-creator-mcp/README.md` | 在快速开始中添加 add-json 示例 |
| P1 | `README.md` | 在配置部分添加 add-json 示例 |

---

## 四、详细实施方案

### 4.1 claude-code-config.md 更新（P0）

**位置**: 第 65-134 行（配置方式章节）

**新增内容**（插入到"方式1：CLI 命令"章节中）：

```markdown
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
```

**CLI 命令参考章节**（第 138-189 行）也需要更新：

```markdown
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
```

### 4.2 skill-creator-mcp/README.md 更新（P1）

**位置**: 第 77-152 行（5分钟快速开始章节）

**在快速开始章节中添加新的配置方式**：

```markdown
## 5分钟快速开始

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
```

### 4.3 README.md 更新（P1）

**位置**: 第 49-150 行（安装步骤章节）

**在配置部分添加 add-json 示例**：

```markdown
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
```

---

## 五、任务清单

| ID | 任务 | 优先级 | 状态 |
|----|------|--------|------|
| 1 | 更新 claude-code-config.md（方式1章节） | P0 | pending |
| 2 | 更新 claude-code-config.md（CLI命令参考章节） | P0 | pending |
| 3 | 更新 skill-creator-mcp/README.md（快速开始） | P1 | pending |
| 4 | 更新根目录 README.md（安装步骤） | P1 | pending |
| 5 | 验证文档交叉引用链接 | P2 | pending |
| 6 | 更新 CHANGELOG.md | P2 | pending |

---

## 六、验收标准

### 6.1 文档完整性

- ✅ 三个主要文档都包含 `claude mcp add-json` 配置说明
- ✅ 示例包含全局安装和源码开发两种方式
- ✅ 包含 `--scope` 参数说明
- ✅ 包含 `claude mcp add` 和 `claude mcp add-json` 的对比

### 6.2 格式规范

- ✅ Markdown 格式正确
- ✅ 代码块语法高亮正确
- ✅ 表格格式正确

### 6.3 一致性

- ✅ 全局安装和源码开发配置区分清晰
- ✅ 命令示例与现有文档风格一致

---

## 七、测试计划

### 7.1 文档测试

```bash
# 验证 markdown 链接
find . -name "*.md" -exec grep -H "\[.*\](" {} \;

# 验证代码块语法
# （手动检查）
```

### 7.2 命令验证

```bash
# 验证 claude mcp add-json 命令格式
claude mcp add-json --help
```

---

## 八、风险与注意事项

| 风险 | 影响 | 缓解措施 |
|------|------|----------|
| JSON 格式错误 | 用户配置失败 | 提供正确的示例和转义说明 |
| scope 参数混淆 | 配置位置错误 | 提供清晰的 scope 对比表 |
| 跨平台引号问题 | 命令执行失败 | 提供单引号包裹的 JSON 示例 |

---

## 九、实施时间估算

| 任务 | 预计时间 |
|------|----------|
| 更新 claude-code-config.md | 30 分钟 |
| 更新 skill-creator-mcp/README.md | 15 分钟 |
| 更新根目录 README.md | 15 分钟 |
| 验证和测试 | 20 分钟 |
| **总计** | **80 分钟** |
