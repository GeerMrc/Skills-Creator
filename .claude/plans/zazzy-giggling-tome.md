# MCP skill-creator-mcp 与 Agent-Skill skill-creator 全面审核与修复

> **计划类型**: 全面审核与修复
> **创建日期**: 2026-01-29
> **状态**: in_progress
> **计划优先级**: P0

---

## 一、审核目标

### 1.1 核心目标

根据 Skills-Creator 项目核心定位，对 **MCP `skill-creator-mcp/`** 和 **Agent-Skill `skill-creator/`** 进行全面系统性审核：

1. **功能定位审核**：确认功能是否准确服务于 Agent-Skills 开发
2. **功能完整性审核**：验证功能实现是否完整
3. **文档一致性审核**：确保所有文档与最新项目代码保持一致
4. **示例文档审核**：检查并清理过时/不可用的示例
5. **代码清理审核**：检查并清理旧的测试代码/重复性/无用已弃用代码

### 1.2 项目核心定位

> **Skills-Creator** 核心定位：为用户进行 Agent-Skills 高效/规范/最佳实践标准化开发

**关键原则**:
- Agent-Skill `skill-creator/` 和 MCP `skill-creator-mcp/` 都服务于这个目标
- 调用外部 MCP（GitHub、Thinking）仅为更好地实现 Agent-Skills 标准化开发

### 1.3 实际 MCP 工具清单（12个）

| 类别 | 工具名 | 状态 |
|------|--------|------|
| **技能工具 (4)** | init_skill_tool | ✅ |
| | validate_skill_tool | ✅ |
| | analyze_skill_tool | ✅ |
| | refactor_skill_tool | ✅ |
| **需求收集 (7)** | create_requirement_session_tool | ✅ |
| | get_requirement_session_tool | ✅ |
| | update_requirement_answer_tool | ✅ |
| | get_static_question_tool | ✅ |
| | generate_dynamic_question_tool | ✅ |
| | validate_answer_format_tool | ✅ |
| | check_requirement_completeness_tool | ✅ |
| **打包工具 (1)** | package_skill | ✅ |

**MCP 组件总计**: 12 工具 + 4 资源 + 3 Prompts

---

## 二、审核发现汇总

### 2.1 版本号不一致问题 (P0)

| 文件 | 当前版本 | 实际版本 | 状态 |
|------|----------|----------|------|
| `skill-creator-mcp/README.md:26,52` | v0.3.3 | v0.3.4 | ❌ |
| `CLAUDE.md:36` | v0.3.3 | v0.3.4 | ❌ |

### 2.2 工具数量描述不一致 (P0)

| 文档位置 | 声称数量 | 实际数量 | 状态 |
|----------|----------|----------|------|
| `SKILL.md:89` | 18个工具 | 12个工具 | ❌ |
| `SKILL.md:133` | 18 工具 | 12个工具 | ❌ |
| `CLAUDE.md:56` | 13 Tools | 12个工具 | ❌ |

### 2.3 测试用例数量不一致 (P0)

| 文档 | 声称数量 | 实际数量 | 状态 |
|------|----------|----------|------|
| `CLAUDE.md:38` | 588个测试用例 | 568个测试用例 | ❌ |

### 2.4 SKILL.md 中已移除功能引用 (P0)

| 位置 | 内容 | 状态 |
|------|------|------|
| 第19-20行 | 触发词: 批量验证、批量分析 | ❌ 需删除 |
| 第24-25行 | 触发词: 健康检查、系统监控 | ❌ 需删除 |
| 第38行 | 核心能力: 批量操作、健康检查 | ❌ 需删除 |
| 第46-47行 | 快速开始: 批量操作、健康检查 | ❌ 需删除 |
| 第50行 | 引用过时示例文档链接 | ❌ 需更新 |

### 2.5 示例文档严重问题 (P0)

| 文件 | 问题描述 | 严重程度 |
|------|----------|----------|
| `examples/mcp-batch-operations.md` (286行) | 引用不存在的批量工具（13处） | **严重** |
| `examples/mcp-health-check.md` (303行) | 引用不存在的健康检查工具（12处） | **严重** |
| `examples/packaging-basic.md` | 使用已弃用 package_agent_skill (27处) | **严重** |
| `examples/packaging-advanced.md` | 使用已弃用 package_agent_skill | **严重** |
| `examples/cache-advanced-examples.md:51` | 引用批量工具 | **中等** |
| `examples/README.md` | 索引引用过时示例 | **中等** |

### 2.6 引用文档问题 (P1)

| 文件 | 问题描述 | 状态 |
|------|----------|------|
| `references/mcp-integration.md:48` | 引用 package_agent_skill | ❌ |
| `references/packaging.md` | 可能引用已弃用函数 | ⚠️ 待验证 |

### 2.7 无效文档链接 (P1)

| 位置 | 问题链接 | 实际位置 |
|------|----------|----------|
| `examples/mcp-skill-collaboration.md:176` | `../references/architecture.md` | `../../docs/adr/001-hybrid-architecture.md` |
| `examples/requirement-collection-basic.md:76` | `../references/fallback-mechanism.md` | 不存在 |

### 2.8 MCP 文档问题 (P1)

| 文件 | 问题描述 | 状态 |
|------|----------|------|
| `skill-creator-mcp/docs/README.md:181` | package_agent_skill 引用 | ❌ |
| `skill-creator-mcp/docs/api/index.rst:108` | package_agent_skill 引用 | ❌ |
| `skill-creator-mcp/docs/index.rst:30` | package_agent_skill 引用 | ❌ |

### 2.9 测试代码问题 (P2)

| 文件 | 问题描述 | 状态 |
|------|----------|------|
| `tests/test_integration/test_e2e_workflow.py` | 函数名使用 collect_requirements | ⚠️ 建议重命名 |

### 2.10 代码质量评估 (✅ 良好)

| 评估项 | 结果 |
|--------|------|
| 功能定位 | ✅ 准确 - 所有工具服务于 Agent-Skills 开发 |
| 重复代码 | ✅ 无 |
| 孤立模块 | ✅ 无 |
| 弃用代码清理 | ✅ 良好 - package_agent_skill 已从代码中移除 |
| Phase 0工具处理 | ✅ 正确 - 已迁移到 dev-tools.py |

---

## 三、修复计划

### 3.1 P0 任务（高优先级 - 必须完成）

#### T-001: 修正版本号不一致
**文件**:
- `skill-creator-mcp/README.md` (第26, 52行)
- `CLAUDE.md` (第36行)

**修复**: v0.3.3 → v0.3.4

---

#### T-002: 修正工具数量描述不一致
**文件**:
- `SKILL.md` (第89行标题)
- `SKILL.md` (第133行)
- `CLAUDE.md` (第56行)

**修复**: 18/13 → 12个工具

---

#### T-003: 移除 SKILL.md 中已移除功能的引用
**文件**: `skill-creator/SKILL.md`

**修复内容**:
1. 删除触发词中的 "批量验证"、"批量分析"、"健康检查"、"系统监控"
2. 删除核心能力中的 "批量操作"、"健康检查"
3. 删除快速开始中的 "批量操作"、"健康检查" 示例
4. 更新示例文档链接

---

#### T-004: 修正测试用例数量
**文件**: `CLAUDE.md` (第38行)

**修复**: 588 → 568个测试用例

---

#### T-005: 删除过时的示例文档
**文件**:
- `examples/mcp-batch-operations.md` (286行)
- `examples/mcp-health-check.md` (303行)

**操作**: 删除这两个文件，因为它们引用的工具已不存在

---

#### T-006: 更新示例索引
**文件**: `examples/README.md`

**修复**: 移除对已删除示例的引用

---

#### T-007: 更新打包示例中的已弃用函数
**文件**:
- `examples/packaging-basic.md`
- `examples/packaging-advanced.md`

**修复**: `package_agent_skill` → `package_skill` (添加 `strict=True` 参数)

---

#### T-008: 修复无效文档链接
**文件**:
- `examples/mcp-skill-collaboration.md`
- `examples/requirement-collection-basic.md`

**修复**: 更新为正确的链接路径

---

### 3.2 P1 任务（中优先级）

#### T-009: 更新 MCP 文档中的已弃用工具引用
**文件**:
- `skill-creator-mcp/docs/README.md`
- `skill-creator-mcp/docs/api/index.rst`
- `skill-creator-mcp/docs/index.rst`

**修复**: `package_agent_skill` → `package_skill`

---

#### T-010: 更新引用文档
**文件**:
- `references/mcp-integration.md`
- `references/packaging.md` (如需要)

**修复**: 移除或更新 `package_agent_skill` 引用

---

#### T-011: 修复缓存示例
**文件**: `examples/cache-advanced-examples.md`

**修复**: 移除或更新批量工具引用

---

### 3.3 P2 任务（低优先级）

#### T-012: 重命名测试函数
**文件**: `tests/test_integration/test_e2e_workflow.py`

**修复**: `test_collect_requirements_*` → `test_requirement_collection_*`

---

#### T-013: 验证功能定位
**验证内容**:
- 确认所有 12 个工具都服务于 Agent-Skills 开发
- 确认 4 个资源和 3 个 Prompts 符合核心定位

---

#### T-014: 交叉验证修复结果
**验证内容**:
- 运行所有测试
- 检查文档链接有效性
- 验证版本号和工具数量一致性
- 验证 MCP Server 可正常启动

---

## 四、文件清单

### 4.1 需要修改的文件

| 优先级 | 文件路径 | 修改类型 |
|--------|----------|----------|
| P0 | `skill-creator-mcp/README.md` | 版本号 |
| P0 | `skill-creator/SKILL.md` | 工具数量、移除旧功能引用 |
| P0 | `CLAUDE.md` | 版本号、工具数量、测试数量 |
| P0 | `examples/mcp-batch-operations.md` | **删除** |
| P0 | `examples/mcp-health-check.md` | **删除** |
| P0 | `examples/README.md` | 更新索引 |
| P0 | `examples/packaging-basic.md` | 更新函数调用 |
| P0 | `examples/packaging-advanced.md` | 更新函数调用 |
| P0 | `examples/mcp-skill-collaboration.md` | 修复链接 |
| P0 | `examples/requirement-collection-basic.md` | 修复链接 |
| P1 | `skill-creator-mcp/docs/README.md` | 更新引用 |
| P1 | `skill-creator-mcp/docs/api/index.rst` | 更新引用 |
| P1 | `skill-creator-mcp/docs/index.rst` | 更新引用 |
| P1 | `references/mcp-integration.md` | 更新引用 |
| P1 | `examples/cache-advanced-examples.md` | 移除批量工具引用 |
| P2 | `tests/test_integration/test_e2e_workflow.py` | 函数重命名 |

### 4.2 无需修改的文件（已验证）

- `skill-creator-mcp/pyproject.toml` - 版本号正确
- `skill-creator-mcp/src/skill_creator_mcp/__init__.py` - 版本号正确
- `skill-creator-mcp/src/skill_creator_mcp/server.py` - 工具注册正确
- `skill-creator/scripts/*.py` - 脚本功能正常

---

## 五、验收标准

### 5.1 功能定位验收

- [ ] 所有 12 个 MCP 工具都服务于 Agent-Skills 开发
- [ ] 4 个资源和 3 个 Prompts 符合核心定位
- [ ] 无描述不存在功能的文档

### 5.2 文档一致性验收

- [ ] 所有文档版本号统一为 v0.3.4
- [ ] 所有文档工具数量统一为 12 个
- [ ] 所有文档测试数量统一为 568 个
- [ ] 无已移除功能的引用
- [ ] 无已弃用函数的引用

### 5.3 示例文档验收

- [ ] 所有示例代码可运行
- [ ] 无引用不存在 MCP 工具的示例
- [ ] 示例索引准确

### 5.4 代码质量验收

- [ ] 所有测试通过 (pytest --cov)
- [ ] 无代码检查错误 (ruff check, mypy)
- [ ] MCP Server 可正常启动

### 5.5 文档链接验收

- [ ] 所有内部链接有效
- [ ] 无 404 链接

---

## 六、进度追踪

| 状态 | 开始时间 | 任务完成 | 进度 |
|------|----------|----------|------|
| planning | 2026-01-29 | 0/14 | 0% |

**最近更新**: 2026-01-29

---

## 七、任务清单

| ID | 任务描述 | 优先级 | 状态 | 完成时间 | Commit |
|----|----------|--------|------|----------|--------|
| T-001 | 修正版本号不一致 | P0 | pending | - | - |
| T-002 | 修正工具数量描述 | P0 | pending | - | - |
| T-003 | 移除 SKILL.md 旧功能引用 | P0 | pending | - | - |
| T-004 | 修正测试用例数量 | P0 | pending | - | - |
| T-005 | 删除过时示例文档 | P0 | pending | - | - |
| T-006 | 更新示例索引 | P0 | pending | - | - |
| T-007 | 更新打包示例 | P0 | pending | - | - |
| T-008 | 修复无效链接 | P0 | pending | - | - |
| T-009 | 更新 MCP 文档引用 | P1 | pending | - | - |
| T-010 | 更新引用文档 | P1 | pending | - | - |
| T-011 | 修复缓存示例 | P1 | pending | - | - |
| T-012 | 重命名测试函数 | P2 | pending | - | - |
| T-013 | 验证功能定位 | P2 | pending | - | - |
| T-014 | 交叉验证修复结果 | P2 | pending | - | - |

---

## 八、参考文档

- `CLAUDE.md` - 项目开发指南
- `CHANGELOG.md` - 版本变更记录
- `skill-creator-mcp/README.md` - MCP Server 文档
- `skill-creator/SKILL.md` - Agent-Skill 文档
- `docs/adr/001-hybrid-architecture.md` - 架构设计文档

---

## 九、归档检查清单

- [ ] P0 任务全部完成
- [ ] P1 任务全部完成
- [ ] P2 任务全部完成（或用户同意跳过）
- [ ] 所有验收标准满足
- [ ] 有完整的 Git commit 记录
- [ ] 有阶段性进度报告
- [ ] 未完成任务已处理（迁移或取消）
