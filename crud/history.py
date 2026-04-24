from datetime import datetime, timezone
from turtle import update

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from models.history import History
from models.news import News


# 添加浏览历史
async def add_history_news(db: AsyncSession, user_id: int, news_id: int):
    # 检查是否浏览过当前新闻
    query = select(History).where(History.user_id == user_id, History.news_id == news_id)
    result = await db.execute(query)
    is_history = result.scalar_one_or_none()
    if is_history:
        is_history.view_time = datetime.now(timezone.utc)
        await db.commit()
        await db.refresh(is_history)
        return is_history
    else:
        new_history = History(user_id=user_id, news_id=news_id)
        db.add(new_history)
        await db.commit()
        await db.refresh(new_history)
        return new_history
    
# 获取浏览历史列表：某个用户的收藏列表 + 分页功能
async def get_all_history_list(db: AsyncSession, 
                           user_id: int, 
                           page: int, 
                           page_size: int
):
    count_query = select(func.count()).where(History.user_id == user_id)
    total = await db.execute(count_query)
    total_count = total.scalar_one()

    pick = (page - 1) * page_size
    
    query = select(News,
                   History.id.label("history_id"),
                   History.view_time
                ).join(History,
                        History.news_id == News.id
                    ).where(History.user_id == user_id
                    ).order_by(History.view_time.desc()
                    ).offset(pick
                    ).limit(page_size)
    result = await db.execute(query)
    rows = result.all()
    return rows, total_count
