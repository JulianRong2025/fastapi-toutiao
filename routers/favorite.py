from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from config.db_config import get_db
from crud.favorite import add_favorite_news, check_news_favorite, remove_favorite_news
from models.users import User
from schemas.favorite import FavoriteAddRequest, FavoriteCheckRequest
from utils.auth import get_current_user
from utils.response import success_response
from starlette import status

router = APIRouter(prefix="/api/favorite", tags=["favorite"])

# 检查收藏状态
@router.get("/check")
async def check_favorite(
    news_id: int = Query(..., alias="newsId"),
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    is_favorite = await check_news_favorite(db, user.id, news_id)
    return success_response(message="检查收藏状态成功", data=FavoriteCheckRequest(isFavorite=is_favorite))

# 添加收藏
@router.post("/add")
async def add_favorite(
    data: FavoriteAddRequest,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    result = await add_favorite_news(db, user.id, data.news_id)
    return success_response(message="添加收藏成功", data=result)

# 取消收藏
@router.delete("/remove")
async def remove_favorite(
    news_id: int = Query(..., alias="newsId"),
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    is_remove_favorite = await remove_favorite_news(db, user.id, news_id)
    if not is_remove_favorite:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="收藏记录不存在")
    return success_response(message="取消收藏成功")