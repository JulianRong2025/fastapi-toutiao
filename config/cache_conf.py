import json
from typing import Any

import redis.asyncio as redis

REDIS_HOST = 'localhost'
REDIS_PORT = 6379
REDIS_DB = 0


# 创建 Redis 的链接对象
redis_client = redis.Redis(host=REDIS_HOST,  # Redis 服务器的主机地址
                           port=REDIS_PORT,  # Redis 服务器的端口号
                           db=REDIS_DB, # Redis 数据库索引，0-15
                           decode_responses=True  # 是否自动将 Redis 存储的字节数据解码为字符串
                           )

# 设置 和 读取 （字符串 和 列表或字典）"[{}]""
# 读取：字符串
async def get_cache(key: str):
    try:
        value = await redis_client.get(key)
        return value
    except Exception as e:
        print(f"获取缓存失败: {e}")
        return None
    
# 读取：列表或字典
async def get_cache_json(key: str):
    try:
        value = await redis_client.get(key)
        if value:
            return json.loads(value)  # 将 JSON 字符串转换为 Python 对象，去掉引号。序列化
        return None
    except Exception as e:
        print(f"获取 JSON 缓存失败: {e}")
        return None
    
# 设置缓存 setex(key, expire, value) key: 键，expire: 过期时间（秒），value: 值
async def set_cache(key: str, value: Any, expire: int = 3600):
    try:
        if isinstance(value, (dict, list)):
            # 将 Python 对象转换为 JSON 字符串,ensure_ascii=False 保持中文字符不被转义
            value = json.dumps(value, ensure_ascii=False)  
        await redis_client.setex(key, expire, value)
        return True
    except Exception as e:
        print(f"设置缓存失败: {e}")