# 完整模式使用示例

本文档展示如何使用 `collect_requirements` 的完整模式创建复杂技能。

## 概述

完整模式 (complete) 通过 10 个步骤全面收集技术细节：

**基础 5 步** + **额外 5 步**：
1. 技能名称
2. 主要功能
3. 使用场景
4. 模板类型
5. 额外需求
6. **目标用户** - 谁会使用这个技能
7. **技术栈** - Python, Node.js 等
8. **外部依赖** - API、库、服务
9. **测试要求** - 单元测试、集成测试
10. **文档级别** - 基础/完整/详细

预计时间：10-15 分钟

---

## 完整对话流程

### 步骤 1-5：基础信息收集

与基础模式相同，收集名称、功能、场景、模板、额外需求。

---

### 步骤 6：目标用户

**请求**:
```json
{
  "action": "next",
  "session_id": "req_20250123_xyz789",
  "user_input": "数据分析师、研究人员、文档管理员"
}
```

**响应**:
```json
{
  "success": true,
  "current_step": {
    "key": "target_users",
    "title": "目标用户",
    "prompt": "谁是这个技能的主要用户？"
  },
  "step_index": 5,
  "total_steps": 10,
  "progress": 50.0,
  "answers": {
    "skill_name": "data-pipeline-orchestrator",
    "target_users": "数据分析师、研究人员、文档管理员"
  }
}
```

---

### 步骤 7：技术栈

**请求**:
```json
{
  "action": "next",
  "session_id": "req_20250123_xyz789",
  "user_input": "Python 3.10+, Apache Airflow, Pandas, SQLAlchemy"
}
```

**响应**:
```json
{
  "success": true,
  "current_step": {
    "key": "tech_stack",
    "title": "技术栈",
    "prompt": "使用什么技术栈？"
  },
  "step_index": 6,
  "total_steps": 10,
  "progress": 60.0,
  "answers": {
    "tech_stack": "Python 3.10+, Apache Airflow, Pandas, SQLAlchemy"
  }
}
```

---

### 步骤 8：外部依赖

**请求**:
```json
{
  "action": "next",
  "session_id": "req_20250123_xyz789",
  "user_input": "PostgreSQL database, Redis cache, AWS S3 storage, REST API endpoints"
}
```

**响应**:
```json
{
  "success": true,
  "current_step": {
    "key": "dependencies",
    "title": "外部依赖",
    "prompt": "需要哪些外部依赖？"
  },
  "step_index": 7,
  "total_steps": 10,
  "progress": 70.0,
  "answers": {
    "dependencies": "PostgreSQL database, Redis cache, AWS S3 storage, REST API endpoints"
  }
}
```

---

### 步骤 9：测试要求

**请求**:
```json
{
  "action": "next",
  "session_id": "req_20250123_xyz789",
  "user_input": "单元测试覆盖率 ≥85%，包含集成测试和端到端测试"
}
```

**响应**:
```json
{
  "success": true,
  "current_step": {
    "key": "testing_requirements",
    "title": "测试要求",
    "prompt": "有什么测试要求？"
  },
  "step_index": 8,
  "total_steps": 10,
  "progress": 80.0,
  "answers": {
    "testing_requirements": "单元测试覆盖率 ≥85%，包含集成测试和端到端测试"
  }
}
```

---

### 步骤 10：文档级别

**请求**:
```json
{
  "action": "next",
  "session_id": "req_20250123_xyz789",
  "user_input": "完整文档：API 文档 + 使用示例 + 部署指南"
}
```

**响应**:
```json
{
  "success": true,
  "step_index": 9,
  "total_steps": 10,
  "progress": 90.0,
  "answers": {
    "documentation_level": "完整文档：API 文档 + 使用示例 + 部署指南"
  },
  "message": "所有步骤已完成，请使用 complete 完成收集"
}
```

---

### 完成收集

**请求**:
```json
{
  "action": "complete",
  "session_id": "req_20250123_xyz789"
}
```

**响应**:
```json
{
  "success": true,
  "completed": true,
  "progress": 100.0,
  "answers": {
    "skill_name": "data-pipeline-orchestrator",
    "skill_function": "自动化数据处理流水线编排和监控",
    "use_cases": "ETL 任务、数据同步、批量处理",
    "template_type": "workflow-based",
    "additional_features": "支持动态任务依赖、失败重试、性能监控",
    "target_users": "数据分析师、研究人员、文档管理员",
    "tech_stack": "Python 3.10+, Apache Airflow, Pandas, SQLAlchemy",
    "dependencies": "PostgreSQL database, Redis cache, AWS S3 storage, REST API endpoints",
    "testing_requirements": "单元测试覆盖率 ≥85%，包含集成测试和端到端测试",
    "documentation_level": "完整文档：API 文档 + 使用示例 + 部署指南"
  },
  "is_complete": true,
  "missing_info": [],
  "suggestions": [
    "考虑添加任务调度性能指标",
    "可以添加数据质量校验功能"
  ]
}
```

---

## 模式对比

| 特性 | 基础模式 | 完整模式 |
|------|----------|----------|
| 步骤数 | 5 | 10 |
| 时间 | 3-5 分钟 | 10-15 分钟 |
| 适用场景 | 明确需求 | 复杂技能/团队项目 |
| 技术细节 | 基础 | 详细 |
| 文档级别 | 简单 | 完整 |

---

## 适用场景

### 团队协作项目

完整模式提供详细的规格说明，便于团队成员理解和协作。

### 生产环境部署

详细的技术栈、依赖和测试要求确保生产环境的稳定性。

### 复杂业务逻辑

10 个步骤确保所有技术细节都被考虑。

---

## 额外信息的作用

### 目标用户 (target_users)

帮助确定：
- UI/UX 设计方向
- 功能优先级
- 文档风格

### 技术栈 (tech_stack)

指导：
- 代码结构设计
- 依赖管理
- 部署配置

### 外部依赖 (dependencies)

明确：
- 集成需求
- 环境配置
- 故障处理

### 测试要求 (testing_requirements)

确保：
- 代码质量
- 系统稳定性
- 维护性

### 文档级别 (documentation_level)

决定：
- 文档详细程度
- 维护成本
- 用户体验

---

## 最佳实践

### 1. 团队讨论

在开始完整模式收集前，先与团队讨论关键决策。

### 2. 技术预研

对于不确定的技术栈，先进行简单的技术预研。

### 3. 分阶段收集

如果 10 步太长，可以先完成基础 5 步，后续补充。

### 4. 记录决策理由

在额外需求中记录关键决策的理由，便于后续回顾。

---

## 相关文档

- **[基础模式示例](example-basic-mode.md)** - 5 步快速收集
- **[需求收集模式详解](../references/requirement-collection-modes.md)** - 模式对比
- **[最佳实践](../references/best-practices-core.md)** - 开发规范
