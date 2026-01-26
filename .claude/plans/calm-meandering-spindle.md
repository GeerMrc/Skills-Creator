# 项目开发规范化综合推进计划

**计划日期**: 2026-01-26
**计划类型**: 综合规范化（开发流程 + Git管理 + 计划归档）
**当前分支**: develop
**预估时间**: 4-5小时

---

## 一、问题诊断

### 1.1 当前状态分析

**项目健康度**: 88/100 (优秀)

| 维度 | 得分 | 评价 | 问题 |
|------|------|------|------|
| 计划管理 | 75 | 良好 | 2个已完成计划未归档 |
| Git规范 | 85 | 优秀 | 代码未测试提交 |
| 代码质量 | 95 | 优秀 | 无问题 |
| 文档完整性 | 90 | 优秀 | 无问题 |
| 测试覆盖 | 95 | 优秀 | 无问题 |

### 1.2 发现的问题

**P0级别**（阻塞问题）:
| 问题ID | 问题描述 | 影响 |
|--------|----------|------|
| P0-1 | 打包规范修复代码未测试 | 质量风险 |
| P0-2 | 代码未提交到Git | 版本管理混乱 |
| P0-3 | 已完成计划未归档 | 工作流阻塞 |

**P1级别**（重要问题）:
| 问题ID | 问题描述 | 影响 |
|--------|----------|------|
| P1-1 | server.py覆盖率85% | 未达95%目标 |
| P1-2 | 计划归档不及时 | 管理效率低 |

### 1.3 未提交修改清单

```
修改文件（7个，942行新增）:
├── CHANGELOG.md                               +84行   ✅ v0.3.2记录
├── CLAUDE.md                                  +117行  ✅ 第七章打包规范
├── skill-creator-mcp/src/skill_creator_mcp/
│   ├── server.py                              +101行  ⚠️ 需审查
│   └── utils/packagers.py                     +292行  ✅ 核心修复
├── skill-creator-mcp/tests/test_tools/
│   └── test_package_skill.py                 +351行  ✅ 新增测试
├── skill-creator/SKILL.md                     +2行    ⚠️ 需审查
└── skill-creator-mcp/coverage.json            +2行    (自动生成)
```

---

## 二、修复方案

### 2.1 第一阶段：验证和提交打包规范修复

**目标**: 完成打包规范修复的测试验证和Git提交

**任务清单**:
| 任务ID | 任务描述 | 优先级 | 预计时间 |
|--------|----------|--------|----------|
| 20260126-01 | 运行完整测试套件验证修复 | P0 | 20分钟 |
| 20260126-02 | 审查server.py和SKILL.md修改 | P0 | 15分钟 |
| 20260126-03 | 运行代码质量检查 | P0 | 10分钟 |
| 20260126-04 | 提交打包规范修复代码 | P0 | 10分钟 |
| 20260126-05 | 验证提交完整性 | P0 | 5分钟 |

**验收标准**:
- [ ] pytest --cov 所有测试通过，覆盖率≥95%
- [ ] ruff check 0错误
- [ ] mypy check 0错误
- [ ] Git提交格式规范
- [ ] CHANGELOG.md已更新

### 2.2 第二阶段：归档已完成计划

**目标**: 清理计划管理状态，归档已完成的计划

**任务清单**:
| 任务ID | 任务描述 | 优先级 | 预计时间 |
|--------|----------|--------|----------|
| 20260126-06 | 归档precious-snacking-giraffe.md | P0 | 5分钟 |
| 20260126-07 | 归档idempotent-floating-dragonfly.md | P0 | 5分钟 |
| 20260126-08 | 验证归档完整性 | P0 | 5分钟 |

**归档规范**:
```bash
# 归档命名格式
archive/{date}-{original-name}.md

# 示例
archive/2026-01-26-packaging-fix-precious-snacking-giraffe.md
archive/2026-01-26-audit-idempotent-floating-dragonfly.md
```

**验收标准**:
- [ ] plans/目录下无已完成计划
- [ ] archive/目录包含归档文件
- [ ] 归档文件命名规范

### 2.3 第三阶段：开发规范梳理

**目标**: 全面梳理开发规范，制定后续迭代指导

**任务清单**:
| 任务ID | 任务描述 | 优先级 | 预计时间 |
|--------|----------|--------|----------|
| 20260126-09 | 审核CLAUDE.md完整性 | P1 | 30分钟 |
| 20260126-10 | 创建开发规范检查清单 | P1 | 45分钟 |
| 20260126-11 | 更新快速参考章节 | P1 | 20分钟 |
| 20260126-12 | 创建规范执行指南 | P2 | 30分钟 |

**交付物**:
1. **开发规范检查清单** (新文件)
   - 九步法执行检查清单
   - Git规范检查清单
   - 文档管理检查清单

2. **规范执行指南** (新文件)
   - 常见场景处理流程
   - 问题诊断和解决方案
   - 最佳实践案例

### 2.4 第四阶段：测试覆盖优化

**目标**: 提升server.py测试覆盖率到95%

**任务清单**:
| 任务ID | 任务描述 | 优先级 | 预计时间 |
|--------|----------|--------|----------|
| 20260126-13 | 分析server.py覆盖缺口 | P2 | 30分钟 |
| 20260126-14 | 补充server.py测试用例 | P2 | 1小时 |
| 20260126-15 | 验证覆盖率提升 | P2 | 10分钟 |

**验收标准**:
- [ ] server.py覆盖率 ≥95%
- [ ] 所有新测试通过
- [ ] 无测试代码质量问题

---

## 三、验收标准

### 3.1 第一阶段验收

**代码质量**:
- [ ] pytest --cov: 所有测试通过
- [ ] 覆盖率: ≥95%
- [ ] ruff check: 0错误
- [ ] mypy check: 0错误

**Git提交**:
- [ ] 提交格式: `fix(packaging): 修复 Agent-Skill 打包规范`
- [ ] 提交内容: 包含所有修改文件
- [ ] CHANGELOG.md: 已更新v0.3.2记录

**功能验证**:
- [ ] package_agent_skill() 函数正常工作
- [ ] 排除模式完整覆盖
- [ ] 版本号正确添加到包名

### 3.2 第二阶段验收

**计划管理**:
- [ ] precious-snacking-giraffe.md 已归档
- [ ] idempotent-floating-dragonfly.md 已归档
- [ ] 归档文件命名规范
- [ ] plans/目录干净（无已完成计划）

### 3.3 第三阶段验收

**文档完整性**:
- [ ] CLAUDE.md 检查清单章节完整
- [ ] 开发规范检查清单文件存在
- [ ] 规范执行指南文件存在
- [ ] 快速参考章节更新

### 3.4 第四阶段验收

**测试覆盖**:
- [ ] server.py覆盖率 ≥95%
- [ ] 新增测试用例通过
- [ ] 整体覆盖率维持≥95%

---

## 四、关键文件路径

### 4.1 需要验证的文件

| 文件 | 路径 | 说明 |
|------|------|------|
| packagers.py | skill-creator-mcp/src/skill_creator_mcp/utils/packagers.py | 打包修复核心代码 |
| server.py | skill-creator-mcp/src/skill_creator_mcp/server.py | MCP工具注册 |
| test_package_skill.py | skill-creator-mcp/tests/test_tools/test_package_skill.py | 打包测试 |
| SKILL.md | skill-creator/SKILL.md | Agent-Skill入口 |
| CLAUDE.md | CLAUDE.md | 开发指南 |
| CHANGELOG.md | CHANGELOG.md | 变更日志 |

### 4.2 需要归档的计划

| 计划 | 当前位置 | 目标位置 |
|------|----------|----------|
| 打包规范修复 | .claude/plans/precious-snacking-giraffe.md | .claude/plans/archive/2026-01-26-packaging-fix.md |
| 前期审核 | .claude/plans/idempotent-floating-dragonfly.md | .claude/plans/archive/2026-01-26-audit-report.md |

### 4.3 需要创建的文件

| 文件 | 路径 | 说明 |
|------|------|------|
| 开发规范检查清单 | .claude/plans/checklists.md | 九步法检查清单 |
| 规范执行指南 | skill-creator/references/dev-standards.md | 开发规范指南 |

---

## 五、执行步骤

### 5.1 第一阶段执行

```bash
# 1. 进入MCP Server目录
cd skill-creator-mcp

# 2. 运行完整测试套件
uv run pytest --cov

# 3. 代码质量检查
uv run ruff check .
uv run mypy src/

# 4. 审查修改内容
git diff skill-creator-mcp/src/skill_creator_mcp/server.py
git diff skill-creator/SKILL.md

# 5. 提交变更
git add .
git commit -m "fix(packaging): 修复 Agent-Skill 打包规范

问题：
- skill-creator-v0.3.1.zip 包含整个项目（392个文件，16MB）
- 应该只包含 skill-creator/ 目录内容（标准 Agent-Skill）

修复：
- 更新 packagers.py 排除模式列表（13类文件）
- 新增 package_agent_skill() 专用函数
- 支持版本号和标准化包名
- 新增12个测试用例

文档更新：
- CLAUDE.md 新增第七章打包规范
- 新增 references/packaging.md 完整指南
- 更新 SKILL.md 工具列表（17个工具）

测试：所有测试通过，覆盖率 95%
"
```

### 5.2 第二阶段执行

```bash
# 1. 归档打包规范修复计划
mv .claude/plans/precious-snacking-giraffe.md \
   .claude/plans/archive/2026-01-26-packaging-fix-precious-snacking-giraffe.md

# 2. 归档前期审核计划
mv .claude/plans/idempotent-floating-dragonfly.md \
   .claude/plans/archive/2026-01-26-audit-idempotent-floating-dragonfly.md

# 3. 验证归档
ls -la .claude/plans/
ls -la .claude/plans/archive/ | tail -5
```

### 5.3 第三阶段执行

```bash
# 1. 审核CLAUDE.md完整性
grep -n "## 章" CLAUDE.md
wc -l CLAUDE.md

# 2. 创建开发规范检查清单
# （新文件内容见附录A）

# 3. 创建规范执行指南
# （新文件内容见附录B）
```

### 5.4 第四阶段执行

```bash
# 1. 分析server.py覆盖缺口
uv run pytest --cov --cov-report=term-missing src/skill_creator_mcp/server.py

# 2. 补充测试用例
# （根据覆盖缺口添加测试）

# 3. 验证覆盖率提升
uv run pytest --cov
```

---

## 六、风险和缓解

| 风险 | 概率 | 影响 | 缓解措施 |
|------|------|------|----------|
| 测试失败 | 低 | 高 | 修复代码或调整测试 |
| 提交冲突 | 极低 | 中 | 解决冲突后重新提交 |
| 覆盖率未达标 | 中 | 低 | 优先补充关键路径测试 |

---

## 七、后续建议

### 7.1 短期改进（本周）

1. **建立计划归档自动化**
   - 在步骤9完成后自动移动计划
   - 重命名格式添加完成日期

2. **设置Git Hooks**
   - pre-commit: 运行ruff和mypy
   - pre-push: 运行pytest

3. **创建计划模板**
   - 标准化计划文档格式
   - 包含检查清单章节

### 7.2 中期改进（本月）

1. **补充集成测试**
   - MCP工具端到端测试
   - GitHub/Thinking MCP集成验证

2. **优化文档交叉引用**
   - 定期审查链接有效性
   - 统一版本标记

3. **建立质量看板**
   - 测试覆盖率趋势
   - 代码质量指标
   - 计划完成率

### 7.3 长期改进（下月）

1. **CI/CD流程优化**
   - 自动化测试和部署
   - 代码审查自动化

2. **开发规范培训**
   - 新人入职培训材料
   - 最佳实践案例库

3. **项目治理改进**
   - 定期项目健康检查
   - 技术债务管理

---

## 八、附录A：开发规范检查清单

### 九步法执行检查清单

#### 步骤0: 前置任务审核
- [ ] 前一阶段计划已完成
- [ ] 文档已归档到archive/
- [ ] 当前分支正确
- [ ] 代码已同步（working directory clean）

#### 步骤1: 制定开发计划
- [ ] 计划文档已创建（.claude/plans/feat-xxx.md）
- [ ] 目标明确，范围清晰
- [ ] 交付物清单完整
- [ ] 技术依赖和风险已识别
- [ ] 验收标准已定义

#### 步骤2: 拆分任务清单
- [ ] 使用TodoWrite创建任务
- [ ] 任务数量3-10个
- [ ] 任务ID格式：YYYYMMDD-序号
- [ ] 优先级标注（P0-P3）
- [ ] 依赖关系明确

#### 步骤3: 执行开发工作
- [ ] 按优先级顺序执行
- [ ] 每完成一项更新状态
- [ ] 遇到阻塞及时记录
- [ ] 保持代码提交原子性

#### 步骤4: 测试验证
- [ ] 编写/更新测试用例
- [ ] 运行pytest --cov
- [ ] 确保覆盖率≥99%
- [ ] 运行ruff, mypy检查

#### 步骤5: 交叉验证
- [ ] 对照计划检查完成度
- [ ] 验证所有验收标准
- [ ] 检查TODO状态一致性
- [ ] 发现问题及时回退

#### 步骤6: 更新文档
- [ ] 更新技术文档
- [ ] 更新CHANGELOG.md
- [ ] 更新任务追踪文档
- [ ] 检查交叉引用链接

#### 步骤7: 阶段性审计
- [ ] 审查是否100%按计划执行
- [ ] 记录偏差和改进措施
- [ ] 确认代码质量检查通过
- [ ] 准备Git提交信息

#### 步骤8: Git提交
- [ ] 代码通过所有测试
- [ ] 代码通过质量检查
- [ ] 文档已同步更新
- [ ] 使用规范的commit信息

#### 步骤9: 阶段汇报
- [ ] 汇总已完成任务
- [ ] 记录问题和解决方案
- [ ] 记录测试和质量指标
- [ ] 归档计划到archive/

### Git规范检查清单

#### 分支管理
- [ ] 使用正确的分支前缀（feature/fix/hotfix/refactor/docs/test）
- [ ] 分支名称描述清晰
- [ ] 从develop分支创建
- [ ] 推送到远程

#### Commit规范
- [ ] 使用格式：`<type>(<scope>): <subject>`
- [ ] Type选择正确（feat/fix/docs/style/refactor/test/chore）
- [ ] Scope合理指定或省略
- [ ] Subject描述简洁明确
- [ ] Body包含详细说明（可选）
- [ ] Footer包含关联信息（可选）

#### 代码质量
- [ ] 通过所有测试
- [ ] ruff check 0错误
- [ ] mypy check 0错误
- [ ] 代码已格式化

#### 文档同步
- [ ] CHANGELOG.md已更新
- [ ] 相关文档已同步
- [ ] 交叉引用链接有效

### 文档管理检查清单

#### 文档完整性
- [ ] 核心文档存在（CLAUDE.md, SKILL.md, README.md）
- [ ] 引用文档完整
- [ ] 交叉引用链接有效
- [ ] 文档版本标记

#### 文档质量
- [ ] 内容准确反映代码
- [ ] 代码示例可执行
- [ ] 格式规范统一
- [ ] 无过时信息

#### 计划文档
- [ ] 计划已完成
- [ ] 验收标准已满足
- [ ] 已归档到archive/
- [ ] 归档命名规范

---

## 九、附录B：规范执行指南

### 常见场景处理流程

#### 场景1: 新功能开发

**流程**:
```
1. 创建功能分支
   git checkout develop
   git checkout -b feature/your-feature-name

2. 创建计划文档
   .claude/plans/feat-your-feature-name.md

3. 拆分任务清单（3-10个任务）
   TaskCreate工具

4. 执行开发工作
   - 编码
   - 测试
   - 文档更新

5. 验证和提交
   - pytest --cov
   - ruff check && mypy
   - git commit

6. 创建PR到develop
   - Code Review
   - Squash and Merge

7. 归档计划
   mv plans/feat-xxx.md archive/2026-01-26-feat-xxx.md
```

#### 场景2: Bug修复

**流程**:
```
1. 创建修复分支
   git checkout -b fix/bug-description

2. 创建修复计划
   .claude/plans/fix-bug-description.md

3. 执行修复（5步法）
   - 分析问题
   - 编写测试（先写测试）
   - 修复代码
   - 验证测试通过
   - 更新文档

4. 快速验证
   - pytest tests/test_specific.py
   - ruff check

5. 提交合并
   git commit -m "fix(scope): description"
```

#### 场景3: 打包发布

**流程**:
```
1. 验证代码质量
   - 测试覆盖率≥95%
   - ruff/mypy 0错误
   - 文档完整

2. 使用package_agent_skill()
   - 指定版本号
   - 选择格式（zip）
   - 验证包结构

3. 验证包质量
   - 文件数量<50
   - 包大小<500KB
   - 排除项正确

4. 更新CHANGELOG.md
   - 版本号
   - 变更内容
   - 发布日期

5. 提交和打标签
   git commit -m "chore: release v0.3.2"
   git tag v0.3.2
   git push --tags
```

### 问题诊断和解决方案

#### 问题1: 测试失败

**诊断步骤**:
```bash
# 1. 查看失败详情
uv run pytest -v

# 2. 运行特定测试
uv run pytest tests/test_specific.py::test_function

# 3. 查看覆盖率
uv run pytest --cov --cov-report=term-missing
```

**解决方案**:
- 修复代码使测试通过
- 或更新测试用例（如果测试不合理）
- 重新运行验证

#### 问题2: 代码检查失败

**诊断步骤**:
```bash
# ruff检查
uv run ruff check .

# 自动修复
uv run ruff check --fix .

# mypy检查
uv run mypy src/
```

**解决方案**:
- 添加类型注解
- 修复导入错误
- 调整代码结构

#### 问题3: Git提交冲突

**诊断步骤**:
```bash
# 查看冲突
git status

# 查看差异
git diff
```

**解决方案**:
```bash
# 1. 拉取最新代码
git pull origin develop

# 2. 解决冲突
# 编辑冲突文件

# 3. 标记冲突已解决
git add .

# 4. 提交
git commit
```

#### 问题4: 计划未完成但声称完成

**预防措施**:
- 在步骤5交叉验证时严格检查
- 使用TODO回退机制
- 真实记录偏差

**处理方法**:
1. 识别未完成的任务
2. 回退TODO状态到in_progress
3. 完成任务后再更新状态
4. 修正阶段报告

### 最佳实践案例

#### 案例1: 正确的九步法执行

**场景**: 添加新MCP工具

**执行记录**:
```
步骤0: ✅ 前一阶段计划已归档，develop分支干净
步骤1: ✅ 创建计划 feat-add-mcp-tool.md（150行）
步骤2: ✅ 拆分5个任务（20260126-01至05）
步骤3: ✅ 按顺序执行，实时更新TODO
步骤4: ✅ 新增8个测试用例，覆盖率99%
步骤5: ✅ 交叉验证发现遗漏，补充完成
步骤6: ✅ 更新CHANGELOG.md和SKILL.md
步骤7: ✅ 真实审计，记录2处偏差
步骤8: ✅ 规范commit，合并到develop
步骤9: ✅ 生成汇报，归档计划
```

**关键成功因素**:
- 严格执行每个步骤
- 真实记录问题和偏差
- 及时回退TODO状态

#### 案例2: 正确的问题处理

**场景**: 测试覆盖率不达标

**处理流程**:
```
1. 发现问题：server.py覆盖率85%（未达95%）
2. 分析原因：缺少某些分支的测试
3. 回退TODO：将任务20260126-14状态改为in_progress
4. 补充测试：添加6个测试用例
5. 验证结果：覆盖率提升到96%
6. 更新TODO：标记任务completed
7. 记录偏差：在阶段报告中说明
```

**关键成功因素**:
- 及时发现问题
- 使用TODO回退机制
- 真实记录处理过程

---

**文档版本**: v1.0
**创建日期**: 2026-01-26
**状态**: planning
**下一步**: 等待用户批准后开始执行
