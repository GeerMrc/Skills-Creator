# 工作流编排示例

> **文档版本**: v1.0
> **创建日期**: 2026-01-27
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
    requirements = await collect_requirements(
        ctx,
        action="start",
        mode="basic"
    )

    # 步骤2: 初始化技能
    init_result = await init_skill(
        ctx,
        name=requirements["skill_name"],
        template=requirements["template_type"]
    )

    # 步骤3: 验证技能
    validation = await validate_skill(
        ctx,
        init_result.skill_path
    )

    # 步骤4: 分析质量
    analysis = await analyze_skill(
        ctx,
        init_result.skill_path
    )

    # 步骤5: 返回结果
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
        # 验证失败，返回错误
        return {
            "success": False,
            "errors": validation.errors
        }

    # 步骤3: 验证通过，进行分析
    analysis = await analyze_skill(ctx, skill_path)

    # 步骤4: 根据分析结果决定
    if analysis.quality_score < 70:
        # 质量低，建议重构
        refactor_suggestions = await refactor_skill(ctx, skill_path)
        return {
            "success": True,
            "needs_refactor": True,
            "suggestions": refactor_suggestions
        }

    # 质量合格，可以打包
    return {
        "success": True,
        "ready_to_package": True
    }
```

### 2.3 并行执行模式

**场景**: 多个独立操作可以同时执行

```python
# Agent-Skill层编排
async def batch_analysis_workflow(skill_paths: list[str]):
    """批量分析工作流."""

    # 并行执行多个分析任务
    import asyncio

    tasks = [
        analyze_skill(ctx, path)
        for path in skill_paths
    ]

    results = await asyncio.gather(*tasks)

    # 汇总结果
    return {
        "total": len(results),
        "valid": sum(1 for r in results if r.valid),
        "high_quality": sum(1 for r in results if r.quality_score >= 80),
        "details": results
    }
```

---

## 3. 与collect_requirements的对比

### 3.1 理想MCP工具用法

**特征**: 单次调用，返回简单结果

```python
# 理想：Agent-Skill层编排
async def collect_requirements_ideal():
    """理想的需求收集流程."""

    # Agent-Skill层循环
    while not completed:
        # 1. 获取下一个问题
        question = await mcp.requirement_get_next_question(session_id)

        # 2. 获取用户输入（Agent-Skill层的elicit）
        answer = await ctx.elicit(question.prompt)

        # 3. 验证答案
        is_valid = await mcp.requirement_validate_answer(session_id, answer)

        # 4. 保存答案
        if is_valid:
            await mcp.requirement_save_answer(session_id, question.key, answer)

    # 完成收集
    return await mcp.requirement_complete_session(session_id)
```

### 3.2 collect_requirements的特殊性

**原因**: 需要使用 `ctx.elicit()` API（MCP Server级别）

**详细说明**: 参见 [需求收集架构文档](../references/requirement-collection-architecture.md)

**实际用法**:

```python
# 实际：MCP层包含循环（因为需要ctx.elicit）
result = await mcp.collect_requirements(
    ctx,
    action="start",
    mode="basic",
    use_elicit=True  # 自动完成整个循环
)

# 一次调用完成所有收集
answers = result["answers"]
```

**对比**:

| 维度 | 理想MCP工具 | collect_requirements |
|------|------------|---------------------|
| 循环逻辑位置 | Agent-Skill层 | MCP层 |
| 调用次数 | 多次 | 一次 |
| 原因 | 架构原则 | elicit API限制 |
| 可复用性 | 高 | 中等 |

---

## 4. 完整示例：技能创建工作流

### 4.1 场景描述

用户想要创建一个新的Agent-Skill，需要：

1. 收集需求（技能名称、功能、模板类型等）
2. 初始化技能结构
3. 验证技能质量
4. 分析技能复杂度
5. 生成重构建议（如果需要）

### 4.2 Agent-Skill层实现

```python
# skill-creator/examples/complete-creation-workflow.md

async def create_new_skill_complete_workflow():
    """完整的技能创建工作流."""

    # ==================== 阶段1: 需求收集 ====================
    print("📋 阶段1: 收集需求...")

    # 使用 collect_requirements（特殊情况：MCP包含循环）
    requirements = await mcp.collect_requirements(
        ctx,
        action="start",
        mode="complete",
        use_elicit=True
    )

    if not requirements["success"]:
        return {
            "success": False,
            "stage": "requirements",
            "error": requirements["error"]
        }

    print(f"✓ 需求收集完成: {requirements['answers']['skill_name']}")

    # ==================== 阶段2: 初始化技能 ====================
    print("📦 阶段2: 初始化技能...")

    init_result = await mcp.init_skill(
        ctx,
        name=requirements["answers"]["skill_name"],
        template=requirements["answers"]["template_type"],
        with_examples=True,
        with_scripts=True
    )

    if not init_result["success"]:
        return {
            "success": False,
            "stage": "init",
            "error": init_result["error"]
        }

    skill_path = init_result["skill_path"]
    print(f"✓ 技能初始化完成: {skill_path}")

    # ==================== 阶段3: 验证技能 ====================
    print("🔍 阶段3: 验证技能...")

    validation = await mcp.validate_skill(
        ctx,
        skill_path=skill_path,
        check_structure=True,
        check_content=True
    )

    if not validation["valid"]:
        print(f"✗ 验证失败: {validation['errors']}")
        return {
            "success": False,
            "stage": "validation",
            "errors": validation["errors"]
        }

    print(f"✓ 验证通过 (结构: {validation['structure_valid']}, 内容: {validation['content_valid']})")

    # ==================== 阶段4: 分析质量 ====================
    print("📊 阶段4: 分析质量...")

    analysis = await mcp.analyze_skill(
        ctx,
        skill_path=skill_path,
        analyze_structure=True,
        analyze_complexity=True,
        analyze_quality=True
    )

    quality_score = analysis["quality_score"]
    print(f"✓ 质量分析完成 (评分: {quality_score}/100)")

    # ==================== 阶段5: 生成建议（可选） ====================
    refactor_suggestions = None
    if quality_score < 80:
        print("💡 阶段5: 生成重构建议...")

        refactor_result = await mcp.refactor_skill(
            ctx,
            skill_path=skill_path,
            focus=["structure", "documentation"]
        )

        refactor_suggestions = refactor_result["suggestions"]
        print(f"✓ 生成 {len(refactor_suggestions)} 条建议")

    # ==================== 返回完整结果 ====================
    return {
        "success": True,
        "skill_path": skill_path,
        "requirements": requirements["answers"],
        "validation": {
            "valid": validation["valid"],
            "structure_valid": validation["structure_valid"],
            "content_valid": validation["content_valid"]
        },
        "analysis": {
            "quality_score": quality_score,
            "structure_analysis": analysis["structure"],
            "complexity_metrics": analysis["complexity"]
        },
        "refactor_suggestions": refactor_suggestions,
        "ready_to_use": quality_score >= 80
    }
```

### 4.3 执行结果示例

```json
{
  "success": true,
  "skill_path": "/home/user/skills/my-new-skill",
  "requirements": {
    "skill_name": "my-new-skill",
    "skill_function": "数据分析",
    "use_cases": "处理CSV文件",
    "template_type": "tool-based"
  },
  "validation": {
    "valid": true,
    "structure_valid": true,
    "content_valid": true
  },
  "analysis": {
    "quality_score": 85,
    "structure_analysis": {
      "has_skill_md": true,
      "has_examples": true,
      "has_references": true
    },
    "complexity_metrics": {
      "total_complexity": "low"
    }
  },
  "refactor_suggestions": null,
  "ready_to_use": true
}
```

---

## 5. 最佳实践

### 5.1 职责分离原则

**DO ✅**:
- MCP工具: 单一职责，原子操作
- Agent-Skill: 编排工作流，传递知识

**DON'T ❌**:
- MCP工具: 包含循环逻辑或复杂业务流程
- Agent-Skill: 直接操作文件系统或执行I/O

### 5.2 错误处理

**DO ✅**:
```python
# Agent-Skill层统一错误处理
try:
    result = await mcp.some_tool(ctx, params)
    if not result["success"]:
        # 处理错误，决定是否继续
        return handle_error(result)
except Exception as e:
    # 捕获异常，提供友好提示
    return handle_exception(e)
```

**DON'T ❌**:
```python
# MCP工具不应该处理业务逻辑错误
async def some_tool(ctx, params):
    # ❌ 不要在这里处理"下一步该做什么"
    if not valid:
        # ❌ 不要决定是否调用其他工具
        return call_another_tool()
```

### 5.3 状态管理

**DO ✅**:
```python
# Agent-Skill层管理工作流状态
workflow_state = {
    "stage": "initialization",
    "data": {}
}

# 根据状态决定下一步
if workflow_state["stage"] == "validation":
    result = await mcp.validate(ctx, params)
```

**DON'T ❌**:
```python
# MCP工具不应该维护跨调用状态
# ❌ 避免使用全局变量或类级别的状态
class ToolState:
    last_result = None  # ❌ 不要这样做
```

---

## 6. 参考文档

### 6.1 架构文档

- [需求收集架构文档](../references/requirement-collection-architecture.md) - 详解 `collect_requirements` 的特殊性

### 6.2 MCP集成

- [MCP集成指南](../references/mcp-integration.md) - MCP工具使用和资源访问

### 6.3 最佳实践

- [最佳实践 - 核心](../references/best-practices-core.md) - 基础架构和规范

---

**文档维护**: 随着项目演进，持续更新工作流示例。
**最后更新**: 2026-01-27
