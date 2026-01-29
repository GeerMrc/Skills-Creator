# Skills-Creator [MCP skill-creator-mcp] 全面审核与修复计划

**计划类型**: 代码质量与文档一致性全面审核修复
**创建日期**: 2026-01-29
**优先级**: P0 (严重)
**计划状态**: in_progress

---

## 一、项目核心定位回顾

> **核心定位**（必读）

**Skills-Creator** 项目（包含 Agent-Skill `skill-creator/` 与 MCP `skill-creator-mcp/`）的核心定位是：

**为用户提出的需求进行 Agent-Skills 技能开发（高效/规范/最佳实践标准化开发）**

**关键原则**:
- Agent-Skill `skill-creator/` 和 MCP `skill-creator-mcp/` 都服务于这个目标
- 调用外部 MCP（GitHub、Thinking等）仅为更好地实现 Agent-Skill 标准化开发
- 所有任务执行必须以核心定位为前提

---

## 二、问题背景

### 2.1 审核发现摘要

基于100%实际代码审核，发现以下5类严重问题：

| 问题类别 | 严重程度 | 影响范围 |
|----------|----------|----------|
| **工具数量不一致** | 🔴 严重 | 多个文档声称18个工具，实际12个 |
| **测试数量不一致** | 🔴 严重 | 文档显示588/613个，实际568个 |
| **版本号不一致** | 🔴 严重 | 文档显示v0.3.4，代码仍是v0.3.3 |
| **过时工具引用** | 🔴 严重 | 15处文档引用已移除工具 |
| **无用代码残留** | 🟡 中等 | ~160行未使用代码 |

### 2.2 实际MCP工具清单（审核基准）

**实际暴露的工具数量：12个**

```
技能工具（4个）：
├── init_skill_tool
├── validate_skill_tool
├── analyze_skill_tool
└── refactor_skill_tool

需求收集原子工具（7个）：
├── create_requirement_session_tool
├── get_requirement_session_tool
├── update_requirement_answer_tool
├── get_static_question_tool
├── generate_dynamic_question_tool
├── validate_answer_format_tool
└── check_requirement_completeness_tool

打包工具（1个）：
└── package_skill

总计：12个工具
```

### 2.3 已移除工具列表（用于清理）

**已从代码中移除，但文档中仍有引用的工具：**

1. `package_agent_skill` - 已在v0.3.3中被`package_skill`替代
2. `batch_validate_skills` - 批量验证工具
3. `batch_analyze_skills` - 批量分析工具
4. `health_check` - 健康检查工具
5. `quick_status` - 快速状态工具
6. `is_healthy` - 快速健康检查工具

---

## 三、执行任务清单

| 任务ID | 任务名称 | 优先级 | 状态 | 完成时间 | Commit |
|--------|----------|--------|------|----------|--------|
| T-20260129-101 | 运行测试获取准确数量 | P0 | completed | 2026-01-29 | - |
| T-20260129-102 | 发布v0.3.4版本 | P0 | completed | 2026-01-29 | - |
| T-20260129-103 | 清理CLAUDE.md工具数量 | P0 | completed | 2026-01-29 | - |
| T-20260129-104 | 清理docs/README.md过时引用 | P0 | completed | 2026-01-29 | - |
| T-20260129-105 | 清理docs/ide-config.md过时引用 | P0 | completed | 2026-01-29 | - |
| T-20260129-106 | 清理docs/quick-start.md过时引用 | P0 | completed | 2026-01-29 | - |
| T-20260129-107 | 清理API文档过时引用 | P1 | completed | 2026-01-29 | - |
| T-20260129-108 | 删除无用代码PackageAgentSkillInput | P1 | completed | 2026-01-29 | - |
| T-20260129-109 | 删除validation_helpers.py模块 | P2 | completed | 2026-01-29 | - |
| T-20260129-110 | 更新所有测试徽章数量 | P0 | completed | 2026-01-29 | - |
| T-20260129-111 | 运行完整测试验证 | P1 | completed | 2026-01-29 | - |
| T-20260129-112 | 代码质量检查 | P1 | completed | 2026-01-29 | - |

---

## 四、任务详细说明

### T-20260129-101: 运行测试获取准确数量 (P0)

**目标**: 确认实际测试用例数量

**执行命令**:
```bash
cd /models/claude-glm/Skills-Creator/skill-creator-mcp
uv run pytest --collect-only -q 2>/dev/null | tail -1
```

**验收标准**:
- [ ] 获取准确的测试数量
- [ ] 记录到计划文档

---

### T-20260129-102: 发布v0.3.4版本 (P0)

**用户决策**: 发布v0.3.4

**执行步骤**:
1. 更新 `pyproject.toml` 版本号从 0.3.3 → 0.3.4
2. 更新 `src/skill_creator_mcp/__init__.py` 版本号（如有）
3. 保留 CHANGELOG.md 的 v0.3.4 条目
4. 提交正式发布 commit

**验收标准**:
- [ ] pyproject.toml 版本号为 0.3.4
- [ ] __init__.py 版本号为 0.3.4
- [ ] CHANGELOG.md v0.3.4 条目完整

---

### T-20260129-103: 清理CLAUDE.md工具数量 (P0)

**文件**: `/models/claude-glm/Skills-Creator/CLAUDE.md`

**问题位置**: 第1.5节 "MCP工具分类标准"

**需要修改的内容**:
```markdown
# 当前（错误）：
MCP Server提供13个工具，按功能划分为3类：
...
**总计**: 4 + 7 + 2 = 13个工具（1个别名，实际12个实现）

# 修改为（正确）：
MCP Server提供12个工具，按功能划分为3类：
| 类别 | 工具数量 | 工具列表 |
|------|----------|----------|
| **技能工具** | 4 | init_skill, validate_skill, analyze_skill, refactor_skill |
| **需求收集原子工具** | 7 | create_requirement_session, get_requirement_session, update_requirement_answer, get_static_question, generate_dynamic_question, validate_answer_format, check_requirement_completeness |
| **打包工具** | 1 | package_skill |
**总计**: 4 + 7 + 1 = 12个工具
```

**验收标准**:
- [ ] 工具数量从13改为12
- [ ] 删除package_agent_skill引用
- [ ] 删除"1个别名"的错误描述

---

### T-20260129-104: 清理docs/README.md过时引用 (P0)

**文件**: `skill-creator-mcp/docs/README.md`

**需要删除的行**:
- 第142行: `| `package_agent_skill` | 标准打包工具（推荐） |`
- 第148行: `| `batch_validate_skills_tool` | 批量验证多个 Agent-Skill |`
- 第149行: `| `batch_analyze_skills_tool` | 批量分析多个 Agent-Skill |`
- 第155行: `| `health_check_tool` | 完整健康检查 |`
- 第156行: `| `quick_status_tool` | 快速状态摘要 |`
- 第157行: `| `is_healthy_tool` | 快速健康检查 |`

**需要更新的内容**:
- 工具总数从18个改为12个
- 更新项目统计表格

**验收标准**:
- [ ] 所有已移除工具引用已删除
- [ ] 工具数量更新为12个

---

### T-20260129-105: 清理docs/ide-config.md过时引用 (P0)

**文件**: `skill-creator-mcp/docs/ide-config.md`

**需要清理的位置**:
- 第369行: package_agent_skill引用
- 第381-382行: 批量操作工具引用
- 第385-387行: 健康检查工具引用

**需要更新的内容**:
- 工具总数从18个改为12个

**验收标准**:
- [ ] 所有已移除工具引用已删除
- [ ] 工具数量更新为12个

---

### T-20260129-106: 清理docs/quick-start.md过时引用 (P0)

**文件**: `skill-creator-mcp/docs/quick-start.md`

**需要清理的位置**:
- 第237行: health_check使用示例
- 第260行: 工具分类表中的已移除工具
- 第262行: 批量操作工具引用

**需要更新的内容**:
- 工具总数从18个改为12个

**验收标准**:
- [ ] 所有已移除工具引用已删除
- [ ] 工具数量更新为12个

---

### T-20260129-107: 清理API文档过时引用 (P1)

**文件**:
1. `skill-creator-mcp/docs/api/index.rst`
   - 第32行: `.. autofunction:: skill_creator_mcp.server.package_agent_skill`
   - 第48-49行: 批量操作工具autofunction引用
   - 第54-56行: 健康检查工具autofunction引用
   - 第122行及以后: 相关说明文字

2. `skill-creator-mcp/docs/index.rst`
   - 第44-45行: 批量操作工具引用
   - 第49-51行: 健康检查工具引用

3. `skill-creator-mcp/docs/claude-code-config.md`
   - 第478行: package_agent_skill引用
   - 第490-496行: 批量操作和健康检查工具引用

4. `skill-creator-mcp/docs/troubleshooting.md`
   - 第288行: batch_validate_skills_tool使用示例

**验收标准**:
- [ ] API文档中所有autofunction引用已清理
- [ ] 所有工具列表已更新

---

### T-20260129-108: 删除无用代码PackageAgentSkillInput (P1)

**文件**: `skill-creator-mcp/src/skill_creator_mcp/models/skill_config.py`

**需要删除的内容**:
- 第500-539行: `PackageAgentSkillInput` 类定义（40行）

**理由**:
- `package_agent_skill` 工具已被移除
- 该模型未被任何代码使用
- grep搜索确认无引用

**验收标准**:
- [ ] PackageAgentSkillInput类已删除
- [ ] 代码检查通过（ruff + mypy）
- [ ] 测试通过

---

### T-20260129-109: 删除validation_helpers.py模块 (P2)

**用户决策**: 删除

**文件**: `skill-creator-mcp/src/skill_creator_mcp/tools/validation_helpers.py`

**执行步骤**:
1. 删除整个 validation_helpers.py 文件（92行）
2. 搜索确认无引用
3. 运行代码检查

**验收标准**:
- [ ] validation_helpers.py 已删除
- [ ] grep搜索无引用
- [ ] 代码检查通过（ruff + mypy）

---

### T-20260129-110: 更新所有测试徽章数量 (P0)

**需要更新的文件**:
1. `/models/claude-glm/Skills-Creator/README.md`
   - 测试徽章: 从613个改为实际数量

2. `/models/claude-glm/Skills-Creator/skill-creator-mcp/README.md`
   - 测试徽章: 从588个改为实际数量

**执行**:
- 先运行T-20260129-101获取准确数量
- 然后更新两个README.md的测试徽章

**验收标准**:
- [ ] 主README测试徽章准确
- [ ] skill-creator-mcp/README测试徽章准确
- [ ] 两个徽章数量一致

---

### T-20260129-111: 运行完整测试验证 (P1)

**执行命令**:
```bash
cd /models/claude-glm/Skills-Creator/skill-creator-mcp
uv run pytest --cov --cov-report=term-missing
```

**验收标准**:
- [ ] 所有测试通过
- [ ] 测试覆盖率 ≥95%
- [ ] 无失败或错误

---

### T-20260129-112: 代码质量检查 (P1)

**执行命令**:
```bash
cd /models/claude-glm/Skills-Creator/skill-creator-mcp
uv run ruff check .
uv run ruff format .
uv run mypy src/
```

**验收标准**:
- [ ] ruff 0错误
- [ ] mypy 0错误
- [ ] 代码格式正确

---

## 五、关键文件路径

### 需要修改的文件汇总

| 文件路径 | 修改类型 | 影响范围 |
|---------|---------|---------|
| `CLAUDE.md` | 更新 | 工具数量13→12 |
| `skill-creator-mcp/docs/README.md` | 删除+更新 | 删除6个已移除工具引用 |
| `skill-creator-mcp/docs/ide-config.md` | 删除+更新 | 删除6个已移除工具引用 |
| `skill-creator-mcp/docs/quick-start.md` | 删除+更新 | 删除6个已移除工具引用 |
| `skill-creator-mcp/docs/api/index.rst` | 删除 | autofunction引用 |
| `skill-creator-mcp/docs/index.rst` | 删除 | 工具列表引用 |
| `skill-creator-mcp/docs/claude-code-config.md` | 删除 | 工具列表引用 |
| `skill-creator-mcp/docs/troubleshooting.md` | 删除 | 使用示例 |
| `skill-creator-mcp/src/skill_creator_mcp/models/skill_config.py` | 删除 | PackageAgentSkillInput类 |
| `skill-creator-mcp/tools/validation_helpers.py` | 删除/使用 | 整个模块 |
| `README.md` | 更新 | 测试徽章 |
| `skill-creator-mcp/README.md` | 更新 | 测试徽章 |
| `pyproject.toml` | 更新（可选） | 版本号 |
| `CHANGELOG.md` | 更新（可选） | 版本号 |

---

## 六、验收标准

### 代码质量验收
- [ ] 实际测试数量确认
- [ ] 所有测试通过
- [ ] 代码质量检查通过（ruff 0错误, mypy 0错误）

### 文档一致性验收
- [ ] 所有文档工具数量统一为12个
- [ ] 所有文档测试徽章数量准确
- [ ] 所有文档版本号一致
- [ ] 所有已移除工具引用已删除

### 无用代码清理验收
- [ ] PackageAgentSkillInput已删除
- [ ] validation_helpers.py已处理
- [ ] grep搜索无残留引用

---

## 七、风险评估

| 风险 | 严重性 | 缓解措施 |
|------|--------|---------|
| 版本号不一致 | 中 | 确认策略后统一更新 |
| 文档同步遗漏 | 低 | 使用grep全局搜索逐一确认 |
| 删除有用代码 | 低 | grep确认无引用后再删除 |

---

## 八、进度追踪

**当前状态**: completed
**开始时间**: 2026-01-29
**任务完成进度**: 12/12 (100%)
**最近更新**: 2026-01-29

**实际测试数量**: 568个测试用例（566通过，2跳过）
**测试覆盖率**: 97%
**代码质量**: ruff 0错误，mypy 0错误

---

## 九、审核发现详情

### 9.1 工具数量不一致

| 文档 | 声称数量 | 实际数量 | 偏差 |
|------|----------|----------|------|
| CLAUDE.md | 13个 | 12个 | +1 |
| docs/README.md | 18个 | 12个 | +6 |
| docs/ide-config.md | 18个 | 12个 | +6 |
| docs/quick-start.md | 18个 | 12个 | +6 |

### 9.2 测试数量不一致

| 文档 | 声称数量 | 实际数量（待确认） |
|------|----------|-------------------|
| 主README.md | 613个 | 568个（预估） |
| skill-creator-mcp/README.md | 588个 | 568个（预估） |

### 9.3 过时引用统计

| 工具名称 | 引用次数 | 文件数量 |
|----------|----------|----------|
| package_agent_skill | 15+ | 8 |
| batch_validate_skills | 6+ | 5 |
| batch_analyze_skills | 6+ | 5 |
| health_check | 6+ | 5 |
| quick_status | 6+ | 5 |
| is_healthy | 6+ | 5 |

### 9.4 无用代码统计

| 代码项 | 位置 | 行数 | 状态 |
|--------|------|------|------|
| PackageAgentSkillInput | models/skill_config.py | 40 | 未使用 |
| validation_helpers模块 | tools/validation_helpers.py | 92 | 未使用 |

---

**计划状态**: planning → in_progress
**创建时间**: 2026-01-29
