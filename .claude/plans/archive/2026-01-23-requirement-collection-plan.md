# 需求澄清功能开发计划

> **创建日期**: 2026-01-23
> **状态**: planning
> **优先级**: P1
> **方案**: 方案 C - MCP Tool + Session State + AI 对话引导

---

## 用户期望

基于需求澄清，用户对功能的期望为：

### 核心期望
1. **AI 对话引导**：真正的动态对话，能根据用户回答智能调整问题
2. **优先级排序**：需求完整性 > 架构示范 > 对话体验 > 新手友好
3. **实施策略**：技术验证优先（先确认可行性再决定范围）

### 功能定位
- **不是**简单的结构化问卷（预定义问题列表）
- **而是**真正的 AI 驱动的对话引导系统
- **利用** FastMCP 的 LLM Sampling (`ctx.sample()`) 和 User Elicitation (`ctx.elicit()`) 能力

---

## 目标

在现有 `skills-creator` 项目基础上，添加一个**AI 驱动的需求澄清/头脑风暴**前置功能模块：

### 核心能力
1. **AI 对话引导**：利用 LLM 动态生成引导问题
2. **需求完整性保障**：确保收集到创建技能所需的所有关键信息
3. **架构示范**：作为 MCP + Agent-Skill 混合架构的最佳实践参考
4. **会话状态管理**：支持会话恢复和进度追踪
5. **智能模板推荐**：基于用户描述推荐合适的模板类型

### 实现方式
- **不是**预定义的问题列表（传统问卷）
- **而是**利用 `ctx.sample()` 让 LLM 动态生成引导问题
- **结合** `ctx.elicit()` 收集结构化用户输入
- **使用** session state 保存对话历史和收集进度

---

## 范围

### 包含内容
1. **MCP Server 侧**
   - 新增 `collect_requirements` Tool（支持 session state）
   - 新增数据模型（RequirementCollectionInput, RequirementCollectionResult）
   - 新增验证工具（_validate_answer）

2. **Agent-Skill 侧**
   - 更新 SKILL.md 添加需求澄清流程
   - 创建 `requirement-collection.md` 引用文档
   - 添加需求收集示例到 `examples/`

3. **测试**
   - 单元测试（验证逻辑）
   - 集成测试（session state 行为）
   - 端到端测试（完整流程）

### 不包含内容
- Redis 等外部存储后端（使用默认内存存储）
- 需求历史记录功能
- 多人协作需求收集

---

## 技术依赖

### 现有技术栈
- FastMCP SDK ≥ 0.11.0
- Pydantic 2.0+
- Python 3.10+

### 新增依赖
- 无（使用 FastMCP 内置 session state）

---

## 技术验证方案 (Phase 0)

### 验证目标

在正式实现前，先验证关键技术点是否可行，确保方案能够交付预期价值。

### 验证内容

#### 验证点 1: LLM Sampling 能力验证
**目的**: 确认 MCP Server 可以通过 `ctx.sample()` 调用客户端 LLM

**验证步骤**:
1. 创建一个简单的测试工具 `test_llm_sampling`
2. 在工具中调用 `ctx.sample()` 请求 LLM 生成文本
3. 验证返回结果是否包含预期的响应

**预期结果**:
- `ctx.sample()` 能够成功调用客户端 LLM
- 返回包含 `text` 和 `history` 的 `SamplingResult` 对象
- 支持传入 `system_prompt` 控制生成行为

**代码示例**:
```python
@mcp.tool()
async def test_llm_sampling(ctx: Context, prompt: str) -> str:
    """测试 LLM Sampling 能力."""
    result = await ctx.sample(
        messages=prompt,
        system_prompt="You are a helpful assistant for skill creation.",
        temperature=0.7,
    )
    return result.text or "No response"
```

#### 验证点 2: User Elicitation 能力验证
**目的**: 确认可以通过 `ctx.elicit()` 请求用户输入结构化数据

**验证步骤**:
1. 创建测试工具 `test_user_elicitation`
2. 在工具中调用 `ctx.elicit()` 请求用户输入
3. 验证用户响应的格式和内容

**预期结果**:
- `ctx.elicit()` 能够暂停工具执行并等待用户输入
- 返回包含用户输入的 `ElicitationResult` 对象
- 支持 `response_type` 参数指定输入类型

**代码示例**:
```python
@mcp.tool()
async def test_elicitation(ctx: Context) -> dict:
    """测试用户征询能力."""
    result = await ctx.elicit(
        "请提供技能名称（小写字母、数字、连字符）",
        response_type=str,
    )
    if result.action == "accept":
        return {"user_input": result.data}
    return {"status": "cancelled"}
```

#### 验证点 3: Session State + LLM 结合验证
**目的**: 确认可以在对话循环中使用 session state 保存历史

**验证步骤**:
1. 创建测试工具 `test_conversation_loop`
2. 在多轮对话中保存和读取 session state
3. 验证 LLM 可以访问历史对话上下文

**预期结果**:
- `ctx.set_state()` 和 `ctx.get_state()` 能够正常工作
- LLM 可以利用对话历史生成更连贯的响应
- 支持会话中断后恢复

**代码示例**:
```python
@mcp.tool()
async def test_conversation_loop(ctx: Context, user_input: str) -> str:
    """测试对话循环和状态管理."""
    # 获取历史对话
    history = await ctx.get_state("conversation_history") or []

    # 添加用户输入
    history.append({"role": "user", "content": user_input})

    # 调用 LLM 生成响应
    result = await ctx.sample(
        messages=history,
        system_prompt="You are a skill creation consultant.",
    )

    # 添加 AI 响应
    history.append({"role": "assistant", "content": result.text})

    # 保存历史
    await ctx.set_state("conversation_history", history)

    return result.text or "No response"
```

#### 验证点 4: 需求完整性验证
**目的**: 确认 LLM 能够判断需求是否完整

**验证步骤**:
1. 创建测试工具 `test_requirement_completeness`
2. 传入不同的需求描述（完整/不完整）
3. 让 LLM 判断是否缺少关键信息

**预期结果**:
- LLM 能够识别缺少的关键信息
- 返回缺失信息列表
- 提供具体的补充建议

**代码示例**:
```python
@mcp.tool()
async def test_requirement_completeness(ctx: Context, requirement: str) -> dict:
    """测试需求完整性检查."""
    prompt = f"""
    分析以下技能创建需求，判断是否包含所有必要信息：
    {requirement}

    必要信息包括：
    1. 技能名称（skill_name）
    2. 主要功能（skill_function）
    3. 使用场景（use_cases）
    4. 模板类型（template_type）

    请返回 JSON 格式，包含：
    - is_complete: bool
    - missing_info: list[str]
    - suggestions: list[str]
    """

    result = await ctx.sample(
        messages=prompt,
        result_type=dict,  # 请求结构化输出
    )

    return result.result or {}
```

### 验证结果评估

| 验证点 | 通过标准 | 失败应对 |
|--------|----------|----------|
| LLM Sampling | 能成功调用并获取响应 | 降级到结构化问卷方案 |
| User Elicitation | 能正确收集用户输入 | 使用传统参数传递 |
| Session State + LLM | 状态正常读写和恢复 | 简化为无状态模式 |
| 需求完整性 | 能准确判断缺失信息 | 固定检查列表 |

### 验证时间估算

| 验证点 | 预估时间 |
|--------|----------|
| 验证点 1: LLM Sampling | 0.5 天 |
| 验证点 2: User Elicitation | 0.5 天 |
| 验证点 3: Session State + LLM | 1 天 |
| 验证点 4: 需求完整性 | 0.5 天 |
| **总计** | **2-3 天** |

---

## 任务清单

### Phase 0: 技术验证 (P0 - 必须完成)
- [ ] 0.1 创建测试工具
  - [ ] test_llm_sampling
  - [ ] test_user_elicitation
  - [ ] test_conversation_loop
  - [ ] test_requirement_completeness
- [ ] 0.2 运行验证测试
  - [ ] 在 Claude Code 中测试每个工具
  - [ ] 记录测试结果
  - [ ] 评估可行性
- [ ] 0.3 决策
  - [ ] 如果所有验证点通过 → 进入 Phase 1
  - [ ] 如果部分失败 → 调整方案或降级

### Phase 1: MCP Server 实现 (P0)
- [ ] 1.1 添加数据模型到 `models/skill_config.py`
  - [ ] RequirementCollectionInput
  - [ ] RequirementCollectionResult
  - [ ] ValidationRule
  - [ ] RequirementStep
- [ ] 1.2 实现 `collect_requirements` Tool
  - [ ] 定义需求收集步骤（REQUIREMENT_STEPS）
  - [ ] 实现 action 处理逻辑（start/next/previous/status/complete）
  - [ ] 实现 session state 读写（ctx.set_state/get_state）
  - [ ] 实现答案验证（_validate_answer）
- [ ] 1.3 添加辅助函数
  - [ ] _validate_answer（验证用户答案）
  - [ ] _get_next_step（获取下一个步骤）
  - [ ] _calculate_progress（计算进度百分比）

### Phase 2: Agent-Skill 更新 (P0)
- [ ] 2.1 更新 `SKILL.md`
  - [ ] 添加需求澄清流程章节
  - [ ] 更新核心能力列表
  - [ ] 更新工作流程图
- [ ] 2.2 创建引用文档
  - [ ] `references/requirement-collection.md`（需求收集指南）
  - [ ] `references/brainstorming-techniques.md`（头脑风暴技巧）
- [ ] 2.3 添加示例
  - [ ] `examples/requirement-collection-basic.md`（基础需求收集）
  - [ ] `examples/require-collection-brainstorm.md`（头脑风暴模式）

### Phase 3: 测试 (P0)
- [ ] 3.1 单元测试
  - [ ] 测试验证逻辑（_validate_answer）
  - [ ] 测试进度计算
  - [ ] 测试步骤导航
- [ ] 3.2 集成测试
  - [ ] 测试 session state 读写
  - [ ] 测试 session 隔离性
  - [ ] 测试 state 过期机制
- [ ] 3.3 端到端测试
  - [ ] 测试完整需求收集流程
  - [ ] 测试会话恢复
  - [ ] 测试与 init_skill 的集成

### Phase 4: 文档和优化 (P1)
- [ ] 4.1 更新 MCP Server README
  - [ ] 添加 collect_requirements 工具说明
  - [ ] 添加 session state 说明
- [ ] 4.2 更新 CHANGELOG.md
- [ ] 4.3 代码审查和质量检查
  - [ ] ruff check
  - [ ] mypy type check
  - [ ] bandit security check

---

## 验收标准

- [ ] `collect_requirements` Tool 正常工作
- [ ] 支持 4 种模式（基础/完整/头脑风暴/渐进式）
- [ ] Session state 正确保存和读取
- [ ] 支持会话恢复（中断后继续）
- [ ] 所有测试通过（覆盖率 ≥80%）
- [ ] 代码质量检查通过（ruff + mypy）
- [ ] 文档完整更新

---

## 风险评估

| 风险 | 影响 | 缓解措施 |
|------|------|----------|
| Session state 不可用 | 高 | 在启动时检查 FastMCP 版本（≥3.0） |
| 并发场景下的状态冲突 | 中 | Session 自动隔离，不同 session 互不影响 |
| State 泄漏导致内存问题 | 低 | State 1 天自动过期 |
| 客户端不支持 session | 中 | 降级到无状态模式（提示用户一次性提供所有信息） |

---

## 实现细节

### Session State 结构

```python
{
    "current_step_index": 0,        # 当前步骤索引
    "answers": {                    # 已收集的答案
        "skill_name": "pdf-processor",
        "template": "tool-based",
    },
    "started_at": "2026-01-23T10:00:00Z",
    "completed": False,
    "mode": "basic",                # basic/complete/brainstorm/progressive
}
```

### 需求收集步骤

#### 基础模式（5 步）
1. `skill_name` - 技能名称（必填）
2. `skill_function` - 主要功能（必填）
3. `use_cases` - 使用场景（必填，至少 2 个）
4. `template_type` - 模板类型（必填）
5. `additional_features` - 额外需求（可选）

#### 完整模式（10 步）
包含基础模式的 5 步，外加：
6. `target_users` - 目标用户
7. `tech_stack` - 技术栈偏好
8. `dependencies` - 外部依赖
9. `testing_requirements` - 测试要求
10. `documentation_level` - 文档级别

---

## 关键文件路径

### MCP Server 侧
- `skill-creator-mcp/src/skill_creator_mcp/server.py` - 添加 collect_requirements Tool
- `skill-creator-mcp/src/skill_creator_mcp/models/skill_config.py` - 添加数据模型
- `skill-creator-mcp/tests/test_tools/test_collect_requirements.py` - 测试文件

### Agent-Skill 侧
- `skill-creator/SKILL.md` - 更新工作流程
- `skill-creator/references/requirement-collection.md` - 新增引用文档
- `skill-creator/examples/requirement-collection-basic.md` - 新增示例

---

## 参考资料

### 外部资源
- [FastMCP Context 文档](https://gofastmcp.com/servers/context) - Session state 管理
- [Agentic AI Design Patterns 2026](https://medium.com/@dewasheesh.rana/agentic-ai-design-patterns-2026-ed-e3a5125162c5) - 对话模式
- [Microsoft Research Agentic AI](https://www.microsoft.com/en-us/research/articles/agentic-ai-reimagining-future-human-agent-communication-and-collaboration/) - 人机协作
- [Brainstorming & Design Architect Skill](https://mcpmarket.com/zh/tools/skills/brainstorming-design-architect-4) - 头脑风暴实践

### 内部文档
- `CLAUDE.md` - 项目开发指南
- `ARCHITECTURE_AUDIT_REPORT_v2.md` - 架构审计报告
- `skill-creator/SKILL.md` - Agent-Skill 入口

---

## 时间估算

| 阶段 | 预估时间 | 说明 |
|------|----------|------|
| Phase 0: 技术验证 | 2-3 天 | 验证 LLM Sampling、Elicitation、Session State |
| Phase 1: MCP Server 实现 | 2-3 天 | collect_requirements Tool 实现 |
| Phase 2: Agent-Skill 更新 | 1-2 天 | SKILL.md 和引用文档更新 |
| Phase 3: 测试 | 2-3 天 | 单元测试、集成测试、端到端测试 |
| Phase 4: 文档和优化 | 1 天 | README 更新、CHANGELOG |
| **总计** | **8-12 天** | 含技术验证阶段 |

---

## 参考资料

### 外部资源
#### FastMCP 核心功能
- [FastMCP Context 文档](https://gofastmcp.com/servers/context) - Session state 管理
- [FastMCP Sampling 文档](https://gofastmcp.com/servers/sampling) - LLM Sampling 完整指南
- [O'Reilly: MCP Sampling - When Your Tools Need to Think](https://www.oreilly.com/radar/mcp-sampling-when-your-tools-need-to-think/) - LLM Sampling 深度解析
- [中文博客: MCP Sampling 示例](https://www.cnblogs.com/XY-Heruo/p/19093219) - 详细的代码示例
- [中文博客: MCP Elicitation 示例](https://www.cnblogs.com/XY-Heruo/p/19094012) - User Elicitation 实践

#### 架构和设计模式
- [Agentic AI Design Patterns 2026](https://medium.com/@dewasheesh.rana/agentic-ai-design-patterns-2026-ed-e3a5125162c5) - 对话模式和多轮交互
- [Microsoft Research Agentic AI](https://www.microsoft.com/en-us/research/articles/agentic-ai-reimagining-future-human-agent-communication-and-collaboration/) - 人机协作最佳实践

### 内部文档
- `CLAUDE.md` - 项目开发指南
- `ARCHITECTURE_AUDIT_REPORT_v2.md` - 架构审计报告
- `skill-creator/SKILL.md` - Agent-Skill 入口
