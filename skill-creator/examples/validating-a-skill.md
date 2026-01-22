# 验证技能示例

## 验证现有技能

```
验证 /path/to/existing-skill
```

## 验证输出解读

验证结果包含：
- **结构检查**: 必需文件和目录
- **命名检查**: 目录名格式一致性
- **内容检查**: YAML frontmatter 和必需字段
- **模板检查**: 根据模板类型检查特定要求

## 常见问题修复

### 缺少 allowed-tools

在 SKILL.md 的 YAML frontmatter 添加：

```yaml
---
name: my-skill
description: |
  技能描述
allowed-tools: Read, Write, Edit, Bash
---
```

### 缺少必需目录

创建缺少的目录：

```bash
mkdir -p references examples scripts .claude
```
