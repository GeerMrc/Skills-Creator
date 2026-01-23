# Agent-Skills 验证实施指南

本文档是 [验证规范](validation.md) 的配套指南，提供等级划分标准、常见问题解答和自动化验证集成示例。

## 等级划分

基于综合评分的等级划分标准：

### 优秀 (90-100分)

**特征**：
- SKILL.md ≤150行
- 描述三要素完整
- 按能力组织
- Token 效率 ≥70%

**示例**：
```
pdf-processor/           # ✓ 命名清晰
├── SKILL.md (120行)    # ✓ 简洁
├── references/         # ✓ 结构化引用
│   ├── api.md (250行)
│   └── examples.md (280行)
└── scripts/
    └── validate.py     # ✓ 黑盒脚本
```

### 良好 (75-89分)

**特征**：
- SKILL.md ≤200行
- 描述包含功能和场景
- 基本按能力组织
- Token 效率 ≥50%

**示例**：
```
git-helper/              # △ 命名较模糊
├── SKILL.md (180行)    # ✓ 可接受
├── references/
│   ├── guide.md (300行)
│   └── workflows.md (320行)  # △ 稍长
```

### 及格 (60-74分)

**特征**：
- SKILL.md ≤350行
- 描述有功能陈述
- 部分按能力组织
- Token 效率 ≥30%

**改进方向**：
1. 精简 SKILL.md 内容
2. 补充描述的使用场景
3. 重新组织按能力分类
4. 移动详细内容到引用文件

### 不及格 (<60分)

**特征**：
- SKILL.md >500行
- 描述缺少要素
- 按工具组织
- Token 效率 <30%

**必须改进**：
1. 完全重写 SKILL.md
2. 修正 YAML frontmatter
3. 重新设计技能结构
4. 实施渐进式披露

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

通过 MCP Server 调用验证工具：

```python
from skill_creator_mcp import validate_skill

# 基本验证
result = validate_skill(
    skill_path="/path/to/skill",
    template_type="tool-based"
)

# 输出报告
print(result.report)
```

或使用命令行：

```bash
# 基本验证
python scripts/validate_skill.py /path/to/skill

# 带模板验证
python scripts/validate_skill.py /path/to/skill --template tool-based

# 输出详细报告
python scripts/validate_skill.py /path/to/skill --verbose
```

### 集成到 CI/CD

#### GitHub Actions 示例

```yaml
# .github/workflows/skill-validation.yml
name: Skill Validation

on:
  push:
    paths:
      - 'skills/**'
      - 'SKILL.md'
  pull_request:
    paths:
      - 'skills/**'
      - 'SKILL.md'

jobs:
  validate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.12'

      - name: Install dependencies
        run: |
          pip install skill-creator-mcp

      - name: Validate Skills
        run: |
          # 验证主技能
          python scripts/validate_skill.py . --template workflow-based

          # 验证子技能（如果存在）
          for skill in skills/*/; do
            echo "Validating $skill"
            python scripts/validate_skill.py "$skill"
          done

      - name: Upload validation report
        if: always()
        uses: actions/upload-artifact@v4
        with:
          name: validation-report
          path: |
            validation-report.json
            validation-report.html
```

#### GitLab CI 示例

```yaml
# .gitlab-ci.yml
stages:
  - validate

validate_skill:
  stage: validate
  image: python:3.12
  script:
    - pip install skill-creator-mcp
    - python scripts/validate_skill.py . --template workflow-based
  artifacts:
    paths:
      - validation-report.json
      - validation-report.html
    when: always
  only:
    - merge_requests
    - main
```

#### Pre-commit Hook

```bash
# .git/hooks/pre-commit
#!/bin/bash

echo "Running skill validation..."

# 验证主技能
python scripts/validate_skill.py . || exit 1

# 验证子技能
for skill in skills/*/; do
    python scripts/validate_skill.py "$skill" || exit 1
done

echo "Validation passed!"
```

使用方式：
```bash
# 安装 hook
cp .git/hooks/pre-commit.example .git/hooks/pre-commit
chmod +x .git/hooks/pre-commit
```

### 本地开发工作流

```bash
# 1. 开发技能
vim SKILL.md

# 2. 快速验证（5秒）
python scripts/validate_skill.py . --fast

# 3. 详细分析（30秒）
python scripts/validate_skill.py . --verbose

# 4. 生成报告
python scripts/validate_skill.py . --report > report.html

# 5. 提交前检查
pre-commit run
```

## 评分计算

### 自动计算脚本

```python
def calculate_skill_score(skill_path: str) -> dict:
    """计算技能综合评分."""
    from skill_creator_mcp import validate_skill, analyze_skill

    # 验证技能
    validation = validate_skill(skill_path)

    # 分析技能
    analysis = analyze_skill(skill_path)

    # 计算各维度得分
    naming_score = _calculate_naming_score(validation)
    description_score = _calculate_description_score(validation)
    structure_score = _calculate_structure_score(validation)
    content_score = _calculate_content_score(validation)
    token_score = _calculate_token_score(analysis)

    # 综合评分（加权）
    overall_score = (
        naming_score * 0.15 +
        description_score * 0.25 +
        structure_score * 0.30 +
        content_score * 0.20 +
        token_score * 0.10
    )

    return {
        "overall": overall_score,
        "naming": naming_score,
        "description": description_score,
        "structure": structure_score,
        "content": content_score,
        "token_efficiency": token_score,
    }
```

### 等级判断

```python
def get_grade(score: float) -> str:
    """根据分数返回等级."""
    if score >= 90:
        return "优秀"
    elif score >= 75:
        return "良好"
    elif score >= 60:
        return "及格"
    else:
        return "不及格"
```

## 相关资源

- **[验证规范](validation.md)** - 核心验证规则和检查清单
- **[最佳实践 - 核心](best-practices-core.md)** - 渐进式披露架构和设计原则
- **[MCP 集成指南](mcp-integration.md)** - MCP 工具使用和资源访问
