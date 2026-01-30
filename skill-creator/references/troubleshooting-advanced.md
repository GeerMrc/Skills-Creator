# 高级调试指南

> **相关文档**：[故障排除指南](troubleshooting.md) - 常见问题快速解决

本文档提供深度问题排查方法。

---

## 日志分析

### 启用调试日志

```bash
# MCP Server 调试模式
uv run python -m skill_creator_mcp --log-level debug

# 测试调试输出
uv run pytest --log-cli-level=DEBUG -k test_name
```

### 日志级别说明

| 级别 | 用途 | 示例 |
|------|------|------|
| DEBUG | 详细执行信息 | 函数调用、变量值 |
| INFO | 一般运行信息 | 工具调用、会话创建 |
| WARNING | 警告信息 | 回退模式启用 |
| ERROR | 错误信息 | 验证失败、异常 |

### 常见日志模式

**成功初始化**：
```
INFO:skill_creator_mcp.server:Registered tool: init_skill
INFO:skill_creator_mcp.server:Registered tool: validate_skill
INFO:skill_creator_mcp.server:MCP Server started successfully
```

**回退模式启用**：
```
WARNING:skill_creator_mcp.server:Client capabilities limited
WARNING:skill_creator_mcp.server:Fallback mode enabled
```

**会话创建**：
```
INFO:skill_creator_mcp.server:Session created: req_20260124_123456
INFO:skill_creator_mcp.server:Mode: basic, Steps: 5
```

---

## 性能诊断

### 工具响应时间

```python
import time

start = time.time()
result = await validate_skill(skill_path="/path/to/skill")
elapsed = time.time() - start
print(f"验证耗时: {elapsed:.2f}秒")
```

### LLM Sampling 性能

```python
start = time.time()
result = await ctx.sample(messages="Test")
elapsed = time.time() - start
print(f"LLM 响应时间: {elapsed:.2f}秒")
```

### 内存使用监控

```bash
ps aux | grep python
pip install memory_profiler
python -m memory_profiler script.py
```

---

## MCP 协议调试

### 检查工具注册

```python
import skill_creator_mcp
server = skill_creator_mcp.server

print("可用工具:")
for tool in server._mcp_tools:
    print(f"  - {tool.name}")
```

### 测试工具调用

```python
from skill_creator_mcp.server import validate_skill

result = await validate_skill(skill_path="/path/to/skill")
print(result)
```

### 资源访问测试

```python
from skill_creator_mcp.server import _get_template_resource

template = await _get_template_resource("minimal")
print(template[:100])
```

---

## 会话状态调试

### 查看会话内容

```python
import json

result = await get_requirement_session_tool(session_id="req_xxx")
print(json.dumps(result, indent=2))
```

### 手动恢复会话

```python
saved_session_id = "req_20260124_123456"
session = await get_requirement_session_tool(session_id=saved_session_id)

result = await update_requirement_answer_tool(
    session_id=saved_session_id,
    question_key="skill_name",
    answer="answer"
)
```

---

## 常见错误模式

### Pydantic 序列化错误

```
pydantic.seriation.SerializableTypeError: Unable to serialize unknown type
```

**解决方案**：
```python
return {"success": True, "data": str(data)}
```

### Session State 丢失

```
KeyError: 'session_state'
```

**解决方案**：
```python
session_id = result["session_id"]
```

### LLM Sampling 超时

```
TimeoutError: LLM sampling timed out after 30 seconds
```

**解决方案**：
```python
fallback_questions = ["备用问题1", "备用问题2"]
```

---

## 调试检查清单

### 基础检查
- [ ] Python 版本 >= 3.10
- [ ] FastMCP 版本 >= 3.0.0b1
- [ ] uv sync 已执行
- [ ] MCP Server 可启动

### 连接检查
- [ ] MCP 配置正确
- [ ] 工具列表非空
- [ ] 可以调用工具

### 功能检查
- [ ] init_skill 正常
- [ ] validate_skill 正常
- [ ] 需求收集工具正常

---

## 获取帮助

### 收集调试信息

```bash
cat <<'EOF' > debug-report.txt
=== 环境信息 ===
Python: $(python --version)
FastMCP: $(uv pip list | grep fastmcp)
系统: $(uname -a)

=== 错误信息 ===
$(cat error.log)

=== 配置文件 ===
$(cat ~/.config/claude/mcp_config.json)
EOF
```

### 提交问题时附上

1. 完整错误堆栈
2. 调试日志（--log-level debug）
3. 最小复现示例
4. 环境信息

---

**相关文档**：
- **[故障排除指南](troubleshooting.md)** - 常见问题快速解决
- **[MCP 集成指南](mcp-tools-reference.md)** - MCP 配置详情
