# 开发规范执行指南

> **版本**: v1.1
> **更新日期**: 2026-01-27
> **适用范围**: Skills-Creator 项目开发
> **配套文档**:
> - [九步法工作流](dev-standards-workflow.md)
> - [Git工作流规范](dev-standards-git.md)
> - [文档管理规范](dev-standards-documentation.md)

---

## 一、常见场景处理流程

### 场景1: 新功能开发

**适用**: 添加新的MCP工具、Agent-Skill功能等

**完整流程**: 详见 [九步法工作流](dev-standards-workflow.md)

**快速命令**:
```bash
# 创建功能分支
git checkout -b feature/your-feature-name

# 开发 + 测试
uv run pytest --cov
uv run ruff check .

# 提交
git commit -m "feat(scope): description"
git push -u origin feature/your-feature-name
```

---

### 场景2: Bug修复

**适用**: 修复已知问题

**快速流程** (5步法):
```bash
# 1. 创建修复分支
git checkout -b fix/bug-description

# 2. 执行修复 (TDD)
# 先编写测试（失败）
# 修复代码
# 测试通过

# 3. 快速验证
uv run pytest tests/test_specific.py
uv run ruff check

# 4. 提交
git commit -m "fix(scope): description"
git push

# 5. 创建PR到develop (可选)
```

**修复原则**:
- **先写测试**: 确保问题可复现
- **最小修改**: 只修复问题，不添加额外功能
- **快速验证**: 只运行相关测试

---

### 场景3: 打包发布

**适用**: 发布新版本

**完整流程**:
```bash
# 1. 验证代码质量
uv run pytest --cov
uv run ruff check .
uv run mypy src/

# 2. 更新版本号
# 更新 pyproject.toml
# 更新 CHANGELOG.md

# 3. 打包
# 使用 package_agent_skill() MCP 工具

# 4. 验证包质量
unzip -l skill-creator-v0.x.x.zip | head -30
ls -lh skill-creator-v0.x.x.zip

# 5. 提交和打标签
git commit -m "chore: release v0.x.x"
git tag v0.x.x
git push --tags
```

**包质量标准**:
- 文件数量 <50
- 包大小 <500KB
- 排除项正确

---

### 场景4: 代码重构

**适用**: 改善代码结构，不改变功能

**快速流程**:
```bash
# 1. 创建重构分支
git checkout -b refactor/module-name

# 2. 执行重构
# 保持测试不变
# 逐步重构
# 每步验证测试通过

# 3. 验证
uv run pytest

# 4. 更新文档

# 5. 提交
git commit -m "refactor(scope): description"
git push
```

**重构原则**:
- **小步快跑**: 每次只重构一小部分
- **测试保护**: 确保所有测试通过
- **行为不变**: 功能保持一致

---

### 场景5: 文档更新

**适用**: 更新技术文档、README等

**简化流程** (3步法):
```bash
# 1. 创建文档分支
git checkout -b docs/update-documentation

# 2. 更新文档
# 编辑文档内容
# 检查交叉引用
# 更新版本标记

# 3. 提交合并
git commit -m "docs: update XXX documentation"
git push
```

**文档检查清单**:
- [ ] 内容准确
- [ ] 格式规范
- [ ] 代码示例可运行
- [ ] 交叉引用有效
- [ ] 无过时信息

> 详见：[文档管理规范](dev-standards-documentation.md)

---

## 二、问题诊断和解决方案

### 问题1: 测试失败

**诊断**:
```bash
# 查看失败详情
uv run pytest -v tests/test_example.py::test_function

# 查看覆盖率
uv run pytest --cov --cov-report=term-missing

# 进入调试模式
uv run pytest --pdb tests/test_example.py::test_function
```

**解决方案**:
- 修复代码使测试通过
- 更新测试用例（如果测试不合理）
- 跳过测试并创建Issue（临时方案）

---

### 问题2: 代码检查失败

**诊断**:
```bash
# ruff检查
uv run ruff check .

# 自动修复
uv run ruff check --fix .

# mypy检查
uv run mypy src/
```

**常见错误**:

| 错误 | 原因 | 解决 |
|------|------|------|
| `undefined-variable` | 变量未定义 | 添加变量定义或导入 |
| `unused-import` | 未使用的导入 | 删除导入 |
| `missing-type-arg` | 缺少类型注解 | 添加类型注解 |

---

### 问题3: Git提交冲突

**诊断**:
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

# 2. 解决冲突（编辑文件）

# 3. 标记冲突已解决
git add .

# 4. 提交
git commit

# 5. 推送
git push
```

> 详见：[Git工作流规范](dev-standards-git.md)

---

### 问题4: 计划未完成但声称完成

**预防措施**:
- 步骤5交叉验证时严格检查
- 使用TODO回退机制
- 真实记录偏差

**处理方法**:
```python
# 1. 识别未完成的任务
TaskGet(taskId="xxx")

# 2. 回退TODO状态
TaskUpdate(taskId="xxx", status="in_progress")

# 3. 完成任务后更新
TaskUpdate(taskId="xxx", status="completed")
```

---

### 问题5: 包大小超出限制

**诊断**:
```bash
# 查看包大小
ls -lh skill-creator-v0.x.x.zip

# 查看包内容
unzip -l skill-creator-v0.x.x.zip | head -50
```

**常见原因**:
- 包含了不应该包含的文件（测试、文档、构建产物）
- 包含了MCP Server代码
- 包含了整个项目而非单个Agent-Skill

**解决方案**:
- 检查排除模式
- 使用 `package_agent_skill()` 而非 `package_skill()`
- 重新打包

---

## 三、最佳实践案例

### 案例1: 正确的九步法执行

**场景**: 添加新MCP工具 `package_agent_skill`

**执行记录**:
```
步骤0: ✅ 前一阶段计划已归档，develop分支干净
步骤1: ✅ 创建计划（150行）
       - 目标：修复打包规范
       - 范围：packagers.py, server.py, tests
       - 验收：覆盖率≥95%，包大小<500KB
步骤2: ✅ 拆分5个任务
步骤3: ✅ 按顺序执行，实时更新TODO
步骤4: ✅ 新增12个测试用例，覆盖率95%
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

**处理流程**:
```
1. 发现问题 → 运行 pytest --cov 查看覆盖缺口
2. 分析原因 → 缺少某些分支的测试
3. 回退TODO → 将任务状态改为in_progress
4. 补充测试 → 添加6个测试用例
5. 验证结果 → 覆盖率提升到96% ✅
6. 更新TODO → 标记任务completed
7. 记录偏差 → 在阶段报告中说明调整
```

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
| 执行指南 | `skill-creator/references/dev-standards.md` |
| 工作流详解 | `skill-creator/references/dev-standards-workflow.md` |
| Git规范 | `skill-creator/references/dev-standards-git.md` |
| 文档规范 | `skill-creator/references/dev-standards-documentation.md` |
| 变更日志 | `CHANGELOG.md` |

### 优先级定义

| 优先级 | 说明 | 响应时间 |
|--------|------|----------|
| P0 | 阻塞性问题 | 立即 |
| P1 | 高优先级 | 本周内 |
| P2 | 中优先级 | 本月内 |
| P3 | 低优先级 | 有时间时 |

---

## 五、专题文档索引

| 专题 | 文档 | 说明 |
|------|------|------|
| 九步法 | [dev-standards-workflow.md](dev-standards-workflow.md) | 完整的开发工作流详解 |
| Git规范 | [dev-standards-git.md](dev-standards-git.md) | 分支策略、Commit规范 |
| 文档管理 | [dev-standards-documentation.md](dev-standards-documentation.md) | 文档更新、放置规则 |

---

**文档维护**: 请在每次发现新场景或问题时更新此指南。
**最后更新**: 2026-01-27 (v1.1 - 拆分为专题文档)
