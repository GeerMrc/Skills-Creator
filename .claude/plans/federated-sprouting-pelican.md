# Skill-Creator 完整开发执行计划

> **计划版本**：v2.0
> **最后更新**：2026-01-20
> **状态**：已审核通过

---

## 项目概述

**项目名称**：skill-creator

**核心定位**：一个基于 **MCP Server + Agent-Skill 混合架构**的完整解决方案，用于开发、验证和优化 Agent-Skills。

**技术架构决策**：
- **MCP Server**：使用 FastMCP SDK 开发，提供 Tools、Resources、Prompts
- **Agent-Skill**：编排 MCP 工具，提供渐进式披露的知识和工作流

---

## 一、架构设计

### 1.1 完整架构图

```
┌─────────────────────────────────────────────────────────────────┐
│                        Claude Code / Desktop                     │
│                                                                 │
│  ┌───────────────────────────────────────────────────────────┐  │
│  │           skill-creator (Agent-Skill)                     │  │
│  │                                                           │  │
│  │  职责：教 Claude 如何创建技能                              │  │
│  │  - 渐进式披露三层架构                                      │  │
│  │  - 工作流定义（初始化 → 验证 → 分析 → 重构 → 打包）        │  │
│  │  - 最佳实践知识传递                                        │  │
│  │  - 编排 MCP 工具                                           │  │
│  │                                                           │  │
│  │  ┌─────────────────────────────────────────────────┐     │  │
│  │  │         MCP 客户端层                            │     │  │
│  │  └────────────────┬────────────────────────────────┘     │  │
│  └───────────────────┼───────────────────────────────────────┘  │
│                      │                                          │
│  ┌───────────────────▼───────────────────────────────────────┐  │
│  │              MCP Server (skill-creator-mcp)               │  │
│  │                                                           │  │
│  │  ┌─────────────────────────────────────────────────┐     │  │
│  │  │  Tools（可执行函数）                              │     │  │
│  │  │  • init_skill() - 初始化技能                     │     │  │
│  │  │  • validate_skill() - 验证技能                   │     │  │
│  │  │  • analyze_skill() - 分析技能                    │     │  │
│  │  │  • refactor_skill() - 重构建议                   │     │  │
│  │  │  • package_skill() - 打包技能                    │     │  │
│  │  └─────────────────────────────────────────────────┘     │  │
│  │                                                           │  │
│  │  ┌─────────────────────────────────────────────────┐     │  │
│  │  │  Resources（只读数据源）                          │     │  │
│  │  │  • skill://templates/{type} - 技能模板            │     │  │
│  │  │  • skill://best-practices - 最佳实践              │     │  │
│  │  │  • skill://validation-rules - 验证规则            │     │  │
│  │  └─────────────────────────────────────────────────┘     │  │
│  │                                                           │  │
│  │  ┌─────────────────────────────────────────────────┐     │  │
│  │  │  Prompts（可重用模板）                            │     │  │
│  │  │  • create-skill - 创建技能模板                    │     │  │
│  │  │  • validate-skill - 验证技能模板                  │     │  │
│  │  │  • refactor-skill - 重构技能模板                  │     │  │
│  │  └─────────────────────────────────────────────────┘     │  │
│  └───────────────────────────────────────────────────────────┘  │
│                      │                                          │
│                      ▼                                          │
│              文件系统 / Git                                     │
└─────────────────────────────────────────────────────────────────┘
```

### 1.2 MCP Server vs Agent-Skill 职责划分

| 维度 | MCP Server | Agent-Skill |
|------|-----------|-------------|
| **本质** | 标准化协议服务 | 能力扩展机制 |
| **开发方式** | FastMCP SDK + Python | 文件系统架构 |
| **传输协议** | STDIO / SSE | N/A |
| **提供内容** | Tools（原子操作）<br>Resources（数据源）<br>Prompts（模板） | 工作流定义<br>最佳实践知识<br>渐进式披露 |
| **控制方** | Model 控制工具调用<br>Application 控制资源<br>User 控制提示 | Claude 自主判断激活 |
| **相互关系** | 被 Agent-Skill 编排调用 | 编排 MCP 工具完成任务 |

---

## 二、开发执行规范（新增）

### 2.1 Git 工作流

采用 **Feature Branch Workflow**：

```
main (生产分支)
  │
  ├─ develop (开发分支)
  │   │
  │   ├─ feature/server-framework (功能分支)
  │   ├─ feature/init-skill-tool
  │   ├─ feature/validate-skill-tool
  │   └─ feature/agent-skill
  │
  └─ hotfix/critical-bug (热修复分支)
```

**分支命名规范**：
- `feature/功能描述` - 新功能开发
- `fix/问题描述` - Bug 修复
- `hotfix/紧急问题` - 生产环境紧急修复
- `refactor/重构描述` - 代码重构
- `docs/文档更新` - 文档更新
- `test/测试相关` - 测试相关

**分支操作规范**：
```bash
# 1. 从 develop 创建功能分支
git checkout develop
git pull origin develop
git checkout -b feature/server-framework

# 2. 开发完成后推送到远程
git push -u origin feature/server-framework

# 3. 创建 Pull Request 到 develop
# 通过 GitHub / GitLab 界面创建

# 4. Code Review 通过后合并
# 使用 Squash and Merge 保持提交历史整洁

# 5. 合并后删除功能分支
git branch -d feature/server-framework
```

### 2.2 Commit 规范

采用 **Conventional Commits** 格式：

```
<type>(<scope>): <subject>

<body>

<footer>
```

**Type 类型**：
- `feat` - 新功能
- `fix` - Bug 修复
- `docs` - 文档更新
- `style` - 代码格式（不影响功能）
- `refactor` - 重构（既不是新功能也不是修复）
- `test` - 测试相关
- `chore` - 构建过程或辅助工具变动

**示例**：
```bash
# 新功能
git commit -m "feat(tools): add init_skill tool implementation"

# Bug 修复
git commit -m "fix(validators): handle edge case in skill name validation

Fixes issue where skill names with consecutive hyphens were incorrectly rejected."

# 文档更新
git commit -m "docs(readme): update installation instructions"

# 重构
git commit -m "refactor(models): extract common validation logic"
```

**Commit 消息要求**：
1. 使用中文（与用户沟通语言一致）
2. subject 行不超过 50 字符
3. subject 行首字母大写
4. subject 行结尾不加句号
5. body 行每行不超过 72 字符
6. footer 必须包含关闭的 issue 编号（如有）

### 2.3 Code Review 规范

**Pull Request 模板**：
```markdown
## 变更说明
<!-- 简要描述本次变更的内容 -->

## 变更类型
- [ ] feat - 新功能
- [ ] fix - Bug 修复
- [ ] docs - 文档更新
- [ ] refactor - 重构
- [ ] test - 测试
- [ ] chore - 其他

## 测试情况
- [ ] 单元测试已通过
- [ ] 集成测试已通过
- [ ] 手动测试已完成

## 检查清单
- [ ] 代码符合项目规范（ruff 通过）
- [ ] 类型检查通过（mypy 通过）
- [ ] 测试覆盖率符合要求（>80%）
- [ ] 文档已更新（如需要）
- [ ] 无新增 TODO（或已创建 issue 追踪）

## 相关 Issue
Closes #(issue number)
```

**Code Review 检查项**：
1. **功能正确性**：代码是否实现了预期功能
2. **代码质量**：是否符合项目编码规范
3. **测试覆盖**：是否有足够的测试覆盖
4. **文档完整性**：文档是否同步更新
5. **性能考虑**：是否存在性能问题
6. **安全性**：是否存在安全漏洞

**Review 流程**：
1. 作者创建 PR
2. 自动检查（CI/CD）运行
3. 至少一名审查者人工 Review
4. 提出修改意见或批准
5. 修改通过后合并

### 2.4 环境初始化检查清单

**开发环境初始化**：

```bash
# 1. 检查 Python 版本
python --version  # 必须 >= 3.10

# 2. 安装 uv（如果未安装）
curl -LsSf https://astral.sh/uv/install.sh | sh

# 3. 克隆仓库
git clone <repository-url>
cd skill-creator-mcp

# 4. 创建虚拟环境并安装依赖
uv sync --dev

# 5. 激活 pre-commit hooks
uv run pre-commit install

# 6. 验证安装
uv run pytest --version
uv run ruff --version
uv run mypy --version

# 7. 运行测试确认环境正常
uv run pytest
```

**环境验证脚本**（可保存为 `scripts/check-env.sh`）：
```bash
#!/bin/bash
set -e

echo "检查开发环境..."

# Python 版本
PYTHON_VERSION=$(python --version | awk '{print $2}')
echo "Python 版本: $PYTHON_VERSION"

# uv
echo "uv 版本: $(uv --version)"

# 依赖检查
echo "运行测试..."
uv run pytest -q

# 代码规范检查
echo "代码规范检查..."
uv run ruff check .

# 类型检查
echo "类型检查..."
uv run mypy src/

echo "环境检查完成！"
```

### 2.5 开发流程控制机制

**阶段门禁**：每个开发阶段必须通过验收标准才能进入下一阶段。

```mermaid
graph LR
    A[阶段1: 框架搭建] -->|验收通过| B[阶段2: Tools开发]
    B -->|验收通过| C[阶段3: Resources开发]
    C -->|验收通过| D[阶段4: Prompts开发]
    D -->|验收通过| E[阶段5: Agent-Skill开发]
    E -->|验收通过| F[阶段6: 测试优化]
    F -->|验收通过| G[阶段7: 文档示例]
    G -->|验收通过| H[项目交付]
```

**每日开发检查**：
```bash
# 每日开发前
git checkout develop
git pull origin develop

# 每日开发结束后
git add .
git commit -m "wip: daily progress"
git push origin feature/current-feature

# 运行完整测试套件
uv run pytest --cov

# 运行代码检查
uv run ruff check .
uv run mypy src/
```

**发布前检查清单**：
```bash
#!/bin/bash
# scripts/pre-release-check.sh

echo "发布前检查..."

# 1. 所有测试通过
echo "运行测试套件..."
uv run pytest

# 2. 代码覆盖率检查
echo "检查测试覆盖率..."
COVERAGE=$(uv run pytest --cov --cov-report=term-missing | grep TOTAL | awk '{print $4}' | sed 's/%//')
if (( $(echo "$COVERAGE < 80" | bc -l) )); then
    echo "错误：测试覆盖率 $COVERAGE% 低于 80%"
    exit 1
fi

# 3. 代码规范检查
echo "代码规范检查..."
uv run ruff check .

# 4. 类型检查
echo "类型检查..."
uv run mypy src/

# 5. 文档生成
echo "生成文档..."
uv run mkdocs build

# 6. 打包测试
echo "测试打包..."
uv build

echo "发布前检查完成！"
```

### 2.6 质量保证机制

**自动化 CI/CD 流水线**：
```yaml
# .github/workflows/quality-gate.yml
name: Quality Gate

on:
  pull_request:
    branches: [develop, main]

jobs:
  quality-check:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Install uv
        run: curl -LsSf https://astral.sh/uv/install.sh | sh

      - name: Install dependencies
        run: uv sync --dev

      - name: Run tests
        run: uv run pytest --cov

      - name: Check coverage
        run: |
          COVERAGE=$(uv run pytest --cov --cov-report=term-missing | grep TOTAL | awk '{print $4}' | sed 's/%//')
          if (( $(echo "$COVERAGE < 80" | bc -l) )); then
            echo "Coverage $COVERAGE% is below 80%"
            exit 1
          fi

      - name: Lint check
        run: uv run ruff check .

      - name: Type check
        run: uv run mypy src/

      - name: Security check
        run: uv run bandit -r src/
```

**质量标准**：
| 指标 | 标准 | 检查方式 |
|------|------|----------|
| 测试覆盖率 | ≥ 80% | pytest --cov |
| 代码规范 | 无警告 | ruff check |
| 类型检查 | 无错误 | mypy src/ |
| 安全漏洞 | 无高危 | bandit -r src/ |
| 文档覆盖率 | 100% | interrogate |

---

## 三、技术规格

### 3.1 MCP Server 技术栈

**核心框架**：FastMCP SDK（Python）

**传输协议支持**：
- **STDIO**：本地开发，最佳性能
- **SSE (HTTP)**：远程部署，支持标准认证

**关键依赖**：
```toml
[project]
name = "skill-creator-mcp"
version = "0.1.0"
requires-python = ">=3.10"
dependencies = [
    "fastmcp>=0.11.0",
    "pydantic>=2.0.0",
    "aiohttp>=3.9.0",
    "aiofiles>=23.0.0",
]
```

### 3.2 MCP Server 目录结构

```
skill-creator-mcp/
├── pyproject.toml
├── README.md
├── .gitignore
├── LICENSE
├── src/skill_creator_mcp/
│   ├── __init__.py
│   ├── __main__.py
│   ├── server.py
│   ├── tools/
│   ├── resources/
│   ├── prompts/
│   ├── models/
│   ├── templates/
│   └── utils/
├── tests/
├── examples/
└── docs/
```

---

## 四、开发阶段规划

| 阶段 | 内容 | 工作量 | 验收标准 |
|------|------|--------|----------|
| **阶段 1** | MCP Server 框架搭建 | 2-3天 | 服务器启动、MCP Inspector 连接 |
| **阶段 2** | MCP Tools 开发 | 5-7天 | 所有工具可用、测试覆盖率>80% |
| **阶段 3** | MCP Resources 开发 | 2-3天 | 所有资源可访问 |
| **阶段 4** | MCP Prompts 开发 | 2-3天 | 所有提示可调用 |
| **阶段 5** | Agent-Skill 开发 | 2-3天 | SKILL.md ≤150行、自验证通过 |
| **阶段 6** | 测试和优化 | 3-4天 | 所有测试通过、响应<1s |
| **阶段 7** | 文档和示例 | 2-3天 | 文档完整、示例可运行 |

---

## 五、验证标准

### 5.1 MCP Server 验证标准

| 检查项 | 标准 | 优先级 |
|--------|------|--------|
| 服务器启动 | STDIO 和 SSE 都能正常启动 | 必须 |
| 工具注册 | 所有工具可被发现和调用 | 必须 |
| 资源注册 | 所有资源可被发现和读取 | 必须 |
| 提示注册 | 所有提示可被发现和调用 | 必须 |
| 测试覆盖 | 单元测试覆盖率 > 80% | 必须 |

### 5.2 Agent-Skill 验证标准

| 检查项 | 标准 | 优先级 |
|--------|------|--------|
| SKILL.md 行数 | ≤150行 | 必须 |
| 描述完整性 | 功能+场景+触发词 | 必须 |
| MCP 集成 | 正确引用 MCP 工具 | 必须 |
| 自洽性 | 自身符合最佳实践 | 必须 |

---

## 六、关键文件清单

### MCP Server 文件

| 文件 | 优先级 | 预估行数 |
|------|--------|---------|
| `src/skill_creator_mcp/server.py` | P0 | ~100 |
| `src/skill_creator_mcp/tools/init_skill.py` | P0 | ~200 |
| `src/skill_creator_mcp/tools/validate_skill.py` | P0 | ~250 |
| `src/skill_creator_mcp/tools/analyze_skill.py` | P1 | ~300 |
| `src/skill_creator_mcp/tools/refactor_skill.py` | P2 | ~250 |
| `src/skill_creator_mcp/tools/package_skill.py` | P2 | ~150 |
| `tests/test_*.py` | P1 | ~800 |

### Agent-Skill 文件

| 文件 | 优先级 | 预估行数 |
|------|--------|---------|
| `SKILL.md` | P0 | ≤150 |
| `references/mcp-integration.md` | P0 | ~200 |
| `references/best-practices.md` | P1 | ~280 |
| `references/validation.md` | P1 | ~300 |

---

## 七、部署配置

### 7.1 Claude Code 配置

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

---

## 八、参考资源

**FastMCP**：
- [FastMCP GitHub](https://github.com/jlowin/fastmcp)
- [FastMCP 文档](https://gofastmcp.com)

**MCP 官方**：
- [MCP Python SDK](https://github.com/modelcontextprotocol/python-sdk)

**本地参考**：
- DeepSkills 项目：`/models/claude-glm/DeepSkills/`
- MCP 边界文档：`/models/claude-glm/claude-code-docs/MCP-AgentSkills使用与开发边界.md`

---

## 九、项目交付清单

### 9.1 代码交付

- [ ] MCP Server 源代码（`src/skill_creator_mcp/`）
- [ ] 单元测试（`tests/`）
- [ ] 配置文件（`pyproject.toml`, `.gitignore`）

### 9.2 文档交付

- [ ] README.md
- [ ] API 文档
- [ ] 架构文档
- [ ] 部署指南

### 9.3 示例交付

- [ ] 基本使用示例
- [ ] 高级用法示例
- [ ] 集成测试示例

### 9.4 Agent-Skill 交付

- [ ] SKILL.md（≤150行）
- [ ] 引用文档（references/）
- [ ] 使用示例（examples/）

---

## 附录 A：完整 pyproject.toml

```toml
[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[project]
name = "skill-creator-mcp"
version = "0.1.0"
description = "Agent-Skills 开发与质量保证 MCP Server"
readme = "README.md"
requires-python = ">=3.10"
license = { text = "MIT" }
dependencies = [
    "fastmcp>=0.11.0",
    "pydantic>=2.0.0",
    "aiohttp>=3.9.0",
    "aiofiles>=23.0.0",
]

[project.optional-dependencies]
dev = [
    "pytest>=7.0.0",
    "pytest-asyncio>=0.21.0",
    "pytest-cov>=4.0.0",
    "ruff>=0.1.0",
    "mypy>=1.0.0",
]

[tool.ruff]
line-length = 100
target-version = "py310"

[tool.mypy]
python_version = "3.10"
disallow_untyped_defs = true

[tool.pytest.ini_options]
asyncio_mode = "auto"
testpaths = ["tests"]
```

---

## 附录 B：验收测试脚本

```bash
#!/bin/bash
# scripts/acceptance-test.sh

echo "运行验收测试..."

# 1. 环境检查
echo "检查 Python 版本..."
python --version

# 2. 依赖检查
echo "检查依赖安装..."
uv run pip list

# 3. 服务器启动测试
echo "测试服务器启动..."
timeout 5 uv run python -m skill_creator_mcp || true

# 4. 测试套件
echo "运行测试套件..."
uv run pytest -v

# 5. 代码规范
echo "代码规范检查..."
uv run ruff check .

# 6. 类型检查
echo "类型检查..."
uv run mypy src/

echo "验收测试完成！"
```

---

**计划制定完成日期**：2026-01-20
**预计项目开始日期**：待定
**预计项目完成日期**：开始后 3-4 周
