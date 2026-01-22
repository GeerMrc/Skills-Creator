# 创建新技能示例

## 基础示例

使用 MCP init_skill 工具创建一个 minimal 模板技能：

```json
{
  "name": "my-first-skill",
  "template": "minimal",
  "output_dir": "./skills"
}
```

## Tool-Based 模板示例

创建一个需要集成 MCP 工具的技能：

```json
{
  "name": "git-helper",
  "template": "tool-based",
  "output_dir": "./skills",
  "with_scripts": true,
  "with_examples": true
}
```

## 验证结果

使用 validate_skill 验证创建的技能：

```
验证 /path/to/my-first-skill
```

预期输出：
- ✓ 结构验证通过
- ✓ 命名规范符合
- ✓ 内容格式正确
