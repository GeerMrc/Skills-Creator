# Web Search MCP 集成示例

## 概述

本示例展示如何为 Agent-Skill 集成 Web Search MCP，实现网络搜索功能。

**示例场景**：创建一个"技术问答助手"Agent-Skill，能够搜索网络获取最新的技术资料。

> **扩展提示**：此示例可作为集成其他 MCP（如 Database、FileSystem、Weather）的参考模板。

---

## 集成步骤

### Step 1: 配置声明

在 SKILL.md 的 frontmatter 中声明 MCP：

```yaml
---
name: tech-qa-assistant
description: 技术问答助手，搜索网络获取最新技术资料
version: 0.1.0
mcp_servers:
  required: ["skill-creator"]
  optional: ["WebSearch"]
---
```

**说明**：
- `required` - 必需的 MCP（skill-creator）
- `optional` - 可选的 MCP（WebSearch）

---

### Step 2: 工作流集成

在 Agent-Skill 工作流中调用 MCP 工具：

```python
# 检查 MCP 是否可用
if "WebSearch" in available_mcps:
    # 使用 WebSearch MCP
    search_results = await mcp_websearch_search(query="Python asyncio best practices")
else:
    # 降级处理
    return {"error": "WebSearch MCP 不可用，无法执行搜索"}
```

**集成模式**：

**1. 直接调用**（最简单）

```python
results = await mcp_websearch_search(query="搜索内容")
```

**2. 条件调用**（推荐）

```python
if "WebSearch" in available_mcps:
    results = await mcp_websearch_search(query="搜索内容")
else:
    log("WebSearch 不可用，使用本地缓存")
    results = get_from_cache(query)
```

**3. 错误处理**（生产环境）

```python
try:
    results = await mcp_websearch_search(query="搜索内容")
except Exception as e:
    log(f"搜索失败: {e}")
    results = get_fallback_results(query)
```

---

### Step 3: 测试验证

**单元测试**（Mock MCP）：

```python
import pytest
from unittest.mock import AsyncMock, patch

@pytest.mark.asyncio
async def test_websearch_integration():
    # Mock WebSearch MCP
    with patch("mcp_websearch_search", new_callable=AsyncMock) as mock_search:
        mock_search.return_value = [
            {"title": "Python Asyncio Guide", "url": "https://example.com"}
        ]

        # 调用集成代码
        results = await search_tech_info("Python asyncio")

        # 验证结果
        assert len(results) == 1
        assert results[0]["title"] == "Python Asyncio Guide"
```

**集成测试**（真实 MCP）：

```python
@pytest.mark.asyncio
async def test_websearch_real():
    # 连接真实 MCP 测试
    results = await mcp_websearch_search(query="Python asyncio")

    # 验证返回结果
    assert isinstance(results, list)
    assert len(results) > 0
    assert "title" in results[0]
    assert "url" in results[0]
```

**端到端测试**（完整工作流）：

```python
@pytest.mark.asyncio
async def test_tech_qa_workflow():
    # 测试完整工作流
    user_query = "如何使用 Python asyncio？"

    # 1. 搜索网络
    search_results = await mcp_websearch_search(query=user_query)

    # 2. 获取内容
    content = await mcp_webreader_webReader(url=search_results[0]["url"])

    # 3. 提取答案
    answer = extract_answer(content)

    # 验证
    assert answer is not None
    assert len(answer) > 0
```

---

## 完整示例代码

### tech-qa-assistant/SKILL.md

```yaml
---
name: tech-qa-assistant
description: 技术问答助手，搜索网络获取最新技术资料
version: 0.1.0
mcp_servers:
  required: ["skill-creator"]
  optional: ["WebSearch"]
triggers:
  - 搜索技术资料
  - 查找最新文档
  - 技术问答
---

# Tech QA Assistant

技术问答助手，通过 Web Search MCP 获取最新技术资料。

## 核心功能

搜索技术资料 | 提取答案 | 本地缓存
```

### workflow.py 示例

```python
from typing import Dict, Any

AVAILABLE_MCPS = get_available_mcps()

async def search_tech_info(query: str) -> Dict[str, Any]:
    """搜索技术信息"""
    if "WebSearch" not in AVAILABLE_MCPS:
        return {"error": "WebSearch MCP 不可用"}

    try:
        results = await mcp_websearch_search(query=query)
        return {"query": query, "results": results[:5], "count": len(results)}
    except Exception as e:
        return {"error": f"搜索失败: {e}", "query": query}

async def answer_tech_question(question: str) -> Dict[str, Any]:
    """完整工作流：搜索 + 获取内容 + 提取答案"""
    search_results = await search_tech_info(question)
    if "error" in search_results:
        return search_results

    content = await mcp_webreader_webReader(url=search_results["results"][0]["url"])
    return {"question": question, "answer": content[:500], "source": search_results["results"][0]["url"]}
```

---

## 常见问题

### Q1: 用户没有安装 WebSearch MCP？

使用降级方案：`if "WebSearch" not in available_mcps: return search_local(query)`

### Q2: 如何限制搜索结果数量？

使用切片：`results = await mcp_websearch_search(query=query); top_results = results[:5]`

### Q3: 如何缓存搜索结果？

使用本地缓存：保存到文件或数据库，搜索前先检查缓存

---

## 扩展建议

### 扩展1: 添加 Database MCP

搜索后保存到数据库：
```python
async def search_and_save(query: str):
    results = await mcp_websearch_search(query=query)
    await mcp_database_execute(sql="INSERT INTO searches (query, results) VALUES (?, ?)", params=[query, json.dumps(results)])
    return results
```

### 扩展2: 添加 Thinking MCP

记录搜索思考过程：
```python
async def search_with_thinking(query: str):
    session = await mcp_thinking_create_session(name=f"搜索-{query}")
    await mcp_thinking_sequential_thinking(thought=f"搜索查询: {query}", session_id=session["id"], thoughtNumber=1, totalThoughts=2, nextThoughtNeeded=True)
    results = await mcp_websearch_search(query=query)
    await mcp_thinking_sequential_thinking(thought=f"找到 {len(results)} 个结果", session_id=session["id"], thoughtNumber=2, totalThoughts=2, nextThoughtNeeded=False)
    return results
```

### 扩展3: 多 MCP 组合

WebSearch + Thinking + Database 组合使用。

---

## 总结

本示例展示了如何为 Agent-Skill 集成 Web Search MCP：

1. **配置声明** - 在 SKILL.md 中声明 MCP
2. **工作流集成** - 调用 MCP 工具，处理结果
3. **测试验证** - 单元测试、集成测试、端到端测试

**关键要点**：
- 检查 MCP 可用性，提供降级方案
- 处理 MCP 调用错误
- 编写完整的测试用例

**扩展参考**：
- [MCP 集成扩展指南](../references/mcp-integration-guide.md) - 通用方法论
- [GitHub MCP 集成示范](../references/mcp-github-integration.md) - GitHub 集成示例
- [Thinking MCP 集成示范](../references/mcp-thinking-integration.md) - Thinking 集成示例
