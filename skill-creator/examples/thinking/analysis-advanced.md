# Thinking 高级分析示例

高级思考模式：对比思考、逆向思考、假设思考。

## 1. 对比思考（多个技能对比）

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

### 对比思考输出示例

```
## 步骤 1: 评分对比

对比 pdf-processor 和 image-processor:
- pdf-processor 评分: 75/100
- image-processor 评分: 85/100

差异: 10 分

## 步骤 2: 优劣势分析

pdf-processor:
- 优势: 支持多种 PDF 格式，错误处理完善
- 劣势: 文档不完整，缺少单元测试

image-processor:
- 优势: 测试覆盖率高，代码结构清晰
- 劣势: 仅支持常见图片格式

## 步骤 3: 推荐结论

推荐: 优先使用 image-processor
理由: 整体质量更高，且测试覆盖率更好，维护成本更低
```

---

## 2. 逆向思考（从目标反推方案）

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

### 逆向思考输出示例

```
## 步骤 1: 目标设定

目标: 将 pdf-processor 的质量从 75 提升到 90
差距: 15 分

## 步骤 2: 改进策略

改进策略:
1. 修复所有 P0 和 P1 问题（8个问题）
2. 补充单元测试（目标覆盖率 90%）
3. 完善文档（SKILL.md 和 README）

## 步骤 3: 预期结果

预期: 执行上述改进后，质量可达到 90 分

## 步骤 4: 工作量评估

结论: 需要投入半天时间
```

---

## 3. 假设思考（探索不同方案）

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

### 假设思考输出示例

```
## 步骤 1: 方案 A 分析

**假设条件**: 采用完全重构方案

**影响分析**:
- 优点: 代码更清晰，架构更合理
- 缺点: 耗时长（2周），风险高
- 适用场景: 长期维护的项目

**预期结果**: 代码质量提升 30%
**可能性评估**: 80%

## 步骤 2: 方案 B 分析

**假设条件**: 采用渐进式改进方案

**影响分析**:
- 优点: 风险低，快速见效
- 缺点: 可能遗留技术债务
- 适用场景: 有时间压力的项目

**预期结果**: 代码质量提升 15%
**可能性评估**: 95%

## 步骤 3: 决策结论

**决策**: 推荐方案 B（渐进式改进）

**理由**:
1. 时间紧迫（需要在 1 周内完成）
2. 方案 B 成功率更高（95% vs 80%）
3. 风险可控，不会影响当前功能
```

## 思考类型对比

| 思考类型 | 用途 | 优势 | 典型场景 |
|---------|------|------|----------|
| **常规思考** | 逐步分析 | 清晰的逻辑链 | 代码分析、问题诊断 |
| **对比思考** | 多方案比较 | 突出差异 | 技术选型、方案评审 |
| **逆向思考** | 目标推导 | 明确改进路径 | 目标设定、改进规划 |
| **假设思考** | 方案探索 | 评估风险收益 | 架构设计、重构决策 |

## 相关文档

- **[基础分析示例](analysis-basic.md)** - 基础分析集成
- **[分析工作流](analysis-workflow.md)** - 思考步骤规划
- **[MCP 工具参考](../../references/mcp-tools-reference.md)** - MCP 工具配置
