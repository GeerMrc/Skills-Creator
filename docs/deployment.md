# 部署指南

本文档介绍如何部署 Skills-Creator MCP Server。

---

## 目录

- [环境要求](#环境要求)
- [安装步骤](#安装步骤)
- [配置](#配置)
- [Docker 部署](#docker-部署)
- [生产环境](#生产环境)

---

## 环境要求

### 最低要求

- Python >= 3.10
- pip 或 uv 包管理器
- 100MB 可用磁盘空间

### 推荐配置

- Python 3.12+
- uv 包管理器
- 512MB 可用内存

---

## 安装步骤

### 使用 uv（推荐）

```bash
# 1. 克隆仓库
git clone https://github.com/yourusername/Skills-Creator.git
cd Skills-Creator/skill-creator-mcp

# 2. 安装依赖
uv sync --dev

# 3. 验证安装
uv run python -m skill_creator_mcp --help
```

### 使用 pip

```bash
# 1. 克隆仓库
git clone https://github.com/yourusername/Skills-Creator.git
cd Skills-Creator/skill-creator-mcp

# 2. 安装依赖
pip install -e ".[dev]"

# 3. 验证安装
python -m skill_creator_mcp --help
```

---

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

### 环境变量配置

创建 `.env` 文件：

```bash
cp .env.example .env
vim .env
```

**常用配置**：

```bash
# 日志级别
SKILL_CREATOR_LOG_LEVEL=INFO

# 输出目录
SKILL_CREATOR_OUTPUT_DIR=./output

# 开发模式
SKILL_CREATOR_DEV_MODE=false
```

---

## Docker 部署

### 构建 Docker 镜像

```bash
cd skill-creator-mcp
docker build -t skill-creator-mcp:latest .
```

### 运行容器（STDIO 模式）

```bash
docker run -d \
  --name skill-creator \
  -v /path/to/output:/app/output \
  -e SKILL_CREATOR_LOG_LEVEL=INFO \
  skill-creator-mcp:latest
```

### 运行容器（HTTP/SSE 模式）

```bash
docker run -d \
  --name skill-creator-http \
  -p 8000:8000 \
  -v /path/to/output:/app/output \
  -e SKILL_CREATOR_LOG_LEVEL=INFO \
  skill-creator-mcp:latest \
  python -m skill_creator_mcp.http
```

### Docker Compose

```yaml
version: '3.8'
services:
  skill-creator:
    build: ./skill-creator-mcp
    container_name: skill-creator
    volumes:
      - ./output:/app/output
    environment:
      - SKILL_CREATOR_LOG_LEVEL=INFO
      - SKILL_CREATOR_OUTPUT_DIR=/app/output
    restart: unless-stopped

  # HTTP 模式服务（可选）
  skill-creator-http:
    build: ./skill-creator-mcp
    container_name: skill-creator-http
    ports:
      - "8000:8000"
    volumes:
      - ./output:/app/output
    environment:
      - SKILL_CREATOR_LOG_LEVEL=INFO
    restart: unless-stopped
    command: python -m skill_creator_mcp.http
```

### Docker 容器管理示例

```bash
# 查看容器日志
docker logs -f skill-creator

# 进入容器调试
docker exec -it skill-creator bash

# 停止容器
docker stop skill-creator

# 删除容器
docker rm skill-creator

# 重启容器
docker restart skill-creator
```

### 常见环境变量

```bash
# 日志级别
-e SKILL_CREATOR_LOG_LEVEL=DEBUG

# 输出目录
-e SKILL_CREATOR_OUTPUT_DIR=/app/output

# 最大重试次数
-e SKILL_CREATOR_MAX_RETRIES=5

# 超时时间（秒）
-e SKILL_CREATOR_TIMEOUT_SECONDS=60

# 开发模式
-e SKILL_CREATOR_DEV_MODE=true
```

---

## 生产环境

### 性能优化

1. **缓存机制**：使用文件缓存提高重复操作速度
2. **并发处理**：启用异步处理多个请求
3. **资源限制**：设置合理的内存和 CPU 限制

### 监控

```bash
# 查看日志
tail -f /var/log/skill-creator.log

# 检查服务状态
ps aux | grep skill_creator_mcp
```

### 日志管理

配置日志轮转：

```bash
# /etc/logrotate.d/skill-creator
/var/log/skill-creator.log {
    daily
    rotate 7
    compress
    missingok
    notifempty
}
```

---

## 故障排除

### 常见问题

1. **ImportError**: 确保所有依赖已安装
   ```bash
   uv sync --dev
   ```

2. **权限错误**: 检查输出目录权限
   ```bash
   chmod 755 /path/to/output
   ```

3. **端口占用**: 检查是否有其他服务占用端口

---

## 更新

```bash
# 拉取最新代码
git pull origin main

# 更新依赖
uv sync --dev

# 验证更新
uv run pytest --cov
```

---

**相关文档**：
- [开发指南](../CLAUDE.md)
- [贡献指南](contributing.md)
