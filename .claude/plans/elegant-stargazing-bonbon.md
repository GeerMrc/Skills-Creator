# 项目开发规范执行与未完成任务推进计划

> **创建日期**: 2026-01-25
> **状态**: planning
> **优先级**: P0/P1/P2
> **类型**: 规范审核 + 任务推进

---

## 一、项目开发规范概述

### 1.1 七步法开发流程

```
┌─────────────────────────────────────────────────────────────────┐
│                    七步法开发流程                               │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  步骤1: 制定开发计划 → .claude/plans/feat-xxx.md                │
│       ↓                                                          │
│  步骤2: 拆分任务清单 → TodoWrite 工具                            │
│       ↓                                                          │
│  步骤3: 执行开发工作 → 编码 + 测试                               │
│       ↓                                                          │
│  步骤4: 测试验证 → pytest --cov                                 │
│       ↓                                                          │
│  步骤5: 交叉验证 → 对照计划检查完成度                            │
│       ↓                                                          │
│  步骤6: 更新文档 → CHANGELOG.md                                 │
│       ↓                                                          │
│  步骤7: 阶段性审计 → 归档计划 + 汇报                            │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### 1.2 禁止行为清单

| 禁止行为 | 后果 | 替代方案 |
|----------|------|----------|
| 虚假审核 | 代码被拒绝 | 真实执行 Code Review |
| 跨流程开发 | 工作混乱 | 严格按七步法执行 |
| 绕过测试直接提交 | 质量风险 | 必须通过全部测试 |
| 直接修改 main 分支 | 破坏稳定性 | 使用功能分支 + PR |
| 危险命令执行 | 系统崩溃 | 使用安全替代方案 |

### 1.3 质量标准

| 指标 | 要求 | 当前状态 |
|------|------|----------|
| 测试覆盖率 | ≥80% (目标≥95%) | ✅ 98% (498个测试) |
| 代码检查 | 0 错误 | ✅ Ruff 0, Mypy 0 |
| 安全检查 | 0 高危 | ✅ 通过 |
| 文档一致性 | 100% | ⚠️ 部分过时 |

---

## 二、未完成任务审核

### 2.1 comprehensive-audit-2026-01-25.md 审核结果

| 阶段 | 状态 | 完成度 | 说明 |
|------|------|--------|------|
| 阶段 1: 紧急修复 | ⚠️ 部分完成 | 33% | 仅提交 Git，文档未更新 |
| 阶段 2: 文档优化 | ⏸️ 未开始 | 0% | P2 优先级 |
| 阶段 3: 代码优化 | ⏸️ 未开始 | 0% | P3 优先级 |
| 阶段 4: 审计归档 | ⏸️ 未开始 | 0% | 依赖阶段 1 完成 |

### 2.2 fix-fallback-verification-gaps.md 审核结果

| Phase | 状态 | 优先级 | 说明 |
|-------|------|--------|------|
| Phase 1: 单元测试 | ⏸️ 未开始 | P0 | capability_detection.py 0% 覆盖 |
| Phase 2: 集成测试 | ⏸️ 未开始 | P0 | 真实异常场景未验证 |
| Phase 3: 异常格式统一 | ⏸️ 未开始 | P1 | 返回格式不一致 |
| Phase 4: 文档更新 | ⏸️ 未开始 | P1 | 回退机制说明缺失 |
| Phase 5: 验证合并 | ⏸️ 未开始 | P0 | 整体验收 |

### 2.3 iridescent-doodling-swing.md 审核结果

| 阶段 | 状态 | 优先级 | 说明 |
|------|------|--------|------|
| 阶段 1: 审核验证 | ✅ 完成 | - | 已完成 |
| 阶段 2: 功能验证 | ⏸️ 未开始 | P0 | 测试套件验证 |
| 阶段 3: 分支清理 | ⏸️ 未开始 | P1 | 删除已合并分支 |
| 阶段 4: 文档补充 | ⏸️ 未开始 | P1 | requirement-collection 用户文档 |
| 阶段 5: 阶段审计 | ⏸️ 未开始 | P1 | 归档和汇报 |

### 2.4 v0.3.0 开发计划审核结果

| 阶段 | 状态 | 完成度 | 说明 |
|------|------|--------|------|
| 阶段 1: Docker + 基础 CI | ⚠️ 部分完成 | 75% | 覆盖率报告上传待完成 |
| 阶段 2: 文档 + 高级 CI | ⏸️ 未开始 | 0% | Sphinx API 文档 |
| 阶段 3: 性能优化 + 监控 | ⏸️ 未开始 | 0% | 缓存机制 |

---

## 三、完整 TODO 任务清单

### A. 紧急修复任务 (P0 - 立即执行)

#### A.1 comprehensive-audit 阶段 1 完成

- [ ] **A.1.1** 更新文档测试数据 (P1)
  - [ ] skill-creator-mcp/README.md: 414 → 498 个测试
  - [ ] skill-creator-mcp/README.md: 94% → 98% 覆盖率
  - [ ] CHANGELOG.md 测试统计
  - [ ] ISSUES.md 测试统计
  - [ ] next-steps-v0.3.0.md 测试统计

- [ ] **A.1.2** 版本号一致性检查 (P1)
  - [ ] 检查所有版本号位置
  - [ ] 确认 __init__.py 版本
  - [ ] 确认 pyproject.toml 版本
  - [ ] 确认 CHANGELOG.md 版本

- [ ] **A.1.3** 归档审计计划 (P1)
  - [ ] 移动到 archive/
  - [ ] 提交 Git 变更
  - [ ] 更新计划索引

#### A.2 fix-fallback-verification-gaps Phase 1 (P0)

- [ ] **A.2.1** 创建测试文件
  - [ ] tests/test_utils/test_capability_detection.py

- [ ] **A.2.2** 实现 check_sampling_capability 测试 (4个)
  - [ ] test_sampling_supported
  - [ ] test_sampling_unsupported_not_declared
  - [ ] test_sampling_unsupported_error
  - [ ] test_sampling_unexpected_error

- [ ] **A.2.3** 实现 check_elicitation_capability 测试 (4个)
  - [ ] test_elicitation_supported
  - [ ] test_elicitation_unsupported_method_not_found
  - [ ] test_elicitation_unsupported_error
  - [ ] test_elicitation_unexpected_error

- [ ] **A.2.4** 实现 get_client_capabilities 测试 (6个)
  - [ ] test_both_supported
  - [ ] test_both_unsupported
  - [ ] test_only_sampling_supported
  - [ ] test_only_elicitation_supported
  - [ ] test_summary_advanced_apis_supported
  - [ ] test_summary_fallback_required

- [ ] **A.2.5** 验证测试覆盖
  - [ ] 运行 pytest --cov
  - [ ] 确认 coverage ≥80%

#### A.3 iridescent-doodling-swing 阶段 2 (P0)

- [ ] **A.3.1** 运行完整测试套件
  - [ ] cd skill-creator-mcp && uv run pytest --cov

- [ ] **A.3.2** 运行代码质量检查
  - [ ] uv run ruff check .
  - [ ] uv run mypy src/

- [ ] **A.3.3** 验证工具可用性
  - [ ] 手动测试 init_skill
  - [ ] 手动测试 collect_requirements

---

### B. 高优先级任务 (P1 - 本周内完成)

#### B.1 fix-fallback-verification-gaps Phase 2-4 (P1)

- [ ] **B.1.1** Phase 2: 真实异常场景集成测试 (8个)
  - [ ] test_collect_requirements_with_elicit_unsupported
  - [ ] test_collect_requirements_fallback_to_traditional
  - [ ] test_collect_requirements_brainstorm_fallback
  - [ ] test_collect_requirements_progressive_fallback
  - [ ] test_collect_requirements_completeness_fallback
  - [ ] test_e2e_fallback_workflow_basic
  - [ ] test_e2e_fallback_workflow_complete
  - [ ] test_e2e_fallback_with_session_recovery

- [ ] **B.1.2** Phase 3: 统一异常返回格式
  - [ ] 分析不一致性
  - [ ] 修改异常处理代码
  - [ ] 更新相关测试

- [ ] **B.1.3** Phase 4: 文档更新
  - [ ] 更新 SKILL.md 添加回退机制说明
  - [ ] 更新示例文档
  - [ ] 更新 CHANGELOG.md

#### B.2 iridescent-doodling-swing 阶段 3-5 (P1)

- [ ] **B.2.1** 阶段 3: 分支清理
  - [ ] git branch -d feature/init-skill-tool
  - [ ] git branch -d feature/requirement-collection

- [ ] **B.2.2** 阶段 4: 文档补充
  - [ ] 创建 requirement-collection 用户文档
  - [ ] 创建 requirement-collection 使用示例
  - [ ] 更新 CHANGELOG.md v0.2.1 条目

- [ ] **B.2.3** 阶段 5: 阶段审计
  - [ ] 审查执行情况
  - [ ] 记录偏差和改进措施
  - [ ] 归档计划文档
  - [ ] 生成阶段性工作汇报

#### B.3 v0.3.0 阶段 1 完成任务 (P1)

- [ ] **B.3.1** 配置覆盖率报告上传
  - [ ] 配置 Codecov 集成
  - [ ] 更新 CI 工作流

- [ ] **B.3.2** 创建部署文档
  - [ ] docs/deployment.md
  - [ ] Docker 相关示例

---

### C. 中优先级任务 (P2 - 本月内完成)

#### C.1 comprehensive-audit 阶段 2 (P2)

- [ ] **C.1.1** 精简 SKILL.md
  - [ ] 审查第 82-99 行详细说明
  - [ ] 移动到 references/requirement-collection-workflow.md
  - [ ] 更新引用链接

- [ ] **C.1.2** 拆分长示例文件
  - [ ] 创建 example-elicit-basic.md
  - [ ] 创建 example-elicit-advanced.md
  - [ ] 更新 examples/README.md

#### C.2 v0.3.0 阶段 2 启动 (P2)

- [ ] **C.2.1** 安装 Sphinx 和扩展
- [ ] **C.2.2** 创建 docs/conf.py
- [ ] **C.2.3** 配置自动文档提取
- [ ] **C.2.4** 创建高级 CI 工作流
  - [ ] release.yml
  - [ ] security.yml

---

### D. 低优先级任务 (P3 - 有时间处理)

#### D.1 comprehensive-audit 阶段 3 (P3)

- [ ] **D.1.1** 进一步模块化 requirement_collection.py
- [ ] **D.1.2** 清理备份文件 server.py.backup2
- [ ] **D.1.3** 配置远程仓库（如需要）

#### D.2 v0.3.0 阶段 3 规划 (P3)

- [ ] **D.2.1** 缓存机制设计
- [ ] **D.2.2** 批量操作支持设计
- [ ] **D.2.3** 健康检查和监控设计

---

## 四、执行计划

### 4.1 执行顺序

```
Week 1 (P0 任务)
├─ Day 1-2: A.1 comprehensive-audit 阶段 1 完成
├─ Day 3-4: A.2 fix-fallback-verification-gaps Phase 1
└─ Day 5:   A.3 iridescent-doodling-swing 阶段 2

Week 2 (P1 任务)
├─ Day 1-3: B.1 fix-fallback-verification-gaps Phase 2-4
├─ Day 4-5: B.2 iridescent-doodling-swing 阶段 3-5
└─ 背景:  B.3 v0.3.0 阶段 1 完成任务

Week 3-4 (P2 任务)
├─ C.1 comprehensive-audit 阶段 2
└─ C.2 v0.3.0 阶段 2 启动

后续 (P3 任务)
├─ D.1 comprehensive-audit 阶段 3
└─ D.2 v0.3.0 阶段 3 规划
```

### 4.2 质量检查点

每个任务完成后必须执行：

```bash
# 测试验证
cd skill-creator-mcp && uv run pytest --cov

# 代码检查
uv run ruff check .
uv run mypy src/

# 安全检查
uv run bandit -r src/
```

---

## 五、验收标准

### 5.1 功能验收

- [ ] 所有 P0-P1 任务已完成
- [ ] 文档数据与代码一致
- [ ] Git 工作区清洁
- [ ] 测试覆盖率保持 ≥95%

### 5.2 质量验收

- [ ] 测试覆盖率 ≥95%
- [ ] 代码检查 0 错误
- [ ] 类型检查 0 错误
- [ ] 安全检查 0 高危

### 5.3 文档验收

- [ ] 所有文档版本号一致
- [ ] 测试数量一致（498个）
- [ ] 覆盖率数据一致（98%）
- [ ] CHANGELOG.md 已更新

---

## 六、风险评估

| 风险 | 影响 | 缓解措施 |
|------|------|----------|
| 任务量过大 | 中 | 按优先级分批执行 |
| 文档更新遗漏 | 低 | 交叉验证检查 |
| 代码修改引入回归 | 中 | 充分测试 |
| Git 提交冲突 | 低 | 先 pull 后 push |

---

## 七、参考资料

### 7.1 相关计划文档

- `.claude/plans/archive/comprehensive-audit-2026-01-25.md`
- `.claude/plans/archive/fix-fallback-verification-gaps.md`
- `.claude/plans/archive/iridescent-doodling-swing.md`
- `.claude/plans/next-steps-v0.3.0.md`

### 7.2 项目规范

- `CLAUDE.md` - 开发规范指南
- `ARCHITECTURE_AUDIT_REPORT_v2.md` - 架构审计报告
- `ROADMAP.md` - 项目路线图
- `ISSUES.md` - 问题清单

---

## 八、下一步

1. 用户审核本计划
2. 按优先级执行任务清单
3. 每个阶段完成后更新此文档
4. 完成后归档计划

---

**计划维护**: 请在每个任务完成后更新状态。
**最后更新**: 2026-01-25
