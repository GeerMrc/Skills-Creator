# 审核计划P1任务执行方案

**计划ID**: misty-snuggling-scone
**基于**: tranquil-dreaming-hellman (项目全面审核)
**创建日期**: 2026-01-27
**计划类型**: 代码质量改进

---

## 一、执行目标

基于审核报告发现的P1高优先级问题，执行代码质量改进：

1. **P1-001**: 修复批量操作中的Mock使用 (batch_operations.py:78, 151)
2. **P1-002**: 消除Pydantic验证代码重复 (skill_tools.py, package_tools.py)
3. **P1-003**: 消除output_dir验证重复 (skill_config.py 3处)

---

## 二、任务清单

### T-20260127-001: 修复批量操作的Mock使用

**问题文件**: `skill-creator-mcp/src/skill_creator_mcp/tools/batch_operations.py`

**当前问题**:
- 在生产代码中使用 `unittest.mock.MagicMock`
- 导致无法使用真实MCP Context功能

**解决方案**:
创建轻量级Context适配器，提供必要的接口方法

**验收标准**:
- [ ] 移除MagicMock导入
- [ ] 批量操作使用真实Context
- [ ] 所有测试通过

### T-20260127-002: 消除Pydantic验证代码重复

**问题文件**: `skill_tools.py`, `package_tools.py`

**当前问题**:
- 每个工具都有相同的验证模式重复

**解决方案**:
创建通用验证装饰器或辅助函数

**验收标准**:
- [ ] 创建通用验证装饰器
- [ ] 重构所有工具使用新装饰器
- [ ] 测试覆盖率保持96%+

### T-20260127-003: 消除output_dir验证重复

**问题文件**: `skill-creator-mcp/src/skill_creator_mcp/models/skill_config.py`

**当前问题**:
- output_dir验证在3个模型中重复

**解决方案**:
创建Mixin或基类

**验收标准**:
- [ ] 创建OutputDirMixin或基类
- [ ] 重构3个模型使用Mixin
- [ ] 所有测试通过

---

## 三、执行流程

1. **使用TodoWrite创建任务清单** (3-10个任务)
2. **按优先级顺序执行**: T-001 → T-002 → T-003
3. **每完成一项立即更新TODO状态**
4. **执行测试验证**: `uv run pytest --cov`
5. **代码质量检查**: `uv run ruff check . && uv run mypy src/`
6. **更新CHANGELOG.md**
7. **Git提交**: 使用规范commit信息
8. **归档计划**

---

## 四、质量标准

| 指标 | 要求 | 当前值 |
|------|------|--------|
| 测试覆盖率 | ≥95% | 96% |
| MyPy错误 | 0 | 0 |
| Ruff警告 | 0 | 6 |

---

## 五、关键文件

- `skill-creator-mcp/src/skill_creator_mcp/tools/batch_operations.py`
- `skill-creator-mcp/src/skill_creator_mcp/tools/skill_tools.py`
- `skill-creator-mcp/src/skill_creator_mcp/tools/package_tools.py`
- `skill-creator-mcp/src/skill_creator_mcp/models/skill_config.py`
- `skill-creator-mcp/tests/`

---

**参考文档**: `tranquil-dreaming-hellman.md` (完整审核报告)
