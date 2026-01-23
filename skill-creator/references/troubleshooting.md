# 故障排除指南

本文档提供 Skill-Creator 使用过程中常见问题的解决方案。

> **相关文档**：
> - [回退机制说明](fallback-mechanism.md) - 客户端限制与自动降级策略
> - [MCP 集成指南](mcp-integration.md) - MCP 工具配置

---

## 目录

- [MCP Server 连接问题](#mcp-server-连接问题)
- [客户端兼容性问题](#客户端兼容性问题)
- [工具调用错误](#工具调用错误)
- [验证相关错误](#验证相关错误)
- [需求澄清问题](#需求澄清问题)

---

## MCP Server 连接问题

### 问题：MCP Server 未启动

**错误信息**：
```
Failed to connect to MCP server: skill-creator
```

**解决方案**：

1. **检查 MCP Server 是否已安装**
   ```bash
   cd skill-creator-mcp
   uv sync --dev
   ```

2. **手动启动测试**
   ```bash
   uv run python -m skill_creator_mcp
   ```

3. **检查 Claude Code 配置**
   ```json
   {
     "mcpServers": {
       "skill-creator": {
         "command": "uv",
         "args": [
           "--directory",
           "/path/to/Skills-Creator/skill-creator-mcp",
           "run",
           "python",
           "-m",
           "skill_creator_mcp"
         ]
       }
     }
   }
   ```

---

### 问题：工具列表为空

**错误信息**：
```
No tools available from skill-creator MCP server
```

**解决方案**：

1. **检查 Server 日志**
   ```bash
   # 查看启动时的输出
   uv run python -m skill_creator_mcp
   ```

2. **确认 FastMCP 版本**
   ```bash
   uv pip list | grep fastmcp
   # 需要 >= 3.0.0b1
   ```

3. **重新安装依赖**
   ```bash
   cd skill-creator-mcp
   uv sync --dev
   ```

---

## 客户端兼容性问题

### 问题：高级功能不可用

**错误信息**：
```
Advanced features not available, using fallback mode
```

**原因**：客户端不支持 FastMCP 的高级 API（`ctx.sample()` 或 `ctx.elicit()`）

**解决方案**：

1. **检查客户端能力**
   - Claude Code Desktop >= 最新版本
   - 确认支持 FastMCP 3.0+ 特性

2. **使用回退模式**
   - 回退模式会自动启用
   - 功能完全相同，只是交互方式不同

3. **了解回退机制**
   - 详见 [回退机制说明](fallback-mechanism.md)

---

### 问题：会话状态不保存

**错误信息**：
```
Session not found: req_xxx
```

**解决方案**：

1. **检查会话 ID 是否正确**
   ```python
   # 使用 status 查询会话状态
   result = await collect_requirements(
       action="status",
       session_id="your_session_id"
   )
   ```

2. **确认客户端支持状态持久化**
   - 需要支持 FastMCP Context API
   - 不支持时请记录 session_id 手动传递

3. **重新开始收集**
   ```python
   result = await collect_requirements(
       action="start",
       mode="basic"
   )
   # 保存新的 session_id
   session_id = result["session_id"]
   ```

---

## 工具调用错误

### 问题：技能路径无效

**错误信息**：
```
Invalid skill path: /path/to/skill
```

**解决方案**：

1. **检查路径是否存在**
   ```bash
   ls -la /path/to/skill
   ```

2. **确认路径包含 SKILL.md**
   ```bash
   ls /path/to/skill/SKILL.md
   ```

3. **使用绝对路径**
   ```python
   # 推荐使用绝对路径
   skill_path = "/full/path/to/skill"
   ```

---

### 问题：验证失败

**错误信息**：
```
Validation failed: Invalid skill name format
```

**解决方案**：

1. **检查命名规则**
   - 只能包含小写字母、数字和连字符
   - 必须以字母开头
   - 长度 1-64 个字符

2. **正确的命名示例**
   ```
   ✅ pdf-parser
   ✅ git-helper
   ✅ docker-manager
   ❌ PDF-Parser
   ❌ my_skill
   ❌ 123-skill
   ```

3. **修复命名**
   ```bash
   # 重命名目录
   mv My-Skill my-skill
   ```

---

## 验证相关错误

### 问题：描述格式错误

**错误信息**：
```
Invalid description format in SKILL.md
```

**解决方案**：

1. **检查 YAML Frontmatter**
   ```yaml
   ---
   name: skill-name
   description: |
     Multi-line description
     with proper formatting
   ---
   ```

2. **确认格式正确**
   - description 使用 `|` 支持多行
   - 或使用单行 `description: Single line`

3. **参考模板**
   ```bash
   # 查看模板示例
   ls skill-creator-mcp/src/skill_creator_mcp/resources/templates/
   ```

---

### 问题：结构验证失败

**错误信息**：
```
Structure validation failed: missing required files
```

**解决方案**：

1. **检查必需文件**
   ```bash
   ls -la skill/SKILL.md
   ls -la skill/examples/
   ls -la skill/references/
   ```

2. **最小结构**
   ```
   skill/
   ├── SKILL.md          # 必需
   ├── examples/         # 推荐
   │   └── creating-a-skill.md
   └── references/       # 推荐
       └── validation.md
   ```

3. **创建缺失文件**
   ```bash
   mkdir -p skill/examples skill/references
   touch skill/examples/creating-a-skill.md
   ```

---

## 需求澄清问题

### 问题：输入验证失败

**错误信息**：
```
Validation failed: Invalid input format
```

**解决方案**：

1. **检查输入格式**
   ```python
   # 基础模式：技能名称
   user_input = "pdf-parser"  # ✅ 小写字母+连字符

   # 完整模式：模板类型
   user_input = "tool-based"  # ✅ 有效选项
   ```

2. **常见验证规则**
   | 字段 | 规则 | 示例 |
   |------|------|------|
   | skill_name | 小写字母、数字、连字符 | `pdf-parser` |
   | template_type | 预定义选项 | `minimal/tool-based/workflow-based/analyzer-based` |

3. **查看帮助文本**
   ```python
   result = await collect_requirements(action="start", mode="basic")
   print(result["current_step"]["validation"]["help_text"])
   ```

---

### 问题：完整性检查失败

**错误信息**：
```
Requirements incomplete: missing critical information
```

**解决方案**：

1. **查看缺失信息**
   ```python
   result = await collect_requirements(action="complete", session_id=...)
   print("缺失信息：", result["missing_info"])
   print("建议：", result["suggestions"])
   ```

2. **补充缺失信息**
   - 使用 `next` 继续补充
   - 或选择 `progressive` 模式快速开始

3. **降低完整性要求**
   - `progressive` 模式只要求核心信息
   - 可以后续逐步完善

---

## 获取更多帮助

### 查看日志

```bash
# MCP Server 日志
uv run python -m skill_creator_mcp --log-level debug

# 测试输出
uv run pytest --log-cli-level=DEBUG -k test_name
```

### 检查版本

```bash
# Python 版本
python --version  # 需要 >= 3.10

# FastMCP 版本
uv pip list | grep fastmcp

# 项目版本
cd skill-creator-mcp
grep version pyproject.toml
```

### 相关文档

- **[回退机制说明](fallback-mechanism.md)** - 客户端限制与自动降级策略
- **[MCP 集成指南](mcp-integration.md)** - MCP 工具配置
- **[验证规范](validation.md)** - 技能验证规则
- **[API 使用示例](requirement-collection-api-examples.md)** - 实际使用场景

---

## 报告问题

如果以上解决方案无法解决您的问题：

1. **收集信息**
   - 错误信息完整内容
   - 客户端版本（Claude Code / Desktop）
   - Python 版本
   - FastMCP 版本

2. **检查已知问题**
   - 查看 [ISSUES.md](../../../ISSUES.md)
   - 查看 [CHANGELOG.md](../../../CHANGELOG.md)

3. **提交问题**
   - GitHub Issues: https://github.com/yourusername/Skills-Creator/issues
