# 贡献指南

感谢您对 Skills-Creator 项目的关注！

---

## 目录

- [行为准则](#行为准则)
- [如何贡献](#如何贡献)
- [开发流程](#开发流程)
- [代码规范](#代码规范)
- [提交规范](#提交规范)
- [问题报告](#问题报告)

---

## 行为准则

- 尊重所有贡献者
- 使用友好和包容的语言
- 专注于项目改进

---

## 如何贡献

### 报告问题

1. 检查 [ISSUES.md](../ISSUES.md) 确认问题未被报告
2. 使用 GitHub Issues 提供详细信息
3. 包含复现步骤和环境信息

### 提交代码

1. Fork 项目仓库
2. 创建功能分支
3. 提交变更
4. 创建 Pull Request

---

## 开发流程

### 1. 设置开发环境

```bash
# 克隆仓库
git clone https://github.com/yourusername/Skills-Creator.git
cd Skills-Creator

# 安装依赖
cd skill-creator-mcp
uv sync --dev

# 运行测试
uv run pytest --cov
```

### 2. 创建功能分支

```bash
git checkout develop
git pull origin develop
git checkout -b feature/your-feature-name
```

### 3. 开发和测试

- 遵循 [代码规范](#代码规范)
- 编写或更新测试
- 确保测试覆盖率不降低
- 运行 `uv run pytest --cov`

### 4. 提交变更

```bash
git add .
git commit -m "feat(scope): description"
git push -u origin feature/your-feature-name
```

### 5. 创建 Pull Request

- 在 GitHub 上创建 PR
- 填写 PR 模板
- 等待 Code Review

---

## 代码规范

### Python 代码

- 遵循 PEP 8
- 使用类型注解
- 添加文档字符串

```python
async def example_function(param: str) -> dict[str, Any]:
    """
    函数简短描述.

    Args:
        param: 参数描述

    Returns:
        返回值描述
    """
    pass
```

### 代码质量检查

```bash
# 格式化代码
uv run ruff format .

# 检查代码
uv run ruff check .

# 类型检查
uv run mypy src/
```

---

## 提交规范

使用 [Conventional Commits](https://www.conventionalcommits.org/) 格式：

```
<type>(<scope>): <subject>

<body>

<footer>
```

### Type 类型

- `feat`: 新功能
- `fix`: Bug 修复
- `docs`: 文档更新
- `style`: 代码格式
- `refactor`: 重构
- `test`: 测试相关
- `chore`: 构建过程或辅助工具变动

### 示例

```
feat(tools): add package_skill tool

Implement packaging functionality for Agent-Skills.
Supports zip, tar.gz, and tar.bz2 formats.

Closes #123
```

---

## 测试要求

### 测试覆盖率

- 新代码必须有测试覆盖
- 整体覆盖率不低于 94%
- 运行 `uv run pytest --cov` 验证

### 测试文件位置

```
skill-creator-mcp/tests/
├── test_tools/
├── test_resources/
└── test_prompts/
```

---

## 文档要求

### 代码文档

- 所有公共函数必须有文档字符串
- 使用 Google 风格或 NumPy 风格

### 项目文档

- 更新相关文档（README.md、CLAUDE.md）
- 添加新功能的示例
- 更新 CHANGELOG.md

---

## 问题报告

### 问题模板

创建 Issue 时包含：

1. **问题描述**：清晰简洁的问题描述
2. **复现步骤**：如何复现问题
3. **预期行为**：期望的正确行为
4. **实际行为**：实际观察到的行为
5. **环境信息**：
   - Python 版本
   - 操作系统
   - 项目版本

---

## Pull Request 审查

### 审查清单

- [ ] 代码符合规范
- [ ] 测试通过
- [ ] 文档已更新
- [ ] CHANGELOG 已更新
- [ ] 没有合并冲突

### 审查流程

1. 自动化检查通过
2. 至少一名维护者审查
3. 解决所有审查意见
4. 使用 Squash and Merge 合并

---

## 获取帮助

- 查看 [故障排除指南](../skill-creator/references/troubleshooting.md)
- 阅读现有代码和测试
- 在 GitHub Issues 中提问

---

**感谢您的贡献！**
