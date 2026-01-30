# Thinking 思考记录集成示例

演示如何将 `analyze_skill` 与 Thinking MCP 集成，记录代码分析的思考过程。

## 概述

当使用 `analyze_skill` 分析技能代码质量时，可以使用 Thinking MCP 记录分析思路、优先级排序逻辑和改进建议的推导过程，使分析过程可追溯、可复现。

## 场景：代码分析 → 思考记录

### 集成前（无思考记录）

```python
# 直接分析，返回建议
analysis = analyze_skill(skill_path="pdf-processor")

# 返回建议
suggestions = analysis["suggestions"]
# [
#   {"priority": "P0", "issue": "缺少单元测试", "suggestion": "添加测试用例"},
#   {"priority": "P1", "issue": "文档不完整", "suggestion": "补充文档"},
#   ...
# ]

# 问题：
# 1. 不知道为什么这样排序优先级
# 2. 不知道建议的推导过程
# 3. 无法追溯分析决策
```

### 集成后（有思考记录）

```python
# 1. 分析技能
analysis = await analyze_skill(skill_path="pdf-processor")

# 2. 创建思考会话
session = await create_session(
    name=f"分析-{skill_path}",
    description="代码质量分析和改进建议思考过程"
)
session_id = session["id"]

# 3. 记录初始分析思考
await sequential_thinking(
    thought=f"开始分析技能 {skill_path}。\n"
           f"质量评分: {analysis['quality']['overall_score']}/100\n"
           f"结构评分: {analysis['quality']['structure_score']}/40\n"
           f"文档评分: {analysis['quality']['documentation_score']}/30\n"
           f"测试评分: {analysis['quality']['test_coverage_score']}/30\n\n"
           f"总体评估: {'优秀' if analysis['quality']['overall_score'] >= 90 else "
                       f"'良好' if analysis['quality']['overall_score'] >= 70 else '需改进'}",
    session_id=session_id,
    thoughtNumber=1,
    totalThoughts=6,
    nextThoughtNeeded=True
)

# 4. 记录问题分类思考
suggestions = analysis["suggestions"]
p0_issues = [s for s in suggestions if s["priority"] == "P0"]
p1_issues = [s for s in suggestions if s["priority"] == "P1"]
p2_issues = [s for s in suggestions if s["priority"] == "P2"]

await sequential_thinking(
    thought=f"问题分类结果：\n"
           f"- P0（阻塞性）: {len(p0_issues)} 个\n"
           f"- P1（高优先级）: {len(p1_issues)} 个\n"
           f"- P2（中优先级）: {len(p2_issues)} 个\n\n"
           f"分析: {len(p0_issues)} 个 P0 问题需要立即处理，否则影响技能可用性。",
    session_id=session_id,
    thoughtNumber=2,
    totalThoughts=6,
    nextThoughtNeeded=True
)

# 5. 记录优先级排序思考
await sequential_thinking(
    thought=f"优先级排序逻辑：\n"
           f"1. P0 问题（阻塞性）: 影响技能基本功能，必须优先修复\n"
           f"2. P1 问题（高优先级）: 影响代码质量，应尽快处理\n"
           f"3. P2 问题（中优先级）: 改进建议，有时间时处理\n\n"
           f"修复顺序: 先 P0 → 再 P1 → 最后 P2",
    session_id=session_id,
    thoughtNumber=3,
    totalThoughts=6,
    nextThoughtNeeded=True
)

# 6. 记录具体问题思考
for i, issue in enumerate(p0_issues[:3], 4):
    await sequential_thinking(
        thought=f"P0 问题 {i-3}: {issue['issue']}\n"
               f"影响: {issue.get('impact', '影响技能可用性')}\n"
               f"建议: {issue['suggestion']}\n"
               f"工作量: {issue.get('effort', '中等')}",
        session_id=session_id,
        thoughtNumber=i,
        totalThoughts=6,
        nextThoughtNeeded=(i < 6)
    )

# 7. 记录最终结论
await sequential_thinking(
    thought=f"分析完成。\n\n"
           f"总结:\n"
           f"- 总体评分: {analysis['quality']['overall_score']}/100\n"
           f"- P0 问题: {len(p0_issues)} 个（需立即修复）\n"
           f"- P1 问题: {len(p1_issues)} 个（本周内修复）\n"
           f"- P2 问题: {len(p2_issues)} 个（有时间时处理）\n\n"
           f"建议修复顺序:\n"
           f"1. 修复所有 P0 问题\n"
           f"2. 修复高影响的 P1 问题\n"
           f"3. 逐步处理 P2 改进建议",
    session_id=session_id,
    thoughtNumber=6,
    totalThoughts=6,
    nextThoughtNeeded=False
)

# 8. 导出思考记录
export_result = await export_session(
    session_id=session_id,
    format_type="markdown",
    output_path=f"{skill_path}/docs/analysis-thinking.md"
)

print(f"思考记录已导出: {export_result['output_path']}")
```

### 输出示例

**思考记录文件** (`pdf-processor/docs/analysis-thinking.md`):

```markdown
# 代码分析思考记录

## 会话信息
- **会话ID**: sess_2026-01-26_10:30:00
- **技能**: pdf-processor
- **分析时间**: 2026-01-26 10:30:00

## 思考过程

### 步骤 1: 初始评估

技能 `pdf-processor` 的质量评分为 75/100。

- **结构评分**: 30/40
- **文档评分**: 20/30
- **测试评分**: 25/30

总体评估: 良好，但需要改进文档和结构。

### 步骤 2: 问题分类

问题分类结果：
- P0（阻塞性）: 2 个
- P1（高优先级）: 5 个
- P2（中优先级）: 3 个

分析: 2 个 P0 问题需要立即处理，否则影响技能可用性。

### 步骤 3: 优先级排序

优先级排序逻辑：
1. P0 问题（阻塞性）: 影响技能基本功能，必须优先修复
2. P1 问题（高优先级）: 影响代码质量，应尽快处理
3. P2 问题（中优先级）: 改进建议，有时间时处理

修复顺序: 先 P0 → 再 P1 → 最后 P2

### 步骤 4: P0 问题分析

P0 问题 1: 缺少错误处理
- 影响: PDF 解析失败时程序崩溃
- 建议: 添加 try-except 处理
- 工作量: 小

### 步骤 5: P0 问题分析

P0 问题 2: 依赖版本不固定
- 影响: 不同环境可能行为不一致
- 建议: 在 requirements.txt 中固定版本
- 工作量: 小

### 步骤 6: 最终结论

分析完成。

总结:
- 总体评分: 75/100
- P0 问题: 2 个（需立即修复）
- P1 问题: 5 个（本周内修复）
- P2 问题: 3 个（有时间时处理）

建议修复顺序:
1. 修复所有 P0 问题
2. 修复高影响的 P1 问题
3. 逐步处理 P2 改进建议
```

## 增强能力

| 维度 | 无思考记录 | 有思考记录 |
|------|-----------|-----------|
| 分析过程 | 不可见 | 完整记录 |
| 优先级逻辑 | 不透明 | 清晰展示 |
| 决策追溯 | 无法追溯 | 完整可追溯 |
| 知识传递 | 困难 | 通过思考文档 |
| 复盘分析 | 无依据 | 有完整依据 |

## 实用价值

**场景**: 团队审查代码分析结果

**无思考记录**:
```
审查者: "为什么这个问题是 P0？"
分析者: "因为... 呃，我觉得它很重要"
审查者: "有什么具体依据吗？"
分析者: "没有，只是经验判断"
```

**有思考记录**:
```
审查者: "为什么这个问题是 P0？"
分析者: "请看思考文档步骤 4"
审查者: "（查看文档）明白了，因为它会导致程序崩溃"
分析者: "对，这正是思考记录中记录的"
```

## 高级用法

### 1. 对比思考（多个技能对比）

```python
# 对比两个技能的分析结果
async def compare_skills_analysis(skill1, skill2):
    """对比分析两个技能"""

    session = await create_session(
        name=f"对比-{skill1}-vs-{skill2}",
        description="技能对比分析"
    )

    # 记录对比思考
    await sequential_thinking(
        thought=f"对比 {skill1} 和 {skill2}:\n"
               f"{skill1} 评分: {score1}/100\n"
               f"{skill2} 评分: {score2}/100\n\n"
               f"差异: {abs(score1 - score2)} 分",
        session_id=session["id"],
        thoughtNumber=1,
        totalThoughts=3,
        nextThoughtNeeded=True
    )

    # 记录优劣势分析
    await sequential_thinking(
        thought=f"{skill1} 优势: {advantages1}\n"
               f"{skill1} 劣势: {disadvantages1}\n"
               f"{skill2} 优势: {advantages2}\n"
               f"{skill2} 劣势: {disadvantages2}",
        session_id=session["id"],
        thoughtNumber=2,
        totalThoughts=3,
        nextThoughtNeeded=True
    )

    # 记录推荐结论
    await sequential_thinking(
        thought=f"推荐: {'优先使用 ' + skill1 if score1 > score2 else '优先使用 ' + skill2}\n"
               f"理由: {reason}",
        session_id=session["id"],
        thoughtNumber=3,
        totalThoughts=3,
        nextThoughtNeeded=False
    )

    return session
```

### 2. 逆向思考（从目标反推方案）

```python
async def reverse_think_improvement(skill_path, target_score=90):
    """逆向思考：从目标分数反推改进方案"""

    analysis = await analyze_skill(skill_path)
    current_score = analysis['quality']['overall_score']
    gap = target_score - current_score

    session = await create_session(name=f"改进-{skill_path}")

    # 目标
    await sequential_thinking(
        thought=f"目标: 将 {skill_path} 的质量从 {current_score} 提升到 {target_score}\n"
               f"差距: {gap} 分",
        session_id=session["id"],
        thoughtNumber=1,
        totalThoughts=4,
        nextThoughtNeeded=True
    )

    # 反推改进点
    improvements = []
    if gap > 20:
        improvements.append("重构整体结构")
    elif gap > 10:
        improvements.append("修复所有 P0 和 P1 问题")
    else:
        improvements.append("修复部分 P1 问题，改进文档")

    await sequential_thinking(
        thought=f"改进策略: {improvements}",
        session_id=session["id"],
        thoughtNumber=2,
        totalThoughts=4,
        nextThoughtNeeded=True
    )

    # 预期结果
    await sequential_thinking(
        thought=f"预期: 执行上述改进后，质量可达到 {target_score} 分",
        session_id=session["id"],
        thoughtNumber=3,
        totalThoughts=4,
        nextThoughtNeeded=True
    )

    # 结论
    await sequential_thinking(
        thought=f"结论: 需要投入 {'1-2天' if gap > 20 else '半天' if gap > 10 else '2小时'}",
        session_id=session["id"],
        thoughtNumber=4,
        totalThoughts=4,
        nextThoughtNeeded=False
    )

    return session
```

### 3. 假设思考（探索不同方案）

```python
async def hypothetical_refactoring(skill_path):
    """假设思考：探索不同重构方案"""

    session = await create_session(name=f"重构假设-{skill_path}")

    # 方案 A
    await sequential_thinking(
        thought="方案 A: 完全重构\n"
               "优点: 代码更清晰\n"
               "缺点: 耗时长，风险高\n"
               "适用: 长期维护的项目",
        session_id=session["id"],
        thoughtNumber=1,
        totalThoughts=3,
        nextThoughtNeeded=True,
        hypotheticalCondition="采用完全重构方案",
        hypotheticalImpact="代码质量提升 30%，但需要 2 周时间",
        hypotheticalProbability="80%"
    )

    # 方案 B
    await sequential_thinking(
        thought="方案 B: 渐进式改进\n"
               "优点: 风险低，快速见效\n"
               "缺点: 可能遗留技术债务\n"
               "适用: 有时间压力的项目",
        session_id=session["id"],
        thoughtNumber=2,
        totalThoughts=3,
        nextThoughtNeeded=True,
        hypotheticalCondition="采用渐进式改进方案",
        hypotheticalImpact="代码质量提升 15%，需要 3 天",
        hypotheticalProbability="95%"
    )

    # 决策
    await sequential_thinking(
        thought="决策: 根据当前项目情况，推荐方案 B（渐进式改进）\n"
               "理由: 时间紧迫，且方案 B 成功率更高",
        session_id=session["id"],
        thoughtNumber=3,
        totalThoughts=3,
        nextThoughtNeeded=False
    )

    return session
```

## 最佳实践

### 1. 思考步骤规划

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

### 2. 思考内容模板

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
        "conclusion": (
            "## 结论\n\n"
            "总体评分: {score}/100\n"
            "主要问题: {main_issue}\n"
            "建议: {suggestion}"
        )
    }

    return templates[step].format(**data)
```

### 3. 会话命名规范

```python
def generate_session_name(skill_path, analysis_type="analysis"):
    """生成会话名称"""
    timestamp = datetime.now().strftime("%Y%m%d")
    return f"{analysis_type}-{skill_path}-{timestamp}"

# 示例
# analysis-pdf-processor-20260126
# refactoring-git-helper-20260126
```

## 相关文档

- **[analyze_skill 示例](mcp-analyze-examples.md)** - 代码分析详解
- **[Thinking 导出示例](thinking-export.md)** - 思考会话导出
- **[MCP 集成指南](../references/mcp-tools-reference.md)** - MCP 工具配置
