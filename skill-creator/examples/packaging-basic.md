# 打包基础示例

> **配套文档**: [packaging.md](../references/packaging.md)

---

## 一、快速开始

### 最简单的打包方式

```python
from skill_creator_mcp.utils.packagers import package_agent_skill

# 打包单个技能
result = package_agent_skill(
    skill_path="/path/to/my-skill",
    version="1.0.0"
)

if result.success:
    print(f"✅ {result.package_path}")
else:
    print(f"❌ {result.error}")
```

**输出示例**:
```
✅ /output/my-skill-v1.0.0.zip
文件数量: 23
包大小: 156KB
```

---

## 二、常见用例

### 用例1: 打包到指定目录

```python
result = package_agent_skill(
    skill_path="skill-creator",
    output_dir="~/dist",
    version="0.3.1"
)
```

### 用例2: 使用 tar.gz 格式

```python
result = package_agent_skill(
    skill_path="my-skill",
    version="1.0.0",
    package_format="tar.gz"
)
```

### 用例3: 包含测试文件（调试用）

```python
result = package_agent_skill(
    skill_path="my-skill",
    version="1.0.0",
    include_tests=True
)
```

### 用例4: 跳过验证（已知问题）

```python
result = package_agent_skill(
    skill_path="my-skill",
    version="1.0.0",
    validate_before_package=False
)
```

---

## 三、完整工作流示例

### 场景: 发布新版本

```python
from skill_creator_mcp.utils.packagers import package_agent_skill

# 1. 准备发布
skill_path = "skill-creator"
version = "0.3.2"
output_dir = "release"

# 2. 打包
result = package_agent_skill(
    skill_path=skill_path,
    output_dir=output_dir,
    version=version,
    package_format="zip",
    include_tests=False,
    validate_before_package=True
)

# 3. 检查结果
if result.success:
    print(f"✅ 打包成功!")
    print(f"   文件: {result.package_path}")
    print(f"   大小: {result.package_size} 字节")
    print(f"   文件数: {result.files_included}")
else:
    print(f"❌ 打包失败: {result.error}")
    exit(1)

# 4. 验证包质量
import os
package_path = result.package_path
size_mb = os.path.getsize(package_path) / 1024 / 1024

print(f"\n📦 包质量检查:")
print(f"   大小: {size_mb:.2f} MB {'✅' if size_mb < 0.5 else '❌'}")
print(f"   文件数: {result.files_included} {'✅' if result.files_included < 50 else '❌'}")
```

---

## 四、常见错误处理

### 错误1: SKILL.md 不存在

```python
result = package_agent_skill(
    skill_path="incomplete-skill",
    version="1.0.0"
)

if not result.success:
    if "SKILL.md" in result.error:
        print("❌ 缺少必需文件 SKILL.md")
        print("   请先创建 SKILL.md")
```

### 错误2: 路径不存在

```python
from pathlib import Path

skill_path = "non-existent-skill"
if not Path(skill_path).exists():
    print(f"❌ 路径不存在: {skill_path}")
    print("   请检查路径是否正确")
else:
    result = package_agent_skill(skill_path=skill_path)
```

### 错误3: 包大小超限

```python
result = package_agent_skill(skill_path="my-skill", version="1.0.0")

if result.success:
    size_mb = result.package_size / 1024 / 1024
    if size_mb > 0.5:
        print(f"⚠️  包大小过大: {size_mb:.2f} MB")
        print("   建议检查是否包含了不必要的文件")
```

---

## 五、验证命令

### 检查包内容

```bash
# 列出前30个文件
unzip -l my-skill-v1.0.0.zip | head -30

# 统计文件数量
unzip -l my-skill-v1.0.0.zip | tail -1

# 检查包大小
ls -lh my-skill-v1.0.0.zip
```

### 解压测试

```bash
# 解压到临时目录
unzip -q my-skill-v1.0.0.zip -d /tmp/test-skill

# 验证结构
ls -la /tmp/test-skill/my-skill/
```

---

**更多高级示例**: [packaging-advanced.md](packaging-advanced.md)
**规范文档**: [packaging.md](../references/packaging.md)
