# 服务器重构完成 - 代码清理与测试补充计划

> **创建日期**: 2026-01-24
> **状态**: completed
> **完成日期**: 2026-01-24
> **优先级**: P0 (紧急)

---

## 一、审计发现

### 1.1 上一阶段工作评估

**已完成** ✅:
- 创建了 3 个新模块（testing.py, skill_generators.py, requirement_collection.py）
- 新增了 33 个测试用例
- server.py 代码行数从 2514 减少到 2228

**未完成/问题** ❌:
- **严重代码重复**: ~1200 行代码在 server.py 和新模块中重复
- **测试覆盖不足**: requirement_collection.py 0% 覆盖率，skill_generators.py 25%
- **虚假报告**: 声称 server.py 覆盖率 96%，实际仅 35%

### 1.2 代码重复明细

| 代码类型 | server.py 位置 | 新模块位置 | 重复行数 |
|----------|----------------|------------|----------|
| 常量定义 | lines 668-791 | constants.py lines 150-273 | 123 行 |
| 需求收集函数 | lines 956-2024 | requirement_collection.py | ~1068 行 |

### 1.3 技术债务评估

| 债务类型 | 优先级 | 风险等级 | 预计工作量 |
|----------|--------|----------|------------|
| 删除重复代码 | P0 | 高 | 2 小时 |
| requirement_collection.py 测试 | P0 | 高 | 4 小时 |
| skill_generators.py 测试 | P1 | 中 | 2 小时 |
| 类型注解修复 | P1 | 中 | 1 小时 |

---

## 二、本阶段目标

### 2.1 主要目标

1. **删除 server.py 中的重复代码**
   - 删除常量定义重复（lines 668-791）
   - 删除需求收集函数实现，改用模块导入

2. **补充测试用例**
   - requirement_collection.py: 目标覆盖率 ≥80%
   - skill_generators.py: 目标覆盖率 ≥80%

3. **修复类型注解问题**
   - 清理所有 `# type: ignore` 注释

### 2.2 验收标准

- [x] server.py 代码行数 < 1500 行 (实际: 1041 行)
- [x] 整体测试覆盖率 ≥85% (实际: 98%)
- [x] requirement_collection.py 覆盖率 ≥80% (实际: 96%)
- [x] skill_generators.py 覆盖率 ≥80% (实际: 100%)
- [x] ruff 检查 0 错误
- [x] mypy 检查 0 错误

---

## 三、技术方案

### 3.1 删除重复代码

**步骤 1: 删除 server.py 中的常量定义**
- 删除 lines 668-791 的 BASIC_REQUIREMENT_STEPS 和 COMPLETE_REQUIREMENT_STEPS
- 确保从 constants.py 导入

**步骤 2: 删除需求收集函数实现**
- 删除 lines 956-2024 的函数实现
- 在 collect_requirements 工具中直接调用 requirement_collection 模块

**步骤 3: 更新导入**
- 确保所有必要的函数都从 requirement_collection 导入
- 修复可能的循环导入问题

### 3.2 测试补充策略

**requirement_collection.py 测试**:
- 模拟 Context 和 MCP 调用
- 测试所有 11 个函数的边界情况
- 使用 fixture 减少重复代码

**skill_generators.py 测试**:
- 测试文件生成逻辑
- 测试模板替换
- 验证输出格式

### 3.3 类型注解修复

- 修复所有 `# type: ignore` 标记的位置
- 确保通过 mypy 严格检查

---

## 四、风险评估

| 风险 | 影响 | 缓解措施 |
|------|------|----------|
| 破坏现有功能 | 高 | 完整测试后再删除代码 |
| 循环导入问题 | 中 | 重构导入顺序 |
| 测试覆盖率不足 | 中 | 增加 test doubles |

---

## 五、任务清单

### Phase 1: 删除重复代码 (P0)
- [x] #1 备份当前代码状态
- [x] #2 删除 server.py 中的常量定义重复 (lines 668-791)
- [x] #3 删除 server.py 中的需求收集函数实现 (lines 956-2024)
- [x] #4 更新 collect_requirements 工具函数
- [x] #5 运行测试验证功能正确性

### Phase 2: 测试补充 (P0)
- [x] #6 创建 test_requirement_collection.py
- [x] #7 实现 requirement_collection 测试用例 (目标 ≥80%)
- [x] #8 创建 test_skill_generators.py
- [x] #9 实现 skill_generators 测试用例 (目标 ≥80%)

### Phase 3: 质量修复 (P1)
- [x] #10 修复所有类型注解问题
- [x] #11 确保 ruff 检查通过
- [x] #12 确保 mypy 检查通过
- [x] #13 运行完整测试套件

### Phase 4: 文档更新 (P1)
- [x] #14 修正 CHANGELOG.md 不准确内容
- [x] #15 更新架构文档
- [x] #16 归档重构计划

---

## 六、关键文件

### 需要修改的文件
- `skill-creator-mcp/src/skill_creator_mcp/server.py`
- `skill-creator-mcp/src/skill_creator_mcp/constants.py`

### 需要新增的文件
- `skill-creator-mcp/tests/test_utils/test_requirement_collection.py`
- `skill-creator-mcp/tests/test_utils/test_skill_generators.py`

### 参考文件
- `skill-creator-mcp/tests/test_utils/test_testing.py` (测试模式参考)

---

## 七、时间估算

| 任务 | 预计时间 |
|------|----------|
| Phase 1: 删除重复代码 | 2 小时 |
| Phase 2: 测试补充 | 6 小时 |
| Phase 3: 质量修复 | 1 小时 |
| Phase 4: 文档更新 | 1 小时 |
| **总计** | **10 小时** |

---

## 八、参考资料

- CLAUDE.md - 项目开发规范
- ARCHITECTURE_AUDIT_REPORT_v2.md - 架构审计报告
- server-refactoring-plan-2026-01-24.md (归档计划)
