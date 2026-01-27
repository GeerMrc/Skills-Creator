# SKILL_CREATOR_DEFAULT_OUTPUT_DIR 参数系统性审核与优化计划

> **计划日期**: 2026-01-26
> **计划类型**: 系统审核与优化
> **优先级**: P0 (核心功能)
> **基于**: MCP 社区最佳实践研究 + 当前实现全面审核

---

## 一、研究背景

### 1.1 用户需求

全面审核当前项目关于 `SKILL_CREATOR_DEFAULT_OUTPUT_DIR` 参数的实现：
1. 研究社区 MCP 项目（web-reader、websearch、Context7）的默认路径处理方式
2. 借鉴 MCP 社区最佳实践
3. 对当前实现进行系统性审核

### 1.2 MCP 协议核心限制

> **根本问题**: MCP Server 无法获取客户端工作目录

**实际影响**:
- 相对路径 "." 基于服务器启动目录解析
- 用户期望的"当前项目开发环境目录"无法直接实现
- 需要通过环境变量或绝对路径配置

---

## 二、社区最佳实践研究

### 2.1 2025年趋势总结

| 时期 | 默认策略 | 理由 |
|------|---------|------|
| 早期 | 安装路径 | 简单直接 |
| 2025中期 | **当前工作目录** | 更稳定，支持相对路径 |
| 2025后期 | 智能默认值 + 环境变量 | 最佳用户体验 |

**关键发现** (来自 [MCP Servers PR #2160](https://github.com/modelcontextprotocol/servers/pull/2160)):
> "Changes the default behavior from using the installation path to the current working directory"

### 2.2 社区项目实现策略

| 项目 | 默认路径策略 | 特点 |
|------|-------------|------|
| **mcp-zero** | `current directory` | 明确文档说明 |
| **gemini-mcp-server** | `~/Claude/gemini-images` | 固定用户目录 |
| **crawl4ai-mcp-server** | `required` | 强制用户提供路径 |
| **Pdftools-mcp** | `Downloads` | 验证路径安全性 |

### 2.3 可借鉴的最佳实践

**分级配置策略**（推荐）:
```
优先级 1: 工具参数（用户显式提供）
    ↓ None
优先级 2: 环境变量 SKILL_CREATOR_OUTPUT_DIR
    ↓ 未设置
优先级 3: 智能默认值（当前目录 OR 固定目录）
```

**默认路径选择指南**:

| 场景 | 推荐策略 | 理由 |
|------|---------|------|
| **项目开发工具** | 当前目录 `.` | 用户在项目目录中工作 |
| **全局工具** | 固定目录 `~/skills` | 跨项目一致性 |
| **临时文件** | 系统临时目录 `/tmp` | 自动清理 |
| **用户数据** | 用户主目录 `~` | 持久化存储 |

---

## 三、当前实现审核

### 3.1 实现概述

**配置层级**:
```python
# config.py (第55-60行)
default_output = os.getenv("SKILL_CREATOR_DEFAULT_OUTPUT_DIR", ".")
output_dir_value = os.getenv("SKILL_CREATOR_OUTPUT_DIR", default_output)
self._output_dir = Path(output_dir_value).expanduser().resolve(strict=False)
```

**优先级**:
```
工具参数 > SKILL_CREATOR_OUTPUT_DIR > SKILL_CREATOR_DEFAULT_OUTPUT_DIR > "."
```

### 3.2 发现的问题

#### 问题1: 默认值 "." 导致语义混淆 ⚠️

| 期望行为 | 实际行为 |
|----------|----------|
| 指向客户端工作目录 | 指向 MCP Server 启动目录 |

**影响**:
- 全局安装用户: Server 在 Python 环境目录启动
- 源码开发用户: Server 在 `skill-creator-mcp/` 目录启动

#### 问题2: 双环境变量设计复杂 ⚠️

**当前设计**:
- `SKILL_CREATOR_OUTPUT_DIR` - 主输出目录
- `SKILL_CREATOR_DEFAULT_OUTPUT_DIR` - 默认输出目录

**问题**:
- 功能重叠，增加理解成本
- 使用场景不明确
- 维护成本高

#### 问题3: 文档说明不一致 ⚠️

| 文档 | 说明 |
|------|------|
| `config.py` | 提及两个环境变量 |
| `README.md` | 仅提及 `SKILL_CREATOR_OUTPUT_DIR` |
| `configuration.md` | 仅提及 `SKILL_CREATOR_OUTPUT_DIR` |

#### 问题4: 测试覆盖不完整 ⚠️

```python
# test_config.py (第42-43行)
assert config.output_dir == Path(".").resolve() or str(config.output_dir) == "."
```
- 测试过于宽松
- 未验证实际路径是否符合预期

---

## 四、改进方案

### 4.1 短期方案（向后兼容）

**目标**: 快速改善用户体验，不破坏现有配置

**改进项**:

| 优先级 | 改进项 | 工作量 |
|--------|--------|--------|
| P0 | 统一文档说明 | 小 |
| P0 | 添加配置警告 | 小 |
| P1 | 增强测试覆盖 | 中 |

**具体措施**:

1. **统一文档说明**:
   - 在 README.md 中增加 MCP 协议限制说明章节
   - 在 configuration.md 中增加 "MCP 协议限制" 专门章节
   - 统一所有文档中的环境变量说明

2. **添加配置警告**:
   ```python
   def validate(self) -> list[str]:
       """验证配置的有效性."""
       errors: list[str] = []
       warnings: list[str] = []

       # 检查是否使用相对路径
       if not self._output_dir.is_absolute():
           warnings.append(
               "SKILL_CREATOR_OUTPUT_DIR 使用相对路径，"
               "将基于 MCP Server 启动目录解析。"
               "推荐使用绝对路径如 ~/skills"
           )

       return errors, warnings
   ```

3. **增强测试覆盖**:
   - 添加默认值实际路径验证
   - 添加 MCP 协议限制场景测试
   - 添加环境变量优先级测试

### 4.2 长期方案（破坏性变更）

**目标**: 简化设计，提升用户体验，实现目录自动管理

**核心变更**:

| 变更项 | 当前 | 目标 |
|--------|------|------|
| 环境变量数量 | 2个 | 1个 (`SKILL_CREATOR_DEFAULT_OUTPUT_DIR`) |
| 默认值 | "." | "~/skills" |
| 配置优先级 | 4级 | 3级 |
| 目录管理 | 手动 | **自动检测和创建** |

**新设计**:
```
工具参数 > SKILL_CREATOR_DEFAULT_OUTPUT_DIR > "~/skills"
                              ↓
                        自动检测并创建目录
```

**目录自动管理逻辑**:

```python
def ensure_output_dir(output_dir: Path) -> Path:
    """确保输出目录存在，不存在则自动创建.

    Args:
        output_dir: 输出目录路径（可以是相对路径、绝对路径、~路径）

    Returns:
        已验证/创建的绝对路径

    Raises:
        ValueError: 目录创建失败或无权限
    """
    # 1. 展开 ~ 为用户主目录
    expanded_dir = output_dir.expanduser()

    # 2. 解析为绝对路径
    absolute_dir = expanded_dir.resolve()

    # 3. 检查目录是否存在
    if not absolute_dir.exists():
        # 4. 不存在则自动创建
        try:
            absolute_dir.mkdir(parents=True, exist_ok=True)
        except OSError as e:
            raise ValueError(
                f"无法创建输出目录 {absolute_dir}: {e}"
            ) from e

    # 5. 验证是否为目录
    if not absolute_dir.is_dir():
        raise ValueError(
            f"输出路径不是目录: {absolute_dir}"
        )

    # 6. 验证可写性
    if not os.access(absolute_dir, os.W_OK):
        raise ValueError(
            f"输出目录不可写: {absolute_dir}"
        )

    return absolute_dir
```

**配置流程**:

```
1. 读取 SKILL_CREATOR_DEFAULT_OUTPUT_DIR
   ├─ 已设置 → 使用用户配置的目录
   └─ 未设置 → 使用默认值 ~/skills

2. 对目录路径进行处理
   ├─ 展开 ~ 为 $HOME
   ├─ 解析为绝对路径
   └─ 规范化路径格式

3. 目录验证和创建
   ├─ 检查目录是否存在
   │   ├─ 存在 → 验证可写性
   │   └─ 不存在 → 自动创建
   └─ 返回最终路径
```

**迁移指南**:
```markdown
## v0.4.0 迁移指南

### 环境变量变更

**已简化**: 仅保留 `SKILL_CREATOR_DEFAULT_OUTPUT_DIR`

**新默认值**: `~/skills`（自动创建）

### 行为变更

**v0.3.x**:
- 默认值: "." (MCP Server 启动目录)
- 用户需手动创建目录

**v0.4.0**:
- 默认值: "~/skills" (用户主目录)
- 自动检测和创建目录
- 支持自定义: `SKILL_CREATOR_DEFAULT_OUTPUT_DIR=~/.claude/skills`

### 配置示例

**使用默认值**（推荐）:
```bash
# 不设置环境变量，自动使用 ~/skills
# 首次使用时自动创建目录
```

**自定义目录**:
```bash
# 在 .env 或配置文件中设置
export SKILL_CREATOR_DEFAULT_OUTPUT_DIR=~/.claude/skills
```

### 迁移步骤

如果您之前设置了环境变量:
1. **保留** `SKILL_CREATOR_DEFAULT_OUTPUT_DIR`（如果已配置）
2. **移除** `SKILL_CREATOR_OUTPUT_DIR`（已被废弃）
3. **新用户**: 无需任何配置，使用默认的 ~/skills
```

### 用户需求确认

| 场景 | SKILL_CREATOR_DEFAULT_OUTPUT_DIR | 行为 |
|------|----------------------------------|------|
| **未配置** | (未设置) | 使用 `~/skills`，自动创建 |
| **配置 ~/.claude/skills** | `~/.claude/skills` | 使用 `~/.claude/skills`，自动创建 |
| **配置 /absolute/path** | `/absolute/path` | 使用绝对路径，自动创建 |
| **配置相对路径** | `./skills` | 解析为绝对路径，自动创建 |

---

## 五、实施计划

### 5.1 长期方案实施（v0.4.0）- 完整功能实现

#### 步骤1: 代码修改

**文件1: `src/skill_creator_mcp/config.py`**

**修改内容**:

```python
# 第54-66行 - 更新配置逻辑
# 新逻辑：优先使用工具参数，否则使用 SKILL_CREATOR_DEFAULT_OUTPUT_DIR 或 ~/skills
# 注意：
# 1. ~/skills 会被自动创建（如果不存在）
# 2. 推荐使用绝对路径避免混淆
# 3. 相对路径将基于 MCP Server 启动目录解析
default_output = os.getenv(
    "SKILL_CREATOR_DEFAULT_OUTPUT_DIR",
    "~/skills"  # 修改默认值为 ~/skills
)
output_dir_value = os.getenv("SKILL_CREATOR_OUTPUT_DIR", default_output)

# 移除 SKILL_CREATOR_OUTPUT_DIR 的处理，简化为单一环境变量
# 保留向后兼容：如果用户设置了 SKILL_CREATOR_OUTPUT_DIR，仍然生效
# 但文档中不再推荐使用
```

**第12-16行 - 更新文档字符串**:
```python
SKILL_CREATOR_DEFAULT_OUTPUT_DIR: 默认输出目录（当工具参数未设置时）
    - 默认值：~/skills (自动创建)
    - 推荐值：~/.claude/skills 或其他绝对路径
    - 注意：目录不存在时自动创建
```

---

**文件2: `src/skill_creator_mcp/utils/path_helpers.py`**

**新增函数**:

```python
def ensure_output_dir(output_dir: str | Path) -> Path:
    """确保输出目录存在，不存在则自动创建.

    Args:
        output_dir: 输出目录路径（支持相对路径、绝对路径、~路径）

    Returns:
        已验证/创建的绝对路径

    Raises:
        ValueError: 目录创建失败或无权限

    Examples:
        >>> # 默认 ~/skills
        >>> ensure_output_dir("~/skills")
        Path("/home/user/skills")

        >>> # 自定义目录
        >>> ensure_output_dir("~/.claude/skills")
        Path("/home/user/.claude/skills")
    """
    import os

    # 转换为 Path 对象
    dir_path = Path(output_dir)

    # 1. 展开 ~ 为用户主目录
    expanded_dir = dir_path.expanduser()

    # 2. 解析为绝对路径
    absolute_dir = expanded_dir.resolve()

    # 3. 检查目录是否存在
    if not absolute_dir.exists():
        # 4. 不存在则自动创建（包括父目录）
        try:
            absolute_dir.mkdir(parents=True, exist_ok=True)
        except OSError as e:
            raise ValueError(
                f"无法创建输出目录 {absolute_dir}: {e}"
            ) from e

    # 5. 验证是否为目录
    if not absolute_dir.is_dir():
        raise ValueError(
            f"输出路径不是目录: {absolute_dir}"
        )

    # 6. 验证可写性
    if not os.access(absolute_dir, os.W_OK):
        raise ValueError(
            f"输出目录不可写: {absolute_dir}"
        )

    return absolute_dir
```

**更新现有函数**:

```python
def get_default_output_dir() -> Path:
    """获取默认输出目录.

    优先级:
    1. SKILL_CREATOR_DEFAULT_OUTPUT_DIR 环境变量
    2. ~/skills (自动创建)

    注意：目录不存在时自动创建

    Returns:
        默认输出目录路径（已确保存在）
    """
    import os

    default_output = os.getenv("SKILL_CREATOR_DEFAULT_OUTPUT_DIR", "~/skills")
    return ensure_output_dir(default_output)
```

---

**文件3: `src/skill_creator_mcp/models/skill_config.py`**

**更新验证器**（在 `@model_validator(mode="after")` 中）:

```python
@model_validator(mode="after")
def validate_output_dir(self) -> Self:
    """验证并确保输出目录存在."""
    if self.output_dir is not None:
        # 使用新的 ensure_output_dir 函数
        from skill_creator_mcp.utils.path_helpers import ensure_output_dir

        try:
            self._output_dir = str(ensure_output_dir(self.output_dir))
        except ValueError as e:
            raise ValueError(f"输出目录验证失败: {e}") from e
    return self
```

---

#### 步骤2: 测试更新

**文件: `tests/test_tools/test_config.py`**

**新增测试**:

```python
def test_default_output_dir_is_home_skills():
    """测试默认输出目录为 ~/skills."""
    config = Config()
    # 验证默认路径包含用户主目录和 skills
    assert "skills" in str(config.default_output_dir)
    assert str(Path.home()) in str(config.default_output_dir)


def test_default_output_dir_auto_created():
    """测试默认目录自动创建."""
    import tempfile
    import shutil

    # 使用临时目录模拟
    with tempfile.TemporaryDirectory() as tmpdir:
        test_path = Path(tmpdir) / "test_skills"
        assert not test_path.exists()

        # 调用 ensure_output_dir
        from skill_creator_mcp.utils.path_helpers import ensure_output_dir
        result = ensure_output_dir(test_path)

        # 验证目录已创建
        assert result.exists()
        assert result.is_dir()


def test_custom_output_dir_from_env():
    """测试从环境变量读取自定义目录."""
    custom_dir = "~/.claude/skills"
    os.environ["SKILL_CREATOR_DEFAULT_OUTPUT_DIR"] = custom_dir

    try:
        config = Config()
        # 验证路径包含 .claude/skills
        assert ".claude" in str(config.default_output_dir)
        assert "skills" in str(config.default_output_dir)
    finally:
        del os.environ["SKILL_CREATOR_DEFAULT_OUTPUT_DIR"]
        reload_config()


def test_output_dir_not_writable_raises_error():
    """测试不可写目录报错."""
    import tempfile
    import stat

    with tempfile.TemporaryDirectory() as tmpdir:
        readonly_dir = Path(tmpdir) / "readonly"
        readonly_dir.mkdir()

        try:
            # 设置只读权限
            readonly_dir.chmod(stat.S_IRUSR | stat.S_IXUSR)

            from skill_creator_mcp.utils.path_helpers import ensure_output_dir
            with pytest.raises(ValueError, match="不可写"):
                ensure_output_dir(readonly_dir)
        finally:
            # 恢复权限以便清理
            readonly_dir.chmod(stat.S_IRWXU)
```

---

**文件: `tests/test_utils/test_path_helpers.py`**

**新增测试**:

```python
def test_ensure_output_dir_creates_missing_directory():
    """测试 ensure_output_dir 自动创建缺失目录."""
    with tempfile.TemporaryDirectory() as tmpdir:
        missing_dir = Path(tmpdir) / "a" / "b" / "skills"
        assert not missing_dir.exists()

        result = ensure_output_dir(missing_dir)

        assert result.exists()
        assert result.is_dir()


def test_ensure_output_dir_expands_tilde():
    """测试 ensure_output_dir 展开 ~."""
    result = ensure_output_dir("~/test_skills")
    assert str(Path.home()) in str(result)
    assert "test_skills" in str(result)


def test_ensure_output_dir_validates_existing_dir():
    """测试 ensure_output_dir 验证现有目录."""
    with tempfile.TemporaryDirectory() as tmpdir:
        # 测试目录
        result = ensure_output_dir(tmpdir)
        assert result == Path(tmpdir).resolve()

        # 测试文件（应报错）
        test_file = Path(tmpdir) / "not_a_dir"
        test_file.write_text("content")

        with pytest.raises(ValueError, match="不是目录"):
            ensure_output_dir(test_file)
```

---

#### 步骤3: 文档更新

**文件1: `README.md`**

**更新环境变量表格**:

```markdown
| 变量名 | 默认值 | 说明 |
|--------|--------|------|
| `SKILL_CREATOR_DEFAULT_OUTPUT_DIR` | `~/skills` (自动创建) | 默认输出目录 |

**配置优先级**：工具参数 > `SKILL_CREATOR_DEFAULT_OUTPUT_DIR` > 默认值 `~/skills`

> ⚠️ **重要提示 - MCP 协议限制**：
>
> 由于 MCP 协议限制，相对路径会基于 MCP Server 启动目录解析。
> **推荐使用绝对路径**（如 `~/.claude/skills`）确保行为一致。
>
> **目录自动管理**：系统会自动检测并创建输出目录（如果不存在）。
```

---

**文件2: `.env.example`**

```bash
# 输出目录配置
# SKILL_CREATOR_DEFAULT_OUTPUT_DIR: 默认输出目录
# 默认值: ~/skills (自动创建)
# 推荐值: ~/.claude/skills 或其他绝对路径
#
# 注意：
# 1. 目录不存在时会自动创建
# 2. 推荐使用绝对路径避免混淆
# 3. 相对路径基于 MCP Server 启动目录解析
#
# 示例：
# SKILL_CREATOR_DEFAULT_OUTPUT_DIR=~/skills
# SKILL_CREATOR_DEFAULT_OUTPUT_DIR=~/.claude/skills
# SKILL_CREATOR_DEFAULT_OUTPUT_DIR=/absolute/path/to/skills
```

---

**文件3: `docs/configuration.md`**

**新增章节**:

```markdown
## 输出目录配置

### 默认行为

当用户未配置 `SKILL_CREATOR_DEFAULT_OUTPUT_DIR` 时：
- 默认使用 `~/skills`
- 目录不存在时自动创建
- 支持所有 Agent-Skill 工具（init_skill, package_skill 等）

### 自定义配置

#### 方式1: 环境变量

```bash
export SKILL_CREATOR_DEFAULT_OUTPUT_DIR=~/.claude/skills
```

#### 方式2: .env 文件

```bash
SKILL_CREATOR_DEFAULT_OUTPUT_DIR=~/.claude/skills
```

#### 方式3: Claude Code 配置

```json
{
  "env": {
    "SKILL_CREATOR_DEFAULT_OUTPUT_DIR": "~/.claude/skills"
  }
}
```

### 目录自动管理

系统会自动执行以下操作：
1. 检查目录是否存在
2. 不存在则自动创建（包括父目录）
3. 验证目录可写性
4. 失败时返回明确的错误信息

### MCP 协议限制

**重要**: 相对路径会基于 MCP Server 启动目录解析，而非客户端工作目录。

**解决方案**: 使用绝对路径（推荐）或环境变量配置。

### 配置场景示例

| 使用场景 | 推荐配置 |
|----------|----------|
| **个人开发** | `~/skills` (默认) |
| **Claude 集成** | `~/.claude/skills` |
| **团队协作** | `/shared/team-skills` |
| **项目特定** | `~/projects/my-skills` |
```

---

**文件4: `CHANGELOG.md`**

```markdown
## [Unreleased]

### Changed

- **BREAKING**: 简化环境变量配置
  - 移除 `SKILL_CREATOR_OUTPUT_DIR`（不再推荐）
  - 保留 `SKILL_CREATOR_DEFAULT_OUTPUT_DIR` 作为唯一配置
  - 新默认值: `~/skills`（自动创建）

### Added

- 目录自动管理功能
  - 自动检测输出目录是否存在
  - 不存在时自动创建目录
  - 验证目录可写性

### Fixed

- 默认输出目录从 "." 改为 "~/skills"
  - 避免相对路径的混淆
  - 提供更好的用户体验

### Migration Notes

#### v0.3.x → v0.4.0

**环境变量变更**:
- ✅ 保留: `SKILL_CREATOR_DEFAULT_OUTPUT_DIR`
- ❌ 废弃: `SKILL_CREATOR_OUTPUT_DIR`

**默认行为变更**:
- v0.3.x: `.` (MCP Server 启动目录)
- v0.4.0: `~/skills` (用户主目录，自动创建)

**迁移步骤**:
1. 如果设置了 `SKILL_CREATOR_OUTPUT_DIR`，改用 `SKILL_CREATOR_DEFAULT_OUTPUT_DIR`
2. 如果未设置任何配置，无需操作，自动使用 `~/skills`
3. 首次使用时目录会自动创建
```

---

#### 步骤4: 验证清单

**代码验证**:
- [ ] `config.py` 默认值改为 `~/skills`
- [ ] `path_helpers.py` 新增 `ensure_output_dir` 函数
- [ ] `skill_config.py` 更新验证器调用 `ensure_output_dir`
- [ ] 所有工具（init_skill, package_skill 等）使用新逻辑

**测试验证**:
- [ ] 默认目录为 `~/skills`
- [ ] 目录不存在时自动创建
- [ ] 自定义目录正确生效
- [ ] 不可写目录正确报错
- [ ] 测试覆盖率 ≥95%
- [ ] 所有测试通过

**文档验证**:
- [ ] README.md 环境变量表格更新
- [ ] configuration.md 新增目录管理章节
- [ ] .env.example 配置示例更新
- [ ] CHANGELOG.md 迁移指南完整
- [ ] 所有文档说明一致

**代码质量**:
- [ ] ruff 检查 0 错误
- [ ] mypy 检查 0 错误
- [ ] 类型注解完整

---

### 5.2 验收标准

#### 功能验收

- [ ] 未配置时默认使用 `~/skills`
- [ ] 配置 `~/.claude/skills` 时正确使用
- [ ] 目录不存在时自动创建
- [ ] 不可写目录正确报错
- [ ] 相对路径正确解析并警告

#### 质量验收

- [ ] 测试覆盖率 ≥95%
- [ ] 所有测试通过
- [ ] ruff 检查 0 错误
- [ ] mypy 检查 0 错误

#### 文档验收

- [ ] 所有文档说明一致
- [ ] MCP 协议限制说明清晰
- [ ] 迁移指南完整
- [ ] 配置示例准确

---

## 六、开发流程（九步法）

### 步骤0: 前置任务审核 ✅

已完成 MCP 社区最佳实践研究和当前实现审核。

### 步骤1: 制定开发计划 ✅

本计划文档已完成。

### 步骤2: 拆分任务清单

**TODO 任务清单**（待执行）:

1. 修改 `config.py` - 更新默认值为 `~/skills`
2. 新增 `path_helpers.py` - 实现 `ensure_output_dir` 函数
3. 更新 `skill_config.py` - 调用目录自动创建逻辑
4. 更新 `test_config.py` - 添加默认值测试
5. 更新 `test_path_helpers.py` - 添加目录管理测试
6. 更新 `README.md` - 环境变量说明
7. 更新 `.env.example` - 配置示例
8. 更新 `docs/configuration.md` - 新增目录管理章节
9. 更新 `CHANGELOG.md` - 迁移指南

### 步骤3: 执行开发工作

按 TODO 清单顺序执行，每完成一项更新状态。

### 步骤4: 测试验证

```bash
# 运行测试套件
uv run pytest --cov

# 验证覆盖率 ≥95%
uv run pytest --cov --cov-report=html

# 代码质量检查
uv run ruff check .
uv run mypy src/
```

### 步骤5: 交叉验证

对照计划检查：
- [ ] 默认值为 `~/skills`
- [ ] 目录自动创建功能正常
- [ ] 自定义配置正确生效
- [ ] 所有文档更新一致

### 步骤6: 更新文档

- CHANGELOG.md
- CLAUDE.md（如需要）

### 步骤7: 阶段性审计

- 审查代码质量
- 审查测试覆盖率
- 审查文档一致性

### 步骤8: Git提交

```bash
git add .
git commit -m "feat(output): 实现目录自动管理功能

- 默认输出目录改为 ~/skills（自动创建）
- 新增 ensure_output_dir 函数实现目录自动管理
- 简化环境变量配置为 SKILL_CREATOR_DEFAULT_OUTPUT_DIR
- 更新所有相关文档和测试

Breaking Changes:
- 默认值从 . 改为 ~/skills
- SKILL_CREATOR_OUTPUT_DIR 标记为废弃

Co-Authored-By: Claude <noreply@anthropic.com>"
```

### 步骤9: 阶段性汇报

生成本次开发的汇报文档，归档计划到 `.claude/plans/archive/`。

---

## 七、关键文件清单

### 需要修改的文件

| 文件 | 修改类型 | 行号/章节 |
|------|----------|-----------|
| `config.py` | 代码 | 第55-60行，第12-16行 |
| `path_helpers.py` | 代码 | 新增 `ensure_output_dir` 函数 |
| `skill_config.py` | 代码 | 更新 `@model_validator` |
| `test_config.py` | 测试 | 新增4个测试用例 |
| `test_path_helpers.py` | 测试 | 新增3个测试用例 |
| `README.md` | 文档 | 环境变量表格 |
| `.env.example` | 配置 | 输出目录配置章节 |
| `docs/configuration.md` | 文档 | 新增目录管理章节 |
| `CHANGELOG.md` | 文档 | Unreleased 章节 |

---

## 八、风险与缓解

| 风险 | 缓解措施 |
|------|----------|
| 用户配置破坏 | 详细的迁移指南 + 版本公告 |
| 目录创建失败 | 明确的错误提示 + 权限检查 |
| 文档更新遗漏 | 交叉引用检查 + 文档审核 |
| 测试覆盖不足 | 新增 7 个测试用例覆盖所有场景 |
| 默认路径不符合预期 | 提供首次使用配置引导 |

---

## 九、参考资料

### 官方资源
- [MCP Servers Repository](https://github.com/modelcontextprotocol/servers)
- [MCP Best Practices](https://steipete.me/posts/2025/mcp-best-practices)
- [FastMCP Documentation](https://jlowin.github.io/fastmcp/)

### 关键 Issues 和 PRs
- [PR #2160: use working directory for default path](https://github.com/modelcontextprotocol/servers/pull/2160)
- [Issue #1520: How to access the current working directory](https://github.com/modelcontextprotocol/python-sdk/issues/1520)
- [Issue #1402: SDK does not handle optional parameters](https://github.com/modelcontextprotocol/python-sdk/issues/1402)

### 社区实现参考
- [mcp-zero](https://github.com/zeromicro/mcp-zero) - 当前工作目录策略
- [context7](https://github.com/upstash/context7) - 动态文档获取
- [gemini-mcp-server](https://github.com/Garblesnarff/gemini-mcp-server) - 用户主目录策略

---

## 十、计划总结

### 核心目标

实现 `SKILL_CREATOR_DEFAULT_OUTPUT_DIR` 参数的完整功能：
1. **默认值**: `~/skills`（自动创建）
2. **自定义支持**: `~/.claude/skills` 或其他路径
3. **目录自动管理**: 检测 → 创建 → 验证

### 实施要点

| 要点 | 说明 |
|------|------|
| **代码修改** | 3个文件（config.py, path_helpers.py, skill_config.py） |
| **测试新增** | 7个测试用例 |
| **文档更新** | 4个文档（README, configuration, .env.example, CHANGELOG） |
| **验收标准** | 测试覆盖率≥95%，所有测试通过 |

### 预期效果

| 用户场景 | 行为 |
|----------|------|
| **未配置** | 自动使用 `~/skills`，目录不存在时自动创建 |
| **配置 `~/.claude/skills`** | 使用用户配置，目录不存在时自动创建 |
| **配置 `/absolute/path`** | 使用绝对路径，目录不存在时自动创建 |

---

**计划版本**: v2.0
**最后更新**: 2026-01-26
**状态**: 待审核批准

