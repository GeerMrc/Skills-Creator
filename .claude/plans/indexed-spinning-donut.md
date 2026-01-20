# Skill-Creator 完整开发执行计划

## 项目概述

**项目名称**：skill-creator

**核心定位**：一个基于 **MCP Server + Agent-Skill 混合架构**的完整解决方案，用于开发、验证和优化 Agent-Skills。

**技术架构决策**：
- **MCP Server**：使用 FastMCP SDK 开发，提供 Tools、Resources、Prompts
- **Agent-Skill**：编排 MCP 工具，提供渐进式披露的知识和工作流

---

## 一、架构设计

### 1.1 完整架构图

```
┌─────────────────────────────────────────────────────────────────┐
│                        Claude Code / Desktop                     │
│                                                                 │
│  ┌───────────────────────────────────────────────────────────┐  │
│  │           skill-creator (Agent-Skill)                     │  │
│  │                                                           │  │
│  │  职责：教 Claude 如何创建技能                              │  │
│  │  - 渐进式披露三层架构                                      │  │
│  │  - 工作流定义（初始化 → 验证 → 分析 → 重构 → 打包）        │  │
│  │  - 最佳实践知识传递                                        │  │
│  │  - 编排 MCP 工具                                           │  │
│  │                                                           │  │
│  │  ┌─────────────────────────────────────────────────┐     │  │
│  │  │         MCP 客户端层                            │     │  │
│  │  └────────────────┬────────────────────────────────┘     │  │
│  └───────────────────┼───────────────────────────────────────┘  │
│                      │                                          │
│  ┌───────────────────▼───────────────────────────────────────┐  │
│  │              MCP Server (skill-creator-mcp)               │  │
│  │                                                           │  │
│  │  ┌─────────────────────────────────────────────────┐     │  │
│  │  │  Tools（可执行函数）                              │     │  │
│  │  │  • init_skill() - 初始化技能                     │     │  │
│  │  │  • validate_skill() - 验证技能                   │     │  │
│  │  │  • analyze_skill() - 分析技能                    │     │  │
│  │  │  • refactor_skill() - 重构建议                   │     │  │
│  │  │  • package_skill() - 打包技能                    │     │  │
│  │  └─────────────────────────────────────────────────┘     │  │
│  │                                                           │  │
│  │  ┌─────────────────────────────────────────────────┐     │  │
│  │  │  Resources（只读数据源）                          │     │  │
│  │  │  • skill://templates/{type} - 技能模板            │     │  │
│  │  │  • skill://best-practices - 最佳实践              │     │  │
│  │  │  • skill://validation-rules - 验证规则            │     │  │
│  │  └─────────────────────────────────────────────────┘     │  │
│  │                                                           │  │
│  │  ┌─────────────────────────────────────────────────┐     │  │
│  │  │  Prompts（可重用模板）                            │     │  │
│  │  │  • create-skill - 创建技能模板                    │     │  │
│  │  │  • validate-skill - 验证技能模板                  │     │  │
│  │  │  • refactor-skill - 重构技能模板                  │     │  │
│  │  └─────────────────────────────────────────────────┘     │  │
│  └───────────────────────────────────────────────────────────┘  │
│                      │                                          │
│                      ▼                                          │
│              文件系统 / Git                                     │
└─────────────────────────────────────────────────────────────────┘
```

### 1.2 MCP Server vs Agent-Skill 职责划分

| 维度 | MCP Server | Agent-Skill |
|------|-----------|-------------|
| **本质** | 标准化协议服务 | 能力扩展机制 |
| **开发方式** | FastMCP SDK + Python | 文件系统架构 |
| **传输协议** | STDIO / SSE | N/A |
| **提供内容** | Tools（原子操作）<br>Resources（数据源）<br>Prompts（模板） | 工作流定义<br>最佳实践知识<br>渐进式披露 |
| **控制方** | Model 控制工具调用<br>Application 控制资源<br>User 控制提示 | Claude 自主判断激活 |
| **相互关系** | 被 Agent-Skill 编排调用 | 编排 MCP 工具完成任务 |

---

## 二、技术规格

### 2.1 MCP Server 技术栈

**核心框架**：FastMCP SDK（Python）

**传输协议支持**：
- **STDIO**：本地开发，最佳性能
- **SSE (HTTP)**：远程部署，支持标准认证

**关键依赖**：
```toml
[project]
name = "skill-creator-mcp"
version = "0.1.0"
requires-python = ">=3.10"
dependencies = [
    "fastmcp>=0.11.0",
    "pydantic>=2.0.0",
    "aiohttp>=3.9.0",
    "aiofiles>=23.0.0",
]

[project.optional-dependencies]
dev = [
    "pytest>=7.0.0",
    "pytest-asyncio>=0.21.0",
    "ruff>=0.1.0",
    "mypy>=1.0.0",
]
```

### 2.2 MCP Server 目录结构（符合最佳实践）

```
skill-creator-mcp/                     # MCP Server 项目根目录
├── pyproject.toml                     # 项目配置
├── README.md                          # 项目说明
├── .gitignore
├── LICENSE
├── src/skill_creator_mcp/             # 源代码目录
│   ├── __init__.py
│   ├── __main__.py                    # 入口点（STDIO）
│   ├── server.py                      # MCP Server 定义
│   ├── tools/                         # Tools 实现
│   │   ├── __init__.py
│   │   ├── init_skill.py              # 初始化工具
│   │   ├── validate_skill.py          # 验证工具
│   │   ├── analyze_skill.py           # 分析工具
│   │   ├── refactor_skill.py          # 重构工具
│   │   └── package_skill.py           # 打包工具
│   ├── resources/                     # Resources 实现
│   │   ├── __init__.py
│   │   ├── templates.py               # 模板资源
│   │   ├── best_practices.py          # 最佳实践资源
│   │   └── validation_rules.py        # 验证规则资源
│   ├── prompts/                       # Prompts 实现
│   │   ├── __init__.py
│   │   ├── create_skill.py            # 创建技能提示
│   │   ├── validate_skill.py          # 验证技能提示
│   │   └── refactor_skill.py          # 重构技能提示
│   ├── models/                        # 数据模型
│   │   ├── __init__.py
│   │   ├── skill_config.py            # 技能配置模型
│   │   ├── validation_result.py       # 验证结果模型
│   │   └── analysis_result.py         # 分析结果模型
│   ├── templates/                     # 技能模板文件
│   │   ├── minimal/
│   │   ├── tool-based/
│   │   ├── workflow-based/
│   │   └── analyzer-based/
│   └── utils/                         # 工具函数
│       ├── __init__.py
│       ├── file_ops.py                # 文件操作
│       ├── validators.py              # 验证器
│       └── analyzers.py               # 分析器
├── tests/                             # 测试目录
│   ├── __init__.py
│   ├── conftest.py                    # pytest 配置
│   ├── test_tools/
│   ├── test_resources/
│   └── test_prompts/
├── examples/                          # 使用示例
│   └── basic_usage.py
└── docs/                              # 文档
    ├── ARCHITECTURE.md
    └── API.md
```

### 2.3 Agent-Skill 目录结构

```
skill-creator/                         # Agent-Skill 项目根目录
├── SKILL.md                           # 主入口（≤150行）
├── README.md                          # 项目说明
├── .claude/
│   └── settings.json                  # Claude Code 配置
├── references/                        # 详细文档（按需加载）
│   ├── initialization.md              # (~250行)
│   ├── validation.md                  # (~300行)
│   ├── best-practices.md              # (~280行)
│   ├── refactoring.md                 # (~250行)
│   └── mcp-integration.md             # (~200行) MCP 集成说明
├── examples/                          # 使用示例
│   ├── creating-simple-skill.md
│   ├── validating-and-fixing.md
│   └── using-mcp-tools.md
└── assets/                            # 资源文件
    └── checklists/
        └── development-checklist.md
```

---

## 三、MCP Server 开发规范

### 3.1 使用 FastMCP SDK

**服务器定义**（`src/skill_creator_mcp/server.py`）：
```python
"""Skill Creator MCP Server."""

from fastmcp import FastMCP
from .tools import (
    init_skill,
    validate_skill,
    analyze_skill,
    refactor_skill,
    package_skill,
)
from .resources import (
    templates,
    best_practices,
    validation_rules,
)
from .prompts import (
    create_skill,
    validate_skill,
    refactor_skill,
)

# 创建 MCP Server
mcp = FastMCP(
    name="skill-creator",
    instructions="""
    Skill Creator MCP Server - Agent-Skills 开发工具

    这个服务器提供创建、验证、分析和重构 Agent-Skills 的工具。

    Tools:
    - init_skill: 初始化新技能
    - validate_skill: 验证技能规范
    - analyze_skill: 分析技能质量
    - refactor_skill: 生成重构建议
    - package_skill: 打包技能

    Resources:
    - skill://templates/{type}: 获取技能模板
    - skill://best-practices: 获取最佳实践
    - skill://validation-rules: 获取验证规则

    Prompts:
    - create-skill: 创建技能工作流
    - validate-skill: 验证技能工作流
    - refactor-skill: 重构技能工作流
    """
)

# 注册 Tools
mcp.add_tool(init_skill)
mcp.add_tool(validate_skill)
mcp.add_tool(analyze_skill)
mcp.add_tool(refactor_skill)
mcp.add_tool(package_skill)

# 注册 Resources
mcp.add_resource(templates)
mcp.add_resource(best_practices)
mcp.add_resource(validation_rules)

# 注册 Prompts
mcp.add_prompt(create_skill)
mcp.add_prompt(validate_skill)
mcp.add_prompt(refactor_skill)

# 创建入口点
server = mcp.get_server()
```

### 3.2 Tool 定义规范

**使用 async/await**：
```python
"""Tools: init_skill"""

from typing import Literal
from pydantic import BaseModel, Field
from ..models.skill_config import SkillConfig
from ..utils.file_ops import create_directory_structure
from ..utils.templates import render_template


class InitSkillInput(BaseModel):
    """初始化技能输入参数"""

    name: str = Field(
        ...,
        description="技能名称（小写字母、数字、连字符，1-64字符）",
        pattern=r"^[a-z0-9]([a-z0-9-]*[a-z0-9])?$",
        min_length=1,
        max_length=64,
    )
    template: Literal["minimal", "tool-based", "workflow-based", "analyzer-based"] = Field(
        default="minimal",
        description="技能模板类型",
    )
    output_dir: str = Field(
        default=".",
        description="输出目录路径",
    )
    with_scripts: bool = Field(
        default=False,
        description="是否包含示例脚本",
    )


async def init_skill(input: InitSkillInput) -> dict:
    """
    初始化新的 Agent-Skill

    创建符合规范的技能目录结构和模板文件。

    Args:
        input: 初始化参数

    Returns:
        包含创建结果的字典
    """
    try:
        # 创建目录结构
        skill_dir = await create_directory_structure(
            input.name,
            input.template,
            input.output_dir,
        )

        # 渲染 SKILL.md
        await render_template(
            input.template,
            skill_dir / "SKILL.md",
            {"name": input.name},
        )

        # 创建引用文件
        if input.template != "minimal":
            await create_reference_files(skill_dir, input.template)

        # 创建示例脚本
        if input.with_scripts:
            await create_example_scripts(skill_dir)

        return {
            "success": True,
            "skill_path": str(skill_dir),
            "message": f"技能 '{input.name}' 已创建",
        }

    except Exception as e:
        return {
            "success": False,
            "error": str(e),
        }
```

### 3.3 Resource 定义规范

```python
"""Resources: templates"""

from fastmcp import Resource
from typing import Literal
import aiofiles
from pathlib import Path


async def get_template(
    template_type: Literal["minimal", "tool-based", "workflow-based", "analyzer-based"]
) -> Resource:
    """获取技能模板内容"""
    template_path = Path(__file__).parent.parent / "templates" / template_type / "SKILL.md.tmpl"

    async with aiofiles.open(template_path, encoding="utf-8") as f:
        content = await f.read()

    return Resource(
        uri=f"skill://templates/{template_type}",
        name=f"{template_type}-template",
        description=f"{template_type} 技能模板",
        mimeType="text/markdown",
        content=content,
    )


# 注册资源模板
templates_resource = mcp.resource("skill://templates/{type}")(get_template)
```

### 3.4 Prompt 定义规范

```python
"""Prompts: create_skill"""

from fastmcp import Prompt
from typing import Optional


async def create_skill_prompt(
    name: str,
    description: Optional[str] = None,
    template_type: str = "minimal",
) -> Prompt:
    """
    创建技能工作流提示

    引导用户完成技能创建的完整流程。
    """
    template = f"""
# 创建 Agent-Skill: {name}

## 步骤 1: 定义技能描述

请提供以下信息：
- 技能名称: {name}
- 技能功能描述: {description or "待填写"}
- 使用场景: 待填写
- 触发词: 待填写

## 步骤 2: 选择模板类型

当前选择: {template_type}

可用模板:
- minimal: 最小模板（约40行）
- tool-based: 工具型模板（约50行）
- workflow-based: 工作流型模板（约70行）
- analyzer-based: 分析型模板（约80行）

## 步骤 3: 生成技能结构

使用工具: init_skill(name="{name}", template="{template_type}")

## 步骤 4: 验证技能

使用工具: validate_skill(path="<技能路径>")

## 步骤 5: 优化和发布

根据验证结果优化技能内容。
"""

    return Prompt(
        name="create-skill",
        description="创建 Agent-Skill 的工作流程",
        template=template,
        arguments=[
            {
                "name": "name",
                "description": "技能名称",
                "required": True,
            },
            {
                "name": "description",
                "description": "技能描述",
                "required": False,
            },
            {
                "name": "template_type",
                "description": "模板类型",
                "required": False,
            },
        ],
    )


# 注册提示
create_skill_prompt = mcp.prompt()(create_skill_prompt)
```

### 3.5 传输协议支持

**STDIO 入口点**（`src/skill_creator_mcp/__main__.py`）：
```python
"""STDIO 传输入口点（本地开发）"""

import asyncio
from .server import mcp


async def main():
    """启动 STDIO 服务器"""
    from mcp.server.stdio import stdio_server

    async with stdio_server() as (read_stream, write_stream):
        await mcp.run(
            read_stream,
            write_stream,
            mcp.get_server_initialization_options(),
        )


if __name__ == "__main__":
    asyncio.run(main())
```

**SSE 入口点**（`src/skill_creator_mcp/http_server.py`）：
```python
"""SSE 传输入口点（远程部署）"""

import asyncio
from fastmcp import FastMCP
from mcp.server.sse import SseServerTransport
from starlette.applications import Starlette
from starlette.routing import Route
from starlette.requests import Request
import uvicorn

from .server import mcp


# 创建 SSE 服务器
app = Starlette(
    debug=True,
    routes=[
        Route("/sse", endpoint=handle_sse),
    ],
)


async def handle_sse(request: Request):
    """处理 SSE 连接"""
    transport = SseServerTransport("/messages")

    async with transport.connect_sse(
        request.scope,
        request.receive,
        request._send,  # type: ignore
    ) as (read_stream, write_stream):
        await mcp.run(
            read_stream,
            write_stream,
            mcp.get_server_initialization_options(),
        )


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
```

---

## 四、Agent-Skill 开发规范

### 4.1 SKILL.md 模板

```yaml
---
name: skill-creator
description: |
  Agent-Skills 开发与质量保证工具。提供技能初始化、规范验证、结构分析、重构建议、模板生成和打包发布功能。

  何时使用：
  - 创建新的 Agent-Skill
  - 验证技能是否符合最佳实践
  - 分析技能的 token 效率和结构问题
  - 重构现有技能以提升质量
  - 打包和发布技能

  触发词：创建技能、验证技能、分析技能、重构技能、技能模板、技能打包
allowed-tools: Read, Write, Edit, Bash, Glob, Grep
mcp_servers:
  - skill-creator-mcp
---

# Skill-Creator - Agent-Skills 开发工具

## 技能概述

Skill-Creator 是一个元技能，通过 MCP Server 提供专业工具，用于开发、验证和优化 Agent-Skills。

## 核心能力

1. **技能初始化**：通过 MCP 工具生成符合规范的技能结构
2. **规范验证**：自动检查命名、描述、结构是否符合最佳实践
3. **质量分析**：Token 效率分析、反模式识别、改进建议
4. **重构建议**：基于最佳实践生成可执行的重构方案
5. **模板库**：4 种技能模板，支持自定义扩展
6. **打包发布**：质量检查 + 分发包生成

## 快速开始

### 创建新技能

使用 MCP 提示：
```
使用 create-skill 提示创建一个名为 'docker-manager' 的技能
```

或直接调用工具：
```
调用 mcp__skill_creator__init_skill，参数：name="docker-manager", template="tool-based"
```

### 验证技能

```
调用 mcp__skill_creator__validate_skill，参数：path="/path/to/skill"
```

## MCP 工具列表

| 工具 | 描述 |
|------|------|
| `init_skill` | 初始化新技能 |
| `validate_skill` | 验证技能规范 |
| `analyze_skill` | 分析技能质量 |
| `refactor_skill` | 生成重构建议 |
| `package_skill` | 打包技能 |

## MCP 资源列表

| 资源 | 描述 |
|------|------|
| `skill://templates/{type}` | 获取技能模板 |
| `skill://best-practices` | 获取最佳实践 |
| `skill://validation-rules` | 获取验证规则 |

## MCP 提示列表

| 提示 | 描述 |
|------|------|
| `create-skill` | 创建技能工作流 |
| `validate-skill` | 验证技能工作流 |
| `refactor-skill` | 重构技能工作流 |

## 详细文档

- **[MCP 集成说明](references/mcp-integration.md)**
- **[初始化详解](references/initialization.md)**
- **[验证规则](references/validation.md)**
- **[最佳实践](references/best-practices.md)**
- **[重构指南](references/refactoring.md)**
```

---

## 五、开发流程规范

### 5.1 开发阶段划分

| 阶段 | 内容 | 工作量 |
|------|------|--------|
| **阶段 1** | MCP Server 框架搭建 | 2-3天 |
| **阶段 2** | MCP Tools 开发 | 5-7天 |
| **阶段 3** | MCP Resources 开发 | 2-3天 |
| **阶段 4** | MCP Prompts 开发 | 2-3天 |
| **阶段 5** | Agent-Skill 开发 | 2-3天 |
| **阶段 6** | 测试和优化 | 3-4天 |
| **阶段 7** | 文档和示例 | 2-3天 |

**总计**：约 3-4 周开发周期

### 5.2 阶段 1：MCP Server 框架搭建（2-3天）

**任务清单**：
- [ ] 创建项目目录结构
- [ ] 配置 `pyproject.toml`
- [ ] 创建 `server.py` 基础框架
- [ ] 实现 STDIO 入口点
- [ ] 实现 SSE 入口点（可选）
- [ ] 配置开发环境
- [ ] 编写基础测试

**验收标准**：
- [ ] 服务器可以通过 STDIO 启动
- [ ] 可以通过 MCP Inspector 连接
- [ ] 基础测试通过

### 5.3 阶段 2：MCP Tools 开发（5-7天）

**任务清单**：
- [ ] `init_skill` - 初始化工具
- [ ] `validate_skill` - 验证工具
- [ ] `analyze_skill` - 分析工具
- [ ] `refactor_skill` - 重构工具
- [ ] `package_skill` - 打包工具
- [ ] 单元测试

**验收标准**：
- [ ] 所有工具可独立调用
- [ ] 输入验证完整
- [ ] 错误处理完善
- [ ] 单元测试覆盖率 > 80%

### 5.4 阶段 3：MCP Resources 开发（2-3天）

**任务清单**：
- [ ] `templates` - 模板资源
- [ ] `best_practices` - 最佳实践资源
- [ ] `validation_rules` - 验证规则资源
- [ ] 单元测试

**验收标准**：
- [ ] 所有资源可访问
- [ ] 内容格式正确
- [ ] 单元测试通过

### 5.5 阶段 4：MCP Prompts 开发（2-3天）

**任务清单**：
- [ ] `create_skill` - 创建技能提示
- [ ] `validate_skill` - 验证技能提示
- [ ] `refactor_skill` - 重构技能提示
- [ ] 单元测试

**验收标准**：
- [ ] 所有提示可调用
- [ ] 参数验证完整
- [ ] 单元测试通过

### 5.6 阶段 5：Agent-Skill 开发（2-3天）

**任务清单**：
- [ ] 编写 `SKILL.md`
- [ ] 创建引用文件
- [ ] 创建使用示例
- [ ] 自我验证

**验收标准**：
- [ ] SKILL.md ≤ 150行
- [ ] 引用文件完整
- [ ] 自身符合最佳实践

### 5.7 阶段 6：测试和优化（3-4天）

**任务清单**：
- [ ] 集成测试
- [ ] 端到端测试
- [ ] 性能优化
- [ ] 错误处理完善

**验收标准**：
- [ ] 所有测试通过
- [ ] 响应时间 < 1s
- [ ] 无已知 bug

### 5.8 阶段 7：文档和示例（2-3天）

**任务清单**：
- [ ] API 文档
- [ ] 架构文档
- [ ] 使用示例
- [ ] 故障排查指南

**验收标准**：
- [ ] 文档完整清晰
- [ ] 示例可运行

---

## 六、验证标准

### 6.1 MCP Server 验证标准

| 检查项 | 标准 | 优先级 |
|--------|------|--------|
| 服务器启动 | STDIO 和 SSE 都能正常启动 | 必须 |
| 工具注册 | 所有工具可被发现和调用 | 必须 |
| 资源注册 | 所有资源可被发现和读取 | 必须 |
| 提示注册 | 所有提示可被发现和调用 | 必须 |
| 错误处理 | 所有异常都有适当处理 | 必须 |
| 类型注解 | 所有函数都有类型注解 | 推荐 |
| 异步支持 | 所有 I/O 操作都是异步的 | 必须 |
| 测试覆盖 | 单元测试覆盖率 > 80% | 必须 |

### 6.2 Agent-Skill 验证标准

| 检查项 | 标准 | 优先级 |
|--------|------|--------|
| SKILL.md 行数 | ≤200行（推荐≤150行） | 必须 |
| 描述完整性 | 功能+场景+触发词 | 必须 |
| MCP 集成 | 正确引用 MCP 工具 | 必须 |
| 自洽性 | 自身符合最佳实践 | 必须 |

---

## 七、关键文件清单（按优先级）

### MCP Server 文件

| 文件 | 优先级 | 预估行数 | 描述 |
|------|--------|---------|------|
| `src/skill_creator_mcp/server.py` | P0 | ~100 | MCP Server 定义 |
| `src/skill_creator_mcp/tools/init_skill.py` | P0 | ~200 | 初始化工具 |
| `src/skill_creator_mcp/tools/validate_skill.py` | P0 | ~250 | 验证工具 |
| `src/skill_creator_mcp/tools/analyze_skill.py` | P1 | ~300 | 分析工具 |
| `src/skill_creator_mcp/tools/refactor_skill.py` | P2 | ~250 | 重构工具 |
| `src/skill_creator_mcp/tools/package_skill.py` | P2 | ~150 | 打包工具 |
| `src/skill_creator_mcp/resources/templates.py` | P1 | ~150 | 模板资源 |
| `src/skill_creator_mcp/prompts/create_skill.py` | P1 | ~100 | 创建提示 |
| `src/skill_creator_mcp/__main__.py` | P0 | ~50 | STDIO 入口 |
| `src/skill_creator_mcp/http_server.py` | P2 | ~80 | SSE 入口 |
| `tests/test_*.py` | P1 | ~800 | 测试文件 |

### Agent-Skill 文件

| 文件 | 优先级 | 预估行数 | 描述 |
|------|--------|---------|------|
| `SKILL.md` | P0 | ≤150 | 主入口 |
| `references/mcp-integration.md` | P0 | ~200 | MCP 集成说明 |
| `references/best-practices.md` | P1 | ~280 | 最佳实践 |
| `references/validation.md` | P1 | ~300 | 验证规则 |
| `examples/*.md` | P2 | ~500 | 使用示例 |

---

## 八、参考资源

**FastMCP**：
- [FastMCP GitHub](https://github.com/jlowin/fastmcp)
- [FastMCP 文档](https://gofastmcp.com)
- [Building an MCP server in Python using FastMCP](https://mcpcat.io/guides/building-mcp-server-python-fastmcp/)

**MCP 官方**：
- [MCP Python SDK](https://github.com/modelcontextprotocol/python-sdk)
- [MCP 服务器文档](/models/claude-glm/claude-code-docs/claude-mcp-docs/MCP-服务器.md)

**本地参考**：
- DeepSkills 项目：`/models/claude-glm/DeepSkills/`
- MCP 边界文档：`/models/claude-glm/claude-code-docs/MCP-AgentSkills使用与开发边界.md`

---

## 九、部署配置

### 9.1 Claude Code 配置

```json
{
  "mcpServers": {
    "skill-creator": {
      "command": "uv",
      "args": [
        "--directory",
        "/path/to/skill-creator-mcp",
        "run",
        "python",
        "-m",
        "skill_creator_mcp"
      ]
    }
  }
}
```

### 9.2 环境变量配置

```bash
# MCP Server 配置
MCP_SERVER_LOG_LEVEL=info
MCP_SERVER_MAX_CONNECTIONS=10

# 技能模板目录
SKILL_TEMPLATES_DIR=/usr/local/share/skill-creator/templates

# 工作目录
SKILL_WORK_DIR=/tmp/skill-creator
```

---

## 十、完整项目配置文件

### 10.1 pyproject.toml（完整配置）

```toml
[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[project]
name = "skill-creator-mcp"
version = "0.1.0"
description = "Agent-Skills 开发与质量保证 MCP Server"
readme = "README.md"
requires-python = ">=3.10"
license = { text = "MIT" }
authors = [
    { name = "Your Name", email = "your.email@example.com" }
]
keywords = ["mcp", "agent-skills", "claude", "ai"]
classifiers = [
    "Development Status :: 3 - Alpha",
    "Intended Audience :: Developers",
    "License :: OSI Approved :: MIT License",
    "Programming Language :: Python :: 3",
    "Programming Language :: Python :: 3.10",
    "Programming Language :: Python :: 3.11",
    "Programming Language :: Python :: 3.12",
    "Topic :: Software Development :: Libraries :: Python Modules",
]

dependencies = [
    "fastmcp>=0.11.0",
    "pydantic>=2.0.0",
    "aiohttp>=3.9.0",
    "aiofiles>=23.0.0",
    "pyyaml>=6.0",
    "jinja2>=3.1.0",
    "rich>=13.0.0",
]

[project.optional-dependencies]
dev = [
    "pytest>=7.0.0",
    "pytest-asyncio>=0.21.0",
    "pytest-cov>=4.0.0",
    "ruff>=0.1.0",
    "mypy>=1.0.0",
    "pre-commit>=3.0.0",
]
sse = [
    "uvicorn[standard]>=0.24.0",
    "starlette>=0.27.0",
]

[project.urls]
Homepage = "https://github.com/yourusername/skill-creator-mcp"
Documentation = "https://github.com/yourusername/skill-creator-mcp#readme"
Repository = "https://github.com/yourusername/skill-creator-mcp"
Issues = "https://github.com/yourusername/skill-creator-mcp/issues"

[project.scripts]
skill-creator-mcp = "skill_creator_mcp:main"

[tool.hatch.build.targets.wheel]
packages = ["src/skill_creator_mcp"]

[tool.ruff]
line-length = 100
target-version = "py310"
select = [
    "E",
    "F",
    "I",
    "N",
    "W",
    "UP",
]
ignore = [
    "E501",
    "B008",
]

[tool.ruff.isort]
known-first-party = ["skill_creator_mcp"]

[tool.mypy]
python_version = "3.10"
warn_return_any = true
warn_unused_configs = true
disallow_untyped_defs = true
disallow_incomplete_defs = true
check_untyped_defs = true
no_implicit_optional = true

[[tool.mypy.overrides]]
module = "tests.*"
disallow_untyped_defs = false

[tool.pytest.ini_options]
asyncio_mode = "auto"
testpaths = ["tests"]
addopts = [
    "--cov=src/skill_creator_mcp",
    "--cov-report=html",
    "--cov-report=term-missing",
    "-v",
]

[tool.coverage.run]
source = ["src"]
omit = [
    "*/tests/*",
    "*/test_*.py",
]

[tool.coverage.report]
exclude_lines = [
    "pragma: no cover",
    "def __repr__",
    "raise AssertionError",
    "raise NotImplementedError",
    "if __name__ == .__main__.:",
    "if TYPE_CHECKING:",
]
```

### 10.2 .gitignore（完整配置）

```gitignore
# Byte-compiled / optimized / DLL files
__pycache__/
*.py[cod]
*$py.class

# C extensions
*.so

# Distribution / packaging
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
pip-wheel-metadata/
pip-delete-this-directory.txt

# PyInstaller
*.manifest
*.spec

# Unit test / coverage reports
htmlcov/
.tox/
.nox/
.coverage
.coverage.*
.cache
nosetests.xml
coverage.xml
*.cover
*.py,cover
.hypothesis/
.pytest_cache/

# Environments
.env
.venv
env/
venv/
ENV/
env.bak/
venv.bak/

# IDEs
.vscode/
.idea/
*.swp
*.swo
*~

# OS
.DS_Store
Thumbs.db

# Project specific
*.log
.SKILL.md.bak
```

### 10.3 README.md（完整模板）

```markdown
# Skill Creator MCP Server

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![Code style: ruff](https://img.shields.io/badge/code%20style-ruff-000000.svg)](https://github.com/astral-sh/ruff)

Agent-Skills 开发与质量保证 MCP Server。

## 特性

- ✅ 4 种技能模板
- ✅ 自动化规范验证
- ✅ Token 效率分析
- ✅ 反模式识别
- ✅ 重构建议生成
- ✅ 打包发布工具

## 安装

### 使用 uv（推荐）

```bash
uv tool install skill-creator-mcp
```

### 使用 pip

```bash
pip install skill-creator-mcp
```

## 配置

### Claude Code 配置

```json
{
  "mcpServers": {
    "skill-creator": {
      "command": "uv",
      "args": [
        "--directory",
        "/path/to/skill-creator-mcp",
        "run",
        "python",
        "-m",
        "skill_creator_mcp"
      ]
    }
  }
}
```

## 使用

### 初始化技能

```
调用 mcp__skill_creator__init_skill，参数：
- name: "my-skill"
- template: "tool-based"
- output_dir: "./skills"
```

### 验证技能

```
调用 mcp__skill_creator__validate_skill，参数：
- path: "/path/to/skill"
```

## 开发

```bash
# 克隆仓库
git clone https://github.com/yourusername/skill-creator-mcp
cd skill-creator-mcp

# 安装开发依赖
uv sync --dev

# 运行测试
pytest

# 运行 lint
ruff check .
```

## 许可证

MIT License
```

### 10.4 Docker 配置

**Dockerfile**：
```dockerfile
FROM python:3.11-slim

WORKDIR /app

# 安装 uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv

# 复制项目文件
COPY pyproject.toml ./
COPY README.md ./
COPY src/ ./src/

# 安装依赖
RUN uv sync --frozen --no-dev

# 暴露端口（用于 SSE）
EXPOSE 8000

# 运行服务器
CMD ["uv", "run", "python", "-m", "skill_creator_mcp.http_server"]
```

**docker-compose.yml**：
```yaml
version: '3.8'

services:
  skill-creator-mcp:
    build: .
    ports:
      - "8000:8000"
    environment:
      - MCP_SERVER_LOG_LEVEL=info
      - SKILL_WORK_DIR=/workspace
    volumes:
      - ./workspace:/workspace
    restart: unless-stopped
```

### 10.5 CI/CD 配置

**.github/workflows/ci.yml**：
```yaml
name: CI

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main, develop]

jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: ["3.10", "3.11", "3.12"]

    steps:
      - uses: actions/checkout@v4

      - name: Install uv
        run: |
          curl -LsSf https://astral.sh/uv/install.sh | sh
          echo "$HOME/.local/bin" >> $GITHUB_PATH

      - name: Set up Python ${{ matrix.python-version }}
        run: uv python install ${{ matrix.python-version }}

      - name: Install dependencies
        run: uv sync --dev

      - name: Run lint
        run: uv run ruff check .

      - name: Run type check
        run: uv run mypy src/

      - name: Run tests
        run: uv run pytest --cov

      - name: Upload coverage
        uses: codecov/codecov-action@v3

  docker:
    runs-on: ubuntu-latest
    needs: test

    steps:
      - uses: actions/checkout@v4

      - name: Set up Docker Buildx
        uses: docker/setup-buildx-action@v2

      - name: Build Docker image
        run: docker build -t skill-creator-mcp .

      - name: Run Docker tests
        run: docker run skill-creator-mcp uv run pytest
```

---

## 十一、完整实现代码

### 11.1 核心模块实现

**`src/skill_creator_mcp/__init__.py`**：
```python
"""Skill Creator MCP Server."""

__version__ = "0.1.0"

from .server import mcp, server

__all__ = ["mcp", "server"]
```

**`src/skill_creator_mcp/server.py`**（完整实现）：
```python
"""Skill Creator MCP Server."""

from fastmcp import FastMCP

# 创建 MCP Server
mcp = FastMCP(
    name="skill-creator",
    instructions="""
    Skill Creator MCP Server - Agent-Skills 开发工具

    这个服务器提供创建、验证、分析和重构 Agent-Skills 的工具。

    ## Tools（工具）

    ### init_skill
    初始化新的 Agent-Skill。

    参数：
    - name (str): 技能名称（小写字母、数字、连字符，1-64字符）
    - template (str): 模板类型（minimal/tool-based/workflow-based/analyzer-based）
    - output_dir (str): 输出目录路径
    - with_scripts (bool): 是否包含示例脚本

    ### validate_skill
    验证 Agent-Skill 规范。

    参数：
    - path (str): 技能路径
    - strict (bool): 严格模式

    ### analyze_skill
    分析 Agent-Skill 质量。

    参数：
    - path (str): 技能路径

    ### refactor_skill
    生成重构建议。

    参数：
    - path (str): 技能路径
    - auto_apply (bool): 自动应用

    ### package_skill
    打包 Agent-Skill。

    参数：
    - path (str): 技能路径
    - format (str): 打包格式（zip/tar.gz）

    ## Resources（资源）

    ### skill://templates/{type}
    获取技能模板内容。

    参数：
    - type: 模板类型（minimal/tool-based/workflow-based/analyzer-based）

    ### skill://best-practices
    获取最佳实践文档。

    ### skill://validation-rules
    获取验证规则文档。

    ## Prompts（提示）

    ### create-skill
    创建技能工作流。

    参数：
    - name (str): 技能名称
    - description (str): 技能描述
    - template_type (str): 模板类型

    ### validate-skill
    验证技能工作流。

    参数：
    - path (str): 技能路径

    ### refactor-skill
    重构技能工作流。

    参数：
    - path (str): 技能路径
    """
)

# 导入所有工具、资源、提示
from .tools import (
    init_skill_tool,
    validate_skill_tool,
    analyze_skill_tool,
    refactor_skill_tool,
    package_skill_tool,
)
from .resources import (
    templates_resource,
    best_practices_resource,
    validation_rules_resource,
)
from .prompts import (
    create_skill_prompt,
    validate_skill_prompt,
    refactor_skill_prompt,
)

# 注册 Tools
mcp.add_tool(init_skill_tool)
mcp.add_tool(validate_skill_tool)
mcp.add_tool(analyze_skill_tool)
mcp.add_tool(refactor_skill_tool)
mcp.add_tool(package_skill_tool)

# 注册 Resources
mcp.add_resource(templates_resource)
mcp.add_resource(best_practices_resource)
mcp.add_resource(validation_rules_resource)

# 注册 Prompts
mcp.add_prompt(create_skill_prompt)
mcp.add_prompt(validate_skill_prompt)
mcp.add_prompt(refactor_skill_prompt)

# 创建服务器实例
server = mcp.get_server()


async def main():
    """主入口点（STDIO）."""
    import asyncio
    from mcp.server.stdio import stdio_server

    async with stdio_server() as (read_stream, write_stream):
        await mcp.run(
            read_stream,
            write_stream,
            mcp.get_server_initialization_options(),
        )
```

### 11.2 Models 实现

**`src/skill_creator_mcp/models/__init__.py`**：
```python
"""数据模型."""

from .skill_config import (
    SkillConfig,
    SkillTemplateType,
    InitSkillInput,
)
from .validation_result import (
    ValidationResult,
    ValidationSeverity,
)
from .analysis_result import (
    AnalysisResult,
    TokenEfficiencyMetrics,
    AntiPattern,
)

__all__ = [
    "SkillConfig",
    "SkillTemplateType",
    "InitSkillInput",
    "ValidationResult",
    "ValidationSeverity",
    "AnalysisResult",
    "TokenEfficiencyMetrics",
    "AntiPattern",
]
```

**`src/skill_creator_mcp/models/skill_config.py`**：
```python
"""技能配置模型."""

from typing import Literal, Optional
from pydantic import BaseModel, Field, field_validator
import re


class SkillTemplateType(str):
    """技能模板类型."""

    MINIMAL = "minimal"
    TOOL_BASED = "tool-based"
    WORKFLOW_BASED = "workflow-based"
    ANALYZER_BASED = "analyzer-based"


class InitSkillInput(BaseModel):
    """初始化技能输入参数."""

    name: str = Field(
        ...,
        description="技能名称（小写字母、数字、连字符，1-64字符）",
        min_length=1,
        max_length=64,
    )
    template: SkillTemplateType = Field(
        default=SkillTemplateType.MINIMAL,
        description="技能模板类型",
    )
    output_dir: str = Field(
        default=".",
        description="输出目录路径",
    )
    with_scripts: bool = Field(
        default=False,
        description="是否包含示例脚本",
    )
    with_examples: bool = Field(
        default=False,
        description="是否包含使用示例",
    )

    @field_validator("name")
    @classmethod
    def validate_name(cls, v: str) -> str:
        """验证技能名称符合规范."""
        pattern = r'^[a-z0-9]([a-z0-9-]*[a-z0-9])?$'
        if not re.match(pattern, v):
            raise ValueError(
                f"技能名称 '{v}' 不符合规范。"
                "要求：小写字母、数字、连字符，不能以连字符开头或结尾"
            )
        return v


class SkillConfig(BaseModel):
    """技能配置."""

    name: str
    template: SkillTemplateType
    description: Optional[str] = None
    author: Optional[str] = None
    version: Optional[str] = "0.1.0"
```

**`src/skill_creator_mcp/models/validation_result.py`**：
```python
"""验证结果模型."""

from typing import List, Optional
from pydantic import BaseModel
from enum import Enum


class ValidationSeverity(str, Enum):
    """验证严重级别."""

    ERROR = "error"
    WARNING = "warning"
    SUGGESTION = "suggestion"


class ValidationIssue(BaseModel):
    """验证问题."""

    severity: ValidationSeverity
    code: str
    message: str
    file_path: Optional[str] = None
    line: Optional[int] = None


class ValidationResult(BaseModel):
    """验证结果."""

    valid: bool
    issues: List[ValidationIssue] = []
    score: int = 100
    metrics: dict = {}

    def add_error(self, code: str, message: str, **kwargs):
        """添加错误。"""
        self.valid = False
        self.score -= 20
        self.issues.append(ValidationIssue(
            severity=ValidationSeverity.ERROR,
            code=code,
            message=message,
            **kwargs
        ))

    def add_warning(self, code: str, message: str, **kwargs):
        """添加警告。"""
        self.score -= 10
        self.issues.append(ValidationIssue(
            severity=ValidationSeverity.WARNING,
            code=code,
            message=message,
            **kwargs
        ))
```

### 11.3 Tools 实现

**`src/skill_creator_mcp/tools/__init__.py`**：
```python
"""Tools 模块."""

from .init_skill import init_skill_tool
from .validate_skill import validate_skill_tool
from .analyze_skill import analyze_skill_tool
from .refactor_skill import refactor_skill_tool
from .package_skill import package_skill_tool

__all__ = [
    "init_skill_tool",
    "validate_skill_tool",
    "analyze_skill_tool",
    "refactor_skill_tool",
    "package_skill_tool",
]
```

**`src/skill_creator_mcp/tools/init_skill.py`**（完整实现）：
```python
"""初始化技能工具."""

import asyncio
from pathlib import Path
from typing import Dict, Any

from fastmcp import Context
from jinja2 import Environment, FileSystemLoader

from ..models.skill_config import InitSkillInput, SkillTemplateType
from ..utils.validators import validate_skill_name
from ..utils.file_ops import create_directory_structure_async
from ..utils.templates import TEMPLATES_DIR


async def init_skill_tool(
    ctx: Context,
    name: str,
    template: str = "minimal",
    output_dir: str = ".",
    with_scripts: bool = False,
    with_examples: bool = False,
) -> Dict[str, Any]:
    """
    初始化新的 Agent-Skill

    创建符合规范的技能目录结构和模板文件。

    Args:
        ctx: MCP 上下文
        name: 技能名称
        template: 模板类型
        output_dir: 输出目录
        with_scripts: 是否包含示例脚本
        with_examples: 是否包含使用示例

    Returns:
        包含创建结果的字典
    """
    try:
        # 验证技能名称
        validate_skill_name(name)

        # 创建目录结构
        skill_dir = await create_directory_structure_async(
            name=name,
            template_type=template,
            output_dir=Path(output_dir),
        )

        # 渲染 SKILL.md
        await _render_skill_md(
            skill_dir=skill_dir,
            name=name,
            template_type=template,
        )

        # 创建引用文件
        if template != "minimal":
            await _create_reference_files(
                skill_dir=skill_dir,
                template_type=template,
            )

        # 创建示例脚本
        if with_scripts:
            await _create_example_scripts(skill_dir)

        # 创建使用示例
        if with_examples:
            await _create_example_examples(skill_dir, name)

        return {
            "success": True,
            "skill_path": str(skill_dir),
            "skill_name": name,
            "template": template,
            "message": f"✅ 技能 '{name}' 已创建在：{skill_dir}",
            "next_steps": [
                f"1. 编辑 {skill_dir / 'SKILL.md'} 完善技能描述",
                f"2. 编辑 {skill_dir / 'references/'} 中的引用文件",
                f"3. 运行验证：python scripts/validate_skill.py {skill_dir}",
            ],
        }

    except ValueError as e:
        return {
            "success": False,
            "error": str(e),
            "error_type": "validation_error",
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "error_type": "internal_error",
        }


async def _render_skill_md(
    skill_dir: Path,
    name: str,
    template_type: str,
) -> None:
    """渲染 SKILL.md 文件。"""
    env = Environment(
        loader=FileSystemLoader(TEMPLATES_DIR),
        autoescape=False,
    )

    template = env.get_template(f"{template_type}/SKILL.md.tmpl")

    skill_title = name.replace("-", " ").replace("_", " ").title()

    content = await asyncio.to_thread(
        template.render,
        skill_name=name,
        skill_title=skill_title,
    )

    (skill_dir / "SKILL.md").write_text(content, encoding="utf-8")


async def _create_reference_files(
    skill_dir: Path,
    template_type: str,
) -> None:
    """创建引用文件。"""
    # 根据模板类型创建相应的引用文件
    ref_mapping = {
        "tool-based": ["tool-integration.md", "usage-examples.md"],
        "workflow-based": ["workflow-steps.md", "decision-points.md"],
        "analyzer-based": ["analysis-methods.md", "metrics.md"],
    }

    refs = ref_mapping.get(template_type, [])
    refs_dir = skill_dir / "references"
    refs_dir.mkdir(exist_ok=True)

    for ref_file in refs:
        ref_path = refs_dir / ref_file
        # 创建空文件或复制模板
        ref_path.write_text(
            f"# {ref_file.replace('-', ' ').replace('.md', '').title()}\n\n"
            f"TODO: 添加内容\n",
            encoding="utf-8",
        )


async def _create_example_scripts(skill_dir: Path) -> None:
    """创建示例脚本。"""
    scripts_dir = skill_dir / "scripts"
    scripts_dir.mkdir(exist_ok=True)

    script_content = '''#!/usr/bin/env python3
"""
示例脚本

Usage:
    python scripts/helper.py --help
"""

import argparse
import sys


def main():
    parser = argparse.ArgumentParser(description="示例脚本")
    parser.add_argument("--option", help="选项")
    args = parser.parse_args()

    # 实现脚本逻辑
    print(f"执行示例脚本，选项: {args.option}")


if __name__ == "__main__":
    main()
'''

    script_path = scripts_dir / "helper.py"
    script_path.write_text(script_content, encoding="utf-8")
    script_path.chmod(0o755)


async def _create_example_examples(skill_dir: Path, name: str) -> None:
    """创建使用示例。"""
    examples_dir = skill_dir / "examples"
    examples_dir.mkdir(exist_ok=True)

    example_content = f'''# {name} 使用示例

## 示例 1：基本用法

描述基本使用方法。

## 示例 2：高级用法

描述高级使用方法。
'''

    (examples_dir / "basic-usage.md").write_text(
        example_content,
        encoding="utf-8",
    )
```

### 11.4 测试实现

**`tests/conftest.py`**：
```python
"""pytest 配置."""

import pytest
from pathlib import Path
import tempfile
import shutil


@pytest.fixture
def temp_dir():
    """临时目录 fixture。"""
    temp = tempfile.mkdtemp()
    yield Path(temp)
    shutil.rmtree(temp)


@pytest.fixture
def sample_skill_dir(temp_dir):
    """示例技能目录 fixture。"""
    skill_dir = temp_dir / "sample-skill"
    skill_dir.mkdir()

    # 创建 SKILL.md
    (skill_dir / "SKILL.md").write_text("""---
name: sample-skill
description: |
  示例技能。用于测试。

  何时使用：测试
  触发词：测试
---

# Sample Skill

示例技能内容。
""")

    # 创建 references 目录
    refs_dir = skill_dir / "references"
    refs_dir.mkdir()
    (refs_dir / "advanced.md").write_text("# 高级用法\n\n详细内容...")

    return skill_dir
```

**`tests/test_tools/test_init_skill.py`**：
```python
"""测试 init_skill 工具。"""

import pytest
from pathlib import Path

from skill_creator_mcp.tools.init_skill import init_skill_tool


@pytest.mark.asyncio
async def test_init_skill_success(temp_dir):
    """测试成功初始化技能。"""
    result = await init_skill_tool(
        ctx=None,
        name="test-skill",
        template="minimal",
        output_dir=str(temp_dir),
    )

    assert result["success"] is True
    assert "test-skill" in result["skill_path"]

    skill_dir = Path(result["skill_path"])
    assert skill_dir.exists()
    assert (skill_dir / "SKILL.md").exists()
    assert (skill_dir / "references").exists()
    assert (skill_dir / "scripts").exists()


@pytest.mark.asyncio
async def test_init_skill_invalid_name(temp_dir):
    """测试无效技能名称。"""
    result = await init_skill_tool(
        ctx=None,
        name="Invalid_Name",  # 包含大写
        template="minimal",
        output_dir=str(temp_dir),
    )

    assert result["success"] is False
    assert result["error_type"] == "validation_error"


@pytest.mark.asyncio
async def test_init_skill_with_scripts(temp_dir):
    """测试创建包含脚本的技能。"""
    result = await init_skill_tool(
        ctx=None,
        name="test-skill",
        template="tool-based",
        output_dir=str(temp_dir),
        with_scripts=True,
    )

    assert result["success"] is True

    skill_dir = Path(result["skill_path"])
    scripts_dir = skill_dir / "scripts"
    assert scripts_dir.exists()
    assert (scripts_dir / "helper.py").exists()
```

---

## 十二、完整验证清单

### 12.1 MCP Server 验证清单

| 检查项 | 标准 | 验证方式 |
|--------|------|---------|
| 服务器启动 | STDIO 能正常启动 | `uv run python -m skill_creator_mcp` |
| 工具发现 | 所有工具可通过 tools/list 发现 | MCP Inspector |
| 工具调用 | 所有工具可正常调用 | 单元测试 |
| 资源发现 | 所有资源可通过 resources/list 发现 | MCP Inspector |
| 资源读取 | 所有资源可正常读取 | 单元测试 |
| 提示发现 | 所有提示可通过 prompts/list 发现 | MCP Inspector |
| 提示调用 | 所有提示可正常调用 | 单元测试 |
| 错误处理 | 所有异常都有适当处理 | 集成测试 |
| 类型检查 | 通过 mypy 检查 | `uv run mypy src/` |
| 代码规范 | 通过 ruff 检查 | `uv run ruff check .` |
| 测试覆盖 | 覆盖率 > 80% | `uv run pytest --cov` |

### 12.2 Agent-Skill 验证清单

| 检查项 | 标准 | 验证方式 |
|--------|------|---------|
| SKILL.md 行数 | ≤150行 | `wc -l SKILL.md` |
| 描述完整性 | 功能+场景+触发词 | 人工检查 |
| YAML 格式 | 正确解析 | `yamllint SKILL.md` |
| 引用文件 | 独立可读 | 人工检查 |
| MCP 工具引用 | 正确引用 MCP 工具 | 人工检查 |
| 自洽性 | 自身符合最佳实践 | 使用自身验证 |

### 12.3 集成验证清单

| 检查项 | 标准 | 验证方式 |
|--------|------|---------|
| Claude Code 集成 | MCP Server 可被 Claude Code 调用 | 配置并测试 |
| 端到端流程 | 完整的创建-验证-发布流程 | 手动测试 |
| Token 效率 | 首次加载 <1500 tokens | 分析工具 |
| 文档完整性 | 所有文档完整清晰 | 人工检查 |

---

## 十三、部署指南

### 13.1 本地开发部署

```bash
# 1. 克隆仓库
git clone https://github.com/yourusername/skill-creator-mcp
cd skill-creator-mcp

# 2. 安装依赖
uv sync --dev

# 3. 配置 Claude Code
# 编辑 ~/.config/Claude/claude_desktop_config.json
# 添加 MCP Server 配置

# 4. 启动 Claude Code
# Claude Code 将自动连接到 MCP Server
```

### 13.2 Docker 部署

```bash
# 1. 构建镜像
docker build -t skill-creator-mcp .

# 2. 运行容器
docker run -d \
  --name skill-creator-mcp \
  -p 8000:8000 \
  -v $(pwd)/workspace:/workspace \
  skill-creator-mcp

# 3. 配置 Claude Code 使用 SSE 端点
# http://localhost:8000/sse
```

### 13.3 远程服务器部署

```bash
# 1. 部署到服务器
ssh user@server
git clone https://github.com/yourusername/skill-creator-mcp
cd skill-creator-mcp
uv sync --no-dev

# 2. 使用 systemd 管理服务
sudo cp skill-creator-mcp.service /etc/systemd/system/
sudo systemctl enable skill-creator-mcp
sudo systemctl start skill-creator-mcp
```

---

## 十四、故障排查

### 14.1 常见问题

**Q: MCP Server 无法启动**

A: 检查：
1. Python 版本是否 >= 3.10
2. 依赖是否正确安装
3. 端口是否被占用

**Q: 工具调用失败**

A: 检查：
1. 工具参数是否正确
2. 文件权限是否正确
3. 日志输出

**Q: Claude Code 无法连接 MCP Server**

A: 检查：
1. 配置文件路径是否正确
2. 命令路径是否正确
3. MCP Server 是否正常运行
