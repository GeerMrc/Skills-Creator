# 配置文档一致性全面审核计划

> **计划ID**: audit-config-consistency
> **创建日期**: 2026-01-26
> **计划类型**: 文档审核
> **优先级**: P0

---

## 一、任务概述

### 1.1 目标

对项目中所有配置相关文档进行全面审核，确保：
1. `command` 字段使用正确（python vs uv vs uvx）
2. 安装方式与配置方式对应关系准确
3. 全局安装 vs 源码开发配置区分清晰
4. 交叉引用链接有效
5. 为推送到远端仓库做好准备

### 1.2 审核范围

| 文档 | 审核内容 |
|------|----------|
| `README.md` | 安装步骤、配置方式 |
| `skill-creator-mcp/README.md` | 快速开始、配置章节 |
| `skill-creator-mcp/docs/claude-code-config.md` | Claude Code CLI 配置 |
| `skill-creator-mcp/docs/installation.md` | 安装指南 |
| `skill-creator-mcp/docs/mcp-config-guide.md` | MCP 配置说明 |
| `skill-creator-mcp/docs/ide-config.md` | IDE 集成配置 |
| `skill-creator-mcp/docs/configuration.md` | 配置参数参考 |
| `skill-creator-mcp/docs/README.md` | 文档索引 |
| `skill-creator-mcp/docs/troubleshooting.md` | 故障排除 |
| `skill-creator-mcp/docs/sse-guide.md` | SSE 配置 |

---

## 二、审核要点

### 2.1 command 字段使用规范

| 安装方式 | 正确 command | 错误配置 |
|----------|-------------|----------|
| `pip install` | `python` | `uv` / `uvx` |
| `uv pip install` | `python` | `uv` / `uvx` |
| `git clone` + `uv sync` | `uv` (with run) | `python` (直接) |
| `uv tool install` | `uvx` | ⚠️ 本包不支持 |

### 2.2 安装-配置对应关系检查

```
安装方式 → 配置方式映射:

pip install → python -m skill_creator_mcp
uv pip install → python -m skill_creator_mcp
源码开发 → uv --directory ... run python -m skill_creator_mcp
```

### 2.3 scope 参数一致性

| scope | 存储位置 | 适用场景 | 所有文档必须一致 |
|-------|----------|----------|-----------------|
| `project` | `.mcp.json` | 团队协作 | 团队共享、可提交VC |
| `user` | `~/.claude/settings.json` | 跨项目使用 | 个人配置、推荐 |
| `local` | `.claude/settings.json` | 临时测试 | 项目本地、不共享 |

---

## 三、审核方法

### 3.1 关键词搜索

```bash
# 搜索所有配置相关代码块
grep -rn '"command":' *.md skill-creator-mcp/**/*.md

# 搜索 claude mcp add 命令
grep -rn 'claude mcp add' *.md skill-creator-mcp/**/*.md

# 搜索 pip install 命令
grep -rn 'pip install' *.md skill-creator-mcp/**/*.md
```

### 3.2 交叉引用验证

```bash
# 检查所有内部链接
grep -rn '\[.*\](.*\.md)' *.md skill-creator-mcp/**/*.md
```

---

## 四、验收标准

### 4.1 一致性检查

- ✅ 所有文档中 `command` 字段使用正确
- ✅ 安装方式与配置方式对应关系准确
- ✅ scope 参数说明在所有文档中一致
- ✅ 全局安装和源码开发配置区分清晰

### 4.2 完整性检查

- ✅ 所有配置文档都包含 add-json 方式说明（新增）
- ✅ 所有文档都包含 command vs uv vs uvx 说明
- ✅ 交叉引用链接全部有效

### 4.3 准确性检查

- ✅ 没有错误的配置示例
- ✅ 没有过时的安装命令
- ✅ 没有矛盾的配置说明

---

## 五、任务清单

| ID | 任务 | 优先级 |
|----|------|--------|
| 1 | 读取并分析所有配置文档 | P0 |
| 2 | 搜索并验证 command 字段使用 | P0 |
| 3 | 验证安装-配置对应关系 | P0 |
| 4 | 检查 scope 参数一致性 | P1 |
| 5 | 验证交叉引用链接 | P1 |
| 6 | 修复发现的不一致问题 | P0 |
| 7 | 更新 CHANGELOG.md | P2 |
| 8 | Git 提交变更 | P2 |

---

## 六、时间估算

| 任务 | 预计时间 |
|------|----------|
| 文档读取与分析 | 30 分钟 |
| 配置一致性检查 | 45 分钟 |
| 问题修复 | 60 分钟 |
| 验证测试 | 15 分钟 |
| **总计** | **150 分钟** |

---

## 七、风险与注意事项

| 风险 | 影响 | 缓解措施 |
|------|------|----------|
| 配置示例错误 | 用户配置失败 | 仔细验证每个示例 |
| 交叉引用断链 | 文档导航失效 | 逐个验证链接 |
| 不同步更新 | 用户困惑 | 统一更新所有相关文档 |

---

## 八、后续计划

审核完成后：
1. 提交所有变更到 develop 分支
2. 创建 Pull Request 到 main
3. 合并后推送到远端仓库
4. 发布版本更新说明
