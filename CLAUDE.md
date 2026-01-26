# Skills-Creator 开发指南

> **文档版本**: v1.3
> **更新日期**: 2026-01-26
> **适用范围**: Skills-Creator 项目开发
> **主要变更**: 文档结构优化（10章→6章），内容精简~35%

本文档为 Claude AI 提供项目开发规范和工作流程指南，确保代码质量和开发效率。

---

## 一、项目概述

### 1.1 项目定位

**Skills-Creator** 是一个基于 **MCP Server + Agent-Skill 混合架构**的完整解决方案，用于开发、验证和优化 Agent-Skills。

- **当前版本**: v0.2.1-alpha
- **开发环境**: conda base Python 环境
- **测试覆盖率**: 94-95% (414个测试用例)
- **技术栈**: FastMCP SDK + Pydantic 2.0+ + pytest

### 1.2 技术架构

```
┌─────────────────────────────────────────┐
│         Claude Code / Desktop           │
│                                         │
│  ┌───────────────────────────────────┐  │
│  │   skill-creator (Agent-Skill)     │  │
│  │   - 工作流编排                     │  │
│  │   - 渐进式披露                     │  │
│  │   - 最佳实践                       │  │
│  └──────────────┬────────────────────┘  │
│                 │                         │
│  ┌──────────────▼────────────────────┐  │
│  │  MCP Server (skill-creator-mcp)   │  │
│  │  - 16 Tools (5类)                  │  │
│  │  - 4 Resources (只读数据)          │  │
│  │  - 3 Prompts (可重用模板)          │  │
│  └───────────────────────────────────┘  │
└─────────────────────────────────────────┘
```

### 1.3 目录结构

```
/models/claude-glm/Skills-Creator/
├── skill-creator/              # Agent-Skill 代码统一目录
│   ├── SKILL.md                # Agent-Skill 入口
│   ├── examples/               # 使用示例
│   ├── scripts/                # 辅助脚本
│   └── references/             # 引用文档
├── skill-creator-mcp/          # MCP Server (Python)
│   ├── src/skill_creator_mcp/
│   │   ├── server.py           # MCP Server 入口
│   │   ├── models/             # Pydantic 数据模型
│   │   ├── utils/              # 工具函数
│   │   ├── prompts/            # Prompt 模板
│   │   └── resources/          # 资源内容
│   ├── tests/                  # 测试套件 (99% 覆盖率)
│   ├── pyproject.toml          # 项目配置
│   └── README.md
├── docs/                       # 项目文档
│   └── adr/
│       └── 001-hybrid-architecture.md
├── ARCHITECTURE_AUDIT_REPORT_v2.md
├── ROADMAP.md
├── ISSUES.md
├── CHANGELOG.md
├── .claude/
│   └── plans/                  # 开发计划
└── .github/
    ├── workflows/
    │   └── code-review.yml     # CI/CD 流程
    ├── pull_request_template.md
    └── ISSUE_TEMPLATE/
```

### 1.4 核心设计原则

1. **渐进式披露**: YAML Frontmatter → SKILL.md → 引用文件
2. **职责分离**: MCP 提供原子操作，Agent-Skill 编排工作流
3. **Token 优化**: SKILL.md ≤150行，引用文件 200-300行
4. **按能力组织**: 功能分组而非工具堆砌

---

## 二、开发流程九步法

> **重要**: 严格按照以下九步法执行开发工作，确保代码质量和项目进度可控。

### 2.1 流程总览

```
步骤0: 前置任务审核  → 检查前置任务、确认Git环境
步骤1: 制定开发计划  → .claude/plans/feat-xxx.md
步骤2: 拆分任务清单  → TodoWrite 工具 (3-10个任务)
步骤3: 执行开发工作  → 编码 + 测试
步骤4: 测试验证      → pytest --cov
步骤5: 交叉验证      → 对照计划检查 (支持回退)
步骤6: 更新文档      → CHANGELOG.md
步骤7: 阶段性审计    → 内部审查
步骤8: Git提交       → 版本控制
步骤9: 阶段性汇报    → 生成汇报并归档计划
```

### 2.2 各步骤检查清单

| 步骤 | 目的 | 检查项 | 输出 |
|------|------|--------|------|
| **0** | 前置任务审核 | • 前一阶段计划已完成<br>• 文档已归档到 archive/<br>• 当前分支正确<br>• 代码已同步 | 审核报告 |
| **1** | 制定开发计划 | • 在 plans/ 创建计划文档<br>• 明确目标、范围、交付物<br>• 列出技术依赖和风险<br>• 定义验收标准 | 计划文档 |
| **2** | 拆分任务清单 | • 使用 TodoWrite 创建任务<br>• 标注优先级 (P0-P3)<br>• **限制3-10个任务**<br>• 使用稳定ID (YYYYMMDD-序号) | 任务清单 |
| **3** | 执行开发工作 | • 按优先级顺序执行<br>• 每完成一项更新状态<br>• 遇到阻塞及时记录<br>• 保持代码提交原子性 | 可运行代码 |
| **4** | 测试验证 | • 编写/更新测试用例<br>• 运行 pytest --cov<br>• 确保覆盖率≥99%<br>• 运行 ruff, mypy 检查 | 测试报告 |
| **5** | 交叉验证 | • 对照计划检查完成度<br>• 验证所有验收标准<br>• **检查TODO状态一致性**<br>• 发现问题可回退状态 | 验证报告 |
| **6** | 更新文档 | • 更新技术文档<br>• 更新 CHANGELOG.md<br>• 更新任务追踪文档<br>• 检查交叉引用链接 | 更新的文档 |
| **7** | 阶段性审计 | • 审查是否100%按计划执行<br>• 记录偏差和改进措施<br>• 确认代码质量检查通过<br>• 准备Git提交信息 | 审计报告 |
| **8** | Git提交 | • 代码通过所有测试<br>• 代码通过质量检查<br>• 文档已同步更新<br>• 使用规范的commit信息 | Git提交记录 |
| **9** | 阶段性汇报 | • 汇总已完成任务<br>• 记录问题和解决方案<br>• 记录测试和质量指标<br>• **归档计划到 archive/** | 汇报文档 |

### 2.3 TODO管理规范

**任务状态管理**:
- `pending`: 待执行
- `in_progress`: 执行中（同时只能有一个）
- `completed`: 已完成

**状态流转**:
```
pending → in_progress → completed
  ↑                           ↓
  └──── 未完成/不规范 ────────┘
        (回退到 pending 或 in_progress)
```

**实时更新原则**:
- 每完成一步立即更新状态
- 遇到阻塞及时记录
- 定期回顾进度
- 发现问题及时回退状态

### 2.4 流程违规处理

| 违规步骤 | 违规行为 | 后果 | 恢复措施 |
|----------|----------|------|----------|
| 步骤0 | 未检查前置任务 | 基础不牢固 | 返回步骤0，完成审核 |
| 步骤2 | TODO超过10个 | 执行准确性下降 | 拆分为多个小计划 |
| 步骤3 | 未实时更新TODO | 进度不透明 | 补充更新TODO状态 |
| 步骤4 | 跳过测试 | 质量风险 | 补全测试，确保通过 |
| 步骤5 | 未执行交叉验证 | 遗漏问题 | 执行完整交叉验证 |
| 步骤5 | 发现问题未回退 | 质量缺陷 | 使用TODO回退机制 |
| 步骤6 | 文档未同步 | 技术债务 | 补充文档更新 |
| 步骤7 | 未通过审计 | 进度偏差 | 修正偏差后重新审计 |
| 步骤8 | 提交不规范 | 版本混乱 | 修正提交信息 |
| 步骤9 | 未归档计划 | 计划丢失 | 归档到正确位置 |

---

## 三、Git规范与禁止行为

### 3.1 Git分支管理

**当前分支策略**:
```
main (生产分支)
  │
develop (开发分支)
  │
  └─ feature/* (功能分支)
```

**分支命名规范**:

| 前缀 | 用途 | 示例 |
|------|------|------|
| `feature/` | 新功能开发 | `feature/add-validate-tool` |
| `fix/` | Bug 修复 | `fix/naming-validation` |
| `hotfix/` | 生产环境紧急修复 | `hotfix/critical-crash` |
| `refactor/` | 代码重构 | `refactor/async-io` |
| `docs/` | 文档更新 | `docs/update-readme` |
| `test/` | 测试相关 | `test/add-coverage` |

**分支操作规范**:
```bash
# 创建功能分支
git checkout develop
git pull origin develop
git checkout -b feature/your-feature-name
git push -u origin feature/your-feature-name

# 分支合并流程（通过PR）
# 1. 推送到远程
# 2. 创建 Pull Request 到 develop
# 3. Code Review 通过后 Squash and Merge
# 4. 删除功能分支
```

**禁止操作**:
- ❌ 直接在 main 分支提交代码
- ❌ 推送未经测试的代码
- ❌ 强制推送到公共分支
- ❌ 合并有冲突的 PR 未解决

### 3.2 Commit规范

**Commit信息格式**:
```
<type>(<scope>): <subject>

<body>

<footer>
```

**Type类型**:

| Type | 说明 | 示例 |
|------|------|------|
| `feat` | 新功能 | 添加新工具、新功能 |
| `fix` | Bug 修复 | 修复错误、异常处理 |
| `docs` | 文档更新 | 更新 README、注释 |
| `style` | 代码格式 | 代码风格调整（不影响功能） |
| `refactor` | 重构 | 代码重构（不改变功能） |
| `test` | 测试相关 | 添加测试、修复测试 |
| `chore` | 构建过程或辅助工具变动 | 依赖更新、配置修改 |

**提交示例**:
```
feat(工具): 添加批量验证功能

实现批量验证多个Agent-Skill的功能。
- 支持并发控制，默认最多5个并发
- 使用Progress bar显示进度
- 返回详细的验证结果报告

测试: 新增8个测试用例，覆盖率95%

Closes #123
```

### 3.3 高危操作禁止

| 禁止行为 | 后果 | 替代方案 |
|----------|------|----------|
| 虚假审核 | 代码被拒绝 | 真实执行 Code Review |
| 跨流程开发 | 工作混乱 | 严格按九步法执行 |
| 绕过测试直接提交 | 质量风险 | 必须通过全部测试 |
| 直接修改 main 分支 | 破坏稳定性 | 使用功能分支 + PR |
| 危险命令执行 | 系统崩溃 | 使用安全替代方案 |

**危险命令（严格禁止）**:
```bash
# ❌ 根目录递归删除（系统崩溃）
rm -rf /

# ❌ 递归删除重要目录
rm -rf ~/important-data
rm -rf /models/claude-glm/Skills-Creator

# ❌ 磁盘覆盖（数据丢失）
dd if=/dev/zero of=/dev/sda

# ❌ Fork 炸弹（系统崩溃）
:(){ :|:& };:
```

**安全替代方案**:
- 使用 `rm -r` 代替 `rm -rf`（递归但无强制）
- 删除前先用 `ls` 确认目录内容
- 使用 `--interactive` 或 `-i` 参数

### 3.4 开发行为规范

**禁止行为**:
- ❌ **盲目创建文档/目录**: 优先查看目录文档情况
- ❌ **未经规划的新增文件**: 必须在计划中说明
- ❌ **绕过 Code Review**: 所有代码必须经过审查
- ❌ **破坏性重构**: 必须保持向后兼容或提供迁移指南
- ❌ **硬编码敏感信息**: 使用环境变量或配置文件

**敏感信息保护**:
- ❌ 提交 API Key、密码、Token
- ✅ 使用环境变量存储敏感信息
- ✅ 添加 `.env` 到 `.gitignore`

---

## 四、文档与计划管理

### 4.1 文档更新规范

**条理清晰的迭代式更新**:
```
第一批更新（必需章节）: 项目概述、快速开始、核心功能
第二批更新（详细说明）: API 文档、配置说明、故障排除
第三批更新（补充内容）: 高级用法、最佳实践、FAQ
```

**推进项目进度追踪**:
- 每个文档更新都服务于项目目标
- 更新前确认目标达成
- 更新后验证目标完成

**文档一致性检查**:
```bash
# 检查交叉引用链接
grep -r "\[.*\](references/)" . --include="*.md"

# 检查过时引用
grep -r "v0.0.1" . --include="*.md"
```

### 4.2 计划文档管理

**目录结构**:
```
.claude/plans/
├── README.md              # 计划说明
├── archive/               # 已完成的历史计划
├── feat-功能名称.md        # 功能计划
├── fix-问题描述.md         # 修复计划
└── refactor-模块.md        # 重构计划
```

**命名规范**:

| 类型 | 命名格式 | 示例 |
|------|----------|------|
| 功能计划 | `feat-{功能}.md` | `feat-validate-tool.md` |
| 修复计划 | `fix-{问题}.md` | `fix-naming-validation.md` |
| 重构计划 | `refactor-{模块}.md` | `refactor-async-io.md` |
| 阶段报告 | `phase-report-YYYY-MM-DD-{描述}.md` | `phase-report-2026-01-26-v0.3.0.md` |

**计划状态流转**:
```
planning → in_progress → completed → archived
    ↑                                    ↓
    └────────────── reopened ←──────────┘
```

**状态说明**:
- `planning`: 规划中
- `in_progress`: 执行中
- `completed`: 已完成
- `archived`: 已归档

### 4.3 文档放置规则

| 文档类型 | 放置位置 | 说明 |
|----------|----------|------|
| Agent-Skill 相关 | `skill-creator/` | Agent-Skill 代码 |
| Agent-Skill 引用文档 | `skill-creator/references/` | 详细技术文档 |
| Agent-Skill 用户示例 | `skill-creator/examples/` | 使用示例 |
| Agent-Skill 脚本 | `skill-creator/scripts/` | 辅助脚本 |
| 开发计划 | `.claude/plans/` | 开发计划文档 |
| 项目文档 | 根目录 | README, CHANGELOG 等 |
| 代码内文档 | 代码目录 | 模块文档 |

---

## 五、项目架构与常用命令

### 5.1 混合架构设计

**MCP Server 职责**:
- 提供可执行的原子操作
- 处理文件 I/O 和数据验证
- 返回结构化结果

**Agent-Skill 职责**:
- 编排工作流程
- 传递知识和最佳实践
- 提供渐进式披露的内容

**边界原则**:
- MCP 不包含工作流逻辑
- Agent-Skill 不执行 I/O 操作
- 接口定义一致清晰

### 5.2 开发环境设置

```bash
# 默认使用 conda base Python 环境
conda activate base

# 进入项目目录
cd /models/claude-glm/Skills-Creator

# 进入 MCP Server 目录
cd skill-creator-mcp

# 安装依赖（推荐使用 uv）
uv sync --dev
```

### 5.3 测试与质量检查

```bash
# 运行完整测试套件
uv run pytest --cov

# 运行特定测试
uv run pytest tests/test_tools/

# 查看测试覆盖率报告
uv run pytest --cov --cov-report=html
open htmlcov/index.html

# 代码质量检查
uv run ruff check .        # 必须 0 错误
uv run ruff format .       # 格式化代码
uv run mypy src/           # 必须 0 错误
uv run bandit -r src/      # 安全检查

# 组合检查（全部通过）
uv run ruff check . && uv run mypy src/ && uv run pytest
```

### 5.4 Git操作命令

```bash
# 查看当前分支
git branch

# 查看状态
git status
git diff

# 查看提交历史
git log --oneline -10

# 创建新分支
git checkout develop
git pull origin develop
git checkout -b feature/your-feature-name

# 提交变更
git add .
git commit -m "feat(scope): description"
git push -u origin feature/your-feature-name

# 合并到 main (通过 PR)
# 1. 在 GitHub 创建 Pull Request
# 2. Code Review
# 3. Squash and Merge
```

### 5.5 启动服务器

```bash
# STDIO 模式（默认）
uv run python -m skill_creator_mcp

# HTTP/SSE 模式
uv run python -m skill_creator_mcp.http
# 访问: http://localhost:8000
```

---

## 六、快速参考

### 6.1 开发流程速查

```
0. 前置审核 → 检查前置任务、确认Git环境
1. 制定计划 → .claude/plans/feat-xxx.md
2. 拆分任务 → TodoWrite 工具 (3-10个任务)
3. 执行开发 → 编码 + 测试
4. 测试验证 → pytest --cov
5. 交叉验证 → 对照计划检查 (支持回退)
6. 更新文档 → CHANGELOG.md
7. 阶段审计 → 内部审查
8. Git提交 → 版本控制
9. 阶段汇报 → 生成汇报并归档计划
```

### 6.2 常用命令速查表

| 类别 | 命令 | 说明 |
|------|------|------|
| **开发环境** | `cd skill-creator-mcp && uv sync --dev` | 安装依赖 |
| **测试** | `uv run pytest --cov` | 运行测试套件 |
| **代码检查** | `uv run ruff check . && uv run mypy src/` | 质量检查 |
| **启动服务器** | `uv run python -m skill_creator_mcp` | STDIO模式 |
| **创建分支** | `git checkout -b feature/xxx` | 新功能分支 |
| **提交变更** | `git commit -m "feat(scope): desc"` | 提交代码 |
| **推送远程** | `git push -u origin feature/xxx` | 推送到远程 |

### 6.3 优先级定义

| 优先级 | 说明 | 响应时间 |
|--------|------|----------|
| P0 | 阻塞性问题 | 立即 |
| P1 | 高优先级 | 本周内 |
| P2 | 中优先级 | 本月内 |
| P3 | 低优先级 | 有时间时 |

### 6.4 文件大小限制

| 文件类型 | 推荐大小 | 最大大小 |
|----------|----------|----------|
| SKILL.md | ≤150行 | ≤500行 |
| 引用文件 | 200-300行 | ≤400行 |
| 函数长度 | ≤50行 | ≤100行 |
| 类长度 | ≤300行 | ≤500行 |

### 6.5 质量标准

| 指标 | 要求 | 目标 |
|------|------|------|
| 测试覆盖率 | ≥80% | ≥95% |
| 代码检查 | 0 错误 | 0 警告 |
| 类型检查 | 0 错误 | 完整注解 |
| 安全检查 | 0 高危 | 0 中危 |

### 6.6 相关文档链接

**核心文档**:

| 文档 | 路径 | 说明 |
|------|------|------|
| Agent-Skill 入口 | `skill-creator/SKILL.md` | 技能概览和快速开始 |
| MCP Server README | `skill-creator-mcp/README.md` | MCP Server 使用说明 |
| 架构审计报告 | `ARCHITECTURE_AUDIT_REPORT_v2.md` | 完整架构审计结果 |
| 问题清单 | `ISSUES.md` | 已知问题和改进计划 |
| 路线图 | `ROADMAP.md` | 项目发展规划 |
| 变更日志 | `CHANGELOG.md` | 版本变更记录 |

**引用文档**:

| 文档 | 路径 | 说明 |
|------|------|------|
| MCP 集成指南 | `skill-creator/references/mcp-integration.md` | MCP 工具使用和资源访问 |
| 最佳实践 - 核心 | `skill-creator/references/best-practices-core.md` | 基础架构和规范 |
| 最佳实践 - 高级 | `skill-creator/references/best-practices-advanced.md` | 高级技巧和优化 |
| 验证规范 | `skill-creator/references/validation.md` | 命名、结构、内容验证规则 |

**外部参考**:

| 资源 | 链接 | 说明 |
|------|------|------|
| FastMCP 文档 | https://jlowin.github.io/fastmcp/ | FastMCP SDK 官方文档 |
| MCP 规范 | https://modelcontextprotocol.io/ | Model Context Protocol 规范 |
| Pydantic 文档 | https://docs.pydantic.dev/ | Pydantic 2.0 官方文档 |

### 6.7 常见问题

| 问题 | 解决方案 |
|------|----------|
| 如何创建新的 MCP 工具？ | 参考现有工具实现，在 `server.py` 中使用 `@mcp.tool()` 装饰器 |
| 如何添加新的资源？ | 在 `server.py` 中使用 `@mcp.resource()` 装饰器定义资源 |
| 测试失败怎么办？ | 查看测试报告，定位失败原因，修复代码或更新测试 |
| 如何更新文档？ | 确保文档与代码同步，更新 CHANGELOG.md |

---

**文档维护**: 请在每次重大变更后更新本文档。
**最后更新**: 2026-01-26 (v1.3 - 文档结构优化)
