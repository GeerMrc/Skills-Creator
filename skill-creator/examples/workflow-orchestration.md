# 工作流编排示例

> **文档版本**: v1.1
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

    # 步骤1: 收集需求（使用7个原子化工具）
    # 1.1 创建会话
    session = await create_requirement_session_tool(mode="basic")
    session_id = session["session_id"]

    # 1.2 获取并回答问题
    answers = {}
    for i in range(5):  # basic模式有5个问题
        question = await get_static_question_tool(mode="basic", step_index=i)
        answer = await ctx.elicit(question["prompt"])  # Agent-Skill层交互
        answers[question["key"]] = answer
        await update_requirement_answer_tool(
            session_id=session_id,
            question_key=question["key"],
            answer=answer
        )

    # 1.3 检查完整性
    completeness = await check_requirement_completeness_tool(answers=answers)

    # 步骤2: 初始化技能
    init_result = await init_skill(
        ctx,
        name=answers["skill_name"],
        template=answers.get("template_type", "minimal")
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

## 3. 需求收集工作流（7个原子化工具）

### 3.1 架构说明

需求收集功能已重构为**7个原子化MCP工具**，符合ADR 001架构原则：

| 工具 | 职责 | 类别 |
|------|------|------|
| `create_requirement_session_tool` | 创建会话 | 会话管理 |
| `get_requirement_session_tool` | 获取会话状态 | 会话管理 |
| `update_requirement_answer_tool` | 更新答案 | 会话管理 |
| `get_static_question_tool` | 获取预定义问题 | 问题获取 |
| `generate_dynamic_question_tool` | 生成动态问题 | 问题获取 |
| `validate_answer_format_tool` | 验证答案格式 | 验证工具 |
| `check_requirement_completeness_tool` | 检查完整性 | 验证工具 |

### 3.2 正确的工作流用法

**特征**: Agent-Skill层编排，多次调用MCP工具

```python
# 正确：Agent-Skill层编排
async def collect_requirements_workflow():
    """正确的需求收集流程."""

    # 1. 创建会话
    session = await create_requirement_session_tool(mode="basic")
    session_id = session["session_id"]

    # 2. Agent-Skill层循环收集答案
    answers = {}
    for i in range(5):  # basic模式5个问题
        # 获取问题
        question = await get_static_question_tool(mode="basic", step_index=i)

        # 获取用户输入（Agent-Skill层的elicit）
        answer = await ctx.elicit(question["prompt"])

        # 验证答案
        if question.get("validation"):
            is_valid = await validate_answer_format_tool(
                answer=answer,
                validation=question["validation"]
            )
            if not is_valid["valid"]:
                continue  # 重新输入

        # 保存答案
        await update_requirement_answer_tool(
            session_id=session_id,
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

### 3.3 迁移指南

**旧代码（已弃用）**:
```python
# 旧的单个工具（包含循环逻辑）
result = await collect_requirements(
    ctx,
    action="start",
    mode="basic",
    use_elicit=True
)
```

**新代码（推荐）**:
```python
# 新的7个原子化工具（Agent-Skill层编排）
session = await create_requirement_session_tool(mode="basic")
question = await get_static_question_tool(mode="basic", step_index=0)
answer = await ctx.elicit(question["prompt"])
await update_requirement_answer_tool(
    session_id=session["session_id"],
    question_key=question["key"],
    answer=answer
)
# ... 继续其他步骤
```

**主要变化**：
1. 单个工具拆分为7个原子化工具
2. 循环逻辑从MCP层移到Agent-Skill层
3. 更灵活的验证和错误处理
4. 更好的可测试性和可复用性

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

    # 1.1 创建会话
    session = await create_requirement_session_tool(mode="complete")
    session_id = session["session_id"]

    # 1.2 获取并回答问题（complete模式10个问题）
    answers = {}
    for i in range(10):
        question = await get_static_question_tool(mode="complete", step_index=i)
        answer = await ctx.elicit(question["prompt"])

        # 验证答案
        if question.get("validation"):
            validation = await validate_answer_format_tool(
                answer=answer,
                validation=question["validation"]
            )
            if not validation["valid"]:
                print(f"验证失败：{validation['error']}")
                continue

        # 保存答案
        await update_requirement_answer_tool(
            session_id=session_id,
            question_key=question["key"],
            answer=answer
        )
        answers[question["key"]] = answer
        print(f"进度：{(i + 1) * 10}%")

    # 1.3 检查完整性
    completeness = await check_requirement_completeness_tool(answers=answers)

    if not completeness["is_complete"]:
        print("需求不完整：", completeness["missing_info"])
        return {
            "success": False,
            "stage": "requirements",
            "error": "需求不完整"
        }

    print(f"✓ 需求收集完成: {answers['skill_name']}")

    # ==================== 阶段2: 初始化技能 ====================
    print("📦 阶段2: 初始化技能...")

    init_result = await init_skill(
        ctx,
        name=answers["skill_name"],
        template=answers.get("template_type", "minimal"),
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

    validation = await validate_skill(
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

    analysis = await analyze_skill(
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

        refactor_result = await refactor_skill(
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
        "requirements": answers,
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

- [需求收集API核心参考](../references/requirement-collection-api-core.md) - 7个原子化工具的完整API
- [需求收集API示例](../references/requirement-collection-api-examples.md) - 实际使用场景和最佳实践

### 6.2 MCP集成

- [MCP集成指南](../references/mcp-integration.md) - MCP工具使用和资源访问

### 6.3 最佳实践

- [最佳实践 - 核心](../references/best-practices-core.md) - 基础架构和规范

---

**文档维护**: 随着项目演进，持续更新工作流示例。
**最后更新**: 2026-01-29
