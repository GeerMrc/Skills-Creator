# 计划：文档修正与P2任务推进

> **创建日期**: 2026-01-27
> **状态**: planning
> **优先级**: P1

---

## 一、执行摘要

基于对上一阶段工作的全面审核，发现部分任务未完全完成。本计划将：
1. 完成上一阶段的P1遗留问题
2. 继续推进ROADMAP中的P2任务

---

## 二、审核发现

### 审核结论：⚠️ 部分通过

上一阶段工作**基本完成**，但存在3个P1级别问题需要处理。

### 质量指标验证（✅ 全部通过）

| 指标 | 声明值 | 实测值 | 状态 |
|------|--------|--------|------|
| Bandit安全问题 | 0个 | 0个 | ✅ |
| 测试覆盖率 | 95% | 95.06% | ✅ |
| 测试用例数 | 608 | 608 | ✅ |
| Ruff检查 | 0错误 | 0错误 | ✅ |
| MyPy检查 | 0错误 | 0错误 | ✅ |

---

## 三、P1遗留问题修复

### 任务1：修复README.md徽章数据不一致

**文件**: `skill-creator-mcp/README.md:5-6`

**问题**:
- 第5行：Tests 徽章显示 "583 passed"，应为 "608 passed"
- 第6行：Coverage 徽章显示 "96%"，应为 "95%"

**修复内容**:
```markdown
# 修改前
[![Tests](https://img.shields.io/badge/tests-583%20passed-success)](#)
[![Coverage](https://img.shields.io/badge/coverage-96%25-brightgreen)](#)

# 修改后
[![Tests](https://img.shields.io/badge/tests-608%20passed-success)](#)
[![Coverage](https://img.shields.io/badge/coverage-95%25-brightgreen)](#)
```

---

### 任务2：提交归档计划文档

**文件**: `.claude/plans/archive/2026-01-27-doc-fix-and-p2-tasks.md`

**问题**: 计划归档文档未提交到Git

**操作**:
```bash
git add .claude/plans/archive/2026-01-27-doc-fix-and-p2-tasks.md
```

---

### 任务3：同步到远程

**状态**: 本地领先远程9个提交

**操作**:
```bash
git push origin develop
```

---

## 四、P2任务推进

### 背景

根据ROADMAP.md，以下P2任务可以继续推进：

#### 已完成的P2任务
- ✅ 配置外部化（部分完成，需补充.env模板）
- ✅ 文档重构（validation.md, mcp-integration.md）
- ✅ Docker支持
- ✅ CI/CD流程
- ✅ 高级功能（缓存机制、批量操作）
- ✅ 监控和可观测性（健康检查）
- ✅ 文档完善

#### 待执行的P2任务

| # | 任务 | 来源 | 优先级 |
|---|------|------|--------|
| 1 | 添加 .env 模板 | ROADMAP Week 2 | P2 |
| 2 | 拆分 validation.md | ROADMAP Month 1 | P2 |
| 3 | 拆分 best-practices.md | ROADMAP Month 1 | P2 |
| 4 | 实现增量分析 | ROADMAP Month 2 | P2 |
| 5 | 添加使用统计 | ROADMAP Month 2 | P2 |

---

## 五、本阶段范围

### 包含的任务

**P1遗留问题**（必须完成）:
1. 修复 README.md 徽章数据
2. 提交归档计划文档
3. 同步到远程

**P2任务**（选择性推进）:
1. 添加 .env 模板（配置外部化补充）

### 不包含的任务

- 文档拆分（validation.md, best-practices.md）- 可在后续阶段处理
- 增量分析实现 - 需要更详细的规划
- 使用统计功能 - 需求优先级较低

---

## 六、实施计划

### 步骤1：修复README.md徽章数据

**文件**: `skill-creator-mcp/README.md`

**变更**:
```diff
- [![Tests](https://img.shields.io/badge/tests-583%20passed-success)](#)
+ [![Tests](https://img.shields.io/badge/tests-608%20passed-success)](#)

- [![Coverage](https://img.shields.io/badge/coverage-96%25-brightgreen)](#)
+ [![Coverage](https://img.shields.io/badge/coverage-95%25-brightgreen](#)
```

**验证**:
- 检查徽章显示正确
- 确认链接有效

---

### 步骤2：提交归档文件

**操作**:
```bash
git add .claude/plans/archive/2026-01-27-doc-fix-and-p2-tasks.md
git commit -m "chore(plans): 归档文档修正与P2任务计划"
```

---

### 步骤3：添加 .env 模板

**文件**: `skill-creator-mcp/.env.template`

**内容**:
```bash
# MCP Server 配置
MCP_SERVER_LOG_LEVEL=INFO
MCP_SERVER_LOG_FORMAT=%(asctime)s - %(name)s - %(levelname)s - %(message)s

# 缓存配置
CACHE_ENABLED=true
CACHE_TTL=300
CACHE_MAX_SIZE=100

# 输出目录配置
SKILL_CREATOR_OUTPUT_DIR=/path/to/output

# 并发控制
BATCH_CONCURRENT_LIMIT=5
```

**相关文档更新**:
- `skill-creator-mcp/README.md` - 添加环境变量配置说明
- `CLAUDE.md` - 更新配置章节

---

### 步骤4：Git提交与同步

**提交**:
```bash
git add .
git commit -m "fix(docs): 更新README徽章数据并添加.env模板

- 修复README.md徽章：608测试，95%覆盖率
- 添加.env模板文件
- 更新配置文档"
```

**同步**:
```bash
git push origin develop
```

---

## 七、验收标准

### P1遗留问题

| # | 标准 | 验证方法 |
|---|------|----------|
| 1 | README.md 徽章数据正确 | 检查徽章显示608/95% |
| 2 | 归档文件已提交 | `git log` 包含归档提交 |
| 3 | 远程已同步 | `git status` 无领先提交 |

### P2任务

| # | 标准 | 验证方法 |
|---|------|----------|
| 1 | .env.template 存在 | 文件包含所有环境变量 |
| 2 | 文档已更新 | README.md 包含配置说明 |

---

## 八、风险与依赖

### 风险

| 风险 | 影响 | 缓解措施 |
|------|------|----------|
| 远程推送失败 | 中 | 检查网络连接，确认权限 |
| 徽章链接失效 | 低 | 验证链接有效性 |

### 依赖

- 无外部依赖
- Git 远程仓库可访问

---

## 九、技术依赖

- Python 3.10+
- Git
- 远程仓库访问权限

---

## 十、完成标准

1. ✅ README.md 徽章数据已修正
2. ✅ 归档文件已提交到Git
3. ✅ 本地提交已同步到远程
4. ✅ .env.template 已创建
5. ✅ 配置文档已更新
6. ✅ 质量检查通过（ruff, mypy, pytest）
7. ✅ CHANGELOG.md 已更新

---

## 十一、变更日志

### v0.3.4 (计划中)

**Fixed**:
- README.md 徽章数据不一致问题

**Added**:
- .env.template 配置模板

**Docs**:
- 更新环境变量配置说明
