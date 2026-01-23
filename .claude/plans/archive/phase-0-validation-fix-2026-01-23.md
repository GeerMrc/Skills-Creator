# Phase 0 验证结果与解决方案

> **创建日期**: 2026-01-23
> **完成日期**: 2026-01-23
> **状态**: completed
> **优先级**: P0（阻塞性任务）
> **分支**: `feature/requirement-collection`

---

## 一、问题诊断

### 1.1 测试执行结果

| 验证工具 | 状态 | 错误信息 | 根本原因 |
|---------|------|----------|----------|
| `test_llm_sampling` | ❌ | Client does not support sampling | **MCP 客户端未声明 sampling 能力** |
| `test_requirement_completeness` | ❌ | Client does not support sampling | **MCP 客户端未声明 sampling 能力** |
| `test_conversation_loop` | ❌ | object NoneType can't be used in 'await' expression | **代码错误：`ctx.get_state()` 返回值处理问题** |
| `test_user_elicitation` | ❌ | Method not found | **MCP 客户端未声明 elicitation 能力** |

### 1.2 根本原因分析

根据 [MCP 协议规范](https://modelcontextprotocol.io/specification/2025-06-18/client/sampling)：

> **Sampling 和 Elicitation 是 MCP 客户端的能力，必须在初始化时声明**：
> ```json
> {
>   "capabilities": {
>     "sampling": {},
>     "roots": {}
>   }
> }
> ```

**这意味着问题不在 FastMCP 服务器端，而在于 Claude Code 的 MCP 客户端未声明这些能力。**

### 1.3 版本信息

| 组件 | 当前版本 | 最新版本 |
|------|----------|----------|
| FastMCP | 2.14.2 | 2.14.4 |
| Claude Code | 未知 | 未知 |

---

## 二、解决方案设计

### 2.1 解决方案优先级

| 优先级 | 方案 | 说明 |
|--------|------|------|
| **P0-1** | 升级 FastMCP | 确保使用最新版本 (2.14.4) |
| **P0-2** | 添加运行时能力检测 | 检测客户端能力，提供友好错误提示 |
| **P0-3** | 修复 test_conversation_loop | 修复异步处理错误 |
| **P0-4** | 优化 collect_requirements | 添加能力检测，优雅降级 |
| **P1** | 添加完整降级方案 | 如果能力不可用，使用预设问题模板 |

### 2.2 决策流程

```
┌─────────────────────────────────────────────────────────────┐
│                    1. 升级 FastMCP 到 2.14.4                │
└─────────────────────────┬───────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────────┐
│              2. 添加运行时能力检测工具                        │
│         check_client_capabilities() → 返回能力报告            │
└─────────────────────────┬───────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────────┐
│                    3. 修复代码错误                            │
│         test_conversation_loop 的异步处理问题               │
└─────────────────────────┬───────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────────┐
│               4. 重新运行 Phase 0 验证测试                    │
│    如果能力仍不可用 → 实施 P1 降级方案（预设问题模板）          │
└─────────────────────────────────────────────────────────────┘
```

---

## 三、详细实施计划

### 3.1 P0-1: 升级 FastMCP

**命令**:
```bash
cd /models/claude-glm/Skills-Creator/skill-creator-mcp
uv pip install fastmcp==2.14.4
```

**验证**:
```bash
uv pip show fastmcp | grep Version
# 期望: Version: 2.14.4
```

---

### 3.2 P0-2: 添加运行时能力检测

**新建文件**: `src/skill_creator_mcp/utils/capability_detection.py`

```python
"""MCP 客户端能力检测."""

from typing import Any
import inspect
from fastmcp import Context


async def check_sampling_capability(ctx: Context) -> dict[str, Any]:
    """检测客户端是否支持 LLM sampling."""
    try:
        result = await ctx.sample(
            messages="test",
            max_tokens=1,
        )
        return {
            "supported": True,
            "method": "sample",
            "details": "LLM sampling is supported",
        }
    except Exception as e:
        error_msg = str(e)
        if "does not support sampling" in error_msg.lower():
            return {
                "supported": False,
                "method": "sample",
                "details": "Client does not declare sampling capability",
                "error": error_msg,
            }
        return {
            "supported": False,
            "method": "sample",
            "details": f"Unexpected error: {error_msg}",
            "error": error_msg,
        }


async def check_elicitation_capability(ctx: Context) -> dict[str, Any]:
    """检测客户端是否支持 user elicitation."""
    try:
        result = await ctx.elicit("capability check")  # type: ignore[call-arg]
        return {
            "supported": True,
            "method": "elicit",
            "details": "User elicitation is supported",
            "result_type": type(result).__name__,
        }
    except Exception as e:
        error_msg = str(e)
        if "method not found" in error_msg.lower() or "not found" in error_msg.lower():
            return {
                "supported": False,
                "method": "elicit",
                "details": "Client does not support elicitation method",
                "error": error_msg,
            }
        return {
            "supported": False,
            "method": "elicit",
            "details": f"Unexpected error: {error_msg}",
            "error": error_msg,
        }


async def get_client_capabilities(ctx: Context) -> dict[str, Any]:
    """获取客户端的所有 MCP 能力."""
    sampling_result = await check_sampling_capability(ctx)
    elicitation_result = await check_elicitation_capability(ctx)

    return {
        "sampling": sampling_result,
        "elicitation": elicitation_result,
        "summary": {
            "advanced_apis_supported": (
                sampling_result.get("supported", False) and
                elicitation_result.get("supported", False)
            ),
            "fallback_required": not (
                sampling_result.get("supported", False) and
                elicitation_result.get("supported", False)
            ),
        }
    }
```

**在 server.py 中添加工具**:

```python
@mcp.tool()
async def check_client_capabilities(ctx: Context) -> dict[str, Any]:
    """检测 MCP 客户端的能力支持情况.

    Returns:
        包含客户端能力检测结果的字典
    """
    from .utils.capability_detection import get_client_capabilities
    return await get_client_capabilities(ctx)
```

---

### 3.3 P0-3: 修复 test_conversation_loop

**位置**: `server.py:1869-1871`

**问题**: `ctx.get_state()` 可能不是协程，但代码尝试 await 它

**修复**:
```python
# 修复前
history_data = await ctx.get_state("test_conversation_history")
history = list(history_data) if history_data else []

# 修复后
import inspect
state_result = ctx.get_state("test_conversation_history")
if inspect.iscoroutine(state_result):
    history_data = await state_result
else:
    history_data = state_result
history = list(history_data) if history_data else []
```

---

### 3.4 P0-4: 优化 collect_requirements

**位置**: `server.py:877-886`（在 `use_elicit=True` 处理之前）

**添加能力检测**:
```python
# 在 use_elicit=True 之前检测能力
if use_elicit:
    from .utils.capability_detection import check_elicitation_capability
    capability = await check_elicitation_capability(ctx)
    if not capability.get("supported"):
        return {
            "success": False,
            "error": "elicit_mode_not_supported",
            "message": "当前 MCP 客户端不支持交互式输入模式。",
            "fallback_mode": "traditional",
            "traditional_usage": {
                "step_1": "调用 collect_requirements(action='start', mode='basic')",
                "step_2": "使用返回的 session_id 调用 collect_requirements(action='next', session_id='...', user_input='...')",
                "step_3": "重复步骤 2 直到所有问题完成",
            },
            "capability_error": capability.get("error"),
        }
```

---

### 3.5 P1: 完整降级方案（如果能力仍不可用）

**适用场景**: 当 `check_client_capabilities()` 返回 `advanced_apis_supported: false`

#### 降级策略

| 功能 | 原方案 | 降级方案 |
|------|--------|----------|
| LLM 动态问题生成 | `ctx.sample()` | 使用预设问题模板 |
| 用户输入收集 | `ctx.elicit()` | 传统参数传递（action="next" + user_input） |
| 需求完整性分析 | `ctx.sample()` | 固定规则检查列表 |

#### 降级代码示例

```python
def _check_requirement_completeness_fallback(answers: dict[str, str]) -> dict[str, Any]:
    """固定规则的需求完整性检查（降级方案）"""
    required_keys = ["skill_name", "skill_function", "use_cases", "template_type"]
    missing = [k for k in required_keys if k not in answers or not answers[k]]

    return {
        "is_complete": len(missing) == 0,
        "missing_info": missing,
        "suggestions": [
            "请提供技能名称（小写字母、数字、连字符）",
            "请描述技能的主要功能",
            "请描述使用场景（至少2个）",
            "请选择模板类型（minimal/tool-based/workflow-based/analyzer-based）",
        ][:len(missing)] if missing else [],
    }
```

---

## 四、验收标准

### 4.1 升级验证

| 验收项 | 命令 | 期望结果 |
|--------|------|----------|
| FastMCP 版本 | `uv pip show fastmcp \| grep Version` | 2.14.4 |
| 服务器启动 | `uv run python -m skill_creator_mcp` | 正常启动 |

### 4.2 能力检测验收

| 测试 | 期望结果 |
|------|----------|
| `check_client_capabilities()` | 返回准确的能力报告 |
| `collect_requirements(use_elicit=True)` | 如果不支持，返回友好降级提示 |

### 4.3 修复验收

| 测试 | 期望结果 |
|------|----------|
| `test_conversation_loop` | `success: true`，无异步错误 |

---

## 五、参考资料

| 资源 | 链接 |
|------|------|
| MCP Sampling 规范 | https://modelcontextprotocol.io/specification/2025-06-18/client/sampling |
| MCP Elicitation 规范 | https://modelcontextprotocol.io/specification/2025-06-18/client/elicitation |
| FastMCP Context API | https://gofastmcp.com/v2/servers/context |
| FastMCP 更新日志 | https://gofastmcp.com/v2/updates |
| MCP Sampling Guide | https://gyliu513.medium.com/mcp-sampling-architecture-workflow-and-practical-guide-a77581302388 |

---

## 六、后续决策路径

### 路径 A: 升级后能力变为可用
1. 移除或保留降级代码作为可选功能
2. 更新文档说明新功能可用
3. 执行完整 Phase 0 验证
4. 合并到 develop 分支

### 路径 B: 升级后能力仍不可用
1. 实施完整降级方案（P1 任务）
2. 更新文档说明当前限制
3. 联系 Claude Code 团队确认 roadmap
4. 评估是否需要切换到其他 MCP 客户端

---

## 七、时间估算

| 阶段 | 预估时间 |
|------|----------|
| 升级 FastMCP | 5 分钟 |
| 添加能力检测 | 30 分钟 |
| 修复异步错误 | 10 分钟 |
| 优化 collect_requirements | 20 分钟 |
| 重新验证 | 15 分钟 |
| **P0 总计** | **约 1.5 小时** |
| P1 降级方案（如需要） | +1 小时 |

---

**下一步**: 执行 P0 任务，升级 FastMCP 并添加能力检测
