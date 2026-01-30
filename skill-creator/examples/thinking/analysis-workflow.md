# Thinking 分析工作流与最佳实践

思考会话的规范工作流程和最佳实践。

## 思考步骤规划

```python
# 在开始分析前，规划思考步骤
THINKING_STEPS = [
    "初始评估",
    "问题分类",
    "优先级排序",
    "具体问题分析",
    "改进方案制定",
    "最终结论"
]

total_steps = len(THINKING_STEPS)

for i, step in enumerate(THINKING_STEPS, 1):
    await sequential_thinking(
        thought=execute_step(step, analysis),
        thoughtNumber=i,
        totalThoughts=total_steps,
        nextThoughtNeeded=(i < total_steps)
    )
```

### 标准分析工作流

```
1. create_session() - 创建会话
2. sequential_thinking() - 记录初始评估
3. sequential_thinking() - 问题分类
4. sequential_thinking() - 优先级排序
5. sequential_thinking() - 具体问题分析
6. sequential_thinking() - 改进方案
7. sequential_thinking() - 最终结论
8. export_session() - 导出记录
```

## 思考内容模板

```python
def format_thought_content(step, data):
    """格式化思考内容"""
    templates = {
        "initial": (
            "## 初始评估\n\n"
            "技能: {skill}\n"
            "评分: {score}/100\n"
            "状态: {status}"
        ),
        "issues": (
            "## 问题分析\n\n"
            "- P0: {p0_count} 个\n"
            "- P1: {p1_count} 个\n"
            "- P2: {p2_count} 个"
        ),
        "priority": (
            "## 优先级排序\n\n"
            "P0 问题必须优先，因为影响基本功能\n"
            "P1 问题尽快处理，提升代码质量\n"
            "P2 问题有时间时处理"
        ),
        "conclusion": (
            "## 结论\n\n"
            "总体评分: {score}/100\n"
            "主要问题: {main_issue}\n"
            "建议: {suggestion}"
        )
    }

    return templates[step].format(**data)
```

## 会话命名规范

```python
def generate_session_name(skill_path, analysis_type="analysis"):
    """生成会话名称"""
    timestamp = datetime.now().strftime("%Y%m%d")
    skill_name = skill_path.split("/")[-1]
    return f"{analysis_type}-{skill_name}-{timestamp}"

# 示例
# analysis-pdf-processor-20260126
# refactoring-git-helper-20260126
```

### 会话描述规范

```python
def generate_session_description(analysis_type, skill_path):
    """生成会话描述"""
    descriptions = {
        "analysis": f"代码质量分析 - {skill_path}",
        "refactoring": f"重构方案分析 - {skill_path}",
        "comparison": f"技能对比分析",
        "improvement": f"改进目标规划 - {skill_path}"
    }
    return descriptions.get(analysis_type, f"思考会话 - {skill_path}")
```

## 思考步骤详解

### 步骤 1: 初始评估

记录技能的基本信息和质量评分。

```python
await sequential_thinking(
    thought=f"## 初始评估\n\n"
           f"**技能**: {skill_name}\n"
           f"**路径**: {skill_path}\n"
           f"**评分**: {overall_score}/100\n\n"
           f"**分项评分**:\n"
           f"- 结构: {structure_score}/40\n"
           f"- 文档: {doc_score}/30\n"
           f"- 测试: {test_score}/30\n\n"
           f"**总体评估**: {overall_status}",
    session_id=session_id,
    thoughtNumber=1,
    totalThoughts=6,
    nextThoughtNeeded=True
)
```

### 步骤 2: 问题分类

将问题按优先级分类统计。

```python
p0_issues = [s for s in suggestions if s["priority"] == "P0"]
p1_issues = [s for s in suggestions if s["priority"] == "P1"]
p2_issues = [s for s in suggestions if s["priority"] == "P2"]

await sequential_thinking(
    thought=f"## 问题分类\n\n"
           f"**统计结果**:\n"
           f"- P0（阻塞性）: {len(p0_issues)} 个\n"
           f"- P1（高优先级）: {len(p1_issues)} 个\n"
           f"- P2（中优先级）: {len(p2_issues)} 个\n\n"
           f"**分析**: {len(p0_issues)} 个 P0 问题需立即处理。",
    session_id=session_id,
    thoughtNumber=2,
    totalThoughts=6,
    nextThoughtNeeded=True
)
```

### 步骤 3: 优先级排序

说明优先级排序的逻辑和依据。

```python
await sequential_thinking(
    thought=f"## 优先级排序\n\n"
           f"**排序原则**:\n"
           f"1. **P0 优先**: 影响基本功能，必须修复\n"
           f"2. **P1 其次**: 影响代码质量，尽快处理\n"
           f"3. **P2 最后**: 改进建议，有时间处理\n\n"
           f"**修复顺序**: P0 → P1 → P2",
    session_id=session_id,
    thoughtNumber=3,
    totalThoughts=6,
    nextThoughtNeeded=True
)
```

### 步骤 4-6: 具体问题分析

逐个分析高优先级问题。

```python
for i, issue in enumerate(p0_issues + p1_issues[:2], 4):
    await sequential_thinking(
        thought=f"## {issue['priority']} 问题: {issue['issue']}\n\n"
               f"**影响**: {issue.get('impact', 'N/A')}\n"
               f"**建议**: {issue['suggestion']}\n"
               f"**工作量**: {issue.get('effort', '中等')}",
        session_id=session_id,
        thoughtNumber=i,
        totalThoughts=6,
        nextThoughtNeeded=(i < 6)
    )
```

## 完整示例

```python
async def analyze_with_thinking(skill_path):
    """完整的分析工作流"""

    # 1. 分析技能
    analysis = await analyze_skill(skill_path=skill_path)

    # 2. 创建会话
    session = await create_session(
        name=generate_session_name(skill_path, "analysis"),
        description=generate_session_description("analysis", skill_path)
    )
    session_id = session["id"]

    # 3. 执行思考步骤
    steps = [
        ("初始评估", format_initial_assessment(analysis)),
        ("问题分类", format_issue_classification(analysis)),
        ("优先级排序", format_priority_sorting(analysis)),
        ("具体问题", format_specific_issues(analysis)),
        ("改进方案", format_improvement_plan(analysis)),
        ("最终结论", format_final_conclusion(analysis))
    ]

    for i, (step_name, thought_content) in enumerate(steps, 1):
        await sequential_thinking(
            thought=f"## {step_name}\n\n{thought_content}",
            session_id=session_id,
            thoughtNumber=i,
            totalThoughts=len(steps),
            nextThoughtNeeded=(i < len(steps))
        )

    # 4. 导出记录
    export_path = f"{skill_path}/docs/analysis-{datetime.now():%Y%m%d}.md"
    result = await export_session(
        session_id=session_id,
        format_type="markdown",
        output_path=export_path
    )

    return {
        "session_id": session_id,
        "export_path": result['output_path'],
        "analysis": analysis
    }
```

## 相关文档

- **[基础分析示例](analysis-basic.md)** - 基础分析集成
- **[高级分析示例](analysis-advanced.md)** - 对比、逆向、假设思考
- **[导出格式示例](../thinking/export-formats.md)** - 思考会话导出
- **[MCP 工具参考](../../references/mcp-tools-reference.md)** - MCP 工具配置
