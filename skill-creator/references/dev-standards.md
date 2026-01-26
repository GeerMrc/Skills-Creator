# 开发规范执行指南

> **版本**: v1.0
> **更新日期**: 2026-01-26
> **适用范围**: Skills-Creator 项目开发
> **配套文档**: `.claude/plans/checklists.md`

---

## 一、常见场景处理流程

### 场景1: 新功能开发

**适用**: 添加新的MCP工具、Agent-Skill功能等

**完整流程**:

```
步骤0: 前置审核
├─ 确认前一阶段计划已归档
├─ 确认当前分支为 develop
└─ 确认工作目录干净

步骤1: 创建计划
├─ 创建计划文档: .claude/plans/feat-your-feature.md
├─ 定义目标、范围、验收标准
└─ 列出技术依赖和风险

步骤2: 拆分任务
├─ 使用 TaskCreate 创建 3-10 个任务
├─ 标注优先级 (P0-P3)
└─ 明确任务依赖关系

步骤3: 创建功能分支
└─ git checkout -b feature/your-feature-name

步骤4: 执行开发
├─ 编写代码
├─ 编写测试
└─ 实时更新TODO状态

步骤5: 验证
├─ pytest --cov (覆盖率 ≥95%)
├─ ruff check (0错误)
└─ mypy check (0错误)

步骤6: 交叉验证
├─ 对照计划检查完成度
├─ 验证所有验收标准
└─ 发现问题及时回退

步骤7: 更新文档
├─ 更新技术文档
├─ 更新 CHANGELOG.md
└─ 检查交叉引用

步骤8: Git提交
├─ git add .
├─ git commit -m "feat(scope): description"
└─ git push

步骤9: 创建PR (可选)
├─ 在 GitHub 创建 Pull Request
├─ Code Review
└─ Squash and Merge to develop

步骤10: 归档计划
└─ mv plans/feat-xxx.md archive/2026-01-26-feat-xxx.md
```

**关键要点**:
- 每完成一步立即更新TODO状态
- 遇到阻塞及时记录
- 严格按九步法执行

---

### 场景2: Bug修复

**适用**: 修复已知问题

**快速流程** (5步法):

```
步骤1: 创建修复分支
└─ git checkout -b fix/bug-description

步骤2: 创建修复计划
├─ .claude/plans/fix-bug-description.md
└─ 定义问题根因和修复方案

步骤3: 执行修复 (TDD)
├─ 先编写测试（失败）
├─ 修复代码
├─ 测试通过
└─ 实时更新TODO

步骤4: 快速验证
├─ pytest tests/test_specific.py
├─ ruff check
└─ mypy check

步骤5: 提交合并
├─ git commit -m "fix(scope): description"
├─ git push
└─ 创建PR到develop (可选)
```

**修复原则**:
- **先写测试**: 确保问题可复现
- **最小修改**: 只修复问题，不添加额外功能
- **快速验证**: 只运行相关测试

---

### 场景3: 打包发布

**适用**: 发布新版本

**完整流程**:

```
步骤1: 验证代码质量
├─ pytest --cov (覆盖率 ≥95%)
├─ ruff check (0错误)
├─ mypy check (0错误)
└─ 文档完整检查

步骤2: 更新版本号
├─ 更新 pyproject.toml
├─ 更新 CHANGELOG.md
└─ 更新 SKILL.md (如需要)

步骤3: 使用 package_agent_skill()
├─ 指定版本号 (如 "0.3.2")
├─ 选择格式 (zip)
└─ 验证包结构

步骤4: 验证包质量
├─ 文件数量 <50
├─ 包大小 <500KB
└─ 排除项正确

步骤5: 提交和打标签
├─ git commit -m "chore: release v0.3.2"
├─ git tag v0.3.2
└─ git push --tags

步骤6: 创建 GitHub Release
├─ 上传打包文件
├─ 填写 Release Notes
└─ 发布
```

**包质量检查**:
```bash
# 列出包内容
unzip -l skill-creator-v0.3.2.zip | head -30

# 统计文件数量
unzip -l skill-creator-v0.3.2.zip | tail -1

# 检查包大小
ls -lh skill-creator-v0.3.2.zip
```

---

### 场景4: 代码重构

**适用**: 改善代码结构，不改变功能

**完整流程**:

```
步骤1: 创建重构分支
└─ git checkout -b refactor/module-name

步骤2: 创建重构计划
├─ .claude/plans/refactor-module.md
├─ 定义重构目标
└─ 列出重构范围

步骤3: 执行重构
├─ 保持测试不变
├─ 逐步重构
└─ 每步验证测试通过

步骤4: 验证
├─ 所有测试通过
├─ 覆盖率不降低
└─ 性能不退化

步骤5: 更新文档
├─ 更新架构文档
├─ 更新API文档
└─ 更新示例代码

步骤6: 提交合并
├─ git commit -m "refactor(scope): description"
├─ git push
└─ 创建PR到develop
```

**重构原则**:
- **小步快跑**: 每次只重构一小部分
- **测试保护**: 确保所有测试通过
- **行为不变**: 功能保持一致

---

### 场景5: 文档更新

**适用**: 更新技术文档、README等

**简化流程** (3步法):

```
步骤1: 创建文档分支
└─ git checkout -b docs/update-documentation

步骤2: 更新文档
├─ 编辑文档内容
├─ 检查交叉引用
└─ 更新版本标记

步骤3: 提交合并
├─ git commit -m "docs: update XXX documentation"
├─ git push
└─ 创建PR或直接合并
```

**文档检查清单**:
- [ ] 内容准确
- [ ] 格式规范
- [ ] 代码示例可运行
- [ ] 交叉引用有效
- [ ] 无过时信息

---

## 二、问题诊断和解决方案

### 问题1: 测试失败

**症状**:
```
FAILED tests/test_example.py::test_function
AssertionError: Expected 5, got 3
```

**诊断步骤**:
```bash
# 1. 查看失败详情
uv run pytest -v tests/test_example.py::test_function

# 2. 运行特定测试（查看详细输出）
uv run pytest -vv tests/test_example.py::test_function -s

# 3. 查看覆盖率（发现未覆盖的代码）
uv run pytest --cov --cov-report=term-missing

# 4. 进入调试模式
uv run pytest --pdb tests/test_example.py::test_function
```

**解决方案**:
- **选项A**: 修复代码使测试通过
- **选项B**: 更新测试用例（如果测试不合理）
- **选项C**: 跳过测试并创建Issue（临时方案）

---

### 问题2: 代码检查失败

**症状**:
```
error: `name` is not defined  [undefined-variable]
warning: Unused import `os`  [unused-import]
```

**诊断步骤**:
```bash
# ruff检查
uv run ruff check .

# 自动修复
uv run ruff check --fix .

# mypy检查
uv run mypy src/

# 查看具体错误
uv run mypy src/specific_file.py
```

**常见错误和解决**:

| 错误 | 原因 | 解决 |
|------|------|------|
| `undefined-variable` | 变量未定义 | 添加变量定义或导入 |
| `unused-import` | 未使用的导入 | 删除导入 |
| `missing-type-arg` | 缺少类型注解 | 添加类型注解 |
| `assignment` | 赋值错误 | 修复赋值语句 |

---

### 问题3: Git提交冲突

**症状**:
```
CONFLICT (content): Merge conflict in file.py
```

**诊断步骤**:
```bash
# 查看冲突
git status

# 查看差异
git diff

# 查看冲突文件
cat file.py
```

**解决方案**:
```bash
# 1. 拉取最新代码
git pull origin develop

# 2. 解决冲突（编辑文件）
# <<<<<<< HEAD
# 你的代码
# =======
# 别人的代码
# >>>>>>> origin/develop

# 3. 标记冲突已解决
git add .

# 4. 提交
git commit

# 5. 推送
git push
```

**冲突解决技巧**:
- 保留双方代码: `git checkout --ours` 或 `git checkout --theirs`
- 手动合并: 编辑文件，删除冲突标记
- 使用工具: `git mergetool`

---

### 问题4: 计划未完成但声称完成

**症状**: 阶段报告声称100%完成，但实际有遗漏

**预防措施**:
- 步骤5交叉验证时严格检查
- 使用TODO回退机制
- 真实记录偏差

**处理方法**:
```bash
# 1. 识别未完成的任务
TaskGet(taskId="YYYYMMDD-XX")

# 2. 回退TODO状态
TaskUpdate(taskId="YYYYMMDD-XX", status="in_progress")

# 3. 完成任务
# ... 执行开发工作 ...

# 4. 更新状态
TaskUpdate(taskId="YYYYMMDD-XX", status="completed")

# 5. 修正阶段报告
# 更新偏差记录
```

---

### 问题5: 包大小超出限制

**症状**: 打包文件 >500KB

**诊断步骤**:
```bash
# 查看包大小
ls -lh skill-creator-v0.3.2.zip

# 查看包内容
unzip -l skill-creator-v0.3.2.zip | head -50

# 统计文件数量
unzip -l skill-creator-v0.3.2.zip | tail -1
```

**常见原因**:
- 包含了不应该包含的文件（测试、文档、构建产物）
- 包含了MCP Server代码
- 包含了整个项目而非单个Agent-Skill

**解决方案**:
```bash
# 1. 检查排除模式
# 2. 使用 package_agent_skill() 而非 package_skill()
# 3. 重新打包
```

---

## 三、最佳实践案例

### 案例1: 正确的九步法执行

**场景**: 添加新MCP工具 `package_agent_skill`

**执行记录**:
```
步骤0: ✅ 前一阶段计划已归档，develop分支干净
步骤1: ✅ 创建计划 feat-package-agent-skill.md（150行）
       - 目标：修复打包规范
       - 范围：packagers.py, server.py, tests
       - 验收：覆盖率≥95%，包大小<500KB
步骤2: ✅ 拆分5个任务（20260126-01至05）
步骤3: ✅ 按顺序执行，实时更新TODO
       - 修复排除模式逻辑
       - 新增专用打包函数
       - 添加测试用例
步骤4: ✅ 新增12个测试用例，覆盖率95%
       - pytest: 577个测试全部通过
       - ruff: 0错误
       - mypy: 0错误
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
- 完整的交叉验证

---

### 案例2: 正确的问题处理

**场景**: 测试覆盖率不达标

**问题**:
```
server.py覆盖率85%（未达95%目标）
```

**处理流程**:
```
1. 发现问题
   └─ 运行 pytest --cov 查看覆盖缺口

2. 分析原因
   └─ 缺少某些分支的测试

3. 回退TODO
   └─ 将任务20260126-14状态改为in_progress

4. 补充测试
   └─ 添加6个测试用例覆盖缺失分支

5. 验证结果
   └─ 覆盖率提升到96% ✅

6. 更新TODO
   └─ 标记任务completed

7. 记录偏差
   └─ 在阶段报告中说明调整
```

**关键成功因素**:
- 及时发现问题
- 使用TODO回退机制
- 真实记录处理过程

---

### 案例3: 正确的Git工作流

**场景**: 多人协作开发

**工作流**:
```
开发者A: feature/add-mcp-tool
├─ git checkout develop
├─ git checkout -b feature/add-mcp-tool
├─ 开发 + 测试
├─ git push -u origin feature/add-mcp-tool
└─ 创建 PR to develop

开发者B: feature/fix-packaging
├─ git checkout develop
├─ git checkout -b feature/fix-packaging
├─ 开发 + 测试
├─ git push -u origin feature/fix-packaging
└─ 创建 PR to develop

Code Review:
├─ 审查 PR 代码
├─ 请求修改或批准
└─ Squash and Merge

develop分支:
├─ 接受 PR 1
├─ 接受 PR 2
└─ 推送到远程
```

**关键成功因素**:
- 每个功能独立分支
- 通过PR合并
- Code Review
- Squash and Merge保持历史干净

---

## 四、快速参考

### 常用命令

| 操作 | 命令 |
|------|------|
| 运行测试 | `uv run pytest --cov` |
| 代码检查 | `uv run ruff check . && uv run mypy src/` |
| 创建分支 | `git checkout -b feature/xxx` |
| 提交变更 | `git commit -m "feat(scope): desc"` |
| 推送远程 | `git push -u origin feature/xxx` |
| 归档计划 | `git mv plans/xxx.md archive/2026-01-26-xxx.md` |

### 关键文件路径

| 文件 | 路径 |
|------|------|
| 开发指南 | `CLAUDE.md` |
| 检查清单 | `.claude/plans/checklists.md` |
| 执行指南 | `skill-creator/references/dev-standards.md` |
| 变更日志 | `CHANGELOG.md` |

### 优先级定义

| 优先级 | 说明 | 响应时间 |
|--------|------|----------|
| P0 | 阻塞性问题 | 立即 |
| P1 | 高优先级 | 本周内 |
| P2 | 中优先级 | 本月内 |
| P3 | 低优先级 | 有时间时 |

---

**文档维护**: 请在每次发现新场景或问题时更新此指南。
**最后更新**: 2026-01-26
