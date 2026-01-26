# Skill Creator MCP 安装与配置指南

> 版本: 0.3.0
> 更新日期: 2026-01-26

---

## 系统要求

### 最低要求

| 组件 | 要求 |
|------|------|
| **操作系统** | Windows 10+, macOS 10.15+, Linux |
| **Python** | 3.10 或更高版本 |
| **内存** | 512 MB 可用内存 |
| **磁盘空间** | 100 MB 可用空间 |

### 推荐配置

| 组件 | 推荐 |
|------|------|
| **Python** | 3.11 或更高 |
| **内存** | 1 GB 或更多 |
| **磁盘空间** | 200 MB 或更多 |

---

## 安装方法

Skill Creator MCP 提供**开发模式**和**Wheel文件**两种安装方式。

### 开发模式安装 ⭐ （推荐）

直接从源代码以可编辑模式安装。

#### 使用 uv（推荐）

```bash
# 1. 进入 MCP Server 目录
cd skill-creator-mcp

# 2. 安装 uv（如果未安装）
pip install uv

# 3. 同步依赖（包括开发依赖）
uv sync --dev
```

#### 使用虚拟环境

```bash
# 1. 进入 MCP Server 目录
cd skill-creator-mcp

# 2. 创建虚拟环境
python -m venv .venv

# 3. 激活虚拟环境
# macOS/Linux:
source .venv/bin/activate
# Windows:
.venv\Scripts\activate

# 4. 以开发模式安装
pip install -e ".[dev]"
```

**开发模式的优势**：
- ✅ 代码修改立即生效，无需重新安装
- ✅ 指向源代码目录，而非复制文件
- ✅ 适合开发和测试
- ✅ 可以使用 `git pull` 更新代码

---

### Wheel 文件安装（生产环境）

从源码构建 Wheel 文件后安装。

#### 构建和安装

```bash
# 1. 进入 MCP Server 目录
cd skill-creator-mcp

# 2. 安装构建工具
pip install build

# 3. 构建 Wheel 文件
python -m build

# 4. 安装 Wheel 文件
pip install dist/skill_creator_mcp-*.whl
```

#### 使用 uv 构建（更快）

```bash
# 1. 进入 MCP Server 目录
cd skill-creator-mcp

# 2. 使用 uv 构建
uv build

# 3. 安装 Wheel 文件
uv pip install dist/skill_creator_mcp-*.whl
```

---

## 验证安装

### 检查安装

```bash
# 检查是否安装成功
python -c "import skill_creator_mcp; print('✅ 安装成功')"

# 查看帮助信息
python -m skill_creator_mcp --help
```

### 运行测试

```bash
# 进入 MCP Server 目录
cd skill-creator-mcp

# 运行测试套件
uv run pytest

# 查看测试覆盖率
uv run pytest --cov

# 代码质量检查
uv run ruff check .
uv run mypy src/
```

---

## 快速配置

### 1. 创建配置文件

```bash
# 复制示例配置
cp .env.example .env

# 编辑配置
nano .env
```

### 2. 基础配置

```bash
# .env 文件内容
SKILL_CREATOR_LOG_LEVEL=INFO
SKILL_CREATOR_OUTPUT_DIR=.
```

### 3. 启动服务器

```bash
# STDIO 模式（本地）
uv run python -m skill_creator_mcp

# 或使用已安装的包
python -m skill_creator_mcp
```

详细的配置选项请参考：[配置参数参考](./configuration.md)

---

## IDE 集成配置

### Claude Desktop

配置示例：

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
      ],
      "env": {
        "SKILL_CREATOR_LOG_LEVEL": "INFO"
      }
    }
  }
}
```

### Claude Code

```bash
# 添加 MCP 服务器
cd /path/to/Skills-Creator
claude mcp add skill-creator stdio python -m skill_creator_mcp
```

详细的 IDE 配置请参考：
- [IDE 集成配置](./ide-config.md)
- [Claude Code 配置指南](./claude-code-config.md)

---

## 传输模式

Skill Creator MCP 支持两种传输模式：

### STDIO 模式（本地）

适用于本地开发场景，通过标准输入输出进行通信。

```bash
python -m skill_creator_mcp
```

### SSE 模式（远程）

适用于远程服务器部署，通过 HTTP Server-Sent Events 进行通信。

```bash
python -m skill_creator_mcp.http
# 访问: http://localhost:8000
```

详细的 SSE 配置请参考：[SSE 配置指南](./sse-guide.md)

---

## 升级与卸载

### 升级

**开发模式**：
```bash
# 拉取最新代码
cd skill-creator-mcp
git pull

# 重新安装（如果依赖有变化）
uv sync --dev
```

**Wheel 安装**：
```bash
# 构建新版本
cd skill-creator-mcp
python -m build

# 强制重新安装
pip install --force-reinstall dist/skill_creator_mcp-*.whl
```

### 卸载

```bash
pip uninstall skill-creator-mcp
```

---

## 故障排除

### 安装问题

**问题：Python 版本不兼容**
```
错误：Python 3.10 或更高版本 required
解决：升级 Python 版本
```

**问题：依赖安装失败**
```bash
# 更新 pip
pip install --upgrade pip

# 清除缓存重试
pip install --no-cache-dir -e ".[dev]"
```

### 运行问题

**问题：模块未找到**
```bash
# 确认安装位置
pip show skill-creator-mcp

# 重新安装
pip install --force-reinstall -e .
```

**问题：权限错误**
```bash
# 使用用户安装
pip install --user -e ".[dev]"
```

---

## 下一步

- ⚙️ 查看 [配置参数参考](./configuration.md) 了解所有配置选项
- 🔌 参考 [IDE 集成配置](./ide-config.md) 在你的 IDE 中配置
- 🌐 阅读 [SSE 配置指南](./sse-guide.md) 了解远程部署

---

## 相关文档

- [配置参数参考](./configuration.md) - 完整的环境变量配置
- [IDE 集成配置](./ide-config.md) - 各种 IDE 的配置示例
- [Claude Code 配置指南](./claude-code-config.md) - Claude Code 详细配置
- [SSE 配置指南](./sse-guide.md) - SSE 远程模式详细配置
