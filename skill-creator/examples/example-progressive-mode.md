# 渐进模式使用示例

本文档展示如何使用 `collect_requirements` 的渐进模式快速创建技能原型。

## 概述

渐进模式 (progressive) 适合快速原型开发：
- 核心信息优先
- 允许跳过非关键步骤
- 后续可补充细节
- 动态调整问题

预计时间：2-3 分钟（核心信息）

---

## 模式特点

| 特性 | 渐进模式 | 基础模式 |
|------|----------|----------|
| 必填步骤 | 仅核心 2-3 步 | 全部 5 步 |
| 可跳过 | ✅ | ❌ |
| 速度 | 快 | 中等 |
| 完整性 | 中 | 高 |
| 适用场景 | 快速原型 | 正式开发 |

---

## 对话流程

### 开始收集

```json
{"action": "start", "mode": "progressive"}
```

**响应** - 第一个问题（技能名称）：
```json
{
  "session_id": "req_20250123_pro123",
  "current_step": {
    "key": "skill_name",
    "prompt": "请提供技能名称（可跳过，输入 skip）",
    "required": false
  },
  "message": "渐进模式：可以跳过非关键问题"
}
```

### 提供核心信息

步骤 1: `quick-note-taker` → 保存 skill_name
步骤 2: `快速记录和整理笔记` → 保存 skill_function
步骤 3: `skip` → 跳过 use_cases
步骤 4: `minimal` → 保存 template_type
步骤 5: `skip` → 跳过 additional_features

### 最终结果

```json
{
  "completed": true,
  "progress": 100.0,
  "skipped": ["use_cases", "additional_features"],
  "answers": {
    "skill_name": "quick-note-taker",
    "skill_function": "快速记录和整理笔记",
    "template_type": "minimal"
  },
  "message": "核心信息收集完成！可以开始开发，后续可补充细节"
}
```

---

## 快速开始开发

渐进模式完成后，可以立即开始开发：

```bash
# 使用收集的核心信息初始化技能
init_skill(name="quick-note-taker", template="minimal")
```

后续可以根据需要补充细节：
- 添加使用场景
- 定义额外需求
- 完善功能描述

---

## 典型使用场景

| 场景 | 目标 | 流程 |
|------|------|------|
| 快速原型 | 验证想法 | 收集核心信息 → 初始化 → 开发 → 迭代 |
| 逐步明确 | 需求渐进 | 快速开始 → 开发中明确 → 补充细节 |
| 探索开发 | 对比方案 | 创建多原型 → 对比选择 → 完善 |

---

## 跳过策略

### 核心步骤（建议不跳过）

| 步骤 | 键名 | 原因 |
|------|------|------|
| 1 | `skill_name` | 必需，用于目录结构 |
| 2 | `skill_function` | 必需，定义核心功能 |

### 可选步骤（可以跳过）

| 步骤 | 键名 | 可以后续补充 |
|------|------|-------------|
| 3 | `use_cases` | ✅ 可以在使用中明确 |
| 4 | `template_type` | ✅ 默认 minimal |
| 5 | `additional_features` | ✅ 可以迭代添加 |

---

## 补充细节

### 方法 1：重新收集

使用 `previous` 返回并补充信息：

```json
{
  "action": "previous",
  "session_id": "req_20250123_pro123"
}
```

### 方法 2：完整模式

对已创建的技能使用完整模式补充细节。

### 方法 3：代码中补充

直接在代码中补充注释和文档。

---

## 与基础模式对比

| 方面 | 渐进模式 | 基础模式 |
|------|----------|----------|
| 时间投入 | 2-3 分钟 | 3-5 分钟 |
| 信息完整度 | 60% | 90% |
| 灵活性 | 高 | 中 |
| 适合阶段 | 原型/探索 | 正式开发 |
| 后续工作 | 需要补充 | 可直接使用 |

---

## 最佳实践

1. **至少提供核心信息**：确保提供 `skill_name` 和 `skill_function`
2. **使用 skip 明确跳过**：使用 "skip" 而不是留空
3. **记录待补充项**：记录跳过的信息以便后续补充
4. **迭代完善**：渐进模式只是开始，后续持续完善

---

## 回退机制说明

> **注意**: 由于当前客户端限制，渐进模式使用回退策略：
> - 使用预定义问题列表
> - 智能选择下一个问题
> - 固定规则检查完整性

详见 [回退机制文档](../references/fallback-mechanism.md)

---

## 相关文档

- **[基础模式示例](example-basic-mode.md)** - 5 步完整收集
- **[完整模式示例](example-complete-mode.md)** - 10 步详细收集
- **[Elicit 模式示例](example-elicit-mode.md)** - 自动收集
- **[需求收集模式详解](../references/requirement-collection-modes.md)** - 模式对比
