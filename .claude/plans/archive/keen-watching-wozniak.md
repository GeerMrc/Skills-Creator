# Skills-Creator 全面优化改进计划

> **计划版本**: v1.0
> **创建日期**: 2026-01-27
> **计划类型**: 综合优化改进
> **基于审核**: 项目整体审核 (93/100) + Agent-Skill审核 (5/5) + MCP Server审核 (5/5)
> **预计工期**: 2周 (分4个阶段执行)

---

## 执行摘要

基于三个全面审核报告的优秀结果，项目当前状态：
- **项目整体评分**: ⭐⭐⭐⭐⭐ 93/100 优秀
- **Agent-Skill评分**: ⭐⭐⭐⭐⭐ (5/5) 优秀
- **MCP Server评分**: ⭐⭐⭐⭐⭐ (5/5) 优秀

本计划旨在解决已识别的改进空间：
- **P0级**: 2个Git状态问题
- **P1级**: 5个代码质量和文档结构问题
- **P2级**: 6个测试覆盖率和CI/CD问题
- **P3级**: 3个长期改进项

---

## 一、立即执行项 (P0) - 阻塞性问题

### P0-1: 修复Git状态 - 删除未提交的计划文件

**问题描述**: `.claude/plans/streamed-hopping-lecun.md` 显示为已删除状态但未提交。

**解决方案**:
```bash
# 步骤1: 确认文件已在archive/目录
ls -la .claude/plans/archive/streamed-hopping-lecun.md

# 步骤2: 提交删除操作
git add .claude/plans/streamed-hopping-lecun.md
git add .claude/plans/archive/streamed-hopping-lecun.md
git add .claude/plans/archive/wise-tinkering-crab.md
git commit -m "chore(plans): 归档计划文档到archive目录"
```

**验证方法**:
```bash
git status  # 应该不显示streamed-hopping-lecun.md的删除状态
```

**预计时间**: 5分钟

---

### P0-2: 处理coverage.json变更

**问题描述**: `skill-creator-mcp/coverage.json` 显示为已修改状态，这个文件不应该提交到Git。

**解决方案**:
```bash
# 检查.gitignore
grep "coverage.json" skill-creator-mcp/.gitignore || echo "coverage.json" >> skill-creator-mcp/.gitignore

# 从Git中移除（但保留本地文件）
git rm --cached skill-creator-mcp/coverage.json
git commit -m "chore: 将coverage.json加入.gitignore"
```

**验证方法**:
```bash
git status  # coverage.json不应该显示在未跟踪或已修改列表
```

**预计时间**: 5分钟

---

## 二、短期改进项 (P1) - 本周内完成

### P1-1: 修复Ruff代码检查问题

**问题描述**: Ruff检查发现2个F401错误（未使用的导入）

**关键文件**:
- `skill-creator-mcp/src/skill_creator_mcp/models/skill_config.py:3`
- `skill-creator-mcp/tests/test_tools/test_config.py:229`

**解决方案**: 删除未使用的导入

**验证方法**:
```bash
cd skill-creator-mcp
uv run ruff check .
# 预期: 0 errors
```

**预计时间**: 5分钟

---

### P1-2: 拆分dev-standards.md文档

**问题描述**: `skill-creator/references/dev-standards.md` 文件过长（565行）

**解决方案**: 拆分为多个专题文档

```
dev-standards.md (565行) → 拆分为:
1. dev-standards.md (~200行) - 常见场景和快速参考
2. dev-standards-workflow.md (~150行) - 九步法详细说明
3. dev-standards-git.md (~120行) - Git规范详细说明
4. dev-standards-documentation.md (~100行) - 文档管理规范
```

**验证方法**:
```bash
wc -l skill-creator/references/dev-standards*.md
# 预期: 所有文件 ≤300行
```

**预计时间**: 2小时

---

### P1-3: 精简packaging.md文档

**问题描述**: `skill-creator/references/packaging.md` 文件过长（397行）

**解决方案**: 精简并移出详细示例到examples/

```
packaging.md (397行) → 精简为:
1. packaging.md (~200行) - 保留规范和结构
2. examples/packaging-basic.md (~100行) - 基础示例
3. examples/packaging-advanced.md (~100行) - 高级示例
```

**验证方法**:
```bash
wc -l skill-creator/references/packaging.md
# 预期: ≤250行
```

**预计时间**: 1.5小时

---

### P1-4: SKILL.md添加打包规范引用

**问题描述**: SKILL.md未提及打包规范

**解决方案**: 在SKILL.md的"快速开始"部分添加打包相关内容

**关键文件**: `skill-creator/SKILL.md`

**预计时间**: 15分钟

---

### P1-5: 安装bandit安全扫描工具

**问题描述**: bandit未安装，无法执行安全扫描

**解决方案**:
```bash
cd skill-creator-mcp
uv add --dev bandit
uv run bandit --version
```

**预计时间**: 10分钟

---

## 三、中期优化项 (P2) - 本月内完成

### P2-1: 提升测试覆盖率到90%以上

**问题描述**: 3个模块的测试覆盖率低于90%
- `path_helpers.py`: 78.8%
- `testing.py`: 83.3%
- `packagers.py`: 87.8%

**解决方案**: 补充边缘情况和错误处理测试

**关键文件**:
- `skill-creator-mcp/tests/test_utils/test_path_helpers.py`
- `skill-creator-mcp/tests/test_utils/test_testing.py`
- `skill-creator-mcp/tests/test_utils/test_packagers.py`

**验证方法**:
```bash
cd skill-creator-mcp
uv run pytest --cov=skill_creator_mcp.utils.path_helpers --cov-report=term-missing
uv run pytest --cov=skill_creator_mcp.utils.testing --cov-report=term-missing
uv run pytest --cov=skill_creator_mcp.utils.packagers --cov-report=term-missing
# 预期: 每个模块覆盖率 ≥90%
```

**预计时间**: 4小时

---

### P2-2: 精简cache-mechanism-advanced.md

**问题描述**: 文件过长（381行）

**解决方案**: 拆分并移出实战案例

**关键文件**: `skill-creator/references/cache-mechanism-advanced.md`

**预计时间**: 1小时

---

### P2-3: 修复文档中测试数量不一致

**问题描述**: 文档显示589个测试，实际为608个

**解决方案**: 更新所有文档中的测试数量

**关键文件**:
- `README.md` (3处)
- `skill-creator-mcp/README.md`
- `CLAUDE.md`

**验证方法**:
```bash
grep -rn "589.*test\|test.*589" . --include="*.md"
# 预期: 无结果（已全部更新为608）
```

**预计时间**: 15分钟

---

### P2-4: 运行完整的bandit安全扫描

**问题描述**: 未实际运行过安全扫描

**解决方案**:
```bash
cd skill-creator-mcp
uv run bandit -r src/ -f screen
```

**依赖**: P1-5

**预计时间**: 30分钟

---

### P2-5: 创建CI/CD质量检查流程

**问题描述**: 缺少完整的质量检查流程

**解决方案**: 更新或创建 `.github/workflows/quality-check.yml`

**关键文件**: `.github/workflows/quality-check.yml`

**验证方法**: 在GitHub创建测试PR，观察Actions运行

**依赖**: P1-1, P1-5, P2-1, P2-4

**预计时间**: 1小时

---

### P2-6: 文档交叉引用链接检查

**问题描述**: 需要定期检查文档链接有效性

**解决方案**: 创建链接检查脚本

**预计时间**: 1小时

---

## 四、长期规划项 (P3) - 持续改进

### P3-1: 建立定期审计机制

**解决方案**: 创建每月审计计划

### P3-2: 性能优化和监控

### P3-3: 文档国际化

---

## 五、实施时间表

### 第1周 (2026-01-27 ~ 2026-02-02)

**Day 1-2**: P0任务
- ✅ P0-1: 修复Git状态 (5分钟)
- ✅ P0-2: 处理coverage.json (5分钟)

**Day 3**: P1快速修复
- ✅ P1-1: 修复Ruff检查 (5分钟)
- ✅ P1-4: SKILL.md添加打包引用 (15分钟)
- ✅ P1-5: 安装bandit (10分钟)

**Day 4-5**: P1文档优化
- ✅ P1-2: 拆分dev-standards.md (2小时)
- ✅ P1-3: 精简packaging.md (1.5小时)

### 第2周 (2026-02-03 ~ 2026-02-09)

**Day 1-2**: P2测试优化
- ✅ P2-1: 提升测试覆盖率 (4小时)
- ✅ P2-4: 运行bandit扫描 (30分钟)

**Day 3**: P2文档和CI/CD
- ✅ P2-2: 精简cache-mechanism-advanced.md (1小时)
- ✅ P2-3: 修复测试数量文档 (15分钟)
- ✅ P2-5: 创建CI/CD流程 (1小时)

**Day 4-5**: P2验证
- ✅ P2-6: 文档链接检查 (1小时)

---

## 六、关键文件清单

### 需要修改的文件

**Git相关**:
- `.claude/plans/streamed-hopping-lecun.md` (删除)
- `.claude/plans/archive/streamed-hopping-lecun.md` (添加)
- `.claude/plans/archive/wise-tinkering-crab.md` (添加)
- `skill-creator-mcp/.gitignore` (添加coverage.json)

**代码修复**:
- `skill-creator-mcp/src/skill_creator_mcp/models/skill_config.py` (删除未使用导入)
- `skill-creator-mcp/tests/test_tools/test_config.py` (删除未使用导入)

**文档优化**:
- `skill-creator/references/dev-standards.md` (拆分)
- `skill-creator/references/dev-standards-workflow.md` (新建)
- `skill-creator/references/dev-standards-git.md` (新建)
- `skill-creator/references/dev-standards-documentation.md` (新建)
- `skill-creator/references/packaging.md` (精简)
- `skill-creator/references/cache-mechanism-advanced.md` (精简)
- `skill-creator/SKILL.md` (添加打包引用)
- `skill-creator/examples/packaging-basic.md` (新建)
- `skill-creator/examples/packaging-advanced.md` (新建)

**测试补充**:
- `skill-creator-mcp/tests/test_utils/test_path_helpers.py` (补充测试)
- `skill-creator-mcp/tests/test_utils/test_testing.py` (补充测试)
- `skill-creator-mcp/tests/test_utils/test_packagers.py` (补充测试)

**文档更新**:
- `README.md` (更新测试数量)
- `skill-creator-mcp/README.md` (更新测试数量)
- `CLAUDE.md` (检查并更新)

**CI/CD**:
- `.github/workflows/quality-check.yml` (新建或更新)

---

## 七、验收标准

### P0任务验收

```bash
git status
# 预期: 无未提交的删除操作，coverage.json不被跟踪
```

### P1任务验收

```bash
# Ruff检查
cd skill-creator-mcp && uv run ruff check .
# 预期: 0 errors

# 文档长度
wc -l skill-creator/references/*.md | sort -n | tail -5
# 预期: 所有文件 ≤300行

# 打包引用
grep -n "打包" skill-creator/SKILL.md
# 预期: 找到相关引用

# bandit安装
cd skill-creator-mcp && uv run bandit --version
# 预期: 输出版本号
```

### P2任务验收

```bash
# 测试覆盖率
cd skill-creator-mcp && uv run pytest --cov --cov-report=term-missing
# 预期: 所有模块 ≥90%

# 测试数量一致
grep -rn "589\|608" . --include="*.md"
# 预期: 全部显示608

# bandit扫描
cd skill-creator-mcp && uv run bandit -r src/ -f screen
# 预期: No issues identified
```

---

## 八、成功指标

### 定量指标

- **代码质量**: Ruff 0错误, Mypy 0错误, Bandit 0高危
- **测试覆盖率**: 95.4% → 96%+ (所有模块 ≥90%)
- **文档质量**: 所有引用文档 ≤300行
- **CI/CD**: 100%自动化检查通过

### 定性指标

- **开发体验**: 更清晰的文档结构
- **维护效率**: 更容易找到相关文档
- **代码健康**: 更高的测试覆盖率和安全性
- **团队协作**: 更规范的Git流程

---

## 九、总结

本优化改进计划基于三个全面审核报告的优秀结果，共16个改进项：

- **P0级**: 2项 - Git状态修复
- **P1级**: 5项 - 代码质量和文档优化
- **P2级**: 6项 - 测试和CI/CD改进
- **P3级**: 3项 - 长期持续改进

预计总工期2周，投入约15小时。

---

## 十、审核依据

本计划基于以下三个全面审核报告：

1. **项目整体结构和Git状态审核** (93/100 优秀)
2. **skill-creator Agent-Skill审核** (5/5 优秀)
3. **skill-creator-mcp MCP Server审核** (5/5 优秀)

审核发现项目状态优秀，存在少量可优化的中低优先级问题。本计划旨在解决这些问题，进一步提升项目质量。
