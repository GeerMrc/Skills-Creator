# Phase 2: 代码质量优化计划

> **创建日期**: 2026-01-27
> **阶段**: Phase 2 - 代码质量优化
> **前置条件**: Phase 1 已完成
> **预计工期**: 2-3周（分3个子阶段）

---

## 一、背景与目标

### 1.1 Phase 1 审核结果

**已完成**:
- ✅ 测试数量: 614个 (100% 通过)
- ✅ Ruff: 0错误, MyPy: 0错误
- ✅ Git提交: 586d8c5

**遗留问题**:
- ⚠️ README.md 测试数量显示: 608 (应为 614)
- ⚠️ 归档文件未 add 到 git

### 1.2 P2 阶段目标

**优化方向** (用户选择):
1. **代码规范与可读性** - 优化命名、注释、函数长度
2. **性能优化** - 异步化同步I/O、减少重复计算
3. **测试与覆盖率提升** - 提升边缘模块覆盖率
4. **架构重构** - 拆分大文件、优化依赖关系

### 1.3 当前代码质量指标

| 指标 | 当前值 | 目标值 | 评级 |
|------|--------|--------|------|
| 平均文件大小 | 320行 | <200行 | C |
| 最大文件大小 | 1,354行 | <500行 | F |
| 测试覆盖率 | 95% | ≥95% | A |
| 代码重复率 | ~15% | <5% | C |
| **总体评级** | **B+** | **A** | - |

---

## 二、问题清单（优先级排序）

### P0 级别（立即修复）

| ID | 问题 | 文件 | 影响 |
|----|------|------|------|
| P0-1 | `server.py` 过长 (1,354行) | server.py | 难以维护 |
| P0-2 | `skill_config.py` 职责混乱 (792行) | models/skill_config.py | 类型不清晰 |
| P0-3 | `collect_requirements` 函数过长 (~150行) | server.py | 难以理解 |
| P0-4 | 打包函数重复度90% | utils/packagers.py | 维护成本高 |
| P0-5 | `session_manager.py` 覆盖率低 (82%) | utils/requirement_collection/ | 高风险 |

### P1 级别（本周修复）

| ID | 问题 | 文件 | 影响 |
|----|------|------|------|
| P1-1 | `packagers.py` 过长 (623行) | utils/packagers.py | 单一职责违反 |
| P1-2 | 同步I/O阻塞 | utils/refactorors.py | 性能问题 |
| P1-3 | 复杂逻辑缺乏注释 | utils/analyzers.py | 可读性差 |
| P1-4 | `packagers.py` 覆盖率不足 (88%) | utils/packagers.py | 边缘情况未测 |

### P2 级别（本月修复）

| ID | 问题 | 文件 | 影响 |
|----|------|------|------|
| P2-1 | AST遍历效率低 | utils/analyzers.py | 性能问题 |
| P2-2 | 类型忽略注释过多 (37个) | 多文件 | 类型安全弱 |
| P2-3 | 命名不规范 | 多文件 | 可读性问题 |

---

## 三、执行计划（分3个子阶段）

### 子阶段 2.1: 修复 Phase 1 遗留 + P0-5（1-2天）

**目标**:
- 修复 Phase 1 遗留问题
- 修复 `session_manager.py` 测试覆盖率

**任务清单**:
1. 修复 README.md 测试数量显示 (608 → 614)
2. 将 Phase 1 归档文件 add 到 git
3. 新增 `session_manager.py` 测试用例 (覆盖率 82% → 95%)
4. 运行完整测试套件验证

**验收标准**:
- README.md 显示 614 passed
- 所有归档文件已提交
- session_manager.py 覆盖率 ≥95%
- 614/614 测试通过

---

### 子阶段 2.2: 架构重构 - server.py 拆分（3-5天）

**目标**:
- 拆分 `server.py` (1,354行 → 多个 <300行 文件)
- 消除代码重复
- 重构 `collect_requirements`

**任务清单**:
1. 创建 `tools/` 目录结构
2. 提取技能工具到 `tools/skill_tools.py`
   - init_skill
   - validate_skill
   - analyze_skill
   - refactor_skill
3. 提取打包工具到 `tools/package_tools.py`
   - package_skill
   - package_agent_skill
   - 消除重复代码
4. 提取需求工具到 `tools/requirement_tools.py`
   - collect_requirements (重构为 <50行)
5. 提取测试工具到 `tools/test_tools.py`
   - 5个测试工具函数
6. 提取批量操作到 `tools/batch_tools.py`
7. 更新 `server.py` 导入和注册
8. 运行完整测试验证

**验收标准**:
- server.py <300行
- 各工具文件 <300行
- collect_requirements <50行
- 614/614 测试通过
- 无代码重复

---

### 子阶段 2.3: 架构重构 - 模型拆分 + 优化（3-5天）

**目标**:
- 拆分 `skill_config.py` (792行 → 4个文件)
- 拆分 `packagers.py` (623行 → 3个文件)
- 异步化同步I/O
- 提升测试覆盖率

**任务清单**:
1. 拆分 `skill_config.py`:
   - `models/input_models.py` - 输入验证
   - `models/result_models.py` - 输出结果
   - `models/data_models.py` - 数据结构
   - `models/config_models.py` - 配置相关
2. 拆分 `packagers.py`:
   - `packagers/validators.py` - 验证逻辑
   - `packagers/collectors.py` - 文件收集
   - `packagers/writers.py` - 打包写入
3. 异步化 `refactorors.py` 的同步I/O
4. 添加 `analyzers.py` 复杂逻辑注释
5. 提升 `packagers.py` 覆盖率 (88% → 95%)
6. 补充边缘情况测试

**验收标准**:
- 各模型文件 <200行
- 各打包模块 <300行
- packagers.py 覆盖率 ≥95%
- 无同步I/O阻塞
- 614/614 测试通过

---

## 四、技术方案

### 4.1 server.py 拆分方案

**新目录结构**:
```
src/skill_creator_mcp/
├── server.py              # 主入口 (~150行)
├── tools/                 # 工具模块
│   ├── __init__.py
│   ├── skill_tools.py     # 核心技能工具
│   ├── package_tools.py   # 打包工具
│   ├── requirement_tools.py  # 需求收集
│   ├── test_tools.py      # 测试工具
│   └── batch_tools.py     # 批量操作
├── models/                # 数据模型
├── utils/                 # 工具函数
├── resources/             # 资源
└── prompts/               # 提示
```

**拆分原则**:
- 每个文件 <300行
- 单一职责
- 清晰的依赖关系

### 4.2 skill_config.py 拆分方案

**拆分后结构**:
```
models/
├── input_models.py    # InitSkillInput, ValidateSkillInput, etc.
├── result_models.py   # InitResult, ValidationResult, etc.
├── data_models.py     # SessionState, RequirementStep, etc.
└── config_models.py   # SkillConfig, ValidationRule, etc.
```

**迁移路径**:
1. 创建新文件
2. 复制相关类
3. 更新导入
4. 删除原文件
5. 运行测试验证

### 4.3 collect_requirements 重构方案

**当前状态**: ~150行，4层嵌套
**目标**: <50行，2层嵌套

**重构策略**:
- 提取 `_initialize_session()`
- 提取 `_get_question_data()`
- 提取 `_process_answer()`
- 提取 `_advance_step()`

**重构后结构**:
```python
async def collect_requirements(ctx, ...):
    session = await _initialize_session(ctx, session_id, mode)
    while not session.completed:
        question = await _get_question_data(session)
        answer = await ctx.elicit(...)
        await _process_answer(session, answer)
        await _advance_step(session)
    return _build_result(session)
```

### 4.4 消除打包重复代码

**当前重复**:
- `package_skill()` (12-140行)
- `package_agent_skill()` (458-624行)

**提取公共函数**:
```python
async def _validate_and_package(
    ctx, skill_path, output_dir, format,
    exclude_patterns, include_tests, version=None
):
    # 公共验证和打包逻辑
    ...

async def package_skill(ctx, ...):
    return await _validate_and_package(...)

async def package_agent_skill(ctx, version, ...):
    return await _validate_and_package(..., version=version)
```

---

## 五、风险与缓解

| 风险 | 影响 | 缓解措施 |
|------|------|----------|
| 拆分导致导入错误 | 高 | 逐步拆分，每步测试验证 |
| 重构破坏功能 | 中 | 完整测试覆盖，增量提交 |
| 性能退化 | 低 | 基准测试，性能监控 |
| 工期延误 | 中 | 分阶段交付，优先P0 |

---

## 六、验收标准

### 代码质量指标

| 指标 | 当前 | 目标 |
|------|------|------|
| 最大文件大小 | 1,354行 | <300行 |
| 最大函数长度 | 150行 | <100行 |
| 测试覆盖率 | 95% | ≥95% |
| 代码重复率 | ~15% | <5% |
| 类型忽略数量 | 37个 | <20个 |

### 测试要求

- 所有 614 个测试通过
- 新功能必须有测试
- 边缘情况必须有测试

### 文档要求

- 更新 CHANGELOG.md
- 更新架构文档
- 更新引用文档

---

## 七、时间规划

| 子阶段 | 工期 | 开始日期 | 结束日期 |
|--------|------|----------|----------|
| 2.1 修复遗留 | 1-2天 | Day 1 | Day 2 |
| 2.2 server拆分 | 3-5天 | Day 3 | Day 7 |
| 2.3 模型拆分 | 3-5天 | Day 8 | Day 12 |
| **总计** | **7-12天** | - | - |

---

## 八、参考文档

- ARCHITECTURE_AUDIT_REPORT_v2.md - 架构审计报告
- ISSUES.md - 问题清单
- ROADMAP.md - 项目路线图
- CLAUDE.md - 开发规范（九步法）

---

**计划创建**: 2026-01-27
**下一步**: 请求用户审核并批准此计划
