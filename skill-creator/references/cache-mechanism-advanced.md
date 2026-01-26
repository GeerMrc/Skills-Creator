# 缓存机制 - 高级用法

本文档介绍缓存机制的高级配置、性能优化和故障排查技巧。

> **前置阅读**: 先阅读 [缓存机制核心指南](cache-mechanism.md) 了解基础概念。

---

## 性能优化建议

### 1. 预热缓存

应用启动时预加载常用数据到缓存，减少首次请求延迟。

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

### 2. 批量操作使用缓存

在批量验证时启用特殊缓存标记，避免重复计算。

```python
async def batch_validate_with_cache(skill_paths: list[str]) -> list[dict]:
    """批量验证时启用缓存优化"""

    # 设置批量操作标记
    cache.set("batch:validation:active", True)

    try:
        results = await batch_validate_skills(
            skill_paths=skill_paths,
            concurrent_limit=5,
        )
        return results
    finally:
        # 清理批量操作标记
        cache.delete("batch:validation:active")
```

### 3. 缓存失效策略

数据更新时主动失效相关缓存，保持一致性。

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

### 4. 缓存预热策略

根据使用模式选择合适的预热时机：

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

## 缓存相关配置

### 环境变量

通过环境变量调整缓存行为：

```bash
# 缓存大小（默认256）
export SKILL_CREATOR_CACHE_SIZE=512

# 缓存 TTL（默认300秒）
export SKILL_CREATOR_CACHE_TTL=600

# 启用缓存统计（默认启用）
export SKILL_CREATOR_CACHE_STATS=true
```

### Python 配置

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

### 动态调整缓存

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

## 故障排查

### 问题1: 缓存未生效

**症状**: 函数每次都执行，没有从缓存返回

**排查步骤**:

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

# 4. 检查装饰器参数
@cached(ttl=timedelta(minutes=5))  # 确保 TTL 正确
def your_function(param):
    pass
```

**常见原因**:
- 函数参数包含不可哈希类型（如 dict、list）
- 每次调用使用了不同的参数
- TTL 设置过短，缓存已过期

### 问题2: 内存占用过高

**症状**: 应用内存占用持续增长

**排查步骤**:

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

**解决方案**:

```python
# 1. 缓存元数据而非完整数据
@cached
def get_file_metadata(path: str) -> dict:
    """缓存文件元数据，而非完整内容"""
    return {
        "size": os.path.getsize(path),
        "mtime": os.path.getmtime(path),
        "exists": os.path.exists(path),
    }

# 2. 使用弱引用缓存大对象
import weakref

weak_cache = {}
def cache_weakref(key, value):
    weak_cache[key] = weakref.ref(value)

# 3. 定期清理缓存
@repeat_every(seconds=300)
def periodic_cleanup():
    cache.clear()
```

### 问题3: 缓存命中率低

**症状**: 命中率 < 70%

**排查和优化**:

```python
# 1. 分析缓存访问模式
stats = cache.get_stats()
print(f"命中率: {stats['hit_rate']}%")
print(f"命中次数: {stats['hits']}")
print(f"未命中次数: {stats['misses']}")

# 2. 如果未命中过多，检查：
#    - 缓存大小是否太小
#    - TTL 是否太短
#    - 缓存键是否不稳定

# 3. 优化建议
if stats['misses'] > stats['hits']:
    # 增大缓存
    cache = MemoryCache(max_size=cache.max_size * 2)

    # 延长 TTL
    @cached(ttl=timedelta(hours=1))
    def your_function():
        pass
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

### 1. 多级缓存

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

### 2. 缓存分区

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

---

## 相关文档

- [缓存机制核心指南](cache-mechanism.md) - 基础概念和用法
- [批量操作示例](../examples/mcp-batch-operations.md) - 批量操作中的缓存应用
- [健康检查示例](../examples/mcp-health-check.md) - 缓存统计监控
