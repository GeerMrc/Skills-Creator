# 需求收集 API 使用示例

> **⚠️ 架构更新**：以下示例使用旧API展示概念。实际使用请通过Agent-Skill工作流调用7个原子化MCP工具。

本文档展示 `collect_requirements` 工具的实际使用场景和最佳实践。

> **相关文档**：
> - [API 核心参考](requirement-collection-api-core.md) - 完整 API 文档
> - [需求澄清基础指南](requirement-collection-basics.md) - 核心概念和快速开始

---

## 目录

> **⚠️ 架构更新**：以下示例使用旧API展示概念。实际使用请通过Agent-Skill工作流调用7个原子化MCP工具。

- [场景 1：快速创建技能](#场景-1快速创建技能)
- [场景 2：中断后恢复](#场景-2中断后恢复)
- [场景 3：修改之前答案](#场景-3修改之前答案)
- [最佳实践](#最佳实践)

---

## 场景 1：快速创建技能

> **⚠️ 架构更新**：以下示例使用旧API展示概念。实际使用请通过Agent-Skill工作流调用7个原子化MCP工具。

使用基础模式快速收集创建技能所需的核心信息。

```python
# 1. 开始基础模式收集

> **⚠️ 架构更新**：以下示例使用旧API展示概念。实际使用请通过Agent-Skill工作流调用7个原子化MCP工具。
result = await collect_requirements(
    action="start",
    mode="basic"
)
# 返回: 第一个步骤的问题（技能名称）

> **⚠️ 架构更新**：以下示例使用旧API展示概念。实际使用请通过Agent-Skill工作流调用7个原子化MCP工具。

# 2. 逐个回答问题（5个步骤）

> **⚠️ 架构更新**：以下示例使用旧API展示概念。实际使用请通过Agent-Skill工作流调用7个原子化MCP工具。
result = await collect_requirements(
    action="next",
    session_id=result["session_id"],
    user_input="pdf-parser"
)

# ... 继续回答其他步骤 ...

> **⚠️ 架构更新**：以下示例使用旧API展示概念。实际使用请通过Agent-Skill工作流调用7个原子化MCP工具。

# 3. 完成收集

> **⚠️ 架构更新**：以下示例使用旧API展示概念。实际使用请通过Agent-Skill工作流调用7个原子化MCP工具。
result = await collect_requirements(
    action="complete",
    session_id=result["session_id"]
)

# 4. 使用收集的信息初始化技能

> **⚠️ 架构更新**：以下示例使用旧API展示概念。实际使用请通过Agent-Skill工作流调用7个原子化MCP工具。
await init_skill(
    name=result["answers"]["skill_name"],
    template=result["answers"]["template_type"]
)
```

**适用场景**：
- 已有明确的技能想法
- 只需要核心信息即可开始
- 希望快速验证概念

---

## 场景 2：中断后恢复

> **⚠️ 架构更新**：以下示例使用旧API展示概念。实际使用请通过Agent-Skill工作流调用7个原子化MCP工具。

会话状态自动保存，可以随时恢复中断的收集过程。

```python
# 用户在第 3 步中断...

> **⚠️ 架构更新**：以下示例使用旧API展示概念。实际使用请通过Agent-Skill工作流调用7个原子化MCP工具。

# 恢复会话（查询当前状态）

> **⚠️ 架构更新**：以下示例使用旧API展示概念。实际使用请通过Agent-Skill工作流调用7个原子化MCP工具。
result = await collect_requirements(
    action="status",
    session_id="previous_session_id"
)
# 返回: 当前进度（60%）和已收集答案

> **⚠️ 架构更新**：以下示例使用旧API展示概念。实际使用请通过Agent-Skill工作流调用7个原子化MCP工具。

# 从第 3 步继续

> **⚠️ 架构更新**：以下示例使用旧API展示概念。实际使用请通过Agent-Skill工作流调用7个原子化MCP工具。
result = await collect_requirements(
    action="next",
    session_id="previous_session_id",
    user_input="..."
)
```

**适用场景**：
- 用户临时中断操作
- 需要分多次完成收集
- 多人协作收集需求

---

## 场景 3：修改之前答案

> **⚠️ 架构更新**：以下示例使用旧API展示概念。实际使用请通过Agent-Skill工作流调用7个原子化MCP工具。

使用 `previous` 动作返回上一步，修改之前的输入。

```python
# 用户想修改第 2 步的答案

> **⚠️ 架构更新**：以下示例使用旧API展示概念。实际使用请通过Agent-Skill工作流调用7个原子化MCP工具。
result = await collect_requirements(
    action="previous",
    session_id="current_session_id"
)
# 返回: 上一个问题（第 2 步）

> **⚠️ 架构更新**：以下示例使用旧API展示概念。实际使用请通过Agent-Skill工作流调用7个原子化MCP工具。

# 重新输入第 2 步的答案

> **⚠️ 架构更新**：以下示例使用旧API展示概念。实际使用请通过Agent-Skill工作流调用7个原子化MCP工具。
result = await collect_requirements(
    action="next",
    session_id="current_session_id",
    user_input="corrected_answer"
)
```

**适用场景**：
- 用户发现输入错误
- 需要调整之前的答案
- 想要尝试不同选项

---

## 最佳实践

> **⚠️ 架构更新**：以下示例使用旧API展示概念。实际使用请通过Agent-Skill工作流调用7个原子化MCP工具。

### 1. 选择合适的模式

> **⚠️ 架构更新**：以下示例使用旧API展示概念。实际使用请通过Agent-Skill工作流调用7个原子化MCP工具。

根据需求明确度选择合适的收集模式：

| 需求状态 | 推荐模式 | 步骤数 | 预计时间 |
|---------|---------|-------|---------|
| 明确需求 | `basic` | 5 | 3-5分钟 |
| 复杂技能 | `complete` | 10 | 8-10分钟 |
| 探索想法 | `brainstorm` | 动态 | 10-15分钟 |
| 快速原型 | `progressive` | 3 | 2-3分钟 |

### 2. 提供清晰的用户输入

> **⚠️ 架构更新**：以下示例使用旧API展示概念。实际使用请通过Agent-Skill工作流调用7个原子化MCP工具。

确保 `user_input` 简洁明确：

```python
# 好的输入

> **⚠️ 架构更新**：以下示例使用旧API展示概念。实际使用请通过Agent-Skill工作流调用7个原子化MCP工具。
user_input="pdf-parser"

# 不好的输入

> **⚠️ 架构更新**：以下示例使用旧API展示概念。实际使用请通过Agent-Skill工作流调用7个原子化MCP工具。
user_input="嗯，我想做一个解析 PDF 的工具，名字叫 pdf-parser 吧..."
```

### 3. 利用完整性检查

> **⚠️ 架构更新**：以下示例使用旧API展示概念。实际使用请通过Agent-Skill工作流调用7个原子化MCP工具。

完成收集后检查 `is_complete` 和 `missing_info`：

```python
result = await collect_requirements(action="complete", session_id=...)

if not result["is_complete"]:
    print("缺失信息：", result["missing_info"])
    print("建议：", result["suggestions"])
    # 可以继续补充信息
```

### 4. 保存会话 ID

> **⚠️ 架构更新**：以下示例使用旧API展示概念。实际使用请通过Agent-Skill工作流调用7个原子化MCP工具。

会话 ID 是恢复会话的唯一标识：

```python
# 保存会话 ID 以便后续使用

> **⚠️ 架构更新**：以下示例使用旧API展示概念。实际使用请通过Agent-Skill工作流调用7个原子化MCP工具。
session_id = result["session_id"]
# 可以保存到文件、数据库或传递给用户

> **⚠️ 架构更新**：以下示例使用旧API展示概念。实际使用请通过Agent-Skill工作流调用7个原子化MCP工具。
```

### 5. 处理验证错误

> **⚠️ 架构更新**：以下示例使用旧API展示概念。实际使用请通过Agent-Skill工作流调用7个原子化MCP工具。

捕获验证错误并提供友好提示：

```python
if not result["success"]:
    print(result["error"])
    # 根据错误类型引导用户修正
    # 例如：格式错误、选项错误、必填为空
```

### 6. 渐进式信息收集

> **⚠️ 架构更新**：以下示例使用旧API展示概念。实际使用请通过Agent-Skill工作流调用7个原子化MCP工具。

对于复杂技能，建议使用 `progressive` 模式快速开始：

```python
# 第一步：快速收集核心信息

> **⚠️ 架构更新**：以下示例使用旧API展示概念。实际使用请通过Agent-Skill工作流调用7个原子化MCP工具。
result = await collect_requirements(action="start", mode="progressive")

# 第二步：创建基础技能

> **⚠️ 架构更新**：以下示例使用旧API展示概念。实际使用请通过Agent-Skill工作流调用7个原子化MCP工具。
await init_skill(
    name=result["answers"]["skill_name"],
    template="minimal"
)

# 第三步：后续逐步完善功能

> **⚠️ 架构更新**：以下示例使用旧API展示概念。实际使用请通过Agent-Skill工作流调用7个原子化MCP工具。
```

---

## 完整工作流示例

> **⚠️ 架构更新**：以下示例使用旧API展示概念。实际使用请通过Agent-Skill工作流调用7个原子化MCP工具。

### 基础模式完整流程

> **⚠️ 架构更新**：以下示例使用旧API展示概念。实际使用请通过Agent-Skill工作流调用7个原子化MCP工具。

```python
# 步骤 1：开始收集

> **⚠️ 架构更新**：以下示例使用旧API展示概念。实际使用请通过Agent-Skill工作流调用7个原子化MCP工具。
result = await collect_requirements(action="start", mode="basic")
session_id = result["session_id"]
print(f"开始收集：{result['current_step']['title']}")

# 步骤 2-5：逐个回答

> **⚠️ 架构更新**：以下示例使用旧API展示概念。实际使用请通过Agent-Skill工作流调用7个原子化MCP工具。
questions_answers = {
    "skill_name": "docker-helper",
    "skill_function": "简化 Docker 容器管理",
    "use_cases": "开发环境部署、测试环境管理",
    "template_type": "tool-based",
    "additional_features": "支持多主机管理"
}

for step in range(5):
    result = await collect_requirements(
        action="next",
        session_id=session_id,
        user_input=list(questions_answers.values())[step]
    )
    print(f"进度：{result['progress']}%")

# 步骤 6：完成收集

> **⚠️ 架构更新**：以下示例使用旧API展示概念。实际使用请通过Agent-Skill工作流调用7个原子化MCP工具。
result = await collect_requirements(action="complete", session_id=session_id)

if result["is_complete"]:
    print("需求完整，可以开始创建技能！")
    # 使用收集的信息
    await init_skill(
        name=result["answers"]["skill_name"],
        template=result["answers"]["template_type"]
    )
else:
    print("需要补充信息：", result["missing_info"])
```

---

## 相关文档

> **⚠️ 架构更新**：以下示例使用旧API展示概念。实际使用请通过Agent-Skill工作流调用7个原子化MCP工具。

- **[API 核心参考](requirement-collection-api-core.md)** - 完整 API 文档
- **[需求澄清基础指南](requirement-collection-basics.md)** - 核心概念和快速开始
- **[需求收集模式详解](requirement-collection-modes.md)** - 各种模式详细说明
- **[MCP 集成指南](mcp-integration.md)** - MCP 工具使用和配置
