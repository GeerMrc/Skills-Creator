# analyze_skill 使用示例

`analyze_skill` 工具用于分析 Agent-Skill 的代码质量和复杂度。

## 概述

`analyze_skill` 提供深入的代码质量分析，包括：
- Token 效率评分
- 文件大小统计
- 反模式识别
- 优化建议

## 基本用法

### 标准分析

```python
# 分析技能
analyze_skill(skill_path="/path/to/skill")
```

**响应**:
```json
{
  "success": true,
  "quality": {
    "overall_score": 85,
    "token_efficiency": 80,
    "structure": 90,
    "documentation": 85
  },
  "files": {
    "total": 5,
    "total_lines": 450,
    "total_tokens": 8500
  },
  "anti_patterns": [
    {
      "type": "long_file",
      "file": "SKILL.md",
      "issue": "文件过长 (180 行)",
      "suggestion": "建议精简到 150 行以内"
    }
  ],
  "suggestions": [
    "考虑拆分 SKILL.md 为多个引用文件",
    "引用文件建议保持在 200-300 行"
  ]
}
```

---

## 分析报告详解

### quality (质量评分)

```json
{
  "overall_score": 85,        // 综合评分 (0-100)
  "token_efficiency": 80,     // Token 效率
  "structure": 90,            // 结构质量
  "documentation": 85         // 文档质量
}
```

**评分标准**:
- 90-100: 优秀
- 80-89: 良好
- 70-79: 及格
- <70: 需要改进

### files (文件统计)

```json
{
  "total": 5,              // 文件总数
  "total_lines": 450,      // 总行数
  "total_tokens": 8500     // 总 Token 数
}
```

### anti_patterns (反模式识别)

```json
{
  "type": "long_file",         // 反模式类型
  "file": "SKILL.md",          // 问题文件
  "issue": "文件过长 (180 行)", // 问题描述
  "suggestion": "建议精简..."  // 改进建议
}
```

**反模式类型**:
- `long_file` - 文件过长
- `duplicate_content` - 内容重复
- `poor_structure` - 结构不良
- `missing_references` - 缺少引用

---

## 使用场景

### 开发过程中分析

```python
# 定期分析代码质量
result = analyze_skill(skill_path="./my-skill")
print(f"质量评分: {result['quality']['overall_score']}/100")

# 检查反模式
if result['anti_patterns']:
    print("发现反模式：")
    for pattern in result['anti_patterns']:
        print(f"- {pattern['issue']}")
```

### 优化前对比

```python
# 优化前
before = analyze_skill(skill_path="./my-skill")
print(f"优化前评分: {before['quality']['overall_score']}")

# 执行优化...

# 优化后
after = analyze_skill(skill_path="./my-skill")
print(f"优化后评分: {after['quality']['overall_score']}")
```

### 批量分析

```python
# 分析多个技能
skills = ["skill1", "skill2", "skill3"]
results = {}

for skill in skills:
    result = analyze_skill(skill_path=f"./skills/{skill}")
    results[skill] = result['quality']['overall_score']
    print(f"{skill}: {result['quality']['overall_score']}/100")

# 找出质量最低的技能
min_skill = min(results, key=results.get)
print(f"需要改进: {min_skill} ({results[min_skill]}/100)")
```

---

## 常见反模式

### 1. 文件过长

```
Issue: SKILL.md 文件过长 (180 行)
Suggestion: 建议精简到 150 行以内，详细内容移到引用文件
```

**解决**:
- 核心信息保留在 SKILL.md
- 详细说明移到 references/
- 使用渐进式披露

### 2. 内容重复

```
Issue: references/api.md 和 references/integration.md 内容重复
Suggestion: 合并重复内容，使用交叉引用
```

**解决**:
- 识别重复内容
- 合并到单一文件
- 使用链接引用

### 3. 结构不良

```
Issue: 缺少 examples/ 目录
Suggestion: 添加使用示例目录
```

**解决**:
- 创建 examples/ 目录
- 添加使用示例文件
- 更新 SKILL.md 链接

---

## Token 效率分析

### Token 计算

```json
{
  "token_efficiency": 80,
  "total_tokens": 8500,
  "estimated_cost": "0.00085 USD"
}
```

**效率评分标准**:
- 90-100: 优秀 (<5000 tokens)
- 80-89: 良好 (5000-10000)
- 70-79: 及格 (10000-20000)
- <70: 需要改进 (>20000)

### 优化建议

```python
result = analyze_skill(skill_path="./my-skill")

# Token 效率低
if result['quality']['token_efficiency'] < 80:
    print("Token 效率建议：")
    print("- 精简 SKILL.md")
    print("- 拆分引用文件")
    print("- 使用渐进式披露")
```

---

## 最佳实践

### 1. 定期分析

```python
# 每周分析一次
result = analyze_skill(skill_path="./my-skill")
print(f"当前评分: {result['quality']['overall_score']}/100")
```

### 2. 关注反模式

```python
# 检查反模式
result = analyze_skill(skill_path="./my-skill")
for pattern in result['anti_patterns']:
    print(f"修复: {pattern['suggestion']}")
```

### 3. 追踪改进

```python
# 记录评分变化
scores = []
for week in range(4):
    result = analyze_skill(skill_path="./my-skill")
    scores.append(result['quality']['overall_score'])
    print(f"Week {week+1}: {scores[-1]}/100")

# 绘制趋势图
import matplotlib.pyplot as plt
plt.plot(scores)
plt.title("质量评分趋势")
plt.show()
```

---

## 完整工作流

```python
# 1. 创建技能
init_skill(name="my-skill", template="tool-based")

# 2. 编写内容（手动）

# 3. 分析质量
result = analyze_skill(skill_path="./my-skill")
print(f"质量评分: {result['quality']['overall_score']}/100")

# 4. 根据建议优化
for suggestion in result['suggestions']:
    print(f"建议: {suggestion}")

# 5. 重新分析
result = analyze_skill(skill_path="./my-skill")
if result['quality']['overall_score'] >= 85:
    print("✅ 质量良好")
```

---

## 错误处理

### 路径不存在

```python
# 错误：技能路径不存在
analyze_skill(skill_path="/nonexistent/path")

# 响应
{
  "success": false,
  "error": "技能路径不存在"
}
```

### 无法解析

```python
# 错误：无法解析 SKILL.md
analyze_skill(skill_path="./broken-skill")

# 响应
{
  "success": false,
  "error": "无法解析 SKILL.md"
}
```

---

## 相关文档

- **[init_skill 示例](mcp-init-examples.md)** - 创建技能
- **[validate_skill 示例](mcp-validate-examples.md)** - 验证技能
- **[refactor_skill 示例](mcp-refactor-examples.md)** - 重构建议
