# 打包示例

> **配套文档**: [packaging.md](../references/packaging.md)
> **MCP 工具**: `package_skill`

---

## 一、快速开始

### 最简单的打包方式

```yaml
# 通过 MCP 工具调用
skill_path: /path/to/my-skill
output_dir: /output
format: zip
include_tests: false
validate_before_package: true
```

**调用示例**（Claude Code）:
```
使用 package_skill 工具打包 /path/to/my-skill 到 /output 目录
```

**输出示例**:
```
✅ 打包成功: /output/my-skill.zip
文件数量: 23
包大小: 156KB
```

---

## 二、常见用例

### 用例1: 打包到指定目录

```
打包 skill-creator 到 ~/dist 目录
```

### 用例2: 使用 tar.gz 格式

```
打包 my-skill，使用 tar.gz 格式，输出到 /output
```

### 用例3: 包含测试文件（调试用）

```
打包 my-skill，包含测试文件
```

### 用例4: 跳过验证（已知问题）

```
打包 my-skill，跳过验证步骤
```

---

## 三、完整工作流示例

### 场景: 发布新版本

```bash
# 1. 准备发布
SKILL_PATH="skill-creator"
OUTPUT_DIR="release"

# 2. 通过 Claude Code 调用 MCP 工具
# "使用 package_skill 打包 ${SKILL_PATH} 到 ${OUTPUT_DIR}"

# 3. 验证包质量
ls -lh ${OUTPUT_DIR}/*.zip
unzip -l ${OUTPUT_DIR}/*.zip | tail -1
```

**预期输出**:
```
✅ 打包成功!
   文件: release/my-skill.zip
   大小: 156 KB
   文件数: 23

📦 包质量检查:
   大小: 0.15 MB ✅
   文件数: 23 ✅
```

---

## 四、常见错误处理

### 错误1: SKILL.md 不存在

```
打包 incomplete-skill

# 如果失败，检查错误信息
# ❌ 缺少必需文件 SKILL.md
# 请先创建 SKILL.md
```

### 错误2: 路径不存在

```
# 先验证路径存在
ls non-existent-skill

# 如果路径不存在
# ❌ 路径不存在: non-existent-skill
# 请检查路径是否正确
```

### 错误3: 包大小超限

```
打包 my-skill

# 检查输出大小
# 如果大小超过 500KB
# ⚠️  包大小过大: 0.65 MB
# 建议检查是否包含了不必要的文件
```

---

## 五、验证命令

### 检查包内容

```bash
# 列出前30个文件
unzip -l my-skill.zip | head -30

# 统计文件数量
unzip -l my-skill.zip | tail -1

# 检查包大小
ls -lh my-skill.zip
```

### 解压测试

```bash
# 解压到临时目录
unzip -q my-skill.zip -d /tmp/test-skill

# 验证结构
ls -la /tmp/test-skill/
```

---

## 六、高级用法

### 批量打包

```bash
#!/bin/bash
# 批量打包脚本

SKILLS=("skill-creator" "git-helper" "doc-writer")
OUTPUT_DIR="dist"
RESULTS=()

for skill in "${SKILLS[@]}"; do
    echo "📦 打包 $skill..."
    # 通过 Claude Code 调用: "打包 $skill 到 $OUTPUT_DIR"
    if [ -f "$OUTPUT_DIR/$skill.zip" ]; then
        RESULTS+=("✅ $skill")
    else
        RESULTS+=("❌ $skill")
    fi
done

echo -e "\n📊 打包结果:"
for result in "${RESULTS[@]}"; do
    echo "  $result"
done
```

### CI/CD 集成

```yaml
name: Package Agent-Skill

on:
  push:
    tags:
      - 'v*'

jobs:
  package:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3

      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.12'

      - name: Install dependencies
        run: |
          pip install uv
          cd skill-creator-mcp
          uv sync --dev

      - name: Package skill
        run: |
          python -c "
          from skill_creator_mcp.utils.packagers import package_skill
          result = package_skill(
              skill_path='skill-creator',
              output_dir='dist',
              package_format='zip',
              include_tests=False,
              validate_before_package=True
          )
          if not result.success:
              print(f'❌ 打包失败: {result.error}')
              exit(1)
          print(f'✅ {result.package_path}')
          "

      - name: Upload artifact
        uses: actions/upload-artifact@v3
        with:
          name: skill-package
          path: dist/*.zip
```

---

## 七、标准打包模式

### Agent-Skill 标准打包（strict=True）

**标准包名格式**: `{skill-name}-v{version}.{format}`

**使用方式**:
```
使用 package_skill 工具标准打包 skill-creator，版本号 0.3.4
```

**标准打包特点**:
- ✅ 严格的排除模式（排除所有开发文件）
- ✅ 支持版本号（v0.3.4 格式）
- ✅ 标准化包名格式
- ✅ 打包前自动验证

**排除的文件**:
- `.git/`, `.gitignore`, `.github/`
- `__pycache__/`, `*.pyc`
- `tests/`, `.pytest_cache/`
- `docs/`, `README.md`, `CHANGELOG.md`
- `*-mcp/`, `*_mcp/`, `mcp-server/`

### 标准打包 vs 通用打包

| 特性 | 标准打包 (strict=True) | 通用打包 (strict=False) |
|------|----------------------|----------------------|
| **包名格式** | `{name}-v{version}.{ext}` | `{name}.{ext}` |
| **版本号** | 必需 | 不支持 |
| **排除模式** | 严格（Agent-Skill规范） | 灵活（自定义） |
| **适用场景** | Agent-Skill 发布 | 通用 Python 项目 |

**使用建议**：

**标准打包** (推荐用于 Agent-Skills):
```
使用 package_skill 标准打包 skill-creator，版本 0.3.4
```

**通用打包** (用于其他项目):
```
使用 package_skill 打包 my-project，排除 *.log 和 temp/
```

---

## 八、质量检查脚本

### 完整的质量检查流程

```python
#!/usr/bin/env python3
"""Agent-Skill 包质量检查脚本"""

import os
import zipfile
from pathlib import Path

def check_package_quality(package_path: str) -> dict:
    """检查包质量"""
    checks = {
        "size_ok": False,
        "file_count_ok": False,
        "has_skill_md": False,
        "no_dev_files": True,
        "issues": []
    }

    # 检查大小
    size_mb = os.path.getsize(package_path) / 1024 / 1024
    checks["size_ok"] = size_mb < 0.5
    if not checks["size_ok"]:
        checks["issues"].append(f"包大小过大: {size_mb:.2f} MB")

    # 检查内容
    with zipfile.ZipFile(package_path, 'r') as zf:
        files = zf.namelist()
        checks["file_count_ok"] = len(files) < 50

        if not checks["file_count_ok"]:
            checks["issues"].append(f"文件数量过多: {len(files)}")

        checks["has_skill_md"] = any("SKILL.md" in f for f in files)
        if not checks["has_skill_md"]:
            checks["issues"].append("缺少 SKILL.md 文件")

        # 检查开发文件
        dev_patterns = [
            ".git/", "__pycache__/", "tests/",
            ".pytest_cache/", ".coverage", "htmlcov/"
        ]
        for pattern in dev_patterns:
            if any(pattern.replace("/", "") in f for f in files):
                checks["no_dev_files"] = False
                checks["issues"].append(f"包含开发文件: {pattern}")
                break

    return checks

def main():
    package_path = "dist/skill-creator.zip"

    if not Path(package_path).exists():
        print(f"❌ 包文件不存在: {package_path}")
        print("请先使用 package_skill MCP 工具打包技能")
        return 1

    print(f"🔍 质量检查 {package_path}...")
    checks = check_package_quality(package_path)

    all_passed = all(checks.values())
    for check_name, passed in checks.items():
        if check_name == "issues":
            continue
        status = "✅" if passed else "❌"
        print(f"  {status} {check_name}")

    if checks["issues"]:
        print("\n⚠️  发现问题:")
        for issue in checks["issues"]:
            print(f"    - {issue}")

    if all_passed:
        print("\n✅ 所有检查通过!")
        return 0
    else:
        print("\n❌ 质量检查失败")
        return 1

if __name__ == "__main__":
    exit(main())
```

---

**规范文档**: [packaging.md](../references/packaging.md)
