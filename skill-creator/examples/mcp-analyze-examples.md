# analyze_skill 使用示例

`analyze_skill` 工具用于分析 Agent-Skill 的代码质量和复杂度。

## 概述

`analyze_skill` 提供深入的代码质量分析，包括：
- Token 效率评分
- 文件大小统计
- 反模式识别
- 优化建议

## 基本用法

```python
# 分析技能
analyze_skill(skill_path="/path/to/skill")
```

**响应**:
```json
{
  "quality": {"overall_score": 85, "token_efficiency": 80, "structure": 90, "documentation": 85},
  "files": {"total": 5, "total_lines": 450, "total_tokens": 8500},
  "anti_patterns": [
    {"type": "long_file", "file": "SKILL.md", "issue": "文件过长 (180 行)"}
  ],
  "suggestions": ["考虑拆分 SKILL.md 为多个引用文件"]
}
```

---

## 分析报告详解

**质量评分**:
- `overall_score` (0-100): 综合评分
- `token_efficiency`: Token 效率
- `structure`: 结构质量
- `documentation`: 文档质量
- 评分: 90-100优秀, 80-89良好, 70-79及格, <70需改进

**文件统计**: total, total_lines, total_tokens

**反模式类型**:
- `long_file` - 文件过长
- `duplicate_content` - 内容重复
- `poor_structure` - 结构不良
- `missing_references` - 缺少引用

---

## 使用场景

| 场景 | 命令 | 说明 |
|------|------|------|
| 开发过程中分析 | `analyze_skill(skill_path)` | 定期检查质量 |
| 优化前对比 | 优化前后各分析一次 | 对比改进效果 |
| 批量分析 | 循环分析多个技能 | 找出质量最低的 |

---

## 常见反模式

| 反模式 | 问题 | 解决方案 |
|--------|------|----------|
| 文件过长 | SKILL.md 超过 150 行 | 精简到 ≤150 行，详细内容移到 references/ |
| 内容重复 | 多个文件包含相同内容 | 合并重复内容，使用交叉引用 |
| 结构不良 | 缺少 examples/ 目录 | 添加使用示例目录 |

---

## Token 效率分析

**效率评分标准**:
- 90-100: 优秀 (<5000 tokens)
- 80-89: 良好 (5000-10000)
- 70-79: 及格 (10000-20000)
- <70: 需要改进 (>20000)

**优化建议**: 精简 SKILL.md、拆分引用文件、使用渐进式披露

---

## 最佳实践

1. **定期分析**：每周分析一次代码质量
2. **关注反模式**：检查并修复反模式
3. **追踪改进**：记录评分变化趋势

---

## 完整工作流

```python
# 1. 创建技能 → 2. 编写内容 → 3. 分析质量 → 4. 根据建议优化 → 5. 重新分析
result = analyze_skill(skill_path="./my-skill")
print(f"质量评分: {result['quality']['overall_score']}/100")
for s in result['suggestions']:
    print(f"建议: {s}")
# 优化后重新分析验证
```

---

## 错误处理

| 错误类型 | 响应 | 处理方式 |
|----------|------|----------|
| 路径不存在 | `{"success": false, "error": "技能路径不存在"}` | 检查路径拼写 |
| 无法解析 | `{"success": false, "error": "无法解析 SKILL.md"}` | 检查 SKILL.md 格式 |

---

## 相关文档

- **[init_skill 示例](mcp-init-examples.md)** - 创建技能
- **[validate_skill 示例](mcp-validate-examples.md)** - 验证技能
- **[refactor_skill 示例](mcp-refactor-examples.md)** - 重构建议
