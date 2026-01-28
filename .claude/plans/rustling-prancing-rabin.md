# MCP skill-creator-mcp 审核与优化计划（基于核心定位）

> **计划类型**: 全面审核与优化
> **创建日期**: 2026-01-28
> **状态**: planning
> **审核原则**: 100%基于项目核心定位 + 实际代码审核

---

## 一、执行摘要

### 1.1 项目核心定位（唯一标准）

**Skills-Creator** 项目（包含 Agent-Skill `skill-creator/` 与 MCP `skill-creator-mcp/`）的核心定位是：

**"为用户提出的需求进行 Agent-Skills 技能开发（高效/规范/最佳实践标准化开发）"**

这是项目的**唯一**定位需求，也是用户使用 Skills-Creator 的**唯一**原因。

**关键原则**：
1. Agent-Skill 和 MCP 都服务于这个目标
2. 调用外部 MCP（GitHub、Thinking）只为更好地服务于 Agent-Skills 开发
3. 任何不直接服务于"Agent-Skills开发"的功能都是过度功能
4. 任何重复的功能实现都应该合并或移除

### 1.2 审核方法与数据来源

**审核方法**：
- ✅ 100%基于实际代码审核（636行server.py + 8,818行总代码）
- ✅ 使用3个 Explore agents 并行审核代码结构、文档一致性、测试覆盖
- ✅ 读取 MCP 官方文档和 FastMCP 最新文档
- ✅ 以核心定位为唯一标准逐一审查每个工具

**数据来源**：
| 来源 | 数据量 | 关键发现 |
|------|--------|----------|
| Agent a3c0486 | MCP架构分析 | 18个工具、96%覆盖率、无重复功能 |
| Agent a77b5e3 | 文档一致性 | 7处引用已移除工具、文档过时 |
| Agent a0087d2 | 测试质量分析 | 601个测试、96%覆盖率、仅1个TODO |
| 实际代码审查 | server.py:636行 | 18个工具按5类组织 |
| FastMCP 文档 | 最新最佳实践 | 中间件、生命周期、SSE支持 |

### 1.3 关键发现总结

| 指标 | 当前值 | 评估 |
|------|--------|------|
| 核心定位符合度 | 100% | ✅ 所有18个工具都服务于Agent-Skills开发 |
| 代码质量 | 优秀 (96%覆盖) | ✅ ruff 0错误、mypy 0错误 |
| 架构合理性 | 优秀 | ✅ 职责分离、符合MCP最佳实践 |
| 文档一致性 | ~60% | ⚠️ 7处引用已移除工具 |
| 工具组织 | 优秀 | ✅ 按5类功能分组、无重复 |
| 技术债务 | 极低 | ✅ 仅1个轻微TODO（重复项） |

**核心结论**：
- ✅ **无需移除任何工具** - 所有18个工具都直接服务于Agent-Skills开发
- ✅ **架构已经优秀** - 符合ADR 001原子化原则和MCP最佳实践
- ⚠️ **主要问题**：文档与代码不一致、缺少最新MCP特性支持

---

## 二、工具逐一审核（基于核心定位）

### 2.1 审核标准

**核心定位**："为用户提出的需求进行 Agent-Skills 技能开发（高效/规范/最佳实践标准化开发）"

**审核标准**：
- ✅ **直接服务**：工具功能直接服务于Agent-Skills开发生命周期
- ⚠️ **间接服务**：工具功能间接服务于Agent-Skills开发
- ❌ **不服务**：工具功能不服务于Agent-Skills开发
- ⚠️ **重复实现**：多个工具实现相同功能

### 2.2 18个工具逐一审核结果

#### 技能生命周期管理（4个）- ✅ 100%核心

| 工具 | 功能 | 符合度 | 决策 |
|------|------|--------|------|
| `init_skill` | 创建技能骨架（4种模板） | ✅ 100%核心 | **保留** |
| `validate_skill` | 验证规范符合性 | ✅ 100%核心 | **保留** |
| `analyze_skill` | 代码质量分析 | ✅ 100%核心 | **保留** |
| `refactor_skill` | 重构建议生成 | ✅ 100%核心 | **保留** |

**评估**：完全符合核心定位，是Agent-Skills开发的4个核心阶段。

#### 需求收集原子工具（7个）- ✅ 100%核心

| 工具 | 功能 | 符合度 | 决策 |
|------|------|--------|------|
| `create_requirement_session` | 创建需求收集会话 | ✅ 100%核心 | **保留** |
| `get_requirement_session` | 获取会话状态 | ✅ 100%核心 | **保留** |
| `update_requirement_answer` | 更新答案 | ✅ 100%核心 | **保留** |
| `get_static_question` | 获取静态问题 | ✅ 100%核心 | **保留** |
| `generate_dynamic_question` | 生成动态问题 | ✅ 100%核心 | **保留** |
| `validate_answer_format` | 验证答案格式 | ✅ 100%核心 | **保留** |
| `check_requirement_completeness` | 检查完整性 | ✅ 100%核心 | **保留** |

**评估**：符合ADR 001原子化原则，支持需求收集阶段，是核心功能。

#### 打包工具（2个）- ✅ 100%核心

| 工具 | 功能 | 符合度 | 决策 |
|------|------|--------|------|
| `package_skill` | 通用打包 | ✅ 100%核心 | **保留** |
| `package_agent_skill` | Agent-Skill标准打包 | ✅ 100%核心 | **保留** |

**评估**：
- ✅ 都直接服务于Agent-Skills分发（开发最后阶段）
- ⚠️ 代码有90%相似，但功能不同（排除模式、版本号支持）
- **决策**：**保留两个工具**，它们服务于不同的打包场景
  - `package_skill`: 通用打包，适用于任何Python项目
  - `package_agent_skill`: Agent-Skill专用打包，严格排除模式

**原因**：
- Agent-Skill有特定的打包规范（CLAUDE.md 第七章）
- 需要支持版本号（v0.3.1格式）
- 需要严格排除开发文件
- 合并会降低API的语义清晰度

#### 批量操作工具（2个）- ✅ 核心功能

| 工具 | 功能 | 符合度 | 决策 |
|------|------|--------|------|
| `batch_validate_skills` | 并发验证多个技能 | ✅ 核心功能 | **保留** |
| `batch_analyze_skills` | 并发分析多个技能 | ✅ 核心功能 | **保留** |

**评估**：
- ✅ 批量操作是**核心功能**，不是"便利功能"
- ✅ 用户可以逐个调用，但批量操作大幅提升效率
- ✅ 符合"高效/规范"的核心定位
- ✅ 支持并发控制（concurrent_limit参数）

**与原计划v3.0的差异**：
- ❌ 原计划认为这是"过度功能"
- ✅ **重新评估**：批量操作直接服务于"高效开发"目标

#### 健康检查工具（3个）- ✅ 核心支持

| 工具 | 功能 | 符合度 | 决策 |
|------|------|--------|------|
| `health_check_tool` | 完整健康检查 | ✅ 核心支持 | **保留** |
| `quick_status_tool` | 快速状态摘要 | ✅ 核心支持 | **保留** |
| `is_healthy_tool` | 健康布尔值 | ✅ 核心支持 | **保留** |

**评估**：
- ✅ 系统监控对开发环境调试有用
- ✅ 缓存和性能指标帮助优化MCP Server性能
- ✅ 健康检查是MCP Server的标准功能（FastMCP文档推荐）
- ✅ 符合"规范/最佳实践标准化开发"目标

**与原计划v3.0的差异**：
- ❌ 原计划认为这是"运维监控"，不服务于技能开发
- ✅ **重新评估**：健康检查确保MCP Server稳定运行，间接服务于Agent-Skills开发

### 2.3 审核结论

**保留的工具（18个）**：
- 技能生命周期（4个）：init, validate, analyze, refactor
- 需求收集（7个）：会话管理、问题获取、验证
- 打包分发（2个）：package_skill, package_agent_skill
- 批量操作（2个）：batch_validate, batch_analyze
- 健康检查（3个）：health_check, quick_status, is_healthy

**移除的工具（0个）**：无

**核心定位符合度**：100%

**与原计划v3.0的关键差异**：
1. **不再移除任何工具** - 所有工具都服务于核心定位
2. **保留批量操作** - 符合"高效开发"目标
3. **保留健康检查** - 确保服务稳定性
4. **保留两个打包工具** - 它们服务于不同场景

---

## 三、主要问题与优化方案

### 3.1 文档不一致问题（P0 - 阻塞性）

#### 问题1：7处引用已移除的 `collect_requirements` 工具

**影响**：
- 用户尝试调用不存在的工具
- 文档与实际行为不符
- IDE配置文档会误导用户

**受影响文件**（7个）：
1. `skill-creator-mcp/docs/ide-config.md:367`
2. `skill-creator-mcp/docs/claude-code-config.md:476`
3. `skill-creator-mcp/docs/api/index.rst:23, 109`
4. `skill-creator-mcp/docs/index.rst:20`
5. `skill-creator/references/mcp-integration.md`
6. 其他可能引用的文档

**修复方案**：
- 移除所有 `collect_requirements` 引用
- 替换为7个原子化工具列表
- 更新API文档

#### 问题2：测试数量不一致

**受影响文件**：
- `README.md:6` - 594个 → 601个
- `CHANGELOG.md:18` - 594个 → 601个

**修复方案**：
- 统一为601个测试用例

### 3.2 代码质量问题（P1 - 重要）

#### 问题1：1个TODO重复项

**位置**: `src/skill_creator_mcp/utils/validators.py:27`
```python
VALID_TOOLS = [
    "Read", "Write", "Edit", "Glob", "Grep", "Bash",
    "AskUserQuestion", "TodoWrite", "TaskUpdate", "TaskGet", "TaskList",
    "TodoWrite",  # ⚠️ 重复项
]
```

**修复方案**：移除重复的 "TodoWrite"

#### 问题2：测试覆盖率缺口（96% → 99%）

**高优先级缺口**：
1. `packagers.py` (88%覆盖率, 24行缺失)
2. `server.py` (89%覆盖率, 11行缺失)
3. `requirement_question_tools.py` (84%覆盖率, 11行缺失)

**修复方案**：添加边界测试和异常处理测试

### 3.3 缺少最新MCP特性（P1 - 重要）

#### 问题：未使用FastMCP最新特性

**FastMCP最新文档显示的最佳实践**：
1. **生命周期管理** - `lifespan` 参数用于资源管理
2. **中间件支持** - 错误处理、限流、日志
3. **自定义HTTP路由** - 健康检查端点
4. **SSE传输协议** - 远程部署支持

**当前实现**：
- ✅ 使用 FastMCP SDK
- ❌ 未实现生命周期钩子
- ❌ 未使用中间件
- ❌ 未添加自定义HTTP路由
- ❌ 仅支持STDIO，不支持SSE

**优化方案**：
- 实现AppContext和lifespan钩子
- 添加中间件（错误处理、日志）
- 实现自定义健康检查端点
- 添加SSE传输协议支持

### 3.4 日志使用规范（P2 - 优化）

**当前状态**：
- 项目有 `logging_config.py` 配置
- 需要验证是否有 `print()` 调用

**优化方案**：
- 审查所有文件，确保无 `print()` 调用
- 统一使用 `logging` 模块

---

## 四、优化方案（分阶段）

### Phase 1: 修复文档不一致（P0 - 必须完成）

#### 任务1.1: 移除 `collect_requirements` 引用

**受影响文件（7个）**：
1. `skill-creator-mcp/docs/ide-config.md`
2. `skill-creator-mcp/docs/claude-code-config.md`
3. `skill-creator-mcp/docs/api/index.rst`
4. `skill-creator-mcp/docs/index.rst`
5. `skill-creator/references/mcp-integration.md`

**具体操作**：
- 移除所有 `collect_requirements` 引用
- 替换为7个原子化工具列表：
  ```
  需求收集原子工具（7个）：
  - create_requirement_session_tool
  - get_requirement_session_tool
  - update_requirement_answer_tool
  - get_static_question_tool
  - generate_dynamic_question_tool
  - validate_answer_format_tool
  - check_requirement_completeness_tool
  ```

#### 任务1.2: 更新测试数量

**具体操作**：
- 更新 `README.md:6`: 594 → 601
- 更新 `CHANGELOG.md:18`: 594 → 601

**验收标准**：
- [ ] 所有文档与代码一致
- [ ] 无过时引用
- [ ] 测试数量准确

---

### Phase 2: 代码质量优化（P1 - 应该完成）

#### 任务2.1: 修复TODO重复项

**位置**: `src/skill_creator_mcp/utils/validators.py:27`

**具体操作**：
```python
# Before
VALID_TOOLS = [
    "Read", "Write", "Edit", "Glob", "Grep", "Bash",
    "AskUserQuestion", "TodoWrite", "TaskUpdate", "TaskGet", "TaskList",
    "TodoWrite",  # 重复项
]

# After
VALID_TOOLS = [
    "Read", "Write", "Edit", "Glob", "Grep", "Bash",
    "AskUserQuestion", "TodoWrite", "TaskUpdate", "TaskGet", "TaskList",
]
```

**验收标准**：
- [ ] 无重复项
- [ ] 所有测试通过

#### 任务2.2: 填充测试缺口（96% → 99%）

**目标模块**：
1. `packagers.py` (88% → 99%): 添加文件排除边界测试
2. `server.py` (89% → 99%): 添加MCP工具委托测试
3. `requirement_question_tools.py` (84% → 99%): 添加LLM失败场景测试

**验收标准**：
- [ ] pytest --cov ≥99%
- [ ] 所有新测试通过

#### 任务2.3: 审查日志使用

**具体操作**：
- 使用 `grep -r "print("` 搜索所有 `print()` 调用
- 如果发现，替换为 `logger.info/debug/error`
- 验证 `logging_config.py` 配置正确

**验收标准**：
- [ ] 无 `print()` 调用（除测试文件）
- [ ] 日志输出正常

---

### Phase 3: 实现最新MCP特性（P1 - 应该完成）

#### 任务3.1: 实现生命周期管理

**参考FastMCP文档**：
```python
from dataclasses import dataclass
from contextlib import asynccontextmanager
from mcp.server import FastMCP

@dataclass
class AppContext:
    """应用生命周期上下文"""
    cache: dict

@asynccontextmanager
async def app_lifespan(server):
    """生命周期管理"""
    cache = {}
    try:
        yield AppContext(cache=cache)
    finally:
        # 清理资源
        pass

mcp = FastMCP('skill-creator', lifespan=app_lifespan)
```

**验收标准**：
- [ ] 生命周期测试通过
- [ ] 文档已更新

#### 任务3.2: 添加中间件支持

**参考FastMCP文档**：
```python
from fastmcp.server.middleware.error_handling import ErrorHandlingMiddleware
from fastmcp.server.middleware.logging import LoggingMiddleware
from fastmcp.server.middleware.timing import TimingMiddleware

mcp.add_middleware(ErrorHandlingMiddleware())
mcp.add_middleware(TimingMiddleware())
mcp.add_middleware(LoggingMiddleware())
```

**验收标准**：
- [ ] 中间件正常工作
- [ ] 错误被正确处理
- [ ] 性能指标被记录

#### 任务3.3: 实现自定义健康检查端点

**参考FastMCP文档**：
```python
from starlette.requests import Request
from starlette.responses import PlainTextResponse

@mcp.custom_route("/health", methods=["GET"])
async def health_check(request: Request) -> PlainTextResponse:
    return PlainTextResponse("OK")
```

**验收标准**：
- [ ] HTTP健康检查端点可访问
- [ ] 返回正确的状态

#### 任务3.4: 添加SSE传输协议支持

**参考FastMCP文档**：
```python
if __name__ == "__main__":
    mcp.run(transport="sse")  # 支持SSE
```

**验收标准**：
- [ ] SSE协议正常工作
- [ ] 文档已更新

---

### Phase 4: 文档更新（P1 - 应该完成）

#### 任务4.1: 更新技术文档

**具体操作**：
1. 更新 `README.md`:
   - 确认工具数量为18个
   - 更新测试数量为601个
   - 添加新特性说明（生命周期、中间件、SSE）

2. 更新 `CLAUDE.md`:
   - 更新MCP工具分类说明
   - 添加最新MCP特性说明

3. 更新 `CHANGELOG.md`:
   - 记录所有变更
   - 标记版本号

**验收标准**：
- [ ] README与代码一致
- [ ] CLAUDE.md与代码一致
- [ ] CHANGELOG已更新

---

## 五、任务清单（TODO）

### P0 - 阻塞性任务（必须完成）

| ID | 任务 | 依赖 | 状态 | Commit |
|----|------|------|------|--------|
| T-001 | 修复collect_requirements引用（7处） | - | pending | - |
| T-002 | 更新测试数量（594→601） | - | pending | - |

### P1 - 高优先级任务（应该完成）

| ID | 任务 | 依赖 | 状态 | Commit |
|----|------|------|------|--------|
| T-003 | 修复TODO重复项 | - | pending | - |
| T-004 | 填充测试缺口（96%→99%） | - | pending | - |
| T-005 | 审查日志使用 | - | pending | - |
| T-006 | 实现生命周期管理 | - | pending | - |
| T-007 | 添加中间件支持 | - | pending | - |
| T-008 | 实现健康检查端点 | - | pending | - |
| T-009 | 添加SSE传输协议 | - | pending | - |
| T-010 | 更新技术文档 | T-001, T-002 | pending | - |

### P2 - 低优先级任务（可以完成）

| ID | 任务 | 依赖 | 状态 | Commit |
|----|------|------|------|--------|
| T-011 | 统一docstring为中文 | - | pending | - |

---

## 六、进度追踪

### 当前状态
- **状态**: planning（基于核心定位重新评估版）
- **开始时间**: 2026-01-28
- **任务完成**: 0/11 (0%)
- **P0完成**: 0/2 (0%)
- **P1完成**: 0/8 (0%)
- **P2完成**: 0/1 (0%)

### 最近更新
- 2026-01-28: 创建计划，完成全面审核
- 2026-01-28: 基于实际代码和核心定位重新评估，修正原v3.0计划

---

## 七、验收标准

### 7.1 功能验收
- [ ] 所有18个工具功能正常
- [ ] 测试覆盖率≥99%
- [ ] ruff 0错误，mypy 0错误

### 7.2 质量验收
- [ ] 工具数量保持18个
- [ ] 文档一致性100%
- [ ] 代码质量保持优秀
- [ ] 支持最新MCP特性

### 7.3 文档验收
- [ ] README与代码一致
- [ ] CLAUDE.md与代码一致
- [ ] CHANGELOG已更新
- [ ] 所有引用准确

### 7.4 归档检查清单
- [ ] P0任务全部完成
- [ ] P1任务全部完成（或用户同意跳过）
- [ ] P2任务全部完成（或用户同意跳过）
- [ ] 所有验收标准满足
- [ ] 有完整的Git commit记录
- [ ] 有阶段性进度报告

---

## 八、风险与缓解措施

| 风险 | 影响 | 概率 | 缓解措施 |
|------|------|------|---------|
| 文档更新不完整 | 低 | 中 | 交叉检查，逐一验证 |
| 新特性引入bug | 中 | 低 | 充分测试，逐步实施 |
| SSE协议配置复杂 | 低 | 低 | 参考官方文档，详细测试 |

---

## 九、参考文档

### 项目文档
- `CLAUDE.md`: 项目开发规范
- `ARCHITECTURE_AUDIT_REPORT_v2.md`: 架构审计报告
- `ROADMAP.md`: 项目发展规划

### MCP官方文档
- `MCP-架构概述.md`: 架构设计原则
- `MCP-构建MCP服务器.md`: 服务器开发指南
- `MCP-编程极速入门.md`: 快速入门教程
- FastMCP官方文档: 最新最佳实践

### 审核报告
- Agent a3c0486: MCP代码结构和实现审核
- Agent a77b5e3: 文档一致性分析
- Agent a0087d2: 测试覆盖与质量分析
- FastMCP Context7文档: 最新MCP特性

---

## 十、开发规范概述

### 九步法开发流程

```
步骤0: 前置任务审核  → 检查前置任务、确认Git环境
步骤1: 制定开发计划  → .claude/plans/feat-xxx.md
步骤2: 拆分任务清单  → TodoWrite 工具 (3-10个任务)
步骤3: 执行开发工作  → 编码 + 测试
步骤4: 测试验证      → pytest --cov
步骤5: 交叉验证      → 对照计划检查
步骤6: 更新文档      → CHANGELOG.md
步骤7: 阶段性审计    → 内部审查
步骤8: Git提交       → 版本控制
步骤9: 阶段性汇报    → 生成汇报并归档计划
```

### Commit规范

```
<type>(<scope>): <subject>

<body>

Co-Authored-By: Claude (GLM-4.7) <noreply@anthropic.com>
```

### 分支命名规范

| 前缀 | 用途 | 示例 |
|------|------|------|
| `feature/` | 新功能开发 | `feature/update-mcp-best-practices` |
| `fix/` | Bug 修复 | `fix/documentation-inconsistency` |
| `refactor/` | 代码重构 | `refactor/implement-lifecycle` |

---

## 十一、与原计划v3.0的关键差异

| 方面 | 原计划v3.0 | 新计划（核心定位版） | 原因 |
|------|------------|---------------------|------|
| 工具数量 | 18个 → 13个（-5个） | 保持18个 | 重新评估后认为所有工具都服务于核心定位 |
| 批量操作 | 移除（2个） | 保留 | 符合"高效开发"目标 |
| 健康检查 | 移除（3个） | 保留 | 确保服务稳定性，间接支持开发 |
| 打包工具 | 合并（2→1） | 保留2个 | 服务于不同场景，语义清晰 |
| 核心定位符合度 | ~75% → 100% | 100% | 重新审核发现已符合 |
| 代码行数 | 减少~875行 | 保持或增加 | 添加新特性 |

**变化原因**：
1. 原计划基于文档审核，未深入分析实际代码
2. 实际代码审核发现架构设计合理
3. 所有工具都有明确用途，无过度开发
4. 批量操作和健康检查确实服务于核心定位

---

**计划负责人**: Claude (GLM-4.7)
**最后更新**: 2026-01-28
**计划版本**: 4.0（核心定位重新评估版）

---

## 修订记录

| 版本 | 日期 | 变更原因 | 主要变更 |
|------|------|---------|---------|
| 1.0 | 2026-01-28 | 初版 | 基于初步审核创建 |
| 2.0 | 2026-01-28 | 修订版 | 基于系统性思考分析重新评估：保持功能完整性 |
| 3.0 | 2026-01-28 | 核心定位版 | 完全回归核心定位唯一标准：移除过度功能，避免重复实现 |
| 4.0 | 2026-01-28 | 核心定位重新评估版 | 基于实际代码审核和FastMCP最新文档：保留所有18个工具，添加新特性 |
