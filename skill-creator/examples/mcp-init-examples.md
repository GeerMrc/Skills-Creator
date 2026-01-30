# init_skill 使用示例

`init_skill` 工具用于初始化新的 Agent-Skill 项目结构。

## 概述

`init_skill` 创建符合规范的技能目录结构，包含必需的文件和模板。

## 基本用法

### 创建最小技能

```python
# 创建最小模板技能
init_skill(name="git-helper", template="minimal")
```

创建的目录结构：
```
git-helper/
├── SKILL.md
└── references/
```

### 创建工具集成型技能

```python
# 创建工具集成型技能
init_skill(
    name="container-manager",
    template="tool-based",
    path="./skills"
)
```

创建的目录结构：
```
container-manager/
├── SKILL.md
├── examples/
│   └── tool-usage.md
└── references/
    ├── mcp-tools-reference.md
    └── tool-reference.md
```

### 创建工作流型技能

```python
# 创建工作流型技能
init_skill(
    name="deployment-pipeline",
    template="workflow-based"
)
```

创建的目录结构：
```
deployment-pipeline/
├── SKILL.md
├── examples/
│   └── workflow-example.md
└── references/
    └── workflow-guide.md
```

### 创建分析型技能

```python
# 创建分析型技能
init_skill(
    name="code-analyzer",
    template="analyzer-based"
)
```

创建的目录结构：
```
code-analyzer/
├── SKILL.md
├── examples/
│   └── analysis-example.md
└── references/
    └── analysis-methods.md
```

---

## 参数说明

| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `name` | string | 必填 | 技能名称（小写字母、数字、连字符） |
| `template` | string | `"minimal"` | 模板类型：minimal/tool-based/workflow-based/analyzer-based |
| `path` | string | `"."` | 输出目录路径 |
| `with_scripts` | bool | `False` | 是否包含示例脚本 |
| `with_examples` | bool | `False` | 是否包含使用示例 |

---

## 返回值

```json
{
  "success": true,
  "skill_path": "/path/to/skill",
  "message": "技能结构已创建"
}
```

---

## 模板对比

| 模板 | 目录结构 | 适用场景 |
|------|----------|----------|
| **minimal** | SKILL.md + references/ | 最小可用技能 |
| **tool-based** | + examples/ | 集成外部工具 |
| **workflow-based** | + examples/ | 多步骤工作流 |
| **analyzer-based** | + examples/ | 代码/数据分析 |

---

## 命名规范

### 有效名称

```
✅ git-helper
✅ pdf-parser
✅ data-pipeline-orchestrator
✅ v2-api-client
```

### 无效名称

```
❌ GitHelper (大写字母)
❌ git_helper (下划线)
❌ git-helper-v2-.0 (特殊字符)
❌ -git-helper (开头连字符)
```

---

## 完整工作流

### 1. 创建技能

```python
# 初始化技能
result = init_skill(
    name="pdf-helper",
    template="tool-based",
    path="./skills"
)
```

### 2. 编辑 SKILL.md

手动编辑 `skills/pdf-helper/SKILL.md` 添加技能描述。

### 3. 添加引用文件

在 `skills/pdf-helper/references/` 添加详细文档。

### 4. 验证技能

```python
# 验证创建的技能
validation = validate_skill(skill_path="./skills/pdf-helper")
print(f"Validation score: {validation['score']}/100")
```

---

## 错误处理

### 名称格式错误

```python
# 错误：包含大写字母
init_skill(name="PdfHelper")

# 错误：包含下划线
init_skill(name="pdf_helper")

# 错误：包含特殊字符
init_skill(name="pdf@helper")
```

### 模板类型错误

```python
# 错误：无效的模板类型
init_skill(name="test", template="invalid")

# 可用模板：
# - minimal
# - tool-based
# - workflow-based
# - analyzer-based
```

### 路径不存在

```python
# 错误：输出路径不存在
init_skill(name="test", path="/nonexistent/path")
```

---

## 高级用法

### 自定义输出目录

```python
# 指定输出目录
init_skill(
    name="my-skill",
    path="./my-custom-skills",
    template="tool-based"
)
```

### 包含示例和脚本

```python
# 创建完整的示例
init_skill(
    name="my-skill",
    template="tool-based",
    with_examples=True,
    with_scripts=True
)
```

### 批量创建技能

```python
skills = [
    ("skill1", "minimal"),
    ("skill2", "tool-based"),
    ("skill3", "workflow-based")
]

for name, template in skills:
    init_skill(name=name, template=template)
    print(f"Created {name}")
```

---

## 相关文档

- **[validate_skill 示例](mcp-validate-examples.md)** - 验证创建的技能
- **[MCP 集成指南](../references/mcp-tools-reference.md)** - MCP 工具配置
- **[最佳实践](../references/best-practices-core.md)** - 开发规范
