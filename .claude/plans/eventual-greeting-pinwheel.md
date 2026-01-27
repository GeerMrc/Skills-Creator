# 项目全面审核与规范化修复计划

**计划ID**: eventual-greeting-pinwheel
**创建日期**: 2026-01-27
**状态**: planning
**优先级**: P0（紧急）
**负责人**: Claude Code

---

## 一、计划概述

### 1.1 背景

基于对Skills-Creator项目的全面审核（基于实际代码内容），发现项目虽然**代码质量优秀**（96%测试覆盖率，619个测试全部通过），但**流程合规性存在严重问题**（40%合规性）。

### 1.2 审核依据

✅ **100%基于实际代码审核**：
- 运行 `pytest --cov` 获取真实测试覆盖率
- 检查实际文件内容和行数
- 验证计划状态与代码一致性
- 审核Git历史和提交记录

❌ **未仅依赖文档/摘要**：
- 未仅依据README.md中的声明
- 未仅依据git commit message
- 未仅依据计划文档中的状态标记

### 1.3 目标

1. **规范化修复**：修复所有流程违规问题
2. **文档一致性**：确保所有文档数据准确
3. **Git工作流**：清理未提交和未推送的变更
4. **计划归档**：归档所有已完成的计划
5. **建立规范**：为未来开发建立TODO工具使用标准

---

## 二、审核发现（基于实际代码）

### 2.1 代码质量（优秀）✅

| 指标 | 实际值 | 目标值 | 状态 |
|------|--------|--------|------|
| 测试覆盖率 | 96% | ≥95% | ✅ 超标 |
| 测试数量 | 619 | ≥600 | ✅ 超标 |
| 测试通过率 | 100% | 100% | ✅ 完美 |
| Ruff错误 | 0 | 0 | ✅ 通过 |
| MyPy错误 | 10 | 0 | ⚠️ 待修复 |
| 安全漏洞 | 0 | 0 | ✅ 通过 |
| TODO标记 | 0 | 0 | ✅ 无债务 |

**实际验证命令**：
```bash
cd skill-creator-mcp
uv run pytest --cov          # 619 passed, 96% coverage
uv run ruff check .          # 0 errors
uv run mypy src/             # 10 errors (待修复)
uv run bandit -r src/        # 0 issues
```

### 2.2 Phase 2.2 重构状态

**计划声称** (bubbly-swinging-brooks.md):
- 任务进度: 6/8
- 任务7: 更新 server.py 导入和注册 - 待执行
- 任务8: 运行完整测试验证 - 待执行

**实际代码验证**:
```bash
# 检查 server.py 导入
grep "^from \.tools\." server.py
# 结果：已导入所有新工具模块

# 检查 server.py 行数
wc -l server.py
# 结果：557行（目标550行）

# 检查工具模块文件
ls -la tools/*.py
# 结果：5个新模块已创建（skill_tools.py, package_tools.py等）

# 运行测试
uv run pytest
# 结果：619 passed (100%)
```

**结论**：✅ Phase 2.2 **实际已完成**，但计划状态未更新

### 2.3 文档不一致问题

**测试数量不一致**（实际检查）:

| 文件位置 | 声明 | 实际 | 偏差 |
|----------|------|------|------|
| 项目根 README.md | "619 passed" | 619 | ✅ 正确 |
| MCP README.md | "589个测试" | 619 | ❌ -30 |
| CHANGELOG.md | "619" | 619 | ✅ 正确 |

**修复命令**：
```bash
# 需要修复的文件
skill-creator-mcp/README.md  # 第5行：589 → 619
```

**环境变量命名不一致**:

| 位置 | 变量名 | 实际代码使用 |
|------|--------|--------------|
| 计划文档 | `SKILL_CREATOR_DEFAULT_OUTPUT_DIR` | ❌ 不存在 |
| 实际代码 | `SKILL_CREATOR_OUTPUT_DIR` | ✅ 正确 |

**修复命令**：
```bash
# 检查实际使用的环境变量
grep -r "SKILL_CREATOR.*OUTPUT" src/
# 结果：仅 SKILL_CREATOR_OUTPUT_DIR
```

### 2.4 Git工作流问题

**未提交的变更**（实际检查）:
```bash
git status
# 结果：
# modified:   server.py
# modified:   tools/batch_operations.py
# modified:   12个测试文件
# untracked:  5个新工具模块文件
```

**未推送的提交**:
```bash
git log origin/develop..develop --oneline | wc -l
# 结果：18个提交未推送
```

**src/ 目录问题**:
```bash
ls -la /models/claude-glm/Skills-Creator/src/
# 结果：存在符号链接或重复目录
# 问题：根目录不应有 src/，MCP代码已在 skill-creator-mcp/src/
```

### 2.5 计划管理问题

**未归档计划**（实际检查）:
```bash
ls -1 .claude/plans/*.md | grep -v guidelines.md
# 结果：7个未归档计划
```

| 计划文件 | 声称状态 | 实际状态 | 应归档 |
|----------|----------|----------|--------|
| bubbly-swinging-brooks.md | 6/8执行中 | 8/8已完成 | ✅ 是 |
| floofy-napping-glade.md | planning | 已完成 | ✅ 是 |
| refactored-soaring-storm.md | - | 已完成 | ✅ 是 |
| elegant-growing-penguin.md | planning | 未执行 | ⏳ 待定 |
| generic-seeking-toast.md | - | 未执行 | ⏳ 待定 |
| keen-watching-wozniak.md | - | 未执行 | ⏳ 待定 |
| zesty-tinkering-naur.md | - | 未执行 | ⏳ 待定 |

**计划状态与代码一致性验证**:
```bash
# 检查 bubbly-swinging-brooks.md 的任务8
# 计划声称：待执行
# 实际：测试已全部通过（619 passed）
# 结论：计划状态过期
```

---

## 三、违规行为总结

### 3.1 流程违规

| 违规步骤 | 违规行为 | 后果 | 发现方式 |
|----------|----------|------|----------|
| 步骤2 | 未使用TaskCreate工具 | 进度不透明 | 检查计划文档 |
| 步骤5 | 跳过交叉验证 | 质量风险 | 检查Phase 2.2 |
| 步骤9 | 未归档已完成计划 | 计划混乱 | 检查plans/目录 |

### 3.2 文档违规

| 违规类型 | 具体问题 | 影响 | 发现方式 |
|----------|----------|------|----------|
| 数据不一致 | MCP README: 589 vs 619 | 误导用户 | 实际运行测试 |
| 命名不一致 | 环境变量名混淆 | 实现偏差 | 检查代码使用 |

### 3.3 Git违规

| 违规类型 | 具体问题 | 影响 | 发现方式 |
|----------|----------|------|----------|
| 代码未提交 | 13个文件未暂存 | 丢失风险 | git status |
| 提交未推送 | 18个提交积累 | 协作风险 | git log |
| 目录错误 | 根目录src/ | 混淆风险 | ls -la |

---

## 四、TODO任务清单

### 使用TaskCreate工具（符合规范步骤2）

**任务格式**: `YYYYMMDD-序号` 简要描述

**任务限制**: 3-10个任务（符合规范）

---

#### 阶段一：P0紧急修复（必须完成）

**20260127-01**: 归档已完成的Phase 2.2计划
- 移动 `bubbly-swinging-brooks.md` → `archive/`
- 移动 `floofy-napping-glade.md` → `archive/`
- 移动 `refactored-soaring-storm.md` → `archive/`
- 验证：archive/目录中包含3个新文件

**20260127-02**: 修复文档不一致
- 修改 `skill-creator-mcp/README.md` 第5行：589 → 619
- 验证：grep -n "619" skill-creator-mcp/README.md

**20260127-03**: 提交Phase 2.2重构代码
- 暂存13个修改的文件：`git add`
- 提交：`git commit -m "refactor(mcp): 完成Phase 2.2工具模块拆分"`
- 验证：`git status` 显示干净

**20260127-04**: 推送积累的18个提交
- 推送到远程：`git push origin develop`
- 验证：`git log origin/develop..develop` 为空

**20260127-05**: 清理根目录src/
- 确认是否为误创建
- 如确认删除：`rm -rf /models/claude-glm/Skills-Creator/src/`
- 验证：`ls -la /models/claude-glm/Skills-Creator/` 无src/

**20260127-06**: 修复MyPy类型注解问题
- 运行 `uv run mypy src/` 获取完整错误列表
- 为10个函数添加完整类型注解
- 验证：`uv run mypy src/` 通过（0错误）

---

#### 阶段二：P1规范化改进（应完成）

**20260127-07**: 执行Phase 2.2交叉验证
- 对照 `bubbly-swinging-brooks.md` 逐项检查
- 验证所有8个任务完成度
- 记录验证结果到计划文件

**20260127-08**: 统一环境变量命名
- 检查所有计划文档中的环境变量引用
- 将 `SKILL_CREATOR_DEFAULT_OUTPUT_DIR` → `SKILL_CREATOR_OUTPUT_DIR`
- 验证：grep -r "DEFAULT_OUTPUT_DIR" .claude/plans/

**20260127-09**: 评估并合并重叠计划
- 审查 `generic-seeking-toast.md`（28KB，过长）
- 拆分为独立小计划
- 明确计划间依赖关系

**20260127-10**: 建立TODO工具使用规范
- 创建 `.claude/plans/guidelines.md` 补充
- 规定未来计划必须使用TaskCreate
- 建立任务状态实时更新机制

---

## 五、验收标准

### 5.1 P0验收标准

| 标准 | 验证命令 | 预期结果 |
|------|----------|----------|
| 计划已归档 | `ls .claude/plans/archive/*.md \| wc -l` | ≥20个文件 |
| 文档一致 | `grep "619" skill-creator-mcp/README.md` | 匹配 |
| 代码已提交 | `git status --short` | 空输出 |
| 已推送 | `git log origin/develop..develop` | 空输出 |
| src/清理 | `ls -d /models/claude-glm/Skills-Creator/src/ 2>/dev/null` | 失败 |
| MyPy通过 | `uv run mypy src/` | 0错误 |

### 5.2 P1验收标准

| 标准 | 验证方式 | 预期结果 |
|------|----------|----------|
| 交叉验证完成 | 检查计划文件验证章节 | 包含完整验证报告 |
| 环境变量统一 | `grep -r "DEFAULT_OUTPUT_DIR" plans/` | 无结果 |
| 计划已拆分 | `wc -c generic-seeking-toast.md` | <10KB |
| TODO规范 | 检查guidelines.md | 包含TaskCreate使用说明 |

---

## 六、执行流程（九步法）

### 步骤0: 前置任务审核 ✅
- [x] 检查前置任务：Phase 2.1已归档
- [x] 确认Git环境：develop分支
- [x] 代码已同步：最新commit a9e2ca4

### 步骤1: 制定开发计划 ✅
- [x] 创建计划文档：eventual-greeting-pinwheel.md
- [x] 明确目标：规范化修复
- [x] 定义验收标准

### 步骤2: 拆分任务清单 ✅
- [x] 使用TaskCreate创建10个任务
- [x] 标注优先级（P0: 6个，P1: 4个）
- [x] 限制3-10个任务

### 步骤3: 执行开发工作 ⏳
- [ ] 按优先级顺序执行
- [ ] 每完成一项更新状态
- [ ] 遇到阻塞及时记录

### 步骤4: 测试验证 ⏳
- [ ] 运行 `uv run pytest --cov`
- [ ] 确保覆盖率≥95%
- [ ] 运行 `uv run ruff check .` 和 `uv run mypy src/`

### 步骤5: 交叉验证 ⏳
- [ ] 对照计划检查完成度
- [ ] 验证所有验收标准
- [ ] 检查TODO状态一致性

### 步骤6: 更新文档 ⏳
- [ ] 更新CHANGELOG.md
- [ ] 更新相关文档
- [ ] 检查交叉引用

### 步骤7: 阶段性审计 ⏳
- [ ] 审查是否100%按计划执行
- [ ] 记录偏差和改进措施
- [ ] 确认代码质量检查通过

### 步骤8: Git提交 ⏳
- [ ] 代码通过所有测试
- [ ] 代码通过质量检查
- [ ] 文档已同步更新
- [ ] 使用规范的commit信息

### 步骤9: 阶段性汇报 ⏳
- [ ] 汇总已完成任务
- [ ] 记录问题和解决方案
- [ ] 记录测试和质量指标
- [ ] 归档计划到archive/

---

## 七、风险评估

### 7.1 技术风险

| 风险 | 概率 | 影响 | 缓解措施 |
|------|------|------|----------|
| Git推送冲突 | 中 | 中 | 先pull再push |
| src/删除错误 | 低 | 高 | 先备份确认 |
| MyPy修复引入bug | 低 | 中 | 逐个修复并测试 |

### 7.2 流程风险

| 风险 | 概率 | 影响 | 缓解措施 |
|------|------|------|----------|
| 任务超量 | 低 | 低 | 已限制10个 |
| TODO工具不熟悉 | 中 | 低 | 参考文档 |
| 计划归档错误 | 低 | 低 | 逐一验证 |

---

## 八、时间估算

| 阶段 | 任务数 | 预估工作量 |
|------|--------|-----------|
| P0紧急修复 | 6 | 约2小时 |
| P1规范化改进 | 4 | 约3小时 |
| **总计** | 10 | **约5小时** |

---

## 九、参考文档

- **开发规范**: `CLAUDE.md`
- **九步法**: CLAUDE.md 第二章
- **Git规范**: CLAUDE.md 第三章
- **计划管理**: CLAUDE.md 第四章
- **Phase 2.2计划**: `.claude/plans/bubbly-swinging-brooks.md`

---

**计划创建日期**: 2026-01-27
**预计完成日期**: 2026-01-27
**实际完成日期**: _______
**计划状态**: planning → in_progress → completed → archived
