# ctx.elicit() 集成实现计划

> **创建日期**: 2026-01-23
> **状态**: completed
> **优先级**: P0
> **关联任务**: 任务 #9
> **完成日期**: 2026-01-23

---

## 一、目标

将 FastMCP Context API 的 `ctx.elicit()` 方法集成到 `collect_requirements` 工具中，提供更流畅的用户输入体验。

### 实现总结

✅ **已完成**: ctx.elicit() 集成功能已实现并通过测试

**实现内容**:
1. 新增 `use_elicit` 参数到 `collect_requirements()` 函数
2. 实现 `_collect_with_elicit()` 辅助函数（~200行代码）
3. 支持静态和动态模式（basic/complete/brainstorm/progressive）
4. 验证失败重试机制（最多3次）
5. 用户取消处理
6. 会话状态自动保存
7. 5个单元测试用例
8. 文档更新

**测试结果**: 369 测试通过，87% 代码覆盖率

### 当前流程（两步调用）

```
用户 → collect_requirements(action="start") → 返回问题
用户 → collect_requirements(action="next", user_input="...") → 处理并返回下一个问题
```

### 目标流程（一步调用）

```
用户 → collect_requirements(action="start") → 内部调用 ctx.elicit() 自动获取输入 → 返回下一个问题
```

---

## 二、技术分析

### 2.1 ctx.elicit() 功能

根据 FastMCP 文档和测试代码：

```python
result = await ctx.elicit(
    prompt,              # 向用户显示的提示文本
    response_type=str,   # 期望的响应类型
)

# 返回值
result.action  # "accept" | "cancel"
result.data    # 用户输入的数据
```

### 2.2 设计挑战

| 挑战 | 描述 | 解决方案 |
|------|------|----------|
| 流程变更 | 需要从"两步调用"改为"一步调用" | 添加新的 `use_elicit` 参数 |
| 向后兼容 | 现有的 action="next" 流程不能破坏 | 保留原有流程，添加新选项 |
| 错误处理 | 用户取消输入时的处理 | 返回取消状态，保存会话 |
| 验证逻辑 | elicit() 后需要验证输入 | 内置验证循环 |

---

## 三、实现方案

### 3.1 新增参数

```python
async def collect_requirements(
    ctx: Context,
    action: str = "start",
    mode: str = "basic",
    session_id: str | None = None,
    user_input: str | None = None,
    use_elicit: bool = False,  # 新增：是否使用 elicit 模式
) -> dict[str, Any]:
```

### 3.2 交互模式

#### 模式 A：传统模式 (use_elicit=False)

```
用户调用 → 返回问题 → 用户调用 action="next" + user_input → 处理
```

#### 模式 B：Elicit 模式 (use_elicit=True)

```
用户调用 → 内部 ctx.elicit() → 自动处理 → 返回下一个问题或完成
```

### 3.3 核心逻辑

```python
if use_elicit and action == "start":
    # Elicit 模式：自动收集所有输入
    while not session_state.completed:
        if is_dynamic_mode:
            question = await generate_question(...)
        else:
            question = all_steps[session_state.current_step_index]

        # 调用 elicit 获取用户输入
        result = await ctx.elicit(question.prompt, response_type=str)

        if result.action == "cancel":
            return {
                "success": False,
                "action": "cancelled",
                "message": "用户取消了输入",
                "session_id": current_session_id,
            }

        # 验证输入
        validation = _validate_requirement_answer(result.data, ...)
        if not validation["valid"]:
            # 重新 elicit（显示错误）
            continue

        # 保存答案并继续
        session_state.answers[key] = result.data
        session_state.current_step_index += 1
```

### 3.4 错误处理

| 场景 | 处理方式 |
|------|----------|
| 用户取消输入 | 返回 cancelled 状态，保存已收集的答案 |
| 验证失败 | 重新调用 elicit()，附带错误提示 |
| LLM 生成失败 | 使用降级问题 |

---

## 四、实现步骤

### 步骤 1: 添加 use_elicit 参数

修改 `collect_requirements` 函数签名，添加 `use_elicit` 参数。

### 步骤 2: 实现 elicit 循环

创建 `_collect_with_elicit()` 辅助函数，处理完整的 elicit 循环逻辑。

### 步骤 3: 验证循环集成

在 elicit 循环中集成验证逻辑，确保输入符合要求。

### 步骤 4: 错误处理

实现取消、验证失败等场景的处理。

### 步骤 5: 测试

编写单元测试验证 elicit 模式的正确性。

### 步骤 6: 文档更新

更新相关文档说明新的交互模式。

---

## 五、任务拆分

| 任务 | 描述 | 优先级 |
|------|------|--------|
| 9.1 | 添加 use_elicit 参数和基本结构 | P0 |
| 9.2 | 实现 _collect_with_elicit() 辅助函数 | P0 |
| 9.3 | 集成验证循环 | P0 |
| 9.4 | 错误处理和取消场景 | P0 |
| 9.5 | 编写单元测试 | P0 |
| 9.6 | 更新文档 | P1 |

---

## 六、验收标准

- [x] use_elicit=True 时，工具自动调用 ctx.elicit() 收集输入
- [x] 用户取消输入时正确返回 cancelled 状态
- [x] 验证失败时重新请求输入
- [x] 会话状态正确保存
- [x] 向后兼容：use_elicit=False 时保持原有行为
- [x] 测试覆盖率 ≥ 80% (实际: 87%)

---

## 七、风险评估

| 风险 | 影响 | 缓解措施 |
|------|------|----------|
| ctx.elicit() 在某些环境中不可用 | 高 | 添加可用性检测，降级到传统模式 |
| 循环调用导致阻塞 | 中 | 设置最大重试次数限制 |
| 与现有流程冲突 | 低 | 使用参数开关，默认关闭 |

---

## 八、参考资料

- FastMCP Context API 文档: https://gofastmcp.com/servers/context
- 现有实现: `server.py` 第 772-1131 行
- 测试工具: `server.py` 第 1486-1525 行

---

**计划创建**: 2026-01-23
**预计完成**: 当日
