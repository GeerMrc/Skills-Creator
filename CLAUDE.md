# Skills-Creator 开发指南

> **文档版本**: v1.0
> **更新日期**: 2026-01-21
> **适用范围**: Skills-Creator 项目开发

本文档为 Claude AI 提供项目开发规范和工作流程指南，确保代码质量和开发效率。

---

## 一、项目概述

### 1.1 项目定位

**Skills-Creator** 是一个基于 **MCP Server + Agent-Skill 混合架构**的完整解决方案，用于开发、验证和优化 Agent-Skills。

- **当前版本**: v0.1.0-alpha
- **开发环境**: conda base Python 环境
- **测试覆盖率**: 96% (262个测试用例)
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
│  │  - 5 Tools (原子操作)              │  │
│  │  - 3 Resources (只读数据)          │  │
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

## 二、规范的开发流程要求

> **重要**: 严格按照以下七步法执行开发工作，确保代码质量和项目进度可控。

### 2.1 开发流程七步法

```
┌─────────────────────────────────────────────────────────────────┐
│                        完整开发流程                              │
├─────────────────────────────────────────────────────────────────┤
│  步骤1: 制定开发计划 → 步骤2: 拆分任务清单 → 步骤3: 执行开发工作  │
│       ↓                                                          │
│  步骤4: 测试验证 → 步骤5: 交叉验证 → 步骤6: 更新文档 → 步骤7: 审计 │
└─────────────────────────────────────────────────────────────────┘
```

### 步骤 1: 制定开发计划

**目的**: 明确工作目标、范围和验收标准

**检查清单**:
- [ ] 在 `.claude/plans/` 创建或选择现有计划文档
- [ ] 明确计划目标、范围、交付物
- [ ] 列出技术依赖和风险评估
- [ ] 定义验收标准

**计划文档模板**:
```markdown
# 功能名称开发计划

## 目标
描述要实现的功能目标

## 范围
- 包含内容
- 不包含内容

## 技术依赖
- 依赖组件1
- 依赖组件2

## 验收标准
- [ ] 功能正常工作
- [ ] 测试通过
- [ ] 文档更新

## 风险评估
| 风险 | 影响 | 缓解措施 |
|------|------|----------|
```

**输出**: `.claude/plans/feat-功能名称.md`

### 步骤 2: 拆分任务清单

**目的**: 将计划分解为可执行的任务项

**检查清单**:
- [ ] 使用 TodoWrite 工具创建任务清单
- [ ] 标注任务优先级（P0/P1/P2/P3）
- [ ] 估算每个任务的工作量
- [ ] 识别任务依赖关系

**优先级定义**:
- **P0**: 阻塞性问题，必须立即解决
- **P1**: 高优先级，本周内完成
- **P2**: 中优先级，本月内完成
- **P3**: 低优先级，有时间时处理

**输出**: TodoWrite 任务清单

### 步骤 3: 执行开发工作

**目的**: 按照任务清单逐项执行开发

**检查清单**:
- [ ] 按照优先级顺序执行任务
- [ ] 每完成一项立即更新 TodoWrite 状态
- [ ] 遇到阻塞问题及时记录并寻求帮助
- [ ] 保持代码提交的原子性

**开发原则**:
- **小步快跑**: 每次提交一个完整的变更
- **持续测试**: 每个功能完成后立即测试
- **文档同步**: 代码变更时同步更新文档

**输出**: 可运行的代码 + Git 提交

### 步骤 4: 测试验证

**目的**: 确保代码质量和功能正确性

**检查清单**:
- [ ] 编写或更新测试用例
- [ ] 运行完整测试套件 (`uv run pytest --cov`)
- [ ] 确保测试覆盖率不降低（当前 96%）
- [ ] 运行代码质量检查 (`ruff`, `mypy`)
- [ ] 记录测试结果

**质量标准**:
```bash
# 测试覆盖率要求
pytest --cov           # 必须 ≥80%, 目标 ≥95%

# 代码规范检查
uv run ruff check .    # 必须 0 错误
uv run mypy src/       # 必须 0 错误

# 安全检查
uv run bandit -r src/  # 0 高危问题
```

**输出**: 测试报告

### 步骤 5: 交叉验证

**目的**: 对照原始开发计划检查完成度

**检查清单**:
- [ ] 对照原始开发计划检查完成度
- [ ] 验证所有验收标准是否满足
- [ ] 确认无遗漏的边界情况
- [ ] 进行代码自审或同行评审
- [ ] 确认无性能回归

**验证方法**:
- 功能测试: 手动验证所有功能点
- 边界测试: 测试异常输入和边界条件
- 性能测试: 对比基准性能
- 安全测试: 检查常见安全问题

**输出**: 验证报告

### 步骤 6: 更新文档

**目的**: 保持文档与代码同步

**检查清单**:
- [ ] 更新相关技术文档
- [ ] 更新 CHANGELOG.md
- [ ] 更新任务追踪文档
- [ ] 标记计划状态
- [ ] 检查交叉引用链接

**文档更新原则**:
- **条理清晰**: 按逻辑顺序分批次更新
- **服务目标**: 每个更新都服务于项目目标
- **保持一致**: 确保跨文档引用准确
- **定期审计**: 每个版本发布前全面检查

**输出**: 更新的文档

### 步骤 7: 阶段性审计

**目的**: 审查执行情况并总结经验

**检查清单**:
- [ ] 审查是否 100% 按计划执行
- [ ] 记录偏差原因和改进措施
- [ ] 归档计划文档到 `.claude/plans/archive/`
- [ ] 生成阶段性工作汇报

### 2.2 阶段性工作汇报模板

**格式**:
```markdown
### 阶段性工作汇报

**计划工作内容**: [描述原计划要完成的工作]

**具体阶段性工作执行进度情况汇报**:
- 已完成任务:
  - [x] 任务1 - 完成情况描述
  - [x] 任务2 - 完成情况描述
- 进行中任务:
  - [ ] 任务3 - 当前进度
  - [ ] 任务4 - 预计完成时间
- 遇到的问题:
  - 问题描述1 - 解决方案
  - 问题描述2 - 解决方案
- 测试验证结果:
  - 测试覆盖率: XX%
  - 发现问题: XX 个
  - 已修复: XX 个

**下一阶段开发建议**:
- 建议的后续工作:
  1. 工作1
  2. 工作2
- 需要注意的事项:
  - 注意事项1
  - 注意事项2
```

### 2.3 流程违规处理

**违反规范的后果**:
- 未按流程开发 → 代码将被拒绝合并
- 跳过测试环节 → 要求补全测试
- 文档未同步 → 要求补充文档
- 计划未归档 → 要求补充归档

---

## 三、Git 分支管理规范

### 3.1 当前分支策略

```
main (生产分支)
  │
  └─ feature/* (功能分支)
      ├─ feature/init-skill-tool     [当前分支]
      ├─ feature/your-feature-name
      └── ...
```

**说明**: 项目当前使用简化的分支结构，直接从 main 创建功能分支。

### 3.2 分支命名规范

| 前缀 | 用途 | 示例 |
|------|------|------|
| `feature/` | 新功能开发 | `feature/add-validate-tool` |
| `fix/` | Bug 修复 | `fix/naming-validation` |
| `hotfix/` | 生产环境紧急修复 | `hotfix/critical-crash` |
| `refactor/` | 代码重构 | `refactor/async-io` |
| `docs/` | 文档更新 | `docs/update-readme` |
| `test/` | 测试相关 | `test/add-coverage` |

**命名原则**:
- 使用小写字母和连字符
- 简洁描述功能内容
- 避免使用数字

### 3.3 分支操作规范

**创建功能分支**:
```bash
# 1. 确保在最新 main 分支
git checkout main
git pull origin main

# 2. 创建新分支
git checkout -b feature/your-feature-name

# 3. 开始开发
# ... 开发工作 ...

# 4. 推送到远程
git push -u origin feature/your-feature-name
```

**分支合并流程**:
1. 开发完成后推送到远程
2. 创建 Pull Request 到 main
3. Code Review 通过后合并
4. 使用 **Squash and Merge** 保持提交历史整洁
5. 合并后删除功能分支

**禁止操作**:
- ❌ 直接在 main 分支提交代码
- ❌ 推送未经测试的代码
- ❌ 强制推送到公共分支
- ❌ 合并有冲突的 PR 未解决

### 3.4 Commit 规范

采用 **Conventional Commits** 格式，支持中英文。

**英文格式**（推荐，与国际项目一致）:
```
feat(tools): add init_skill tool implementation
fix(validators): handle edge case in skill name validation
docs(readme): update installation instructions
refactor(analyzers): optimize AST parsing performance
test(coverage): add tests for edge cases
chore(deps): update fastmcp to v0.12.0
```

**中文格式**（与计划文档一致）:
```
feat(工具): 添加 init_skill 工具实现
fix(验证器): 处理技能名称验证的边界情况
docs(文档): 更新安装说明
refactor(分析器): 优化 AST 解析性能
test(测试): 添加边界情况测试
chore(依赖): 更新 fastmcp 到 v0.12.0
```

**Type 类型**:
| Type | 说明 | 示例 |
|------|------|------|
| `feat` | 新功能 | 添加新工具、新功能 |
| `fix` | Bug 修复 | 修复错误、异常处理 |
| `docs` | 文档更新 | 更新 README、注释 |
| `style` | 代码格式 | 代码风格调整（不影响功能） |
| `refactor` | 重构 | 代码重构（不改变功能） |
| `test` | 测试相关 | 添加测试、修复测试 |
| `chore` | 构建过程或辅助工具变动 | 依赖更新、配置修改 |

**Commit 消息结构**:
```
<type>(<scope>): <subject>

<body>

<footer>
```

**示例**:
```
feat(tools): add package_skill tool

Implement packaging functionality for Agent-Skills.
Supports zip, tar.gz, and tar.bz2 formats.

Closes #123
```

**Commit 最佳实践**:
- 原子提交: 每次提交一个完整的变更
- 清晰描述: 让人理解为什么做这个变更
- 避免过大: 单个提交不超过 500 行变更
- 及时提交: 完成一个功能立即提交

---

## 四、禁止行为清单

> **严重警告**: 以下禁止行为违反将导致严重后果，请严格遵守。

### 4.1 高危操作（严格禁止）

| 禁止行为 | 后果 | 替代方案 |
|----------|------|----------|
| 虚假审核 | 代码被拒绝 | 真实执行 Code Review |
| 跨流程开发 | 工作混乱 | 严格按七步法执行 |
| 绕过测试直接提交 | 质量风险 | 必须通过全部测试 |
| 直接修改 main 分支 | 破坏稳定性 | 使用功能分支 + PR |
| 危险命令执行 | 系统崩溃 | 使用安全替代方案 |

### 4.2 命令执行安全规范

**安全操作（推荐）**:
```bash
# 查看目录内容
ls -la /path/to/directory

# 读取文件内容
cat file.txt

# 查看 git 状态
git status
git diff

# 删除单个文件
rm /path/to/specific/file

# 递归删除（需要 cd 到指定目录）
cd /safe/directory && rm -r subdirectory
```

**危险操作（严格禁止）**:
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

# ❌ 批量删除（危险）
mv * /dev/null
```

**安全替代方案**:
- 使用 `rm -r` 代替 `rm -rf`（递归但无强制）
- 删除前先用 `ls` 确认目录内容
- 使用 `--interactive` 或 `-i` 参数
- 考虑使用 `trash` 命令代替 `rm`

**删除前检查清单**:
```bash
# 1. 确认当前位置
pwd

# 2. 查看目录内容
ls -la

# 3. 确认要删除的内容
ls -la directory-to-delete/

# 4. 安全删除
rm -r directory-to-delete/
```

### 4.3 开发行为规范

**禁止行为**:
- ❌ **盲目创建文档/目录**: 优先查看目录文档情况
- ❌ **未经规划的新增文件**: 必须在计划中说明
- ❌ **绕过 Code Review**: 所有代码必须经过审查
- ❌ **破坏性重构**: 必须保持向后兼容或提供迁移指南
- ❌ **硬编码敏感信息**: 使用环境变量或配置文件

**正确做法**:
```bash
# 创建新文件前检查
ls -la /path/to/directory/
cat /path/to/directory/existing-file.md

# 在计划中说明新增文件
# .claude/plans/feat-new-function.md
## 新增文件
- `src/new_module.py` - 新功能模块
- `tests/test_new_module.py` - 测试文件
```

### 4.4 数据安全规范

**敏感信息保护**:
- ❌ 提交 API Key、密码、Token
- ✅ 使用环境变量存储敏感信息
- ✅ 添加 `.env` 到 `.gitignore`

**.gitignore 配置**:
```
# 环境变量
.env
.env.local

# Python
__pycache__/
*.pyc
.venv/

# IDE
.vscode/
.idea/
```

---

## 五、任务追踪和文档更新规范

### 5.1 任务追踪规范

**使用 TodoWrite 工具**:
```python
# 创建任务清单
TodoWrite(
    todos=[
        {
            "content": "实现 init_skill 工具",
            "status": "in_progress",
            "activeForm": "实现 init_skill 工具中"
        },
        {
            "content": "编写测试用例",
            "status": "pending",
            "activeForm": "编写测试用例"
        },
        {
            "content": "更新文档",
            "status": "pending",
            "activeForm": "更新文档"
        }
    ]
)
```

**任务状态管理**:
- `pending`: 待执行
- `in_progress`: 执行中（同时只能有一个）
- `completed`: 已完成

**实时更新原则**:
- 每完成一步立即更新状态
- 遇到阻塞及时记录
- 定期回顾进度

### 5.2 项目目录管理规范

**禁止盲目创建文档**:
```bash
# 创建新文档前检查
# 1. 查看目录结构
ls -la /models/claude-glm/Skills-Creator/

# 2. 检查是否存在类似文档
cat /models/claude-glm/Skills-Creator/EXISTING.md

# 3. 评估必要性
# - 是否真的需要新文档？
# - 能否更新现有文档？
# - 内容应该放在哪里？
```

**目录组织原则**:
```
/models/claude-glm/Skills-Creator/
├── skill-creator/              # Agent-Skill 代码
│   ├── SKILL.md                # Agent-Skill 入口
│   ├── examples/               # 使用示例
│   ├── scripts/                # 辅助脚本
│   └── references/             # 引用文档
├── skill-creator-mcp/          # MCP Server 代码
│   ├── src/                    # 源代码
│   ├── tests/                  # 测试代码
├── .claude/
│   └── plans/                  # 开发计划
├── .github/                    # GitHub 配置
└── [根目录文档]                 # 项目级文档
    ├── README.md
    ├── CHANGELOG.md
    ├── ROADMAP.md
    └── ARCHITECTURE_*.md
```

**文档放置规则**:
- Agent-Skill 相关 → `skill-creator/`
- Agent-Skill 引用文档 → `skill-creator/references/`
- Agent-Skill 用户示例 → `skill-creator/examples/`
- Agent-Skill 脚本 → `skill-creator/scripts/`
- 开发计划 → `.claude/plans/`
- 项目文档 → 根目录
- 代码内文档 → 代码目录

### 5.3 文档更新规范

**条理清晰的迭代式更新**:
```markdown
# 文档更新示例

## 第一批更新（必需章节）
1. 项目概述
2. 快速开始
3. 核心功能

## 第二批更新（详细说明）
1. API 文档
2. 配置说明
3. 故障排除

## 第三批更新（补充内容）
1. 高级用法
2. 最佳实践
3. FAQ
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

# 验证所有链接
# (需要手动验证或使用工具)
```

### 5.4 文档创建流程

**完整流程**:
```
1. 检查现有文档 (ls, cat)
   ↓
2. 评估必要性 (是否真的需要?)
   ↓
3. 规划内容结构 (章节大纲)
   ↓
4. 逐步填充内容 (分批次填写)
   ↓
5. 同步更新引用 (更新其他文档的链接)
   ↓
6. 验证一致性 (检查交叉引用)
```

**示例**:
```bash
# 1. 检查现有文档
ls skill-creator/references/
cat skill-creator/references/validation.md

# 2. 评估必要性
# 决定: 需要拆分为两个文件

# 3. 规划内容结构
# - validation-rules.md (规则说明)
# - validation-checklist.md (检查清单)

# 4. 逐步填充内容
# 先创建 validation-rules.md
# 再创建 validation-checklist.md

# 5. 同步更新引用
# 更新 SKILL.md 中的链接

# 6. 验证一致性
# 确保所有链接正确
```

---

## 六、项目架构概述

### 6.1 混合架构设计

**架构图**:
```
┌─────────────────────────────────────────────────────────────┐
│                     Claude Code / Desktop                    │
│                                                              │
│  ┌────────────────────────────────────────────────────────┐ │
│  │          Agent-Skill (skill-creator)                   │ │
│  │  ┌──────────────────────────────────────────────────┐  │ │
│  │  │ YAML Frontmatter (~100词)                        │  │ │
│  │  │ - name: skill-creator                            │  │ │
│  │  │ - description: 功能陈述 + 场景 + 触发词          │  │ │
│  │  ├──────────────────────────────────────────────────┤  │ │
│  │  │ SKILL.md (≤150行)                               │  │ │
│  │  │ - 技能概述、核心能力、快速开始                   │  │ │
│  │  │ - MCP 工具集成、资源访问                         │  │ │
│  │  │ - 详细文档链接                                   │  │ │
│  │  ├──────────────────────────────────────────────────┤  │ │
│  │  │ 引用文件 (200-300行)                             │  │ │
│  │  │ - mcp-integration.md                            │  │ │
│  │  │ - best-practices.md                             │  │ │
│  │  │ - validation.md                                 │  │ │
│  │  └──────────────────────────────────────────────────┘  │ │
│  └──────────────────────┬─────────────────────────────────┘ │
│                         │                                     │
│  ┌──────────────────────▼─────────────────────────────────┐ │
│  │         MCP Server (skill-creator-mcp)                 │ │
│  │  ┌──────────────────────────────────────────────────┐  │ │
│  │  │ Tools (5个原子操作)                               │  │ │
│  │  │ - init_skill: 初始化技能结构                     │  │ │
│  │  │ - validate_skill: 验证规范符合度                 │  │ │
│  │  │ - analyze_skill: 分析代码质量                    │  │ │
│  │  │ - refactor_skill: 生成重构建议                   │  │ │
│  │  │ - package_skill: 打包分发                        │  │ │
│  │  ├──────────────────────────────────────────────────┤  │ │
│  │  │ Resources (3个只读资源)                           │  │ │
│  │  │ - templates: 技能模板内容                        │  │ │
│  │  │ - best-practices: 最佳实践指南                   │  │ │
│  │  │ - validation-rules: 验证规则详情                 │  │ │
│  │  ├──────────────────────────────────────────────────┤  │ │
│  │  │ Prompts (3个可重用模板)                           │  │ │
│  │  │ - create-skill: 创建技能引导                     │  │ │
│  │  │ - validate-skill: 验证技能引导                   │  │ │
│  │  │ - refactor-skill: 重构技能引导                   │  │ │
│  │  └──────────────────────────────────────────────────┘  │ │
│  └─────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────┘
```

### 6.2 职责边界

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

### 6.3 核心组件

**MCP Tools** (技能操作):
```
init_skill    → 创建目录结构、生成模板文件
validate_skill → 检查命名、结构、内容规范
analyze_skill  → 分析复杂度、可维护性、代码质量
refactor_skill → 生成优先级排序的改进建议
package_skill  → 打包为 zip/tar.gz/tar.bz2
```

**MCP Resources** (只读数据):
```
http://skills/schema/templates/{type}  → 模板内容
http://skills/schema/best-practices    → 最佳实践
http://skills/schema/validation-rules  → 验证规则
```

**MCP Prompts** (可重用模板):
```
create-skill   → 引导创建新技能
validate-skill → 引导验证现有技能
refactor-skill → 引导重构技能
```

---

## 七、常用命令

### 7.1 开发环境设置

```bash
# 默认使用 conda base Python 环境
conda activate base  # 或确保在 base 环境

# 进入项目目录
cd /models/claude-glm/Skills-Creator
```

### 7.2 MCP Server 开发

```bash
# 进入 MCP Server 目录
cd skill-creator-mcp

# 安装依赖（推荐使用 uv）
uv sync --dev

# 或使用 pip
pip install -e ".[dev]"
```

### 7.3 测试命令

```bash
# 运行完整测试套件
uv run pytest --cov

# 运行特定测试
uv run pytest tests/test_tools/

# 运行特定测试文件
uv run pytest tests/test_tools/test_init_skill.py

# 运行特定测试用例
uv run pytest tests/test_tools/test_init_skill.py::test_init_skill_basic

# 查看测试覆盖率报告
uv run pytest --cov --cov-report=html
open htmlcov/index.html
```

### 7.4 代码质量检查

```bash
# 进入 MCP Server 目录
cd skill-creator-mcp

# ruff 代码检查
uv run ruff check .

# ruff 格式化
uv run ruff format .

# mypy 类型检查
uv run mypy src/

# bandit 安全检查
uv run bandit -r src/skill_creator_mcp/

# 组合检查（全部通过）
uv run ruff check . && uv run mypy src/ && uv run pytest
```

### 7.5 启动服务器

```bash
# STDIO 模式（默认）
uv run python -m skill_creator_mcp

# HTTP/SSE 模式
uv run python -m skill_creator_mcp.http
# 访问: http://localhost:8000
```

### 7.6 Git 操作

```bash
# 查看当前分支
git branch

# 查看状态
git status

# 查看变更
git diff

# 查看提交历史
git log --oneline -10

# 创建新分支
git checkout main
git pull origin main
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

### 7.7 文档操作

```bash
# 查看项目结构
tree -L 2 -I '.venv|__pycache__|*.pyc'

# 查找特定文件
find . -name "*.md" -type f

# 查找特定内容
grep -r "TODO" . --include="*.md"

# 检查链接
# (需要手动验证或使用 markdown-link-check)
```

---

## 八、.claude/plans/ 目录说明

### 8.1 目录结构

```
.claude/plans/
├── README.md              # 本说明文件
├── main/                  # 主计划和总体架构
├── phases/                # 分阶段实施计划
├── features/              # 功能特性计划
├── archive/               # 已完成的历史计划
├── feat-功能名称.md        # 功能计划
├── fix-问题描述.md         # 修复计划
└── refactor-模块.md        # 重构计划
```

### 8.2 命名规范

| 类型 | 命名格式 | 示例 |
|------|----------|------|
| 主计划 | `main-{功能}.md` | `main-mcp-server.md` |
| 阶段计划 | `phase-{N}-{描述}.md` | `phase-1-initial-setup.md` |
| 功能计划 | `feat-{功能}.md` | `feat-validate-tool.md` |
| 修复计划 | `fix-{问题}.md` | `fix-naming-validation.md` |
| 重构计划 | `refactor-{模块}.md` | `refactor-async-io.md` |

### 8.3 计划文档模板

```markdown
# 功能名称开发计划

> **创建日期**: YYYY-MM-DD
> **状态**: planning/in_progress/completed/archived
> **优先级**: P0/P1/P2/P3

## 目标
描述要实现的功能目标

## 范围
- 包含内容
- 不包含内容

## 技术依赖
- 依赖组件1
- 依赖组件2

## 任务清单
- [ ] 任务1
- [ ] 任务2
- [ ] 任务3

## 验收标准
- [ ] 功能正常工作
- [ ] 测试通过
- [ ] 文档更新

## 风险评估
| 风险 | 影响 | 缓解措施 |
|------|------|----------|

## 时间估算
- 任务1: 1天
- 任务2: 2天
- 总计: 3天

## 参考资料
- 相关文档1
- 相关文档2
```

### 8.4 计划状态流转

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
- `reopened`: 重新打开

---

## 九、相关文档链接

### 9.1 核心文档

| 文档 | 路径 | 说明 |
|------|------|------|
| Agent-Skill 入口 | `skill-creator/SKILL.md` | 技能概览和快速开始 |
| MCP Server README | `skill-creator-mcp/README.md` | MCP Server 使用说明 |
| 架构审计报告 | `ARCHITECTURE_AUDIT_REPORT_v2.md` | 完整架构审计结果 |
| 问题清单 | `ISSUES.md` | 已知问题和改进计划 |
| 路线图 | `ROADMAP.md` | 项目发展规划 |
| 变更日志 | `CHANGELOG.md` | 版本变更记录 |

### 9.2 引用文档

| 文档 | 路径 | 说明 |
|------|------|------|
| MCP 集成指南 | `skill-creator/references/mcp-integration.md` | MCP 工具使用和资源访问 |
| 最佳实践 | `skill-creator/references/best-practices.md` | 渐进式披露和描述规范 |
| 验证规范 | `skill-creator/references/validation.md` | 命名、结构、内容验证规则 |

### 9.3 计划文档

| 文档 | 路径 | 说明 |
|------|------|------|
| 计划目录 | `.claude/plans/` | 所有开发计划 |
| 计划说明 | `.claude/plans/README.md` | 计划文档规范 |

### 9.4 示例文档

| 文档 | 路径 | 说明 |
|------|------|------|
| 创建技能示例 | `skill-creator/examples/creating-a-skill.md` | 如何创建新技能 |
| 验证技能示例 | `skill-creator/examples/validating-a-skill.md` | 如何验证技能 |
| 分析技能示例 | `skill-creator/examples/analyzing-a-skill.md` | 如何分析技能 |

### 9.5 外部参考

| 资源 | 链接 | 说明 |
|------|------|------|
| FastMCP 文档 | https://jlowin.github.io/fastmcp/ | FastMCP SDK 官方文档 |
| MCP 规范 | https://modelcontextprotocol.io/ | Model Context Protocol 规范 |
| Pydantic 文档 | https://docs.pydantic.dev/ | Pydantic 2.0 官方文档 |

---

## 十、快速参考

### 10.1 开发流程速查

```
1. 制定计划 → .claude/plans/feat-xxx.md
2. 拆分任务 → TodoWrite 工具
3. 执行开发 → 编码 + 测试
4. 测试验证 → pytest --cov
5. 交叉验证 → 对照计划检查
6. 更新文档 → CHANGELOG.md
7. 阶段审计 → 归档计划
```

### 10.2 常用命令速查

```bash
# 开发环境
cd skill-creator-mcp && uv sync --dev

# 测试
uv run pytest --cov

# 代码检查
uv run ruff check . && uv run mypy src/

# 启动服务器
uv run python -m skill_creator_mcp

# Git 操作
git checkout -b feature/xxx
git commit -m "feat(scope): desc"
git push -u origin feature/xxx
```

### 10.3 优先级定义

| 优先级 | 说明 | 响应时间 |
|--------|------|----------|
| P0 | 阻塞性问题 | 立即 |
| P1 | 高优先级 | 本周内 |
| P2 | 中优先级 | 本月内 |
| P3 | 低优先级 | 有时间时 |

### 10.4 文件大小限制

| 文件类型 | 推荐大小 | 最大大小 |
|----------|----------|----------|
| SKILL.md | ≤150行 | ≤500行 |
| 引用文件 | 200-300行 | ≤400行 |
| 函数长度 | ≤50行 | ≤100行 |
| 类长度 | ≤300行 | ≤500行 |

### 10.5 质量标准

| 指标 | 要求 | 目标 |
|------|------|------|
| 测试覆盖率 | ≥80% | ≥95% |
| 代码检查 | 0 错误 | 0 警告 |
| 类型检查 | 0 错误 | 完整注解 |
| 安全检查 | 0 高危 | 0 中危 |

---

## 附录

### A. 开发环境检查清单

```bash
# 1. 检查 Python 版本
python --version  # 需要 >=3.10

# 2. 检查 conda 环境
conda info --envs  # 应在 base 环境

# 3. 检查 uv 安装
uv --version

# 4. 检查项目依赖
cd skill-creator-mcp
uv sync --dev

# 5. 运行测试
uv run pytest --cov

# 6. 检查代码质量
uv run ruff check .
uv run mypy src/
```

### B. 常见问题

**Q: 如何创建新的 MCP 工具？**
A: 参考现有工具实现，在 `server.py` 中使用 `@mcp.tool()` 装饰器。

**Q: 如何添加新的资源？**
A: 在 `server.py` 中使用 `@mcp.resource()` 装饰器定义资源。

**Q: 测试失败怎么办？**
A: 查看测试报告，定位失败原因，修复代码或更新测试。

**Q: 如何更新文档？**
A: 确保文档与代码同步，更新 CHANGELOG.md。

### C. 获取帮助

- 查看 `references/` 目录下的详细文档
- 阅读现有测试用例了解用法
- 查看 `ARCHITECTURE_AUDIT_REPORT_v2.md` 了解架构
- 查看 `ISSUES.md` 了解已知问题

---

**文档维护**: 请在每次重大变更后更新本文档。
**最后更新**: 2026-01-21
