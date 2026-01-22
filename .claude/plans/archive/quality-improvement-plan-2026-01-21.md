# Skill-Creator 开发计划 - 质量提升与下一阶段推进

> **计划版本**: v1.0
> **制定日期**: 2026-01-21
> **当前分支**: feature/init-skill-tool
> **状态**: 待批准

---

## 一、当前状态审核

### 1.1 已完成工作

| Commit | 内容 | 状态 |
|--------|------|------|
| e0a2945 | feat(project): initialize skill-creator-mcp project framework | ✅ |
| bad964f | feat(tools): implement init_skill tool | ✅ |
| d50c980 | feat(tools): add validate_skill tool | ✅ |
| 76aead3 | feat(tools): add analyze_skill tool | ✅ |
| 6bd819d | test: 补充测试覆盖率到 95% 并修复类型检查 | ⚠️ 需验证 |

### 1.2 质量门禁检查结果

| 指标 | 要求 | 当前 | 状态 |
|------|------|------|------|
| 测试覆盖率 | ≥95% | **84%** | ❌ 不达标 |
| 代码规范 | 无警告 | 通过 | ✅ |
| 类型检查 | 无错误 | 通过 | ✅ |

### 1.3 工具实现状态

| 工具 | 实现状态 | 测试状态 |
|------|----------|----------|
| init_skill | ✅ 完整 | ✅ 11 个测试通过 |
| validate_skill | ✅ 完整 | ✅ 19 个测试通过 |
| analyze_skill | ✅ 完整 | ✅ 15 个测试通过 |

### 1.4 问题分析

**测试覆盖率 84% 低于要求 95% 的原因：**
- `server.py` 覆盖率仅 50%（第 174-247, 279-350 行未覆盖）
- `analyzers.py` 覆盖率 89%（部分边界情况未覆盖）
- `validators.py` 覆盖率 97%（第 217-220 行未覆盖）
- `__main__.py` 未实现（0% 覆盖率）

---

## 二、完整 TODO 任务清单

### 阶段 1：提升测试覆盖率至 95%

#### 1.1 补充 validate_skill 测试用例
- [ ] 1.1.1 测试错误分支：目录不存在
- [ ] 1.1.2 测试错误分支：路径不是目录
- [ ] 1.1.3 测试异常处理：内部错误捕获
- [ ] 1.1.4 测试 check_structure=False 分支
- [ ] 1.1.5 测试 check_content=False 分支
- [ ] 1.1.6 测试 validators.py 第 217-220 行（模板特定验证边界情况）

#### 1.2 补充 analyze_skill 测试用例
- [ ] 1.2.1 测试 analyze_structure=False 分支
- [ ] 1.2.2 测试 analyze_complexity=False 分支
- [ ] 1.2.3 测试 analyze_quality=False 分支
- [ ] 1.2.4 测试 analyzers.py 未覆盖行（33, 40-41, 69, 100, 111-112, 141, 143, 145, 283-284, 331, 334, 338, 341, 363, 365）
- [ ] 1.2.5 测试异常处理：内部错误捕获

#### 1.3 修复集成测试
- [ ] 1.3.1 修复 test_integration/ 导入问题
- [ ] 1.3.2 修复 test_mcp/ 导入问题
- [ ] 1.3.3 确保集成测试可运行

#### 1.4 验证覆盖率
- [ ] 1.4.1 运行 `PYTHONPATH=src uv run pytest --cov`
- [ ] 1.4.2 确认覆盖率 ≥95%

---

### 阶段 2：实现 __main__.py 入口点

#### 2.1 命令行入口实现
- [ ] 2.1.1 实现基本 CLI 入口点
- [ ] 2.1.2 添加 --version 参数
- [ ] 2.1.3 添加 --help 参数
- [ ] 2.1.4 编写 __main__.py 测试

---

### 阶段 3：代码质量提升

#### 3.1 更新 ruff 配置
- [ ] 3.1.1 修复 pyproject.toml 中的 deprecated 警告
  - 将 'ignore' 更新为 'lint.ignore'
  - 将 'select' 更新为 'lint.select'
  - 将 'isort' 更新为 'lint.isort'

#### 3.2 代码审查
- [ ] 3.2.1 审查 server.py 代码质量
- [ ] 3.2.2 审查 utils/ 目录代码质量
- [ ] 3.2.3 审查 models/ 目录代码质量

---

### 阶段 4：文档补充

#### 4.1 README 更新
- [ ] 4.1.1 添加完整的功能说明
- [ ] 4.1.2 添加安装配置指南
- [ ] 4.1.3 添加使用示例

#### 4.2 API 文档
- [ ] 4.2.1 为所有 MCP 工具添加详细文档
- [ ] 4.2.2 为所有辅助函数添加 docstring

---

### 阶段 5：下一阶段规划

#### 5.1 确定下一阶段工作
- [ ] 5.1.1 审视开发计划文档中的 7 个阶段
- [ ] 5.1.2 确定当前处于哪个阶段
- [ ] 5.1.3 制定下一阶段具体任务

#### 5.2 分支策略
- [ ] 5.2.1 决定是否创建新分支或继续当前分支
- [ ] 5.2.2 决定是否合并到 develop

---

## 三、关键文件路径

### 需要修改的文件

| 文件 | 修改类型 | 优先级 |
|------|----------|--------|
| `tests/test_tools/test_validate_skill.py` | 补充测试用例 | P0 |
| `tests/test_tools/test_analyze_skill.py` | 补充测试用例 | P0 |
| `tests/test_integration/test_*.py` | 修复导入问题 | P1 |
| `tests/test_mcp/test_*.py` | 修复导入问题 | P1 |
| `src/skill_creator_mcp/__main__.py` | 实现入口点 | P1 |
| `pyproject.toml` | 更新 ruff 配置 | P2 |
| `README.md` | 补充文档 | P2 |

---

## 四、验收标准

### 质量验收
- [ ] 测试覆盖率 ≥95%
- [ ] ruff 检查无警告（包括 deprecated 警告）
- [ ] mypy 类型检查无错误
- [ ] 所有测试通过（94+ 测试用例）

### 功能验收
- [ ] validate_skill 所有代码分支被测试覆盖
- [ ] analyze_skill 所有代码分支被测试覆盖
- [ ] __main__.py 实现并测试
- [ ] 集成测试可以运行

---

## 五、开发规范要点提醒

### 5.1 提交前检查清单
```bash
# 运行测试
PYTHONPATH=src uv run pytest --cov

# 代码规范检查
uv run ruff check .

# 类型检查
uv run mypy src/
```

### 5.2 Commit 规范
```
<type>(<scope>): <subject>

类型: feat | fix | test | refactor | docs | chore
```

### 5.3 质量门禁
| 指标 | 标准 |
|------|------|
| 测试覆盖率 | ≥95% |
| 代码规范 | 无警告 |
| 类型检查 | 无错误 |

---

**计划状态**: 待用户批准
**预计完成时间**: 1-2 天
