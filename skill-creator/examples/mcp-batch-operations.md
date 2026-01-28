# 批量操作使用示例

本文档展示如何使用 `batch_validate_skills_tool` 和 `batch_analyze_skills_tool` 进行批量技能验证和分析。

---

## 概述

批量操作工具可以并发处理多个技能，显著提高处理效率：

- **`batch_validate_skills_tool`** - 并发验证多个技能的规范符合度
- **`batch_analyze_skills_tool`** - 并发分析多个技能的代码质量

支持可配置的并发限制，默认为5个并发任务。

---

## 批量验证示例

### 场景：验证多个技能项目

假设你开发了多个技能，需要一次性验证它们是否符合规范：

```python
# 批量验证3个技能
result = await batch_validate_skills_tool(
    ctx,
    skill_paths=[
        "/path/to/git-helper",
        "/path/to/code-analyzer",
        "/path/to/doc-generator",
    ],
    check_structure=True,  # 检查目录结构
    check_content=True,     # 检查内容格式
    concurrent_limit=3,     # 并发限制为3
)

# 检查结果
if result["success"]:
    summary = result["summary"]
    print(f"总计: {summary['total']}")
    print(f"成功: {summary['successful']}")
    print(f"失败: {summary['failed']}")
    print(f"成功率: {summary['success_rate']:.1f}%")
```

### 返回结果示例

```json
{
  "success": true,
  "results": [
    {
      "skill_path": "/path/to/git-helper",
      "success": true,
      "result": {
        "valid": true,
        "skill_name": "git-helper",
        "template_type": "tool-based"
      }
    },
    {
      "skill_path": "/path/to/code-analyzer",
      "success": true,
      "result": {
        "valid": false,
        "skill_name": "code-analyzer",
        "errors": ["缺少 SKILL.md 文件"]
      }
    },
    {
      "skill_path": "/path/to/doc-generator",
      "success": true,
      "result": {
        "valid": true,
        "skill_name": "doc-generator",
        "template_type": "minimal"
      }
    }
  ],
  "summary": {
    "total": 3,
    "successful": 2,
    "failed": 1,
    "success_rate": 66.67
  }
}
```

---

## 批量分析示例

### 场景：分析多个技能的质量

```python
# 批量分析3个技能
result = await batch_analyze_skills_tool(
    ctx,
    skill_paths=[
        "/path/to/git-helper",
        "/path/to/code-analyzer",
        "/path/to/doc-generator",
    ],
    analyze_structure=True,   # 分析代码结构
    analyze_complexity=True,  # 分析代码复杂度
    analyze_quality=True,     # 分析代码质量
    concurrent_limit=5,       # 并发限制为5（默认）
)

# 检查结果
if result["success"]:
    for item in result["results"]:
        if item["success"]:
            analysis = item["result"]
            print(f"{analysis['skill_name']}: 质量得分 {analysis['quality']['overall_score']}")
```

### 返回结果示例

```json
{
  "success": true,
  "results": [
    {
      "skill_path": "/path/to/git-helper",
      "success": true,
      "result": {
        "skill_name": "git-helper",
        "quality": {
          "overall_score": 85.5,
          "structure_score": 90.0,
          "documentation_score": 82.0,
          "test_coverage_score": 80.0
        },
        "complexity": {
          "cyclomatic_complexity": 3.2,
          "maintainability_index": 75.0
        },
        "suggestions": [
          "提高测试覆盖率到90%以上",
          "添加更多内联文档"
        ]
      }
    }
  ],
  "summary": {
    "total": 3,
    "successful": 3,
    "failed": 0,
    "success_rate": 100.0
  }
}
```

---

## 并发控制

### 调整并发限制

根据系统资源调整并发限制：

```python
# 高性能服务器：使用更高并发
result = await batch_validate_skills_tool(
    ctx,
    skill_paths=skill_list,
    concurrent_limit=10,  # 10个并发任务
)

# 资源受限环境：降低并发
result = await batch_validate_skills_tool(
    ctx,
    skill_paths=skill_list,
    concurrent_limit=2,   # 2个并发任务
)
```

### 并发限制建议

| 场景 | 建议并发数 | 说明 |
|------|-----------|------|
| 本地开发 | 2-3 | 避免占用过多资源 |
| CI/CD 环境 | 5-10 | 利用CI服务器资源 |
| 高性能服务器 | 10-20 | 充分利用系统资源 |
| 资源受限环境 | 1-2 | 确保稳定性 |

---

## 错误处理

### 处理失败项

```python
result = await batch_validate_skills_tool(
    ctx,
    skill_paths=skill_paths,
    concurrent_limit=5,
)

# 检查失败的技能
for item in result["results"]:
    if not item["success"]:
        print(f"验证失败: {item['skill_path']}")
        print(f"错误: {item.get('error', 'Unknown')}")

# 汇总统计
summary = result["summary"]
if summary["failed"] > 0:
    print(f"警告: {summary['failed']} 个技能验证失败")
```

### 容错处理

即使部分技能验证失败，批量操作仍会继续处理其他技能：

```python
# 即使某些技能路径无效，也会处理有效的路径
result = await batch_validate_skills_tool(
    ctx,
    skill_paths=[
        "/valid/path/skill1",
        "/invalid/path/skill2",  # 不存在
        "/valid/path/skill3",
    ],
)

# 结果：skill1 和 skill3 被处理，skill2 返回错误
```

---

## 最佳实践

### 1. 分批处理大量技能

对于超过50个技能的项目，建议分批处理：

```python
def batch_process_large_list(skill_paths, batch_size=20):
    results = []
    for i in range(0, len(skill_paths), batch_size):
        batch = skill_paths[i:i+batch_size]
        result = await batch_validate_skills_tool(
            ctx,
            skill_paths=batch,
            concurrent_limit=5,
        )
        results.extend(result["results"])
    return results
```

### 2. 结合健康检查

在批量操作前先检查系统健康状态：

```python
# 先检查系统健康
health = await health_check_tool(ctx)
if health["success"] and health["health"]["status"] == "healthy":
    # 系统健康，执行批量操作
    result = await batch_validate_skills_tool(ctx, skill_paths)
else:
    print("系统状态不佳，建议延迟批量操作")
```

### 3. 保存结果到文件

```python
import json

result = await batch_validate_skills_tool(ctx, skill_paths)

# 保存结果到文件
with open("validation_results.json", "w") as f:
    json.dump(result, f, indent=2)
```

---

## 相关文档

- [MCP 集成指南](../references/mcp-integration.md) - MCP 工具使用详解
- [健康检查示例](mcp-health-check.md) - 系统监控和性能指标
