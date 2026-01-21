# Skills-Creator 问题清单

> **生成日期**：2026-01-21
> **基于审计报告**：ARCHITECTURE_AUDIT_REPORT_v2.md

---

## 问题统计总览

| 级别 | 已修复 | 待修复 | 总计 |
|------|--------|--------|------|
| Critical | 4 | 0 | **4** |
| High | 1 | 8 | **9** |
| Medium | 1 | 10 | **11** |
| Low | 0 | 11 | **11** |
| **总计** | **6** | **29** | **35** |

---

## Critical 级问题（已修复 ✅）

### C-001: Tool 命名不一致 ✅
**文件**: `server.py:496`
**问题**: 函数名为 `package_skill_tool`，但 SKILL.md 中为 `package_skill`
**修复**: 重命名函数为 `package_skill`
**状态**: ✅ 已修复

### C-002: 资源 URI 格式非标准 ✅
**文件**: `server.py:729-763`
**问题**: 使用 `skill://` 而非 MCP 标准格式
**修复**: 改为 `http://skills/schema/`
**状态**: ✅ 已修复

### C-006: mcp-integration.md 缺少 package_skill 工具文档 ✅
**文件**: `references/mcp-integration.md`
**问题**: 缺少第5个工具的文档说明
**修复**: 在 refactor_skill 后添加 package_skill 文档
**状态**: ✅ 已修复

### C-007: validation.md 包含引用文件间相互引用 ✅
**文件**: `references/validation.md:428-430`
**问题**: 违反"引用文件独立性"原则
**修复**: 删除"参考资源"章节
**状态**: ✅ 已修复

---

## High 级问题（9项）

### H-001: 缺少日志系统

**文件**: 所有 Python 文件
**问题**: 无日志记录，调试困难
**修复**: 添加 `logging` 模块，配置日志级别

**建议实现**：
```python
import logging

logger = logging.getLogger(__name__)

@mcp.tool()
async def some_tool(ctx, skill_path: str):
    logger.info("Processing skill: %s", skill_path)
    try:
        ...
    except Exception as e:
        logger.error("Failed: %s", e, exc_info=True)
```

**优先级**: P0 (1-2天)

---

### H-002: Pydantic 模型未被使用

**文件**: `models/skill_config.py`
**问题**: 定义了 Pydantic 模型但未在工具函数中使用
**修复**: 在工具函数中使用 Pydantic 验证输入

**建议实现**：
```python
@mcp.tool()
async def init_skill(...):
    input_data = InitSkillInput(
        name=name,
        template=template,
        output_dir=output_dir,
        with_scripts=with_scripts,
        with_examples=with_examples,
    )
    # 使用 input_data
```

**优先级**: P0 (2-3天)

---

### H-003: 异步函数使用同步 I/O

**文件**: `analyzers.py:36`
**问题**: 在异步函数中使用同步文件读取
**修复**: 改用 `asyncio.to_thread` 或 `aiofiles`

**建议实现**：
```python
# 当前代码
with open(py_file, encoding="utf-8") as f:
    lines = f.readlines()

# 修复后
lines = await asyncio.to_thread(py_file.read_text)
```

**优先级**: P1 (3-5天)

---

### H-004: 配置硬编码

**文件**: 多处
**问题**: 魔法数字和字符串散布代码中
**修复**: 外部化配置，使用环境变量或配置文件

**建议实现**：
```python
import os
from dotenv import load_dotenv

load_dotenv()

TEMPLATE_REQUIREMENTS = {
    "max_lines": int(os.getenv("SKILL_MAX_LINES", "150")),
    "max_tokens": int(os.getenv("SKILL_MAX_TOKENS", "2000")),
}
```

**优先级**: P1 (2-3天)

---

### H-005: best-practices.md 包含不存在的示例文件引用

**文件**: `references/best-practices.md:251`
**问题**: 引用了不存在的示例文件
**修复**: 改为注释说明或通用示例

**优先级**: P1 (1天)

---

### H-006: validation.md 行数超过最佳实践推荐

**文件**: `references/validation.md`: 425行
**问题**: 超过400行推荐值
**修复**: 拆分为 `validation-rules.md` 和 `validation-checklist.md`

**优先级**: P1 (2-3天)

---

### H-007: architecture-audit-report.md 行数超出引用文件范围

**文件**: `references/architecture-audit-report.md`: 552行
**问题**: 应放在项目根目录
**修复**: 移至项目根目录

**优先级**: P2 (1天)

---

### H-008: 缺少 Code Review 流程

**文件**: 项目根目录缺失 `.github/`
**问题**: 无 PR 模板和检查清单
**修复**: 创建 PR 模板和检查清单

**建议文件**：
```
.github/
├── PULL_REQUEST_TEMPLATE.md
├── ISSUE_TEMPLATE/
│   ├── bug_report.md
│   └── feature_request.md
└── workflows/
    └── code-review.yml
```

**优先级**: P1 (3-5天)

---

### H-009: Commit 消息语言不统一

**文件**: Git 历史
**问题**: 计划要求中文，实际使用英文
**决策**: 继续使用英文（国际项目标准）

**优先级**: P2 (文档更新)

---

## Medium 级问题（11项）

### M-001: 类型提示不完整

**文件**: 多处
**修复**: 补全所有函数的类型注解

**优先级**: P2

---

### M-002: 文档字符串格式不统一

**文件**: 多处
**修复**: 统一使用 Google 或 NumPy 风格

**优先级**: P2

---

### M-003: 魔法数字散布代码中

**文件**: 多处
**修复**: 提取为常量

**优先级**: P2

---

### M-004: 资源内容过时

**文件**: `resources/*.py`
**修复**: 更新模板内容

**优先级**: P2

---

### M-005: 缺少路径清理验证

**文件**: `validators.py`, `file_ops.py`
**修复**: 添加路径规范化检查

**优先级**: P2

---

### M-006: SKILL.md "触发词"使用动词形式

**文件**: `SKILL.md:13`
**问题**: "创建技能、初始化技能" 是动词短语
**修复**: 改为关键词形式

**建议**：
```yaml
触发词：技能创建、技能初始化、技能验证、技能分析、技能重构、技能模板
```

**优先级**: P2

---

### M-007: mcp-integration.md 行数超标

**文件**: `references/mcp-integration.md`: 342行
**修复**: 将示例移至 `examples/mcp-usage.md`

**优先级**: P2

---

### M-008: validation.md 交叉引用已删除 ✅

**状态**: 已修复

---

### M-009: SKILL.md 修改未提交

**文件**: `SKILL.md`
**修复**: 检查并提交修改

**优先级**: P2

---

### M-010: CHANGELOG.md 未提交

**文件**: `CHANGELOG.md`
**修复**: 添加并提交

**优先级**: P2

---

### M-011: prompts 参数类型注解

**文件**: `server.py:805`
**问题**: `list[str] | None` 可能不被某些 MCP 客户端支持
**修复**: 使用字符串描述或简化类型

**优先级**: P2

---

## Low 级问题（11项）

### L-001: 缺少性能分析工具

**修复**: 添加性能监控装饰器

**优先级**: P3

---

### L-002: 部分单元测试缺失

**修复**: 补充测试用例

**优先级**: P3

---

### L-003: 错误消息未国际化

**修复**: 支持多语言错误消息

**优先级**: P3

---

### L-004: 代码重复

**修复**: 提取公共函数

**优先级**: P3

---

### L-005: 资源 URI 缺少版本控制

**修复**: 添加版本号到 URI

**优先级**: P3

---

### L-006: MCP 资源 URI 表缺少表头

**文件**: `SKILL.md:78-84`
**修复**: 添加表头

**优先级**: P3

---

### L-007: 配置示例路径占位符不够明确

**文件**: `references/mcp-integration.md:20`
**修复**: 添加注释说明

**优先级**: P3

---

### L-008: 评分标准缺少 token 效率阈值

**文件**: `references/best-practices.md:376-381`
**修复**: 添加 token 效率行

**优先级**: P3

---

### L-009: Git 工作流文档需要更新

**修复**: 更新为实际工作流

**优先级**: P3

---

### L-010: MCP Inspector 指南缺失

**修复**: 添加交互式测试指南

**优先级**: P3

---

### L-011: 性能基准测试未实施

**修复**: 添加响应时间基准

**优先级**: P3

---

## 修复优先级路线图

### 立即修复（本周内）

1. ✅ C-001: Tool 命名不一致
2. ✅ C-002: 资源 URI 格式
3. ✅ C-006: mcp-integration.md 缺少文档
4. ✅ C-007: validation.md 交叉引用
5. H-001: 添加日志系统

### 尽快修复（2周内）

1. H-002: 使用 Pydantic 验证
2. H-003: 优化异步 I/O
3. H-004: 外部化配置
4. H-005: 修复示例文件引用
5. H-008: 创建 Code Review 流程

### 计划修复（1个月内）

1. H-006: 拆分 validation.md
2. H-007: 移动 audit 报告
3. M-001 到 M-011: Medium 级问题

### 有时间时修复（持续）

1. L-001 到 L-011: Low 级问题

---

## 问题跟踪

所有问题将追踪至 GitHub Issues（待创建）。
