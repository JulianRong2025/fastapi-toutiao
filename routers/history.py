from fastapi import APIRouter, Depends

from crud.history import add_history_news
from models.users import User
from utils.auth import get_current_user
from utils.response import success_response
from config.db_config import get_db
from sqlalchemy.ext.asyncio import AsyncSession
from schemas.history import HistoryAddRequest


# 创建apirouter实例
# prefix: 路由前缀(根据 api 接口规范文档编写)，tags: 标签（分组）
router = APIRouter(prefix="/api/history", tags=["history"])

# 添加浏览历史
@router.post("/add")
async def add_history(
    data: HistoryAddRequest,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    result = await add_history_news(db, user.id, data.news_id)
    return success_response(message="添加成功", data=result)
