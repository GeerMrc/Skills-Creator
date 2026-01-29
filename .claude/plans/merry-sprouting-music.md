# MCP Server 全面优化与重构计划

> **计划ID**: merry-sprouting-music
> **创建日期**: 2026-01-29
> **状态**: planning
> **负责人**: Claude
> **版本**: v1.0.0

---

## 执行摘要

基于对 `skill-creator-mcp/` MCP Server 的全面审核，本计划针对发现的代码质量问题、一致性问题和文档差距进行优化和重构。同时确保符合 MCP 最佳实践，并回归项目核心定位。

### 当前状态评估

| 维度 | 评分 | 说明 |
|------|------|------|
| **架构质量** | ⭐⭐⭐⭐⭐ (5/5) | 严格遵循ADR 001原则，职责分离清晰 |
| **功能完整性** | ⭐⭐⭐⭐⭐ (5/5) | 18个工具、4个资源、3个Prompts全部实现 |
| **代码质量** | ⭐⭐⭐⭐ (4/5) | 存在重复代码和一致性问题 |
| **核心定位一致性** | ⭐⭐⭐⭐⭐ (5/5) | 所有工具服务于Agent-Skills标准化开发 |
| **测试覆盖率** | ⭐⭐⭐⭐⭐ (95%) | 615个测试用例，代码质量检查全通过 |

### 核心问题总结

1. **代码重复**: analyze_skill和refactor_skill存在50+行重复分析逻辑
2. **注册方式不一致**: 技能工具使用`add_tool()`，其他工具使用`@mcp.tool()`装饰器
3. **资源缺少MIME类型**: 4个资源都未声明MIME类型
4. **文档不一致**: 测试数量声明为613，实际为615

---

## 问题清单与优先级

### P0 - 必须修复（4小时）

| ID | 问题 | 文件 | 工作量 | 影响 |
|----|------|------|--------|------|
| P0-1 | 消除analyze/refactor重复代码 | skill_tools.py | 2h | 代码可维护性 |
| P0-2 | 统一工具注册方式 | server.py | 1h | 代码一致性 |
| P0-3 | 添加资源MIME类型 | server.py | 30min | MCP规范符合度 |
| P0-4 | 更新测试数量文档 | README.md, CLAUDE.md, CHANGELOG.md | 5min | 文档一致性 |

### P1 - 重要改进（4.5小时）

| ID | 问题 | 文件 | 工作量 | 影响 |
|----|------|------|--------|------|
| P1-1 | 添加资源订阅机制 | server.py | 1h | MCP最佳实践 |
| P1-2 | 提升Prompt透明度 | prompts/*.py | 1h | 用户体验 |
| P1-3 | 区分打包工具文档 | README.md, docs/ | 30min | 文档清晰度 |
| P1-4 | 补充server.py测试 | tests/test_server.py | 2h | 测试覆盖率(77%→90%) |

### P2 - 可选优化（6.5小时）

| ID | 问题 | 文件 | 工作量 | 影响 |
|----|------|------|--------|------|
| P2-1 | 简化BatchContextAdapter | batch_operations.py | 1h | 代码简化 |
| P2-2 | 合并健康检查工具 | health_check.py | 1h | API精简 |
| P2-3 | 添加Resource Templates | server.py | 2h | 功能增强 |
| P2-4 | 添加进度追踪 | tools/*.py | 2.5h | 用户体验 |

---

## 重构方案详情

### P0-1: 消除analyze_skill和refactor_skill重复代码

**问题**:
- `analyze_skill` (第348-375行) 和 `refactor_skill` (第464-489行) 包含完全相同的分析逻辑
- 重复代码约50行

**解决方案**:
```python
# 在 skill_tools.py 中新增公共函数
async def _perform_analysis(
    skill_dir: Path,
    analyze_structure: bool,
    analyze_complexity: bool,
    analyze_quality: bool,
) -> tuple[StructureAnalysis, ComplexityMetrics, QualityScore]:
    """执行完整的技能分析（公共逻辑）."""
    # 1. 结构分析
    if analyze_structure:
        structure = await _analyze_structure(skill_dir)
    else:
        structure = StructureAnalysis(total_files=0, total_lines=0, file_breakdown={})

    # 2. 复杂度分析
    if analyze_complexity:
        complexity = await _analyze_complexity(skill_dir)
    else:
        complexity = ComplexityMetrics(...)

    # 3. 质量分析
    if analyze_quality:
        quality = await _analyze_quality(skill_dir)
    else:
        quality = QualityScore(...)

    return structure, complexity, quality

# analyze_skill 和 refactor_skill 都调用此函数
```

**影响文件**:
- `src/skill_creator_mcp/tools/skill_tools.py`

**测试要求**:
- 运行现有测试确保无回归
- `tests/test_tools/test_analyze_skill.py`
- `tests/test_tools/test_refactor_skill.py`

---

### P0-2: 统一工具注册方式

**问题**:
- 技能工具在`server.py`中使用`mcp.add_tool()`注册
- 其他工具在`server.py`中使用`@mcp.tool()`装饰器
- 代码风格不一致

**解决方案**:
```python
# 当前（server.py 第341-344行）
mcp.add_tool(init_skill)
mcp.add_tool(validate_skill)
mcp.add_tool(analyze_skill)
mcp.add_tool(refactor_skill)

# 修改为：在 skill_tools.py 中使用装饰器
@mcp.tool()
async def init_skill(...) -> dict[str, Any]:
    ...

# 然后在 server.py 中只需导入
from .tools.skill_tools import init_skill, validate_skill, analyze_skill, refactor_skill
```

**影响文件**:
- `src/skill_creator_mcp/server.py`
- `src/skill_creator_mcp/tools/skill_tools.py`

**测试要求**:
- 验证所有18个工具正确注册
- `pytest tests/test_mcp/ -v`

---

### P0-3: 添加资源MIME类型

**问题**:
- 4个资源函数都缺少MIME类型声明
- 不符合MCP官方最佳实践

**解决方案**:
```python
# 当前（server.py 第737-770行）
@mcp.resource("http://skills/schema/templates")
def list_templates_resource() -> str:
    ...

# 修改为
@mcp.resource("http://skills/schema/templates", mime_type="text/markdown")
def list_templates_resource() -> str:
    ...

# 同样处理其他3个资源
```

**影响文件**:
- `src/skill_creator_mcp/server.py`

**测试要求**:
- `pytest tests/test_resources/ -v`

---

### P0-4: 更新测试数量文档

**问题**:
- README.md: 613 → 615
- CLAUDE.md: 613 → 615 (2处)
- CHANGELOG.md: 601 → 615

**解决方案**:
```bash
# 批量替换
sed -i 's/613%20passed/615%20passed/g' README.md
sed -i 's/613 个测试/615 个测试/g' CLAUDE.md
sed -i 's/601 个测试用例/615 个测试用例/g' CHANGELOG.md
```

**影响文件**:
- `skill-creator-mcp/README.md`
- `CLAUDE.md`
- `CHANGELOG.md`

---

### P1-1: 添加资源订阅机制

**问题**:
- MCP官方标准支持`resources/subscribe`用于实时更新
- 当前实现缺少订阅机制

**解决方案**:
```python
# 在 server.py 中添加
@mcp.resource("http://skills/schema/templates", mime_type="text/markdown")
async def list_templates_resource() -> str:
    """列出所有可用的技能模板（支持订阅）."""
    return list_templates()

# 添加订阅支持（可选，根据需求）
```

**影响文件**:
- `src/skill_creator_mcp/server.py`

---

### P1-2: 提升Prompt透明度

**问题**:
- Prompt模板内容不够透明，用户看不到完整模板

**解决方案**:
```python
# 在 prompts/*.py 中添加文档字符串
def get_create_skill_prompt(name: str, template: str = "minimal") -> str:
    """
    创建新技能的 Prompt 模板。

    ## 完整模板内容
    {template_content}

    ## 参数说明
    - name: 技能名称
    - template: 模板类型
    """
    ...
```

**影响文件**:
- `src/skill_creator_mcp/prompts/create_skill.py`
- `src/skill_creator_mcp/prompts/validate_skill.py`
- `src/skill_creator_mcp/prompts/refactor_skill.py`

---

### P1-3: 区分打包工具文档

**问题**:
- `package_skill`和`package_agent_skill`功能相似，易混淆
- 文档需要更清晰地区分使用场景

**解决方案**:
在README.md中添加对比表格：

| 工具 | 使用场景 | 特点 |
|------|----------|------|
| `package_skill` | 通用打包 | 灵活排除选项，包含测试 |
| `package_agent_skill` | 标准打包（推荐） | 版本号支持，严格排除，默认不含测试 |

**影响文件**:
- `skill-creator-mcp/README.md`
- `docs/packaging.md`（新建或更新）

---

### P1-4: 补充server.py测试覆盖

**问题**:
- server.py覆盖率77%（42行未覆盖）
- 缺少中间件和HTTP端点测试

**解决方案**:
创建新文件 `tests/test_server.py`:
```python
import pytest
from fastmcp import FastMCP

def test_middleware_registration():
    """测试中间件注册."""

def test_http_health_endpoint():
    """测试/health端点."""

def test_http_metrics_endpoint():
    """测试/metrics端点."""

def test_lifespan_hooks():
    """测试生命周期钩子."""
```

**影响文件**:
- `skill-creator-mcp/tests/test_server.py`（新建）

---

## 实施时间表

### 阶段1: P0任务（必须修复）

| 任务 | 预计时间 | 依赖 | 顺序 |
|------|----------|------|------|
| P0-4: 更新文档 | 5分钟 | 无 | 1 |
| P0-3: 添加MIME类型 | 30分钟 | 无 | 2 |
| P0-2: 统一注册方式 | 1小时 | P0-3 | 3 |
| P0-1: 消除重复代码 | 2小时 | 无 | 4 |

### 阶段2: P1任务（重要改进）

| 任务 | 预计时间 | 依赖 | 顺序 |
|------|----------|------|------|
| P1-3: 打包工具文档 | 30分钟 | 无 | 1 |
| P1-1: 资源订阅 | 1小时 | P0-3 | 2 |
| P1-2: Prompt透明度 | 1小时 | 无 | 3 |
| P1-4: server.py测试 | 2小时 | P0-2 | 4 |

### 阶段3: P2任务（可选优化）

根据P0+P1完成后评估决定是否执行。

---

## 验收标准

### 功能完整性
- [ ] 所有18个MCP工具功能正常
- [ ] 所有4个Resources可访问
- [ ] 所有3个Prompts可使用
- [ ] 无功能退化

### 测试覆盖率
- [ ] 整体覆盖率 ≥ 95%
- [ ] server.py覆盖率 ≥ 90%（从77%提升）
- [ ] 所有新代码有对应测试

### 代码质量
- [ ] `ruff check .` - 0错误
- [ ] `mypy src/` - 0错误
- [ ] `bandit -r src/` - 0高危/中危
- [ ] `pytest --cov` - 全部通过

### 文档一致性
- [ ] README.md与代码一致
- [ ] CLAUDE.md与代码一致
- [ ] CHANGELOG.md更新
- [ ] 所有链接有效

### MCP最佳实践
- [ ] 资源有MIME类型声明
- [ ] 工具注册方式统一
- [ ] Prompt模板透明
- [ ] 代码无明显重复

---

## 风险评估

### 高风险（需要缓解）

| 风险 | 影响 | 概率 | 缓解措施 |
|------|------|------|----------|
| 工具注册方式变更导致现有集成失效 | 高 | 中 | 充分测试，保持向后兼容 |
| 代码重构引入新Bug | 高 | 低 | 完整测试套件，Code Review |

### 中风险

| 风险 | 影响 | 概率 | 缓解措施 |
|------|------|------|----------|
| MIME类型变更导致客户端解析问题 | 中 | 低 | 文档说明，渐进式迁移 |
| 测试覆盖提升过程中发现隐藏Bug | 中 | 中 | 及时修复，更新测试 |

### 低风险

| 风险 | 影响 | 概率 | 缓解措施 |
|------|------|------|----------|
| 文档更新遗漏 | 低 | 低 | 多人审核 |
| P2任务时间估算不准 | 低 | 中 | 可延期或拆分 |

---

## 关键文件清单

### 需要修改的文件

| 文件 | 修改类型 | 优先级 |
|------|----------|--------|
| `src/skill_creator_mcp/server.py` | 重构 | P0, P1 |
| `src/skill_creator_mcp/tools/skill_tools.py` | 重构 | P0 |
| `README.md` | 文档更新 | P0, P1 |
| `CLAUDE.md` | 文档更新 | P0 |
| `CHANGELOG.md` | 文档更新 | P0 |
| `tests/test_server.py` | 新建 | P1 |
| `prompts/*.py` | 文档增强 | P1 |

### 参考文件（只读）

| 文件 | 用途 |
|------|------|
| `tests/test_tools/test_analyze_skill.py` | 确保重构无回归 |
| `tests/test_tools/test_refactor_skill.py` | 确保重构无回归 |
| `tests/test_resources/` | 资源测试参考 |

---

## 核心定位一致性验证

**核心定位回顾**:
> 为用户进行 Agent-Skills 高效/规范/最佳实践标准化开发

**一致性检查**:

| 任务 | 服务于核心定位 | 说明 |
|------|---------------|------|
| P0-1: 消除重复代码 | ✅ 间接服务 | 提高代码质量，确保工具稳定性 |
| P0-2: 统一注册方式 | ✅ 间接服务 | 提高代码一致性，降低维护成本 |
| P0-3: 添加MIME类型 | ✅ 间接服务 | 符合MCP规范，提升互操作性 |
| P0-4: 更新文档 | ✅ 直接服务 | 确保文档准确，帮助用户理解工具 |
| P1-1: 资源订阅 | ✅ 间接服务 | 提升用户体验，符合MCP最佳实践 |
| P1-2: Prompt透明度 | ✅ 直接服务 | 帮助用户理解工具行为 |
| P1-3: 打包工具文档 | ✅ 直接服务 | 帮助用户选择正确的工具 |
| P1-4: server.py测试 | ✅ 间接服务 | 确保工具质量 |

**结论**: ✅ 所有任务都服务于核心定位或提升MCP Server质量

---

## 回归计划

如果重构导致问题，按以下顺序回退：

1. **立即回退**: P0-2（工具注册方式变更）→ 恢复add_tool()方式
2. **评估回退**: P0-1（代码重构）→ 恢复原始函数
3. **文档回退**: 所有文档更新可独立回退

---

## 附录: MCP最佳实践参考

### 官方文档位置

- FastMCP文档: `/models/claude-glm/claude-code-docs/claude-mcp-docs/`
- MCP规范: https://modelcontextprotocol.io/

### 关键最佳实践

1. **工具设计**: 单一职责、原子操作、清晰命名
2. **资源设计**: MIME类型声明、支持订阅、Resource Templates
3. **Prompt设计**: 参数化、透明化、参数补全
4. **错误处理**: 结构化响应、仅写stderr
5. **性能优化**: 异步I/O、缓存、并发控制

---

## 计划状态追踪

**当前状态**: planning
**下一步**: 等待用户审核后进入in_progress

**任务清单**:

| ID | 任务 | 优先级 | 状态 | 完成时间 | Commit |
|----|------|--------|------|----------|--------|
| P0-1 | 消除analyze/refactor重复代码 | P0 | pending | - | - |
| P0-2 | 统一工具注册方式 | P0 | pending | - | - |
| P0-3 | 添加资源MIME类型 | P0 | pending | - | - |
| P0-4 | 更新测试数量文档 | P0 | pending | - | - |
| P1-1 | 添加资源订阅机制 | P1 | pending | - | - |
| P1-2 | 提升Prompt透明度 | P1 | pending | - | - |
| P1-3 | 区分打包工具文档 | P1 | pending | - | - |
| P1-4 | 补充server.py测试 | P1 | pending | - | - |

**进度追踪**:
- 开始时间: 待定
- 任务完成: 0/8 (0%)
- 最近更新: 2026-01-29

**归档检查清单**:
- [ ] P0任务全部完成
- [ ] P1任务全部完成（或用户同意跳过）
- [ ] 验收标准全部满足
- [ ] 有完整的Git commit记录
- [ ] 有阶段性进度报告
- [ ] 未完成任务已处理（迁移或取消）
