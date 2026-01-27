# 文档数据修正与P2任务推进计划

> **计划编号**: 20260127-001
> **创建日期**: 2026-01-27
> **负责人**: Claude AI
> **预计工时**: 7-8小时
> **状态**: planning

---

## 一、前置任务审核结果

### 1.1 P0+P1阶段完成情况

| 任务 | 状态 | 审核依据 |
|------|------|----------|
| P0-1: 归档计划文档 | ✅ 完成 | 93个文档已归档到archive/ |
| P0-2: 处理coverage.json | ✅ 完成 | 已从Git跟踪移除 |
| P1-1: Ruff代码检查 | ✅ 完成 | All checks passed! |
| P1-2: dev-standards拆分 | ✅ 完成 | 1个主文档(382行) + 3个拆分文档 |
| P1-3: packaging精简 | ✅ 完成 | 245行 + 2个示例文档 |
| P1-4: bandit安装 | ⚠️ 部分完成 | v1.9.3已安装，发现3个安全问题 |

### 1.2 发现的质量指标偏差

| 指标 | 文档声称 | 实际情况 | 偏差 |
|------|----------|----------|------|
| 项目版本 | v0.3.2 | v0.3.3 | +1个小版本 |
| 测试数量 | 614个 | 608个 | -6个 (-1%) |
| 测试覆盖率 | 96% | 95% | -1% |
| 归档文件数 | 62个 | 93个 | +31个 |

### 1.3 bandit安全问题

| 文件 | 行号 | 严重程度 | 问题描述 |
|------|------|----------|----------|
| `cache.py` | 226 | High | MD5哈希用于缓存键 |
| `analyzers.py` | 49, 122 | Low | try-except-pass模式 |

---

## 二、当前任务目标

### 2.1 主要目标

1. **修正文档数据不一致**（P1遗留）
2. **推进P2阶段任务**
3. **修复bandit发现的安全问题**

### 2.2 交付物

- 更新后的CLAUDE.md（版本号、测试数据）
- 更新后的archive/README.md（归档文件数）
- 修复的安全问题代码
- P2阶段任务进展

---

## 三、任务清单

### 阶段1：修正文档数据（30分钟）

#### T1-1: 更新CLAUDE.md项目信息 (15分钟)
- [ ] 将版本号 v0.3.2 → v0.3.3
- [ ] 将测试数量 614 → 608
- [ ] 将覆盖率 96% → 95%
- [ ] 更新文档版本日期

**相关文件**:
- `/models/claude-glm/Skills-Creator/CLAUDE.md` (第18-20行)

---

#### T1-2: 更新archive/README.md (15分钟)
- [ ] 更新归档文件数: 62 → 93
- [ ] 更新最后更新日期: 2026-01-26 → 2026-01-27

**相关文件**:
- `/models/claude-glm/Skills-Creator/.claude/plans/archive/README.md` (第4行)

---

### 阶段2：修复bandit安全问题（1小时）

#### T2-1: 修复MD5哈希问题 (30分钟)
- [ ] 在`cache.py:226`中为MD5添加`usedforsecurity=False`参数
- [ ] 添加注释说明MD5仅用于缓存键生成，非安全场景
- [ ] 运行bandit扫描验证修复

**相关文件**:
- `/models/claude-glm/Skills-Creator/skill-creator-mcp/src/skill_creator_mcp/utils/cache.py:226`

---

#### T2-2: 改进异常处理模式 (30分钟)
- [ ] 在`analyzers.py:49,122`中替换try-except-pass
- [ ] 根据业务逻辑添加适当的异常处理（日志或特定异常）
- [ ] 运行测试验证不影响功能

**相关文件**:
- `/models/claude-glm/Skills-Creator/skill-creator-mcp/src/skill_creator_mcp/utils/analyzers.py:49,122`

---

### 阶段3：P2任务推进（5-6小时）

#### T3-1: 精简cache-mechanism-advanced.md (1小时)
- [ ] 检查当前文档行数和内容结构
- [ ] 识别可精简的内容（示例、冗长说明）
- [ ] 将示例代码提取到独立文档
- [ ] 更新主文档的交叉引用

**相关文件**:
- `/models/claude-glm/Skills-Creator/skill-creator/references/cache-mechanism-advanced.md`

---

#### T3-2: 文档交叉引用链接检查 (1小时)
- [ ] 使用grep查找所有markdown链接 `[.*](references/)`
- [ ] 验证每个链接的文件是否存在
- [ ] 修复无效链接或更新文档路径
- [ ] 生成链接检查报告

**检查范围**:
- `skill-creator/SKILL.md`
- `skill-creator/references/*.md`
- `skill-creator/examples/*.md`

---

#### T3-3: 提升测试覆盖率 (2小时)
- [ ] 运行`pytest --cov --cov-report=term-missing`
- [ ] 识别覆盖率最低的模块（当前打包工具88%、路径助手79%）
- [ ] 为低覆盖率模块添加测试用例
- [ ] 目标：整体覆盖率≥96%

**重点关注**:
- `src/skill_creator_mcp/utils/packagers.py` (当前88%)
- `src/skill_creator_mcp/utils/path_helpers.py` (当前79%)

---

#### T3-4: 创建CI/CD质量检查流程 (1小时)
- [ ] 在`.github/workflows/`中创建新的workflow文件
- [ ] 配置质量检查步骤：ruff, mypy, pytest, bandit
- [ ] 设置触发条件（push, pull_request）
- [ ] 添加报告生成和注释功能

**输出文件**:
- `.github/workflows/quality-check.yml`

---

#### T3-5: 运行完整bandit扫描并生成报告 (30分钟)
- [ ] 运行完整bandit扫描: `bandit -r src/ -f json -o bandit-report.json`
- [ ] 分析所有发现的问题
- [ ] 分类处理：High需修复，Medium评估，Low记录
- [ ] 生成扫描摘要报告

---

### 阶段4：测试验证（30分钟）

#### T4-1: 运行完整质量检查套件 (30分钟)
- [ ] `uv run ruff check .`
- [ ] `uv run mypy src/`
- [ ] `uv run pytest --cov`
- [ ] `uv run bandit -r src/`

**验收标准**:
- Ruff: 0错误
- Mypy: 0错误
- Pytest: 全部通过
- Bandit: 0 High/Medium问题

---

### 阶段5：Git提交（15分钟）

#### T5-1: 提交变更
- [ ] Review所有变更
- [ ] 创建规范的commit信息
- [ ] 推送到远程develop分支

**Commit格式**:
```
fix(docs): 更新项目质量指标数据

- 版本号: v0.3.2 → v0.3.3
- 测试数量: 614 → 608
- 覆盖率: 96% → 95%
- 归档文件数: 62 → 93

修复bandit安全问题:
- cache.py: MD5添加usedforsecurity参数
- analyzers.py: 改进异常处理模式
```

---

## 四、技术依赖

| 依赖项 | 要求 | 当前状态 |
|--------|------|----------|
| Python环境 | conda base | ✅ 满足 |
| uv工具 | 最新版本 | ✅ 满足 |
| ruff | 0错误 | ✅ 满足 |
| mypy | 0错误 | ✅ 满足 |
| pytest | 全部通过 | ⚠️ 6个失败(配置) |
| bandit | v1.9.3 | ✅ 满足 |

---

## 五、风险与缓解

| 风险 | 影响 | 概率 | 缓解措施 |
|------|------|------|----------|
| bandit修复影响功能 | 高 | 低 | 充分测试后再提交 |
| 测试覆盖率提升困难 | 中 | 中 | 优先提升最低模块 |
| 文档链接检查遗漏 | 低 | 中 | 使用脚本自动化检查 |
| CI/CD配置复杂 | 中 | 低 | 参考现有workflow模板 |

---

## 六、验收标准

### 6.1 文档数据准确性
- [ ] CLAUDE.md中版本号、测试数据与实际一致
- [ ] archive/README.md归档文件数准确

### 6.2 代码质量
- [ ] Ruff检查: 0错误
- [ ] Mypy检查: 0错误
- [ ] Bandit扫描: 0 High/Medium问题
- [ ] 测试覆盖率: ≥95%

### 6.3 功能完整性
- [ ] 所有现有测试通过
- [ ] 修复不影响现有功能
- [ ] CI/CD workflow配置正确

---

## 七、参考文档

- [CLAUDE.md](../../CLAUDE.md) - 项目开发指南
- [CHANGELOG.md](../../CHANGELOG.md) - 变更日志
- [archive/README.md](archive/README.md) - 归档索引
- [九步法开发流程](../../skill-creator/references/dev-standards-workflow.md)

---

## 八、变更记录

| 日期 | 版本 | 变更内容 | 作者 |
|------|------|----------|------|
| 2026-01-27 | 1.0 | 创建计划文档 | Claude AI |
