# v0.3.3 发布计划

**计划类型**: 版本发布
**创建日期**: 2026-01-26
**状态**: planning
**目标版本**: v0.3.3

---

## 一、开发规范流程概述

### 九步法开发流程

```
步骤0: 前置任务审核  → 检查前置任务、确认Git环境
步骤1: 制定开发计划  → .claude/plans/feat-xxx.md
步骤2: 拆分任务清单  → TaskCreate (3-10个任务)
步骤3: 执行开发工作  → 编码 + 测试
步骤4: 测试验证      → pytest --cov
步骤5: 交叉验证      → 对照计划检查 (支持回退)
步骤6: 更新文档      → CHANGELOG.md
步骤7: 阶段性审计    → 内部审查
步骤8: Git提交       → 版本控制
步骤9: 阶段性汇报    → 生成汇报并归档计划
```

### 核心原则

1. **基于事实审核**: 必须基于实际代码内容，不能仅依据文档记录
2. **TODO实时更新**: 每完成一步立即更新状态
3. **质量门禁**: 测试100%通过、ruff/mypy 0错误
4. **禁止虚假审核**: 不得声称未完成的工作已完成

---

## 二、发布目标

### 2.1 版本变更

```
当前版本: v0.3.2
目标版本: v0.3.3
```

### 2.2 主要发布内容

1. **环境变量支持**: `SKILL_CREATOR_OUTPUT_DIR` 全局配置
2. **路径解析修复**: 相对路径自动转换为绝对路径
3. **参数优化**: `output_dir` 改为可选参数
4. **文档完善**: 更新配置说明和安装方法

### 2.3 发布产物

| 产物 | 格式 | 目标位置 |
|------|------|----------|
| Agent-Skill | skill-creator-v0.3.3.zip | GitHub Releases |
| MCP Server | skill_creator_mcp-0.3.3-py3-none-any.whl | PyPI |
| MCP Server | skill_creator_mcp-0.3.3.tar.gz | PyPI |

---

## 三、项目状态审核

### 3.1 版本号不一致问题

| 文件 | 当前版本 | 目标版本 |
|------|----------|----------|
| pyproject.toml | 0.3.2 | **0.3.3** |
| src/__init__.py | 0.3.0 | **0.3.3** |
| docs/conf.py | 0.2.1 | **0.3.3** |
| README.md | v0.3.0 | **v0.3.3** |
| docs/*.md | 0.3.0/0.3.1 | **0.3.3** |

### 3.2 文档问题

| 问题 | 优先级 | 文件 |
|------|--------|------|
| 缺少 package_agent_skill 文档 | P0 | README.md |
| 测试数量不一致 (563 vs 583) | P1 | README.md |
| 未实现的环境变量说明 | P2 | README.md |

### 3.3 Git 状态

- 当前分支: develop
- 领先 origin/develop: 4个提交
- 现有 tag: v0.2.1, v0.3.0, v0.3.2
- 缺失: v0.3.1 tag（CHANGELOG有记录但Git无）

---

## 四、任务清单

### 任务 1: 更新版本号到 v0.3.3

**优先级**: P0 (阻塞性)
**文件**:
- `skill-creator-mcp/pyproject.toml`
- `skill-creator-mcp/src/skill_creator_mcp/__init__.py`
- `skill-creator-mcp/docs/conf.py`
- `README.md`
- `skill-creator-mcp/README.md`
- `skill-creator-mcp/docs/README.md`
- `skill-creator-mcp/docs/configuration.md`
- `skill-creator-mcp/docs/mcp-config-guide.md`
- `skill-creator-mcp/docs/installation.md`

**修改内容**:
- pyproject.toml: `version = "0.3.3"`
- __init__.py: `__version__ = "0.3.3"`
- docs/conf.py: `version = "0.3.3"`, `release = "0.3.3"`
- README 文件: 更新版本声明为 v0.3.3

**验收标准**:
- 所有文件版本号一致为 0.3.3
- `health_check_tool` 返回正确版本

---

### 任务 2: 更新 CHANGELOG.md

**优先级**: P0 (阻塞性)
**文件**: `CHANGELOG.md`

**操作**:
1. 将 Unreleased 章节内容移至 `## [0.3.3] - 2026-01-26`
2. 创建新的空 `## [Unreleased]` 章节

**变更内容**:
```markdown
## [0.3.3] - 2026-01-26

### Added
- init_skill, package_skill, package_agent_skill 工具支持 SKILL_CREATOR_OUTPUT_DIR 环境变量
- 路径验证器功能：自动创建目录、检查可写性、支持 ~ 展开、相对路径转绝对路径
- PackageAgentSkillInput 数据模型

### Fixed
- 环境变量 SKILL_CREATOR_OUTPUT_DIR 现在在相关工具中生效
- 路径解析相对于 MCP Server 启动目录的问题

### Changed
- output_dir 参数改为可选，默认使用环境变量配置
- 使用 model_validator(mode="after") 确保默认值处理
```

---

### 任务 3: 完善 README.md 安装说明

**优先级**: P0 (阻塞性)
**文件**: `README.md` 和 `skill-creator-mcp/README.md`

**添加内容**:
```markdown
## 快速开始

### 1. 安装 MCP Server

```bash
# 方式1：使用 pip
pip install skill-creator-mcp

# 方式2：使用 uv pip
uv pip install skill-creator-mcp
```

### 2. 配置 Claude Code

**方式1：使用 claude mcp add-json（推荐）**

```bash
# 用户级配置（跨项目使用）
claude mcp add-json "skill-creator" '{
  "command": "python",
  "args": ["-m", "skill_creator_mcp"]
}' --scope user
```

**方式2：手动编辑配置文件**

用户配置文件位置：
- macOS: `~/Library/Application Support/Claude/claude_desktop_config.json`
- Windows: `%APPDATA%\Claude\claude_desktop_config.json`
- Linux: `~/.config/Claude/claude_desktop_config.json`

添加以下配置：
```json
{
  "mcpServers": {
    "skill-creator": {
      "command": "python",
      "args": ["-m", "skill_creator_mcp"]
    }
  }
}
```

### 3. 环境变量配置（推荐）

设置 `SKILL_CREATOR_OUTPUT_DIR` 环境变量，统一管理技能输出位置：

```bash
# 添加到 ~/.bashrc 或 ~/.zshrc
export SKILL_CREATOR_OUTPUT_DIR=~/my-skills
```
```

---

### 任务 4: 添加 package_agent_skill 工具文档

**优先级**: P0 (阻塞性)
**文件**: `README.md` 和 `skill-creator-mcp/README.md`

**添加位置**: MCP 工具列表

**添加内容**:
```markdown
### package_agent_skill

打包 Agent-Skill 为标准分发格式（推荐使用）。

**参数**:
- `skill_path` (str): Agent-Skill 目录路径
- `output_dir` (str, 可选): 输出目录，默认使用环境变量
- `version` (str, 可选): 版本号，格式如 "0.3.3"
- `format` (str): 打包格式，默认 "zip"
- `include_tests` (bool): 是否包含测试文件，默认 False
- `validate_before_package` (bool): 打包前是否验证，默认 True

**特点**:
- 生成标准化包名: `skill-creator-v{version}.zip`
- 使用严格排除模式，确保包最小化
- 打包前自动验证结构和内容
```

---

### 任务 5: 修复测试数据不一致

**优先级**: P1 (高优先级)
**文件**: `README.md` 和 `skill-creator-mcp/README.md`

**操作**:
1. 运行测试获取准确数量
2. 统一测试数量描述

```bash
cd skill-creator-mcp
uv run pytest --collect-only -q | grep "test session starts" -A 5
```

**当前测试数量**: 589 个（根据最新运行）

**修改**:
- 将 "563个测试用例" 更新为 "589个测试用例"
- 更新测试覆盖率（当前 95%）

---

### 任务 6: 移除未实现的环境变量说明

**优先级**: P2 (中优先级)
**文件**: `README.md`

**操作**:
- 删除或实现 `SKILL_CREATOR_DEV_MODE` 环境变量说明（第276行）

---

### 任务 7: 更新 MCP Server 版本并打包

**优先级**: P0 (阻塞性)

**操作**:
```bash
cd skill-creator-mcp
uv build
```

**验收标准**:
- 生成 `dist/skill_creator_mcp-0.3.3-py3-none-any.whl`
- 生成 `dist/skill_creator_mcp-0.3.3.tar.gz`
- 版本号正确

---

### 任务 8: 打包 Agent-Skill

**优先级**: P0 (阻塞性)

**操作**:
```python
from skill_creator_mcp.utils.packagers import package_agent_skill

result = package_agent_skill(
    skill_path="/models/claude-glm/Skills-Creator/skill-creator",
    output_dir="/models/claude-glm/Skills-Creator",
    version="0.3.3",
    package_format="zip",
    include_tests=False,
    validate_before_package=True
)
```

**验收标准**:
- 生成 `skill-creator-v0.3.3.zip`
- 包含约 39 个文件
- 大小约 100-120KB

---

### 任务 9: 运行完整测试验证

**优先级**: P0 (阻塞性)

**操作**:
```bash
cd skill-creator-mcp
uv run pytest --cov
uv run ruff check .
uv run mypy src/
```

**验收标准**:
- 测试通过: 589/589 (100%)
- 覆盖率: ≥95%
- ruff: 0 错误
- mypy: 0 错误

---

### 任务 10: Git 提交版本更新

**优先级**: P0 (阻塞性)

**提交信息**:
```
chore(release): 准备 v0.3.3 发布

更新：
- 版本号统一为 0.3.3
- CHANGELOG.md 添加 v0.3.3 章节
- README.md 完善安装配置说明
- 添加 package_agent_skill 工具文档
- 修复测试数据不一致

新功能：
- SKILL_CREATOR_OUTPUT_DIR 环境变量支持
- 路径验证器：自动创建目录、检查可写性
- output_dir 参数改为可选

Co-Authored-By: Claude <noreply@anthropic.com>
```

---

### 任务 11: 创建 Git Tag v0.3.3

**优先级**: P0 (阻塞性)

**操作**:
```bash
git tag -a v0.3.3 -m "Release v0.3.3: 环境变量支持和路径解析修复

- 新增 SKILL_CREATOR_OUTPUT_DIR 环境变量支持
- 修复路径解析问题，支持相对 MCP Server 启动目录
- 改进 output_dir 参数，使其可选并默认使用环境变量
- 完善文档和安装配置说明"
```

---

### 任务 12: 推送到远端

**优先级**: P0 (阻塞性)

**操作**:
```bash
git push origin develop
git push origin v0.3.3
```

---

### 任务 13: 创建 GitHub Release

**优先级**: P0 (阻塞性)

**操作**:
1. 上传 `skill-creator-v0.3.3.zip` 到 Releases
2. 使用 v0.3.3 tag
3. 添加发布说明

**发布说明模板**:
```markdown
# v0.3.3 发布

## 新增功能

### 环境变量支持
- 新增 `SKILL_CREATOR_OUTPUT_DIR` 环境变量，统一管理技能输出位置
- 支持相对路径、绝对路径、~ 展开
- 配置优先级：工具参数 > 环境变量 > 默认值

### 路径验证增强
- 自动创建不存在的目录
- 验证路径可写性
- 支持 `~` 展开
- 相对路径自动转换为绝对路径

### 参数优化
- `output_dir` 参数改为可选
- 默认使用环境变量配置

## 安装

```bash
pip install skill-creator-mcp
```

## 配置

```bash
claude mcp add-json "skill-creator" '{
  "command": "python",
  "args": ["-m", "skill_creator_mcp"]
}' --scope user
```

## 完整变更日志

详见 [CHANGELOG.md](https://github.com/...)
```

---

### 任务 14: 推送到 PyPI

**优先级**: P0 (阻塞性)

**操作**:
```bash
cd skill-creator-mcp
uv publish
```

---

### 任务 15: 清理旧 Tag（可选）

**优先级**: P2 (中优先级)

**操作**:
```bash
# 如果需要删除远端旧 tag
git push origin --delete v0.3.0 v0.3.2

# 然后重新推送
git push origin v0.3.3
```

---

## 五、关键文件清单

| 文件 | 修改类型 | 状态 |
|------|----------|------|
| `skill-creator-mcp/pyproject.toml` | 版本号 0.3.3 | 需修改 |
| `skill-creator-mcp/src/skill_creator_mcp/__init__.py` | 版本号 0.3.3 | 需修改 |
| `skill-creator-mcp/docs/conf.py` | 版本号 0.3.3 | 需修改 |
| `CHANGELOG.md` | 添加 v0.3.3 章节 | 需修改 |
| `README.md` | 版本号 + 安装说明 | 需修改 |
| `skill-creator-mcp/README.md` | 版本号 + 工具文档 | 需修改 |
| `skill-creator-mcp/docs/*.md` | 版本号更新 | 需修改 |

---

## 六、验收标准

### 功能验收

| 验收项 | 标准 |
|--------|------|
| 版本号一致性 | 所有文件显示 0.3.3 |
| 测试通过率 | 589/589 (100%) |
| 测试覆盖率 | ≥95% |
| 代码质量检查 | ruff 0 错误, mypy 0 错误 |
| 打包产物 | skill-creator-v0.3.3.zip 存在且有效 |
| Git Tag | v0.3.3 已创建并推送 |
| GitHub Release | 已创建并上传 zip 文件 |
| PyPI 发布 | 0.3.3 版本可安装 |

### 文档验收

| 验收项 | 标准 |
|--------|------|
| 安装说明完整 | 包含 pip/uv 安装和 claude mcp add-json 配置 |
| 环境变量说明 | SKILL_CREATOR_OUTPUT_DIR 使用方法清晰 |
| 工具文档完整 | package_agent_skill 有详细说明 |
| 版本号统一 | 所有文档显示 v0.3.3 |
| 测试数据一致 | 测试数量统一为 589 |

---

## 七、风险与注意事项

### 7.1 风险

| 风险 | 影响 | 缓解措施 |
|------|------|----------|
| PyPI 发布失败 | 阻塞发布 | 提前检查 PyPI token 和权限 |
| 版本号冲突 | 依赖混乱 | 确认 0.3.3 未被占用 |
| 文档不完整 | 用户困惑 | 仔细审核所有文档 |

### 7.2 注意事项

1. **版本号同步**: 确保所有文件版本号一致
2. **测试验证**: 发布前必须运行完整测试
3. **文档审核**: 确保文档与代码实现一致
4. **可编辑安装**: 开发环境使用 `uv pip install -e .`

---

## 八、后续步骤

完成本次发布后：

1. **创建 v0.3.4 开发分支**: 如果需要继续开发
2. **归档发布计划**: 移动到 `archive/` 目录
3. **生成发布报告**: 记录发布过程和经验教训
4. **更新文档站点**: 发布最新版本文档

---

**计划创建时间**: 2026-01-26
**预计发布时间**: 完成所有15个任务后
