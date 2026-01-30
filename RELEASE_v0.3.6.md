# v0.3.6 发布说明

## 已完成 ✅

### 1. Git Tag 推送
```bash
git push origin v0.3.6  # ✅ 已成功
```

### 2. GitHub Release 创建
```
https://github.com/GeerMrc/Skills-Creator/releases/tag/v0.3.6  # ✅ 已创建
```

已附加产物：
- `skill-creator-v0.3.6.zip` (68KB, 35个文件)
- `skill_creator_mcp-0.3.6-py3-none-any.whl` (86KB)

### 3. 发布产物

| 产物 | 路径 | 大小 |
|------|------|------|
| Agent-Skill | `skill-creator-v0.3.6.zip` | 68KB |
| MCP Wheel | `skill-creator-mcp/dist/skill_creator_mcp-0.3.6-py3-none-any.whl` | 86KB |
| MCP Source | `skill-creator-mcp/dist/skill_creator_mcp-0.3.6.tar.gz` | 442KB |

---

## 待完成 ⏳

### PyPI 发布

**方法1: 使用 UV (推荐)**
```bash
cd skill-creator-mcp

# 设置 PyPI API Token
export UV_PUBLISH_TOKEN="pypi-xxx"

# 发布到 PyPI
uv publish dist/skill_creator_mcp-0.3.6-py3-none-any.whl

# 或同时发布两个文件
uv publish dist/
```

**方法2: 使用 Twine**
```bash
cd skill-creator-mcp

# 安装 twine
pip install twine

# 发布到 PyPI
twine upload dist/skill_creator_mcp-0.3.6-py3-none-any.whl

# 或同时发布两个文件
twine upload dist/*
```

**获取 PyPI API Token:**
1. 访问 https://pypi.org/manage/account/token/
2. 创建新的 API token
3. 设置环境变量或直接使用 token

---

## 用户安装说明

### 从 GitHub Release 安装

**Agent-Skill:**
```bash
# 下载
wget https://github.com/GeerMrc/Skills-Creator/releases/download/v0.3.6/skill-creator-v0.3.6.zip

# 解压到 Claude Desktop skills 目录
unzip skill-creator-v0.3.6.zip -d ~/.config/claude/skills/
```

**MCP Server:**
```bash
# 直接从 wheel 安装
pip install https://github.com/GeerMrc/Skills-Creator/releases/download/v0.3.6/skill_creator_mcp-0.3.6-py3-none-any.whl
```

### 从 PyPI 安装 (发布后)

```bash
pip install skill-creator-mcp==0.3.6
```

---

## 质量指标

- **测试覆盖率**: 97% (553个测试用例)
- **工具数量**: 12个 (4技能+7需求+1打包)
- **代码质量**: ruff 0错误, mypy 0错误, bandit 0高危

---

## 创建时间
2026-01-30
