# Agent-Skills 最佳实践 - 高级技巧

## 概述

本文档涵盖 Agent-Skills 开发的高级技巧，包括 Token 优化、脚本黑盒化实践和常见反模式。

> **返回**: [核心原则](best-practices-core.md) 包含渐进式披露架构和描述写作规范。

---

## Token 优化技巧

### 1. 保持 SKILL.md 简洁

**移除内容**：
- 详细示例 → 移至 `examples/`
- API 文档 → 移至 `references/api.md`
- 配置说明 → 移至 `references/config.md`
- 历史背景 → 完全删除

**保留内容**：
- 技能概述（2-3段）
- 核心能力列表
- 快速开始（2-3个简单示例）
- 导航到引用文件

### 2. 使用引用文件

**好处**：
- 减少首次加载 Token
- 按需加载详细内容
- 便于维护和更新

**实践**：
```
SKILL.md (100行)
├── references/
│   ├── mcp-integration.md (200行)  # 需要时加载
│   ├── best-practices-core.md (206行)   # 核心原则
│   ├── best-practices-advanced.md (232行)  # 高级技巧
│   └── validation.md (220行)       # 需要时加载
```

### 3. 避免内容重复

**错误示例**：
```markdown
## 核心能力

### 文件处理
处理各种文件格式...

## 详细说明

### 文件处理
详细说明如何处理文件...（重复内容）
```

**正确示例**：
```markdown
## 核心能力

1. 技能验证 - 验证技能规范符合度

## 详细文档

- **[验证规范详解](validation.md)**
```

### 4. 控制引用深度

**错误**（深度嵌套）：
```
SKILL.md → advanced.md → internal.md → utils.md → details.md
```

**正确**（扁平引用）：
```
SKILL.md → advanced.md
SKILL.md → internal.md
SKILL.md → utils.md
```

**规则**：引用深度 ≤2层

---

## 脚本黑盒化实践

### 原则

脚本作为独立命令调用，不读取源码到上下文。

### 好处

1. **Token 高效**：不加载脚本源码
2. **执行可靠**：预测试的脚本行为一致
3. **维护简单**：脚本独立修改不影响技能

### 实现方式

**1. 提供 --help**

```python
#!/usr/bin/env python3
import argparse

def main():
    parser = argparse.ArgumentParser(description='验证 Agent-Skill 规范')
    parser.add_argument('path', help='技能目录路径')
    parser.add_argument('--template', help='模板类型')
    args = parser.parse_args()
    # ...

if __name__ == '__main__':
    main()
```

**2. 在 SKILL.md 中指引使用**

在 SKILL.md 中添加脚本使用说明：

```markdown
## 运行验证

\`\`\`bash
# 查看帮助
python scripts/validate.py --help

# 验证技能
python scripts/validate.py /path/to/skill
\`\`\`
```

注意：先运行 `--help` 了解用法，而非读取源码。

**3. 错误处理和提示**

```python
try:
    validate_skill(args.path)
except FileNotFoundError:
    print(f"错误：技能路径不存在: {args.path}")
    sys.exit(1)
except Exception as e:
    print(f"错误：{e}")
    sys.exit(1)
```

---

## 常见反模式

### 1. 文档思维

**症状**：把技能当作通用文档

**表现**：
- SKILL.md 超过500行
- 包含大量教程内容
- 详尽的历史背景和设计理念

**解决方案**：
- 移动详细内容到引用文件
- 保留概览和快速导航
- 删除非核心信息

### 2. 上下文爆炸

**症状**：激活时加载过多无关内容

**表现**：
- 首次加载超过5000 tokens
- 90%内容与当前任务无关
- 包含所有可能的边缘情况

**解决方案**：
- 实施渐进式披露
- 精简 SKILL.md
- 使用引用文件按需加载

### 3. 工具堆砌

**症状**：按工具而非能力组织

**表现**：
- 每个工具一个技能
- 技能名称直接使用工具名
- 没有工作流编排

**解决方案**：
- 按工作流能力分组
- 合并相关工具技能
- 在技能内编排工具使用

---

## 评分标准

| 评分 | 渐进式披露 | 描述质量 | 能力组织 |
|------|-----------|---------|---------|
| 优秀 (90-100) | ≤150行，三层清晰 | 三要素完整，第三人称 | 按能力，名称明确 |
| 良好 (75-89) | ≤200行，有引用 | 功能+场景 | 基本按能力 |
| 及格 (60-74) | ≤350行，引用少 | 有功能描述 | 部分按能力 |
| 不及格 (<60) | >500行 | 缺少要素 | 按工具堆砌 |

---

## 检查清单

创建技能后，逐项检查：

**结构检查**：
- [ ] SKILL.md ≤ 150行
- [ ] 引用文件 200-300行
- [ ] 引用深度 ≤2层
- [ ] 无重复内容

**描述检查**：
- [ ] 包含功能陈述
- [ ] 包含使用场景
- [ ] 包含触发词
- [ ] 使用第三人称

**组织检查**：
- [ ] 按能力而非工具组织
- [ ] 能力命名明确
- [ ] 脚本有 --help
- [ ] 无深层嵌套

---

**返回**: [核心原则](best-practices-core.md)
