# Skills-Creator 开发指南

> **文档版本**: v1.5.1
> **更新日期**: 2026-01-27
> **适用范围**: Skills-Creator 项目开发
> **主要变更**: 计划管理流程规范化（v1.5优化：消除重复、精简内容）

本文档为 Claude AI 提供项目开发规范和工作流程指南，确保代码质量和开发效率。

---

## 一、项目概述

### 1.1 项目定位

**Skills-Creator** 是一个基于 **MCP Server + Agent-Skill 混合架构**的完整解决方案，用于开发、验证和优化 Agent-Skills。

- **当前版本**: v0.3.3
- **开发环境**: conda base Python 环境
- **测试覆盖率**: 96% (594个测试用例)
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
│  │  - 18 Tools (5类)                  │  │
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
│   ├── tests/                  # 测试套件 (96% 覆盖率, 594个测试)
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
│   ├── plans/                  # 开发计划
│   │   ├── .templates/         # 计划模板
│   │   └── archive/            # 已归档计划
│   └── scripts/                # 辅助脚本
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

### 1.5 MCP工具分类标准

MCP Server提供18个工具，按功能划分为5类：

| 类别 | 工具数量 | 工具列表 |
|------|----------|----------|
| **技能工具** | 4 | init_skill, validate_skill, analyze_skill, refactor_skill |
| **打包工具** | 2 | package_skill, package_agent_skill |
| **需求收集原子工具** | 7 | create_requirement_session, get_requirement_session, update_requirement_answer, get_static_question, generate_dynamic_question, validate_answer_format, check_requirement_completeness |
| **批量操作** | 2 | batch_validate_skills, batch_analyze_skills |
| **健康检查** | 3 | health_check, quick_status, is_healthy |

**总计**: 4 + 2 + 7 + 2 + 3 = 18个工具

**注意**: Phase 0验证工具（5个）已迁移到开发工具脚本（`skill-creator-mcp/scripts/dev-tools.py`），不作为MCP工具暴露。

**注意**:
- 需求收集原子工具（7个）替代了旧的`collect_requirements`单一工具，符合ADR 001原子化原则
- MCP Server还提供4个Resources和3个Prompts，但这些不计入工具数量

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
| **9** | 阶段性汇报 | • 汇总已完成任务<br>• 记录问题和解决方案<br>• 记录测试和质量指标<br>• **归档检查清单验证**<br>• **全部完成或用户同意后归档** | 汇报文档 |

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
| 步骤3 | 未更新计划进度或未提交commit | 追溯困难 | 补充更新计划并提交commit |
| 步骤4 | 跳过测试 | 质量风险 | 补全测试，确保通过 |
| 步骤5 | 未执行交叉验证 | 遗漏问题 | 执行完整交叉验证 |
| 步骤5 | 发现问题未回退 | 质量缺陷 | 使用TODO回退机制 |
| 步骤6 | 文档未同步 | 技术债务 | 补充文档更新 |
| 步骤7 | 未通过审计 | 进度偏差 | 修正偏差后重新审计 |
| 步骤8 | 提交不规范 | 版本混乱 | 修正提交信息 |
| 步骤9 | 未全部完成任务且未经用户同意就归档 | 计划不完整 | 恢复计划，完成剩余任务或获取用户同意 |
| 步骤9 | 归档时缺少追溯记录 | 无法追溯 | 补充commit记录和进度报告 |
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

**Scope（作用域）说明**:

| 规则 | 说明 | 示例 |
|------|------|------|
| **推荐使用** | 对于涉及特定模块或组件的更改 | `fix(test): 修复导入错误` |
| **可省略** | 对于涉及多个模块或通用性更改 | `docs: 更新README` |
| **常用scope** | mcp/skill/test/docs/audit/plan | `feat(mcp): 添加新工具` |
| **避免过细** | 不需要指定到具体函数或类 | ❌ `fix(utils/validators.py:validate_naming): ...` |

**何时使用scope**:
- ✅ 修复特定模块的bug → `fix(test): 修复测试导入`
- ✅ 添加功能到特定组件 → `feat(mcp): 添加批量验证`
- ✅ 更新特定文档 → `docs(api): 更新API文档`
- ⚠️ 多个模块改动 → 可省略或使用通用scope
- ❌ 微小改动（如拼写修复） → 直接用type即可

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
├── .templates/            # 计划模板（新增）
│   ├── plan-template.md
│   └── progress-report-template.md
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

#### 4.2.1 计划状态管理

**状态定义（5种）**:
```
planning → in_progress → partially_completed → completed → archived
    ↑           │              │                    │
    └───────────┴──────────────┴────────────────────┘
              (状态可回退，需记录原因)
```

**状态说明**:

| 状态 | 含义 | 进入条件 | 可执行操作 |
|------|------|----------|------------|
| `planning` | 规划中 | 计划创建 | 编辑计划内容 |
| `in_progress` | 执行中 | 开始执行第一个任务 | 更新任务状态、提交commit |
| `partially_completed` | 阶段性完成 | P0+P1任务完成 | 更新计划状态、提交阶段性报告、**不可归档** |
| `completed` | 全部完成 | 所有任务完成或用户同意 | 执行九步法步骤6-9 |
| `archived` | 已归档 | 完成步骤9 | 只读，不可修改 |

**状态流转规则**:
- 正常流程：`planning → in_progress → partially_completed → completed → archived`
- 允许回退：任何状态可回退到前一状态（需记录原因）
- 禁止跳过：不可从 `in_progress` 直接跳到 `archived`

#### 4.2.2 归档条件（强制）

**条件1: 全部完成**
```
所有任务状态 = completed
AND
所有验收标准满足
AND
代码已通过测试验证
```

**条件2: 用户明确同意**
```
P0+P1任务完成
AND
用户明确同意归档未完成的计划
AND
未完成任务已迁移到新计划或标记为cancelled
AND
原计划包含完整的追溯记录（commit + 进度报告）
```

**归档检查清单**:
- [ ] P0任务全部完成
- [ ] P1任务全部完成
- [ ] P2任务全部完成（或用户同意跳过）
- [ ] P3任务全部完成（或用户同意跳过）
- [ ] 验收标准全部满足
- [ ] 有完整的Git commit记录
- [ ] 有阶段性进度报告
- [ ] 未完成任务已处理（迁移或取消）

#### 4.2.3 进度追踪机制

**每次任务完成必须执行**:
1. 更新计划文档中的任务状态
2. 更新TodoWrite中的任务状态
3. 提交Git commit（规范格式见3.2节和4.2.4节）
4. （可选）生成阶段性进度报告

**计划文档必须包含**:

**1. 任务清单表格** - 记录任务ID、名称、优先级、状态、完成时间、commit

**2. 进度追踪区域** - 记录当前状态、开始时间、任务完成情况、最近更新

**3. 归档检查清单** - 验证归档条件是否满足

> 详细的任务清单表格和进度追踪区域示例，请参见：`.claude/plans/.templates/plan-template.md`

#### 4.2.4 Commit规范（强制性）

> 通用Commit规范详见 **第三章3.2节**。

**计划进度更新的Commit格式**:
```
chore(plan): 更新计划进度 - [计划名称]

完成工作:
- [任务ID] 任务描述 (状态: completed)
- [任务ID] 任务描述 (状态: in_progress)

变更文件:
- .claude/plans/[计划名称].md

任务完成进度: X/Y (Z%)
下一阶段: [下一阶段任务描述]
```

**示例**:
```
chore(plan): 更新P3阶段优化任务进度

完成工作:
- T-301 清理__pycache__ (状态: completed)
- T-302 测试覆盖率缺口分析 (状态: in_progress)

变更文件:
- .claude/plans/jolly-exploring-pinwheel.md

任务完成进度: 1/2 (50%)
下一阶段: 继续执行T-302覆盖率缺口分析
```

#### 4.2.5 未完成任务处理机制

> 详细的迁移流程和示例，请参见迁移工具：`.claude/scripts/migrate-plan.py`

**机制1: 迁移到新计划**

适用场景：P2/P3任务需要延期但不阻塞当前计划归档

流程：
1. 在原计划中标记任务状态为 `migrated`
2. 创建新计划，包含迁移的任务
3. 在新计划中引用原计划（追溯关系）
4. 用户明确同意后归档原计划

**机制2: 用户同意归档**

适用场景：低优先级任务决定不再执行

流程：
1. 在计划中标记任务状态为 `cancelled`
2. 记录取消原因和用户同意时间
3. 在归档报告中说明
4. 用户明确确认后归档

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

> 本章为速查参考，详细说明请参见对应章节。

### 6.1 开发流程速查

完整流程说明详见 **第二章**，简要流程如下：

```
步骤0: 前置审核 → 步骤1: 制定计划 → 步骤2: 拆分任务 → 步骤3: 执行开发
→ 步骤4: 测试验证 → 步骤5: 交叉验证 → 步骤6: 更新文档 → 步骤7: 阶段审计
→ 步骤8: Git提交 → 步骤9: 阶段汇报并归档
```

### 6.2 常用命令速查表

完整命令说明详见 **第五章**。

| 类别 | 命令 | 说明 | 详细章节 |
|------|------|------|----------|
| **开发环境** | `cd skill-creator-mcp && uv sync --dev` | 安装依赖 | 5.2 |
| **测试** | `uv run pytest --cov` | 运行测试套件 | 5.3 |
| **代码检查** | `uv run ruff check . && uv run mypy src/` | 质量检查 | 5.3 |
| **启动服务器** | `uv run python -m skill_creator_mcp` | STDIO模式 | 5.5 |
| **创建分支** | `git checkout -b feature/xxx` | 新功能分支 | 5.4 |
| **提交变更** | `git commit -m "feat(scope): desc"` | 提交代码 | 5.4 |
| **推送远程** | `git push -u origin feature/xxx` | 推送到远程 | 5.4 |

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
| CLAUDE.md | ≤800行 | ≤1000行 |
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
| 技术债务 | `.claude/technical-debt.md` | 技术债务追踪 |

**引用文档**:

| 文档 | 路径 | 说明 |
|------|------|------|
| MCP 集成指南 | `skill-creator/references/mcp-integration.md` | MCP 工具使用和资源访问 |
| 最佳实践 - 核心 | `skill-creator/references/best-practices-core.md` | 基础架构和规范 |
| 最佳实践 - 高级 | `skill-creator/references/best-practices-advanced.md` | 高级技巧和优化 |
| 验证规范 | `skill-creator/references/validation.md` | 命名、结构、内容验证规则 |

**计划管理**:

| 文档 | 路径 | 说明 |
|------|------|------|
| 计划模板 | `.claude/plans/.templates/plan-template.md` | 标准计划模板 |
| 进度报告模板 | `.claude/plans/.templates/progress-report-template.md` | 进度报告模板 |
| 归档计划 | `.claude/plans/archive/` | 已归档的计划文档 |

**外部参考**:

| 资源 | 链接 | 说明 |
|------|------|------|
| FastMCP 文档 | https://jlowin.github.io/fastmcp/ | FastMCP SDK 官方文档 |
| MCP 规范 | https://modelcontextprotocol.io/ | Model Context Protocol 规范 |
| Pydantic 文档 | https://docs.pydantic.dev/ | Pydantic 2.0 官方文档 |

### 6.7 常见问题

| 问题 | 解决方案 | 相关章节 |
|------|----------|----------|
| 如何创建新的 MCP 工具？ | 参考现有工具实现，在 `server.py` 中使用 `@mcp.tool()` 装饰器 | 5.1 |
| 如何添加新的资源？ | 在 `server.py` 中使用 `@mcp.resource()` 装饰器定义资源 | 5.1 |
| 测试失败怎么办？ | 查看测试报告，定位失败原因，修复代码或更新测试 | 5.3 |
| 如何更新文档？ | 确保文档与代码同步，更新 CHANGELOG.md | 4.1 |
| 如何创建开发计划？ | 使用 `.claude/plans/.templates/plan-template.md` 模板 | 4.2 |
| 如何归档计划？ | 所有任务完成或用户同意后，移动到 `archive/` 目录 | 4.2.2 |

---

## 七、Agent-Skill 打包规范

### 7.1 打包规范概述

Agent-Skill 打包是发布和分发技能的重要环节。标准化的打包格式确保用户可以轻松安装和使用技能。

**核心原则**:
- **最小化**: 只包含必需文件，排除开发文件
- **标准化**: 使用统一的包名格式和版本号
- **可验证**: 打包后可验证结构和内容

### 7.2 标准包结构

**正确的 Agent-Skill 包结构**:
```
skill-creator-v0.3.1.zip
└── skill-creator/
    ├── SKILL.md          # 必需
    ├── examples/         # 可选
    ├── references/       # 可选
    └── scripts/          # 可选
```

**质量指标**:
| 指标 | 推荐值 | 最大值 |
|------|--------|--------|
| 文件数量 | 20-40 | <50 |
| 包大小 | 100-300KB | <500KB |

### 7.3 排除文件列表

**必须排除的文件和目录**:

| 类别 | 排除项 | 原因 |
|------|--------|------|
| 版本控制 | `.git`, `.gitignore`, `.gitattributes`, `.github` | 开发专用 |
| 开发环境 | `.vscode`, `.idea`, `*.swp`, `*.swo` | IDE 配置 |
| 计划归档 | `.claude/plans/archive`, `.claude/archive` | 开发历史 |
| 项目文档 | `README.md`, `CHANGELOG.md`, `CONTRIBUTING.md`, `LICENSE` | 项目级 |
| MCP Server | `*-mcp`, `*_mcp`, `mcp-server` | 独立打包 |
| 测试文件 | `tests/`, `.pytest_cache`, `htmlcov`, `.coverage` | 开发专用 |
| Python 构建 | `__pycache__`, `*.pyc`, `*.pyo`, `*.egg-info`, `dist/`, `build/` | 构建产物 |
| 虚拟环境 | `.venv`, `venv`, `env`, `.env` | 环境特定 |
| 日志临时 | `*.log`, `*.tmp`, `*.bak` | 临时文件 |

### 7.4 打包命令示例

**使用 package_agent_skill（推荐）**:
```python
from skill_creator_mcp.utils.packagers import package_agent_skill

result = package_agent_skill(
    skill_path="/path/to/skill-creator",
    output_dir="/output",
    version="0.3.1",
    package_format="zip",
    include_tests=False,
    validate_before_package=True
)

# 结果: skill-creator-v0.3.1.zip
```

**使用 MCP 工具**:
```python
# 在 Claude Code 中调用 MCP 工具
await package_agent_skill(
    ctx,
    skill_path="/path/to/skill-creator",
    output_dir="/output",
    version="0.3.1",
    format="zip"
)
```

### 7.5 验证包质量

**解压验证**:
```bash
# 列出包内容（前30行）
unzip -l skill-creator-v0.3.1.zip | head -30

# 统计文件数量
unzip -l skill-creator-v0.3.1.zip | tail -1

# 检查包大小
ls -lh skill-creator-v0.3.1.zip
```

**结构验证**:
```bash
# 解压到临时目录
unzip -q skill-creator-v0.3.1.zip -d /tmp/test-skill
cd /tmp/test-skill/skill-creator

# 验证排除项
[ -d ".claude/plans/archive" ] && echo "❌" || echo "✅ 归档已排除"
[ -f "README.md" ] && echo "❌" || echo "✅ README 已排除"
[ -d "../skill-creator-mcp" ] && echo "❌" || echo "✅ MCP 已排除"

# 验证包含项
[ -f "SKILL.md" ] && echo "✅" || echo "❌ 缺少 SKILL.md"
[ -d "examples" ] && echo "✅" || echo "❌ 缺少 examples/"
```

### 7.6 发布流程

1. **打包**: 使用 `package_agent_skill()` 创建标准包
2. **验证**: 检查包结构和质量指标
3. **测试**: 在新环境中解压并验证
4. **发布**: 上传到 GitHub Releases 或其他分发平台
5. **文档**: 更新 CHANGELOG.md 和发布说明

---

**文档维护**: 请在每次重大变更后更新本文档。
**最后更新**: 2026-01-27 (v1.5.1 - 计划管理流程规范化优化)
