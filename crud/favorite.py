from sqlalchemy import delete, func, select
from sqlalchemy.ext.asyncio import AsyncSession

from models.favorite import Favorite
from models.news import News

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

# 获取收藏列表:某个用户，分页查询
async def get_favorite_list(db: AsyncSession, 
                            user_id: int, 
                            page: int = 1, 
                            page_size: int = 10
                            ):
    # 总量
    count_stmt = select(func.count(Favorite.id)).where(Favorite.user_id == user_id)  # 获取总量
    count_result = await db.execute(count_stmt)
    total = count_result.scalar_one()

    # 收藏的列表：联表查询 join + 收藏的时间排序 + 分页查询
    # join(联合查询的表， 联合查询的条件)
    # 别名 Favorite.id.label("favorite_id")
    query = select(
        News,
        Favorite.created_at.label("favorite_time"),
        Favorite.id.label("favorite_id")
        ).join(
            Favorite, 
            Favorite.news_id == News.id
        ).where(
        Favorite.user_id == user_id, 
        ).order_by(
            Favorite.created_at.desc()
        ).offset(
            (page - 1) * page_size
        ).limit(page_size)
    list_result = await db.execute(query)
    rows = list_result.all()
    # 这里 rows 的格式是：[(新闻对象，收藏时间，收藏 id), (新闻对象，收藏时间，收藏 id), ...]
    # 处理数据
    return rows, total
    