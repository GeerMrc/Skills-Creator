# Skill-Creator 开发执行计划 - validate_skill Tool

> **计划版本**: v2.0
> **制定日期**: 2026-01-20
> **当前分支**: feature/init-skill-tool
> **状态**: 已规划完成

---

## 一、开发规范要求概述

### 1.1 Git 工作流
- 采用 **Feature Branch Workflow**
- 继续在当前分支 `feature/init-skill-tool` 开发
- 使用 Conventional Commits 格式：`<type>(<scope>): <subject>`

### 1.2 质量门禁标准
| 指标 | 标准 | 检查命令 |
|------|------|----------|
| 测试覆盖率 | ≥95% | `PYTHONPATH=src uv run pytest --cov` |
| 代码规范 | 无警告 | `uv run ruff check` |
| 类型检查 | 无错误 | `uv run mypy src/` |

### 1.3 阶段验收机制
每个开发阶段必须通过验收标准才能进入下一阶段。

---

## 二、当前任务分析

### 2.1 已完成工作
- `e0a2945` - feat(project): initialize skill-creator-mcp project framework
- `bad964f` - feat(tools): implement init_skill tool
- `6bd819d` - test: 补充测试覆盖率到 95% 并修复类型检查

### 2.2 用户确认决策
- ✅ 继续在 `feature/init-skill-tool` 分支开发
- ✅ 优先实现 **validate_skill** tool (P0)

---

## 三、代码库探索结果总结

### 3.1 现有验证器 (utils/validators.py)
| 函数 | 功能 | 可复用性 |
|------|------|----------|
| `validate_skill_name()` | 验证名称格式 | ✅ 可复用 |
| `validate_skill_directory()` | 验证目录存在和 SKILL.md | ✅ 可复用 |
| `validate_template_type()` | 验证模板类型 | ✅ 可复用 |

### 3.2 init_skill 实现模式参考
- **MCP Tool 装饰器**: `@mcp.tool()`
- **异步 I/O**: 使用 `asyncio.to_thread()` 包装文件操作
- **错误处理**: 区分 `ValueError` 和通用 `Exception`
- **返回格式**: `{"success": bool, "data": dict, "error": str}`

### 3.3 项目测试标准
- **测试目录**: tests/{test_tools, test_models, test_integration, test_mcp}/
- **共享 fixtures**: `temp_dir`, `sample_skill_dir`
- **测试配置**: asyncio_mode = "auto", 覆盖率报告 HTML

---

## 四、validate_skill 功能需求

### 4.1 验证类别

| 验证类别 | 验证项 | 优先级 |
|---------|--------|--------|
| **基础结构** | 目录存在性、SKILL.md 存在、必需子目录 | P0 |
| **命名规范** | 目录名格式、name 字段与目录名一致 | P0 |
| **格式规范** | YAML frontmatter 有效、必需字段存在 | P0 |
| **模板特定** | 根据模板类型检查必需引用文件 | P1 |
| **内容质量** | description 质量、示例完整性 | P2 |

### 4.2 模板特定验证规则

| 模板类型 | 必需引用文件 | allowed-tools |
|---------|-------------|---------------|
| minimal | 无 | Read, Write, Edit, Bash |
| tool-based | tool-integration.md, usage-examples.md | Read, Write, Edit, Bash |
| workflow-based | workflow-steps.md, decision-points.md | Read, Write, Edit, Bash, Glob, Grep |
| analyzer-based | analysis-methods.md, metrics.md | Read, Glob, Grep, Bash |

---

## 五、完整 TODO 任务清单

### 阶段 1：数据模型设计

- [ ] 1.1 在 `models/skill_config.py` 添加 `ValidateSkillInput` 模型
  - 参数：`skill_path: str`, `check_structure: bool = True`, `check_content: bool = True`
- [ ] 1.2 添加 `ValidationResult` 模型
  - 字段：`valid: bool`, `skill_path: str`, `skill_name: str`, `errors: list[str]`, `warnings: list[str]`, `checks: dict[str, bool]`
- [ ] 1.3 创建模型单元测试 `tests/test_models/test_validate_skill.py`

### 阶段 2：验证逻辑实现

- [ ] 2.1 在 `utils/validators.py` 添加 `_validate_structure()` 函数
  - 检查必需文件：SKILL.md
  - 检查必需目录：references, examples, scripts, .claude
- [ ] 2.2 添加 `_validate_naming()` 函数
  - 验证目录名格式（复用 `validate_skill_name()`）
  - 验证 SKILL.md 中的 name 字段与目录名一致
- [ ] 2.3 添加 `_validate_skill_md()` 函数
  - 解析 YAML frontmatter
  - 检查必需字段：name, description, allowed-tools
  - 验证 allowed-tools 包含有效工具名
- [ ] 2.4 添加 `_validate_template_requirements()` 函数
  - 根据模板类型检查必需的引用文件

### 阶段 3：MCP Tool 实现

- [ ] 3.1 在 `server.py` 添加 `validate_skill` 函数（使用 `@mcp.tool()` 装饰器）
- [ ] 3.2 实现异步验证流程
- [ ] 3.3 添加详细的错误处理和日志记录

### 阶段 4：单元测试

- [ ] 4.1 创建 `tests/test_tools/test_validate_skill.py`
- [ ] 4.2 测试有效技能目录验证（所有检查通过）
- [ ] 4.3 测试无效技能目录（缺少 SKILL.md）
- [ ] 4.4 测试无效目录名
- [ ] 4.5 测试 SKILL.md 格式错误（无 YAML frontmatter）
- [ ] 4.6 测试缺失必需字段
- [ ] 4.7 测试模板特定验证

### 阶段 5：集成测试

- [ ] 5.1 创建 `tests/test_integration/test_validate_skill_integration.py`
- [ ] 5.2 测试完整的验证流程（使用 init_skill 创建后验证）

### 阶段 6：MCP 测试

- [ ] 6.1 创建 `tests/test_mcp/test_validate_skill_mcp.py`
- [ ] 6.2 测试 MCP 工具调用和返回格式

### 阶段 7：质量检查

- [ ] 7.1 运行所有测试：`PYTHONPATH=src uv run pytest`
- [ ] 7.2 检查覆盖率 ≥95%：`PYTHONPATH=src uv run pytest --cov`
- [ ] 7.3 代码规范检查：`uv run ruff check`
- [ ] 7.4 类型检查：`uv run mypy src/`

### 阶段 8：提交代码

- [ ] 8.1 Git add 新增/修改的文件
- [ ] 8.2 创建符合规范的提交：`feat(tools): add validate_skill tool`
- [ ] 8.3 推送到远程：`git push origin feature/init-skill-tool`

---

## 六、关键文件清单

### 需要修改的文件

| 文件路径 | 修改内容 | 优先级 |
|---------|---------|--------|
| `skill-creator-mcp/src/skill_creator_mcp/models/skill_config.py` | 添加验证模型 | P0 |
| `skill-creator-mcp/src/skill_creator_mcp/utils/validators.py` | 添加验证函数 | P0 |
| `skill-creator-mcp/src/skill_creator_mcp/server.py` | 添加 validate_skill tool | P0 |

### 需要新建的文件

| 文件路径 | 内容 | 优先级 |
|---------|------|--------|
| `skill-creator-mcp/tests/test_models/test_validate_skill.py` | 模型测试 | P0 |
| `skill-creator-mcp/tests/test_tools/test_validate_skill.py` | 单元测试 | P0 |
| `skill-creator-mcp/tests/test_integration/test_validate_skill_integration.py` | 集成测试 | P1 |
| `skill-creator-mcp/tests/test_mcp/test_validate_skill_mcp.py` | MCP 测试 | P1 |

---

## 七、验收标准

### 功能验收
- [ ] 可以验证技能目录结构完整性
- [ ] 可以检测缺失的必需文件/目录
- [ ] 可以验证 SKILL.md 格式和必需字段
- [ ] 可以根据模板类型检查特定要求
- [ ] 返回清晰的验证结果（成功/失败+详情）

### 质量验收
- [ ] 所有测试通过
- [ ] 测试覆盖率 ≥95%
- [ ] ruff 检查无警告
- [ ] mypy 类型检查无错误

---

## 八、实现参考代码片段

### 8.1 数据模型示例

```python
# models/skill_config.py
class ValidateSkillInput(BaseModel):
    """验证技能输入参数模型."""
    skill_path: str = Field(..., description="技能目录路径")
    check_structure: bool = Field(default=True, description="检查目录结构")
    check_content: bool = Field(default=True, description="检查内容格式")

class ValidationResult(BaseModel):
    """验证结果模型."""
    valid: bool
    skill_path: str
    skill_name: str | None = None
    template_type: str | None = None
    errors: list[str] = []
    warnings: list[str] = []
    checks: dict[str, bool] = {}
```

### 8.2 验证函数示例

```python
# utils/validators.py
def _validate_structure(skill_dir: Path) -> list[str]:
    """验证目录结构."""
    errors = []
    required_dirs = ["references", "examples", "scripts", ".claude"]
    for dir_name in required_dirs:
        if not (skill_dir / dir_name).exists():
            errors.append(f"缺少必需目录: {dir_name}")
    return errors
```

---

**计划状态**: 已完成，等待用户批准进入实施阶段
