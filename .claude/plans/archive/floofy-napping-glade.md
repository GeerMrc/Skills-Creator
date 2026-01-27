# Phase 2.2: Server.py 工具模块拆分重构

> **计划日期**: 2026-01-27
> **状态**: 执行中 (6/8 任务完成)
> **目标**: 将 server.py (1,354行) 按功能拆分为独立工具模块

---

## 当前进度

### ✅ 已完成任务 (6/8)

1. **✅ 创建 tools/ 目录结构** - 完成
   - 创建 `src/skill_creator_mcp/tools/` 目录

2. **✅ 提取技能工具到 skill_tools.py** - 完成
   - 提取: init_skill, validate_skill, analyze_skill, refactor_skill
   - 文件: `tools/skill_tools.py` (192行)

3. **✅ 提取打包工具到 package_tools.py** - 完成
   - 提取: package_skill, package_agent_skill
   - 文件: `tools/package_tools.py`

4. **✅ 提取需求工具到 requirement_tools.py** - 完成
   - 提取: collect_requirements
   - 文件: `tools/requirement_tools.py`

5. **✅ 提取测试工具到 test_tools.py** - 完成
   - 提取: check_client_capabilities, test_llm_sampling, test_user_elicitation, test_conversation_loop, test_requirement_completeness
   - 文件: `tools/test_tools.py`

6. **✅ 提取批量操作到 batch_tools.py** - 完成
   - 提取: batch_validate_skills_tool, batch_analyze_skills_tool
   - 文件: `tools/batch_tools.py`

### ⏳ 待执行任务 (2/8)

7. **更新 server.py 导入和注册** - 待执行
   - 添加新工具模块导入
   - 替换 @mcp.tool() 装饰器为模块调用
   - 移除已提取的函数定义

8. **运行完整测试验证重构** - 待执行
   - `uv run pytest --cov`
   - 确保所有测试通过
   - 验证覆盖率≥99%

---

## 任务7详细计划

### 7.1 更新 server.py 导入

**需要添加的导入**:
```python
from .tools.batch_tools import (
    batch_analyze_skills_tool,
    batch_validate_skills_tool,
)
from .tools.package_tools import (
    package_agent_skill,
    package_skill,
)
from .tools.requirement_tools import collect_requirements
from .tools.skill_tools import (
    analyze_skill,
    init_skill,
    refactor_skill,
    validate_skill,
)
from .tools.test_tools import (
    check_client_capabilities,
    test_conversation_loop,
    test_llm_sampling,
    test_requirement_completeness,
    test_user_elicitation,
)
```

### 7.2 更新工具注册

**需要替换的 @mcp.tool() 装饰器**:

| 原函数名 | 新调用方式 | 行号 |
|---------|-----------|------|
| `init_skill` | `mcp.add_tool(init_skill)` | 145 |
| `validate_skill` | `mcp.add_tool(validate_skill)` | 259 |
| `analyze_skill` | `mcp.add_tool(analyze_skill)` | 376 |
| `refactor_skill` | `mcp.add_tool(refactor_skill)` | 492 |
| `package_skill` | `mcp.add_tool(package_skill)` | 617 |
| `package_agent_skill` | `mcp.add_tool(package_agent_skill)` | 712 |
| `collect_requirements` | `mcp.add_tool(collect_requirements)` | 819 |
| `check_client_capabilities` | `mcp.add_tool(check_client_capabilities)` | 987 |
| `test_llm_sampling` | `mcp.add_tool(test_llm_sampling)` | 1001 |
| `test_user_elicitation` | `mcp.add_tool(test_user_elicitation)` | 1019 |
| `test_conversation_loop` | `mcp.add_tool(test_conversation_loop)` | 1037 |
| `test_requirement_completeness` | `mcp.add_tool(test_requirement_completeness)` | 1054 |
| `batch_validate_skills_tool` | `mcp.add_tool(batch_validate_skills_tool)` | 1073 |
| `batch_analyze_skills_tool` | `mcp.add_tool(batch_analyze_skills_tool)` | 1115 |

### 7.3 需要移除的内容

- 已提取的工具函数定义（行145-1154）
- 不再需要的单独导入

### 7.4 需要保留的内容

- `mcp = FastMCP(...)` 创建
- `@mcp.resource()` 装饰的资源注册
- `@mcp.prompt()` 装饰的提示注册

---

## 验证计划

### 测试步骤
1. 启动服务器: `uv run python -m skill_creator_mcp`
2. 运行测试套件: `uv run pytest --cov`
3. 检查代码质量: `uv run ruff check . && uv run mypy src/`

### 预期结果
- 所有测试通过
- server.py 减少约800-900行
- 工具功能完全正常

---

## 关键文件

### 需要修改
- `src/skill_creator_mcp/server.py` - 主服务器文件

### 已创建
- `src/skill_creator_mcp/tools/skill_tools.py`
- `src/skill_creator_mcp/tools/package_tools.py`
- `src/skill_creator_mcp/tools/requirement_tools.py`
- `src/skill_creator_mcp/tools/test_tools.py`
- `src/skill_creator_mcp/tools/batch_tools.py`

### 已存在
- `src/skill_creator_mcp/tools/batch_operations.py`
- `src/skill_creator_mcp/tools/health_check.py`

---

## 风险与注意事项

1. **导入冲突**: 使用 `mcp.add_tool()` 而非 `@mcp.tool()` 装饰器
2. **函数签名**: 确保包装函数接受 `ctx` 和 `mcp` 参数
3. **测试覆盖**: 验证所有 MCP 工具正常工作
4. **向后兼容**: 确保工具名称和参数不变
