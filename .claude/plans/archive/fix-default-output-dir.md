# 默认输出目录修复计划

> **计划日期**: 2026-01-26
> **计划类型**: Bug修复 - 回滚错误变更
> **优先级**: P0 (阻塞)
> **相关审核**: 基于用户对 `2026-01-26-hardcoded-path-fix-report.md` 的全面审核反馈

---

## 一、问题确认

### 1.1 用户明确要求

```
在不配置 SKILL_CREATOR_OUTPUT_DIR 参数时，默认必须使用当前项目开发环境目录
在用户配置 SKILL_CREATOR_OUTPUT_DIR 时，使用用户自定义配置的目录
```

### 1.2 当前实现状态 (commit 206c7cb, Unreleased)

| 项目 | 值 | 符合用户要求 |
|------|-----|-------------|
| 默认输出目录 | `~/agent-skills` | ❌ 否 |
| 环境变量支持 | ✅ | ✅ 是 |
| 路径验证 | ✅ | ✅ 是 |

### 1.3 版本对比

| 版本 | 默认值 | 状态 |
|------|--------|------|
| v0.3.3 (已发布) | `.` | ✅ 符合用户要求 |
| commit 206c7cb (Unreleased) | `~/agent-skills` | ❌ 不符合用户要求 |

---

## 二、根因分析

### 2.1 错误引入

Commit `206c7cb` ("fix: 全面修复硬编码路径问题") 将默认值从 `.` 改为 `~/agent-skills`，这**与用户明确要求相反**。

### 2.2 技术限制

MCP 协议无法获取客户端工作目录：
- `.` 实际指向 MCP Server 启动目录
- 无法指向客户端工作目录（如 `~/test/tmp/`）

但用户明确要求：**默认必须使用当前项目开发环境目录**，即恢复 `.` 作为默认值。

---

## 三、修复方案

### 3.1 方案选择

**方案**: 精准回滚默认值，保留其他改进

### 3.2 核心原则

1. **禁止使用所谓的向后兼容** - 直接恢复正确行为
2. **保留有价值改进** - 环境变量、缓存配置等功能
3. **完整文档说明** - 明确技术限制和推荐用法

---

## 四、详细修改清单

### 4.1 代码修改

#### 文件1: `skill-creator-mcp/src/skill_creator_mcp/config.py`

**第55-57行** - 恢复默认值为 `.`

```python
# 修改前
default_output = os.getenv(
    "SKILL_CREATOR_DEFAULT_OUTPUT_DIR",
    "~/agent-skills"
)

# 修改后
default_output = os.getenv(
    "SKILL_CREATOR_DEFAULT_OUTPUT_DIR",
    "."
)
```

**第54行** - 更新注释

```python
# 修改前
# 新逻辑：优先使用 SKILL_CREATOR_OUTPUT_DIR，否则使用 SKILL_CREATOR_DEFAULT_OUTPUT_DIR 或 ~/agent-skills

# 修改后
# 新逻辑：优先使用 SKILL_CREATOR_OUTPUT_DIR，否则使用 SKILL_CREATOR_DEFAULT_OUTPUT_DIR 或 . (当前目录)
```

**文档字符串第14行、第16行** - 更新说明

```python
# 修改前
# - 默认值：SKILL_CREATOR_DEFAULT_OUTPUT_DIR 或 ~/agent-skills
# SKILL_CREATOR_DEFAULT_OUTPUT_DIR: 默认输出目录（当 OUTPUT_DIR 未设置时）
#     - 默认值：~/agent-skills

# 修改后
# - 默认值：SKILL_CREATOR_DEFAULT_OUTPUT_DIR 或 . (当前目录)
# SKILL_CREATOR_DEFAULT_OUTPUT_DIR: 默认输出目录（当 OUTPUT_DIR 未设置时）
#     - 默认值：. (当前目录)
#     - 注意：由于MCP协议限制，"." 指向MCP Server启动目录
```

---

#### 文件2: `skill-creator-mcp/src/skill_creator_mcp/utils/path_helpers.py`

**第33行** - 恢复默认值为 `.`

```python
# 修改前
default_output = os.getenv("SKILL_CREATOR_DEFAULT_OUTPUT_DIR", "~/agent-skills")

# 修改后
default_output = os.getenv("SKILL_CREATOR_DEFAULT_OUTPUT_DIR", ".")
```

**第24-26行** - 更新文档字符串

```python
# 修改前
# 优先级:
# 1. SKILL_CREATOR_DEFAULT_OUTPUT_DIR 环境变量
# 2. ~/agent-skills

# 修改后
# 优先级:
# 1. SKILL_CREATOR_DEFAULT_OUTPUT_DIR 环境变量
# 2. . (当前目录)
#
# 注意：由于MCP协议限制，"." 指向MCP Server启动目录，而非客户端工作目录
```

---

### 4.2 测试修改

#### 文件3: `skill-creator-mcp/tests/test_tools/test_config.py`

**第42-43行** - 更新测试断言

```python
# 修改前
# 默认输出目录现在是 ~/agent-skills
assert "agent-skills" in str(config.output_dir) or config.output_dir == Path("~/agent-skills").expanduser()

# 修改后
# 默认输出目录是当前目录 "."
assert config.output_dir == Path(".").resolve() or str(config.output_dir) == "."
```

---

### 4.3 配置示例修改

#### 文件4: `skill-creator-mcp/.env.example`

**第20行、第24行** - 更新示例

```bash
# 修改前
SKILL_CREATOR_OUTPUT_DIR=~/agent-skills
SKILL_CREATOR_DEFAULT_OUTPUT_DIR=~/agent-skills

# 修改后
# 推荐设置为绝对路径，确保在不同工作目录下行为一致
# SKILL_CREATOR_OUTPUT_DIR=~/my-skills
# SKILL_CREATOR_DEFAULT_OUTPUT_DIR=.  # 默认值，通常不需要设置

# 注意：由于MCP协议限制，"." 指向MCP Server启动目录
# 推荐使用绝对路径避免混淆
```

---

### 4.4 文档修改

#### 文件5: `skill-creator-mcp/README.md`

**更新配置优先级说明章节**

在适当位置添加重要提示：

```markdown
**重要提示 - MCP 协议限制**：

由于 MCP 协议限制，默认值 `.` 实际指向 MCP Server 启动目录，而非客户端工作目录。

**推荐配置**：
```bash
# 使用绝对路径确保行为一致
export SKILL_CREATOR_OUTPUT_DIR=~/my-skills
```

**配置优先级**：工具参数 > `SKILL_CREATOR_OUTPUT_DIR` > 默认值 `.`
```

---

#### 文件6: `skill-creator-mcp/docs/configuration.md`

**添加技术限制说明章节**

```markdown
### MCP 协议限制说明

#### 默认值 `.` 的实际行为

由于 MCP 协议设计限制，MCP Server 无法获取客户端工作目录。

| 期望行为 | 实际行为 |
|----------|----------|
| 指向客户端工作目录 | 指向 MCP Server 启动目录 |

**推荐解决方案**：

1. **使用环境变量**（推荐）：
   ```bash
   export SKILL_CREATOR_OUTPUT_DIR=~/my-skills
   ```

2. **Claude Code 配置**：
   ```json
   {
     "env": {
       "SKILL_CREATOR_OUTPUT_DIR": "~/my-skills"
     }
   }
   ```

3. **工具参数显式指定**：
   ```python
   await init_skill(ctx, name="test", output_dir="~/my-skills")
   ```
```

---

### 4.5 变更日志

#### 文件7: `CHANGELOG.md`

**替换 Unreleased 章节内容**

```markdown
## [Unreleased]

### Fixed

- **P0**: 修复默认输出目录不符合用户要求的问题
  - 默认值从 `~/agent-skills` 恢复为 `.` (与 v0.3.3 一致)
  - 用户明确要求：不配置时默认必须使用当前项目开发环境目录
  - 更新文档说明 MCP 协议限制和推荐用法

### Changed

- **BREAKING**: 恢复 v0.3.3 的默认输出目录行为 (`.` 而非 `~/agent-skills`)
- `SKILL_CREATOR_DEFAULT_OUTPUT_DIR` 不再推荐在文档中作为默认配置

### Migration Notes

如果您已在 `.env` 中设置了 `SKILL_CREATOR_DEFAULT_OUTPUT_DIR=~/agent-skills`：
- 可以安全移除此配置
- 系统将使用默认值 `.`

**推荐配置**（由于 MCP 协议限制）：
```bash
# 使用绝对路径避免 "." 指向 MCP Server 启动目录的混淆
export SKILL_CREATOR_OUTPUT_DIR=~/my-skills
```
```

---

## 五、验证计划

### 5.1 功能验证

```python
# 测试1: 验证默认值
import os
os.environ.pop("SKILL_CREATOR_OUTPUT_DIR", None)
os.environ.pop("SKILL_CREATOR_DEFAULT_OUTPUT_DIR", None)

from skill_creator_mcp.config import get_config
config = get_config()
assert config.output_dir == Path(".").resolve()

# 测试2: 验证环境变量优先级
os.environ["SKILL_CREATOR_OUTPUT_DIR"] = "/tmp/test"
config = get_config()
assert config.output_dir == Path("/tmp/test")
```

### 5.2 测试套件验证

```bash
cd skill-creator-mcp
uv run pytest --cov
uv run ruff check .
uv run mypy src/
```

**验收标准**:
- ✅ 所有测试通过
- ✅ 测试覆盖率 ≥94%
- ✅ 代码检查 0 错误
- ✅ 类型检查 0 错误

### 5.3 交叉验证

| 检查项 | 方法 | 预期 |
|--------|------|------|
| 默认值 | 代码审查 | `.` |
| 环境变量 | 功能测试 | 优先级正确 |
| 文档一致性 | 文档审查 | 说明正确 |
| 测试覆盖 | pytest | 全部通过 |

---

## 六、关键文件清单

| 文件 | 修改类型 | 行号 |
|------|----------|------|
| `src/skill_creator_mcp/config.py` | 代码 | 54, 55-57, 14, 16 |
| `src/skill_creator_mcp/utils/path_helpers.py` | 代码 | 33, 24-26 |
| `tests/test_tools/test_config.py` | 测试 | 42-43 |
| `.env.example` | 配置 | 20, 24 |
| `README.md` | 文档 | 配置章节 |
| `docs/configuration.md` | 文档 | 新增章节 |
| `CHANGELOG.md` | 文档 | Unreleased章节 |

---

## 七、风险与缓解

| 风险 | 缓解措施 |
|------|----------|
| 用户设置了 `SKILL_CREATOR_DEFAULT_OUTPUT_DIR=~/agent-skills` | CHANGELOG 明确说明迁移指南 |
| 依赖 `~/agent-skills` 的自动化脚本 | 文档明确说明变更 |

---

## 八、验收标准

### 8.1 功能验收

- [ ] 默认输出目录为 `.`（与 v0.3.3 一致）
- [ ] `SKILL_CREATOR_OUTPUT_DIR` 环境变量优先级正确
- [ ] 文档说明 MCP 协议限制

### 8.2 质量验收

- [ ] 所有测试通过
- [ ] 测试覆盖率 ≥94%
- [ ] ruff check 0 错误
- [ ] mypy 0 错误

### 8.3 文档验收

- [ ] CHANGELOG.md 更新完整
- [ ] README.md 说明正确
- [ ] docs/configuration.md 技术限制说明完整

---

## 九、开发规范流程（九步法）

```
步骤0: 前置任务审核  → ✅ 本次审核已完成
步骤1: 制定开发计划  → ✅ 本计划文档
步骤2: 拆分任务清单  → 待执行（7个文件修改）
步骤3: 执行开发工作  → 待执行
步骤4: 测试验证      → 待执行
步骤5: 交叉验证      → 待执行
步骤6: 更新文档      → 待执行
步骤7: 阶段性审计    → 待执行
步骤8: Git提交       → 待执行
步骤9: 阶段性汇报    → 待执行
```
