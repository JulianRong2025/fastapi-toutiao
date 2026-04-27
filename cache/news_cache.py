# 新闻相关的缓存方法：新闻分类的读取和写入
# key - value

from typing import Any, Dict, List

from config.cache_conf import get_cache_json, set_cache


CATEGORIES_KEY = "news:categories"

# 获取新闻分类缓存
async def get_cached_categories():
    return await get_cache_json(CATEGORIES_KEY)

# 写入新闻分类缓存:缓存的数据、过期时间
# 分类、配置:7200;列表:600;详情:1800;验证码:120    --- 数据越稳定，缓存越持久
# 不同类型的数据设置不同过期时间，能够避免缓存雪崩（大量数据同时过期）和热点数据频繁失效的问题
async def set_cached_categories(data: List[Dict[str, Any]], expire: int = 7200):
    return await set_cache(CATEGORIES_KEY, data, expire)