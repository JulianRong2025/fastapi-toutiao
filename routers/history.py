from fastapi import APIRouter, Depends, HTTPException, Query

from crud.history import add_history_news, clear_all_history_news, delete_history_news, get_all_history_list
from models.users import User
from utils.auth import get_current_user
from utils.response import success_response
from config.db_config import get_db
from sqlalchemy.ext.asyncio import AsyncSession
from schemas.history import HistoryAddRequest, HistoryListResponse, HistoryNewsItemResponse
from starlette import status

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
    return success_response(message="添加浏览记录成功", data=result)

# 获取浏览历史列表
@router.get("/list")
async def get_history_list(
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=100, alias="pageSize"),
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    rows, total_count = await get_all_history_list(db, user.id, page, page_size)
    history_list = [HistoryNewsItemResponse.model_validate({
        **news.__dict__,
        "history_id": history_id,
        "view_time": view_time
    }) for news, history_id, view_time in rows]
    has_more = page * page_size < total_count
    data = HistoryListResponse(list=history_list, total=total_count, hasMore=has_more)
    return success_response(data=data)

# 删除浏览历史记录
@router.delete("/delete/{history_id}")
async def delete_history(
    history_id: int,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    result = await delete_history_news(db, history_id, user.id)
    if not result:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="浏览历史记录不存在")
    return success_response(message="删除成功")

# 清空浏览历史记录
@router.delete("/clear")
async def clear_history(
    user: User = Depends (get_current_user),
    db: AsyncSession =Depends(get_db)):
    result = await clear_all_history_news(db, user.id)
    return success_response(message="清空成功")