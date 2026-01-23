# Server.py 测试覆盖率提升计划

> **创建日期**: 2026-01-23
> **状态**: in_progress
> **优先级**: P1

## 目标

将 `server.py` 测试覆盖率从 79% 提升到 85%+。

## 当前状态

- **当前覆盖率**: 79% (501 行代码，107 行未覆盖)
- **目标覆盖率**: 85%+ (≤75 行未覆盖)
- **未覆盖行号**: 900, 935, 980, 1087-1130, 1202, 1226-1227, 1276-1303, 1312-1316, 1416-1421, 1432-1433, 1437-1463, 1586-1602, 1755-1756, 1822-1824, 1840-1857, 1880-1900, 1922-1953, 1974-2023, 2228

## 范围

### 包含内容
- 为 `_collect_with_elicit` 函数添加测试
- 为动态模式 (brainstorm/progressive) 添加测试
- 为 elicit 用户取消场景添加测试
- 为验证重试逻辑添加测试
- 为异常处理分支添加测试

### 不包含内容
- 重构现有代码
- 修改 server.py 的业务逻辑
- 添加新功能

## 技术依赖

- FastMCP 3.0.0b1+ 的 elicit 功能
- pytest 异步测试支持
- pytest-cov 覆盖率报告

## 未覆盖代码分析

### 1. `_collect_with_elicit` 函数 (1235-1469)
**未覆盖行数**: ~80 行
**原因**: 需要 elicit 功能的完整集成测试

**未覆盖分支**:
- brainstorm 模式的 LLM 问题生成 (1276-1288)
- progressive 模式的 LLM 问题生成 (1290-1300)
- elicit 用户取消处理 (1352-1361)
- 验证重试循环 (1337-1409)
- 对话历史更新 (1415-1421)
- 动态模式完成检查 (1430-1437)
- 异常处理 (1462-1469)

### 2. collect_requirements 边缘分支
**未覆盖行数**: ~20 行
**原因**: 动态模式的特殊返回路径未测试

**未覆盖分支**:
- _collect_with_elicit 调用路径 (900)
- 动态模式 previous 返回 (935-952)
- 已经是第一步错误返回 (980)
- 动态模式 next/complete 处理 (1087-1145)
- 动态模式默认错误 (1202-1207)
- 异常处理 (1226-1232)

## 任务清单

### Phase 1: 分析现有测试结构
- [ ] 分析 `test_fallback_scenarios.py` 的测试覆盖
- [ ] 识别可以复用的测试工具函数
- [ ] 确定需要 mock 的 MCP Context 方法

### Phase 2: 创建 elicit 模式测试套件
- [ ] 创建 `test_elicit_mode.py` 专门测试 elicit 模式
- [ ] 测试 `use_elicit=True` 的 collect_requirements 调用
- [ ] 测试用户取消 elicit 场景
- [ ] 测试验证失败重试场景

### Phase 3: 创建动态模式测试套件
- [ ] 创建 `test_dynamic_modes.py` 专门测试动态模式
- [ ] 测试 brainstorm 模式的完整流程
- [ ] 测试 progressive 模式的完整流程
- [ ] 测试动态模式的 previous/next/complete 操作

### Phase 4: 创建异常处理测试
- [ ] 测试内部异常处理分支
- [ ] 测试 LLM 调用失败的降级行为
- [ ] 测试状态存储失败的处理

### Phase 5: 覆盖率验证
- [ ] 运行完整测试套件
- [ ] 生成覆盖率报告
- [ ] 验证达到 85%+ 目标
- [ ] 更新 CI 配置（如需要）

## 验收标准

- [ ] server.py 测试覆盖率 ≥ 85%
- [ ] 所有新测试通过
- [ ] ruff 检查 0 错误
- [ ] mypy 检查 0 错误
- [ ] 现有测试不回归

## 风险评估

| 风险 | 影响 | 缓解措施 |
|------|------|----------|
| elicit 功能不稳定 | 高 | 使用 mock 模拟 elicit 行为 |
| LLM 调用依赖外部 | 中 | 使用 mock 模拟 LLM 响应 |
| 测试编写复杂 | 中 | 复用现有测试工具函数 |
| 覆盖率提升不明显 | 低 | 逐个分支覆盖，确保有效 |

## 时间估算

- Phase 1: 1 小时
- Phase 2: 3 小时
- Phase 3: 3 小时
- Phase 4: 2 小时
- Phase 5: 1 小时
- **总计**: 10 小时

## 参考资料

- `tests/test_integration/test_fallback_scenarios.py` - 现有 fallback 测试
- `src/skill_creator_mcp/server.py:1235-1469` - `_collect_with_elicit` 函数
- `src/skill_creator_mcp/server.py:750-1232` - `collect_requirements` 函数
- FastMCP 文档: https://jlowin.github.io/fastmcp/
