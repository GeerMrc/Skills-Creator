# 计划 swirling-giggling-rainbow 遗漏问题修复

> **计划ID**: swirling-giggling-rainbow-audit-fix
> **创建日期**: 2026-01-29
> **状态**: planning
> **触发原因**: 归档审核发现 swirling-giggling-rainbow 计划未100%完成

---

## 一、问题发现

**归档后强制审核**（CLAUDE.md 2.5节）发现：

| 文件 | 行号 | 当前值 | 正确值 |
|------|------|--------|--------|
| `skill-creator-mcp/README.md` | 5 | `568 passed` | `566 passed` |
| `skill-creator-mcp/docs/README.md` | 165 | `95% (568)` | `97% (566)` |
| `/models/claude-glm/Skills-Creator/README.md` | 5 | `95% (568)` | `97% (566)` |
| `/models/claude-glm/Skills-Creator/README.md` | 208 | `95% (568)` | `97% (566)` |

**实际测试数据**：
- `pytest --collect-only`: 568 tests collected
- `pytest --tb=no -q`: 566 passed, 2 skipped
- `pytest --cov`: 97% coverage

---

## 二、根本原因分析

**原计划验收标准**：
> [x] 所有文档中测试数量一致（566）

**实际执行情况**：
- 仅修复了 `CLAUDE.md`（行38、行79）
- 未全面搜索并修复所有文档

**违反的规范**：
- CLAUDE.md 2.5节：归档前强制审核（100%基于实际代码审核）
- CLAUDE.md 2.7节：禁止虚假审核

---

## 三、任务清单

### T-20260129-A1: 修复 skill-creator-mcp/README.md 徽章

**优先级**: P0

**描述**:
第5行徽章从 `568 passed` 改为 `566 passed`

**影响文件**:
- `/models/claude-glm/Skills-Creator/skill-creator-mcp/README.md`

---

### T-20260129-A2: 修复 skill-creator-mcp/docs/README.md

**优先级**: P0

**描述**:
第165行从 `95% (568 个测试用例)` 改为 `97% (566 个测试用例)`

**影响文件**:
- `/models/claude-glm/Skills-Creator/skill-creator-mcp/docs/README.md`

---

### T-20260129-A3: 修复主项目 README.md

**优先级**: P0

**描述**:
- 第5行: `95% (568个测试)` → `97% (566个测试)`
- 第208行: `95% (568个测试)` → `97% (566个测试)`

**影响文件**:
- `/models/claude-glm/Skills-Creator/README.md`

---

### T-20260129-A4: 全面搜索并验证

**优先级**: P0

**描述**:
搜索所有文档中 `568` 和 `566` 的引用，确保全部修复

**命令**:
```bash
grep -rn "568\|566" /models/claude-glm/Skills-Creator --include="*.md"
```

---

## 四、验收标准

- [ ] 所有文档中测试数量一致为 566
- [ ] 所有文档中覆盖率一致为 97%
- [ ] 所有徽章显示正确
- [ ] 100%基于实际代码审核

---

## 五、进度追踪

**当前状态**: planning
**任务完成进度**: 0/4 (0%)

---

**计划创建时间**: 2026-01-29
