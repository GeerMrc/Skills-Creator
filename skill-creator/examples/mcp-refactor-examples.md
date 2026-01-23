# refactor_skill 使用示例

`refactor_skill` 工具用于生成 Agent-Skill 的重构建议。

## 概述

`refactor_skill` 分析代码并提供优先级排序的改进建议：
- 结构优化
- Token 效率提升
- 文档改进
- 可维护性增强

## 基本用法

### 全面重构建议

```python
# 获取全面重构建议
refactor_skill(skill_path="/path/to/skill")
```

**响应**:
```json
{
  "success": true,
  "suggestions": [
    {
      "priority": "P0",
      "category": "structure",
      "issue": "SKILL.md 过长 (180 行)",
      "impact": "high",
      "effort": "medium",
      "suggestion": "精简 SKILL.md 到 150 行以内，详细内容移到引用文件"
    },
    {
      "priority": "P1",
      "category": "token-efficiency",
      "issue": "引用文件过长 (350 行)",
      "impact": "medium",
      "effort": "low",
      "suggestion": "拆分引用文件为多个小文件"
    }
  ],
  "summary": {
    "total": 2,
    "by_priority": {
      "P0": 1,
      "P1": 1,
      "P2": 0
    }
  }
}
```

---

## 专注特定领域

### 专注结构优化

```python
# 只获取结构相关建议
refactor_skill(
    skill_path="/path/to/skill",
    focus=["structure"]
)
```

### 专注 Token 效率

```python
# 只获取 Token 效率相关建议
refactor_skill(
    skill_path="/path/to/skill",
    focus=["token-efficiency"]
)
```

### 专注多个领域

```python
# 获取多个领域的建议
refactor_skill(
    skill_path="/path/to/skill",
    focus=["structure", "token-efficiency", "documentation"]
)
```

---

## 建议详解

### priority (优先级)

| 优先级 | 说明 | 响应时间 |
|--------|------|----------|
| **P0** | 阻塞性问题 | 立即 |
| **P1** | 高优先级 | 本周内 |
| **P2** | 中优先级 | 本月内 |

### category (类别)

- `structure` - 结构问题
- `token-efficiency` - Token 效率
- `documentation` - 文档质量
- `maintainability` - 可维护性

### impact (影响)

- `high` - 高影响
- `medium` - 中等影响
- `low` - 低影响

### effort (工作量)

- `high` - 需要 3+ 小时
- `medium` - 需要 1-3 小时
- `low` - 需要 <1 小时

---

## 使用场景

### 开发过程中获取建议

```python
# 定期获取重构建议
result = refactor_skill(skill_path="./my-skill")

# 按优先级排序
suggestions = sorted(
    result['suggestions'],
    key=lambda x: x['priority']
)

for suggestion in suggestions:
    print(f"[{suggestion['priority']}] {suggestion['issue']}")
```

### 专注特定问题

```python
# 只关注 Token 效率
result = refactor_skill(
    skill_path="./my-skill",
    focus=["token-efficiency"]
)

print("Token 效率建议：")
for suggestion in result['suggestions']:
    print(f"- {suggestion['suggestion']}")
```

### 估算工作量

```python
# 估算总工作量
result = refactor_skill(skill_path="./my-skill")

effort_map = {"low": 1, "medium": 2, "high": 4}
total_hours = sum(
    effort_map[s['effort']]
    for s in result['suggestions']
)

print(f"预计工作量: {total_hours} 小时")
```

---

## 常见建议

### P0: SKILL.md 过长

```
Issue: SKILL.md 过长 (180 行)
Impact: high
Effort: medium
Suggestion: 精简 SKILL.md 到 150 行以内，详细内容移到引用文件
```

**解决步骤**:
1. 识别核心信息
2. 移动详细内容到引用文件
3. 更新 SKILL.md 链接

### P1: 引用文件过长

```
Issue: 引用文件过长 (350 行)
Impact: medium
Effort: low
Suggestion: 拆分引用文件为多个小文件
```

**解决步骤**:
1. 分析文件结构
2. 按主题拆分
3. 更新交叉引用

### P2: 文档不完整

```
Issue: 缺少使用示例
Impact: low
Effort: low
Suggestion: 添加 examples/ 目录和使用示例
```

**解决步骤**:
1. 创建 examples/ 目录
2. 添加使用示例文件
3. 更新 SKILL.md

---

## 最佳实践

### 1. 按优先级处理

```python
# 先处理 P0，再处理 P1
result = refactor_skill(skill_path="./my-skill")

p0_suggestions = [s for s in result['suggestions'] if s['priority'] == 'P0']
p1_suggestions = [s for s in result['suggestions'] if s['priority'] == 'P1']

print("P0 问题：")
for s in p0_suggestions:
    print(f"- {s['issue']}")

print("\nP1 问题：")
for s in p1_suggestions:
    print(f"- {s['issue']}")
```

### 2. 追踪进度

```python
# 记录已处理的建议
processed = set()

result = refactor_skill(skill_path="./my-skill")
for suggestion in result['suggestions']:
    if suggestion['issue'] not in processed:
        print(f"待处理: {suggestion['issue']}")
        # 处理后标记
        processed.add(suggestion['issue'])
```

### 3. 影响与工作量平衡

```python
# 优先处理高影响/低工作量的建议
result = refactor_skill(skill_path="./my-skill")

quick_wins = [
    s for s in result['suggestions']
    if s['impact'] == 'high' and s['effort'] == 'low'
]

print("快速改进：")
for s in quick_wins:
    print(f"- {s['suggestion']}")
```

---

## 完整工作流

```python
# 1. 分析技能
result = refactor_skill(skill_path="./my-skill")

# 2. 按优先级排序
suggestions = sorted(
    result['suggestions'],
    key=lambda x: x['priority']
)

# 3. 逐个处理
for suggestion in suggestions:
    print(f"[{suggestion['priority']}] {suggestion['issue']}")
    print(f"建议: {suggestion['suggestion']}")
    print(f"影响: {suggestion['impact']}, 工作量: {suggestion['effort']}")
    print()

    # 执行重构...

# 4. 验证改进
validation = validate_skill(skill_path="./my-skill")
print(f"改进后评分: {validation['score']}/100")
```

---

## 错误处理

### 路径不存在

```python
# 错误：技能路径不存在
refactor_skill(skill_path="/nonexistent/path")

# 响应
{
  "success": false,
  "error": "技能路径不存在"
}
```

### 无法分析

```python
# 错误：无法解析技能结构
refactor_skill(skill_path="./broken-skill")

# 响应
{
  "success": false,
  "error": "无法解析技能结构"
}
```

---

## 相关文档

- **[init_skill 示例](mcp-init-examples.md)** - 创建技能
- **[analyze_skill 示例](mcp-analyze-examples.md)** - 分析质量
- **[最佳实践](../references/best-practices-core.md)** - 开发规范
