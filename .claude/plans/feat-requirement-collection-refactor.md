# 需求收集工具重构计划

> **计划日期**: 2026-01-27
> **计划类型**: 架构重构 (P0优先级)
> **状态**: planning
> **预计工期**: 10-15天
> **基于审核**: 项目全面审核报告 (96/100评分)

---

## 执行摘要

### 问题识别

`collect_requirements` 工具（1078行）违反了MCP架构原则：
- 包含复杂的工作流循环逻辑（`while not session_state.completed`）
- 职责边界模糊：MCP承担了Agent-Skill的编排职责
- 可测试性差：需要模拟完整的对话循环

### 重构方案

采用**渐进式重构**（方案B），分3个阶段执行：

| 阶段 | 内容 | 优先级 | 预估时间 |
|------|------|--------|----------|
| **Phase 1.1** | 内部重构：简化函数，提取状态管理 | P0 | 3-5天 |
| **Phase 1.2** | 架构文档：解释权衡决策 | P0 | 1天 |
| **Phase 1.3** | 模块拆分：提高可维护性 | P1 | 2-3天 |
| **Phase 2** | 文档完善：工作流编排示例 | P1 | 2-3天 |
| **Phase 3** | 优化改进：错误消息、监控 | P2 | 3-5天 |

---

## 一、Phase 1.1: 内部重构（P0优先级）

### 目标

在保持API不变的情况下，改进 `requirement_collection.py` 的内部实现。

### 任务1.1: 简化 `_collect_with_elicit` 函数

**当前问题**:
- 224行的单一函数
- 4层嵌套循环
- 难以理解和测试

**重构方案**:
```python
# 提取子函数，降低嵌套层次
async def _collect_with_elicit(...):
    """使用 ctx.elicit() 自动收集所有用户输入."""
    session_state = await _initialize_session(ctx, session_state, current_session_id)

    while not session_state.completed:
        step_result = await _process_single_step(
            ctx, session_state, current_session_id,
            is_dynamic_mode, all_steps, input_data
        )
        if not step_result["continue"]:
            break
        session_state = step_result["updated_state"]

    return _build_completion_result(session_state, current_session_id)
```

**验收标准**:
- [ ] 主函数从224行减少到约40行
- [ ] 嵌套层次从4层降低到2层
- [ ] 新增 `_process_single_step` 子函数
- [ ] 新增 `_initialize_session` 子函数
- [ ] 新增 `_elicit_with_retry` 子函数
- [ ] 所有子函数有完整测试覆盖

### 任务1.2: 提取状态管理逻辑

**当前问题**:
- 状态管理逻辑分散在多个函数中
- `ctx.set_state` 调用重复

**重构方案**:
```python
# 新增状态管理辅助类
class SessionStateManager:
    """会话状态管理器."""

    def __init__(self, ctx: Context, session_id: str):
        self.ctx = ctx
        self.session_id = session_id
        self._state: SessionState | None = None

    async def load(self) -> SessionState:
        """加载会话状态."""

    async def save(self) -> None:
        """保存会话状态."""

    async def update(self, **updates) -> None:
        """更新会话状态字段."""
```

**验收标准**:
- [ ] 新增 `SessionStateManager` 类
- [ ] 状态管理逻辑集中化
- [ ] 减少 `ctx.set_state` 重复调用
- [ ] 新增状态管理器测试

### 任务1.3: 保持向后兼容

**要求**:
- [ ] 现有API保持不变
- [ ] 所有现有测试通过
- [ ] 代码覆盖率保持≥95%

---

## 二、Phase 1.2: 架构文档（P0优先级）

### 任务2.1: 创建架构权衡文档

**文件**: `skill-creator/references/requirement-collection-architecture.md`

**内容结构**:
```markdown
# 需求收集架构设计文档

## 1. 当前架构概述
### 1.1 MCP工具特性
### 1.2 架构特点

## 2. 架构权衡分析
### 2.1 为什么循环逻辑在MCP层？
### 2.2 理想架构 vs 实际架构
### 2.3 影响评估

## 3. 未来重构方向
### 3.1 短期优化（当前计划）
### 3.2 长期重构（可选）
### 3.3 决策建议

## 4. 测试策略
```

**验收标准**:
- [ ] 文档创建完成
- [ ] 包含当前架构概述
- [ ] 包含权衡分析对比表
- [ ] 包含技术原因说明（elicit API限制）
- [ ] 包含未来重构方向
- [ ] 所有交叉引用链接有效

---

## 三、Phase 1.3: 模块拆分（P1优先级）

### 任务3.1: 创建新模块结构

**当前结构**:
```
utils/
└── requirement_collection.py (1079行)
```

**目标结构**:
```
utils/
├── requirement_collection/
│   ├── __init__.py          # 导出接口
│   ├── session_manager.py    # 会话状态管理（150行）
│   ├── question_generator.py # 问题生成逻辑（200行）
│   ├── answer_validator.py   # 答案验证（100行）
│   ├── workflow.py           # 工作流编排（250行）
│   └── llm_functions.py      # LLM调用函数（200行）
└── requirement_collection.py # 向后兼容包装（100行）
```

### 任务3.2: 模块职责划分

| 模块 | 职责 | 预估行数 |
|------|------|----------|
| `session_manager.py` | 会话状态管理 | 150行 |
| `question_generator.py` | 问题生成逻辑 | 200行 |
| `answer_validator.py` | 答案验证 | 100行 |
| `workflow.py` | 工作流编排 | 250行 |
| `llm_functions.py` | LLM调用函数 | 200行 |

**验收标准**:
- [ ] `utils/requirement_collection/` 目录创建
- [ ] 所有模块创建完成
- [ ] 每个模块职责单一
- [ ] 原始文件改为向后兼容包装
- [ ] 所有导入路径更新
- [ ] 代码覆盖率保持≥95%

---

## 四、Phase 2: 文档完善（P1优先级）

### 任务4: 添加工作流编排示例

**文件**: `skill-creator/examples/workflow-orchestration.md`

**内容**:
- MCP工具与Agent-Skill职责分工
- 技能创建完整工作流示例
- `collect_requirements` 的特殊性说明

### 任务5: 更新需求澄清文档

**文件**: `skill-creator/references/requirement-collection.md`

**更新内容**:
- 添加架构权衡说明章节
- 引用新的架构文档
- 说明未来重构方向

---

## 五、Phase 3: 优化改进（P2优先级）

### 任务6: 改进错误消息

**目标**: 统一错误格式，添加可执行建议

### 任务7: 添加性能监控

**目标**: 集成OpenTelemetry追踪（可选）

### 任务8: 文档化缓存行为

**目标**: 说明资源访问的缓存策略

---

## 六、验收标准

### 整体质量标准

- [ ] Ruff 0错误
- [ ] MyPy 0错误
- [ ] 所有测试通过（现有+新增）
- [ ] 代码覆盖率≥95%
- [ ] 所有文档链接有效
- [ ] CHANGELOG.md 更新

### 分阶段验收

详见各章节的验收标准清单。

---

## 七、风险评估

| 风险 | 影响 | 概率 | 缓解措施 |
|------|------|------|----------|
| 重构破坏现有功能 | 高 | 中 | 完整测试覆盖，渐进式重构 |
| 用户需要适配代码 | 中 | 高 | 提供迁移指南，保持向后兼容 |
| 测试覆盖下降 | 中 | 低 | 每次重构后验证覆盖率 |

---

## 八、技术背景

### 为什么循环逻辑在MCP层？

**技术原因**:
1. **ctx.elicit() 只能在MCP层调用**
   - FastMCP的elicit API是MCP Server级别的
   - Agent-Skill无法直接访问ctx对象

2. **会话状态管理需要MCP能力**
   - ctx.set_state / ctx.get_state 是MCP Server的能力
   - 状态持久化需要MCP Server支持

3. **LLM采样需要MCP上下文**
   - ctx.sample() 用于动态问题生成
   - 需要MCP Server的LLM集成

### 架构权衡

| 维度 | 理想架构 | 实际架构 | 权衡原因 |
|------|----------|----------|----------|
| 循环逻辑 | Agent-Skill层 | MCP层 | elicit API限制 |
| 状态管理 | Agent-Skill层 | MCP层 | ctx.set_state API |
| LLM采样 | Agent-Skill层 | MCP层 | ctx.sample API |

---

## 九、参考资料

- `CLAUDE.md` - 项目开发规范
- `ARCHITECTURE_AUDIT_REPORT_v2.md` - 架构审计报告
- `skill-creator/references/mcp-integration.md` - MCP集成指南
- FastMCP文档: https://jlowin.github.io/fastmcp/

---

**计划创建**: 2026-01-27
**预计开始**: 待步骤2任务拆分完成后
**预计完成**: 2026-02-10（约10-15天）
