# 健康检查使用示例

本文档展示如何使用健康检查工具监控系统状态、性能指标和缓存统计。

---

## 概述

健康检查工具提供三个级别的系统监控：

- **`health_check_tool`** - 完整健康检查（系统、缓存、性能指标）
- **`quick_status_tool`** - 快速状态摘要（一行字符串）
- **`is_healthy_tool`** - 快速健康判断（布尔值）

---

## 完整健康检查

### 获取系统全面状态

```python
result = await health_check_tool(ctx)

if result["success"]:
    health = result["health"]
    system = result["system"]
    cache = result["cache"]
    performance = result["performance"]

    # 健康状态
    print(f"状态: {health['status']}")
    print(f"运行时间: {health['uptime_seconds']} 秒")
    print(f"版本: {health['version']}")

    # 系统指标
    print(f"CPU: {system['cpu_percent']}%")
    print(f"内存: {system['memory_percent']}%")
    print(f"磁盘: {system['disk_percent']}%")
```

### 返回结果示例

```json
{
  "success": true,
  "health": {
    "status": "healthy",
    "timestamp": "2026-01-25T13:30:00",
    "uptime_seconds": 3600.5,
    "version": "0.3.0"
  },
  "system": {
    "cpu_percent": 15.2,
    "memory_percent": 45.8,
    "memory_used_mb": 920.5,
    "memory_available_mb": 1087.5,
    "disk_percent": 62.3,
    "disk_used_gb": 125.6,
    "disk_free_gb": 75.8
  },
  "cache": {
    "size": 128,
    "max_size": 256,
    "utilization_percent": 50.0
  },
  "performance": {
    "total_requests": 1523,
    "successful_requests": 1489,
    "failed_requests": 34,
    "avg_response_time_ms": 45.2
  },
  "environment": {
    "python_version": "3.12.0",
    "platform": "Linux-5.4.0-x86_64",
    "system": "Linux",
    "release": "5.4.0-216-generic"
  }
}
```

---

## 快速状态摘要

### 获取一行状态信息

```python
result = await quick_status_tool(ctx)

if result["success"]:
    print(result["status"])
    # 输出示例:
    # Status: HEALTHY | Uptime: 1h 0m | CPU: 15.2% | Memory: 45.8% | Requests: 1523
```

### 适用场景

- 日志记录
- 状态栏显示
- 定时健康检查
- 轻量级监控

---

## 快速健康判断

### 布尔值健康检查

```python
result = await is_healthy_tool(ctx)

if result["success"]:
    if result["healthy"]:
        print("系统健康，可以继续处理任务")
    else:
        print("系统不健康，建议检查")
```

### 适用场景

- 条件判断
- 自动化决策
- 告警触发

---

## 健康状态级别

### 状态定义

| 状态 | CPU | 内存 | 磁盘 | 失败率 | 说明 |
|------|-----|------|------|--------|------|
| `healthy` | <70% | <80% | <95% | <10% | 系统正常 |
| `degraded` | 70-90% | 80-90% | - | 10-50% | 性能下降 |
| `unhealthy` | >90% | >90% | >95% | >50% | 需要关注 |

### 状态判断逻辑

```python
# 系统不健康条件
if cpu_percent > 90:
    return "unhealthy"
if memory_percent > 90:
    return "unhealthy"
if disk_percent > 95:
    return "unhealthy"

# 系统降级条件
if failure_rate > 0.5:
    return "unhealthy"
if failure_rate > 0.1:
    return "degraded"

# 资源使用率较高
if cpu_percent > 70 or memory_percent > 80:
    return "degraded"

return "healthy"
```

---

## 使用场景示例

### 场景1：定时健康检查

```python
import asyncio

async def health_monitor(interval=60):
    """定时检查系统健康"""
    while True:
        result = await is_healthy_tool(ctx)
        if not result["healthy"]:
            # 发送告警
            print("警告：系统不健康！")
            # 获取详细信息
            health = await health_check_tool(ctx)
            print(health)
        await asyncio.sleep(interval)
```

### 场景2：批量操作前检查

```python
async def safe_batch_operation(skill_paths):
    """在系统健康时执行批量操作"""
    # 先检查健康状态
    health = await is_healthy_tool(ctx)

    if not health["healthy"]:
        print("系统状态不佳，延迟操作")
        return None

    # 系统健康，执行批量操作
    return await batch_validate_skills_tool(
        ctx,
        skill_paths=skill_paths,
    )
```

### 场景3：性能监控

```python
async def performance_monitor():
    """监控系统性能指标"""
    result = await health_check_tool(ctx)

    perf = result["performance"]

    # 检查响应时间
    if perf["avg_response_time_ms"] > 100:
        print("警告：响应时间过长")

    # 检查成功率
    total = perf["total_requests"]
    if total > 0:
        success_rate = perf["successful_requests"] / total
        if success_rate < 0.95:
            print(f"警告：成功率仅为 {success_rate*100:.1f}%")
```

### 场景4：缓存利用率监控

```python
async def cache_monitor():
    """监控缓存使用情况"""
    result = await health_check_tool(ctx)

    cache = result["cache"]
    utilization = cache["utilization_percent"]

    if utilization > 90:
        print("警告：缓存即将满，考虑增加容量")
    elif utilization < 20:
        print("提示：缓存利用率较低，可以减小容量")
```

---

## 告警策略

### 定义告警阈值

```python
ALERT_THRESHOLDS = {
    "cpu_high": 80,
    "memory_high": 85,
    "disk_high": 90,
    "response_time_high": 100,
    "success_rate_low": 0.95,
}

async def check_alerts():
    """检查告警条件"""
    result = await health_check_tool(ctx)

    alerts = []

    # CPU 告警
    if result["system"]["cpu_percent"] > ALERT_THRESHOLDS["cpu_high"]:
        alerts.append(f"CPU 使用率过高: {result['system']['cpu_percent']}%")

    # 内存告警
    if result["system"]["memory_percent"] > ALERT_THRESHOLDS["memory_high"]:
        alerts.append(f"内存使用率过高: {result['system']['memory_percent']}%")

    # 响应时间告警
    if result["performance"]["avg_response_time_ms"] > ALERT_THRESHOLDS["response_time_high"]:
        alerts.append(f"响应时间过长: {result['performance']['avg_response_time_ms']}ms")

    return alerts
```

---

## 性能指标说明

### 性能统计字段

| 字段 | 说明 |
|------|------|
| `total_requests` | 总请求数（自启动） |
| `successful_requests` | 成功请求数 |
| `failed_requests` | 失败请求数 |
| `avg_response_time_ms` | 平均响应时间（毫秒） |

### 指标重置

```python
from skill_creator_mcp.tools.health_check import reset_performance_stats

# 重置性能统计数据
reset_performance_stats()
```

---

## 相关文档

- [MCP 集成指南](../references/mcp-integration.md) - MCP 工具使用详解
- [批量操作示例](mcp-batch-operations.md) - 批量验证和分析
