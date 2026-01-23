# validate_skill 使用示例

`validate_skill` 工具用于验证 Agent-Skill 的结构和内容符合规范。

## 概述

`validate_skill` 检查技能的目录结构、命名规范、内容完整性等。

## 基本用法

### 完整验证（默认）

```python
# 验证技能（检查结构和内容）
validate_skill(skill_path="/path/to/skill")
```

**响应**:
```json
{
  "valid": true,
  "issues": [],
  "warnings": [
    {
      "category": "description",
      "message": "描述缺少使用场景",
      "suggestion": "添加 '何时使用' 章节"
    }
  ],
  "score": 85
}
```

### 只检查结构

```python
# 只检查目录结构，不检查内容
validate_skill(
    skill_path="/path/to/skill",
    check_structure=True,
    check_content=False
)
```

检查项目：
- SKILL.md 存在
- references/ 目录存在
- 文件命名规范

### 只检查内容

```python
# 只检查内容质量，不检查结构
validate_skill(
    skill_path="/path/to/skill",
    check_structure=False,
    check_content=True
)
```

检查项目：
- YAML frontmatter 完整性
- 描述质量
- 文档链接有效

---

## 验证报告结构

### valid

```python
"valid": True  # 技能是否符合基本规范
```

### issues

```python
"issues": [
    {
        "category": "naming",
        "message": "SKILL.md 引用文件名格式错误",
        "suggestion": "使用 references/filename.md 格式"
    }
]
```

**类别**:
- `naming` - 命名规范
- `structure` - 目录结构
- `content` - 内容质量
- `links` - 引用链接

### warnings

```python
"warnings": [
    {
        "category": "description",
        "message": "描述缺少使用场景",
        "suggestion": "添加 '何时使用' 章节"
    }
]
```

**类别**:
- `description` - 描述质量
- `token-efficiency` - Token 使用
- `documentation` - 文档完整性

### score

```python
"score": 85  # 综合评分 (0-100)
```

评分标准：
- 90-100: 优秀
- 80-89: 良好
- 70-79: 及格
- <70: 需要改进

---

## 验证项详解

### 目录结构验证

| 检查项 | 说明 |
|--------|------|
| SKILL.md 存在 | 必需文件 |
| references/ 存在 | 引用文档目录 |
| 命名规范 | 小写字母、数字、连字符 |

### 内容验证

| 检查项 | 说明 |
|--------|------|
| YAML frontmatter | name, description, triggers |
| 描述完整性 | 功能陈述、使用场景 |
| 引用链接 | 检查链接有效性 |

---

## 使用场景

### 开发过程中验证

```python
# 编写代码时定期验证
while developing:
    result = validate_skill(skill_path="./my-skill")
    if result['score'] < 80:
        print(f"需要注意：{result['issues']}")
        break
```

### 提交前验证

```python
# 提交前完整验证
result = validate_skill(skill_path="./my-skill")
if result['valid'] and result['score'] >= 80:
    print("✅ 可以提交")
else:
    print("❌ 需要修复问题")
    for issue in result['issues']:
        print(f"- {issue['message']}")
```

### 批量验证

```python
# 验证多个技能
skills = ["skill1", "skill2", "skill3"]
results = {}

for skill in skills:
    result = validate_skill(skill_path=f"./skills/{skill}")
    results[skill] = result['score']
    print(f"{skill}: {result['score']}/100")

# 输出汇总
for skill, score in results.items():
    status = "✓" if score >= 80 else "⚠" if score >= 60 else "✗"
    print(f"{status} {skill}: {score}/100")
```

---

## 常见问题

### 问题 1: SKILL.md 过长

```
Issue: SKILL.md 行数超过 150
Suggestion: 精简 SKILL.md，将详细内容移到引用文件
```

**解决**:
1. 保留核心信息在 SKILL.md
2. 详细说明移到 references/
3. 使用渐进式披露

### 问题 2: 引用链接断链

```
Issue: 引用文件 references/api.md 不存在
Suggestion: 创建引用文件或更新链接
```

**解决**:
1. 检查引用文件是否存在
2. 更新 SKILL.md 中的链接
3. 运行 `validate_skill` 重新检查

### 问题 3: 描述不完整

```
Issue: 描述缺少使用场景
Suggestion: 添加 '何时使用' 章节
```

**解决**:
在 SKILL.md 添加使用场景说明。

---

## 最佳实践

### 1. 定期验证

```python
# 每次修改后验证
result = validate_skill(skill_path="./my-skill")
print(f"当前评分: {result['score']}/100")
```

### 2. 关注警告

```python
# 即使 valid=True，也要检查 warnings
result = validate_skill(skill_path="./my-skill")
if result['warnings']:
    print("建议改进：")
    for warning in result['warnings']:
        print(f"- {warning['suggestion']}")
```

### 3. 验证阈值

```python
# 设置最低可接受评分
MIN_SCORE = 80

result = validate_skill(skill_path="./my-skill")
if result['score'] >= MIN_SCORE:
    print("✅ 质量合格")
else:
    print(f"❌ 需要改进，当前: {result['score']}")
```

---

## 错误处理

### 路径不存在

```python
# 错误：技能路径不存在
validate_skill(skill_path="/nonexistent/path")

# 响应
{
  "success": false,
  "error": "技能路径不存在"
}
```

### 权限不足

```python
# 错误：无读取权限
validate_skill(skill_path="/root/skill")

# 响应
{
  "success": false,
  "error": "权限不足"
}
```

---

## 完整工作流

```python
# 1. 创建技能
init_skill(name="my-skill", template="tool-based")

# 2. 编写内容（手动）

# 3. 验证
result = validate_skill(skill_path="./my-skill")
print(f"Validation score: {result['score']}/100")

# 4. 修复问题
for issue in result['issues']:
    print(f"修复: {issue['suggestion']}")

# 5. 重新验证
result = validate_skill(skill_path="./my-skill")
if result['valid']:
    print("✅ 验证通过")
```

---

## 相关文档

- **[init_skill 示例](mcp-init-examples.md)** - 创建技能
- **[analyze_skill 示例](mcp-analyze-examples.md)** - 分析质量
- **[验证规范](../references/validation.md)** - 验证规则
