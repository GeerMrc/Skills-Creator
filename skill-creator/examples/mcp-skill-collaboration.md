# MCP 与 Agent-Skill 协同示例

## 概述

本文档展示 MCP Server 和 Agent-Skill 如何协同工作，实现完整的 Agent-Skills 开发工作流。

> **相关文档**: [MCP 集成指南](../references/mcp-integration.md) | [混合架构 ADR](../../docs/adr/001-hybrid-architecture.md)

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

### 用户请求

```
"创建一个名为 'pdf-processor' 的技能，使用 tool-based 模板"
```

### Agent-Skill 编排流程

```yaml
步骤1: [Agent-Skill] 理解用户意图
  ├─ 解析技能名称: pdf-processor
  ├─ 选择模板: tool-based
  └─ 准备调用 MCP 工具

步骤2: [Agent-Skill → MCP] 调用 init_skill
  ├─ 工具: init_skill
  ├─ 参数:
  │   ├─ name: "pdf-processor"
  │   ├─ template: "tool-based"
  │   ├─ output_dir: "."
  │   ├─ with_scripts: true
  │   └─ with_examples: true
  └─ 返回: 创建结果

步骤3: [Agent-Skill] 引导用户完善内容
  ├─ "请编辑 pdf-processor/SKILL.md 完善技能描述"
  ├─ "参考最佳实践: references/best-practices-core.md"
  └─ "完成后运行验证"

步骤4: [Agent-Skill → MCP] 调用 validate_skill
  ├─ 工具: validate_skill
  ├─ 参数:
  │   ├─ skill_path: "./pdf-processor"
  │   ├─ check_structure: true
  │   └─ check_content: true
  └─ 返回: 验证报告
```

### 预期输出

```json
{
  "success": true,
  "skill_path": "./pdf-processor",
  "files_created": [
    "SKILL.md",
    "references/tool-integration.md",
    "references/usage-examples.md",
    "scripts/validate.py",
    "examples/basic-usage.md"
  ],
  "next_steps": [
    "1. 编辑 pdf-processor/SKILL.md",
    "2. 实现工具集成逻辑",
    "3. 运行验证: python scripts/validate.py"
  ]
}
```

---

## 示例 2: 技能验证工作流

### 用户请求

```
"验证 my-skill 是否符合规范"
```

### Agent-Skill 编排流程

```yaml
步骤1: [Agent-Skill] 调用 MCP 验证工具
  ├─ 工具: validate_skill
  ├─ 参数: { skill_path: "./my-skill" }
  └─ 获取验证结果

步骤2: [Agent-Skill] 分析验证结果
  ├─ 检查 errors 数组
  ├─ 检查 warnings 数组
  ├─ 检查 checks 对象
  └─ 生成可执行建议

步骤3: [Agent-Skill] 传递知识
  ├─ "发现 3 个问题:"
  ├─ "1. 描述缺少使用场景 (参考 best-practices-core.md)"
  ├─ "2. SKILL.md 超过 150 行 (考虑拆分引用文件)"
  └─ "3. 缺少验证脚本 (添加 scripts/validate.py)"
```

### 预期输出

```markdown
## 验证结果

### 状态: ❌ 验证失败 (3 个错误)

### 错误列表

1. **描述缺少使用场景**
   - 文件: SKILL.md:5
   - 建议: 添加 "何时使用" 章节，参考 [最佳实践](../references/best-practices-core.md)

2. **SKILL.md 行数超标**
   - 当前: 185 行
   - 推荐: ≤150 行
   - 建议: 移动详细示例到 `examples/`

3. **缺少验证脚本**
   - 期望: scripts/validate.py
   - 建议: 添加黑盒验证脚本

### 下一步

1. 修复上述错误
2. 重新运行验证
3. 确认所有 checks 为 true
```

---

## 示例 3: 技能分析与重构工作流

### 用户请求

```
"分析 my-skill 并给出改进建议"
```

### Agent-Skill 编排流程

```yaml
步骤1: [Agent-Skill → MCP] 分析技能
  ├─ 工具: analyze_skill
  ├─ 参数: {
  │     skill_path: "./my-skill",
  │     analyze_structure: true,
  │     analyze_complexity: true,
  │     analyze_quality: true
  │   }
  └─ 获取分析结果

步骤2: [Agent-Skill] 解读分析结果
  ├─ 结构: total_files=10, total_lines=500
  ├─ 复杂度: cyclomatic_complexity=8 (偏高)
  ├─ 质量: overall_score=65/100 (需改进)
  └─ 识别问题: token 效率低、文档不完整

步骤3: [Agent-Skill → MCP] 生成重构建议
  ├─ 工具: refactor_skill
  ├─ 参数: {
  │     skill_path: "./my-skill",
  │     focus: ["structure", "documentation"]
  │   }
  └─ 获取重构建议

步骤4: [Agent-Skill] 编排建议展示
  ├─ 按优先级排序 (P0/P1/P2)
  ├─ 添加具体代码示例
  ├─ 引用最佳实践文档
  └─ 估算工作量
```

### 预期输出

```markdown
## 分析结果

### 质量评分: 65/100 (及格)

| 维度 | 得分 | 状态 |
|------|------|------|
| 结构 | 20/30 | ⚠️ 需改进 |
| 文档 | 15/25 | ❌ 不及格 |
| 测试覆盖 | 20/20 | ✅ 优秀 |
| Token 效率 | 10/25 | ⚠️ 需改进 |

### 改进建议 (按优先级)

**P0 - 必须修复**
1. 添加使用场景到描述 (参考 [描述写作规范](../references/best-practices-core.md))
2. 移动示例到 `examples/` 目录

**P1 - 尽快修复**
3. 降低函数复杂度 (拆分 `process_file()` 函数)
4. 添加类型注解

**P2 - 有时间时修复**
5. 添加单元测试覆盖边界情况
6. 优化首次加载 token

### 工作量估算
- P0: 30 分钟
- P1: 1 小时
- P2: 2 小时
- **总计**: 3.5 小时
```

---

## 示例 4: MCP 资源访问模式

### Agent-Skill 访问 MCP 资源

```yaml
场景: 用户询问 "有哪些可用的技能模板？"

步骤1: [Agent-Skill] 决定访问 MCP 资源
  ├─ 资源: http://skills/schema/templates
  └─ 目的: 获取所有可用模板列表

步骤2: [Agent-Skill → MCP] 读取资源
  └─ 返回: 模板列表

步骤3: [Agent-Skill] 格式化展示
  └─ "有 4 种模板可选..."

用户确认选择后:

步骤4: [Agent-Skill → MCP] 读取特定模板
  ├─ 资源: http://skills/schema/templates/tool-based
  └─ 返回: tool-based 模板内容

步骤5: [Agent-Skill] 使用模板内容
  └─ 调用 init_skill 工具
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
# MCP Server 返回结构化错误
{
  "success": False,
  "error": "目录不存在",
  "error_type": "path_error",
  "suggestion": "检查路径是否正确"
}

# Agent-Skill 解读并引导用户
"❌ 验证失败: 目录不存在
💡 建议: 检查路径拼写，或使用绝对路径
📖 参考: [验证规范](../references/validation.md)"
```

### 3. 渐进式披露

```yaml
第一次交互:
  - 返回: 简洁摘要 + 可选详情链接

用户要求详情时:
  - 访问: MCP 资源或引用文件
  - 返回: 深度内容
```

---

## 调试协同问题

### 常见问题排查

**问题 1**: MCP 工具未找到
```bash
# 检查 MCP Server 连接
npx @modelcontextprotocol/inspector ./skill-creator-mcp/src/skill_creator_mcp

# 检查配置文件
cat ~/.config/Claude/claude_desktop_config.json
```

**问题 2**: Agent-Skill 未激活
```yaml
# 检查 SKILL.md 触发词
触发词:
  - 技能创建    # ✅ 名词形式
  - 创建技能    # ❌ 动词形式（不一致）
```

**问题 3**: 协同流程卡住
```bash
# 查看 MCP Server 日志
# 在 Claude Code 中检查日志输出

# 测试单个工具
python -m skill_creator_mcp  # STDIO 模式测试
```

---

## 相关文档

- **[MCP 集成指南](../references/mcp-integration.md)** - 工具和资源详细说明
- **[最佳实践 - 核心原则](../references/best-practices-core.md)** - 架构设计原则
- **[混合架构 ADR](../../docs/adr/001-hybrid-architecture.md)** - 架构决策记录
