# Git 工作流规范

> **版本**: v1.0
> **更新日期**: 2026-01-26
> **配套文档**: `dev-standards.md`

---

## 一、分支策略

### 分支结构

```
main (生产分支)
  │
develop (开发分支)
  │
  └─ feature/* (功能分支)
```

### 分支命名规范

| 前缀 | 用途 | 示例 |
|------|------|------|
| `feature/` | 新功能开发 | `feature/add-validate-tool` |
| `fix/` | Bug 修复 | `fix/naming-validation` |
| `hotfix/` | 生产环境紧急修复 | `hotfix/critical-crash` |
| `refactor/` | 代码重构 | `refactor/async-io` |
| `docs/` | 文档更新 | `docs/update-readme` |
| `test/` | 测试相关 | `test/add-coverage` |

---

## 二、分支操作规范

### 创建功能分支

```bash
# 1. 切换到develop
git checkout develop
git pull origin develop

# 2. 创建功能分支
git checkout -b feature/your-feature-name

# 3. 推送到远程
git push -u origin feature/your-feature-name
```

### 分支合并流程（通过PR）

```
1. 推送到远程
   └─ git push -u origin feature/xxx

2. 创建 Pull Request 到 develop
   └─ 在 GitHub 创建 PR

3. Code Review
   └─ 审查代码，请求修改或批准

4. Squash and Merge
   └─ 保持历史干净

5. 删除功能分支
   └─ git branch -d feature/xxx
```

---

## 三、Commit 规范

### Commit 信息格式

```
<type>(<scope>): <subject>

<body>

<footer>
```

### Type 类型

| Type | 说明 | 示例 |
|------|------|------|
| `feat` | 新功能 | 添加新工具、新功能 |
| `fix` | Bug 修复 | 修复错误、异常处理 |
| `docs` | 文档更新 | 更新 README、注释 |
| `style` | 代码格式 | 代码风格调整（不影响功能） |
| `refactor` | 重构 | 代码重构（不改变功能） |
| `test` | 测试相关 | 添加测试、修复测试 |
| `chore` | 构建过程或辅助工具变动 | 依赖更新、配置修改 |

### Scope（作用域）说明

| 规则 | 说明 | 示例 |
|------|------|------|
| **推荐使用** | 涉及特定模块或组件 | `fix(test): 修复导入错误` |
| **可省略** | 涉及多个模块或通用性 | `docs: 更新README` |
| **常用scope** | mcp/skill/test/docs/audit/plan | `feat(mcp): 添加新工具` |

### Commit 示例

```
feat(工具): 添加批量验证功能

实现批量验证多个Agent-Skill的功能。
- 支持并发控制，默认最多5个并发
- 使用Progress bar显示进度
- 返回详细的验证结果报告

测试: 新增8个测试用例，覆盖率95%

Closes #123
```

---

## 四、禁止操作

### 高危操作（严格禁止）

```bash
# ❌ 根目录递归删除（系统崩溃）
rm -rf /

# ❌ 递归删除重要目录
rm -rf ~/important-data

# ❌ 磁盘覆盖（数据丢失）
dd if=/dev/zero of=/dev/sda

# ❌ Fork 炸弹（系统崩溃）
:(){ :|:& };:
```

### Git 危险操作（禁止）

```bash
# ❌ 直接在 main 分支提交代码
git checkout main
git commit -m "xxx"  # 禁止

# ❌ 推送未经测试的代码
git push  # 未运行测试

# ❌ 强制推送到公共分支
git push -f origin main

# ❌ 合并有冲突的 PR 未解决
```

### 安全替代方案

```bash
# ✅ 使用功能分支
git checkout -b feature/xxx

# ✅ 先测试再推送
uv run pytest && git push

# ✅ 使用 --force-with-lease
git push --force-with-lease origin feature/xxx
```

---

## 五、冲突解决

### 冲突诊断

```bash
# 查看冲突
git status

# 查看差异
git diff

# 查看冲突文件
cat file.py
```

### 冲突解决流程

```bash
# 1. 拉取最新代码
git pull origin develop

# 2. 解决冲突（编辑文件）
# <<<<<<< HEAD
# 你的代码
# =======
# 别人的代码
# >>>>>>> origin/develop

# 3. 标记冲突已解决
git add .

# 4. 提交
git commit

# 5. 推送
git push
```

### 冲突解决技巧

- **保留双方代码**: `git checkout --ours` 或 `git checkout --theirs`
- **手动合并**: 编辑文件，删除冲突标记
- **使用工具**: `git mergetool`

---

## 六、多人协作工作流

### 开发者A: feature/add-mcp-tool

```bash
git checkout develop
git checkout -b feature/add-mcp-tool
# 开发 + 测试
git push -u origin feature/add-mcp-tool
# 创建 PR to develop
```

### 开发者B: feature/fix-packaging

```bash
git checkout develop
git checkout -b feature/fix-packaging
# 开发 + 测试
git push -u origin feature/fix-packaging
# 创建 PR to develop
```

### Code Review

```bash
# 审查 PR 代码
# 请求修改或批准
# Squash and Merge
```

### develop 分支

```bash
# 接受 PR 1
# 接受 PR 2
# 推送到远程
```

---

## 七、最佳实践

### 关键成功因素

- ✅ 每个功能独立分支
- ✅ 通过PR合并
- ✅ Code Review
- ✅ Squash and Merge保持历史干净

### 提交前检查清单

- [ ] 代码通过所有测试
- [ ] 代码通过质量检查
- [ ] 文档已同步更新
- [ ] 使用规范的commit信息

---

**最后更新**: 2026-01-26
