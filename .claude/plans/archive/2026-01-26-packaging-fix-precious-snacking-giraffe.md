# Agent-Skill 打包规范修复计划

**计划日期**: 2026-01-26
**计划类型**: fix (打包规范修复)
**当前分支**: develop
**预估时间**: 3-4小时

---

## 一、问题诊断

### 1.1 问题描述

用户解压的 `skill-creator-v0.3.1.zip` 包含了**整个项目目录**（392个文件，16MB），而非标准的 Agent-Skill 技能包。

**实际解压结构**（错误）:
```
skill-creator-v0.3.1/
├── skill-creator/          # Agent-Skill
├── skill-creator-mcp/      # MCP Server (不应包含)
├── docs/                   # 项目文档 (不应包含)
├── README.md, CHANGELOG.md # 项目根文档 (不应包含)
└── .claude/plans/archive/  # 大量历史归档 (不应包含)
```

**标准 Agent-Skill 格式**（正确）:
```
skill-creator-v0.3.1.zip
└── skill-creator/
    ├── SKILL.md          # 必需
    ├── examples/         # 可选
    ├── references/       # 可选
    └── scripts/          # 可选
```

### 1.2 根本原因

1. **排除模式不完整**：`packagers.py` 缺少对开发文件和项目级文档的排除
2. **打包路径错误**：使用了项目根目录而非 `skill-creator/` 目录
3. **缺少专用函数**：没有区分 Agent-Skill 打包和项目打包

---

## 二、修复方案

### 2.1 代码修复

**文件**: `skill-creator-mcp/src/skill_creator_mcp/utils/packagers.py`

**修改内容**:
1. 扩展排除模式列表（第156-171行）
2. 新增 `_is_project_root()` 函数
3. 新增 `_collect_agent_skill_files()` 函数
4. 新增 `package_agent_skill()` 专用函数

**新增排除模式**:
```python
# 版本控制
".git", ".gitignore", ".gitattributes", ".github"

# 开发环境
".vscode", ".idea", "*.swp", "*.swo"

# 计划和归档（关键！）
".claude/plans/archive", ".claude/archive"

# 项目级文档（不属于单个 Agent-Skill）
"README.md", "CHANGELOG.md", "CONTRIBUTING.md", "LICENSE"

# MCP Server 代码（应该单独打包）
"*_mcp", "skill-creator-mcp"

# 测试和覆盖率
"tests", ".pytest_cache", "htmlcov", ".coverage", "coverage.xml"

# Python 构建产物
"__pycache__", "*.pyc", "*.pyo", "*.pyd", ".mypy_cache", ".ruff_cache"
"*.egg-info", "dist", "build", ".DS_Store"

# 虚拟环境
".venv", "venv", "env", ".env"

# 日志和临时文件
"*.log", "*.tmp", "*.bak"
```

### 2.2 文档更新

**文件1**: `CLAUDE.md` - 新增第七章 "Agent-Skill 打包规范"

**文件2**: `skill-creator/references/packaging.md` - 新建完整打包指南（200-300行）

**文件3**: `skill-creator/SKILL.md` - 更新工具列表，添加 `package_agent_skill`

**文件4**: `CHANGELOG.md` - 添加 v0.3.2 变更记录

### 2.3 测试用例

**文件**: `skill-creator-mcp/tests/test_tools/test_package_skill.py`

**新增测试**（6-8个）:
- `test_package_agent_skill_excludes_project_files`
- `test_package_agent_skill_excludes_archive`
- `test_package_agent_skill_standard_structure`
- `test_package_agent_skill_with_version`
- `test_package_agent_skill_package_name_format`
- `test_package_agent_skill_installation_manifest`

### 2.4 重新打包

**使用修复后的工具**:
```python
package_agent_skill(
    skill_path="/models/claude-glm/Skills-Creator/skill-creator",
    output_dir="/models/claude-glm/Skills-Creator",
    version="0.3.1",
    package_format="zip",
    include_tests=False,
    validate_before_package=True
)
```

**预期结果**:
- 包名: `skill-creator-v0.3.1.zip`
- 文件数: 40-50个（vs 当前392个）
- 包大小: <500KB（vs 当前16MB）
- 不包含: `.claude/plans/archive/`, `skill-creator-mcp/`, 项目根文档

---

## 三、任务清单

| 任务ID | 任务描述 | 优先级 | 预计时间 | 依赖 |
|--------|----------|--------|----------|------|
| 20260126-01 | 更新 packagers.py 排除模式列表 | P0 | 30分钟 | - |
| 20260126-02 | 新增 package_agent_skill() 函数 | P0 | 1小时 | 01 |
| 20260126-03 | 添加测试用例（6-8个） | P0 | 1小时 | 02 |
| 20260126-04 | 更新 server.py 工具注册 | P0 | 10分钟 | 02 |
| 20260126-05 | 更新 CLAUDE.md 添加第七章 | P1 | 30分钟 | 02 |
| 20260126-06 | 创建 packaging.md 引用文档 | P1 | 30分钟 | 02 |
| 20260126-07 | 更新 SKILL.md 和 CHANGELOG | P1 | 15分钟 | 05,06 |
| 20260126-08 | 重新打包 v0.3.1 | P0 | 10分钟 | 01-04 |
| 20260126-09 | 验证包结构和质量 | P0 | 30分钟 | 08 |

---

## 四、验收标准

### 4.1 功能验收

- [ ] `package_agent_skill()` 函数正常工作
- [ ] 排除模式完整覆盖所有开发文件
- [ ] 版本号正确添加到包名
- [ ] 包结构符合 Agent-Skill 规范

### 4.2 包结构验收

**必须包含**:
- [ ] `SKILL.md`
- [ ] `examples/`
- [ ] `references/`
- [ ] `scripts/`

**必须排除**:
- [ ] `.claude/plans/archive/`
- [ ] `README.md`, `CHANGELOG.md`（项目级）
- [ ] `skill-creator-mcp/`
- [ ] `tests/`
- [ ] `.git/`, `.gitignore`

**质量指标**:
- [ ] 文件数量 < 50个
- [ ] 包大小 < 500KB
- [ ] 包名格式: `skill-creator-v0.3.1.zip`

### 4.3 质量验收

- [ ] 单元测试覆盖率 ≥99%
- [ ] `ruff check` 0 错误
- [ ] `mypy` 0 错误
- [ ] 文档链接有效

---

## 五、关键文件路径

### 5.1 需要修改的文件

| 文件 | 操作 | 说明 |
|------|------|------|
| `skill-creator-mcp/src/skill_creator_mcp/utils/packagers.py` | 修改 | 扩展排除模式，新增函数 |
| `skill-creator-mcp/src/skill_creator_mcp/server.py` | 修改 | 注册新工具 |
| `skill-creator-mcp/tests/test_tools/test_package_skill.py` | 修改 | 新增测试用例 |
| `CLAUDE.md` | 修改 | 新增第七章 |
| `skill-creator/references/packaging.md` | 新建 | 打包指南 |
| `skill-creator/SKILL.md` | 修改 | 更新工具列表 |
| `CHANGELOG.md` | 修改 | 添加 v0.3.2 记录 |

### 5.2 绝对路径

```
/models/claude-glm/Skills-Creator/
├── skill-creator-mcp/src/skill_creator_mcp/
│   ├── utils/packagers.py
│   └── server.py
├── skill-creator-mcp/tests/test_tools/test_package_skill.py
├── skill-creator/
│   ├── SKILL.md
│   └── references/packaging.md (新建)
├── CLAUDE.md
└── CHANGELOG.md
```

---

## 六、验证步骤

### 6.1 打包验证

```bash
# 列出包内容（前30行）
unzip -l skill-creator-v0.3.1.zip | head -30

# 统计文件数量
unzip -l skill-creator-v0.3.1.zip | tail -1

# 检查包大小
ls -lh skill-creator-v0.3.1.zip
```

### 6.2 排除项验证

```bash
# 解压到临时目录
unzip -q skill-creator-v0.3.1.zip -d /tmp/test-skill
cd /tmp/test-skill/skill-creator

# 验证排除项
[ -d ".claude/plans/archive" ] && echo "❌" || echo "✅ 归档已排除"
[ -f "README.md" ] && echo "❌" || echo "✅ README 已排除"
[ -d "../skill-creator-mcp" ] && echo "❌" || echo "✅ MCP 已排除"

# 验证包含项
[ -f "SKILL.md" ] && echo "✅" || echo "❌ 缺少 SKILL.md"
[ -d "examples" ] && echo "✅" || echo "❌ 缺少 examples/"
```

### 6.3 功能测试

```bash
# 运行验证脚本
python /tmp/test-skill/skill-creator/scripts/validate_skill.py /tmp/test-skill/skill-creator

# 运行完整测试套件
cd skill-creator-mcp
uv run pytest --cov
```

---

## 七、Git 提交计划

### 7.1 Commit 信息

```
fix(packaging): 修复 Agent-Skill 打包规范

问题：
- skill-creator-v0.3.1.zip 包含整个项目（392个文件，16MB）
- 应该只包含 skill-creator/ 目录内容（标准 Agent-Skill）

修复：
- 更新 packagers.py 排除模式列表
- 新增 package_agent_skill() 专用函数
- 支持版本号和标准化包名
- 添加完整测试用例（6-8个）

文档更新：
- CLAUDE.md 新增第七章打包规范
- 新增 references/packaging.md 完整指南
- 更新 SKILL.md 工具列表

测试：所有测试通过，覆盖率 99%
```

### 7.2 发布更新

1. 替换 GitHub Releases 中的 `v0.3.1.zip`（如果需要）
2. 创建新的 Git tag: `v0.3.2`
3. 更新下载链接

---

## 八、风险和缓解

| 风险 | 概率 | 影响 | 缓解措施 |
|------|------|------|----------|
| 排除模式不完整 | 低 | 中 | 完善测试用例覆盖各种场景 |
| 破坏现有功能 | 低 | 高 | 保持 package_skill() 不变，新增函数 |
| 包大小仍然过大 | 中 | 低 | 优化文件大小，移除冗余内容 |

---

**文档版本**: v1.0
**创建日期**: 2026-01-26
**状态**: planning
**下一步**: 等待用户批准后开始执行
