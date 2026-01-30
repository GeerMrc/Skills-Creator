# 打包示例

> **配套文档**: [packaging.md](../references/packaging.md)
> **MCP 工具**: `package_skill`

---

## 一、快速开始

### 最简单的打包方式

```
使用 package_skill 工具打包 /path/to/my-skill 到 /output 目录
```

**预期输出**:
```
✅ 打包成功: /output/my-skill.zip
文件数量: 23
包大小: 156KB
```

---

## 二、常见用例

| 用例 | 命令示例 |
|------|----------|
| 打包到指定目录 | 打包 skill-creator 到 ~/dist 目录 |
| 使用 tar.gz 格式 | 打包 my-skill，使用 tar.gz 格式 |
| 包含测试文件 | 打包 my-skill，包含测试文件 |
| 跳过验证 | 打包 my-skill，跳过验证步骤 |

---

## 三、标准打包模式

### Agent-Skill 标准打包

**标准包名格式**: `{skill-name}-v{version}.{format}`

**使用方式**:
```
使用 package_skill 标准打包 skill-creator，版本 0.3.4
```

**标准打包特点**:
- 严格的排除模式（排除所有开发文件）
- 支持版本号（v0.3.4 格式）
- 标准化包名格式
- 打包前自动验证

**排除的文件**:
- 版本控制: `.git/`, `.gitignore`, `.github/`
- Python 构建: `__pycache__/`, `*.pyc`, `*.egg-info/`
- 测试文件: `tests/`, `.pytest_cache/`, `htmlcov/`
- 项目文档: `README.md`, `CHANGELOG.md`, `LICENSE`
- MCP Server: `*-mcp/`, `*_mcp/`, `mcp-server/`

### 标准打包 vs 通用打包

| 特性 | 标准打包 (strict=True) | 通用打包 (strict=False) |
|------|----------------------|----------------------|
| 包名格式 | `{name}-v{version}.{ext}` | `{name}.{ext}` |
| 版本号 | 必需 | 不支持 |
| 排除模式 | 严格（Agent-Skill规范） | 灵活（自定义） |
| 适用场景 | Agent-Skill 发布 | 通用项目打包 |

---

## 四、常见错误处理

| 错误 | 原因 | 解决方案 |
|------|------|----------|
| 缺少 SKILL.md | 技能不完整 | 创建 SKILL.md |
| 路径不存在 | 路径错误 | 检查路径是否正确 |
| 包大小超限 | 包含不必要文件 | 检查并排除不必要文件 |
| 验证失败 | 结构不符合规范 | 运行 validate_skill 检查 |

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

## 六、批量打包

```bash
#!/bin/bash
# 批量打包多个技能

SKILLS=("skill-creator" "git-helper" "doc-writer")
OUTPUT_DIR="dist"

for skill in "${SKILLS[@]}"; do
    echo "📦 打包 $skill..."
    # 通过 Claude Code 调用: "打包 $skill 到 $OUTPUT_DIR"
done
```

---

**规范文档**: [packaging.md](../references/packaging.md)
