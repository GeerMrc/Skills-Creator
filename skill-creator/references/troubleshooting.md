# 故障排除指南

> **架构说明**：需求收集基于 **7个原子化MCP工具 + Agent-Skill工作流编排** 的混合架构（符合ADR 001）。本文档提供使用过程中常见问题的解决方案，实际使用通过skill-creator Agent-Skill调用。

本文档提供 Skill-Creator 使用过程中常见问题的解决方案。

> **相关文档**：
> - [回退机制说明](../../skill-creator-mcp/docs/client-compatibility.md) - 客户端限制与自动降级策略
> - [MCP 集成指南](mcp-integration.md) - MCP 工具配置
> - [高级调试指南](troubleshooting-advanced.md) - 深度问题排查

---

## MCP Server 连接问题

### 问题：MCP Server 未启动

**解决方案**：

1. 检查 MCP Server 是否已安装
   ```bash
   cd skill-creator-mcp
   uv sync --dev
   ```

2. 手动启动测试
   ```bash
   uv run python -m skill_creator_mcp
   ```

3. 检查配置文件中路径正确

---

### 问题：工具列表为空

**解决方案**：

1. 确认 FastMCP 版本 >= 3.0.0b1
   ```bash
   uv pip list | grep fastmcp
   ```

2. 重新安装依赖
   ```bash
   cd skill-creator-mcp && uv sync --dev
   ```

---

## 客户端兼容性问题

### 问题：高级功能不可用

**原因**：客户端不支持所需的交互 API

**解决方案**：
- 使用 skill-creator Agent-Skill 进行工作流编排
- Agent-Skill 层负责处理用户交互和状态管理
- 详见 [MCP集成指南](mcp-integration.md)

---

### 问题：会话状态不保存

**解决方案**：

1. 检查会话 ID 是否正确
   ```python
   result = await get_requirement_session_tool(session_id="your_session_id")
   ```

2. 确认客户端支持状态持久化
   - 不支持时请记录 session_id 手动传递

3. 重新开始收集
   ```python
   session = await create_requirement_session_tool(mode="basic")
   session_id = session["session_id"]
   ```

---

## 工具调用错误

### 问题：技能路径无效

**解决方案**：

1. 检查路径是否存在
   ```bash
   ls -la /path/to/skill
   ```

2. 确认路径包含 SKILL.md
   ```bash
   ls /path/to/skill/SKILL.md
   ```

3. 使用绝对路径

---

### 问题：验证失败

**命名规则**：
- 只能包含小写字母、数字和连字符
- 必须以字母开头
- 长度 1-64 个字符

**正确示例**：
```
✅ pdf-parser
✅ git-helper
❌ PDF-Parser
❌ my_skill
```

---

## 验证相关错误

### 问题：描述格式错误

**YAML Frontmatter 格式**：
```yaml
---
name: skill-name
description: |
  Multi-line description
  with proper formatting
---
```

---

### 问题：结构验证失败

**最小结构**：
```
skill/
├── SKILL.md          # 必需
├── examples/         # 推荐
└── references/       # 推荐
```

**创建缺失文件**：
```bash
mkdir -p skill/examples skill/references
touch skill/examples/creating-a-skill.md
```

---

## 需求澄清问题

### 问题：输入验证失败

**常见验证规则**：
| 字段 | 规则 | 示例 |
|------|------|------|
| skill_name | 小写字母、数字、连字符 | `pdf-parser` |
| template_type | 预定义选项 | `minimal/tool-based/workflow-based/analyzer-based` |

---

### 问题：完整性检查失败

**解决方案**：

1. 查看缺失信息
   ```python
   result = await check_requirement_completeness_tool(answers=...)
   print("缺失信息：", result["missing_items"])
   ```

2. 使用 `update_requirement_answer_tool` 继续补充，或选择 `progressive` 模式快速开始

---

## 快速诊断

### 检查版本

```bash
python --version  # 需要 >= 3.10
uv pip list | grep fastmcp
cd skill-creator-mcp && grep version pyproject.toml
```

---

## 相关文档

- **[回退机制说明](../../skill-creator-mcp/docs/client-compatibility.md)** - 客户端限制与自动降级策略
- **[MCP 集成指南](mcp-integration.md)** - MCP 工具配置
- **[验证规范](validation.md)** - 技能验证规则
- **[高级调试指南](troubleshooting-advanced.md)** - 深度问题排查和日志分析

---

## 报告问题

如果以上解决方案无法解决您的问题：

1. 收集信息：错误信息、客户端版本、Python 版本、FastMCP 版本
2. 检查已知问题：访问 [GitHub Issues](https://github.com/your-repo/issues) 和 [CHANGELOG](https://github.com/your-repo/blob/main/CHANGELOG.md)
3. 提交问题：GitHub Issues
