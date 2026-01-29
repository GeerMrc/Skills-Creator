# 工作流编排示例

> **文档版本**: v1.2
> **创建日期**: 2026-01-27
> **更新日期**: 2026-01-29
> **适用场景**: Agent-Skill与MCP工具协同工作

---

## 概述

本文档说明如何正确地编排MCP工具与Agent-Skill的工作流程，以及各自的职责边界。

---

## 1. MCP工具与Agent-Skill职责分工

### 1.1 MCP层职责（原子操作）

**核心原则**: MCP提供原子操作，不包含工作流逻辑

| 职责 | 说明 | 示例 |
|------|------|------|
| **文件I/O操作** | 文件读写、目录操作 | `init_skill`, `package_skill` |
| **数据验证** | 结构验证、格式检查 | `validate_skill` |
| **单个任务执行** | 独立的任务执行 | `analyze_skill`, `refactor_skill` |

### 1.2 Agent-Skill层职责（工作流编排）

**核心原则**: Agent-Skill编排工作流程，传递知识和最佳实践

| 职责 | 说明 | 示例 |
|------|------|------|
| **多个MCP工具的组合** | 协调多个MCP工具 | 先验证 → 再分析 → 最后打包 |
| **业务逻辑实现** | 特定领域的业务流程 | 技能创建完整流程 |
| **用户交互引导** | 渐进式披露信息 | 从简单到复杂引导用户 |

---

## 2. 标准工作流模式

### 2.1 顺序执行模式

**场景**: 需要按顺序执行多个独立操作

```python
# Agent-Skill层编排
async def create_skill_workflow(skill_name: str):
    """技能创建标准工作流."""

    # 步骤1: 收集需求
    session = await create_requirement_session_tool(mode="basic")
    # ... 通过 Agent-Skill 层收集用户输入
    answers = {"skill_name": skill_name, "template_type": "minimal"}

    # 步骤2: 初始化技能
    init_result = await init_skill(
        ctx,
        name=answers["skill_name"],
        template=answers.get("template_type", "minimal")
    )

    # 步骤3: 验证技能
    validation = await validate_skill(ctx, init_result.skill_path)

    # 步骤4: 分析质量
    analysis = await analyze_skill(ctx, init_result.skill_path)

    return {
        "skill_path": init_result.skill_path,
        "validation": validation,
        "analysis": analysis
    }
```

### 2.2 条件分支模式

**场景**: 根据验证结果决定后续操作

```python
# Agent-Skill层编排
async def quality_check_workflow(skill_path: str):
    """质量检查工作流."""

    # 步骤1: 验证结构
    validation = await validate_skill(ctx, skill_path)

    # 步骤2: 根据验证结果决定
    if not validation.valid:
        return {"success": False, "errors": validation.errors}

    # 步骤3: 验证通过，进行分析
    analysis = await analyze_skill(ctx, skill_path)

    # 步骤4: 根据分析结果决定
    if analysis.quality_score < 70:
        refactor_suggestions = await refactor_skill(ctx, skill_path)
        return {
            "success": True,
            "needs_refactor": True,
            "suggestions": refactor_suggestions
        }

    return {"success": True, "ready_to_package": True}
```

### 2.3 并行执行模式

**场景**: 多个独立操作可以同时执行

```python
# Agent-Skill层编排
async def batch_analysis_workflow(skill_paths: list[str]):
    """批量分析工作流."""

    import asyncio

    tasks = [analyze_skill(ctx, path) for path in skill_paths]
    results = await asyncio.gather(*tasks)

    return {
        "total": len(results),
        "valid": sum(1 for r in results if r.valid),
        "high_quality": sum(1 for r in results if r.quality_score >= 80),
        "details": results
    }
```

---

## 3. 需求收集工作流（7个原子化工具）

### 3.1 架构说明

需求收集功能基于**7个原子化MCP工具**：

| 工具 | 职责 |
|------|------|
| `create_requirement_session_tool` | 创建会话 |
| `get_requirement_session_tool` | 获取会话状态 |
| `update_requirement_answer_tool` | 更新答案 |
| `get_static_question_tool` | 获取预定义问题 |
| `generate_dynamic_question_tool` | 生成动态问题 |
| `validate_answer_format_tool` | 验证答案格式 |
| `check_requirement_completeness_tool` | 检查完整性 |

### 3.2 工作流示例

```python
# Agent-Skill层编排
async def collect_requirements_workflow():
    """正确的需求收集流程."""

    # 1. 创建会话
    session = await create_requirement_session_tool(mode="basic")

    # 2. Agent-Skill层循环收集答案
    answers = {}
    for i in range(5):  # basic模式5个问题
        question = await get_static_question_tool(mode="basic", step_index=i)
        # answer 由 Agent-Skill 层通过用户交互获取
        answer = "<由用户提供的答案>"

        # 验证答案
        if question.get("validation"):
            is_valid = await validate_answer_format_tool(
                answer=answer,
                validation=question["validation"]
            )
            if not is_valid["valid"]:
                continue

        # 保存答案
        await update_requirement_answer_tool(
            session_id=session["session_id"],
            question_key=question["key"],
            answer=answer
        )
        answers[question["key"]] = answer

    # 3. 检查完整性
    completeness = await check_requirement_completeness_tool(answers=answers)

    return {
        "success": True,
        "answers": answers,
        "is_complete": completeness["is_complete"]
    }
```

---

## 4. 最佳实践

### 4.1 职责分离原则

**DO ✅**:
- MCP工具: 单一职责，原子操作
- Agent-Skill: 编排工作流，传递知识

**DON'T ❌**:
- MCP工具: 包含循环逻辑或复杂业务流程
- Agent-Skill: 直接操作文件系统或执行I/O

### 4.2 错误处理

**DO ✅**:
```python
# Agent-Skill层统一错误处理
try:
    result = await mcp.some_tool(ctx, params)
    if not result["success"]:
        return handle_error(result)
except Exception as e:
    return handle_exception(e)
```

**DON'T ❌**:
```python
# MCP工具不应该处理业务逻辑错误
async def some_tool(ctx, params):
    if not valid:
        return call_another_tool()  # ❌ 不要决定是否调用其他工具
```

### 4.3 状态管理

**DO ✅**:
```python
# Agent-Skill层管理工作流状态
workflow_state = {"stage": "initialization", "data": {}}

if workflow_state["stage"] == "validation":
    result = await mcp.validate(ctx, params)
```

**DON'T ❌**:
```python
# MCP工具不应该维护跨调用状态
class ToolState:
    last_result = None  # ❌ 不要这样做
```

---

## 5. 参考文档

- [需求收集API核心参考](../references/requirement-collection-api-core.md) - 7个原子化工具的完整API
- [需求收集API示例](../references/requirement-collection-api-examples.md) - 实际使用场景和最佳实践
- [MCP集成指南](../references/mcp-integration.md) - MCP工具使用和资源访问
- [最佳实践 - 核心](../references/best-practices-core.md) - 基础架构和规范

---

**文档维护**: 随着项目演进，持续更新工作流示例。
**最后更新**: 2026-01-29
