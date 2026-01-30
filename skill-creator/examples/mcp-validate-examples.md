# validate_skill_tool 使用示例

`validate_skill_tool` 工具用于验证 Agent-Skill 的结构和内容符合规范。

## 概述

`validate_skill_tool` 检查技能的目录结构、命名规范、内容完整性等。

## 基本用法

```python
# 完整验证（结构和内容）
validate_skill_tool(skill_path="/path/to/skill")

# 只检查结构
validate_skill_tool(skill_path="/path/to/skill", check_structure=True, check_content=False)

# 只检查内容
validate_skill_tool(skill_path="/path/to/skill", check_structure=False, check_content=True)
```

**响应**:
```json
{
  "valid": true,
  "issues": [],
  "warnings": [{"category": "description", "message": "描述缺少使用场景"}],
  "score": 85
}
```

---

## 验证报告结构

**valid**: 技能是否符合基本规范

**issues** (必须修复):
- `naming` - 命名规范
- `structure` - 目录结构
- `content` - 内容质量
- `links` - 引用链接

**warnings** (建议改进):
- `description` - 描述质量
- `token-efficiency` - Token 使用
- `documentation` - 文档完整性

**score**: 综合评分 (0-100)
- 90-100: 优秀, 80-89: 良好, 70-79: 及格, <70: 需要改进

## 验证项详解

**目录结构**: SKILL.md 存在、references/ 存在、命名规范

**内容验证**: YAML frontmatter、描述完整性、引用链接有效性

---

## 使用场景

| 场景 | 命令 | 说明 |
|------|------|------|
| 开发过程中验证 | 循环调用，检查 score < 80 | 定期检查 |
| 提交前验证 | 验证 valid 且 score >= 80 | 确保质量 |
| 批量验证 | 循环验证多个技能 | 找出质量最低的 |

---

## 常见问题

| 问题 | 解决方案 |
|------|----------|
| SKILL.md 过长 (超过 150 行) | 精简 SKILL.md，详细内容移到 references/ |
| 引用链接断链 | 检查引用文件是否存在，更新链接 |
| 描述不完整 | 添加使用场景说明到 SKILL.md |

---

## 最佳实践

1. **定期验证**：每次修改后验证
2. **关注警告**：即使 valid=True，也要检查 warnings
3. **验证阈值**：设置最低可接受评分（如 80）

---

## 错误处理

| 错误类型 | 响应 | 处理方式 |
|----------|------|----------|
| 路径不存在 | `{"success": false, "error": "技能路径不存在"}` | 检查路径拼写 |
| 权限不足 | `{"success": false, "error": "权限不足"}` | 检查文件权限 |

---

## 完整工作流

```python
# 1. 创建技能 → 2. 编写内容 → 3. 验证 → 4. 修复问题 → 5. 重新验证
result = validate_skill(skill_path="./my-skill")
print(f"评分: {result['score']}/100")
for issue in result['issues']:
    print(f"修复: {issue['suggestion']}")
# 修复后重新验证
result = validate_skill(skill_path="./my-skill")
if result['valid']:
    print("✅ 验证通过")
```

---

## 相关文档

- **[init_skill 示例](mcp-init-examples.md)** - 创建技能
- **[analyze_skill 示例](mcp-analyze-examples.md)** - 分析质量
- **[验证规范](../references/validation.md)** - 验证规则
