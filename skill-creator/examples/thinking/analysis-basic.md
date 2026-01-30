# Thinking 分析基础示例

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

## 相关文档

- **[高级分析示例](analysis-advanced.md)** - 对比思考、逆向思考、假设思考
- **[分析工作流](analysis-workflow.md)** - 思考步骤规划和最佳实践
- **[导出格式示例](../thinking/export-formats.md)** - 思考会话导出
- **[MCP 工具参考](../../references/mcp-tools-reference.md)** - MCP 工具配置
