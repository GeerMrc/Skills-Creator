# MCP 使用示例

本文档提供 skill-creator-mcp 工具和资源的详细使用示例。

## 工具示例导航

| 工具 | 说明 | 预估时间 |
|------|------|----------|
| **[init_skill](mcp-init-examples.md)** | 初始化新技能 | 5 分钟 |
| **[validate_skill](mcp-validate-examples.md)** | 验证规范符合度 | 3 分钟 |
| **[analyze_skill](mcp-analyze-examples.md)** | 分析代码质量 | 2 分钟 |
| **[refactor_skill](mcp-refactor-examples.md)** | 生成重构建议 | 2 分钟 |
| **[package_skill](mcp-package-examples.md)** | 打包分发 | 1 分钟 |

---

## 快速开始

### 创建新技能

```python
# 1. 初始化技能
init_skill(name="my-skill", template="tool-based")

# 2. 验证规范
validate_skill(skill_path="./my-skill")

# 3. 分析质量
analyze_skill(skill_path="./my-skill")

# 4. 获取建议
refactor_skill(skill_path="./my-skill")

# 5. 打包分发
package_skill(skill_path="./my-skill", format="zip")
```

---

## 标准开发流程

```python
# 1. 初始化技能结构
init_skill(name="my-skill", template="tool-based")

# 2. 编写 SKILL.md 和引用文件
# （手动完成）

# 3. 验证规范
validation = validate_skill(skill_path="./my-skill")
print(f"Validation score: {validation['score']}/100")

# 4. 分析质量
analysis = analyze_skill(skill_path="./my-skill")
print(f"Quality score: {analysis['quality']['overall_score']}")

# 5. 获取重构建议
refactor = refactor_skill(skill_path="./my-skill")
for suggestion in refactor['suggestions']:
    print(f"[{suggestion['priority']}] {suggestion['issue']}")

# 6. 修改并重新验证
# （根据建议修改代码后重新验证）
```

---

## Claude Code 对话中使用

```python
# 场景 1: 创建新技能
# 你：创建一个名为 pdf-helper 的技能
# Claude：[调用 init_skill 工具]
# 已创建 pdf-helper 技能结构...

# 场景 2: 验证技能
# 你：验证这个技能
# Claude：[调用 validate_skill 工具]
# 验证报告：命名规范 ✓，描述完整 ✓，结构良好 ✓

# 场景 3: 分析质量
# 你：分析 /path/to/skill 的质量
# Claude：[调用 analyze_skill 工具]
# 分析完成：Token 效率 85%，结构评分 90/100

# 场景 4: 获取重构建议
# 你：给我重构建议，关注 token 效率
# Claude：[调用 refactor_skill 工具]
# 建议清单：
# - P0: SKILL.md 过长，建议精简到 150 行以内
# - P1: 引用文件过长，建议拆分为多个小文件
```

---

## 批量操作示例

### 批量验证多个技能

```python
skills = ["skill1", "skill2", "skill3"]
results = {}

for skill in skills:
    result = validate_skill(skill_path=f"./skills/{skill}")
    results[skill] = result['score']
    print(f"{skill}: {result['score']}/100")

# 输出汇总
for skill, score in results.items():
    status = "✓" if score >= 80 else "⚠" if score >= 60 else "✗"
    print(f"{status} {skill}: {score}/100")
```

### 并发操作（异步）

```python
import asyncio

async def validate_all_skills():
    """并发验证多个技能."""
    skills = ["skill1", "skill2", "skill3"]

    results = await asyncio.gather(
        validate_skill(skill_path=f"./skills/{s}")
        for s in skills
    )

    for skill, result in zip(skills, results):
        print(f"{skill}: {result['score']}/100")

# 运行
await validate_all_skills()
```

---

## 错误处理示例

### 处理常见错误

```python
# 错误 1: 技能路径不存在
try:
    validate_skill(skill_path="/nonexistent/path")
except Exception as e:
    if "not found" in str(e):
        print("错误：技能路径不存在")
        print("解决：请确认路径正确")
    else:
        print(f"错误：{e}")

# 错误 2: 模板类型无效
try:
    init_skill(name="test", template="invalid-type")
except Exception as e:
    if "Unknown template" in str(e):
        print("错误：模板类型无效")
        print("可用模板：minimal, tool-based, workflow-based, analyzer-based")

# 错误 3: MCP Server 未连接
try:
    init_skill(name="test")
except Exception as e:
    if "not found" in str(e):
        print("错误：MCP Server 未连接")
        print("解决：检查 Claude Code 配置")
```

---

## 高级用法示例

### 自定义模板开发

```python
# 1. 初始化基础模板
init_skill(name="my-skill", template="tool-based")

# 2. 修改 SKILL.md（手动编辑）

# 3. 添加自定义引用文件
import pathlib
skill_dir = pathlib.Path("./my-skill")
(skill_dir / "references" / "custom-api.md").write_text("""
# Custom API Integration

本文档说明如何集成 Custom API。
...（详细内容）
""")

# 4. 验证修改后的技能
validation = validate_skill(skill_path="./my-skill")
print(f"Validation passed: {validation['valid']}")
```

### 缓存优化

```python
# 首次读取资源
best_practices = await session.read_resource("skill://best-practices")
cached_content = best_practices.contents[0].text

# 后续使用缓存
print(cached_content)  # 不会再次请求 MCP Server
```

---

## 资源访问示例

### 读取技能模板

```python
# 通过 MCP Client 读取模板
resource = await session.read_resource("http://skills/schema/templates/minimal")
template_content = resource.contents[0].text

# 读取其他模板
tool_template = await session.read_resource("http://skills/schema/templates/tool-based")
workflow_template = await session.read_resource("http://skills/schema/templates/workflow-based")
analyzer_template = await session.read_resource("http://skills/schema/templates/analyzer-based")
```

### 读取最佳实践

```python
# 读取最佳实践指南
resource = await session.read_resource("http://skills/schema/best-practices")
practices = resource.contents[0].text
```

### 读取验证规则

```python
# 读取验证规则
resource = await session.read_resource("http://skills/schema/validation-rules")
rules = resource.contents[0].text
```

---

## Prompt 使用示例

### create-skill Prompt

```python
# 获取创建技能的 Prompt 模板
prompt = await session.get_prompt("create-skill", arguments={
    "name": "pdf-helper",
    "template": "tool-based"
})

# 不同模板类型
prompt = await session.get_prompt("create-skill", arguments={
    "name": "git-workflow",
    "template": "workflow-based"
})
```

### validate-skill Prompt

```python
# 获取验证技能的 Prompt 模板
prompt = await session.get_prompt("validate-skill", arguments={
    "skill_path": "/path/to/skill"
})

# 指定模板类型
prompt = await session.get_prompt("validate-skill", arguments={
    "skill_path": "/path/to/skill",
    "template": "tool-based"
})
```

### refactor-skill Prompt

```python
# 获取重构建议的 Prompt 模板
prompt = await session.get_prompt("refactor-skill", arguments={
    "skill_path": "/path/to/skill"
})

# 指定关注领域
prompt = await session.get_prompt("refactor-skill", arguments={
    "skill_path": "/path/to/skill",
    "focus": ["structure", "token-efficiency"]
})
```

---

## 相关文档

- **[MCP 集成指南](../references/mcp-tools-reference.md)** - 配置和基础使用
- **[最佳实践 - 核心](../references/best-practices-core.md)** - 开发规范
- **[最佳实践 - 高级](../references/best-practices-advanced.md)** - Token 优化和高级技巧
- **[验证规范](../references/validation.md)** - 验证规则
