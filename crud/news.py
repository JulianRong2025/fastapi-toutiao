from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession
from models.news import Category, News

async def get_categories(db: AsyncSession, skip: int = 0, limit: int = 100):
    stmt = select(Category).offset(skip).limit(limit)
    result = await db.execute(stmt)
    return result.scalars().all()

async def get_news_list(db: AsyncSession, category_id: int, skip: int = 0, limit: int = 10):
    # 查询指定分类下的新闻
    stmt = select(News).where(News.category_id == category_id).offset(skip).limit(limit)
    result = await db.execute(stmt)
    return result.scalars().all()

async def get_news_count(db: AsyncSession, category_id: int):
    # 查询指定分类下的新闻总数
    stmt = select(func.count(News.id)).where(News.category_id == category_id)
    result = await db.execute(stmt)
    return result.scalar_one()   
    # scalar_one() 只能有一个结果，如果没有结果或有多个结果会抛出异常
    # 数据库没问题可以用 scalars（）,scalars不会报错

async def get_news_detail(db: AsyncSession, news_id: int):
    # 查询指定新闻的详情
    stmt = select(News).where(News.id == news_id)
    result = await db.execute(stmt)
    return result.scalar_one_or_none()
