# skill-creator 全面审核与优化计划

> **计划ID**: transient-hopping-hoare
> **创建时间**: 2026-01-30
> **状态**: planning
> **版本**: v1.0.0

---

## 一、审核概述

### 1.1 审核范围

- **审核目标**: `skill-creator/` Agent-Skill 目录
- **审核依据**:
  - Agent-Skills 最佳实践文档（`/models/claude-glm/claude-code-docs/AgentSkills*.md`）
  - 项目核心定位：为用户进行 Agent-Skills 技能开发（高效/规范/最佳实践标准化开发）
  - 开发规范：九步法流程、Git规范、文档规范

### 1.2 核心定位回顾

**Skills-Creator 核心定位**：
> 为用户进行 Agent-Skills 技能开发（高效/规范/最佳实践标准化开发）

**三大原则**：
1. Agent-Skill `skill-creator/` 和 MCP `skill-creator-mcp/` 都服务于这个目标
2. 调用外部 MCP（GitHub、Thinking）只为更好地实现 Agent-Skill 标准化开发
3. 所有任务执行必须以核心定位为前提

### 1.3 Agent-Skills 最佳实践核心原则

| 原则 | 要求 | skill-creator 状态 |
|------|------|-------------------|
| 简洁性 | 质疑每条信息的必要性 | ✅ 符合 |
| 渐进式披露 | YAML→SKILL.md→引用文件（三层） | ✅ 符合 |
| 200行规则 | SKILL.md ≤200行 | ✅ 139行 |
| 按能力组织 | 不按工具堆砌 | ✅ 按工作流阶段组织 |
| 引用文件 | 一等公民，200-300行 | ✅ 23个引用文件 |

---

## 二、审核发现

### 2.1 高优先级问题

#### 问题1：scripts/ 导入路径错误

**文件**: `skill-creator/scripts/analyze_skill.py`, `validate_skill.py`

**问题描述**:
```python
# 当前代码（错误）
script_dir = Path(__file__).parent.parent
mcp_src = script_dir / "skill-creator-mcp" / "src"
```

**实际路径结构**:
```
/models/claude-glm/Skills-Creator/
├── skill-creator/
│   └── scripts/
│       ├── analyze_skill.py
│       └── validate_skill.py
└── skill-creator-mcp/
    └── src/
```

**问题**: `script_dir.parent` 指向 `/models/claude-glm/Skills-Creator/skill-creator/`，而不是项目根目录

**正确路径**: `script_dir.parent.parent / "skill-creator-mcp" / "src"`

**影响**: 脚本无法独立运行（ImportError）

**优先级**: P0 - 脚本功能损坏

---

### 2.2 中优先级问题

#### 问题2：工具命名不一致

**范围**: SKILL.md、references/、examples/

**问题描述**:
- MCP Server 内部：所有工具都有 `_tool` 后缀（除 `package_skill`）
- 文档中混合使用有/无后缀格式

**具体对比**:

| 工具 | MCP Server 函数名 | SKILL.md 引用 | 状态 |
|------|-----------------|--------------|------|
| 初始化技能 | `init_skill_tool` | `init_skill` | ⚠️ 不一致 |
| 验证技能 | `validate_skill_tool` | `validate_skill` | ⚠️ 不一致 |
| 分析技能 | `analyze_skill_tool` | `analyze_skill` | ⚠️ 不一致 |
| 重构技能 | `refactor_skill_tool` | `refactor_skill` | ⚠️ 不一致 |
| 打包技能 | `package_skill` | `package_skill` | ✅ 一致（但无_tool） |
| 创建会话 | `create_requirement_session_tool` | `create_requirement_session_tool` | ✅ 一致 |
| 获取会话 | `get_requirement_session_tool` | `get_requirement_session_tool` | ✅ 一致 |

**影响**: 文档混淆，用户不知道使用哪种格式

**优先级**: P1 - 文档一致性

---

### 2.3 低优先级问题

#### 问题3：SKILL.md 触发词与最佳实践不完全一致

**Agent-Skills 最佳实践要求**:
- name 应使用**动名词形式**（verb-ing）：`processing-pdfs`, `analyzing-spreadsheets`

**当前状态**:
- name: `skill-creator`（名词形式，非动名词）

**影响**: 轻微，符合命名规范（小写字母、连字符），但不符合最佳实践建议

**优先级**: P3 - 可选优化

---

### 2.4 审核通过项

| 检查项 | 状态 | 说明 |
|--------|------|------|
| 核心定位一致性 | ✅ | 所有内容服务于 Agent-Skills 开发 |
| 无已弃用内容 | ✅ | 没有发现 `@deprecated` 等标记 |
| 无无效引用 | ✅ | 所有 50+ 交叉引用有效 |
| SKILL.md 大小 | ✅ | 139行 ≤ 150行要求 |
| 渐进式披露 | ✅ | 三层架构完整 |
| 按能力组织 | ✅ | 按工作流阶段，不按工具堆砌 |
| 引用文件质量 | ✅ | 23个引用文件，组织良好 |
| 示例完整性 | ✅ | 23个示例文件，覆盖全面 |

---

## 三、执行流程说明

### 3.1 强制执行要求

**逐一执行原则**（禁止跨流程）:
- 任务必须按顺序执行：T-301 → T-302 → T-303
- 每完成一个任务后，必须：
  1. 运行测试验证
  2. 更新计划状态
  3. 提交 Git commit
  4. 确认验收标准满足后，才开始下一个任务

**九步法流程要求**:
- 步骤0: 前置任务审核 ✅ 已完成
- 步骤1: 制定开发计划 ✅ 已完成（本文件）
- 步骤2: 拆分任务清单 → 需创建 TodoWrite 任务
- 步骤3-9: 每个任务执行时遵循

**禁止行为**:
- ❌ 跨任务并行执行
- ❌ 跳过测试验证
- ❌ 不提交 commit 就继续下一个任务
- ❌ 基于文档/摘要审核（必须基于实际代码）

### 3.2 任务执行顺序

```
T-301 (P0)
  ↓ 验收通过 + commit
T-302 (P1)
  ↓ 验收通过 + commit
T-303 (P2)
  ↓ 验收通过 + commit
步骤4-9: 测试验证 → 交叉验证 → 更新文档 → 阶段审计 → Git提交 → 阶段汇报
```

---

## 四、任务清单

### 阶段1：修复高优先级问题（P0）

#### T-301: 修复 scripts/ 导入路径

**描述**: 修复 `analyze_skill.py` 和 `validate_skill.py` 中的导入路径错误

**文件**:
- `skill-creator/scripts/analyze_skill.py`
- `skill-creator/scripts/validate_skill.py`

**变更内容**:
```python
# 修改前
script_dir = Path(__file__).parent.parent
mcp_src = script_dir / "skill-creator-mcp" / "src"

# 修改后
script_dir = Path(__file__).parent.parent.parent
mcp_src = script_dir / "skill-creator-mcp" / "src"
```

**验收标准**:
- [ ] 脚本可以独立运行（不报 ImportError）
- [ ] 测试 `python scripts/analyze_skill.py .` 成功执行
- [ ] 测试 `python scripts/validate_skill.py .` 成功执行

**优先级**: P0

**状态**: pending

---

### 阶段2：修复中优先级问题（P1）

#### T-302: 统一 MCP 工具命名规范

**描述**: 在文档中统一 MCP 工具的命名格式，避免混淆

**用户确认方案**: **选项B - 完整工具名（带 `_tool` 后缀）**

**实施方案**: 文档统一使用完整工具名，与 MCP Server 内部函数名完全一致

**工具命名列表**:
- 技能工具：`init_skill_tool`, `validate_skill_tool`, `analyze_skill_tool`, `refactor_skill_tool`
- 打包工具：`package_skill`（特殊：无 `_tool` 后缀，需在文档中说明）
- 需求工具：`create_requirement_session_tool`, `get_requirement_session_tool`, `update_requirement_answer_tool`, `get_static_question_tool`, `generate_dynamic_question_tool`, `validate_answer_format_tool`, `check_requirement_completeness_tool`

**影响文件**:
- `skill-creator/SKILL.md`
- `skill-creator/references/mcp-integration.md`
- `skill-creator/references/requirement-workflow.md`
- `skill-creator/examples/*.md`

**验收标准**:
- [ ] 所有文档中工具引用格式统一
- [ ] 在 mcp-integration.md 中添加命名约定说明
- [ ] 更新 CHANGELOG.md 记录变更

**优先级**: P1

**状态**: pending

---

### 阶段3：完整性验证（P2）

#### T-303: 完整性验证与文档一致性检查

**描述**: 全面验证 skill-creator/ 目录中所有内容的完整性和一致性

**检查项目**:
1. **引用完整性**: 所有 `[链接](references/xxx.md)` 都有效
2. **示例完整性**: 所有示例代码可执行
3. **术语一致性**: 技术术语在所有文档中保持一致
4. **版本一致性**: SKILL.md 中的版本号与实际版本一致
5. **工具列表一致性**: 所有文档中的工具列表与 MCP Server 实际工具一致

**验收标准**:
- [ ] 所有引用链接有效（无 404）
- [ ] 所有示例代码经过验证
- [ ] 术语表完整并应用于所有文档
- [ ] 版本号一致性确认
- [ ] 工具列表一致性确认

**优先级**: P2

**状态**: pending

---

## 四、进度追踪

### 当前状态

| 状态 | 说明 |
|------|------|
| 计划状态 | in_progress |
| 开始时间 | 2026-01-30 |
| 完成任务 | 2/3 (67%) |
| 最近更新 | 2026-01-30 |

### 任务状态总览

| 任务ID | 任务名称 | 优先级 | 状态 | Commit |
|--------|----------|--------|------|--------|
| T-301 | 修复 scripts/ 导入路径 | P0 | completed | 02d9789 |
| T-302 | 统一 MCP 工具命名规范 | P1 | completed | e161ad5 |
| T-303 | 完整性验证与文档一致性检查 | P2 | pending | - |

**注意**: 所有任务必须逐一执行完成，禁止并行或跨流程

---

## 五、交叉验证

### 验证清单

- [ ] T-301: 脚本可以独立运行
- [ ] T-302: 文档中工具引用格式统一
- [ ] T-303: 完成影响评估（如适用）

---

## 六、归档检查清单

### 所有任务必须完成（100%强制）

- [ ] T-301: 修复 scripts/ 导入路径 - **验收标准全部满足**
- [ ] T-302: 统一 MCP 工具命名规范 - **验收标准全部满足**
- [ ] T-303: 完整性验证与文档一致性检查 - **验收标准全部满足**

### 其他归档条件（100%强制）

- [ ] 所有验收标准满足
- [ ] 有完整的 Git commit 记录（每个任务一个 commit）
- [ ] 更新 CHANGELOG.md
- [ ] **100% 基于实际代码审核**（不依赖文档/摘要）
- [ ] 交叉验证完成（对照计划检查所有任务）

### 禁止虚假审核（强制）

- ❌ 禁止未完成任务就归档
- ❌ 禁止任务状态与实际不符
- ❌ 禁止仅基于文档/摘要审核
- ❌ 禁止跳过交叉验证

---

## 七、参考资料

### Agent-Skills 最佳实践文档

- `/models/claude-glm/claude-code-docs/AgentSkills官方最佳实践.md`
- `/models/claude-glm/claude-code-docs/AgentSkills.md`
- `/models/claude-glm/claude-code-docs/AgentSkills官方文档.md`

### 项目文档

- `/models/claude-glm/Skills-Creator/CLAUDE.md` - 开发指南
- `/models/claude-glm/Skills-Creator/skill-creator/SKILL.md` - Agent-Skill 入口
- `/models/claude-glm/Skills-Creator/skill-creator-mcp/README.md` - MCP Server 说明

---

## 八、变更日志

| 日期 | 版本 | 变更说明 |
|------|------|----------|
| 2026-01-30 | v1.0.0 | 创建审核计划 |
