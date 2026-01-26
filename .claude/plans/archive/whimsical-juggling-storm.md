# 删除Agent-Skill中的违规MCP文档引用

> **计划类型**: 架构修复 (fix-architecture-violation)
> **创建日期**: 2026-01-26
> **目标版本**: v0.3.1
> **当前分支**: develop
> **参考文档**: `docs/adr/001-hybrid-architecture.md`

---

## 一、执行摘要

基于对项目架构的深入审核，发现 Agent-Skill `skill-creator/` 违规引用了 MCP Server `skill-creator-mcp/` 的文档，违反了**混合架构的职责分离原则**。

**核心原则**:
- Agent-Skill: 工作流编排 + 知识传递（用户视角）
- MCP Server: 原子操作 + 文件 I/O（实现细节）
- **Agent-Skill 不应引用 MCP Server 的文档**

**修复方案**: 删除所有违规引用，确保 Agent-Skill 专注于工作流编排。

---

## 二、架构违规分析

### 2.1 职责边界定义（来自 ADR 001）

```
┌─────────────────────────────────────────────────────────────┐
│                     Claude Code / Desktop                    │
│                                                              │
│  ┌────────────────────────────────────────────────────────┐ │
│  │          Agent-Skill (skill-creator)                   │ │
│  │  - 编排工作流程                                        │ │
│  │  - 渐进式披露知识                                      │ │
│  │  - 最佳实践指导                                        │ │
│  └────────────────────┬───────────────────────────────────┘ │
│                         │ 调用（而非引用文档）                │
│  ┌────────────────────▼───────────────────────────────────┐ │
│  │         MCP Server (skill-creator-mcp)                 │ │
│  │  - 原子操作工具                                        │ │
│  │  - 只读资源                                            │ │
│  │  - 可重用模板                                          │ │
│  └─────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────┘
```

### 2.2 正确的引用方向

| 引用来源 | 引用目标 | 是否正确 | 原因 |
|---------|---------|----------|------|
| Agent-Skill | MCP **工具调用** | ✅ | 必需的接口使用 |
| Agent-Skill | MCP **配置文档** | ❌ | 实现细节，不属于工作流 |
| Agent-Skill | 项目级 ADR | ✅ | 架构决策共享 |
| Agent-Skill | Agent-Skill 内部文档 | ✅ | 自身知识传递 |
| MCP Server | Agent-Skill 文档 | ❌ | MCP 不应依赖 Agent-Skill |

### 2.3 Agent-Skill 可以引用的内容

| 类型 | 示例 | 说明 |
|------|------|------|
| 项目级 ADR | `../docs/adr/001-hybrid-architecture.md` | 架构决策 |
| Agent-Skill 引用文档 | `references/mcp-integration.md` | MCP 工具**使用**指南 |
| Agent-Skill 示例 | `examples/mcp-skill-collaboration.md` | 工作流示例 |
| 外部规范 | MCP 规范、FastMCP 文档 | 外部标准 |

### 2.4 Agent-Skill 不应引用的内容

| 类型 | 示例 | 原因 |
|------|------|------|
| MCP 配置文档 | `skill-creator-mcp/docs/configuration.md` | MCP 实现细节 |
| MCP API 文档 | `skill-creator-mcp/docs/api.md` | MCP 实现细节 |
| MCP IDE 配置 | `skill-creator-mcp/docs/ide-config.md` | MCP 运维配置 |

---

## 三、违规引用清单（基于实际代码审核）

### 违规1: SKILL.md 引用 MCP 配置文档 [P0]

**文件**: `skill-creator/SKILL.md:153-159`

**当前内容**:
```markdown
### 详细配置文档

> 📘 完整配置指南请参考：
> - [MCP Server Claude Code 配置指南](skill-creator-mcp/docs/claude-code-config.md)
> - [MCP Server 配置参数参考](skill-creator-mcp/docs/configuration.md)
> - [MCP Server IDE 集成配置](skill-creator-mcp/docs/ide-config.md)
```

**问题**: Agent-Skill 引用了 MCP Server 的配置文档（实现细节）

**修复**: 删除整个章节

---

### 违规2: references/README.md 引用 MCP 配置文档 [P0]

**文件**: `skill-creator/references/README.md:17-21`

**当前内容**:
```markdown
### 配置指南

| 文档 | 说明 | 类型 |
|------|------|------|
| **[Claude Code 配置指南](../docs/claude-code-configuration.md)** | Claude Code 详细配置说明 | 完整指南 |
| **[MCP Server 配置参数](../../skill-creator-mcp/docs/configuration.md)** | 所有环境变量参考 | 参数参考 |
| **[MCP Server IDE 配置](../../skill-creator-mcp/docs/ide-config.md)** | 各种 IDE 集成配置 | 配置示例 |
```

**问题**:
1. 引用了不存在的 `../docs/claude-code-configuration.md`
2. 引用了 MCP Server 的配置文档（实现细节）

**修复**: 删除"配置指南"章节

---

### 违规3: examples/README.md 引用 MCP 配置文档 [P1]

**文件**: `skill-creator/examples/README.md:74`

**当前内容**:
```markdown
| 配置 Claude Code | [Claude Code 配置指南](../docs/claude-code-configuration.md)
```

**问题**: 引用了不存在的文件，且属于 MCP 配置范畴

**修复**: 删除此行

---

### 违规4: ide-config.md 错误反向引用 [P1]

**文件**: `skill-creator-mcp/docs/ide-config.md:341`

**当前内容**:
```markdown
- [Agent-Skill 配置指南](../skill-creator/docs/claude-code-configuration.md)
```

**问题**:
1. 目标文件不存在
2. MCP Server 不应引用 Agent-Skill 的文档（保持独立）

**修复**: 删除此行或改为指向项目根文档

---

### 违规5: CHANGELOG.md 过时记录 [P2]

**文件**: `CHANGELOG.md:22`

**当前内容**:
```markdown
- `skill-creator/docs/claude-code-configuration.md` - Agent-Skill配置指南
```

**问题**: 记录了从未创建的文件

**修复**: 删除此行

---

## 四、修复方案

### 核心原则

**使用 Git 回滚而非手动修改**

理由：
1. 更高效 - 直接恢复到干净的快照点
2. 更精准 - 基于实际历史状态，避免人为错误
3. 可追溯 - 清楚记录回滚操作

### 问题 Commit 识别

**引入违规引用的 commit**: `ab61f83` - "docs: 完善MCP Server和Agent-Skill文档"

**修改的文件**:
```
skill-creator/SKILL.md             +64行（新增配置章节）
skill-creator/examples/README.md   +3行
skill-creator/references/README.md +11行
```

**干净的快照点**: `ab61f83^` (即 commit `9a9fa24`)

### 回滚方案

使用 `git checkout` 直接将文件恢复到 clean 状态：

```bash
# 回滚到 ab61f83 之前的状态
git checkout ab61f83^ -- skill-creator/SKILL.md
git checkout ab61f83^ -- skill-creator/references/README.md
git checkout ab61f83^ -- skill-creator/examples/README.md
```

### MCP Server 文档保留

**重要**: `skill-creator-mcp/docs/` 下的文档不受影响，这些是 MCP Server 的合法文档：
- `skill-creator-mcp/docs/claude-code-config.md`
- `skill-creator-mcp/docs/configuration.md`
- `skill-creator-mcp/docs/ide-config.md`
- 等等...

### 修复后的状态

**skill-creator/SKILL.md**:
- 删除: "Claude Code 配置"章节（第95-159行）
- 删除: "详细配置文档"引用（第153-158行）
- 保留: 工作流编排和 MCP 工具使用说明

**skill-creator/references/README.md**:
- 删除: "配置指南"章节

**skill-creator/examples/README.md**:
- 删除: 配置相关条目

---

## 五、任务清单

### 前置检查（步骤0）

- [x] 确认当前分支: develop
- [ ] 确认无未提交修改
- [ ] 拉取最新代码
- [ ] 创建功能分支 `fix/revert-invalid-mcp-references`

### 任务1: Git 回滚 skill-creator/ 文件到 clean 状态 [P0]

**操作**: 使用 `git checkout` 回滚到 `ab61f83^` 状态

```bash
# 回滚三个文件
git checkout ab61f83^ -- skill-creator/SKILL.md
git checkout ab61f83^ -- skill-creator/references/README.md
git checkout ab61f83^ -- skill-creator/examples/README.md
```

**验证**: 查看修改状态，确认只删除了违规引用

### 任务2: 手动修复 ide-config.md 反向引用 [P1]

**文件**: `skill-creator-mcp/docs/ide-config.md:341`

**操作**: 删除对不存在文件的引用

```bash
# 使用 Edit 工具删除违规引用行
```

**验证**: MCP 文档不再引用不存在的 Agent-Skill 文件

### 任务3: 更新 CHANGELOG.md [P2]

**文件**: `CHANGELOG.md:22`

**操作**: 删除过时的文件引用记录

**验证**: CHANGELOG 与实际文件结构一致

### 任务4: 全局引用验证 [P0]

**操作**:
1. 验证 skill-creator/ 不再引用 skill-creator-mcp/docs/
2. 验证 MCP 文档保持独立
3. 确保所有剩余引用符合架构规范

**验证命令**:
```bash
# 验证无违规引用
grep -r "skill-creator-mcp/docs/" skill-creator/ --include="*.md" || echo "验证通过"
grep -r "claude-code-configuration.md" skill-creator/ --include="*.md" || echo "验证通过"
```

---

## 六、关键文件清单

| 文件 | 操作 | 优先级 |
|------|------|--------|
| `skill-creator/SKILL.md` | 删除章节 | P0 |
| `skill-creator/references/README.md` | 删除章节 | P0 |
| `skill-creator/examples/README.md` | 删除行 | P1 |
| `skill-creator-mcp/docs/ide-config.md` | 删除引用 | P1 |
| `CHANGELOG.md` | 删除行 | P2 |

---

## 七、验证计划

### 7.1 自动化验证

```bash
# 验证 Agent-Skill 不再引用 MCP 文档
grep -r "skill-creator-mcp/docs/" skill-creator/ --include="*.md" && echo "发现违规引用" || echo "验证通过"

# 验证不存在 docs/claude-code-configuration.md 引用
grep -r "claude-code-configuration.md" skill-creator/ --include="*.md" && echo "发现违规引用" || echo "验证通过"
```

### 7.2 架构合规性检查

- [ ] Agent-Skill 所有引用都是: 项目级文档、内部文档、外部规范
- [ ] Agent-Skill 不引用 MCP 文档、配置、API
- [ ] MCP 文档保持独立，不引用 Agent-Skill
- [ ] 符合 ADR 001 的职责分离原则

### 7.3 功能验证

- [ ] SKILL.md 仍能正确引导用户使用 Agent-Skill
- [ ] references/README.md 提供足够的文档索引
- [ ] 删除的引用不影响用户理解和使用

---

## 八、实施步骤（遵循九步法）

```
步骤0: 前置任务审核
  └─ 确认 Git 环境，创建功能分支

步骤1: 制定开发计划
  └─ 创建计划文档（本文档）✅

步骤2: 拆分任务清单
  └─ 创建 6 个任务

步骤3: 执行开发工作
  ├─ 按优先级 P0 → P1 → P2 顺序执行
  └─ 实时更新 TODO 状态

步骤4: 测试验证
  └─ 运行架构合规性检查

步骤5: 交叉验证
  └─ 确认所有违规引用已删除

步骤6: 更新文档
  └─ 更新 CHANGELOG.md

步骤7: 阶段性审计
  └─ 确认符合架构规范

步骤8: Git提交
  └─ 规范 commit 信息

步骤9: 阶段性汇报
  └─ 归档计划到 archive/
```

---

## 九、预期成果

1. **架构合规**: Agent-Skill 不再引用 MCP 文档
2. **职责清晰**: 明确工作流层与工具层的边界
3. **文档简洁**: Agent-Skill 专注于知识传递，而非配置细节
4. **验证报告**: 0 个违规引用

---

## 十、风险评估

| 风险 | 影响 | 缓解措施 |
|------|------|----------|
| 删除后用户找不到配置说明 | 用户体验下降 | MCP 文档已包含完整配置说明 |
| 删除了必要信息 | 功能缺失 | 确保 `mcp-integration.md` 包含工具使用说明 |
| 引用方向理解偏差 | 新的违规 | 严格遵循 ADR 001 架构原则 |

---

## 十一、后续改进

1. **文档规范**: 明确 Agent-Skill 与 MCP 的文档边界
2. **CI 检查**: 添加架构合规性检查到 CI/CD
3. **架构审计**: 定期审核文档引用是否符合 ADR 001

---

**创建者**: Claude AI
**审核状态**: 待用户批准
**参考文档**: `docs/adr/001-hybrid-architecture.md`
**核心原则**: Agent-Skill 编排工作流，MCP Server 提供原子操作
