# skill-creator 内容优化重构计划

**计划日期**: 2026-01-30
**计划类型**: refactor
**当前分支**: develop
**预估时间**: 3-4小时
**审核依据**: 100%基于实际代码内容审核

---

## 一、问题诊断

### 1.1 审核概述

| 审核项 | 状态 | 说明 |
|--------|------|------|
| 目录结构 | ✅ | 清晰，符合 Agent-Skill 规范 |
| SKILL.md | ✅ | 136行，符合≤150行标准 |
| 引用链接 | ✅ | 所有12个引用链接有效 |
| 内容重复 | ⚠️ | 发现多处重复内容 |
| 外部MCP占比 | ⚠️ | GitHub+Thinking占23% |
| 定位偏离 | ✅ | 有明确定位说明 |

### 1.2 发现的问题

#### P0 优先级问题（必须修复）

| 问题ID | 问题描述 | 影响 | 预计减少行数 |
|--------|----------|------|-------------|
| P0-1 | Requirement Collection 文档重复 | 用户阅读重复内容，增加认知负荷 | ~100-150行 |
| P0-2 | Thinking 示例文件过多（7个） | 占比过高，可能造成误解 | ~500行 |

#### P1 优先级问题（建议修复）

| 问题ID | 问题描述 | 影响 | 预计减少行数 |
|--------|----------|------|-------------|
| P1-1 | MCP 集成内容分散重复 | 内容分散，难以导航 | ~100行 |
| P1-2 | mcp-integration-guide.md 过长（323行） | 超过推荐的300行 | ~30行 |
| P1-3 | 最佳实践文档存在交叉引用 | 可能造成循环阅读 | - |

#### P2 优先级问题（可选修复）

| 问题ID | 问题描述 | 影响 |
|--------|----------|------|
| P2-1 | packaging-advanced.md 过长（334行） | 可考虑拆分 |

### 1.3 定位符合性分析

**核心定位**: 为用户进行 Agent-Skills 高效/规范/最佳实践标准化开发

**符合性评估**:
- ✅ 所有内容服务于 Agent-Skills 开发
- ✅ 外部 MCP 集成有明确"示范案例"定位
- ⚠️ 外部 MCP 内容占比略高（23%），需优化平衡

---

## 二、修复方案

### 2.1 P0-1: Requirement Collection 文档整合

**当前状态**:
- `requirement-collection.md` (106行) - 导航/概览
- `requirement-collection-basics.md` (227行) - 核心概念 + 架构
- `requirement-workflow.md` (278行) - 工作流实践

**重复内容**:
- 7个原子工具说明在多处重复
- 架构说明在 basics 和 workflow 中重复
- 模式对比表重复出现

**修复方案**:
1. 保持 `requirement-collection.md` 作为纯导航/索引
2. 将 `requirement-collection-basics.md` 的概念内容合并到 `requirement-collection.md`
3. 保持 `requirement-workflow.md` 专注于实践工作流
4. 删除重复的架构说明

**预期效果**: 减少 ~100-150行重复内容

### 2.2 P0-2: Thinking 示例合并

**当前状态**:
- `examples/thinking/` 目录下7个文件，共1,470行
- 占 examples 总文件数的25%

**文件列表**:
1. `README.md` (54行) - 索引
2. `analysis-basic.md` (238行)
3. `analysis-advanced.md` (270行)
4. `analysis-workflow.md` (244行)
5. `export-formats.md` (252行)
6. `export-workflow.md` (150行)
7. `export-automation.md` (262行)

**修复方案**:
合并为3个文件:
1. `README.md` - 索引和概述（保持）
2. `thinking-analysis.md` - 合并 basic + advanced + workflow（~400行）
3. `thinking-export.md` - 合并 formats + workflow + automation（~350行）

**预期效果**: 减少 ~500行，同时保持完整信息

### 2.3 P1-1: MCP 集成内容整合

**当前状态**:
- `mcp-integration-guide.md` (323行) - 方法论
- `mcp-github-integration.md` (170行) - GitHub示范
- `mcp-thinking-integration.md` (240行) - Thinking示范
- `examples/mcp-integration-example.md` (262行) - 通用示例

**修复方案**:
1. 保持 `mcp-integration-guide.md` 作为纯方法论
2. 将通用配置模式提取到 guide，从具体文档中引用
3. 合并重复的"集成收益"分析表格

**预期效果**: 减少 ~100行重复内容

### 2.4 P1-2: mcp-integration-guide.md 精简

**当前状态**: 323行，超过推荐的300行

**修复方案**:
1. 精简冗长的示例代码
2. 将部分详细内容移到 examples
3. 保持核心方法论清晰

**预期效果**: 减少到 <300行

### 2.5 P1-3: 最佳实践交叉引用优化

**当前状态**:
- `best-practices-core.md` 和 `best-practices-advanced.md` 存在交叉引用

**修复方案**:
1. 保持架构解释只在 `best-practices-core.md`
2. 在 `best-practices-advanced.md` 中使用简要引用而非重述
3. 确保单向引用（core → advanced）

---

## 三、验收标准

### 3.1 内容质量验收

| 验收项 | 标准 | 验证方法 |
|--------|------|----------|
| 重复内容消除 | 无明显重复 | 人工审核 |
| 文件行数合理 | 单文件 ≤300行（特殊情况除外） | 脚本统计 |
| 引用链接有效 | 100%有效 | 自动检查 |
| 定位符合性 | 外部MCP占比 <20% | 统计分析 |

### 3.2 文档完整性验收

| 验收项 | 标准 |
|--------|------|
| SKILL.md | ≤150行，引用有效 |
| references/README.md | 索引准确，行数更新 |
| examples/README.md | 索引准确，行数更新 |
| 交叉引用 | 无循环引用 |

### 3.3 用户体验验收

| 验收项 | 标准 |
|--------|------|
| 信息密度 | 无冗余重复内容 |
| 导航便利性 | 可通过索引快速定位 |
| 渐进式披露 | 概述→详细→高级，层次清晰 |

---

## 四、关键文件路径

### 4.1 需要修改的文件

**P0 优先级**:
- `skill-creator/references/requirement-collection.md`
- `skill-creator/references/requirement-collection-basics.md`（可能删除）
- `skill-creator/references/requirement-workflow.md`
- `skill-creator/examples/thinking/` 目录（7个文件合并为3个）

**P1 优先级**:
- `skill-creator/references/mcp-integration-guide.md`
- `skill-creator/references/best-practices-core.md`
- `skill-creator/references/best-practices-advanced.md`
- `skill-creator/references/mcp-github-integration.md`
- `skill-creator/references/mcp-thinking-integration.md`

**需要更新索引**:
- `skill-creator/references/README.md`
- `skill-creator/examples/README.md`

### 4.2 验证脚本路径

- `skill-creator-mcp/scripts/dev-tools.py` - 文件统计工具

---

## 五、执行步骤

### 阶段一：准备工作

**T-20260130-01** (P0): 确认当前分支和代码状态
- 验证当前在 `develop` 分支
- 确认 `git status` 干净
- 如需要，同步最新代码

**T-20260130-02** (P0): 备份当前 skill-creator 目录
- 创建备份分支
- 或使用 git stash 保存当前状态

### 阶段二：P0 任务执行

**T-20260130-03** (P0): 整合 Requirement Collection 文档
- 读取并分析 `requirement-collection.md`
- 读取并分析 `requirement-collection-basics.md`
- 读取并分析 `requirement-workflow.md`
- 合并内容，消除重复
- 更新交叉引用
- 更新 `references/README.md`

**T-20260130-04** (P0): 合并 Thinking 示例文件
- 读取 `examples/thinking/` 下所有7个文件
- 合并为 `thinking-analysis.md` 和 `thinking-export.md`
- 更新 `thinking/README.md`
- 更新 `examples/README.md`
- 验证内容完整性

**T-20260130-05** (P0): 验证 P0 修改效果
- 运行文件统计脚本
- 检查引用链接有效性
- 人工审核内容质量
- 提交 commit

### 阶段三：P1 任务执行

**T-20260130-06** (P1): 精简 mcp-integration-guide.md
- 分析当前内容结构
- 识别可精简的部分
- 重写精简版本
- 验证信息完整性

**T-20260130-07** (P1): 整合 MCP 集成内容
- 分析重复的配置模式
- 提取通用模式到 guide
- 更新具体集成文档
- 消除重复的"收益"表格

**T-20260130-08** (P1): 优化最佳实践交叉引用
- 检查 `best-practices-core.md` 和 `best-practices-advanced.md`
- 确保架构解释只在 core
- 优化 advanced 中的引用方式
- 确保单向引用

**T-20260130-09** (P1): 验证 P1 修改效果
- 运行文件统计脚本
- 检查引用链接有效性
- 人工审核内容质量
- 提交 commit

### 阶段四：最终验证

**T-20260130-10** (P0): 全面验收测试
- 统计优化后的文件行数
- 验证外部 MCP 内容占比 <20%
- 验证所有引用链接有效
- 验证无循环引用
- 生成优化报告

---

## 六、进度追踪

| 任务ID | 任务名称 | 优先级 | 状态 | 完成时间 | Commit |
|--------|----------|--------|------|----------|--------|
| T-20260130-01 | 确认分支和代码状态 | P0 | pending | - | - |
| T-20260130-02 | 备份当前目录 | P0 | pending | - | - |
| T-20260130-03 | 整合 Requirement Collection 文档 | P0 | pending | - | - |
| T-20260130-04 | 合并 Thinking 示例文件 | P0 | pending | - | - |
| T-20260130-05 | 验证 P0 修改效果 | P0 | pending | - | - |
| T-20260130-06 | 精简 mcp-integration-guide.md | P1 | pending | - | - |
| T-20260130-07 | 整合 MCP 集成内容 | P1 | pending | - | - |
| T-20260130-08 | 优化最佳实践交叉引用 | P1 | pending | - | - |
| T-20260130-09 | 验证 P1 修改效果 | P1 | pending | - | - |
| T-20260130-10 | 全面验收测试 | P0 | pending | - | - |

**当前状态**: planning
**任务完成进度**: 0/10 (0%)
**下一阶段**: T-20260130-01 确认分支和代码状态

---

## 七、风险与应对

| 风险 | 影响 | 概率 | 应对措施 |
|------|------|------|----------|
| 内容丢失风险 | 高 | 低 | 事先备份，git commit |
| 引用链接失效 | 中 | 中 | 修改后统一验证 |
| 信息不完整 | 中 | 低 | 合并时人工审核 |
| 争议性决策 | 低 | 中 | 与用户确认 |

---

## 八、归档检查清单

### 计划完成条件

> **强制要求**: 遵循规范的开发流程，计划内所有任务必须全部执行完成才可以归档。不允许跳过任何任务。

**必须完成**:
- [ ] T-20260130-01 ~ T-20260130-05 (P0任务) 全部完成
- [ ] T-20260130-06 ~ T-20260130-09 (P1任务) 全部完成
- [ ] T-20260130-10 (验收测试) 完成

**验收标准满足**:
- [ ] 重复内容已消除
- [ ] 文件行数合理（≤300行）
- [ ] 引用链接100%有效
- [ ] 外部MCP占比 <20%

**文档已更新**:
- [ ] references/README.md 索引准确
- [ ] examples/README.md 索引准确
- [ ] SKILL.md 引用有效

**Git提交记录**:
- [ ] 每阶段有规范的commit
- [ ] commit信息清晰描述变更

---

## 九、附录

### A. 审核方法论

本次审核基于：
1. 100%实际代码内容审核（非文档摘要）
2. 文件大小、行数、内容完整性分析
3. 交叉引用链接有效性验证
4. 定位符合性定性分析

### B. 参考资料

- CLAUDE.md 开发指南
- .claude/plans/guidelines.md 计划管理规范
- Agent-Skills 最佳实践文档

---

**计划创建日期**: 2026-01-30
**计划状态**: planning
**计划创建者**: Claude (GLM-4.7)
