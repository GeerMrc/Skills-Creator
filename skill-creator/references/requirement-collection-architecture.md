# 需求收集架构设计文档

> **文档版本**: v1.0
> **创建日期**: 2026-01-27
> **相关组件**: `collect_requirements` MCP工具

---

## 1. 当前架构概述

### 1.1 MCP工具: `collect_requirements`

**特性**:
- 支持4种模式: `basic`/`complete`/`brainstorm`/`progressive`
- 支持5种操作: `start`/`next`/`previous`/`status`/`complete`
- 支持2种交互模式: `elicit`（自动） / `manual`（手动）
- 使用 `ctx.set_state` 管理会话状态

**实现位置**:
- 代码: `skill-creator-mcp/src/skill_creator_mcp/utils/requirement_collection.py`
- 工具注册: `skill-creator-mcp/src/skill_creator_mcp/server.py`

### 1.2 架构特点

**循环逻辑位置**: MCP层（`_collect_with_elicit` 函数）

**原因**: 利用 `ctx.elicit()` 的MCP采样能力

**会话状态管理**: 使用 `SessionStateManager` 类集中管理

---

## 2. 架构权衡分析

### 2.1 为什么循环逻辑在MCP层？

#### 技术原因

**1. ctx.elicit() 只能在MCP层调用**

```
FastMCP 的 elicit API 是 MCP Server 级别的
├── 需要访问 MCP Context 对象
├── Agent-Skill 无法直接访问 ctx 对象
└── 必须通过 MCP 工具间接调用
```

**2. 会话状态管理需要MCP能力**

```
ctx.set_state / ctx.get_state 是 MCP Server 的能力
├── 状态持久化需要 MCP Server 支持
├── 跨会话状态管理依赖 MCP 基础设施
└── Agent-Skill 层无法直接访问
```

**3. LLM采样需要MCP上下文**

```
ctx.sample() 用于动态问题生成
├── 需要配置好的 LLM 集成
├── 依赖 MCP Server 的模型配置
└── Agent-Skill 层无法直接调用
```

### 2.2 理想架构 vs 实际架构

| 维度 | 理想架构 | 实际架构 | 权衡原因 |
|------|----------|----------|----------|
| **循环逻辑** | Agent-Skill层 | MCP层 | `elicit` API限制 |
| **状态管理** | Agent-Skill层 | MCP层 | `ctx.set_state` API |
| **LLM采样** | Agent-Skill层 | MCP层 | `ctx.sample` API |
| **职责边界** | 清晰分离 | 部分模糊 | 技术约束 |
| **可复用性** | 高 | 中等 | 工作流绑定在MCP |
| **用户体验** | 需多次调用 | 一次调用完成 | 便利性权衡 |

### 2.3 影响评估

#### 优点

- ✅ **充分利用MCP Server的高级API**
  - `elicit`: 结构化用户输入
  - `state`: 会话持久化
  - `sample`: LLM采样

- ✅ **用户体验好**
  - 一次调用完成整个收集流程
  - 自动处理会话中断恢复
  - 无需Agent-Skill层编排

- ✅ **会话中断恢复**
  - 使用 `ctx.state` 持久化
  - 用户可随时中断和恢复
  - 状态一致性有保障

#### 缺点

- ⚠️ **职责边界模糊**
  - MCP包含工作流逻辑
  - 违反"MCP提供原子操作"原则
  - 架构一致性降低

- ⚠️ **可复用性低**
  - 其他Agent-Skill难以复用
  - 工作流绑定在MCP层
  - 定制化困难

- ⚠️ **测试复杂度**
  - 需要模拟完整的elicit循环
  - 测试依赖MCP上下文
  - 单元测试难度增加

---

## 3. 未来重构方向

### 3.1 短期优化（当前计划 - v0.3.x）

**目标**: 在保持API不变的情况下改进内部实现

#### 已完成的优化

| 任务 | 状态 | 说明 |
|------|------|------|
| 简化 `_collect_with_elicit` | ✅ 完成 | 224行 → 114行，4层嵌套 → 2层 |
| 提取状态管理逻辑 | ✅ 完成 | 创建 `SessionStateManager` 类 |
| 创建架构文档 | ✅ 完成 | 本文档 |

#### 待完成的优化

| 任务 | 优先级 | 预估时间 |
|------|--------|----------|
| 拆分模块（提高可维护性） | P1 | 2-3天 |
| 添加工作流编排示例 | P1 | 1-2天 |
| 更新需求澄清文档 | P1 | 1天 |

### 3.2 长期重构（可选 - v0.5+）

#### 前提条件

- Agent-Skill层获得访问ctx的能力
- 或 FastMCP 提供更细粒度的elicit API

#### 理想重构方案

**MCP层：提供原子操作**

```python
# 纯原子操作，无循环逻辑
mcp.requirement_start_session(mode) -> session_id
mcp.requirement_get_next_question(session_id) -> question
mcp.requirement_validate_answer(session_id, answer) -> valid
mcp.requirement_save_answer(session_id, key, value) -> success
mcp.requirement_complete_session(session_id) -> result
```

**Agent-Skill层：编排工作流**

```python
class RequirementCollectionWorkflow:
    """需求收集工作流编排器（Agent-Skill层）"""

    async def collect(self, mode: str) -> dict:
        """执行完整的需求收集工作流."""
        # 1. 启动会话
        session_id = await mcp.requirement_start_session(mode)

        # 2. 收集循环（工作流逻辑在Agent-Skill层）
        while not self.completed:
            question = await mcp.requirement_get_next_question(session_id)
            answer = await self.elicit_user_input(question)
            await mcp.requirement_save_answer(session_id, question.key, answer)

        # 3. 完成会话
        return await mcp.requirement_complete_session(session_id)

    async def elicit_user_input(self, question: Question) -> str:
        """使用Agent-Skill的elicit能力获取用户输入."""
        # Agent-Skill层可以直接调用elicit
        result = await ctx.elicit(question.prompt)
        return result.data
```

### 3.3 决策建议

#### 当前阶段（v0.3.x）

**推荐策略**: 保持现有架构，改进内部实现

**理由**:
- FastMCP的elicit API限制短期内不会改变
- 当前实现功能完整且稳定
- 用户反馈良好，无迫切需求
- 重构风险 > 收益

**行动**:
- ✅ 简化函数结构（已完成）
- ✅ 提取状态管理（已完成）
- ✅ 完善文档说明（进行中）
- 📋 拆分模块提高可维护性

#### 未来版本（v0.5+）

**评估条件**:
1. FastMCP 是否提供更细粒度的API？
2. 用户是否需要更多定制化能力？
3. 是否有多个Agent-Skill需要类似功能？

**决策树**:
```
FastMCP提供细粒度API？
├── 是 → 考虑迁移到理想架构
└── 否 → 保持当前架构

用户需要定制化？
├── 是 → 评估重构ROI
└── 否 → 保持当前架构

多个Agent-Skill复用？
├── 是 → 提取通用工作流组件
└── 否 → 保持当前架构
```

---

## 4. 测试策略

### 4.1 当前测试覆盖

**测试文件**:
- `tests/test_utils/test_requirement_collection.py` - 单元测试
- `tests/test_tools/test_collect_requirements.py` - 工具测试
- `tests/test_integration/test_requirement_collection.py` - 集成测试

**测试统计**:
- 总测试数: 65个
- 代码覆盖率: 56%
- 通过率: 100%

### 4.2 重构后测试要求

#### 保持现有测试

- ✅ 所有现有测试必须通过
- ✅ 代码覆盖率保持≥56%
- ✅ 集成测试覆盖所有模式

#### 新增测试

| 类型 | 目标 | 预估数量 |
|------|------|----------|
| SessionStateManager测试 | 测试状态管理器 | 5-10个 |
| 子函数单元测试 | 测试提取的辅助函数 | 10-15个 |
| 边界条件测试 | 测试错误处理 | 5-10个 |

### 4.3 测试金字塔

```
        /\
       /  \  E2E测试 (10%)
      /____\
     /      \  集成测试 (30%)
    /________\
   /          \  单元测试 (60%)
  /____________\
```

**说明**:
- **单元测试**: 测试单个函数和类
- **集成测试**: 测试MCP工具与上下文交互
- **E2E测试**: 测试完整的需求收集流程

---

## 5. 参考文档

### 5.1 内部文档

- [MCP集成指南](mcp-integration.md) - MCP工具使用和资源访问
- [最佳实践 - 核心](best-practices-core.md) - 基础架构和规范
- [验证规范](validation.md) - 命名、结构、内容验证规则

### 5.2 外部文档

- [FastMCP 文档](https://jlowin.github.io/fastmcp/) - FastMCP SDK 官方文档
- [MCP 规范](https://modelcontextprotocol.io/) - Model Context Protocol 规范
- [Pydantic 文档](https://docs.pydantic.dev/) - Pydantic 2.0 官方文档

### 5.3 相关代码

- `requirement_collection.py` - 需求收集工具实现
- `skill_config.py` - 数据模型定义
- `server.py` - MCP工具注册

---

## 6. 变更历史

| 版本 | 日期 | 变更说明 |
|------|------|----------|
| v1.0 | 2026-01-27 | 初始版本，记录架构权衡分析 |

---

**文档维护**: 当架构发生重大变更时，请更新本文档。
**最后更新**: 2026-01-27
