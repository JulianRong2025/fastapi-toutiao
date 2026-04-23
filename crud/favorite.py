from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession

from models.favorite import Favorite

# 检查当前用户是否收藏了某条新闻
async def check_news_favorite(db: AsyncSession, user_id: int, news_id: int):
    stmt = select(Favorite).where(Favorite.user_id == user_id, Favorite.news_id == news_id)
    result = await db.execute(stmt)
    favorite = result.scalar_one_or_none()
    return favorite is not None

# 添加收藏
async def add_favorite_news(db: AsyncSession, user_id: int, news_id: int):
    new_favorite = Favorite(user_id=user_id, news_id=news_id)
    db.add(new_favorite)
    await db.commit()
    await db.refresh(new_favorite)
    return new_favorite

# 取消收藏
async def remove_favorite_news(db: AsyncSession, user_id: int, news_id: int):
    stmt = delete(Favorite).where(Favorite.user_id == user_id, Favorite.news_id == news_id)
    result = await db.execute(stmt)
    await db.commit()
    # 检查更新
    return result.rowcount > 0