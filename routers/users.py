from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from config.db_config import get_db
from schemas.users import UserRequest
from crud.users import get_user_by_username, create_user
from starlette import status

# 创建apirouter实例
# prefix: 路由前缀(根据 api 接口规范文档编写)，tags: 标签（分组）
router = APIRouter(prefix="/api/users", tags=["users"])


@router.post("/register")
async def register(user_data: UserRequest, db: AsyncSession = Depends(get_db)):
    # 注册逻辑：验证用户是否存在，创建用户，生成令牌
    existing_user = await get_user_by_username(user_data.username, db)  # 查询用户是否存在
    if existing_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="用户已存在")
    new_user = await create_user(user_data, db)
    return {
        "code": 200,
        "message": "注册成功",
        "data": {
            "token": "用户访问令牌",
            "userInfo": {
                "id": new_user.id,
                "username": new_user.username,
                "bio": new_user.bio,
                "avatar": new_user.avatar
            }
        }
    }