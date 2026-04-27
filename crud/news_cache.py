from fastapi.encoders import jsonable_encoder
from sqlalchemy import func, select, update
from sqlalchemy.ext.asyncio import AsyncSession
from cache.news_cache import get_cached_categories, get_cached_news_detail, get_cached_news_list, get_cached_related_news, set_cached_categories, set_cached_news_detail, set_cached_news_list, set_cached_related_news
from models.news import Category, News
from schemas.base import NewsItemBase


# 查询有多少新闻分类
async def get_categories(db: AsyncSession, skip: int = 0, limit: int = 100):
    # 尝试从缓存中获取数据
    cached_categories = await get_cached_categories()
    if cached_categories is not None:
        return cached_categories
    # 如果缓存中没有数据，则从数据库中查询
    stmt = select(Category).offset(skip).limit(limit)
    result = await db.execute(stmt)
    categories = result.scalars().all()   # ORM
    # 将查询结果缓存
    if categories:
        # orm 不支持orm 格式的数据写入，需要把它转换成字典列表的格式
        categories = jsonable_encoder(categories)
        await set_cached_categories(categories)
    # fastapi 字典列表和 orm 对象都支持
    return categories


# 查询指定分类下的所有新闻列表
async def get_news_list(db: AsyncSession, category_id: int, skip: int = 0, limit: int = 10):
    # 计算页码
    page = skip // limit + 1
    # 尝试从缓存中获取数据
    cached_news_list = await get_cached_news_list(category_id, page, limit)
    if cached_news_list is not None:
        return cached_news_list
    # 如果缓存中没有数据，则从数据库中查询
    stmt = select(News).where(News.category_id == category_id).offset(skip).limit(limit)
    result = await db.execute(stmt)
    news_list =  result.scalars().all()
    # 将查询结果缓存
    if news_list:
        # 把 orm 数据转换为 字典列表格式
        # orm 转成 pydantic 模型，再转成字典列表格式
        news_data = [NewsItemBase.model_validate(item).model_dump(mode="json", by_alias=False) for item in news_list]
        # by_alias=False 不启用别名，因为 redis 数据只给后端使用
        # 这里也可以直接用news_data = jsonable_encoder(news_list)
        await set_cached_news_list(category_id, page, limit, news_data)
    return news_list


async def get_news_count(db: AsyncSession, category_id: int):
    # 查询指定分类下的新闻总数
    stmt = select(func.count(News.id)).where(News.category_id == category_id)
    result = await db.execute(stmt)
    return result.scalar_one()   
    # scalar_one() 只能有一个结果，如果没有结果或有多个结果会抛出异常
    # 数据库没问题可以用 scalars（）,scalars不会报错


# 查询指定新闻的详情
async def get_news_detail(db: AsyncSession, news_id: int):
    # 尝试从缓存中读取新闻详情
    cached_news_detail = await get_cached_news_detail(news_id)
    if cached_news_detail is not None:
        return cached_news_detail
    # 如果缓存中没有数据，则从数据库中查询
    stmt = select(News).where(News.id == news_id)
    result = await db.execute(stmt)
    news_detail =  result.scalar_one_or_none()
    # 将查询结果缓存
    if news_detail:
        news_detail_data = jsonable_encoder(news_detail)
        await set_cached_news_detail(news_id, news_detail_data)
    return news_detail


async def increase_news_views(db: AsyncSession, news_id: int):
    # 浏览量+1
    stmt = update(News).where(News.id == news_id).values(views=News.views + 1)
    result = await db.execute(stmt)
    await db.commit()

    # 更新操作后，要检查数据库是否真的命中的数据，命中了返回 true
    return result.rowcount > 0 # 返回受影响的行数


# 获取相关新闻
async def get_related_news(db: AsyncSession, category_id: int, news_id: int, limit: int = 5):
    # 尝试从缓存中读取相关新闻
    cached_related_news = await get_cached_related_news(news_id)
    if cached_related_news is not None:
        return cached_related_news
    
    # 如果缓存中没有数据，则从数据库中查询
    # order_by 排序：浏览量和发布时间
    stmt = select(News).where(
        News.category_id == category_id, 
        News.id != news_id
        ).order_by(
            News.views.desc(),
            News.publish_time.desc()
        ).limit(
            limit
            )
    result = await db.execute(stmt) 
    related_news = result.scalars().all()
    # 用列表推导式把 News 对象转换成字典，前端需要的字段
    related_news_json = [{
        "id": news.id,
        "title": news.title,
        "content": news.content,
        "image": news.image,
        "author": news.author,
        "publishTime": news.publish_time,
        "category_id": news.category_id,
        "views": news.views
        } for news in related_news]
    # 统一转换为可 JSON 序列化的数据，避免 datetime 写入 Redis 失败
    related_news_json = jsonable_encoder(related_news_json)
    # 将查询结果缓存
    if related_news_json:
        await set_cached_related_news(news_id, related_news_json)
    return related_news_json