# Skills-Creator v0.3.6 全面审核与发布计划

> **计划类型**: 发布计划
> **创建日期**: 2026-01-30
> **目标版本**: v0.3.6
> **计划状态**: planning

---

## 一、执行摘要

### 目标

全面审核 Skills-Creator 项目，确保核心定位符合，统一版本号到 v0.3.6，打包并发布到远端仓库。

### 核心定位

**Skills-Creator** 为用户进行 Agent-Skills 高效/规范/最佳实践标准化开发。

### 项目状态

| 指标 | 状态 |
|------|------|
| 核心版本号 | ✅ v0.3.6 (pyproject.toml, __init__.py) |
| 工具数量 | ✅ 12个 (4技能+7需求+1打包) |
| 测试覆盖 | ✅ 97% (553个测试) |
| 代码质量 | ✅ ruff 0错误, mypy 0错误 |
| 已弃用功能 | ✅ 已正确清理 |

### 发现的问题

**P0 - 版本号不一致**：
1. `skill-creator-mcp/MCP_TOOLS.md`: v0.3.4 → v0.3.6
2. `README.md`: v0.3.4 → v0.3.6
3. `skill-creator-mcp/README.md`: 示例版本号过时
4. `server.py`: 健康检查端点版本
5. `docs/README.md`: v0.3.4 → v0.3.6

**P1 - 测试数量不一致**：
1. `README.md`: 568 → 553

**✅ 良好状态**：
- CHANGELOG.md 包含 v0.3.5 和 v0.3.6 记录
- 已弃用功能已正确清理

---

## 二、任务清单

| ID | 任务名称 | 优先级 | 状态 | 完成时间 | Commit |
|----|---------|--------|------|----------|--------|
| T-001 | 统一所有文档版本号到v0.3.6 | P0 | pending | - | - |
| T-002 | 统一测试数量声明为553 | P1 | pending | - | - |
| T-003 | 全面审核项目核心定位符合度 | P0 | pending | - | - |
| T-004 | 打包skill-creator zip包 | P0 | pending | - | - |
| T-005 | 构建skill-creator-mcp whl包 | P0 | pending | - | - |
| T-006 | 发布前全面检查清单验证 | P0 | pending | - | - |
| T-007 | 创建Git Tag和发布说明 | P0 | pending | - | - |
| T-008 | 归档计划并生成汇报文档 | P1 | pending | - | - |

**进度**: 0/8 任务完成 (0%)

---

## 三、详细任务说明

### T-001: 统一所有文档版本号到v0.3.6 (P0)

**目标**: 确保所有文档版本号与核心代码一致

**验收标准**:
- [ ] `skill-creator-mcp/MCP_TOOLS.md` 第3行: v0.3.4 → v0.3.6
- [ ] 根目录 `README.md` 第3行: v0.3.4 → v0.3.6
- [ ] `skill-creator-mcp/README.md` 示例版本号更新
- [ ] `skill-creator-mcp/src/skill_creator_mcp/server.py` 第287行
- [ ] `docs/README.md` 第163行: v0.3.4 → v0.3.6
- [ ] `ROADMAP.md` 更新过时引用

**变更文件**:
- `skill-creator-mcp/MCP_TOOLS.md`
- `README.md`
- `skill-creator-mcp/README.md`
- `skill-creator-mcp/src/skill_creator_mcp/server.py`
- `docs/README.md`
- `ROADMAP.md`

---

### T-002: 统一测试数量声明为553 (P1)

**目标**: 确保测试数量与实际一致

**验收标准**:
- [ ] `README.md`: 568 → 553
- [ ] 徽章数据准确

**变更文件**:
- `README.md`

---

### T-003: 全面审核项目核心定位符合度 (P0)

**目标**: 100%基于实际代码审核核心定位符合度

**验收标准**:
- [ ] Agent-Skill 所有内容聚焦 Agent-Skills 开发
- [ ] MCP Server 12个工具都服务于核心定位
- [ ] 外部MCP集成服务于核心定位
- [ ] 已弃用功能无活跃引用
- [ ] 架构边界清晰

---

### T-004: 打包skill-creator zip包 (P0)

**目标**: 使用 package_skill(strict=True) 打包

**验收标准**:
- [ ] 包名: `skill-creator-v0.3.6.zip`
- [ ] 包结构符合标准
- [ ] 文件数量 < 50个
- [ ] 包大小 < 500KB
- [ ] 排除项验证通过

**命令**:
```python
from skill_creator_mcp.utils.packagers import package_skill
package_skill(
    skill_path="/models/claude-glm/Skills-Creator/skill-creator",
    version="0.3.6",
    strict=True
)
```

---

### T-005: 构建skill-creator-mcp whl包 (P0)

**目标**: 构建Python包

**验收标准**:
- [ ] 生成: `skill_creator_mcp-0.3.6-py3-none-any.whl`
- [ ] 包大小合理 (< 5MB)
- [ ] 元数据验证通过
- [ ] 新环境安装验证成功

**命令**:
```bash
cd skill-creator-mcp
uv build
```

**使用说明**:
```bash
pip install skill-creator-mcp==0.3.6
```

---

### T-006: 发布前全面检查清单验证 (P0)

**目标**: 100%基于实际代码审核

**检查清单**:

**代码质量**:
- [ ] `pytest --cov` 全部通过 (553测试, 97%)
- [ ] `ruff check .` 0错误
- [ ] `mypy src/` 0错误
- [ ] `bandit -r src/` 0高危

**版本一致性**:
- [ ] 所有文档版本号 = v0.3.6
- [ ] 所有测试数量 = 553

**文档完整性**:
- [ ] CHANGELOG.md 包含 v0.3.6
- [ ] 交叉引用链接有效

**Git状态**:
- [ ] develop 分支领先 origin/develop
- [ ] working tree clean

---

### T-007: 创建Git Tag和发布说明 (P0)

**目标**: 创建 v0.3.6 发布

**验收标准**:
- [ ] 创建 Git Tag `v0.3.6`
- [ ] 推送 Tag 到远端
- [ ] 创建 GitHub Release
- [ ] 附加两个包
- [ ] 包含使用配置说明

**命令**:
```bash
git tag -a v0.3.6 -m "Release v0.3.6"
git push origin v0.3.6
```

**发布说明**:
```markdown
# v0.3.6 - Skills-Creator 全面审核与发布

## 安装

### Agent-Skill
下载 `skill-creator-v0.3.6.zip`

### MCP Server
```bash
pip install skill-creator-mcp==0.3.6
```

## 质量指标
- 测试: 553个 (97%覆盖率)
- 工具: 12个 (4技能+7需求+1打包)
```

---

### T-008: 归档计划并生成汇报文档 (P1)

**目标**: 完成九步法步骤9

**验收标准**:
- [ ] 所有任务状态 = completed
- [ ] 生成汇报文档
- [ ] 归档到 archive/
- [ ] 归档检查清单100%勾选

---

## 四、关键文件清单

### 需要修改的文件

| 文件 | 修改内容 | 位置 |
|------|----------|------|
| `skill-creator-mcp/MCP_TOOLS.md` | 版本号 v0.3.4→v0.3.6 | 第3行 |
| `README.md` | 版本号和测试数量 | 第3、5行 |
| `skill-creator-mcp/README.md` | 示例版本号 | 多处 |
| `skill-creator-mcp/src/skill_creator_mcp/server.py` | 健康检查版本 | 第287行 |
| `docs/README.md` | 版本号 | 第163行 |
| `ROADMAP.md` | 版本引用 | 多处 |

### 验证正确的文件

| 文件 | 状态 |
|------|------|
| `skill-creator-mcp/pyproject.toml` | ✅ v0.3.6 |
| `skill-creator-mcp/src/skill_creator_mcp/__init__.py` | ✅ v0.3.6 |
| `CHANGELOG.md` | ✅ 包含v0.3.5和v0.3.6 |

---

## 五、发布流程

```
T-001: 统一版本号
    ↓
T-002: 统一测试数量
    ↓
T-003: 审核核心定位
    ↓
┌─────────────┬─────────────┐
│ T-004: 打包 │ T-005: 构建 │
│ skill-creator│ MCP whl     │
└─────────────┴─────────────┘
    ↓
T-006: 发布前全面检查
    ↓
T-007: 创建Tag和Release
    ↓
T-008: 归档计划并汇报
```

---

## 六、风险与应对

| 风险 | 可能性 | 影响 | 应对 |
|------|--------|------|------|
| 版本号更新遗漏 | 中 | 文档不一致 | grep全面搜索，逐项验证 |
| 打包验证失败 | 低 | 无法安装 | 虚拟环境验证，保留日志 |
| 发布后发现问题 | 低 | 需要紧急修复 | 执行T-006全面检查 |

---

## 七、成功标准

- [ ] 所有文档版本号 = v0.3.6
- [ ] 所有测试数量 = 553
- [ ] 核心定位100%符合
- [ ] skill-creator-v0.3.6.zip 可用
- [ ] skill_creator_mcp-0.3.6.whl 可用
- [ ] GitHub Release v0.3.6 创建成功
- [ ] 归档检查清单100%勾选

---

## 八、审核方法声明

**本计划100%基于实际代码审核**：

- ✅ 读取实际文件验证版本号
- ✅ 运行pytest统计测试数量
- ✅ 搜索代码中的弃用引用
- ✅ 检查文档一致性
- ✅ 验证CHANGELOG完整性

**未仅依赖**：
- ❌ Git commit 摘要
- ❌ 文档声明
- ❌ 历史记录

---

## 九、归档检查清单

- [ ] P0任务全部完成 (T-001, T-003, T-004, T-005, T-006, T-007)
- [ ] P1任务全部完成或用户同意跳过 (T-002, T-008)
- [ ] 所有验收标准满足
- [ ] 有完整的Git commit记录
- [ ] 有阶段性进度报告
- [ ] 未完成任务已处理（迁移或取消）

---

**计划创建时间**: 2026-01-30
**预计完成时间**: 2026-01-30
**计划状态**: 准备就绪，等待执行
