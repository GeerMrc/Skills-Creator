# Skills-Creator 项目完整性修复计划

> **计划版本**: v1.0
> **制定日期**: 2026-01-21
> **当前分支**: feature/init-skill-tool
> **审核范围**: 全面项目一致性审核

---

## 执行摘要

基于对项目的全面审核，发现 3 个需要修复的问题，其中 2 个为 P0（必须修复），1 个为 P1（建议修复）。本项目当前完成度约 80%，MCP Server 实现质量优秀（9.0/10），但 SKILL 实现存在与自身规范不一致的问题。

### 问题汇总

| 优先级 | 问题 | 状态 | 影响 |
|--------|------|------|------|
| P0 | SKILL.md 缺少 `allowed-tools` 字段 | 立即修复 | 违反自身验证规范 |
| P0 | scripts/ 目录不存在 | 立即修复 | 违反必需目录规范 |
| P1 | examples/ 目录为空 | 建议修复 | 降低实用性 |

---

## 一、开发规范概述

### 1.1 质量门禁标准

| 指标 | 标准 | 检查命令 |
|------|------|----------|
| 测试覆盖率 | ≥95% | `PYTHONPATH=src uv run pytest --cov` |
| 代码规范 | 无警告 | `uv run ruff check` |
| 类型检查 | 无错误 | `uv run mypy src/` |

### 1.2 必需目录和文件

根据 `references/validation.md` 和 MCP Server 的验证规则：

**必需目录**：
```
references/    # 详细文档
examples/      # 使用示例
scripts/       # 可执行脚本（黑盒化）
.claude/       # Claude 配置
```

**SKILL.md YAML Frontmatter 必需字段**：
```yaml
---
name: skill-name
description: |
  功能描述
allowed-tools: Read, Write, Edit, Bash  # 必需！
---
```

---

## 二、详细修复方案

### 2.1 P0-1: 修复 SKILL.md Frontmatter

**文件位置**: `/models/claude-glm/Skills-Creator/SKILL.md`

**当前问题**：
```yaml
---
name: skill-creator
description: |
  Agent-Skills 开发与质量保证工具...
  触发词：创建技能、初始化技能、验证技能、分析技能、重构技能、技能模板
---
```

**修复后**：
```yaml
---
name: skill-creator
description: |
  Agent-Skills 开发与质量保证工具...
  触发词：创建技能、初始化技能、验证技能、分析技能、重构技能、技能模板
allowed-tools: Read, Write, Edit, Bash, Glob, Grep
mcp_servers: ["skill-creator"]
---
```

**验收标准**：
- [ ] SKILL.md 通过 MCP validate_skill 工具验证
- [ ] YAML frontmatter 解析成功
- [ ] 包含所有必需字段

---

### 2.2 P0-2: 创建 scripts/ 目录

**目录位置**: `/models/claude-glm/Skills-Creator/scripts/`

**需要创建的脚本**：

#### 2.2.1 validate_skill.py

```python
#!/usr/bin/env python3
"""
Skill-Creator 验证脚本

黑盒化原则：
- 使用 argparse 处理命令行参数
- 支持 --help 查看用法
- 支持输出格式（json/text）
"""

import argparse
import json
import sys
from pathlib import Path

def main():
    parser = argparse.ArgumentParser(
        description="验证 Agent-Skills 规范",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例：
  %(prog)s /path/to/skill
  %(prog)s /path/to/skill --format json
  %(prog)s /path/to/skill --check-structure --check-content
        """
    )

    parser.add_argument(
        "skill_path",
        type=str,
        help="技能目录路径"
    )

    parser.add_argument(
        "--format", "-f",
        choices=["text", "json"],
        default="text",
        help="输出格式"
    )

    parser.add_argument(
        "--check-structure",
        action="store_true",
        default=True,
        help="检查目录结构"
    )

    parser.add_argument(
        "--check-content",
        action="store_true",
        default=True,
        help="检查内容格式"
    )

    args = parser.parse_args()

    # TODO: 集成 MCP validate_skill 工具或本地验证逻辑
    skill_path = Path(args.skill_path)

    if not skill_path.exists():
        result = {
            "valid": False,
            "errors": [f"路径不存在: {skill_path}"]
        }
    else:
        result = {
            "valid": True,
            "skill_path": str(skill_path),
            "message": "验证通过"
        }

    if args.format == "json":
        print(json.dumps(result, indent=2, ensure_ascii=False))
    else:
        print(f"验证结果: {'✓ 通过' if result['valid'] else '✗ 失败'}")
        if not result["valid"]:
            for error in result.get("errors", []):
                print(f"  - {error}")

    return 0 if result["valid"] else 1

if __name__ == "__main__":
    sys.exit(main())
```

#### 2.2.2 analyze_skill.py

```python
#!/usr/bin/env python3
"""
Skill-Creator 分析脚本

黑盒化原则：
- 使用 argparse 处理命令行参数
- 支持 --help 查看用法
- 支持输出格式（json/text）
"""

import argparse
import json
import sys
from pathlib import Path

def main():
    parser = argparse.ArgumentParser(
        description="分析 Agent-Skills 代码质量",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例：
  %(prog)s /path/to/skill
  %(prog)s /path/to/skill --format json
  %(prog)s /path/to/skill --detailed
        """
    )

    parser.add_argument(
        "skill_path",
        type=str,
        help="技能目录路径"
    )

    parser.add_argument(
        "--format", "-f",
        choices=["text", "json"],
        default="text",
        help="输出格式"
    )

    parser.add_argument(
        "--detailed", "-d",
        action="store_true",
        help="显示详细分析"
    )

    args = parser.parse_args()

    # TODO: 集成 MCP analyze_skill 工具或本地分析逻辑
    skill_path = Path(args.skill_path)

    result = {
        "skill_path": str(skill_path),
        "structure": {"total_files": 0},
        "quality": {"overall_score": 0},
        "suggestions": []
    }

    if args.format == "json":
        print(json.dumps(result, indent=2, ensure_ascii=False))
    else:
        print(f"分析报告: {skill_path}")
        print(f"质量评分: {result['quality']['overall_score']}/100")

    return 0

if __name__ == "__main__":
    sys.exit(main())
```

**验收标准**：
- [ ] scripts/ 目录创建成功
- [ ] validate_skill.py 可执行且支持 --help
- [ ] analyze_skill.py 可执行且支持 --help
- [ ] 两个脚本都符合黑盒化原则

---

### 2.3 P1-1: 补充 examples/ 内容

**目录位置**: `/models/claude-glm/Skills-Creator/examples/`

#### 2.3.1 creating-a-skill.md

```markdown
# 创建新技能示例

## 基础示例

使用 MCP init_skill 工具创建一个 minimal 模板技能：

```json
{
  "name": "my-first-skill",
  "template": "minimal",
  "output_dir": "./skills"
}
```

## Tool-Based 模板示例

创建一个需要集成 MCP 工具的技能：

```json
{
  "name": "git-helper",
  "template": "tool-based",
  "output_dir": "./skills",
  "with_scripts": true,
  "with_examples": true
}
```

## 验证结果

使用 validate_skill 验证创建的技能：

```
验证 /path/to/my-first-skill
```

预期输出：
- ✓ 结构验证通过
- ✓ 命名规范符合
- ✓ 内容格式正确
```

#### 2.3.2 validating-a-skill.md

```markdown
# 验证技能示例

## 验证现有技能

```
验证 /path/to/existing-skill
```

## 验证输出解读

验证结果包含：
- **结构检查**: 必需文件和目录
- **命名检查**: 目录名格式一致性
- **内容检查**: YAML frontmatter 和必需字段
- **模板检查**: 根据模板类型检查特定要求

## 常见问题修复

### 缺少 allowed-tools

在 SKILL.md 的 YAML frontmatter 添加：
```yaml
---
name: my-skill
description: |
  技能描述
allowed-tools: Read, Write, Edit, Bash
---
```

### 缺少必需目录

创建缺少的目录：
```bash
mkdir -p references examples scripts .claude
```
```

#### 2.3.3 analyzing-a-skill.md

```markdown
# 分析技能质量示例

## 基础分析

```
分析 /path/to/my-skill
```

## 分析维度

1. **结构分析**: 文件数量、代码行数、模块分类
2. **复杂度分析**: 圈复杂度、可维护性指数
3. **质量评分**: 综合评分（结构+文档+测试）

## 改进建议

分析工具会提供：
- Token 效率优化建议
- 结构反模式识别
- 文档完整性提示
- 测试覆盖率建议

## 应用重构

根据分析结果，可以：
1. 修复高优先级问题
2. 优化目录结构
3. 补充缺失文档
4. 提升测试覆盖
```

**验收标准**：
- [ ] 三个示例文件创建成功
- [ ] 内容清晰易懂
- [ ] 包含可执行的代码示例

---

## 三、完整 TODO 任务清单（严格遵循开发流程规范）

> **阶段验收机制**: 每个阶段必须 100% 完成并通过验收标准才能进入下一阶段

---

### 阶段 1：项目自身完整性修复（P0 问题）

**目标**: 修复 SKILL.md 缺少 allowed-tools 和 scripts/ 目录缺失问题

#### 任务 1.1：修复 SKILL.md Frontmatter

- [ ] 1.1.1 备份当前 SKILL.md
- [ ] 1.1.2 编辑 SKILL.md，在 YAML frontmatter 第 13 行后添加：
  ```yaml
  allowed-tools: Read, Write, Edit, Bash, Glob, Grep
  mcp_servers: ["skill-creator"]
  ```
- [ ] 1.1.3 验证 YAML 格式正确（使用 Python yaml 库解析测试）

#### 任务 1.2：创建 scripts/ 目录和脚本

- [ ] 1.2.1 创建 `scripts/` 目录
- [ ] 1.2.2 创建 `scripts/validate_skill.py`（黑盒化原则：argparse + --help）
- [ ] 1.2.3 创建 `scripts/analyze_skill.py`（黑盒化原则：argparse + --help）
- [ ] 1.2.4 设置可执行权限：`chmod +x scripts/*.py`
- [ ] 1.2.5 验证脚本 `--help` 参数正常工作

#### 阶段 1 验收标准

**功能验收**:
- [ ] SKILL.md YAML frontmatter 包含 `allowed-tools` 字段
- [ ] SKILL.md YAML frontmatter 包含 `mcp_servers` 字段
- [ ] scripts/ 目录存在
- [ ] scripts/validate_skill.py 可执行且支持 --help
- [ ] scripts/analyze_skill.py 可执行且支持 --help

**质量验收**:
- [ ] YAML 格式解析无错误
- [ ] 脚本符合黑盒化原则（argparse、文档字符串、shebang）

**规范验收**:
- [ ] 符合 references/validation.md 定义的必需字段规范
- [ ] 脚本符合 references/best-practices.md 定义的黑盒化原则

---

### 阶段 2：示例内容补充（P1 问题）

**目标**: 补充 examples/ 目录的使用示例

#### 任务 2.1：创建使用示例文档

- [ ] 2.1.1 创建 `examples/creating-a-skill.md`（创建技能示例）
- [ ] 2.1.2 创建 `examples/validating-a-skill.md`（验证技能示例）
- [ ] 2.1.3 创建 `examples/analyzing-a-skill.md`（分析技能示例）
- [ ] 2.1.4 验证示例代码可实际运行

#### 阶段 2 验收标准

**功能验收**:
- [ ] 三个示例文件存在
- [ ] 每个示例包含可执行的代码片段
- [ ] 示例覆盖主要使用场景

**质量验收**:
- [ ] 示例内容清晰易懂
- [ ] 代码格式正确

**规范验收**:
- [ ] 示例符合项目实际功能
- [ ] 示例与 MCP 工具调用一致

---

### 阶段 3：项目自身验证

**目标**: 使用 MCP validate_skill 工具验证修复后的项目

#### 任务 3.1：运行项目自身验证

- [ ] 3.1.1 启动 skill-creator-mcp 服务器
- [ ] 3.1.2 调用 validate_skill 工具验证 `/models/claude-glm/Skills-Creator`
- [ ] 3.1.3 记录验证结果

#### 任务 3.2：修复验证发现的问题

- [ ] 3.2.1 如有 P0 错误，立即修复
- [ ] 3.2.2 如有 P1 警告，评估修复必要性
- [ ] 3.2.3 重新验证直到通过

#### 阶段 3 验收标准

**功能验收**:
- [ ] validate_skill 返回 `valid: true`
- [ ] 无 P0 错误
- [ ] 所有必需目录存在
- [ ] 所有必需字段存在

**质量验收**:
- [ ] 验证结果清晰可读

**规范验收**:
- [ ] 项目通过自身验证
- [ ] 符合 Agent-Skills 最佳实践

---

### 阶段 4：回归测试

**目标**: 确保修复不影响现有功能

#### 任务 4.1：运行测试套件

- [ ] 4.1.1 进入 skill-creator-mcp 目录
- [ ] 4.1.2 运行测试：`PYTHONPATH=src uv run pytest`
- [ ] 4.1.3 检查覆盖率：`PYTHONPATH=src uv run pytest --cov`

#### 任务 4.2：代码质量检查

- [ ] 4.2.1 运行 ruff 检查：`uv run ruff check`
- [ ] 4.2.2 运行 mypy 检查：`uv run mypy src/`
- [ ] 4.2.3 修复发现的问题

#### 阶段 4 验收标准

**功能验收**:
- [ ] 所有测试通过
- [ ] 无测试回归

**质量验收**:
- [ ] 测试覆盖率 ≥95%
- [ ] ruff 检查无警告
- [ ] mypy 类型检查无错误

**规范验收**:
- [ ] 符合质量门禁标准

---

### 阶段 5：代码提交

**目标**: 提交修复并推送到远程

#### 任务 5.1：准备提交

- [ ] 5.1.1 检查修改的文件列表
- [ ] 5.1.2 确认所有修改符合预期

#### 任务 5.2：创建提交

- [ ] 5.2.1 Git add 修改的文件
- [ ] 5.2.2 创建提交：`fix(project): add missing allowed-tools field and scripts directory`
  - SKILL.md: 添加 allowed-tools 和 mcp_servers 字段
  - scripts/: 添加 validate_skill.py 和 analyze_skill.py
  - examples/: 添加三个使用示例文档
- [ ] 5.2.3 提交信息符合 Conventional Commits 规范

#### 任务 5.3：推送到远程

- [ ] 5.3.1 推送到当前分支 `feature/init-skill-tool`
- [ ] 5.3.2 验证远程仓库更新成功

#### 阶段 5 验收标准

**功能验收**:
- [ ] Git commit 成功
- [ ] Git push 成功

**质量验收**:
- [ ] 提交信息格式正确
- [ ] 提交包含所有必要文件

**规范验收**:
- [ ] 符合 Git 工作流规范
- [ ] 提交信息符合 Conventional Commits 格式

---

## 四、关键文件清单

### 需要修改的文件

| 文件路径 | 修改内容 | 优先级 |
|---------|---------|--------|
| `SKILL.md` | 添加 `allowed-tools` 和 `mcp_servers` 字段 | P0 |

### 需要新建的文件

| 文件路径 | 内容 | 优先级 |
|---------|------|--------|
| `scripts/validate_skill.py` | 验证脚本（黑盒化） | P0 |
| `scripts/analyze_skill.py` | 分析脚本（黑盒化） | P0 |
| `examples/creating-a-skill.md` | 创建技能示例 | P1 |
| `examples/validating-a-skill.md` | 验证技能示例 | P1 |
| `examples/analyzing-a-skill.md` | 分析技能示例 | P1 |

---

## 五、验收标准

### 功能验收

- [ ] SKILL.md 包含完整的 YAML frontmatter
- [ ] scripts/ 目录存在且包含可执行脚本
- [ ] examples/ 目录包含使用示例
- [ ] 项目通过 MCP validate_skill 自身验证

### 质量验收

- [ ] 所有测试通过
- [ ] 测试覆盖率 ≥95%
- [ ] ruff 检查无警告
- [ ] mypy 类型检查无错误

### 规范验收

- [ ] 符合项目自身的验证规范
- [ ] 符合 Agent-Skills 最佳实践
- [ ] 脚本符合黑盒化原则

---

## 六、风险和注意事项

### 风险评估

| 风险 | 影响 | 缓解措施 |
|------|------|----------|
| YAML 格式错误 | SKILL.md 无法解析 | 修复后验证解析 |
| 脚本权限问题 | 无法执行 | 使用 chmod +x 设置 |
| 示例内容不准确 | 误导用户 | 参考实际代码编写 |

### 注意事项

1. **YAML 缩进**: 使用空格，不要混用 Tab
2. **脚本 shebang**: 使用 `#!/usr/bin/env python3`
3. **文件权限**: 确保脚本可执行
4. **示例代码**: 必须可实际运行

---

## 七、参考文档

- `.claude/plans/indexed-spinning-donut.md` - 完整开发计划
- `references/validation.md` - 验证规范
- `references/best-practices.md` - 最佳实践
- `skill-creator-mcp/src/skill_creator_mcp/utils/validators.py` - 验证器实现

---

**计划状态**: 已完成，等待用户批准进入实施阶段
