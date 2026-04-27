

from typing import Any, Dict, List, Optional

from config.cache_conf import get_cache_json, set_cache

# 新闻相关的缓存方法：新闻分类的读取和写入
# key - value

CATEGORIES_KEY = "news:categories"
NEWS_LIST_KEY_PREFIX = "news_list"  # news_list:分类id:页码:每页数量

# 获取新闻分类缓存
async def get_cached_categories():
    return await get_cache_json(CATEGORIES_KEY)

# 写入新闻分类缓存:缓存的数据、过期时间
# 分类、配置:7200;列表:600;详情:1800;验证码:120    --- 数据越稳定，缓存越持久
# 不同类型的数据设置不同过期时间，能够避免缓存雪崩（大量数据同时过期）和热点数据频繁失效的问题
async def set_cached_categories(data: List[Dict[str, Any]], expire: int = 7200):
    return await set_cache(CATEGORIES_KEY, data, expire)

# 读取新闻列表缓存
async def get_cached_news_list(category_id: Optional[int], page: int, page_size: int):
    category_id = category_id if category_id is not None else "all"
    key = f"{NEWS_LIST_KEY_PREFIX}:{category_id}:{page}:{page_size}"
    return await get_cache_json(key)


# 写入新闻列表缓存 key = news_list:分类id:页码:每页数量 + 列表数据 + 过期时间
async def set_cached_news_list(category_id: Optional[int], page:int, page_size: int, data: List[Dict[str, Any]], expire: int = 600):
    category_id = category_id if category_id is not None else "all"
    key = f"{NEWS_LIST_KEY_PREFIX}:{category_id}:{page}:{page_size}"
    return await set_cache(key, data, expire)

# 读取新闻详情缓存
async def get_cached_news_detail(news_id: int):
    key = f"news_detail:{news_id}"
    return await get_cache_json(key)

# 写入新闻详情缓存
async def set_cached_news_detail(news_id: int, data: List[Dict[str, Any]], expire: int = 1800):
    key = f"news_detail:{news_id}"
    return await set_cache(key, data, expire)

# 读取相关新闻缓存
async def get_cached_related_news(news_id: int, expire: int = 600):
    key = f"related_news:{news_id}"
    return await get_cache_json(key)

# 写入相关新闻缓存
async def set_cached_related_news(news_id: int, data: List[Dict[str, Any]], expire: int = 600):
    key = f"related_news:{news_id}"
    return await set_cache(key, data, expire)