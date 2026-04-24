from datetime import datetime, timezone
from turtle import update

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from models.history import History


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
    