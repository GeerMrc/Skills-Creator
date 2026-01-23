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

### 步骤 1：开始渐进模式

**请求**:
```json
{
  "action": "start",
  "mode": "progressive"
}
```

**响应**:
```json
{
  "success": true,
  "session_id": "req_20250123_pro123",
  "action": "start",
  "mode": "progressive",
  "current_step": {
    "key": "skill_name",
    "title": "技能名称",
    "prompt": "请提供技能名称（可跳过，输入 skip）",
    "required": false
  },
  "total_steps": 5,
  "progress": 0.0,
  "message": "渐进模式：可以跳过非关键问题"
}
```

---

### 步骤 2：提供技能名称

**请求**:
```json
{
  "action": "next",
  "session_id": "req_20250123_pro123",
  "user_input": "quick-note-taker"
}
```

**响应**:
```json
{
  "success": true,
  "current_step": {
    "key": "skill_function",
    "title": "主要功能",
    "prompt": "请描述主要功能（可跳过）"
  },
  "step_index": 1,
  "progress": 20.0,
  "answers": {
    "skill_name": "quick-note-taker"
  }
}
```

---

### 步骤 3：描述主要功能

**请求**:
```json
{
  "action": "next",
  "session_id": "req_20250123_pro123",
  "user_input": "快速记录和整理笔记"
}
```

**响应**:
```json
{
  "success": true,
  "current_step": {
    "key": "use_cases",
    "title": "使用场景",
    "prompt": "主要使用场景是什么？（可跳过）"
  },
  "step_index": 2,
  "progress": 40.0,
  "answers": {
    "skill_name": "quick-note-taker",
    "skill_function": "快速记录和整理笔记"
  }
}
```

---

### 步骤 4：跳过使用场景

**请求**:
```json
{
  "action": "next",
  "session_id": "req_20250123_pro123",
  "user_input": "skip"
}
```

**响应**:
```json
{
  "success": true,
  "current_step": {
    "key": "template_type",
    "title": "模板类型",
    "prompt": "选择模板类型（可跳过，默认 minimal）"
  },
  "step_index": 3,
  "progress": 60.0,
  "skipped": ["use_cases"],
  "answers": {
    "skill_name": "quick-note-taker",
    "skill_function": "快速记录和整理笔记"
  },
  "message": "已跳过使用场景"
}
```

---

### 步骤 5：选择模板类型

**请求**:
```json
{
  "action": "next",
  "session_id": "req_20250123_pro123",
  "user_input": "minimal"
}
```

**响应**:
```json
{
  "success": true,
  "current_step": {
    "key": "additional_features",
    "title": "额外需求",
    "prompt": "是否有额外需求？（可跳过）"
  },
  "step_index": 4,
  "progress": 80.0,
  "answers": {
    "skill_name": "quick-note-taker",
    "skill_function": "快速记录和整理笔记",
    "template_type": "minimal"
  }
}
```

---

### 步骤 6：跳过额外需求

**请求**:
```json
{
  "action": "next",
  "session_id": "req_20250123_pro123",
  "user_input": "skip"
}
```

**响应**:
```json
{
  "success": true,
  "step_index": 5,
  "progress": 100.0,
  "completed": true,
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

### 场景 1：快速原型

**目标**: 快速验证想法

**流程**:
1. 渐进模式收集核心信息（2 分钟）
2. 初始化最小技能
3. 快速开发核心功能
4. 迭代完善

### 场景 2：逐步明确

**目标**: 需求逐步明确的项目

**流程**:
1. 先用渐进模式快速开始
2. 开发过程中明确需求
3. 逐步补充细节

### 场景 3：探索性开发

**目标**: 探索不同实现方案

**流程**:
1. 渐进模式快速创建多个原型
2. 对比不同方案
3. 选择最佳方案继续完善

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

### 1. 至少提供核心信息

确保提供 `skill_name` 和 `skill_function`，这是技能的基础。

### 2. 使用 skip 明确跳过

使用 "skip" 明确表示跳过，而不是留空，便于理解。

### 3. 记录待补充项

记录哪些信息被跳过，后续需要补充。

### 4. 迭代完善

渐进模式只是开始，后续持续完善技能。

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
