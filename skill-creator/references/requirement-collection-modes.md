# 需求收集模式详解

> **架构说明**：需求收集基于 **7个原子化MCP工具 + Agent-Skill工作流编排** 的混合架构（符合ADR 001）。本文档展示各种收集模式的概念和用法，实际使用通过skill-creator Agent-Skill调用。

本文档详细说明需求收集功能的各种收集模式，基于7个原子化MCP工具。

> **相关文档**：
> - [需求澄清基础指南](requirement-collection-basics.md) - 核心概念和快速开始
> - [需求收集 API 参考](requirement-collection-api.md) - API 文档索引
> - [API 核心参考](requirement-collection-api-core.md) - 完整的 API 技术文档
> - [API 使用示例](requirement-collection-api-examples.md) - 实际使用场景和最佳实践

## 目录



- [基础模式 (basic)](#基础模式-basic)
- [完整模式 (complete)](#完整模式-complete)
- [头脑风暴模式 (brainstorm)](#头脑风暴模式-brainstorm)
- [渐进式模式 (progressive)](#渐进式模式-progressive)
- [Elicit 自动模式](#elicit-自动模式)

---

## 基础模式 (basic)



5 步快速收集，适合明确需求的用户。

### 步骤详情



| 步骤 | 键名 | 标题 | 验证规则 |
|------|------|------|----------|
| 1 | `skill_name` | 技能名称 | 必填，1-64字符，小写字母+数字+连字符 |
| 2 | `skill_function` | 主要功能 | 必填，简短描述 |
| 3 | `use_cases` | 使用场景 | 必填，列出2-3个场景 |
| 4 | `template_type` | 模板类型 | 必填，4选1 |
| 5 | `additional_features` | 额外需求 | 可选 |

### 适用场景



- 已清楚知道要创建什么技能
- 不需要复杂的技术规格
- 希望快速开始开发

### 示例对话



```python
# 开始


collect_requirements(action="start", mode="basic")
# → "请输入技能名称"



# 回答


collect_requirements(action="next", user_input="pdf-helper")
# → "请简要描述技能的主要功能"



# 继续...


# → "请列出使用场景"


# → "请选择模板类型"


# → "是否有额外需求？"


```

---

## 完整模式 (complete)



10 步全面收集，包含所有技术细节。

### 步骤详情



基础模式 (1-5) + 额外步骤：

| 步骤 | 键名 | 标题 | 说明 |
|------|------|------|------|
| 6 | `target_users` | 目标用户 | 谁会使用这个技能 |
| 7 | `tech_stack` | 技术栈 | Python、Node.js 等 |
| 8 | `dependencies` | 外部依赖 | API、库、服务 |
| 9 | `testing_requirements` | 测试要求 | 单元测试、集成测试 |
| 10 | `documentation_level` | 文档级别 | 基础/完整/详细 |

### 适用场景



- 复杂技能，需要详细规划
- 团队协作，需要明确的规格
- 生产环境部署

### 示例对话



```python
# 步骤 6-10 的对话


# → "谁是目标用户？"


# → "使用什么技术栈？"


# → "需要哪些外部依赖？"


# → "有什么测试要求？"


# → "需要什么级别的文档？"


```

---

## 头脑风暴模式 (brainstorm)



AI 引导的创意发散，探索技能可能性。

### 模式特点



- **开放性问题**：引导思考各种可能性
- **多角度探索**：从不同视角分析
- **记录想法**：保存所有创意
- **动态长度**：默认 5 轮对话

### 适用场景



- 只有模糊的想法
- 需要灵感启发
- 探索多种可能性

### 示例对话



```python
# 开始头脑风暴


collect_requirements(action="start", mode="brainstorm")

# AI: "你想解决什么问题？"


# User: "处理 PDF 文档很麻烦..."



# AI: "有哪些具体场景？"


# User: "提取表格、批量转换、OCR识别..."



# AI: "有什么技术偏好？"


# User: "希望用 Python..."



# AI: "还需要考虑什么？"


# User: "跨平台支持..."



# AI: "还有什么补充？"


# User: "批量处理能力..."



# → AI 总结收集到的想法


```

### 注意事项



- 不强制要求填写所有字段
- 鼓励自由表达想法
- AI 会引导但不会限制

---

## 渐进式模式 (progressive)



快速开始，后续逐步完善。

### 模式特点



- **核心信息优先**：先收集关键信息
- **允许跳过**：非关键步骤可跳过
- **后续补充**：稍后可添加细节
- **动态长度**：根据需要调整

### 适用场景



- 快速原型开发
- 需求逐步明确
- 迭代式开发

### 示例对话



```python
# 开始渐进式收集


collect_requirements(action="start", mode="progressive")

# 核心问题


# → "技能名称是什么？"


# → "主要功能是什么？"



# 可选问题


# → "目标用户是谁？" (可跳过)


# → "有什么特殊需求？" (可跳过)



# → 快速完成，后续可补充


```

### 与基础模式的区别



| 特性 | basic | progressive |
|------|-------|-------------|
| 必填步骤 | 全部 5 步 | 仅核心 2-3 步 |
| 可跳过 | ❌ | ✅ |
| 速度 | 中等 | 快 |
| 完整性 | 高 | 中 |

---

## Elicit 自动模式



设置 `use_elicit=True` 后，AI 自动调用 `ctx.elicit()` 逐个收集输入。

### 工作原理



```python
# 一步完成所有收集


result = await collect_requirements(
    action="start",
    mode="basic",
    use_elicit=True  # 关键参数
)
```

**后台行为**：
1. AI 自动调用 `ctx.elicit()`
2. 逐个显示问题等待输入
3. 验证失败时自动重试（最多 3 次）
4. 每步后自动保存会话状态
5. 收集完成后返回结果

### 与传统模式的区别



| 特性 | 传统模式 | Elicit 模式 |
|------|----------|------------|
| 调用方式 | 多次调用 (start → next×5 → complete) | 一次调用 |
| 用户交互 | 手动传递 user_input | AI 自动调用 elicit |
| 状态管理 | 手动管理 session_id | 自动保存每步 |
| 中断恢复 | 需要保存 session_id | 自动保存 |
| 适用场景 | 需要精细控制的场景 | 快速完成需求收集 |

### 使用示例



```python
# Elicit 模式


result = await collect_requirements(
    action="start",
    mode="basic",
    use_elicit=True
)

# AI 会自动：


# 1. "请输入技能名称" → 等待输入


# 2. "请描述主要功能" → 等待输入


# 3. ... (继续所有步骤)


# 4. 返回完整结果



# 用户可以随时取消


# → 返回 cancelled 状态，已收集信息不会丢失


```

### 错误处理



```python
# 验证失败时


result = await collect_requirements(..., use_elicit=True)

# 如果输入格式错误：


# 1. AI 自动显示错误提示


# 2. 重新请求输入


# 3. 最多重试 3 次


# 4. 仍失败则返回错误


```

### 注意事项



- 需要客户端支持 `ctx.elicit()`
- 用户取消时返回 `cancelled` 状态
- 验证失败自动重试 3 次
- 动态模式 (brainstorm/progressive) 默认 5 轮

---

## 模式选择指南



### 决策树



```
是否需要自动收集？
├─ 是 → Elicit 模式 (use_elicit=True)
└─ 否 → 需求明确度？
    ├─ 非常明确 → Basic 模式
    ├─ 需要细节 → Complete 模式
    ├─ 只有想法 → Brainstorm 模式
    └─ 快速原型 → Progressive 模式
```

### 对比总结



| 模式 | 步骤 | 速度 | 完整性 | 灵活性 |
|------|------|------|--------|--------|
| **basic** | 5 | ⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐ |
| **complete** | 10 | ⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐ |
| **brainstorm** | 动态 | ⭐⭐⭐ | ⭐⭐ | ⭐⭐⭐⭐⭐ |
| **progressive** | 动态 | ⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐⭐ |
| **elicit** | 自动 | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐ |

---

## 相关文档



- **[需求澄清基础指南](requirement-collection-basics.md)** - 核心概念和快速开始
- **[需求收集 API 参考](requirement-collection-api.md)** - API 文档索引
- **[API 核心参考](requirement-collection-api-core.md)** - 完整的 API 技术文档
- **[API 使用示例](requirement-collection-api-examples.md)** - 实际使用场景和最佳实践
- **[需求收集示例](../examples/requirement-collection-basic.md)** - 代码示例
