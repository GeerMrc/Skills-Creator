# Agent-Skill 打包指南

> **文档版本**: v1.1
> **更新日期**: 2026-01-27
> **适用范围**: Agent-Skill 打包和发布

本文档提供 Agent-Skill 打包的规范和验证标准。

> **示例文档**: [基础示例](../examples/packaging-basic.md) | [高级示例](../examples/packaging-advanced.md)

---

## 一、打包规范概述

### 1.1 核心原则

- **最小化**: 只包含必需文件，减少下载和安装时间
- **标准化**: 使用统一的包名格式和版本号
- **可验证**: 打包后可验证结构和内容

### 1.2 标准包结构

```
skill-creator-v0.3.1.zip
└── skill-creator/
    ├── SKILL.md              # 必需 - 技能入口文件
    ├── examples/             # 可选 - 使用示例
    ├── references/           # 可选 - 引用文档
    └── scripts/              # 可选 - 辅助脚本
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

| 模式 | 说明 |
|------|------|
| `.git` | Git 仓库数据 |
| `.gitignore` | Git 忽略规则 |
| `.gitattributes` | Git 属性配置 |
| `.github` | GitHub 配置文件 |

### 2.2 开发环境

| 模式 | 说明 |
|------|------|
| `.vscode` | VS Code 配置 |
| `.idea` | JetBrains IDE 配置 |
| `*.swp`, `*.swo` | Vim 临时文件 |

### 2.3 计划和归档

**关键！** 排除开发计划：

| 模式 | 说明 |
|------|------|
| `.claude/plans/archive` | 已完成的开发计划 |
| `.claude/archive` | 其他归档文件 |

### 2.4 项目级文档

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

### 2.6 测试和构建

| 模式 | 说明 |
|------|------|
| `tests/`, `.pytest_cache` | 测试相关 |
| `__pycache__`, `*.pyc` | Python 字节码 |
| `dist/`, `build/`, `*.egg-info` | 构建产物 |
| `.venv`, `venv` | 虚拟环境 |

---

## 三、打包命令

### 3.1 使用 package_agent_skill（推荐）

```python
from skill_creator_mcp.utils.packagers import package_agent_skill

result = package_agent_skill(
    skill_path="/path/to/skill-creator",
    output_dir="/output",
    version="0.3.1",
    package_format="zip",
    include_tests=False,
    validate_before_package=True
)

if result.success:
    print(f"包已创建: {result.package_path}")
```

**参数说明**:

| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `skill_path` | str | 必需 | Agent-Skill 目录路径 |
| `output_dir` | str | "." | 输出目录路径 |
| `version` | str | None | 版本号（如 "0.3.1"） |
| `package_format` | str | "zip" | 打包格式 |
| `include_tests` | bool | False | 是否包含测试文件 |
| `validate_before_package` | bool | True | 打包前是否验证 |

### 3.2 使用 MCP 工具

在 Claude Code 中调用 MCP 工具：

```python
await package_agent_skill(
    ctx,
    skill_path="/path/to/skill-creator",
    version="0.3.1",
    format="zip"
)
```

---

## 四、验证包质量

### 4.1 命令行验证

```bash
# 列出包内容（前30行）
unzip -l skill-creator-v0.3.1.zip | head -30

# 统计文件数量
unzip -l skill-creator-v0.3.1.zip | tail -1

# 检查包大小
ls -lh skill-creator-v0.3.1.zip
```

### 4.2 质量检查清单

- [ ] 文件数量 <50
- [ ] 包大小 <500KB
- [ ] 包含 SKILL.md
- [ ] 不包含测试文件
- [ ] 不包含 `.git/`
- [ ] 不包含 MCP Server 代码
- [ ] 不包含 `plans/archive/`

---

## 五、常见问题

### 问题1: 包大小超出限制

**原因**: 包含了不应该包含的文件

**解决**:
- 检查排除模式
- 使用 `package_agent_skill()` 而非 `package_skill()`
- 查看包内容，找出大文件

### 问题2: 缺少 SKILL.md

**原因**: 技能目录没有 SKILL.md

**解决**: 先创建 SKILL.md，再打包

### 问题3: 包含了开发文件

**原因**: 排除模式不正确

**解决**: 使用 `package_agent_skill()` 而非手动打包

---

## 六、发布流程

### 6.1 发布前检查

```bash
# 1. 验证代码质量
uv run pytest --cov
uv run ruff check .
uv run mypy src/

# 2. 打包
# 使用 package_agent_skill() MCP 工具

# 3. 验证包
unzip -l skill-creator-v0.x.x.zip | head -30
ls -lh skill-creator-v0.x.x.zip
```

### 6.2 Git 标签和发布

```bash
# 提交
git commit -m "chore: release v0.x.x"

# 打标签
git tag -a v0.x.x -m "Release v0.x.x"

# 推送
git push --tags

# 创建 GitHub Release
# 上传打包文件
```

---

## 七、相关文档

| 文档 | 说明 |
|------|------|
| [基础示例](../examples/packaging-basic.md) | 快速开始和常见用例 |
| [高级示例](../examples/packaging-advanced.md) | 批量打包、CI/CD集成 |

---

**文档维护**: 请在每次打包流程变更后更新此指南。
**最后更新**: 2026-01-27 (v1.1 - 精简并移出示例到examples/)
