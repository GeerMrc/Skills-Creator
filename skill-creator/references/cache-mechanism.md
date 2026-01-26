# 缓存机制 - 核心指南

本文档介绍 Skill-Creator MCP Server 的缓存机制核心概念和基本用法。

> **高级用法**: 参见 [缓存机制高级指南](cache-mechanism-advanced.md)

---

## 概述

缓存机制用于提高重复请求的性能，减少不必要的计算和 I/O 操作。

### 核心组件

| 组件 | 说明 | 用途 |
|------|------|------|
| **`MemoryCache`** | LRU 内存缓存管理器 | 管理缓存条目，自动淘汰 |
| **`cached`** | 函数结果缓存装饰器 | 自动缓存函数返回值 |
| **`cache_key()`** | 缓存键生成函数 | 生成标准化的缓存键 |
| **`hash_content()`** | 内容哈希计算 | 为大数据生成唯一标识 |

---

## MemoryCache 类

### 基本使用

```python
from skill_creator_mcp.utils.cache import MemoryCache

# 创建缓存实例（默认256个条目）
cache = MemoryCache(max_size=256)

# 设置缓存
cache.set("user:123", {"name": "Alice", "email": "alice@example.com"})

# 获取缓存
user = cache.get("user:123")
print(user)  # {"name": "Alice", "email": "alice@example.com"}

# 检查是否存在
if cache.exists("user:123"):
    print("缓存存在")

# 删除缓存
cache.delete("user:123")

# 清空缓存
cache.clear()
```

### TTL 缓存

```python
from datetime import timedelta

# 创建带 TTL 的缓存
cache = MemoryCache(max_size=256)

# 设置10秒过期的缓存
cache.set("session:abc", data, ttl=timedelta(seconds=10))

# 检查是否过期
if cache.exists("session:abc"):
    print("缓存有效且未过期")
```

### 缓存统计

```python
# 获取缓存统计信息
stats = cache.get_stats()

print(f"缓存大小: {stats['size']}")
print(f"最大容量: {stats['max_size']}")
print(f"利用率: {stats['utilization']}%")
print(f"命中次数: {stats['hits']}")
print(f"未命中次数: {stats['misses']}")
print(f"命中率: {stats['hit_rate']:.1f}%")
```

---

## cached 装饰器

### 基本使用

```python
from skill_creator_mcp.utils.cache import cached

@cached
def expensive_function(param: str) -> dict:
    """耗时函数，结果会被缓存"""
    # 复杂计算...
    return {"result": "computed_value"}

# 第一次调用：执行函数
result1 = expensive_function("test")

# 第二次调用：从缓存返回
result2 = expensive_function("test")

print(result1 == result2)  # True
```

### 自定义缓存键

```python
@cached(key=lambda x: f"user:{x}")
def get_user_data(user_id: int) -> dict:
    """使用自定义缓存键"""
    return fetch_user_from_db(user_id)

@cached(key=lambda self, x: f"obj:{self.id}:{x}")
def method_with_cache(self, param: str) -> str:
    """方法也可以使用缓存"""
    return param.upper()
```

### TTL 缓存装饰器

```python
from datetime import timedelta

@cached(ttl=timedelta(minutes=5))
def get_weather(city: str) -> dict:
    """天气数据缓存5分钟"""
    return fetch_weather_data(city)
```

---

## 缓存键生成

### cache_key 函数

```python
from skill_creator_mcp.utils.cache import cache_key

# 生成标准缓存键
key = cache_key("function_name", arg1, arg2, kwarg1=value1)
print(key)  # "function_name:arg1:arg2:kwarg1=value1"
```

### 自定义键生成策略

```python
def custom_key(*args, **kwargs):
    """自定义键生成函数"""
    # 只使用部分参数生成键
    user_id = kwargs.get("user_id")
    return f"user_data:{user_id}"

@cached(key=custom_key)
def get_user_profile(user_id: int, include_history=False):
    """只按 user_id 缓存，忽略 include_history"""
    return fetch_profile(user_id, include_history)
```

---

## 内容哈希

### hash_content 函数

```python
from skill_creator_mcp.utils.cache import hash_content

# 生成内容哈希
content_hash = hash_content("some content")
print(content_hash)  # "a4d5...9f2c" (SHA256前16位)

# 用于大数据集缓存
@cached(key=lambda data: hash_content(data))
def process_large_dataset(data: list) -> dict:
    """按数据内容哈希缓存"""
    return analyze_data(data)
```

---

## 全局缓存实例

```python
from skill_creator_mcp.utils.cache import _global_cache

# 直接使用全局缓存实例
_global_cache.set("key", value)
result = _global_cache.get("key")
```

---

## 最佳实践

### 1. 选择合适的缓存大小

```python
# 小型应用：128个条目
cache = MemoryCache(max_size=128)

# 中型应用：256个条目（默认）
cache = MemoryCache(max_size=256)

# 大型应用：512或更多
cache = MemoryCache(max_size=512)
```

### 2. 设置合理的 TTL

```python
# 频繁变化的数据：短 TTL
@cached(ttl=timedelta(seconds=30))
def get_real_time_data() -> dict:
    pass

# 相对稳定的数据：中等 TTL
@cached(ttl=timedelta(minutes=5))
def get_user_profile(user_id: int) -> dict:
    pass

# 很少变化的数据：长 TTL
@cached(ttl=timedelta(hours=1))
def get_system_config() -> dict:
    pass
```

### 3. 使用分层缓存键

```python
# 推荐的键命名规范
cache.set("user:123:profile", data)        # 用户资料
cache.set("user:123:settings", data)       # 用户设置
cache.set("session:abc", data)             # 会话数据
cache.set("cache:config:default", data)    # 配置缓存
```

### 4. 监控缓存命中率

```python
# 定期检查缓存性能
stats = cache.get_stats()
hit_rate = stats["hit_rate"]

if hit_rate < 70:
    print("警告：缓存命中率较低，考虑调整策略")
elif hit_rate > 90:
    print("缓存效果良好")
```

### 5. 避免缓存过大对象

```python
# 不推荐：缓存大文件
@cached
def get_large_file() -> bytes:
    return read_entire_file("/path/to/large.file")

# 推荐：缓存文件元数据
@cached
def get_file_metadata() -> dict:
    return get_file_info("/path/to/large.file")
```

---

## 相关文档

- [缓存机制高级指南](cache-mechanism-advanced.md) - 性能优化和故障排查
- [批量操作示例](../examples/mcp-batch-operations.md) - 批量操作中的缓存应用
- [健康检查示例](../examples/mcp-health-check.md) - 缓存统计监控
- [MCP 集成指南](mcp-integration.md) - MCP 工具配置
