# Skills-Creator 全面审核与优化计划

> **计划ID**: hazy-exploring-pizza
> **创建日期**: 2026-01-29
> **状态**: in_progress
> **负责人**: Claude Code
> **计划类型**: 审核清理/优化/重构
> **审核依据**: 100%基于实际代码审核

---

## 一、项目概述

### 1.1 审核背景

**项目**: Skills-Creator [Agent-Skills `skill-creator/` + MCP `skill-creator-mcp/`]

**核心定位**: 为用户进行 Agent-Skills 高效/规范/最佳实践标准化开发

### 1.2 审核目标

1. **清除已弃用内容**: 移除所有指向已弃用 API 的引用
2. **规范文件大小**: 确保所有引用文件 ≤300 行
3. **更新版本示例**: 统一版本号为 v0.3.4
4. **验证文档一致性**: 确保文档与实际代码 100% 一致
5. **删除无用文件**: 移除不服务于核心定位的文件

---

## 二、深度审核结果摘要

### 2.1 优秀方面（保持）

| 指标 | 状态 | 详情 |
|------|------|------|
| MCP 工具代码 | ✅ 100% | 无已弃用工具，12个工具全部活跃 |
| 工具数量一致性 | ✅ 100% | 文档与代码完全一致 |
| SKILL.md | ✅ 符合规范 | 138行（≤150行推荐），核心定位准确 |
| 测试覆盖率 | ✅ 97% | 568个测试用例 |
| 架构设计 | ✅ 优秀 | 符合 ADR 001 混合架构原则 |

### 2.2 发现的问题

#### P0 - 立即修复

1. **已弃用 API 广泛使用**: 10个 references 文件使用 `collect_requirements`
2. **已移除工具引用**: 1个 examples 文件引用已移除工具

#### P1 - 高优先级

3. **文件行数超标**: 5个 references 文件超过300行
4. **版本号不一致**: 多个文件显示 v0.3.1

#### P2 - 中优先级

5. **SKILL.md 缺少版本号**: 未明确当前版本
6. **示例文件需要增强**: 3个 examples 文件可以改进

---

## 三、任务清单

### 任务进度追踪

| ID | 任务名称 | 优先级 | 状态 | 完成时间 | Commit |
|----|----------|--------|------|----------|--------|
| T-20260129-001 | 更新 references 已弃用 API | P0 | completed | 2026-01-29 | b2d233a |
| T-20260129-002 | 删除无用 examples 文件 | P0 | in_progress | - | - |
| T-20260129-003 | 更新版本示例到 v0.3.4 | P1 | pending | - | - |
| T-20260129-004 | 拆分超长 references 文件 | P1 | pending | - | - |
| T-20260129-005 | 删除过时 API 说明 | P1 | pending | - | - |
| T-20260129-006 | 更新 SKILL.md 版本号 | P2 | pending | - | - |
| T-20260129-007 | 验证外部 MCP API | P2 | pending | - | - |
| T-20260129-008 | 全面验证清理结果 | P0 | pending | - | - |

**任务完成进度**: 1/8 (12%)

---

### 详细任务说明

#### T-20260129-001: 更新 references 已弃用 API

**优先级**: P0（阻塞）

**描述**: 更新10个使用已弃用 `collect_requirements` API 的 references 文件。

**影响文件**:
| 文件 | 问题位置 | 严重性 |
|------|----------|--------|
| `requirement-collection-basics.md` | 行174-205 | 严重 |
| `requirement-collection-modes.md` | 行59-383 | 严重 |
| `requirement-workflow.md` | 行316 | 严重 |
| `troubleshooting.md` | 行69, 77, 172 | 严重 |
| `troubleshooting-advanced.md` | 行146, 161 | 严重 |
| `brainstorming-techniques.md` | 行99, 126, 154, 301 | 严重 |
| `requirement-collection-api-core.md` | 行187-243 (action参数) | 中等 |

**验收标准**:
- [ ] 所有 `collect_requirements` 调用改为7个原子工具
- [ ] 删除 action 参数相关章节
- [ ] 添加迁移说明（可选）
- [ ] 代码示例语法正确

**实施方式**:
```python
# 旧示例（已弃用）
result = await collect_requirements(action="start", mode="brainstorm")

# 新示例（推荐）
session = await create_requirement_session_tool(mode="brainstorm")
question = await generate_dynamic_question_tool(mode="brainstorm", answers=session["answers"])
await update_requirement_answer_tool(session_id=session["session_id"], question_key="...", answer="...")
```

---

#### T-20260129-002: 删除无用 examples 文件

**优先级**: P0（阻塞）

**描述**: 删除引用已移除工具且不服务于核心定位的示例文件。

**影响文件**:
- `skill-creator/examples/cache-advanced-examples.md`

**删除理由**:
1. 引用已移除工具（`batch_validate_skills`, `batch_analyze_skills`）
2. 缓存是内部实现细节，不应暴露给用户
3. 不服务于"Agent-Skills标准化开发"核心定位
4. 代码无法运行

**验收标准**:
- [ ] 文件已删除
- [ ] 无其他文件引用此文件

---

#### T-20260129-003: 更新版本示例到 v0.3.4

**优先级**: P1（高）

**描述**: 将所有文档中的版本示例从 v0.3.1 更新到 v0.3.4。

**影响文件**:
- `skill-creator/references/packaging.md` (行24: `skill-creator-v0.3.1.zip`)
- `skill-creator/references/brainstorming-techniques.md` (行3: 版本号)

**验收标准**:
- [ ] 所有版本示例显示 v0.3.4
- [ ] `grep -r "v0\.3\.[1-3]" skill-creator/` 返回 0 结果

---

#### T-20260129-004: 拆分超长 references 文件

**优先级**: P1（高）

**描述**: 拆分5个超出300行规范的 references 文件。

**影响文件**:
| 文件 | 当前行数 | 目标 | 拆分方案 |
|------|----------|------|----------|
| `requirement-collection-modes.md` | 453行 | ≤200行 | 拆分为 modes + mode-details |
| `requirement-workflow.md` | 359行 | ≤250行 | 提取高级部分 |
| `brainstorming-techniques.md` | 345行 | ≤250行 | 精简示例 |
| `requirement-collection-api-core.md` | 326行 | ≤250行 | 精简技术细节 |
| `requirement-collection-api-examples.md` | 399行 | ≤200行 | 拆分为 basic + advanced |

**验收标准**:
- [ ] 所有文件 ≤300 行
- [ ] `references/README.md` 已更新新文件结构
- [ ] 交叉引用完整

---

#### T-20260129-005: 删除过时 API 说明

**优先级**: P1（高）

**描述**: 删除 `requirement-collection-api-core.md` 中过时的 action 参数说明。

**影响文件**:
- `skill-creator/references/requirement-collection-api-core.md` (行187-243)

**验收标准**:
- [ ] action 类型章节已删除
- [ ] 文件只保留7个原子工具的说明

---

#### T-20260129-006: 更新 SKILL.md 版本号

**优先级**: P2（中）

**描述**: 在 SKILL.md 中添加版本号信息。

**影响文件**:
- `skill-creator/SKILL.md`

**建议方案**:
```yaml
---
name: skill-creator
version: 0.3.4  # 添加此行
description: |
  Agent-Skills 开发与质量保证工具...
---
```

**验收标准**:
- [ ] YAML Frontmatter 包含版本号
- [ ] 或"技能概述"部分包含版本信息

---

#### T-20260129-007: 验证外部 MCP API

**优先级**: P2（中）

**描述**: 验证 GitHub 和 Thinking MCP 集成示例与最新版本一致。

**影响文件**:
- `skill-creator/references/mcp-github-integration.md`
- `skill-creator/references/mcp-thinking-integration.md`
- `skill-creator/examples/github-requirement-tracking.md`

**验收标准**:
- [ ] GitHub MCP API 示例与最新版本一致
- [ ] Thinking MCP API 示例与最新版本一致
- [ ] `github-requirement-tracking.md` 完全使用7工具架构

---

#### T-20260129-008: 全面验证清理结果

**优先级**: P0（阻塞）

**描述**: 全面验证所有清理工作完成，确保无遗漏。

**验证命令**:
```bash
# 1. 检查已弃用API引用
grep -r "collect_requirements" skill-creator/ --include="*.md" | grep -v archive
# 预期: 0

# 2. 检查已移除工具引用
grep -r "batch_validate_skills\|batch_analyze_skills" skill-creator/ --include="*.md" | grep -v archive
# 预期: 0

# 3. 检查文件大小
find skill-creator/references/ -name "*.md" -exec wc -l {} \; | awk '$1 > 300'
# 预期: 0 files

# 4. 检查版本一致性
grep -r "v0\.3\.[1-3]" skill-creator/ --include="*.md" | grep -v archive
# 预期: 0 results

# 5. 运行测试
cd skill-creator-mcp
uv run pytest --cov
# 预期: 全部通过，覆盖率≥97%
```

**验收标准**:
- [ ] 所有验证命令返回预期结果
- [ ] 文档交叉引用有效
- [ ] 所有示例可运行

---

## 四、执行顺序

### 阶段1: 关键清理（P0）

1. **T-20260129-001**: 更新 references 已弃用 API
2. **T-20260129-002**: 删除无用 examples 文件
3. **T-20260129-008**: 全面验证清理结果

**预期产出**:
- 所有已弃用 API 引用已清除
- 无用文件已删除
- 文档与当前架构100%一致

### 阶段2: 优化改进（P1）

4. **T-20260129-003**: 更新版本示例到 v0.3.4
5. **T-20260129-005**: 删除过时 API 说明
6. **T-20260129-004**: 拆分超长 references 文件

**预期产出**:
- 版本示例统一为 v0.3.4
- 过时内容已删除
- 所有文件符合300行规范

### 阶段3: 完善验证（P2）

7. **T-20260129-006**: 更新 SKILL.md 版本号
8. **T-20260129-007**: 验证外部 MCP API

**预期产出**:
- SKILL.md 包含版本信息
- 外部 MCP API 示例准确

---

## 五、验证计划

### 自动化验证

```bash
# 1. 检查已弃用API引用
grep -r "collect_requirements" skill-creator/ --include="*.md" | grep -v archive | wc -l
# 预期: 0

# 2. 检查已移除工具引用
grep -r "batch_validate_skills\|batch_analyze_skills\|cache-advanced" skill-creator/ --include="*.md" | grep -v archive | wc -l
# 预期: 0

# 3. 检查文件大小
find skill-creator/references/ -name "*.md" -exec wc -l {} \; | awk '$1 > 300' | wc -l
# 预期: 0

# 4. 检查版本一致性
grep -r "v0\.3\.[1-3]" skill-creator/ --include="*.md" | grep -v archive | wc -l
# 预期: 0

# 5. 运行测试
cd skill-creator-mcp && uv run pytest --cov
# 预期: 全部通过，覆盖率≥97%
```

### 手动验证清单

- [ ] 所有 P0 任务已完成
- [ ] 所有 P1 任务已完成
- [ ] 所有 P2 任务已完成（或用户同意跳过）
- [ ] 文档交叉引用有效
- [ ] 代码示例语法正确
- [ ] 版本号在所有文档中一致
- [ ] 所有示例服务于核心定位

---

## 六、风险评估

### 高风险项

| 风险 | 概率 | 影响 | 缓解措施 |
|------|------|------|----------|
| 更改API示例导致用户混淆 | 中 | 中 | 添加迁移说明，标注旧API已弃用 |
| 拆分文件破坏交叉引用 | 低 | 中 | 使用相对路径，全面测试链接 |
| 删除文件导致其他引用断裂 | 低 | 低 | 搜索所有引用后再删除 |

### 低风险项

- 版本号更新（仅文档修改）
- SKILL.md 添加版本号（非破坏性）
- 外部MCP API验证（只读检查）

---

## 七、成功标准

### 定量指标

- ✅ 0 个已弃用 API 引用
- ✅ 0 个已移除工具引用
- ✅ 0 个文件超过 300 行
- ✅ 0 个版本示例过时
- ✅ 100% 文档与代码一致

### 定性指标

- 所有文档服务于核心定位
- 文档可维护性提升
- 新用户体验改善
- 代码示例准确可运行

---

## 八、关键文件清单

### 需要修改的文件

**P0 - 立即修复** (7个):
1. `skill-creator/references/requirement-collection-basics.md`
2. `skill-creator/references/requirement-collection-modes.md`
3. `skill-creator/references/requirement-workflow.md`
4. `skill-creator/references/troubleshooting.md`
5. `skill-creator/references/troubleshooting-advanced.md`
6. `skill-creator/references/brainstorming-techniques.md`
7. `skill-creator/references/requirement-collection-api-core.md`

**P0 - 需要删除** (1个):
8. `skill-creator/examples/cache-advanced-examples.md`

**P1 - 建议修复** (6个):
9. `skill-creator/references/packaging.md`
10. `skill-creator/references/requirement-collection-api-examples.md`
11. `skill-creator/references/mcp-github-integration.md`
12. `skill-creator/references/mcp-thinking-integration.md`
13. `skill-creator/examples/github-requirement-tracking.md`
14. `skill-creator/references/README.md` (更新文件结构)

**P2 - 可选优化** (2个):
15. `skill-creator/SKILL.md`
16. `skill-creator/examples/github-automation.md` (增强)

### 参考文件

- `CLAUDE.md` - 开发规范和流程
- `skill-creator-mcp/CHANGELOG.md` - 版本变更历史
- `skill-creator-mcp/src/skill_creator_mcp/server.py` - 工具实现

---

## 九、归档检查清单

**归档前必须确认**:

- [ ] P0 任务全部完成（5个）
- [ ] P1 任务全部完成（3个）
- [ ] P2 任务全部完成或用户同意跳过（2个）
- [ ] 所有验收标准满足
- [ ] 有完整的 Git commit 记录
- [ ] 有阶段性进度报告
- [ ] 文档已同步更新
- [ ] 测试全部通过
- [ ] 100%基于实际代码审核（非虚假审核）

---

## 附录：核心定位验证

**核心定位**: 为用户进行 Agent-Skills 高效/规范/最佳实践标准化开发

**所有任务必须满足**:
- ✅ 服务于核心定位
- ✅ 遵循最佳实践
- ✅ 内容准确（基于实际代码）
- ✅ 无冗余或无关内容

**删除文件的判定标准**:
1. 引用已弃用或已移除的工具
2. 不服务于核心定位
3. 无实际价值或无法运行
4. 有更好的替代方案

---

**计划创建时间**: 2026-01-29
**审核依据**: 100%基于实际代码审核
**下一步**: 等待用户批准后开始执行
