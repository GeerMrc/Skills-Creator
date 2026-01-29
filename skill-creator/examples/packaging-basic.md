# 打包基础示例

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

## 六、Agent-Skill 标准打包（strict=True）

### 标准打包格式

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

---

**更多高级示例**: [packaging-advanced.md](packaging-advanced.md)
**规范文档**: [packaging.md](../references/packaging.md)
**MCP 文档**: [../../skill-creator-mcp/docs/](../../skill-creator-mcp/docs/)
