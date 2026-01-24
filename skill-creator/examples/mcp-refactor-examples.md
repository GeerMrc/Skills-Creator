# refactor_skill 使用示例

`refactor_skill` 工具用于生成 Agent-Skill 的重构建议。

## 概述

`refactor_skill` 分析代码并提供优先级排序的改进建议：
- 结构优化
- Token 效率提升
- 文档改进
- 可维护性增强

## 基本用法

```python
# 获取全面重构建议
refactor_skill(skill_path="/path/to/skill")
```

**响应**:
```json
{
  "suggestions": [
    {"priority": "P0", "issue": "SKILL.md 过长 (180 行)", "impact": "high", "effort": "medium"},
    {"priority": "P1", "issue": "引用文件过长 (350 行)", "impact": "medium", "effort": "low"}
  ],
  "summary": {"total": 2, "by_priority": {"P0": 1, "P1": 1}}
}
```

---

## 专注特定领域

```python
# 专注结构优化
refactor_skill(skill_path="/path/to/skill", focus=["structure"])

# 专注 Token 效率
refactor_skill(skill_path="/path/to/skill", focus=["token-efficiency"])

# 专注多个领域
refactor_skill(skill_path="/path/to/skill", focus=["structure", "documentation"])
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

| 场景 | 命令 | 说明 |
|------|------|------|
| 开发过程中获取建议 | `refactor_skill(skill_path)` | 定期检查 |
| 专注特定问题 | `refactor_skill(skill_path, focus=["token-efficiency"])` | 针对性优化 |
| 估算工作量 | 遍历 suggestions，计算 effort | 规划时间 |

---

## 常见建议

| 优先级 | 问题 | 解决方案 |
|--------|------|----------|
| P0 | SKILL.md 过长 (180 行) | 精简到 ≤150 行，详细内容移到引用文件 |
| P1 | 引用文件过长 (350 行) | 拆分为多个小文件 |
| P2 | 缺少使用示例 | 添加 examples/ 目录 |

---

## 最佳实践

1. **按优先级处理**：先 P0，再 P1，最后 P2
2. **追踪进度**：记录已处理的建议，避免重复工作
3. **影响与工作量平衡**：优先处理高影响/低工作量的建议（快速改进）

---

## 完整工作流

```python
# 1. 分析技能 → 2. 按优先级排序 → 3. 逐个处理 → 4. 验证改进
result = refactor_skill(skill_path="./my-skill")
suggestions = sorted(result['suggestions'], key=lambda x: x['priority'])
for s in suggestions:
    print(f"[{s['priority']}] {s['issue']}: {s['suggestion']}")
# 执行重构后验证
validation = validate_skill(skill_path="./my-skill")
```

---

## 错误处理

| 错误类型 | 响应 | 处理方式 |
|----------|------|----------|
| 路径不存在 | `{"success": false, "error": "技能路径不存在"}` | 检查路径拼写 |
| 无法分析 | `{"success": false, "error": "无法解析技能结构"}` | 检查 SKILL.md 格式 |

---

## 相关文档

- **[init_skill 示例](mcp-init-examples.md)** - 创建技能
- **[analyze_skill 示例](mcp-analyze-examples.md)** - 分析质量
- **[最佳实践](../references/best-practices-core.md)** - 开发规范
