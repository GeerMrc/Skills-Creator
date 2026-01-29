# 缓存机制 - 高级示例

> **注意**: 本示例展示高级缓存使用技巧。缓存功能由MCP Server内部实现，旨在提高批量操作性能。

本文档包含缓存机制的高级用法示例代码。

---

## 预热缓存

```python
def warm_up_cache():
    """应用启动时预热缓存"""
    cache = MemoryCache()

    # 预加载常用数据
    cache.set("config:default", load_default_config())
    cache.set("template:minimal", load_minimal_template())
    cache.set("validation:rules", load_validation_rules())
    cache.set("best:practices", load_best_practices())

    print(f"预热完成，缓存大小: {cache.get_stats()['size']}")
```

### 预热策略

```python
# 主动预热：应用启动时
@app.on_event("startup")
async def startup_warmup():
    warm_up_cache()

# 被动预热：首次访问时
@cached(ttl=timedelta(hours=1))
def get_skill_template(template_name: str):
    """首次访问时缓存，后续直接返回"""
    return load_template(template_name)

# 定时预热：后台任务
@repeat_every(seconds=3600)  # 每小时
async def scheduled_warmup():
    """定期刷新热点数据"""
    cache.set("hot:data", fetch_hot_data())
```

---

## 批量操作使用缓存

**注意**: 批量工具（batch_validate_skills, batch_analyze_skills）已在 v0.3.4 中移除。
建议使用循环调用单个工具或使用并发库（如 asyncio）自行实现批量操作。

```python
import asyncio
from typing import list

async def batch_validate_with_cache(skill_paths: list[str]) -> list[dict]:
    """批量验证时启用缓存优化（手动实现）"""

    # 设置批量操作标记
    cache.set("batch:validation:active", True)

    try:
        # 手动并发调用 validate_skill
        tasks = [
            validate_skill(skill_path=path)
            for path in skill_paths
        ]
        results = await asyncio.gather(*tasks, return_exceptions=True)
        return results
    finally:
        # 清理批量操作标记
        cache.delete("batch:validation:active")
```

---

## 缓存失效策略

```python
def update_skill_config(skill_id: str, new_config: dict):
    """更新技能配置并失效相关缓存"""

    # 1. 更新数据源
    save_skill_config(skill_id, new_config)

    # 2. 失效相关缓存（使用通配符模式）
    cache.delete(f"skill:{skill_id}:config")
    cache.delete(f"skill:{skill_id}:validation")
    cache.delete(f"skill:{skill_id}:metadata")

    # 3. 预热新数据
    cache.set(f"skill:{skill_id}:config", new_config)
```

---

## Python 配置示例

```python
from skill_creator_mcp.utils.cache import MemoryCache

# 高性能配置：大缓存，长 TTL
high_perf_cache = MemoryCache(
    max_size=1024,          # 更多条目
    default_ttl=600,        # 10分钟TTL
)

# 低内存配置：小缓存，短 TTL
low_mem_cache = MemoryCache(
    max_size=128,           # 较少条目
    default_ttl=120,        # 2分钟TTL
)

# 实时数据配置：禁用 TTL
realtime_cache = MemoryCache(
    max_size=256,
    default_ttl=0,          # 不过期，手动清理
)
```

---

## 动态调整缓存

```python
class AdaptiveCache:
    """自适应缓存：根据命中率动态调整"""

    def __init__(self, initial_size=256):
        self.cache = MemoryCache(max_size=initial_size)

    def monitor_and_adjust(self):
        """监控命中率并调整缓存大小"""
        stats = self.cache.get_stats()
        hit_rate = stats["hit_rate"]

        if hit_rate < 60:
            # 命中率低：增大缓存
            new_size = min(self.cache.max_size * 2, 1024)
            print(f"命中率低({hit_rate}%)，增大缓存到 {new_size}")
            self.cache = MemoryCache(max_size=new_size)

        elif hit_rate > 95 and self.cache.size < self.cache.max_size // 2:
            # 命中率高但利用率低：减小缓存
            new_size = max(self.cache.max_size // 2, 64)
            print(f"利用率低，减小缓存到 {new_size}")
            self.cache = MemoryCache(max_size=new_size)
```

---

## 故障排查代码

### 检查缓存状态

```python
# 1. 检查缓存是否创建
cache = MemoryCache()
print(f"缓存状态: {cache.get_stats()}")

# 2. 检查键是否正确
from skill_creator_mcp.utils.cache import cache_key
key = cache_key("func_name", arg1, arg2)
print(f"缓存键: {key}")

# 3. 检查缓存是否存在
if cache.exists(key):
    print("缓存存在")
else:
    print("缓存不存在，检查函数参数是否一致")
```

### 检查内存占用

```python
# 1. 检查缓存大小
stats = cache.get_stats()
print(f"缓存大小: {stats['size']}/{stats['max_size']}")
print(f"利用率: {stats['utilization']}%")

# 2. 如果利用率 > 90%，考虑清理或减小缓存
if stats['utilization'] > 90:
    cache.clear()  # 清空缓存
    # 或者减小缓存大小
    cache = MemoryCache(max_size=stats['max_size'] // 2)

# 3. 检查是否有大对象被缓存
import sys
for key in list(cache._data.keys()):
    obj = cache._data[key]
    size = sys.getsizeof(obj)
    if size > 1024 * 1024:  # > 1MB
        print(f"大对象: {key} ({size} bytes)")
```

### 缓存元数据而非完整数据

```python
@cached
def get_file_metadata(path: str) -> dict:
    """缓存文件元数据，而非完整内容"""
    return {
        "size": os.path.getsize(path),
        "mtime": os.path.getmtime(path),
        "exists": os.path.exists(path),
    }
```

---

## 缓存监控

### 实时监控

```python
def monitor_cache():
    """实时监控缓存状态"""
    while True:
        stats = cache.get_stats()

        print(f"""
        缓存监控:
        - 大小: {stats['size']}/{stats['max_size']}
        - 利用率: {stats['utilization']}%
        - 命中率: {stats['hit_rate']}%
        - 命中: {stats['hits']} | 未命中: {stats['misses']}
        """)

        time.sleep(60)  # 每分钟检查
```

### Prometheus 指标

```python
from prometheus_client import Gauge, Counter

# 定义指标
cache_size = Gauge('cache_size', 'Cache size')
cache_hits = Counter('cache_hits', 'Cache hits')
cache_misses = Counter('cache_misses', 'Cache misses')

def export_metrics():
    """导出缓存指标到 Prometheus"""
    stats = cache.get_stats()

    cache_size.set(stats['size'])
    cache_hits.inc(stats['hits'])
    cache_misses.inc(stats['misses'])
```

---

## 高级技巧

### 多级缓存

```python
class MultiLevelCache:
    """L1: 内存缓存 + L2: 磁盘缓存"""

    def __init__(self):
        self.l1 = MemoryCache(max_size=256)
        self.l2_path = Path("/tmp/cache_l2")

    def get(self, key: str):
        # 先查 L1
        if self.l1.exists(key):
            return self.l1.get(key)

        # 再查 L2
        l2_file = self.l2_path / key
        if l2_file.exists():
            data = json.loads(l2_file.read_text())
            # 回填 L1
            self.l1.set(key, data)
            return data

        return None
```

### 缓存分区

```python
class PartitionedCache:
    """按类型分区的缓存"""

    def __init__(self):
        self.templates = MemoryCache(max_size=64)
        self.validations = MemoryCache(max_size=128)
        self.metadata = MemoryCache(max_size=256)

    def get(self, partition: str, key: str):
        cache = getattr(self, partition)
        return cache.get(key)

    def set(self, partition: str, key: str, value):
        cache = getattr(self, partition)
        cache.set(key, value)
```
