# 打包高级示例

> **配套文档**: [packaging.md](../references/packaging.md)
> **MCP 工具**: `package_skill`

---

## 一、批量打包

### 场景: 打包多个技能

通过 Claude Code 调用 MCP 工具批量打包：

```bash
#!/bin/bash
# 批量打包脚本

SKILLS=("skill-creator" "git-helper" "doc-writer")
OUTPUT_DIR="dist"
RESULTS=()

for skill in "${SKILLS[@]}"; do
    echo "📦 打包 $skill..."
    # 通过 Claude Code 调用: "打包 $skill 到 $OUTPUT_DIR"
    # 假设输出到 $OUTPUT_DIR/$skill.zip
    if [ -f "$OUTPUT_DIR/$skill.zip" ]; then
        RESULTS+=("✅ $skill")
    else
        RESULTS+=("❌ $skill")
    fi
done

# 汇总结果
echo -e "\n📊 打包结果:"
for result in "${RESULTS[@]}"; do
    echo "  $result"
done
```

---

## 二、CI/CD 集成

### GitHub Actions 示例

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
          # 使用 MCP 工具打包
          # 在 CI 环境中，可以通过 Python 脚本调用 MCP 工具
          python -c "
          from skill_creator_mcp.utils.packagers import package_skill
          from pathlib import Path

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

## 三、质量检查脚本

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

## 四、版本管理

### 自动版本号管理

```python
import re
from pathlib import Path

def get_version_from_pyproject(project_path: str) -> str:
    """从 pyproject.toml 读取版本号"""
    pyproject = Path(project_path) / "pyproject.toml"
    content = pyproject.read_text()

    match = re.search(r'version\s*=\s*["\']([^"\']+)', content)
    if match:
        return match.group(1)
    return "0.0.0"

def bump_version(version: str, bump_type: str = "patch") -> str:
    """增加版本号"""
    parts = version.split(".")
    major, minor, patch = int(parts[0]), int(parts[1]), int(parts[2])

    if bump_type == "major":
        major += 1
        minor, patch = 0, 0
    elif bump_type == "minor":
        minor += 1
        patch = 0
    else:  # patch
        patch += 1

    return f"{major}.{minor}.{patch}"

# 使用示例
current_version = get_version_from_pyproject("skill-creator-mcp")
next_version = bump_version(current_version, "patch")
print(f"当前版本: {current_version}")
print(f"下一版本: {next_version}")
```

---

## 五、发布流程自动化

### 完整的发布脚本

```python
#!/usr/bin/env python3
"""自动化发布流程"""

import subprocess
import sys
from pathlib import Path

def run_cmd(cmd: list) -> bool:
    """运行命令"""
    print(f"$ {' '.join(cmd)}")
    result = subprocess.run(cmd)
    return result.returncode == 0

def release(skill_path: str, version: str):
    """发布流程"""

    # 1. 更新版本号
    print(f"\n📝 更新版本到 {version}...")
    # (实际实现需要更新 pyproject.toml)

    # 2. 运行测试
    print("\n🧪 运行测试...")
    if not run_cmd(["uv", "run", "pytest", "--cov"]):
        print("❌ 测试失败")
        return False

    # 3. 打包（通过 Claude Code 调用 MCP 工具）
    print(f"\n📦 打包 {skill_path} v{version}...")
    print("请调用 package_skill MCP 工具:")
    print(f'  skill_path: {skill_path}')
    print(f'  output_dir: dist')
    print(f'  strict: true (标准打包，版本号: v{version})')

    # 假设包已创建
    package_path = f"dist/{Path(skill_path).name}-v{version}.zip"
    if not Path(package_path).exists():
        print(f"❌ 包文件未创建: {package_path}")
        return False

    # 4. 创建 Git 标签
    print(f"\n🏷️  创建标签 v{version}...")
    if not run_cmd(["git", "tag", "-a", f"v{version}", "-m", f"Release {version}"]):
        return False

    # 5. 推送标签
    print("\n📤 推送标签...")
    if not run_cmd(["git", "push", "--tags"]):
        return False

    print("\n✅ 发布完成!")
    return True

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("用法: python release.py <skill_path> <version>")
        sys.exit(1)

    skill_path = sys.argv[1]
    version = sys.argv[2]

    if release(skill_path, version):
        sys.exit(0)
    else:
        sys.exit(1)
```

---

## 六、标准打包 vs 通用打包

### 对比两种打包模式

| 特性 | 标准打包 (strict=True) | 通用打包 (strict=False) |
|------|----------------------|----------------------|
| **包名格式** | `{name}-v{version}.{ext}` | `{name}.{ext}` |
| **版本号** | 必需 | 不支持 |
| **排除模式** | 严格（Agent-Skill规范） | 灵活（自定义） |
| **适用场景** | Agent-Skill 发布 | 通用 Python 项目 |

### 使用建议

**标准打包** (推荐用于 Agent-Skills):
```
使用 package_skill 标准打包 skill-creator，版本 0.3.4
```

**通用打包** (用于其他项目):
```
使用 package_skill 打包 my-project，排除 *.log 和 temp/
```

---

**基础示例**: [packaging-basic.md](packaging-basic.md)
**规范文档**: [packaging.md](../references/packaging.md)
**MCP 文档**: [../../skill-creator-mcp/docs/](../../skill-creator-mcp/docs/)
