# ADR 001: MCP Server + Agent-Skill 混合架构

## 状态

已接受 (2026-01-22)
**更新** (2026-01-28) - 架构边界彻底重构完成

## 上下文

Skills-Creator 项目需要提供 Agent-Skills 开发与质量保证能力。在架构设计时面临以下选择：

1. **纯 MCP Server 架构** - 仅提供 MCP 工具和资源
2. **纯 Agent-Skill 架构** - 仅提供 Agent-Skill，直接执行文件操作
3. **混合架构** - MCP Server 提供原子操作，Agent-Skill 编排工作流

### 纯 MCP Server 架构的问题

- ❌ 无法传递最佳实践知识
- ❌ 无法实现渐进式披露
- ❌ 工作流逻辑需要用户手动编排

### 纯 Agent-Skill 架构的问题

- ❌ 每次激活加载大量代码到上下文
- ❌ 难以独立测试和复用
- ❌ 不符合 MCP 生态最佳实践

## 决策

采用 **混合架构**：MCP Server + Agent-Skill

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
│  │  - 原子操作工具 (5 Tools)                              │ │
│  │  - 只读资源 (4 Resources)                              │ │
│  │  - 可重用模板 (3 Prompts)                              │ │
│  └─────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────┘
```

### 职责边界

| 组件 | 职责 | 边界 |
|------|------|------|
| **MCP Server** | - 执行原子操作<br>- 处理文件 I/O<br>- 数据验证 | - 不包含工作流逻辑<br>- 不传递业务知识 |
| **Agent-Skill** | - 编排工作流程<br>- 传递最佳实践<br>- 渐进式披露 | - 不直接执行文件 I/O<br>- 不重复实现工具功能 |

## 理由

### 优势

1. **职责分离**
   - MCP Server 专注于可执行的原子操作
   - Agent-Skill 专注于工作流编排和知识传递
   - 两者可独立开发、测试、部署

2. **可复用性**
   - MCP Server 可被其他 Agent-Skill 或直接使用
   - Agent-Skill 可切换到不同的 MCP 实现
   - 工具和资源可被其他项目复用

3. **Token 效率**
   - Agent-Skill 保持轻量 (SKILL.md ≤150行)
   - MCP Server 代码不加载到上下文
   - 引用文件按需加载

4. **符合 MCP 生态**
   - 遵循 MCP 协议标准
   - 可被 MCP Inspector 测试
   - 可集成到 Claude Desktop

5. **测试友好**
   - MCP Server 可独立测试 (99% 覆盖率, 307个测试)
   - Agent-Skill 可单独验证
   - 工具和资源可被 CI/CD 集成

### 权衡

| 方面 | 优势 | 劣势 | 缓解措施 |
|------|------|------|----------|
| 复杂度 | 职责清晰 | 需维护两套代码 | 清晰的接口定义 |
| 部署 | MCP Server 可独立升级 | 需同时部署两组件 | 版本兼容性管理 |
| 学习曲线 | 符合 MCP 标准 | 新概念较多 | 提供完整文档 |

## 实现细节

### MCP Server 组件

```python
# skill-creator-mcp/src/skill_creator_mcp/server.py

@mcp.tool()
async def init_skill(
    ctx: Context,
    name: str,
    template: str = "minimal",
    output_dir: str = ".",
) -> dict[str, Any]:
    """
    初始化新的 Agent-Skill.

    原子操作: 创建目录结构、生成模板文件。
    """
    # 1. 参数验证 (Pydantic)
    # 2. 创建目录结构
    # 3. 生成 SKILL.md
    # 4. 返回结构化结果
    pass
```

**工具列表**:
- `init_skill` - 初始化技能结构
- `validate_skill` - 验证技能规范
- `analyze_skill` - 分析技能质量
- `refactor_skill` - 生成重构建议
- `package_skill` - 打包技能分发

**资源列表**:
- `http://skills/schema/templates` - 模板列表
- `http://skills/schema/templates/{type}` - 特定模板内容
- `http://skills/schema/best-practices` - 最佳实践指南
- `http://skills/schema/validation-rules` - 验证规则详情

### Agent-Skill 组件

```yaml
---
name: skill-creator
description: |
  Agent-Skills 开发与质量保证工具。

  触发词：
  - 技能创建
  - 技能验证
  - 技能分析
allowed-tools: Read, Write, Edit, Bash, Glob, Grep
mcp_servers: ["skill-creator"]
---

# Skill-Creator - Agent-Skills 开发工具

## 工作流程
初始化 → 选择模板 → 生成结构 → 开发内容 → 验证规范 → 分析优化

## MCP 工具集成
| 工具 | 功能 |
|------|------|
| `init_skill` | 初始化新技能结构 |
| `validate_skill` | 验证技能规范 |
...
```

**工作流编排**:
1. 理解用户意图
2. 调用相应的 MCP 工具
3. 解读工具返回结果
4. 结合最佳实践知识
5. 提供可执行建议

## 结果

### 测试覆盖率

| 组件 | 覆盖率 | 测试数 |
|------|--------|--------|
| MCP Server | 98% | 297 |
| Agent-Skill | 100% | 文档验证 |

### 代码质量

| 检查项 | 结果 |
|--------|------|
| Ruff | 0 错误 ✅ |
| Mypy | 0 错误 ✅ |
| Bandit | 0 高危 ✅ |

### 文档完整性

| 文档 | 行数 | 状态 |
|------|------|------|
| SKILL.md | 111 | ✅ ≤150 |
| best-practices-core.md | 206 | ✅ ≤300 |
| best-practices-advanced.md | 232 | ✅ ≤300 |
| mcp-integration.md | 281 | ✅ ≤300 |

## 影响

### 正面影响

1. **开发效率**: 用户通过 Agent-Skill 快速完成技能开发
2. **代码质量**: MCP Server 提供可靠的原子操作
3. **可维护性**: 职责分离使代码易于维护
4. **可扩展性**: 架构支持未来添加新工具和资源

### 需要注意

1. **版本同步**: MCP Server 和 Agent-Skill 需保持版本兼容
2. **文档更新**: 新增工具时需同步更新 Agent-Skill 文档
3. **测试覆盖**: 两者都需要独立的测试覆盖

## 替代方案 (未采纳)

### 方案 A: 纯 MCP Server

**未采纳原因**:
- 无法传递渐进式披露知识
- 无法编排复杂工作流
- 用户体验较差

### 方案 B: 纯 Agent-Skill

**未采纳原因**:
- 首次加载 Token 过多
- 工具难以复用
- 不符合 MCP 生态标准

## 参考

- [MCP 协议规范](https://modelcontextprotocol.io/)
- [FastMCP 文档](https://jlowin.github.io/fastmcp/)
- [协同示例文档](../../skill-creator/examples/mcp-skill-collaboration.md)
- [MCP 集成指南](../../skill-creator/references/mcp-integration.md)

---

## 架构演进历史

### v0.3.3 架构重构 (2026-01-28)

**问题**: `collect_requirements` 工具违反职责边界
- 包含工作流逻辑（action处理、循环控制）
- 包含业务知识（Prompt模板、验证规则）
- 总计约1498行相关代码

**解决方案**: 彻底拆分为原子操作工具
- **删除**: `requirement_tools.py` (185行), `actions.py` (181行), `elicit_workflow.py` (440行)
- **新增**: 7个原子工具（会话管理3个、问题获取2个、验证2个）
- **简化**: `validation.py` (309→85行), `llm_services.py` (268→89行), `session_manager.py` (125→47行), `questions.py` (116→72行)

**成果**:
- 代码减少: ~1683行 → ~560行
- 符合 ADR 001: MCP只提供原子操作，Agent-Skill编排工作流
- 测试覆盖率保持: 478 passed (≥95%)
- 相关计划: [magical-kindling-raccoon.md](../../.claude/plans/magical-kindling-raccoon.md)

**新旧对比**:

| 变更项 | 旧规范 | 新规范 |
|--------|--------|--------|
| **需求收集API** | `collect_requirements(action, mode, session_id, ...)` | 7个原子工具 |
| **工作流编排** | MCP Server包含完整工作流逻辑 | Agent-Skill编排工作流 |
| **Session管理** | SessionStateManager封装所有操作 | 简化为CRUD原子操作 |
| **Prompt工程** | MCP Server包含Prompt模板 | Agent-Skill提供Prompt知识 |
| **代码量** | ~1683行（requirement相关） | ~560行（MCP原子工具 + Agent-Skill工作流） |

**新增文档**:
- [需求收集工作流指南](../../skill-creator/references/requirement-workflow.md)
- Agent-Skill SKILL.md 更新（工作流编排章节）
