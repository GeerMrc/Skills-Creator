# Agent-Skill 打包指南

> **文档版本**: v1.0
> **更新日期**: 2026-01-26
> **适用范围**: Agent-Skill 打包和发布

本文档提供 Agent-Skill 打包的完整指南，包括规范、命令示例、验证步骤和常见问题。

---

## 一、打包规范概述

### 1.1 什么是 Agent-Skill 打包？

Agent-Skill 打包是将技能目录及其所有必需文件打包成标准分发格式的过程。标准化的打包确保：

- **可移植性**: 用户可以在不同环境中安装和使用
- **最小化**: 只包含必需文件，减少下载和安装时间
- **可验证**: 打包后可以验证结构和内容的完整性

### 1.2 标准包结构

一个标准的 Agent-Skill 包应该具有以下结构：

```
skill-creator-v0.3.1.zip
└── skill-creator/
    ├── SKILL.md              # 必需 - 技能入口文件
    ├── examples/             # 可选 - 使用示例
    │   └── basic-usage.md
    ├── references/           # 可选 - 引用文档
    │   ├── mcp-integration.md
    │   └── best-practices.md
    └── scripts/              # 可选 - 辅助脚本
        └── validate_skill.py
```

### 1.3 质量指标

| 指标 | 推荐值 | 最大值 | 说明 |
|------|--------|--------|------|
| 文件数量 | 20-40 | <50 | 只包含必需文件 |
| 包大小 | 100-300KB | <500KB | 压缩后的大小 |
| 必需文件 | SKILL.md | 1个 | 入口文件必须存在 |

---

## 二、排除文件列表

### 2.1 版本控制

排除所有版本控制相关的文件和目录：

| 模式 | 说明 |
|------|------|
| `.git` | Git 仓库数据 |
| `.gitignore` | Git 忽略规则 |
| `.gitattributes` | Git 属性配置 |
| `.github` | GitHub 配置文件 |

### 2.2 开发环境

排除 IDE 和编辑器配置：

| 模式 | 说明 |
|------|------|
| `.vscode` | VS Code 配置 |
| `.idea` | JetBrains IDE 配置 |
| `*.swp` | Vim 交换文件 |
| `*.swo` | Vim 其他临时文件 |

### 2.3 计划和归档

**关键！** 排除开发计划和归档：

| 模式 | 说明 |
|------|------|
| `.claude/plans/archive` | 已完成的开发计划 |
| `.claude/archive` | 其他归档文件 |

### 2.4 项目级文档

排除不属于单个 Agent-Skill 的项目文档：

| 模式 | 说明 |
|------|------|
| `README.md` | 项目根 README |
| `CHANGELOG.md` | 项目变更日志 |
| `CONTRIBUTING.md` | 贡献指南 |
| `LICENSE` | 许可证文件 |

### 2.5 MCP Server 代码

MCP Server 应该单独打包：

| 模式 | 说明 |
|------|------|
| `*-mcp` | 以 `-mcp` 结尾的目录 |
| `*_mcp` | 以 `_mcp` 结尾的目录 |
| `mcp-server` | MCP Server 目录 |

### 2.6 测试和覆盖率

排除所有测试相关文件：

| 模式 | 说明 |
|------|------|
| `tests/` | 测试代码目录 |
| `.pytest_cache` | pytest 缓存 |
| `htmlcov/` | HTML 覆盖率报告 |
| `.coverage` | 覆盖率数据文件 |
| `coverage.xml` | XML 覆盖率报告 |

### 2.7 Python 构建产物

排除 Python 编译和构建文件：

| 模式 | 说明 |
|------|------|
| `__pycache__` | 字节码缓存 |
| `*.pyc` | 编译的 Python 文件 |
| `*.pyo` | 优化的 Python 文件 |
| `*.pyd` | Python 动态链接库 |
| `.mypy_cache` | mypy 类型检查缓存 |
| `.ruff_cache` | ruff 缓存 |
| `*.egg-info` | 分发包元数据 |
| `dist/` | 分发包目录 |
| `build/` | 构建目录 |
| `.DS_Store` | macOS 系统文件 |

### 2.8 虚拟环境

排除虚拟环境目录：

| 模式 | 说明 |
|------|------|
| `.venv` | 虚拟环境 |
| `venv` | 虚拟环境 |
| `env` | 虚拟环境 |
| `.env` | 环境变量配置 |

### 2.9 日志和临时文件

排除日志和临时文件：

| 模式 | 说明 |
|------|------|
| `*.log` | 日志文件 |
| `*.tmp` | 临时文件 |
| `*.bak` | 备份文件 |

---

## 三、打包命令

### 3.1 使用 package_agent_skill（推荐）

```python
from skill_creator_mcp.utils.packagers import package_agent_skill

# 基本用法
result = package_agent_skill(
    skill_path="/path/to/skill-creator",
    output_dir="/output",
    version="0.3.1",
    package_format="zip",
    include_tests=False,
    validate_before_package=True
)

# 检查结果
if result.success:
    print(f"包已创建: {result.package_path}")
    print(f"文件数量: {result.files_included}")
    print(f"包大小: {result.package_size} 字节")
else:
    print(f"打包失败: {result.error}")
```

**参数说明**:

| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `skill_path` | str | 必需 | Agent-Skill 目录路径 |
| `output_dir` | str | "." | 输出目录路径 |
| `version` | str | None | 版本号（如 "0.3.1"） |
| `package_format` | str | "zip" | 打包格式（zip/tar.gz/tar.bz2） |
| `include_tests` | bool | False | 是否包含测试文件 |
| `validate_before_package` | bool | True | 打包前是否验证 |

### 3.2 使用 MCP 工具

在 Claude Code 中调用 MCP 工具：

```python
# 调用 package_agent_skill 工具
await package_agent_skill(
    ctx,
    skill_path="/path/to/skill-creator",
    output_dir="/output",
    version="0.3.1",
    format="zip",
    include_tests=False,
    validate_before_package=True
)
```

### 3.3 不同打包格式

```python
# ZIP 格式（推荐）
result = package_agent_skill(
    skill_path="/path/to/skill",
    version="0.3.1",
    package_format="zip"
)

# tar.gz 格式
result = package_agent_skill(
    skill_path="/path/to/skill",
    version="0.3.1",
    package_format="tar.gz"
)

# tar.bz2 格式
result = package_agent_skill(
    skill_path="/path/to/skill",
    version="0.3.1",
    package_format="tar.bz2"
)
```

---

## 四、验证包质量

### 4.1 解压验证

**列出包内容**:
```bash
# 查看前 30 行
unzip -l skill-creator-v0.3.1.zip | head -30

# 统计文件数量
unzip -l skill-creator-v0.3.1.zip | tail -1

# 检查包大小
ls -lh skill-creator-v0.3.1.zip
```

### 4.2 结构验证

```bash
# 解压到临时目录
unzip -q skill-creator-v0.3.1.zip -d /tmp/test-skill
cd /tmp/test-skill/skill-creator

# 验证排除项
[ -d ".claude/plans/archive" ] && echo "❌ 归档未排除" || echo "✅ 归档已排除"
[ -f "README.md" ] && echo "❌ README 未排除" || echo "✅ README 已排除"
[ -d "../skill-creator-mcp" ] && echo "❌ MCP 未排除" || echo "✅ MCP 已排除"

# 验证包含项
[ -f "SKILL.md" ] && echo "✅ SKILL.md 存在" || echo "❌ 缺少 SKILL.md"
[ -d "examples" ] && echo "✅ examples/ 存在" || echo "❌ 缺少 examples/"
[ -d "references" ] && echo "✅ references/ 存在" || echo "❌ 缺少 references/"
[ -d "scripts" ] && echo "✅ scripts/ 存在" || echo "❌ 缺少 scripts/"
```

### 4.3 内容验证

```bash
# 验证 SKILL.md 格式
grep -q "^---" SKILL.md && echo "✅ YAML frontmatter 存在" || echo "❌ 缺少 YAML"

# 验证必需字段
grep -q "^name:" SKILL.md && echo "✅ name 字段存在" || echo "❌ 缺少 name"
grep -q "^description:" SKILL.md && echo "✅ description 字段存在" || echo "❌ 缺少 description"
grep -q "^allowed-tools:" SKILL.md && echo "✅ allowed-tools 字段存在" || echo "❌ 缺少 allowed-tools"
```

### 4.4 功能验证

```bash
# 运行验证脚本
python scripts/validate_skill.py .

# 运行测试（如果包含）
python -m pytest tests/
```

---

## 五、与项目打包的区别

### 5.1 package_skill vs package_agent_skill

| 特性 | package_skill | package_agent_skill |
|------|---------------|---------------------|
| 排除模式 | 基础排除 | 严格排除 |
| 版本号 | 不支持 | 支持 |
| 默认包含测试 | True | False |
| 包名格式 | `{name}.zip` | `{name}-v{version}.zip` |
| 适用场景 | 开发打包 | 发布打包 |

### 5.2 使用建议

- **开发调试**: 使用 `package_skill`，包含测试文件方便调试
- **正式发布**: 使用 `package_agent_skill`，符合标准规范
- **持续集成**: 使用 `package_agent_skill`，确保包质量一致

---

## 六、发布流程

### 6.1 打包前检查

- [ ] 代码已通过所有测试
- [ ] 文档已更新（CHANGELOG.md）
- [ ] 版本号已更新
- [ ] SKILL.md 完整且正确

### 6.2 打包步骤

1. **打包**: 使用 `package_agent_skill()` 创建标准包
2. **验证**: 检查包结构和质量指标
3. **测试**: 在新环境中解压并验证
4. **发布**: 上传到 GitHub Releases
5. **通知**: 更新文档和发布说明

### 6.3 发布后验证

- [ ] 下载并测试发布的包
- [ ] 验证安装流程
- [ ] 确认文档链接有效
- [ ] 收集用户反馈

---

## 七、常见问题

### Q1: 为什么包大小超过 500KB？

**A**: 检查是否包含了不应该包含的文件：

```bash
# 解压并分析包内容
unzip -l skill-creator-v0.3.1.zip | grep -E "\.pyc|__pycache__|\.git|tests/"
```

### Q2: 如何验证包的完整性？

**A**: 使用校验和验证：

```bash
# 生成 SHA256 校验和
shasum -a 256 skill-creator-v0.3.1.zip > checksum.txt

# 验证校验和
shasum -a 256 -c checksum.txt
```

### Q3: 版本号格式有什么要求？

**A**: 遵循语义化版本规范：

- 格式: `MAJOR.MINOR.PATCH` (如 `0.3.1`)
- MAJOR: 重大变更（不兼容）
- MINOR: 新功能（向后兼容）
- PATCH: Bug 修复

### Q4: 如何包含测试文件？

**A**: 设置 `include_tests=True`：

```python
result = package_agent_skill(
    skill_path="/path/to/skill",
    version="0.3.1",
    include_tests=True  # 包含测试文件
)
```

### Q5: 排除模式不生效怎么办？

**A**: 检查排除模式格式：

- 确保模式字符串正确
- 使用 `*` 通配符匹配文件后缀
- 路径使用 `/` 分隔符

---

**相关文档**:
- [CLAUDE.md 七、Agent-Skill 打包规范](../../CLAUDE.md#七agent-skill-打包规范)
- [validation.md](validation.md) - 验证规范
- [mcp-integration.md](mcp-integration.md) - MCP 集成指南
