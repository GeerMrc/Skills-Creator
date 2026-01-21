# Agent-Skills 验证规范

## 概述

本文档定义 Agent-Skills 的验证规则和检查清单。使用这些规则确保技能符合官方最佳实践。

## 验证维度

### 1. 命名验证

#### 技能名称规范

**格式**：kebab-case

**规则**：
```regex
^[a-z][a-z0-9-]*[a-z0-9]$
```

**要求**：
- 只包含小写字母、数字、连字符
- 必须以字母开头
- 不能以连字符结尾
- 不能有连续连字符
- 长度：3-50字符

**正确示例**：
```
✓ git-workflow
✓ pdf-processor
✓ container-management
✓ data-analyzer-v2
```

**错误示例**：
```
✓ Git-Workflow           # 大写字母
✓ pdf_processor          # 下划线
✓ -container-manager     # 连字符开头
✓ container--manager     # 连续连字符
✓ container-manager-     # 连字符结尾
✓ ab                     # 太短
```

#### 能力命名

**推荐模式**：
- **动名词形式**：`processing-pdfs`、`analyzing-data`、`managing-containers`
- **名词短语**：`pdf-processing`、`data-analysis`、`container-management`

**避免使用**：
- `helper` - 太模糊
- `utils` - 太通用
- `tools` - 按工具组织的信号
- `manager` - 除非真正管理资源

### 2. 描述验证

#### YAML Frontmatter 检查

**必需字段**：
```yaml
---
name: skill-name
description: |
  功能描述
---
```

#### 描述三要素

**1. 功能陈述**（必须）
- 使用第三人称
- 描述能力而非工具
- 1句话，约20字符

**示例**：
```yaml
# 正确
description: |
  PDF 文档处理能力。提取文本、填充表单、合并文档。

# 错误
description: |
  我可以帮助您处理 PDF 文档。  # 第一人称
  这是一个 PDF 处理工具。      # 不明确
```

**2. 使用场景**（必须）
- 2-4个具体场景
- 每个场景1行
- 以"何时使用"开头

**示例**：
```yaml
description: |
  ...

  何时使用：
  - 需要从 PDF 提取文本或图片
  - 填充 PDF 表单模板
  - 合并多个 PDF 文件
```

**3. 触发词**（必须）
- 3-6个关键词
- 用户可能使用的词汇
- 以"触发词"开头

**示例**：
```yaml
description: |
  ...

  触发词：PDF、提取、表单、合并、水印
```

#### 描述长度

| 指标 | 最小 | 推荐 | 最大 |
|------|------|------|------|
| 字符数 | 50 | 150-300 | 1024 |

### 3. 结构验证

#### SKILL.md 行数

**标准**：
- 优秀：≤150行
- 良好：≤200行
- 及格：≤350行
- 不及格：>500行

#### 必需章节

**SKILL.md 必须包含**：
```markdown
## 技能概述
## 核心能力
## 快速开始
## 详细文档（或导航到引用文件）
```

#### 目录结构

**最小结构**：
```
skill-name/
├── SKILL.md
```

**标准结构**：
```
skill-name/
├── SKILL.md              # ≤150行
├── references/           # 详细文档
│   ├── guide.md         # 200-300行
│   └── examples.md      # 200-300行
└── scripts/             # 黑盒脚本
    └── validate.py
```

#### 引用文件规范

**大小**：每个文件200-300行

**深度**：≤2层

```
✓ 正确：扁平引用
SKILL.md → guide.md
SKILL.md → examples.md

✗ 错误：深层嵌套
SKILL.md → guide.md → internal.md → utils.md
```

**独立性**：引用文件不应相互引用

### 4. 内容质量验证

#### 第三人称检查

**正确**：
```yaml
description: |
  Docker 容器管理能力。创建、启动、停止容器。
```

**错误**：
```yaml
description: |
  我可以管理容器。           # ❌ 第一人称
  使用这个工具管理容器。     # ❌ 第二人称
```

#### 按能力组织检查

**正确**：
```
✓ container-management     # 容器管理能力
✓ cloud-deployment         # 云部署能力
```

**错误**：
```
✗ docker-skill            # 按工具命名
✗ kubectl-helper          # 按工具命名
```

#### 脚本黑盒化检查

**每个脚本必须**：
- 有 `--help` 选项
- 独立可执行
- 有清晰的错误提示

**示例**：
```python
#!/usr/bin/env python3
import argparse

def main():
    parser = argparse.ArgumentParser(description='验证 Agent-Skill')
    parser.add_argument('path', help='技能路径')
    args = parser.parse_args()
    # ...

if __name__ == '__main__':
    main()
```

### 5. Token 效率验证

#### 首次加载检查

**优秀**：≤1000 tokens
**良好**：≤2000 tokens
**及格**：≤3500 tokens
**不及格**：>5000 tokens

#### 内容密度检查

计算方法：
```
内容密度 = (核心内容 tokens) / (总 tokens)

优秀：≥70%
良好：≥50%
及格：≥30%
```

#### 重复内容检查

自动检查：
- 相同段落出现多次
- 引用文件内容重复
- 示例代码重复

## 验证清单

### 完整清单

使用以下清单全面验证技能：

**命名检查**：
- [ ] 名称使用 kebab-case
- [ ] 名称以字母开头
- [ ] 名称 3-50 字符
- [ ] 无连续连字符
- [ ] 按能力而非工具命名

**描述检查**：
- [ ] 包含功能陈述
- [ ] 使用第三人称
- [ ] 包含使用场景
- [ ] 包含触发词
- [ ] 字符数 50-1024

**结构检查**：
- [ ] SKILL.md ≤150行
- [ ] 包含必需章节
- [ ] 引用文件 200-300行
- [ ] 引用深度 ≤2层
- [ ] 引用文件独立

**内容检查**：
- [ ] 使用第三人称
- [ ] 按能力组织
- [ ] 脚本有 --help
- [ ] 无重复内容

**效率检查**：
- [ ] 首次加载 ≤2000 tokens
- [ ] 内容密度 ≥50%
- [ ] 无明显重复

### 快速检查

5分钟快速验证：

1. 检查 YAML frontmatter（30秒）
2. 数 SKILL.md 行数（10秒）
3. 验证描述三要素（30秒）
4. 检查目录结构（30秒）
5. 运行 validate_skill 工具（3分钟）

## 评分系统

### 综合评分

| 维度 | 权重 | 评分标准 |
|------|------|---------|
| 命名质量 | 15% | 优秀=100，良好=75，及格=50 |
| 描述质量 | 25% | 三要素完整=100，缺一=60 |
| 结构规范 | 30% | ≤150行=100，≤200行=80 |
| 内容质量 | 20% | 符合规范=100 |
| Token 效率 | 10% | ≥70%=100，≥50%=70 |

### 等级划分

**优秀 (90-100分)**：
- SKILL.md ≤150行
- 描述三要素完整
- 按能力组织
- Token 效率 ≥70%

**良好 (75-89分)**：
- SKILL.md ≤200行
- 描述包含功能和场景
- 基本按能力组织
- Token 效率 ≥50%

**及格 (60-74分)**：
- SKILL.md ≤350行
- 描述有功能陈述
- 部分按能力组织
- Token 效率 ≥30%

**不及格 (<60分)**：
- SKILL.md >500行
- 描述缺少要素
- 按工具组织
- Token 效率 <30%

## 常见问题

### Q1: SKILL.md 多少行合适？

**A**: 推荐 ≤150行。如果内容较多：
1. 移动详细示例到 `examples/`
2. 移动 API 文档到 `references/api.md`
3. 移动配置说明到 `references/config.md`

### Q2: 描述应该多长？

**A**:
- 最小：50字符（避免太短）
- 推荐：150-300字符（平衡信息量和效率）
- 最大：1024字符（MCP 协议限制）

### Q3: 如何判断按能力还是按工具？

**A**: 问自己：
- 这个技能解决什么工作流问题？（能力）
- 还是提供什么工具？（工具）

如果答案是工作流，按能力组织。

### Q4: 引用文件可以互相引用吗？

**A**: 不推荐。原因：
1. Claude 可能部分读取
2. 深层嵌套导致信息不完整
3. 增加导航复杂度

最佳实践：所有引用文件直接从 SKILL.md 链接。

### Q5: 如何测量 Token 效率？

**A**: 使用 analyze_skill 工具：
```python
analyze_skill(skill_path="/path/to/skill")
```

返回包含：
- 首次加载 tokens
- 内容密度百分比
- 优化建议

## 自动化验证

### 使用 validate_skill 工具

```bash
# 基本验证
python scripts/validate_skill.py /path/to/skill

# 带模板验证
python scripts/validate_skill.py /path/to/skill --template tool-based

# 输出详细报告
python scripts/validate_skill.py /path/to/skill --verbose
```

### 集成到 CI/CD

```yaml
# .github/workflows/skill-validation.yml
name: Skill Validation

on: [push, pull_request]

jobs:
  validate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Validate Skills
        run: |
          for skill in skills/*; do
            python scripts/validate_skill.py "$skill"
          done
```

## 参考资源

- **[MCP 集成指南](mcp-integration.md)** - MCP 工具和资源使用
- **[最佳实践](best-practices.md)** - 渐进式披露和开发规范
- **[SKILL.md](../SKILL.md)** - 技能入口点
