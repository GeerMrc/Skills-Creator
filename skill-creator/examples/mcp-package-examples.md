# package_skill 使用示例

`package_skill` 工具用于打包 Agent-Skill 为分发格式。

## 概述

`package_skill` 将技能打包为以下格式：
- **ZIP** (默认) - 最通用
- **tar.gz** - Linux 常用
- **tar.bz2** - 更高压缩率

## 基本用法

### 默认 ZIP 打包

```python
# 打包为 ZIP 格式（默认）
package_skill(skill_path="/path/to/skill", format="zip")
```

**响应**:
```json
{
  "success": true,
  "package_path": "/path/to/skill.zip",
  "files_included": 15,
  "package_size": 12345,
  "validation_passed": true
}
```

---

## 不同格式

### tar.gz 格式

```python
# 打包为 tar.gz
package_skill(
    skill_path="/path/to/skill",
    format="tar.gz"
)
```

### tar.bz2 格式

```python
# 打包为 tar.bz2
package_skill(
    skill_path="/path/to/skill",
    format="tar.bz2"
)
```

---

## 高级选项

### 排除测试文件

```python
# 不包含测试文件
package_skill(
    skill_path="/path/to/skill",
    format="tar.gz",
    include_tests=False
)
```

**包含文件对比**:
- `include_tests=True`: SKILL.md, references/, examples/, tests/
- `include_tests=False`: SKILL.md, references/, examples/

### 指定输出目录

```python
# 指定输出目录
package_skill(
    skill_path="/path/to/skill",
    output_dir="./dist"
)
```

### 打包前验证

```python
# 打包前先验证技能
package_skill(
    skill_path="/path/to/skill",
    validate_before_package=True
)
```

### 组合多个选项

```python
# 组合使用
package_skill(
    skill_path="/path/to/skill",
    format="zip",
    output_dir="./dist",
    include_tests=True,
    validate_before_package=True
)
```

---

## 参数说明

| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `skill_path` | string | 必填 | 技能目录路径 |
| `format` | string | `"zip"` | 打包格式：zip/tar.gz/tar.bz2 |
| `output_dir` | string | `"."` | 输出目录路径 |
| `include_tests` | bool | `True` | 是否包含测试文件 |
| `validate_before_package` | bool | `False` | 打包前是否验证 |

---

## 返回值详解

```json
{
  "success": true,              // 打包是否成功
  "package_path": "/path/to/skill.zip",  // 打包文件路径
  "files_included": 15,         // 包含的文件数
  "package_size": 12345,        // 打包文件大小（字节）
  "validation_passed": true,    // 验证是否通过
  "validation_errors": []       // 验证错误列表
}
```

---

## 使用场景

### 标准发布

```python
# 发布前完整流程
result = package_skill(
    skill_path="./my-skill",
    format="zip",
    output_dir="./dist",
    validate_before_package=True
)

if result['success']:
    print(f"✅ 打包成功: {result['package_path']}")
    print(f"文件数: {result['files_included']}")
    print(f"大小: {result['package_size']} 字节")
else:
    print("❌ 打包失败")
```

### 开发版本

```python
# 开发版本快速打包（不包含测试）
result = package_skill(
    skill_path="./my-skill",
    format="tar.gz",
    include_tests=False
)
```

### 批量打包

```python
# 批量打包多个技能
skills = ["skill1", "skill2", "skill3"]

for skill in skills:
    result = package_skill(
        skill_path=f"./skills/{skill}",
        format="zip",
        output_dir="./dist"
    )
    print(f"{skill}: {result['package_path']}")
```

---

## 打包验证

### 验证失败处理

```python
# 打包前验证
result = package_skill(
    skill_path="./my-skill",
    validate_before_package=True
)

if not result['validation_passed']:
    print("验证失败：")
    for error in result['validation_errors']:
        print(f"- {error}")
    # 修复问题后重新打包
else:
    print("✅ 验证通过，打包成功")
```

### 手动验证后打包

```python
# 先验证
validation = validate_skill(skill_path="./my-skill")
if validation['valid']:
    # 验证通过后再打包
    result = package_skill(
        skill_path="./my-skill",
        format="zip"
    )
```

---

## 格式对比

| 格式 | 压缩率 | 兼容性 | 速度 | 推荐场景 |
|------|--------|--------|------|----------|
| **ZIP** | 中 | 最好 | 快 | 通用分发 |
| **tar.gz** | 高 | 良好 | 中 | Linux 环境 |
| **tar.bz2** | 最高 | 较差 | 慢 | 存储优化 |

---

## 错误处理

### 路径不存在

```python
# 错误：技能路径不存在
package_skill(skill_path="/nonexistent/path")

# 响应
{
  "success": false,
  "error": "技能路径不存在"
}
```

### 格式不支持

```python
# 错误：无效的格式
package_skill(skill_path="./my-skill", format="7z")

# 响应
{
  "success": false,
  "error": "不支持的格式，使用 zip/tar.gz/tar.bz2"
}
```

### 验证失败

```python
# 验证失败但仍打包（如果不设置 validate_before_package）
result = package_skill(
    skill_path="./my-skill",
    validate_before_package=True
)

# 响应
{
  "success": true,
  "validation_passed": false,
  "validation_errors": [
    "SKILL.md 不符合规范"
  ],
  "package_path": "/path/to/skill.zip"
}
```

---

## 最佳实践

### 1. 打包前验证

```python
# 总是验证后再打包
result = package_skill(
    skill_path="./my-skill",
    validate_before_package=True
)
```

### 2. 使用输出目录

```python
# 使用专门的输出目录
result = package_skill(
    skill_path="./my-skill",
    output_dir="./dist"
)
```

### 3. 选择合适的格式

```python
# 通用：ZIP
package_skill(skill_path="./my-skill", format="zip")

# Linux：tar.gz
package_skill(skill_path="./my-skill", format="tar.gz")
```

---

## 完整工作流

```python
# 1. 验证技能
validation = validate_skill(skill_path="./my-skill")
if not validation['valid']:
    print("❌ 验证失败，请修复问题")
    exit(1)

# 2. 分析质量
analysis = analyze_skill(skill_path="./my-skill")
print(f"质量评分: {analysis['quality']['overall_score']}/100")

# 3. 打包发布
result = package_skill(
    skill_path="./my-skill",
    format="zip",
    output_dir="./dist",
    validate_before_package=True
)

# 4. 检查结果
if result['success']:
    print(f"✅ 打包成功")
    print(f"文件: {result['package_path']}")
    print(f"大小: {result['package_size']} 字节")
```

---

## 相关文档

- **[init_skill 示例](mcp-init-examples.md)** - 创建技能
- **[validate_skill 示例](mcp-validate-examples.md)** - 验证技能
- **[最佳实践](../references/best-practices-core.md)** - 开发规范
