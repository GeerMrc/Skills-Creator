# MCP 与 Agent-Skill 协同示例

## 概述

本文档展示 MCP Server 和 Agent-Skill 如何协同工作，实现完整的 Agent-Skills 开发工作流。

> **相关文档**: [MCP 集成指南](../references/mcp-integration.md) | [混合架构设计](../references/architecture.md)

---

## 架构协同模式

```
┌─────────────────────────────────────────────────────────────┐
│                     Claude Code / Desktop                    │
│                                                              │
│  ┌────────────────────────────────────────────────────────┐ │
│  │          Agent-Skill (skill-creator)                   │ │
│  │  - 编排工作流程                                        │ │
│  │  - 渐进式披露知识                                      │ │
│  │  - 最佳实践指导                                        │ │
│  └────────────────────┬───────────────────────────────────┘ │
│                         │ 调用                                │
│  ┌────────────────────▼───────────────────────────────────┐ │
│  │         MCP Server (skill-creator-mcp)                 │ │
│  │  - init_skill     → 原子操作: 创建目录结构              │ │
│  │  - validate_skill → 原子操作: 验证规范                  │ │
│  │  - analyze_skill  → 原子操作: 分析质量                  │ │
│  │  - refactor_skill → 原子操作: 生成建议                  │ │
│  │  - package_skill  → 原子操作: 打包分发                  │ │
│  └─────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────┘
```

**协同原则**:
- **MCP Server**: 提供可执行的原子操作
- **Agent-Skill**: 编排工作流程，传递知识
- **接口清晰**: 工具参数和返回值结构化

---

## 示例 1: 创建新技能工作流

**用户请求**: "创建一个名为 'pdf-processor' 的技能，使用 tool-based 模板"

**协同流程**:
```yaml
步骤1: [Agent-Skill] 解析意图 → name=pdf-processor, template=tool-based
步骤2: [Agent-Skill → MCP] init_skill() → 创建目录结构
步骤3: [Agent-Skill] 引导用户 → 编辑 SKILL.md，参考最佳实践
步骤4: [Agent-Skill → MCP] validate_skill() → 验证规范
```

**MCP 返回**:
```json
{
  "success": true,
  "skill_path": "./pdf-processor",
  "files_created": ["SKILL.md", "references/", "scripts/", "examples/"],
  "next_steps": ["编辑 SKILL.md", "实现工具逻辑", "运行验证"]
}
```

---

## 示例 2: 技能验证工作流

**用户请求**: "验证 my-skill 是否符合规范"

**协同流程**:
```yaml
步骤1: [Agent-Skill → MCP] validate_skill("./my-skill")
步骤2: [Agent-Skill] 分析 errors/warnings/checks
步骤3: [Agent-Skill] 生成可执行建议并引用最佳实践
```

**Agent-Skill 输出**:
```markdown
## 验证结果: ❌ 失败 (3 个错误)

1. 描述缺少使用场景 → 参考 [最佳实践](../references/best-practices-core.md)
2. SKILL.md 超过 150 行 → 移动详细示例到 `examples/`
3. 缺少验证脚本 → 添加 scripts/validate.py
```

---

## 示例 3: 技能分析与重构工作流

**用户请求**: "分析 my-skill 并给出改进建议"

**协同流程**:
```yaml
步骤1: [Agent-Skill → MCP] analyze_skill() → 获取质量评分
步骤2: [Agent-Skill] 解读结果 → 识别问题
步骤3: [Agent-Skill → MCP] refactor_skill() → 获取改进建议
步骤4: [Agent-Skill] 按优先级编排建议展示
```

**Agent-Skill 输出**:
```markdown
## 分析结果: 65/100 (及格)

| 维度 | 得分 | 状态 |
|------|------|------|
| 结构 | 20/30 | ⚠️ 需改进 |
| 文档 | 15/25 | ❌ 不及格 |
| 测试覆盖 | 20/20 | ✅ 优秀 |

## 改进建议
- **P0**: 添加使用场景、移动示例到 `examples/`
- **P1**: 拆分复杂函数、添加类型注解
- **P2**: 添加边界测试、优化首次加载

**工作量估算**: 3.5 小时
```

---

## 示例 4: MCP 资源访问模式

**用户询问**: "有哪些可用的技能模板？"

**协同流程**:
```yaml
步骤1: [Agent-Skill] 访问资源 → http://skills/schema/templates
步骤2: [MCP] 返回 → 模板列表 (minimal/tool-based/workflow/analyzer)
步骤3: [Agent-Skill] 格式化展示 → "有 4 种模板可选..."
用户确认后:
步骤4: [Agent-Skill] 读取特定模板 → http://skills/schema/templates/tool-based
步骤5: [Agent-Skill → MCP] 调用 init_skill() 使用模板
```

---

## 协同最佳实践

### 1. 职责边界清晰

| 组件 | 职责 | 不做 |
|------|------|------|
| MCP Server | 执行原子操作 | 工作流编排 |
| Agent-Skill | 编排工作流 | 直接文件 I/O |

### 2. 错误处理协同

```python
# MCP 返回结构化错误 → Agent-Skill 解读并引导用户
{"success": False, "error": "目录不存在", "suggestion": "检查路径"}
→ "❌ 验证失败: 目录不存在\n💡 建议: 检查路径拼写\n📖 参考: [验证规范](../references/validation.md)"
```

### 3. 渐进式披露

```yaml
首次交互: 简洁摘要 + 详情链接
用户要求详情: 访问 MCP 资源或引用文件 → 返回深度内容
```

---

## 调试协同问题

| 问题 | 排查方法 |
|------|----------|
| MCP 工具未找到 | 检查配置文件 `~/.config/Claude/claude_desktop_config.json` |
| Agent-Skill 未激活 | 检查 SKILL.md 触发词格式一致性 |
| 协同流程卡住 | 查看 MCP Server 日志，测试单个工具 `python -m skill_creator_mcp` |

---

## 相关文档

- **[MCP 集成指南](../references/mcp-integration.md)** - 工具和资源详细说明
- **[最佳实践 - 核心原则](../references/best-practices-core.md)** - 架构设计原则
- **[混合架构设计](../references/architecture.md)** - 架构设计说明
