# Skills-Creator 迁移指南

> **版本**: v0.2.0
> **发布日期**: 2026-01-22
> **变更类型**: 目录结构重构

---

## 概述

从 v0.1.0 开始，Skills-Creator 项目进行了目录结构重构，以提供更清晰的职责边界和更好的开发体验。

**核心变更**: Agent-Skill 相关代码统一到 `skill-creator/` 目录。

---

## 迁移影响

### 受影响的用户

如果您是以下用户，本迁移对您有影响：

- ✅ 直接引用项目根目录 `SKILL.md` 的用户
- ✅ 直接访问 `examples/`, `references/`, `scripts/` 目录的用户
- ✅ 基于旧目录结构编写自定义脚本的用户

### 不受影响的用户

如果您是以下用户，本迁移对您**无影响**：

- ✅ 通过 MCP Server 使用工具的用户
- ✅ 仅使用 MCP 工具和资源的用户
- ✅ 通过 Claude Code Desktop 自动加载技能的用户

---

## 目录结构变更

### 变更前（v0.1.0）

```
/models/claude-glm/Skills-Creator/
├── SKILL.md                    # Agent-Skill 入口（根目录）
├── examples/                   # 示例文档（根目录）
├── references/                 # 引用文档（根目录）
├── scripts/                    # 脚本（根目录）
└── skill-creator-mcp/          # MCP Server
```

### 变更后（v0.2.0）

```
/models/claude-glm/Skills-Creator/
├── skill-creator/              # Agent-Skill 代码统一目录
│   ├── SKILL.md                # Agent-Skill 入口
│   ├── examples/               # 使用示例
│   ├── scripts/                # 辅助脚本
│   └── references/             # 引用文档
└── skill-creator-mcp/          # MCP Server（不变）
```

---

## 迁移步骤

### 方式 1: Claude Code Desktop 用户（推荐）

如果您使用 Claude Code Desktop，技能会自动加载，无需任何操作：

```bash
# 技能路径示例（如需手动配置）
~/.claude/skills/skill-creator/
```

### 方式 2: MCP Server 用户

如果您使用 MCP Server，无需任何操作。MCP Server 配置和用法保持不变：

```json
{
  "mcpServers": {
    "skill-creator": {
      "command": "uv",
      "args": ["--directory", "/path/to/Skills-Creator/skill-creator-mcp", "run", "python", "-m", "skill_creator_mcp"]
    }
  }
}
```

### 方式 3: 直接引用 SKILL.md 的用户

如果您直接引用 `SKILL.md`，请更新路径：

**更新前**:
```bash
# 旧路径
ls /models/claude-glm/Skills-Creator/SKILL.md
```

**更新后**:
```bash
# 新路径
ls /models/claude-glm/Skills-Creator/skill-creator/SKILL.md
```

### 方式 4: 访问示例/引用文档的用户

如果您直接访问 `examples/` 或 `references/`，请更新路径：

**更新前**:
```bash
# 旧路径
cat /models/claude-glm/Skills-Creator/examples/creating-a-skill.md
cat /models/claude-glm/Skills-Creator/references/best-practices.md
```

**更新后**:
```bash
# 新路径
cat /models/claude-glm/Skills-Creator/skill-creator/examples/creating-a-skill.md
cat /models/claude-glm/Skills-Creator/skill-creator/references/best-practices.md
```

---

## 兼容性说明

### 向后兼容

- ✅ MCP Server API 完全兼容
- ✅ 所有工具和资源 URI 不变
- ✅ 功能行为完全一致

### 破坏性变更

- ⚠️ 项目根目录不再包含 `SKILL.md`
- ⚠️ `examples/`, `references/`, `scripts/` 移至 `skill-creator/` 子目录

---

## 验证迁移

### 验证 MCP Server

```bash
cd /models/claude-glm/Skills-Creator/skill-creator-mcp
uv run pytest --cov
```

预期输出: `307 passed` (99% 覆盖率)

### 验证技能结构

```bash
ls -la /models/claude-glm/Skills-Creator/skill-creator/
```

预期输出:
```
drwxr-xr-x examples/
drwxr-xr-x references/
drwxr-xr-x scripts/
-rw-r--r-- SKILL.md
```

### 验证文档链接

```bash
grep -r "skill-creator/references/" skill-creator/SKILL.md
```

预期输出: 空或使用相对路径 `references/...`

---

## 常见问题

### Q1: 我的 MCP 配置需要更新吗？

**A**: 不需要。MCP Server 路径和配置保持不变。

### Q2: 我该如何引用新的文档路径？

**A**:
- 项目根目录文档 → 使用 `skill-creator/` 前缀
- skill-creator/ 内部文档 → 使用相对路径

### Q3: 旧版本是否仍然可用？

**A**: 建议迁移到新结构。旧版本可能不再接收更新。

### Q4: 迁移后功能有变化吗？

**A**: 没有任何功能变化，只是目录结构更清晰。

---

## 获取帮助

如果您在迁移过程中遇到问题：

1. 查看 [README.md](README.md) 获取项目概述
2. 查看 [CLAUDE.md](CLAUDE.md) 了解开发规范
3. 提交 Issue 到 GitHub 仓库

---

## 变更历史

| 日期 | 版本 | 变更说明 |
|------|------|----------|
| 2026-01-22 | v0.2.0 | 目录结构重构：Agent-Skill 代码统一到 `skill-creator/` |
| 2026-01-21 | v0.1.0 | 初始版本 |

---

**迁移完成后，您将继续享受所有 Skills-Creator 功能，同时拥有更清晰的项目结构。**
