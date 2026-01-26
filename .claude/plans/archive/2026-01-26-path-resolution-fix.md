# 路径解析修复与用户工作目录支持计划

**计划类型**: 缺陷修复 + 用户体验优化
**创建日期**: 2026-01-26
**状态**: planning
**相关Issue**: 用户报告在`~/test/tmp/`目录开发时，代码被写入`~/.claude/skills/generating-presentations`而非当前目录

---

## 一、问题摘要

### 1.1 用户报告的问题

在测试开发目录 `~/test/tmp/` 下进行 PPT Agent-Skill 开发时，发现技能代码被写入 `~/.claude/skills/generating-presentations` 而非当前工作目录。

### 1.2 根因分析

经过深入审查，确认以下问题：

| 问题 | 根因 | 影响 |
|------|------|------|
| **路径解析错误** | `output_dir="."` 相对于 **MCP Server 启动目录**解析，而非用户工作目录 | 文件写入错误位置 |
| **环境变量未生效** | `SKILL_CREATOR_OUTPUT_DIR` 在 `config.py` 定义，但工具未读取 | 用户配置失效 |
| **路径验证缺失** | `InitSkillInput.output_dir` 无验证器 | 无错误提示 |
| **文档说明不清晰** | 未明确说明路径解析规则 | 用户困惑 |

### 1.3 关键发现

**FastMCP Context 限制**:
- Context 类**没有** `cwd` 或 `working_directory` 属性
- 无法通过 Context 直接获取用户当前工作目录
- MCP 协议本身不传递客户端工作目录信息

**MCP Server 工作目录**:
- 用户配置中未指定 `--directory` 参数
- MCP Server 工作目录 = Python 环境工作目录
- `output_dir="."` 解析为该目录，而非用户目录

### 1.4 审查结论

**代码质量**: ✅ 无明显 bug，存在配置机制未完善的问题

**核心缺陷**:
1. `server.py:150` - `init_skill` 工具的 `output_dir` 参数硬编码为 `"."`
2. `models/skill_config.py:25` - `InitSkillInput.output_dir` 缺少验证器
3. `mcp-integration.md:48` - 环境变量说明未说明工具支持情况

**技术限制**:
- FastMCP Context 类无 `cwd` 属性
- MCP 协议不传递客户端工作目录
- 无法自动获取用户当前工作目录

---

## 二、解决方案

### 2.1 设计原则

- **不考虑向后兼容**: 用户有 Git 快照可回滚
- **配置优先级**: 工具参数 > 环境变量 > 默认值
- **用户友好**: 支持环境变量配置，自动创建目录

### 2.2 配置优先级

```
1. 工具参数 output_dir="xxx" (最高优先级)
2. 环境变量 SKILL_CREATOR_OUTPUT_DIR
3. 默认值 "." (MCP Server 启动目录)
```

### 2.3 技术方案

**方案 A: 环境变量支持**
- 工具读取 `SKILL_CREATOR_OUTPUT_DIR` 环境变量
- 用户可在 shell 中配置默认输出目录
- 示例: `export SKILL_CREATOR_OUTPUT_DIR=$HOME/my-skills`

**方案 B: 路径验证增强**
- 添加 `output_dir` 参数验证器
- 自动创建不存在的目录
- 验证路径可写性
- 支持 `~` 展开

**方案 C: 清晰文档说明**
- 明确说明 `output_dir="."` 的解析规则
- 提供使用绝对路径的示例
- 添加故障排除章节

---

## 三、实施任务清单

### 任务 1: 添加路径验证器

**优先级**: P0 (阻塞性)
**文件**: `skill-creator-mcp/src/skill_creator_mcp/models/skill_config.py`

**修改内容**:

在 `InitSkillInput` 类中添加验证器:
```python
from pathlib import Path
import os

class InitSkillInput(BaseModel):
    # ... 现有字段 ...

    @field_validator("output_dir")
    @classmethod
    def validate_output_dir(cls, v: str) -> str:
        """验证输出目录路径."""
        original = v

        # 展开 ~ 和转换为绝对路径
        path = Path(v).expanduser().resolve()

        # 自动创建不存在的目录
        if not path.exists():
            try:
                path.mkdir(parents=True, exist_ok=True)
            except OSError as e:
                raise ValueError(
                    f"无法创建输出目录 '{original}': {e}. "
                    f"请确保父目录存在且有写入权限。"
                )

        # 验证是目录
        if not path.is_dir():
            raise ValueError(f"输出路径 '{original}' 不是目录")

        # 验证可写
        if not os.access(path, os.W_OK):
            raise ValueError(f"输出目录 '{original}' 不可写")

        return str(path)
```

同样为 `PackageSkillInput` 和 `PackageAgentSkillInput` 添加验证器。

**验收标准**:
- 不存在的路径自动创建
- 文件路径报错"不是目录"
- 只读目录报错"不可写"
- `~` 正确展开

---

### 任务 2: 修改 server.py - 环境变量支持

**优先级**: P0 (阻塞性)
**文件**: `skill-creator-mcp/src/skill_creator_mcp/server.py`

**修改内容**:

1. **init_skill** (Line 146-250):
   ```python
   async def init_skill(
       ctx: Context,
       name: str,
       template: str = "minimal",
       output_dir: str | None = None,  # 改为可选
       with_scripts: bool = False,
       with_examples: bool = False,
   ) -> dict[str, Any]:
       from .config import get_config

       config = get_config()
       # 优先级：参数 > 环境变量 > 默认值
       if output_dir is None:
           output_dir = str(config.output_dir)

       input_data = InitSkillInput.model_validate({
           "name": name,
           "template": template,
           "output_dir": output_dir,
           "with_scripts": with_scripts,
           "with_examples": with_examples,
       })
       # ... 后续逻辑不变
   ```

2. **package_skill** (Line 615): 同样修改
3. **package_agent_skill** (Line 704): 同样修改

**验收标准**:
- 未传参数时使用环境变量或默认值
- 传入参数时优先使用参数

---

### 任务 3: 更新 mcp-integration.md 文档

**优先级**: P1 (高优先级)
**文件**: `skill-creator/references/mcp-integration.md`

**修改内容**:

在环境变量配置章节 (Line 39-48) 添加:

```markdown
| 环境变量 | 说明 | 默认值 | 工具支持 |
|---------|------|--------|----------|
| SKILL_CREATOR_OUTPUT_DIR | 默认输出目录 | 当前目录 | init_skill, package_skill, package_agent_skill |

### 路径解析规则

**重要说明**: `output_dir` 是相对于 **MCP Server 启动目录** 的路径，而非用户当前目录。

**优先级**: 工具参数 > 环境变量 > 当前目录

**推荐做法**:
1. 设置环境变量统一管理输出目录:
   ```bash
   export SKILL_CREATOR_OUTPUT_DIR=~/my-skills
   ```

2. 使用绝对路径避免歧义:
   ```python
   init_skill(name="test", output_dir="/home/user/project")
   ```

3. 使用 `~` 简化路径:
   ```python
   init_skill(name="test", output_dir="~/my-skills")
   ```

**路径验证**:
- 路径不存在时自动创建
- 验证路径是否为目录
- 验证路径是否可写
- 支持 `~` 展开
- 相对路径转换为绝对路径
```

---

### 任务 4: 更新 SKILL.md

**优先级**: P1 (高优先级)
**文件**: `skill-creator/SKILL.md`

**修改内容**:

在快速开始章节添加环境配置建议:
```markdown
### 环境配置（推荐）

设置 `SKILL_CREATOR_OUTPUT_DIR` 环境变量，统一管理技能输出位置：

```bash
export SKILL_CREATOR_OUTPUT_DIR=~/my-skills
```

添加到 `~/.bashrc` 或 `~/.zshrc` 使配置持久化。
```

---

### 任务 5: 添加测试用例

**优先级**: P1 (高优先级)
**文件**: `skill-creator-mcp/tests/test_tools/test_init_skill.py`

**新增测试**:

```python
import os
import pytest
from pathlib import Path
from skill_creator_mcp.models.skill_config import InitSkillInput

def test_output_dir_validation_with_nonexistent_path(temp_dir):
    """测试不存在的路径自动创建."""
    nonexistent = temp_dir / "new" / "nested" / "dir"
    result = InitSkillInput.model_validate({
        "name": "test-skill",
        "output_dir": str(nonexistent),
    })
    assert result.output_dir == str(nonexistent.resolve())
    assert nonexistent.exists()

def test_output_dir_validation_with_file_instead_of_dir(temp_dir):
    """测试路径是文件而非目录时报错."""
    file_path = temp_dir / "not-a-dir"
    file_path.write_text("content")
    with pytest.raises(ValueError, match="不是目录"):
        InitSkillInput.model_validate({
            "name": "test-skill",
            "output_dir": str(file_path),
        })

def test_output_dir_expands_tilde():
    """测试 ~ 展开为用户主目录."""
    input_data = InitSkillInput.model_validate({
        "name": "test-skill",
        "output_dir": "~/test",
    })
    home = Path.home()
    expected = str(home / "test")
    assert input_data.output_dir == expected

@pytest.mark.asyncio
async def test_init_skill_respects_env_var(monkeypatch, temp_dir):
    """测试工具读取环境变量."""
    env_dir = temp_dir / "env-output"
    monkeypatch.setenv("SKILL_CREATOR_OUTPUT_DIR", str(env_dir))

    from skill_creator_mcp.config import reload_config
    reload_config()

    result = await init_skill(
        ctx=None,
        name="test-skill",
    )
    assert "env-output" in result["skill_path"]
```

---

### 任务 6: 更新 config.py 文档

**优先级**: P2 (中优先级)
**文件**: `skill-creator-mcp/src/skill_creator_mcp/config.py`

**修改内容**:

更新模块文档字符串:
```python
"""配置管理模块.

通过环境变量提供可配置的设置。

环境变量：
    SKILL_CREATOR_OUTPUT_DIR: 默认输出目录
        - 由 init_skill, package_skill, package_agent_skill 使用
        - 优先级：工具参数 > 环境变量 > 默认值 "."
        - 默认值：当前目录（MCP Server 启动目录）
        - 推荐：设置为绝对路径如 ~/my-skills
"""
```

---

### 任务 7: 运行完整测试验证

**优先级**: P0 (阻塞性)

**执行命令**:
```bash
cd skill-creator-mcp
uv run pytest --cov
uv run ruff check .
uv run mypy src/
```

**验收标准**:
- 所有测试通过
- 覆盖率 ≥96%
- ruff check: 0 错误
- mypy: 0 错误

---

### 任务 8: 更新 CHANGELOG.md

**优先级**: P1 (高优先级)
**文件**: `CHANGELOG.md`

**添加内容**:
```markdown
## [Unreleased]

### Added
- init_skill, package_skill, package_agent_skill 工具支持 SKILL_CREATOR_OUTPUT_DIR 环境变量
- output_dir 参数路径验证：自动创建目录、检查可写性、支持 ~ 展开

### Fixed
- 环境变量 SKILL_CREATOR_OUTPUT_DIR 现在在相关工具中生效
- output_dir 路径验证：创建不存在的目录，检查可写性

### Changed
- output_dir 参数改为可选，默认使用环境变量配置
- 文档说明路径解析规则和推荐用法
```

---

### 任务 9: Git 提交

**优先级**: P0 (阻塞性)

**提交信息**:
```
fix(config): 修复路径解析并支持环境变量

问题：
- output_dir="." 相对于 MCP Server 启动目录解析
- 用户在 ~/test/tmp/ 开发时文件被写入错误位置
- SKILL_CREATOR_OUTPUT_DIR 环境变量未生效

修改：
- init_skill, package_skill, package_agent_skill 读取环境变量
- 添加 InitSkillInput.validate_output_dir 验证器
- 自动创建不存在的目录
- 支持 ~ 展开、相对路径转换
- 更新文档说明路径解析规则和推荐用法

测试：新增6个测试用例，覆盖率96%
```

---

### 任务 10: 归档计划并生成汇报

**优先级**: P1 (高优先级)

**执行步骤**:
1. 将计划文件移动到 `archive/2026-01-26-path-resolution-fix.md`
2. 生成阶段汇报文档
3. 提交归档

---

## 四、关键文件清单

| 文件 | 修改类型 | 优先级 |
|------|----------|--------|
| `skill-creator-mcp/src/skill_creator_mcp/server.py` | 修改 3 个工具函数 | P0 |
| `skill-creator-mcp/src/skill_creator_mcp/models/skill_config.py` | 添加验证器 | P0 |
| `skill-creator/references/mcp-integration.md` | 文档更新 | P1 |
| `skill-creator/SKILL.md` | 文档更新 | P1 |
| `skill-creator-mcp/tests/test_tools/test_init_skill.py` | 新增测试 | P1 |
| `skill-creator-mcp/src/skill_creator_mcp/config.py` | 文档更新 | P2 |

---

## 五、验收标准

### 功能验收

| 场景 | 预期行为 |
|------|----------|
| 设置环境变量 | 技能创建在环境变量指定目录 |
| 工具参数 | 参数覆盖环境变量 |
| 路径不存在 | 自动创建目录 |
| 路径是文件 | 报错"不是目录" |
| 只读目录 | 报错"不可写" |
| ~ 展开 | 展开为用户主目录 |
| 相对路径 | 转换为绝对路径 |

### 质量验收

| 指标 | 要求 |
|------|------|
| 测试覆盖率 | ≥96% |
| ruff check | 0 错误 |
| mypy check | 0 错误 |

---

## 六、用户使用指南

### 推荐配置方式

**方式 1: 环境变量（推荐）**
```bash
# 添加到 ~/.bashrc 或 ~/.zshrc
export SKILL_CREATOR_OUTPUT_DIR=~/my-skills
```

**方式 2: 绝对路径**
```python
# 调用时明确指定
init_skill(name="test", output_dir="/home/user/project")
```

**方式 3: ~ 简化**
```python
# 使用 ~ 展开
init_skill(name="test", output_dir="~/my-skills")
```

### 故障排除

**问题**: 文件被写入错误位置

**原因**: MCP Server 工作目录与用户目录不一致

**解决方案**:
1. 设置环境变量 `SKILL_CREATOR_OUTPUT_DIR`
2. 使用绝对路径
3. 使用 `~` 简化路径

---

## 七、预计时间

| 阶段 | 预计时间 |
|------|----------|
| 代码修改 (任务 1-2) | 2-3 小时 |
| 文档更新 (任务 3-4, 6) | 1 小时 |
| 测试补充 (任务 5) | 2 小时 |
| 验证提交 (任务 7-10) | 1 小时 |
| **总计** | **6-7 小时** |
