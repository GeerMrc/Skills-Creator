# 路径解析修复与用户工作目录支持 - 阶段汇报

**日期**: 2026-01-26
**计划类型**: 缺陷修复 + 用户体验优化
**状态**: 已完成

---

## 一、执行摘要

本次修复解决了用户报告的路径解析问题：在 `~/test/tmp/` 目录开发时，代码被写入 `~/.claude/skills/generating-presentations` 而非当前目录。

### 核心变更

| 变更类型 | 描述 |
|---------|------|
| **新增功能** | `SKILL_CREATOR_OUTPUT_DIR` 环境变量支持 |
| **路径验证** | 自动创建目录、检查可写性、支持 `~` 展开 |
| **参数优化** | `output_dir` 改为可选，默认使用环境变量 |
| **文档更新** | 路径解析规则说明和推荐用法 |

### 质量指标

| 指标 | 结果 |
|------|------|
| 测试通过率 | 589/589 (100%) |
| 测试覆盖率 | 95% |
| ruff check | 0 错误 |
| mypy check | 0 错误 |

---

## 二、完成的工作

### 2.1 代码修改

**文件**: `skill-creator-mcp/src/skill_creator_mcp/models/skill_config.py`
- 添加 `model_validator` 导入
- 为 `InitSkillInput` 添加 `validate_output_dir_model()` 验证器
- 为 `PackageSkillInput` 添加 `validate_output_dir_model()` 验证器
- 新增 `PackageAgentSkillInput` 数据模型

**文件**: `skill-creator-mcp/src/skill_creator_mcp/server.py`
- `init_skill`: `output_dir` 改为可选，读取环境变量
- `package_skill`: `output_dir` 改为可选，读取环境变量
- `package_agent_skill`: `output_dir` 改为可选，使用 `PackageAgentSkillInput` 验证

**文件**: `skill-creator-mcp/src/skill_creator_mcp/config.py`
- 更新模块文档字符串，详细说明环境变量用法

### 2.2 文档更新

**文件**: `skill-creator/references/mcp-integration.md`
- 添加环境变量工具支持列
- 新增"路径解析规则"章节
- 说明配置优先级和推荐做法

**文件**: `skill-creator/SKILL.md`
- 添加"环境配置（推荐）"章节
- 说明如何设置 `SKILL_CREATOR_OUTPUT_DIR`

**文件**: `CHANGELOG.md`
- 添加 [Unreleased] 变更记录

### 2.3 测试新增

**文件**: `skill-creator-mcp/tests/test_tools/test_init_skill.py`
- `test_output_dir_validation_with_nonexistent_path`: 测试自动创建目录
- `test_output_dir_validation_with_file_instead_of_dir`: 测试文件路径报错
- `test_output_dir_expands_tilde`: 测试 `~` 展开
- `test_output_dir_validates_read_only_directory`: 测试只读目录报错
- `test_output_dir_converts_relative_to_absolute`: 测试相对路径转换
- `test_init_skill_respects_env_var`: 测试环境变量读取

**文件**: `skill-creator-mcp/tests/test_models/test_skill_config.py`
- 更新 `test_init_skill_input_valid` 和 `test_init_skill_input_defaults` 以反映新行为

**文件**: `skill-creator-mcp/tests/test_tools/test_health_check.py`
- 修复 `test_package_agent_skill_internal_error_handling` 使用临时目录

---

## 三、技术实现细节

### 3.1 验证器架构

使用 Pydantic v2 的 `@model_validator(mode="after")` 确保默认值也被处理：

```python
@model_validator(mode="after")
def validate_output_dir_model(self) -> "InitSkillInput":
    """验证 output_dir 字段（模型级别验证，确保默认值也被处理）."""
    original = self.output_dir
    path = Path(original).expanduser().resolve()

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

    # 更新 output_dir 为绝对路径
    self.output_dir = str(path)
    return self
```

### 3.2 配置优先级

```
工具参数 output_dir="xxx"
  ↓ (如果为 None)
环境变量 SKILL_CREATOR_OUTPUT_DIR
  ↓ (如果未设置)
默认值 "."
```

### 3.3 工具函数修改

```python
async def init_skill(
    ctx: Context,
    name: str,
    template: str = "minimal",
    output_dir: str | None = None,  # 改为可选
    ...
) -> dict[str, Any]:
    from .config import get_config

    # 优先级：工具参数 > 环境变量 > 默认值
    config = get_config()
    if output_dir is None:
        output_dir = str(config.output_dir)

    # 使用 Pydantic 验证输入参数
    input_data = InitSkillInput.model_validate({
        "name": name,
        "template": template,
        "output_dir": output_dir,
        ...
    })
    ...
```

---

## 四、用户使用指南

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

## 五、验收结果

### 功能验收

| 场景 | 预期行为 | 结果 |
|------|----------|------|
| 设置环境变量 | 技能创建在环境变量指定目录 | ✅ 通过 |
| 工具参数 | 参数覆盖环境变量 | ✅ 通过 |
| 路径不存在 | 自动创建目录 | ✅ 通过 |
| 路径是文件 | 报错"不是目录" | ✅ 通过 |
| 只读目录 | 报错"不可写" | ✅ 通过 |
| ~ 展开 | 展开为用户主目录 | ✅ 通过 |
| 相对路径 | 转换为绝对路径 | ✅ 通过 |

### 质量验收

| 指标 | 要求 | 结果 |
|------|------|------|
| 测试覆盖率 | ≥80% | 95% ✅ |
| ruff check | 0 错误 | 0 ✅ |
| mypy check | 0 错误 | 0 ✅ |
| 新增测试用例 | - | 6 个 |

---

## 六、Git 提交

**提交哈希**: `53080ac`
**分支**: `develop`

**提交信息**:
```
fix(config): 修复路径解析并支持环境变量

问题：
- output_dir="." 相对于 MCP Server 启动目录解析
- 用户在 ~/test/tmp/ 开发时文件被写入错误位置
- SKILL_CREATOR_OUTPUT_DIR 环境变量未生效

修改：
- init_skill, package_skill, package_agent_skill 读取环境变量
- 添加 InitSkillInput, PackageSkillInput, PackageAgentSkillInput 路径验证器
- 自动创建不存在的目录
- 支持 ~ 展开、相对路径转换
- 更新文档说明路径解析规则和推荐用法

测试：新增6个测试用例，覆盖率95%

Co-Authored-By: Claude <noreply@anthropic.com>
```

**修改文件**:
- `CHANGELOG.md`
- `skill-creator-mcp/src/skill_creator_mcp/config.py`
- `skill-creator-mcp/src/skill_creator_mcp/models/skill_config.py`
- `skill-creator-mcp/src/skill_creator_mcp/server.py`
- `skill-creator-mcp/tests/test_models/test_skill_config.py`
- `skill-creator-mcp/tests/test_tools/test_health_check.py`
- `skill-creator-mcp/tests/test_tools/test_init_skill.py`
- `skill-creator/SKILL.md`
- `skill-creator/references/mcp-integration.md`

---

## 七、已知限制

1. **FastMCP Context 限制**: Context 类没有 `cwd` 属性，无法直接获取用户当前工作目录
2. **MCP 协议限制**: 协议本身不传递客户端工作目录信息
3. **解决方案**: 通过环境变量配置默认输出目录

---

## 八、后续建议

1. **文档推广**: 在 README.md 中添加环境变量配置说明
2. **用户反馈**: 收集用户使用环境变量的反馈
3. **监控**: 添加路径验证失败情况监控
4. **优化**: 考虑支持更多路径相关配置选项

---

**报告生成时间**: 2026-01-26
**计划归档位置**: `.claude/plans/archive/2026-01-26-path-resolution-fix.md`
